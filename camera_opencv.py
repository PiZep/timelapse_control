"""camera_opencv"""
import os
import cv2
# from stream_camera import BaseStreamCamera
from stream_camera import BaseCamera


class Camera(BaseCamera):
    """Camera class implementing the streaming base class"""
    video_source = 0
    # stream = None

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super().__init__()

    # @classmethod
    def permstream(self):
        self.stream()

    @staticmethod
    def set_video_source(source):
        """Set video source"""
        Camera.video_source = source

    @staticmethod
    def frames():
        """See BaseCamera"""
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

    @staticmethod
    def take_picture(fullname, res):
        """Method to take a single picture"""
        camera = cv2.VideoCapture(Camera.video_source)
        camera.set(3, res[0])
        camera.set(4, res[1])

        camera.open(Camera.video_source)
        if not Camera.isOpened():
            raise RuntimeError('Could not start camera.')

        _, pic = camera.read()
        cv2.imwrite(fullname, pic)
        camera.release()
        return cv2.imencode('.jpg', pic)[1].tobytes()

