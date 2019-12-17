#!/usr/bin/env python
"""Flask forms"""
import calendar
from datetime import time
import logging
from wtforms import (BooleanField,
                     widgets,
                     SubmitField,
                     SelectField,
                     SelectMultipleField)
from wtforms.validators import DataRequired
from wtforms.fields.html5 import (IntegerField,
                                  TimeField)
from flask_wtf import FlaskForm  # , CsrfProtect


class MultiCheckboxField(SelectMultipleField):
    """
    Multiple checkbox form
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class TimelapseForm(FlaskForm):
    """
    Timelapse webform fields
    """
    resolutions = [('240p', '320x240'),
                   ('480p', '640x480'),
                   ('600p', '800x600'),
                   ('720p', '1280x720'),
                   ('1080p', '1920x1080'),
                   ('1440p', '2560x1440'),
                   ('2160p', '3840x2160')]

    daysfields = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    daysnames = [calendar.day_name[i] for i, _ in enumerate(daysfields)]

    timelapse_on = BooleanField('Time Lapse')
    interval = IntegerField(validators=[DataRequired()])
    timeset = BooleanField('Jours de la semaine')

    dayslabels = list(zip(daysfields, daysnames))
    days = MultiCheckboxField('Label', choices=dayslabels)

    start = TimeField('De : ', format='%H:%M')
    end = TimeField('à : ', format='%H:%M')
    res = SelectField('Résolution', choices=resolutions)
    submit = SubmitField('Enregistrer')
    # path = FileField('Répertoire :', default=timelapse.conf.path)
    # print(path)

    def __init__(self, conf, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.res.default = self.get_name_from_res(conf.res)
        self.process()
        self.timelapse_on.data = conf.timelapse_on
        self.start.data = \
            time(hour=conf.start['hour'],
                 minute=conf.start['minute'])
        self.end.data = time(hour=conf.end['hour'],
                             minute=conf.end['minute'])
        self.timeset.data = conf.timeset
        self.interval.data = conf.interval
        self.logger = \
            logging.getLogger('server_app.webforms.TimelapseForm')
        # self.logger.debug('__init__')

    def get_res_from_name(self, resname):
        res = (0, 0)
        for r in TimelapseForm.resolutions:
            if resname == r[0]:
                res = [int(v) for v in r[1].split('x')]
                break
        # self.logger.debug('get_res_from_name(%s) -> %s', resname, res)
        return res

    def get_name_from_res(self, res):
        name = ''
        for i, r in enumerate(TimelapseForm.resolutions):
            value = 'x'.join([str(v) for v in res])
            if value == r[1]:
                name = r[0]
                break
        # self.logger.debug('get_name_from_res(%s) -> %s', res, name)
        return name

    def boolean_daylist(self, days):
        booldays = [d in days for d, _ in TimelapseForm.dayslabels]
        self.logger.debug('boolean_daylist(%s) -> %s', days, booldays)
        return booldays

    def daylist_frombool(self, days):
        daylist = [d for i, d in enumerate(TimelapseForm.daysfields)
                   if days[i]]
        self.logger.debug('daylist_frombool(%s) -> %s', days, daylist)
        return daylist


class ConfigForm(FlaskForm):
    submit = SubmitField('Configurer')

