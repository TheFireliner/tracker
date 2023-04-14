import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib
import copy
matplotlib.use('Qt5Agg')
import numpy
from scipy.ndimage import label
exit = False
while not exit:
    cap1 = cv2.VideoCapture('tracking.mp4')
    while True:
             ret1, frame1 = cap1.read()
             if frame1 is None:
                break
             # render
             cv2.imshow('ORIGINAL', frame1)
             cv2.moveWindow("ORIGINAL", 0, 0)
             # handle keys
             key = cv2.waitKey(0) & 0xFF
             if key == ord('d'):
                 ret1, frame1 = cap1.read()
             elif key == ord('q'):
                exit = True
                break
             elif key == ord('s'):
                 break
    if exit:
        break
    # Track Init
    ret1, frame1 = cap1.read()
    region = cv2.selectROI("Select region", frame1, False)
    if (not region):
        quit()
    # coord = region
    # p1 = (int(coord[0]), int(coord[1]))
    # p2 = (int(coord[0] + coord[2]), int(coord[1] + coord[3]))
    # frame_region = frame1
    # cv2.rectangle(frame_region, p1, p2, (0, 255, 0), 2, 1)
    # cv2.imshow('FRAME', frame_region)
    # cv2.moveWindow("FRAME", 0, 500)
    cv2.destroyWindow("Select region")
    cv2.destroyWindow("ORIGINAL")
    # init kcf tracker
    trackers = {
        "KCF": cv2.TrackerKCF_create(),
        "BOOSTING": cv2.TrackerBoosting_create(),
        "MIL": cv2.TrackerMIL_create(),
        "TLD": cv2.TrackerTLD_create(),
        "MEDIAN_FLOW": cv2.TrackerMedianFlow_create(),
    }
    status = [trackers[k].init(frame1, region) for k in trackers]
    if not all(status):
        print('ERROR')
        quit()
    coord = [region for i in range(0, 5)] 
    draw_coord = [region for i in range(0, 5)] 
    isWorking = [True for i in range(0, 5)] 
    ####

    exit = False
    while not exit:
        cap1 = cv2.VideoCapture('tracking.mp4')
        while True:
            ret1, frame1 = cap1.read()
            if frame1 is None:
                break
            cv2.imshow('ORIGINAL', frame1)
            cv2.moveWindow("ORIGINAL", 0, 0)

            # track
            if isWorking:
                for k in trackers:
                    frame = copy.copy(frame1)
                    status, coord = trackers[k].update(frame)
                    if status and draw_coord:
                        p1 = (int(coord[0]), int(coord[1]))
                        p2 = (int(coord[0] + coord[2]), int(coord[1] + coord[3]))
                        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
                    if k == "KCF":
                        cv2.imshow('KCF TRACKER', frame)
                        cv2.moveWindow("KCF TRACKER", 650, 0)
                    elif k == "BOOSTING":
                        cv2.imshow('BOOSTING TRACKER', frame)
                        cv2.moveWindow("BOOSTING TRACKER", 1500, 0)
                    elif k == "MIL":
                        cv2.imshow('MIL TRACKER', frame)
                        cv2.moveWindow("MIL TRACKER", 650, 480)
                    elif k == "TLD":
                        cv2.imshow('TLD TRACKER', frame)
                        cv2.moveWindow("TLD TRACKER", 1500, 480)
                    elif k == "MEDIAN_FLOW":
                        cv2.imshow('MEDIAN_FLOW TRACKER', frame)
                        cv2.moveWindow("MEDIAN_FLOW TRACKER", 0, 500)
            # handle keys
            key = cv2.waitKey(0) & 0xFF
            if key == ord('d'):
                ret1, frame1 = cap1.read()
            elif key == ord('q'):
                exit = True 
                break
        if exit:
            break        
cap1.release()
cv2.destroyAllWindows()