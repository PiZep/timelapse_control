"""stream_camera

This file is based on Miguel Grinberg work:
https://github.com/miguelgrinberg/flask-video-streaming

"""
import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class StopableThread(threading.Thread):
    """Thread with a stop() method. Based upon:
    https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread/325528#325528"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stopevent = threading.Event()

    def stop(self):
        self._stopevent.set()

    def stopped(self):
        return self._stopevent.is_set()


class CameraEvent():
    """An Event-like class that signals all active clients when a new frame is
    available.
    """

    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera():
    """Super class used by camera_pi and camera_opencv"""
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()

    def __init__(self, video=False):
        if video:
            self.perm_stream()

    def perm_stream(self):
        """Start or stop the streaming thread"""
        if BaseCamera.thread is None:
            # start background frame thread
            BaseCamera.thread = StopableThread(target=self._thread)
            BaseCamera.thread.start()
            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)
        else:
            BaseCamera.thread.stop()

    def get_frame(self):
        """Return the current camera frame."""
        self.last_access = time.time()

        # wait for a signal from the camera thread
        self.event.wait()
        self.event.clear()

        return self.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise NotImplementedError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            # if time.time() - BaseCamera.last_access > 10:
            #     frames_iterator.close()
            #     print('Stopping camera thread due to inactivity.')
            #     break
            if BaseCamera.thread.stopped():
                frames_iterator.close()
                print('Stopping camera thread on demand.')
                break

        BaseCamera.thread = None

