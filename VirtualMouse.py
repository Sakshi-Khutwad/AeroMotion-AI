import pyautogui as pag
from HandTrackingModule import HandDetector, fingers
import time
import cv2
import numpy as np
import sys
from CameraUtils import open_camera

previous_time = 0
current_time = 0

cap = open_camera("Virtual Mouse")

detector = HandDetector(max_hands=1, detection_confidence=0.85)
pag.FAILSAFE = False
screen_width, screen_height = pag.size()

# Frame reduction: ignore the outer edges of the camera frame so you
# don't have to reach the very corners. This defines a smaller bounding
# box inside the camera feed that maps to the full screen.
FRAME_REDUCTION = 100  # pixels to ignore on each side

# Smoothing factor (0 = no smoothing / instant, higher = smoother / slower).
# Value between 0 and 1 — closer to 1 means more responsive, closer to 0
# means smoother but laggier.
SMOOTHING = 0.35

# Previous smoothed cursor position
prev_screen_x, prev_screen_y = 0, 0

img = None


def should_exit(window_name):
    if cv2.waitKey(1) & 0xFF == 27:
        return True

    try:
        return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1
    except cv2.error:
        return True

while cap.isOpened():

    try:
        success, img = cap.read()
        if not success:
            raise Exception("Error: Unable to read the Video")
    except Exception as e:
        print(f"Error: {e}")

    img_flip = cv2.flip(img, 1)
    img = detector.find_hands(img_flip)

    landmarks_list = detector.find_position(img)

    frame_height, frame_width, _ = img.shape

    if len(landmarks_list) != 0:

        # Get index finger tip coordinates (in camera frame pixels)
        index_tip_x, index_tip_y = landmarks_list[8][1], landmarks_list[8][2]

        # Draw tracking circle at the original landmark position on the camera feed
        cv2.circle(img, (index_tip_x, index_tip_y), 10, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (index_tip_x, index_tip_y), 12, (255, 255, 255), 2)

        # Map camera coordinates to screen coordinates using interpolation.
        # The FRAME_REDUCTION zone at each edge is mapped to screen edges,
        # so the usable camera area is smaller but the mapping covers the
        # full screen.
        raw_screen_x = np.interp(index_tip_x,
                                 (FRAME_REDUCTION, frame_width - FRAME_REDUCTION),
                                 (0, screen_width))
        raw_screen_y = np.interp(index_tip_y,
                                 (FRAME_REDUCTION, frame_height - FRAME_REDUCTION),
                                 (0, screen_height))

        # Apply exponential smoothing to reduce jitter
        cur_screen_x = prev_screen_x + SMOOTHING * (raw_screen_x - prev_screen_x)
        cur_screen_y = prev_screen_y + SMOOTHING * (raw_screen_y - prev_screen_y)

        # Clamp to screen bounds
        cur_screen_x = max(0, min(screen_width - 1, cur_screen_x))
        cur_screen_y = max(0, min(screen_height - 1, cur_screen_y))

        prev_screen_x, prev_screen_y = cur_screen_x, cur_screen_y

        finger = fingers(landmarks_list)

        screen_x_int = int(cur_screen_x)
        screen_y_int = int(cur_screen_y)

        if all(finger):
            pag.mouseUp()

        elif finger[1]:
            pag.moveTo(screen_x_int, screen_y_int)

            if finger[0] and finger[2] == 0:
                pag.leftClick(screen_x_int, screen_y_int)
                time.sleep(0.2)

            if finger[2] and not finger[0]:
                pag.rightClick(screen_x_int, screen_y_int)
                time.sleep(0.2)

            if finger[4]:
                pag.doubleClick(screen_x_int, screen_y_int)
                time.sleep(0.2)

        elif not any(finger):
            pag.mouseDown()
            pag.moveTo(screen_x_int, screen_y_int)

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Draw the frame reduction zone for visual reference
    cv2.rectangle(img, (FRAME_REDUCTION, FRAME_REDUCTION),
                  (frame_width - FRAME_REDUCTION, frame_height - FRAME_REDUCTION),
                  (255, 0, 255), 2)

    cv2.imshow("Virtual Mouse", img)

    if should_exit("Virtual Mouse"):
        break

cap.release()
cv2.destroyAllWindows()
