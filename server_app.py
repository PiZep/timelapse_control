#!/usr/bin/env python
"""Main app"""
import locale
import logging
import calendar
from importlib import import_module
import os
from flask import (Flask,
                   render_template,
                   Response,
                   request,
                   send_file,
                   flash)
from flask_wtf import FlaskForm
from wtforms import (BooleanField,
                     widgets,
                     TimeField,
                     SubmitField,
                     SelectMultipleField)
from wtforms.validators import DataRequired
from wtforms.fields.html5 import IntegerField
import configtest
from timelapse import TimeLapse

app = Flask(__name__)

format = "%(asctime)s -> %(name)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,
                    datefmt='%H:%M:%S')
# import camera driver
if os.environ.get('CAMERA'):
    app.logger.info(os.environ.get('CAMERA'))
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    import camera_pi as Camera

app.logger.info('going to init Camera()')
cam = Camera()

app.logger.info('going to init TimeLapse()')
timelapse = TimeLapse(cam, configtest)
app.logger.info(timelapse.conf)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dumb_key'


app.config.from_object(Config)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class TimelapseForm(FlaskForm):
    """
    Timelapse webform fields
    """
    locale.setlocale(locale.LC_ALL, '')

    app.logger.debug(f'config: {timelapse.conf}')
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


class ToggleStream:
    stream = BooleanField('Streaming')


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    app.logger.info("index function launched")
    form = TimelapseForm()
    if request.method == 'POST':
        for field in form:
            app.logger.debug(f'{field.name}')
            if field.name in timelapse.conf.keys():
                timelapse.conf[field.name] = field.data
                app.logger.debug(f'{field.name}({type(field.data)})'
                                 f' = {field.data}')
    else:
        app.logger.debug('Not validated')
    if form.validate_on_submit():
        timelapse.save()
    return render_template('index.html', form=form)


def gen(camera):
    """Video streaming generator function."""
    app.logger.debug("gen")
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    togglestream = ToggleStream()
    video = togglestream.stream.data if request.method == 'POST' else False
    app.logger.debug(f"video_feed, video = {video}")

    if video:
        if not timelapse.camera.thread:
            timelapse.camera.perm_stream()
            # return None
        return Response(gen(timelapse.camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        if timelapse.camera.thread:
            timelapse.camera.perm_stream()
        if not timelapse.last_pic:
            name = timelapse.take_picture()
        return send_file(timelapse.last_pic, attachment_filename=name,
                         mimetype="image/jpeg")


@app.route('/last_pic')
def last_pic():
    app.logger.debug("last_pic")
    if timelapse.camera.thread:
        timelapse.perm_stream()
    return timelapse.last_pic


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

