#!/usr/bin/env python
"""Main app"""
import locale
import calendar
from importlib import import_module
import os
from flask import Flask, render_template, Response, request, flash
from flask_wtf import FlaskForm
from wtforms import (BooleanField, FileField, widgets, TimeField,
                     SubmitField, SelectMultipleField)
from wtforms.validators import DataRequired
from wtforms.fields.html5 import IntegerField
import configtest
from timelapse import TimeLapse

# import camera driver
if os.environ.get('CAMERA'):
    print(os.environ.get('CAMERA'))
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from camera import Camera

app = Flask(__name__)

timelapse = TimeLapse(Camera(), configtest)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dumb_key'


app.config.from_object(Config)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class TimelapseForm(FlaskForm):
    locale.setlocale(locale.LC_ALL, '')

    # config = timelapse.conf
    # print(f'config: {config}')
    stream = BooleanField('Streaming')
    # print(stream)
    interval = IntegerField(default=timelapse.conf.interval,
                            validators=[DataRequired()])
    # print(interval)
    timeset = BooleanField('Jours de la semaine',
                           default=timelapse.conf.timeset)
    # print(timeset)

    daysfields = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    dayslabels = [(d, calendar.day_name[i]) for i, d in enumerate(daysfields)]
    days = MultiCheckboxField('Label', choices=dayslabels)
    # print(days)

    start = TimeField('De : ')
    # print(start)
    end = TimeField('à : ')
    # print(end)
    submit = SubmitField('Enregistrer')
    # print(submit)
    # path = FileField('Répertoire :', default=timelapse.conf.path)
    # print(path)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    print("index")
    form = TimelapseForm()
    if request.method == 'POST':
        for field in form:
            print(f'{field.name}')
            if field.name in timelapse.conf.keys():
                timelapse.conf[field.name] = field.data
                print(f'{field.name}({type(field.data)}) = {field.data}')
    else:
        print('Not validated')
    return render_template('index.html', form=form)


def gen(camera):
    """Video streaming generator function."""
    print("gen")
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed(video=True):
    """Video streaming route. Put this in the src attribute of an img tag."""
    print("video_feed")
    if video:
        cam = Camera()
        cam.perm_stream()
        return Response(gen(cam),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        cam.perm_stream()
        # return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

