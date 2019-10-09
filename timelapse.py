#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
import os
import logging
import threading
# from camera_opencv import Camera
from datetime import datetime, timedelta
import time
from configmodule import ConfigJSON

# camera = Camera()

MAX_PIC = 1000
MAX_DIR = 10
MAIN_DIR = "timelapse"


class TimeLapse(ConfigJSON):
    """Main TimeLapse class"""

    def __init__(self, camera, config=None, naming_func=None, **kwargs):
        super().__init__(config)
        self.logger = logging.getLogger('server_app.timelapse.Timelapse')
        self.camera = camera
        self.naming = naming_func
        self.naming_args = kwargs
        self.last_shot = None
        self._count = 0
        self.started = False

        self.logger.debug('__init__')

    def take_picture(self, name_fun=None, **kwargs):
        """Take a picture"""
        self._set_path()
        self.logger.debug('take_picture')
        self._count += 1
        if name_fun:
            name = name_fun(**kwargs)
        else:
            name = self._default_naming()
        pic_full_path = os.path.sep.join((self.conf.path, name))
        print(pic_full_path)
        self.camera.take_picture(pic_full_path, self.conf.res)
        self.conf.lastpic = pic_full_path
        self.save()
        self.logger.info('%s', name)
        return name

    def delay(self):
        """Calculate the delay in second before the next picture"""

        self.logger.debug('delay')
        next_pic = datetime.fromtimestamp(self.last_shot + self.conf.interval)

        forecast = timedelta(hours=next_pic.hour,
                             minutes=next_pic.minute).total_seconds()
        limit = timedelta(hours=self.conf.end.hour,
                          minutes=self.conf.end.minute).total_seconds()

        # Calculate next day if the next forecast picture
        # is taken after the limit hour
        week_day = next_pic.weekday()
        d_days = 0
        if forecast > limit:
            d_days += 1
            while not self.conf.days[week_day]:
                week_day = week_day + 1 if week_day < 6 else 0
                d_days += 1

            next_pic = datetime(year=self.last_shot.year, month=next_pic.month,
                                day=self.last_shot.day + d_days,
                                hour=self.conf.start.hour,
                                minute=self.conf.start.minute)

        delay = next_pic - datetime.now()

        print(d_days, delay.total_seconds(), self.last_shot, next_pic)
        return delay.total_seconds()

    def cycle(self):
        """Set timelapse"""
        self.logger.debug('timelapse')
        self._set_path()
        self.started = True
        while True:
            pstart = time.time()
            self.take_picture(self.naming, **self.naming_args)
            self.last_shot = time.time()
            print(f"pic time: {self.last_shot},"
                  f"method pstart: {pstart}, delay: {self.last_shot - pstart}")
            if self.conf.timeset:
                delay = self.delay()
            else:
                delay = float(self.conf.interval) - self.last_shot + pstart
            delay = delay if delay >= 0 else 0
            time.sleep(delay)
            yield self.last_shot

    def _set_path(self):
        """Verify or make the required directories"""
        self.logger.debug('_set_path')
        path = os.path.join(self.conf.path, MAIN_DIR)
        if not os.access(path, os.F_OK):
            os.mkdir(MAIN_DIR)

    def _default_naming(self):
        """Default naming function

        Register with a numbering system, creating directories on the
        same principle. 1000 pictures is the maximum number by directory.
        The maximum number of directories is 10.
        """

        self.logger.debug('_default_naming')
        for d in range(1, MAX_DIR + 1):
            count = 1
            dir_name = os.path.join(MAIN_DIR, str(d).zfill(2))
            if not os.access(dir_name, os.F_OK):
                print(f"Making a new directory: {str(d).zfill(2)}")
                os.mkdir(dir_name)
                break
            else:
                abs_path = os.path.abspath(dir_name)
                count = len([f for f in os.listdir(dir_name)
                             if os.path.isfile(os.path.join(abs_path, f))
                             ]) + 1
                if not count >= MAX_PIC:
                    print(f"Saving new pic:"
                          f"{str(d).zfill(2) +'_' + str(count).zfill(3)}")
                    break

        name = os.path.join(dir_name, '_'.join((str(d).zfill(2),
                                                str(count).zfill(3))))
        self._count += self._count
        return name + ".jpg"

    # def launch_timelapse(self, camera_status):
    #     thread = threading.Thread(target=video_feed)
    #     thread.start()
    #     camera_status.wait()
    #     if self.conf.timelapse_on:
    #         for t in self.timelapse():
    #             self.logger.info(t)

