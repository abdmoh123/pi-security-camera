from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

# create an example test config for previewing
camera_config = picam2.create_preview_configuration()
# set the config of the camera to use the one above
picam2.configure(camera_config)

# start the preview window using QT as backend
picam2.start_preview(Preview.QTGL)
# start the camera (begin recording)
picam2.start()

# wait for 2 seconds
time.sleep(2)

# take a picture and save it to the following path
picam2.capture_file("test_photo.jpg")
