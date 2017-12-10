import picamera

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.start_recording('launch-video.h264')
camera.wait_recording(300)
camera.stop_recording()