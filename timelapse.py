#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
import os
# import threading
# from camera_opencv import Camera
from datetime import datetime, timedelta
import time
import tlconfig

# camera = Camera()

# Configuration constants

TIMESET = tlconfig.TIMESET
CAM_RES = tlconfig.CAM_RES
INTERVAL = tlconfig.INTERVAL
PATH = tlconfig.PATH
DAYS = tlconfig.DAYS
START_HOUR = tlconfig.START_HOUR
START_MIN = tlconfig.START_MIN
END_HOUR = tlconfig.END_HOUR
END_MIN = tlconfig.END_MIN
LAST_PIC = tlconfig.LAST


class TimeLapse(object):
    """"""

    def __init__(self, camera):
        camera
        self.camera = camera
        self.config = tlconfig
        self.last_pic = None
        self.last_shot = None
        self._count = 0

    def name_picture(self):
        """Set and return the name of a picture"""
        print("name_picture")
        return tlconfig.PATH

    def take_picture(self, name_fun=None, *args, **kwargs):
        """Take a picture"""
        print("take_picture")
        self._count += 1
        if name_fun:
            name = name_fun(*args, **kwargs)
        else:
            name = self._count
        pic_full_path = os.path.sep.join((PATH, name))
        print(pic_full_path)
        self.camera.take_picture(pic_full_path, CAM_RES)
        return name

    def daysset():
        """Check that every days are set the same

        All values True or False means every day is set
        """
        print("daysset")
        return DAYS[1:] == DAYS[:-1]

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
            if not self.alldays:
                while not DAYS[week_day]:
                    week_day = week_day + 1 if week_day < 6 else 0
                    d_days += 1

            next_pic = datetime(year=self.last_shot.year, month=next_pic.month,
                                day=self.last_shot.day + d_days,
                                hour=tlconfig.START_HOUR,
                                minute=tlconfig.START_MIN)

        delay = next_pic - datetime.now()

        print(d_days, delay.total_seconds(), self.last_shot, next_pic)
        return delay.total_seconds()

    def timelapse(self):
        """Set timelapse"""
        print("timelapse")
        while True:
            self.last_shot = time.time()
            self.last_pic = self.take_picture()
            if TIMESET:
                time.sleep(self.delay())
            else:
                time.sleep(INTERVAL - time.time() - self.last_shot)

