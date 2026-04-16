"""Frame difference implementation of the MotionDetectorService."""


import time
from dataclasses import dataclass

import cv2
import numpy as np
from cv2.typing import MatLike

from app.core.cameras.camera import Camera


@dataclass
class CV2FrameDifferenceDetectorService:
    """Detection service that uses frame difference to detect motion."""

    camera: Camera

    def __compute_mask(
        self,
        frame1: MatLike,
        frame2: MatLike,
        kernel: np.ndarray[tuple[int, int], np.dtype[np.uint8]],
    ) -> MatLike:
        """Creates a mask from the difference between 2 frames.

        Techniques like blurring and morphological operations are used to
        improve the accuracy

        Args:
            frame1: The first frame (assumed grayscale).
            frame2: The second frame (assumed grayscale).
            kernel: The kernel to use for morphological operations. Shape must
                be square.

        Returns:
            The mask.
        """
        # Ensure the kernel shape is square so the blurring is correct
        if kernel.shape[0] != kernel.shape[1]:
            raise ValueError("Kernel must be square")
        kernel_size: int = kernel.shape[0]

        # Blur the frame before generating the mask
        blurred_frame = cv2.medianBlur(
            cv2.subtract(frame1, frame2), kernel_size
        )
        mask = cv2.adaptiveThreshold(
            blurred_frame,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY_INV,
            blockSize=11,
            C=kernel_size,
        )

        # Apply blur and morphological operations to improve accuracy
        return cv2.morphologyEx(
            cv2.medianBlur(mask, kernel_size),
            cv2.MORPH_CLOSE,
            kernel,
            iterations=1
        )


    def detect_motion(self, delta_ms: int = 1000) -> bool:
        """Detects motion in the camera feed.

        Args:
            delta_ms: The time in milliseconds to wait between the 2 frames.

        Returns:
            True if motion is detected, False otherwise.
        """
        # Capture and convert 2 images to grayscale
        img1 = cv2.cvtColor(self.camera.capture_frame(), cv2.COLOR_RGB2GRAY)
        time.sleep(delta_ms // 1000)
        img2 = cv2.cvtColor(self.camera.capture_frame(), cv2.COLOR_RGB2GRAY)

        # Create a mask from the difference between the 2 images
        kernel = np.array((9, 9), dtype=np.uint8)
        mask = self.__compute_mask(img1, img2, kernel)

        # The mask will only have non-zero pixels where motion was detected
        return cv2.countNonZero(mask) > 0
