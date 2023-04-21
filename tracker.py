import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib
import copy

matplotlib.use('Qt5Agg')
import numpy
from scipy.ndimage import label


# def create_tracker_by_name(tracker_name):
#     try:
#         tracker_median_flow_create = cv2.TrackerMedianFlow_create
#     except AttributeError:
#         tracker_median_flow_create = None
#
#     available_trackers = {
#         "KCF": cv2.TrackerKCF_create,
#         "BOOSTING": cv2.TrackerBoosting_create if hasattr(cv2, "TrackerBoosting_create") else None,
#         "MIL": cv2.TrackerMIL_create if hasattr(cv2, "TrackerMIL_create") else None,
#         "TLD": cv2.TrackerTLD_create if hasattr(cv2, "TrackerTLD_create") else None,
#         "MEDIAN_FLOW": tracker_median_flow_create,
#     }
#
#     if tracker_name not in available_trackers:
#         raise ValueError("Invalid tracker name")
#
#     if available_trackers[tracker_name] is None:
#         raise NotImplementedError(f"{tracker_name} tracker is not available in your OpenCV version")
#
#     return available_trackers[tracker_name]()


def create_tracker_by_name(tracker_name):
    # Create a dictionary of available tracker constructors
    try:
        tracker_median_flow_create = cv2.TrackerMedianFlow_create
    except AttributeError:
        tracker_median_flow_create = None

    try:
        tracker_boosting_create = cv2.TrackerBoosting_create
    except AttributeError:
        tracker_boosting_create = None

    available_trackers = {
        "KCF": cv2.TrackerKCF_create,
        "BOOSTING": tracker_boosting_create,
        "MIL": cv2.TrackerMIL_create if hasattr(cv2, "TrackerMIL_create") else None,
        "TLD": cv2.TrackerTLD_create if hasattr(cv2, "TrackerTLD_create") else None,
        "MEDIAN_FLOW": tracker_median_flow_create,
    }

    if tracker_name not in available_trackers:
        raise ValueError("Invalid tracker name")

    if available_trackers[tracker_name] is None:
        print(f"Warning: {tracker_name} tracker is not available in your OpenCV version.")
        return None

    return available_trackers[tracker_name]()


exit = False
while not exit:
    cap1 = cv2.VideoCapture('tracking.mp4')
    while True:
        ret1, frame1 = cap1.read()
        if frame1 is None:
            break
        cv2.imshow('ORIGINAL', frame1)
        cv2.moveWindow("ORIGINAL", 0, 0)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('d'):
            ret1, frame1 = cap1.read()
        elif key == ord('q'):
            exit = True
            break
        elif key == ord('s'):
            break
    if exit:
        break

    ret1, frame1 = cap1.read()
    region = cv2.selectROI("Select region", frame1, False)
    if not region:
        quit()

    coord = region
    p1 = (int(coord[0]), int(coord[1]))
    p2 = (int(coord[0] + coord[2]), int(coord[1] + coord[3]))
    frame_region = frame1
    cv2.rectangle(frame_region, p1, p2, (0, 255, 0), 2, 1)
    cv2.imshow('FRAME', frame_region)
    cv2.moveWindow("FRAME", 0, 500)
    cv2.destroyWindow("Select region")
    cv2.destroyWindow("ORIGINAL")

    # trackers = {
    #     "KCF": create_tracker_by_name("KCF"),
    #     "BOOSTING": create_tracker_by_name("BOOSTING"),
    #     "MIL": create_tracker_by_name("MIL"),
    #     "TLD": create_tracker_by_name("TLD"),
    #     "MEDIAN_FLOW": create_tracker_by_name("MEDIAN_FLOW"),
    # }

    trackers = {
        k: create_tracker_by_name(k)
        for k in ["KCF", "BOOSTING", "MIL", "TLD", "MEDIAN_FLOW"]
        if create_tracker_by_name(k) is not None
    }

    # status = [trackers[k].init(frame1, region) for k in trackers]
    # if not all(status):
    #     print('ERROR')
    #     quit()

    status = {k: trackers[k].init(frame1, region) if trackers[k] is not None else False for k in trackers}
    for k, initialized in status.items():
        if not initialized:
            print(f"ERROR: {k} tracker not initialized.")

    if not any(status.values()):
        print('ERROR: No trackers available or initialized.')
        quit()

    coord = [region for i in range(0, 5)]
    draw_coord = [region for i in range(0, 5)]
    isWorking = [True for i in range(0, 5)]

    exit = False
    while not exit:
        cap1 = cv2.VideoCapture('tracking.mp4')
        while True:
            ret1, frame1 = cap1.read()
            if frame1 is None:
                break

