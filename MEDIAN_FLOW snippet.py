import cv2
import numpy as np

# Function to initialize the Median Flow tracker
def create_median_flow_tracker():
    return cv2.TrackerMedianFlow_create()

# Function to select the ROI for tracking
def select_roi(frame):
    roi = cv2.selectROI("Select ROI", frame, False)
    return roi

# Main function
if __name__ == "__main__":
    video_path = "/Users/georgijzukov/PycharmProjects/tracker/tracker/tracking.mp4"
    cap = cv2.VideoCapture(video_path)

    # Read the first frame
    ret, frame = cap.read()

    # Select the ROI for tracking
    roi = select_roi(frame)

    # Initialize the Median Flow tracker
    tracker = create_median_flow_tracker()

    # Initialize the tracker with the first frame and selected ROI
    tracker.init(frame, roi)

    # Process the video frames
    while True:
        # Read the next frame
        ret, frame = cap.read()

        # Break the loop if we have reached the end of the video
        if not ret:
            break

        # Update the tracker with the current frame
        success, new_roi = tracker.update(frame)

        # Draw the tracked object if the tracker update was successful
        if success:
            p1 = (int(new_roi[0]), int(new_roi[1]))
            p2 = (int(new_roi[0] + new_roi[2]), int(new_roi[1] + new_roi[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
        else:
            cv2.putText(frame, "Tracking failure", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display the current frame with the tracked object
        cv2.imshow("Median Flow Tracker", frame)

        # Exit the loop if the 'q' key is pressed

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()
