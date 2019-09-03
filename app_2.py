#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
from datetime import datetime, timedelta
import time
from importlib import import_module
import os
import socket
# import cv2
# import threading
from flask import Flask, render_template, Response
import tlconfig

# import camera driver
if os.environ.get('CAMERA'):
    StreamCamera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera
# camera = Camera()


app = Flask(__name__)
cam = StreamCamera()
last_pic = None


@app.route('/')
def index():
    """Home and only page"""
    return render_template('index.html')


def gen(camera, video=True):
    """Video generator, stream for video True"""
    while video:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Types: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put it in the src attribute of an <img>"""
    return Response(gen(StreamCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def take_picture():
    """Take a picture"""
    pic_full_path = (tlconfig.PATH + socket.gethostname() +
                     datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.jpg')
    print(pic_full_path)
    res = tlconfig.CAM_RES
    cam.take_picture(pic_full_path, res)


def daysset():
    """Check that every days are set the same

    All values True or False means every day is set
    """
    return tlconfig.DAYS[1:] == tlconfig.DAYS[:-1]


def delay(self):
    """Calculate the delay in second before the next picture"""

    next_pic = datetime.fromtimestamp(last_pic + tlconfig.INTERVAL)

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
            while not tlconfig.DAYS[week_day]:
                week_day = week_day + 1 if week_day < 6 else 0
                d_days += 1

        next_pic = datetime(year=last_pic.year, month=next_pic.month,
                            day=last_pic.day + d_days,
                            hour=tlconfig.START_HOUR,
                            minute=tlconfig.START_MIN)

    delay = next_pic - datetime.now()

    print(d_days, delay.total_seconds(), last_pic, next_pic)
    return delay.total_seconds()


def run_timelapse():
    """Set timelapse"""
    global last_pic
    while True:
        last_pic = time.time()
        take_picture()
        if tlconfig.TIMESET:
            time.sleep(delay())
        else:
            time.sleep(tlconfig.INTERVAL - time.time() - last_pic)

