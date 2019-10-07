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
                   request)
from flask_wtf import FlaskForm
from wtforms import (BooleanField,
                     widgets,
                     SubmitField,
                     SelectField,
                     SelectMultipleField)
from wtforms.validators import DataRequired
from wtforms.fields.html5 import (IntegerField,
                                  TimeField)
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
    timelapse_on = BooleanField('Time Lapse',
                                default=timelapse.conf.timelapse_on)
    interval = IntegerField(default=timelapse.conf.interval,
                            validators=[DataRequired()])
    timeset = BooleanField('Jours de la semaine',
                           default=timelapse.conf.timeset)

    daysfields = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    dayslabels = [(d, calendar.day_name[i]) for i, d in enumerate(daysfields)]
    days = MultiCheckboxField('Label', choices=dayslabels)

    start = TimeField('De : ', format='%H:%M')
    end = TimeField('à : ', format='%H:%M')
    res = SelectField('Résolution')
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
        if not self.res.choices:
            self.res.choices = [('240p', '320x240'),
                                ('480p', '640x480'),
                                ('600p', '800x600'),
                                ('720p', '1280x720'),
                                ('1080p', '1920x1080'),
                                ('1440p', '2560x1440'),
                                ('2160p', '3840x2160')]
            self.res.data = self._get_name_from_res(timelapse.conf.res)

    @staticmethod
    def _get_res_from_name(resname):
        res = (0, 0)
        if resname == '240p':
            res = [320, 240]
        if resname == '480p':
            res = [640, 480]
        if resname == '600p':
            res = [800, 600]
        if resname == '720p':
            res = [1280, 720]
        if resname == '1080p':
            res = [1920, 1080]
        if resname == '1440p':
            res = [2560, 1440]
        if resname == '2160p':
            res = [3840, 2160]
        return res

    @staticmethod
    def _get_name_from_res(res):
        name = '240p'
        if res == (320, 240):
            name = '240p'
        if res == (640, 480):
            name = '480p'
        if res == (800, 600):
            name = '600p'
        if res == (1280, 720):
            name = '720p'
        if res == (1920, 1080):
            name = '1080p'
        if res == (2560, 1440):
            name = '1440p'
        if res == (3840, 2160):
            name = '2160p'
        return name


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    app.logger.info("index function launched")
    form = TimelapseForm()
    timelapse_on = form.timelapse_on
    app.logger.info(f'index.togglestream.data: {timelapse_on.data}')

    app.logger.debug(f'{form.errors}')
    if request.method == 'GET':
        timelapse_on = form.timelapse_on
        app.logger.debug(f'index.{request.method} -> '
                         f'timelapse_on.data: {timelapse_on.data}')
        app.logger.debug(f'index.{request.method} -> errors -> {form.errors}')

    if form.validate_on_submit():
        app.logger.info('index.form validated')
        for field in form:
            if field.name == 'start' or field.name == 'end':
                timelapse.conf[field.name]['hour'] = 0  # params.hour
                timelapse.conf[field.name]['minute'] = 0  # params.minute
            elif field.name in timelapse.conf.keys():
                timelapse.conf[field.name] = field.data
            elif field.name == 'res':
                timelapse.conf[field.name] = \
                    form._get_res_from_name(field.data)
            else:
                continue
            app.logger.debug(f'index.form: {field.name} ='
                             f' {field.data} ({timelapse.conf[field.name]})')
        timelapse.save()

    else:
        app.logger.info(f'index.form not validated -> {form.errors}')

    return render_template('index.html', form=form)


def gen(camera):
    """Video streaming generator function."""
    app.logger.debug("gen")
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # video = togglestream.data if togglestream else False
    app.logger.info(f'video_feed')

    # resp = Response(mimetype='multipart/x-mixed-replace; boundary=frame')
    if not timelapse.camera.thread:
        timelapse.camera.perm_stream()
    return Response(gen(timelapse.camera),
                    mimetype='multipart/x-mixed-replace;'
                    'boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

