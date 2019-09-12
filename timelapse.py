#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
import os
# import threading
# from camera_opencv import Camera
from datetime import datetime, timedelta
import time
from config import *
import tlconfig

# camera = Camera()


class TimeLapse():
    """Main TimeLapse class"""

    def __init__(self, camera):
        self.camera = camera
        self.config = tlconfig.get_config()
        self.last_pic = None
        self.last_shot = None
        self._count = 0

    def take_picture(self, name_fun, *args, **kwargs):
        """Take a picture"""
        print("take_picture")
        self._count += 1
        if name_fun:
            name = name_fun(*args, **kwargs)
        else:
            name = str(self._count) + ".jpg"
        pic_full_path = os.path.sep.join((PATH, name))
        print(pic_full_path)
        self.camera.take_picture(pic_full_path, CAM_RES)
        return name

    def delay(self):
        """Calculate the delay in second before the next picture"""

        print("delay")
        next_pic = datetime.fromtimestamp(self.last_shot + INTERVAL)

        forecast = timedelta(hours=next_pic.hour,
                             minutes=next_pic.minute).total_seconds()
        limit = timedelta(hours=tlconfig.END_HOUR,
                          minutes=tlconfig.END_MIN).total_seconds()

        # Calculate next day if the next forecast picture
        # is taken after the limit hour
        week_day = next_pic.weekday()
        d_days = 0
        if forecast > limit:
            d_days += 1
            while not DAYS[week_day]:
                week_day = week_day + 1 if week_day < 6 else 0
                d_days += 1

            next_pic = datetime(year=self.last_shot.year, month=next_pic.month,
                                day=self.last_shot.day + d_days,
                                hour=tlconfig.START['hour'],
                                minute=tlconfig.START['minute'])

        delay = next_pic - datetime.now()

        print(d_days, delay.total_seconds(), self.last_shot, next_pic)
        return delay.total_seconds()

    def timelapse(self, name_func, *args, **kwargs):
        """Set timelapse"""
        print("timelapse")
        while True:
            self.last_shot = time.time()
            self.last_pic = self.take_picture(name_func, *args, **kwargs)
            if TIMESET:
                time.sleep(self.delay())
            else:
                time.sleep(INTERVAL - self.last_shot)
            return self.last_shot

