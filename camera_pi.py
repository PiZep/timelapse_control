"""camera_pi"""
import io
import time
import picamera
from stream_camera import BaseCamera


class Camera(BaseCamera):
    """Camera class for pi camera"""
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)

            camera.resolution = (640, 480)
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                               use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

    @staticmethod
    def take_picture(fullname, res):
        camera = picamera.PiCamera(resolution=res)
        # let camera warm up
        time.sleep(2)
        # camera.start_preview()
        camera.resolution = res

        camera.capture(fullname)
        camera.close()

