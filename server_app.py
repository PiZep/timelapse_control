#!/usr/bin/env python
"""Main app"""
import locale
import logging
import calendar
from datetime import time
from importlib import import_module
import os
from flask import (Flask,
                   render_template,
                   Response,
                   request,
                   send_file)
from flask_wtf import FlaskForm
from wtforms import (BooleanField,
                     widgets,
                     SubmitField,
                     SelectMultipleField)
from wtforms.validators import DataRequired
from wtforms.fields.html5 import IntegerField
                                  # TimeField)
from wtforms_components import TimeField
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
    stream = BooleanField('Streaming')
    interval = IntegerField(default=timelapse.conf.interval,
                            validators=[DataRequired()])
    timeset = BooleanField('Jours de la semaine',
                           default=timelapse.conf.timeset)

    daysfields = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    dayslabels = [(d, calendar.day_name[i]) for i, d in enumerate(daysfields)]
    days = MultiCheckboxField('Label', choices=dayslabels)

    start = TimeField('De : ', format='%H:%M')
    end = TimeField('à : ', format='%H:%M')
    submit = SubmitField('Enregistrer')
    # path = FileField('Répertoire :', default=timelapse.conf.path)
    # print(path)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.start.data:
            self.start.data = \
               time(hour=timelapse.conf.start['hour'],
                    minute=timelapse.conf.start['minute'])
        if not self.end.data:
            self.end.data = time(hour=timelapse.conf.end['hour'],
                                 minute=timelapse.conf.end['minute'])


# class ToggleStream(FlaskForm):
#     """
#     Checkbox switch for streaming
#     """
#     stream = BooleanField('Streaming')


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    app.logger.info("index function launched")
    form = TimelapseForm()
    togglestream = form.stream
    app.logger.info(f'index.togglestream.data: {togglestream.data}')

    app.logger.debug(f'{form.errors}')
    if request.method == 'GET':
        togglestream = form.stream
        app.logger.debug(f'index.{request.method} -> '
                         f'togglestream.data: {togglestream.data}')
        app.logger.debug(f'index.{request.method} -> errors -> {form.errors}')

        video_feed(togglestream)
        return render_template('index.html', form=form)

    if form.validate_on_submit():
        app.logger.info('index.form validated')
        for field in form:
            app.logger.debug(f'index.form: {field.name} ='
                             f' {field.data} ({type(field.data)})')
            if field.name == 'start' or field.name == 'end':
                timelapse.conf[field.name]['hour'] = 0  # params.hour
                timelapse.conf[field.name]['minute'] = 0  # params.minute
            elif field.name in timelapse.conf.keys():
                timelapse.conf[field.name] = field.data
            elif field.name == 'stream':
                video_feed(field)
            else:
                continue
        timelapse.save()
        return render_template('index.html', form=form)
    else:
        app.logger.info(f'index.form not validated -> {form.errors}')
        return render_template('index.html', form=form)

    return render_template('index.html', form=form)


def gen(camera):
    """Video streaming generator function."""
    app.logger.debug("gen")
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed(video=None):
    """Video streaming route. Put this in the src attribute of an img tag."""
    # video = togglestream.data if togglestream else False
    if video:
        app.logger.debug(f'video_feed -> video: {video}')

    # resp = Response(mimetype='multipart/x-mixed-replace; boundary=frame')
        if video.data:
            if not timelapse.camera.thread:
                timelapse.camera.perm_stream()
        else:
            timelapse.camera.perm_stream()
        return Response(gen(timelapse.camera),
                        mimetype='multipart/x-mixed-replace;'
                        'boundary=frame')

    else:
        name = (timelapse.conf.lastpic if timelapse.conf.lastpic
                else timelapse.take_picture())

        # return send_file(timelapse.conf.lastpic,
        #                  attachment_filename=name,
        #                  mimetype="image/jpeg")
        return Response(name,
                        mimetype='multipart/x-mixed-replace;'
                        'boundary=frame')


# @app.route('/lastpic')
# def last_pic():
#     app.logger.debug("last_pic")
#     if timelapse.camera.thread:
#         timelapse.perm_stream()
#     return timelapse.last_pic


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

