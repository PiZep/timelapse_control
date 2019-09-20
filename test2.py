#!/usr/bin/env python3

import timelapse
import camera_pi
# import config
# import tlconfig

cam = camera_pi.Camera()
tl = timelapse.TimeLapse(cam)

tl.config.PARAM['res'] = {'width': 1080, 'height': 1920}
tl.config.PARAM['interval'] = 15
tl.config.set_config()

for t in tl.timelapse():
    print(t)

