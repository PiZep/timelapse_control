#!/usr/bin/env python3

import timelapse
import camera_pi
# import config
# import tlconfig

cam = camera_pi.Camera()
tl = timelapse.TimeLapse(cam)

tl.config.PARAM['res'] = {'width': 1920, 'height': 1080}
tl.config.PARAM['interval'] = 5
tl.config.set_config()

for t in tl.timelapse():
    print(t)

