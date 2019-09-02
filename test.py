#/bin/usr/env python3
# coding: utf-8

import os
import cv2

p = os.chdir(os.getenv('HOME') + "/projets/test_webcam/timelapse")

i = cv2.imread("2019-08-13-09:46.jpg")
i2 = cv2.resize(i, (800, 600))

cv2.imshow('i2', i2)
cv2.imshow('i', i)
cv2.waitKey(0)

cam = cv2.VideoCapture(0)
_, i3 = cam.read()
cv2.imshow('i3', i3)
cam.release()
cv2.waitKey(0)

