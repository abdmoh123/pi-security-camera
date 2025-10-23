from picamera2 import Picamera2


picam2 = Picamera2()


# start recording a video for 5s and save it to the given path
picam2.start_and_record_video("test_video.mp4", duration=5)
