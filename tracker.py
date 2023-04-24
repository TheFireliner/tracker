import cv2
import numpy as np

def create_tracker_by_name(tracker_name):
    available_trackers = {
        "KCF": cv2.TrackerKCF_create,
        "BOOSTING": getattr(cv2, "TrackerBoosting_create", None),
        "MIL": getattr(cv2, "TrackerMIL_create", None),
        "TLD": getattr(cv2, "TrackerTLD_create", None),
        "MEDIAN_FLOW": getattr(cv2, "TrackerMedianFlow_create", None),
    }

    if tracker_name not in available_trackers:
        raise ValueError("Invalid tracker name")

    if available_trackers[tracker_name] is None:
        print(f"Warning: {tracker_name} tracker is not available in your OpenCV version.")
        return None

    return available_trackers[tracker_name]()

def play_original_video(cap):
    exit = False
    while not exit:
        ret, frame = cap.read()
        if frame is None:
            break
        cv2.imshow('ORIGINAL', frame)
        cv2.moveWindow("ORIGINAL", 0, 0)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('d'):
            ret, frame = cap.read()
        elif key == ord('q'):
            exit = True
            break
        elif key == ord('s'):
            break
    return exit

def select_roi(cap):
    ret, frame = cap.read()
    region = cv2.selectROI("Select region", frame, False)
    if not region:
        quit()

    coord = region
    p1 = (int(coord[0]), int(coord[1]))
    p2 = (int(coord[0] + coord[2]), int(coord[1] + coord[3]))
    frame_region = frame
    cv2.rectangle(frame_region, p1, p2, (0, 255, 0), 2, 1)
    cv2.imshow('FRAME', frame_region)
    cv2.moveWindow("FRAME", 0, 500)
    cv2.destroyWindow("Select region")
    cv2.destroyWindow("ORIGINAL")

    return frame, region  # Return both frame and region

def initialize_trackers(frame, region):
    trackers = {
        k: create_tracker_by_name(k)
        for k in ["KCF", "BOOSTING", "MIL", "TLD", "MEDIAN_FLOW"]
    }

    status = {k: trackers[k].init(frame, region) if trackers[k] is not None else False for k in trackers}
    for k, initialized in status.items():
        if not initialized and trackers[k] is not None:
            print(f"ERROR: {k} tracker not initialized.")
        elif trackers[k] is None:
            print(f"Warning: {k} tracker not available or initialized.")

    return trackers

def track_objects(cap, trackers):
    coord = [region for _ in range(len(trackers))]
    draw_coord = [region for _ in range(len(trackers))]
    isWorking = [True for _ in range(len(trackers))]

    tracker_names = list(trackers.keys())

    while True:
        ret, frame = cap.read()
        if frame is None:
            break

        for idx, (name, tracker) in enumerate(trackers.items()):
            if isWorking[idx] and tracker is not None:  # Check if tracker is not None
                ret, temp_coord = tracker.update(frame)
                if ret:
                    draw_coord[idx] = temp_coord
                    coord[idx] = temp_coord
                else:
                    isWorking[idx] = False

            for idx, (name, _) in enumerate(trackers.items()):
                if isWorking[idx] and tracker is not None:  # Check if tracker is not None
                    p1 = (int(coord[idx][0]), int(coord[idx][1]))
                    p2 = (int(coord[idx][0] + coord[idx][2]), int(coord[idx][1] + coord[idx][3]))
                    cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
                    cv2.putText(frame, name, (p1[0], p1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow('FRAME', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

if __name__ == "__main__":
    cap = cv2.VideoCapture('tracking.mp4')

    exit = play_original_video(cap)
    if exit:
        quit()

    frame, region = select_roi(cap)  # Unpack frame and region
    trackers = initialize_trackers(frame, region)  # Pass both frame and region
    track_objects(cap, trackers)

