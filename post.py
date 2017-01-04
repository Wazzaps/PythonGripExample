#!/usr/bin/python3

"""
Post-processing program, takes the data from the GRIP outputs and publishes it to the robot, or displays it in a window
"""

"""
Copyright (c) 2017 David Shlemayev

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import cv2
from networktables import NetworkTable
from grip import GripPipeline
import numpy as np
import operator

def init():
    print('Initializing NetworkTables')
    NetworkTable.setClientMode()
    NetworkTable.setIPAddress('192.168.1.102')
    NetworkTable.initialize()

def process(frame, pipeline):
    table = NetworkTable.getTable('/SmartDashboard')
    table.putNumber('imgWidth', frame.shape[1])
    table.putNumber('imgHeight', frame.shape[0])
    cv2.imshow("original", frame)
    cv2.imshow("hls", pipeline.cv_bitwise_or_output)
    if len(pipeline.convex_hulls_output) > 0:
        largestContour = max(pipeline.convex_hulls_output, key=cv2.contourArea)
        area = cv2.contourArea(largestContour)
        x, y, w, h = cv2.boundingRect(largestContour)
        contourframe = frame.copy()
        cv2.drawContours(contourframe, pipeline.convex_hulls_output, 0, (0,0,255), 2)
        cv2.drawContours(contourframe, [largestContour], 0, (0,255,255), 2)
        table.putNumber('x', x)
        table.putNumber('y', y)
        table.putNumber('width', w)
        table.putNumber('height', h)
        table.putNumber('area', area)
        table.putBoolean('found', True)
        cv2.imshow("contours", contourframe)
    else:
        cv2.imshow("contours", frame)
        table.putBoolean('found', False)
    cv2.waitKey(1)

    