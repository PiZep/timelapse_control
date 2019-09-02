"""camera_opencv"""
import os
import cv2
from stream_camera import BaseStreamCamera


class Camera():
    """Camera class implementing the streaming base class"""
    video_source = 0
    camera = None
    stream = None

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        self.camera = cv2.VideoCapture(self.video_source)

    @staticmethod
    def stream():
        stream = BaseStreamCamera()
        return stream

    @staticmethod
    def set_video_source(source):
        """Set video source"""
        Camera.video_source = source

    @staticmethod
    def frames():
        """See BaseCamera"""
        Camera.camera = cv2.VideoCapture(Camera.video_source)
        if not Camera.camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = Camera.camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

    @staticmethod
    def take_picture(fullname, res):
        """Method to take a single picture"""
        Camera.camera.set(3, res[0])
        Camera.camera.set(4, res[1])

        Camera.camera.open(Camera.video_source)
        if not Camera.camera.isOpened():
            raise RuntimeError('Could not start camera.')

        _, pic = Camera.camera.read()
        cv2.imwrite(fullname, pic)
        Camera.camera.release()
        return cv2.imencode('.jpg', pic)[1].tobytes()

