from HandTrackingModule import HandDetector, fingers
import cv2
import pyautogui as pag
from math import hypot
import time
import numpy as np
import PlatformUtils as platform_utils


def is_browser_open():
    if window is None:
        return False

    for player in media_players:
        if player in window.title:
            return False

    for browser in browsers:
        print(window.title)
        if browser in window.title:
            return True

    return False


def is_thumb_down():
    tip_ids = [4, 8, 12, 16, 20]
    thumb_status = []

    # thumb
    if (landmarks_list[tip_ids[0]][2] > landmarks_list[tip_ids[0] - 1][2] > landmarks_list[tip_ids[0] - 2][2] >
            landmarks_list[tip_ids[0] - 3][2]):
        thumb_status.append(1)
    else:
        thumb_status.append(0)

    # other fingers
    for tip_id in range(1, 5):
        if landmarks_list[tip_ids[tip_id]][1] < landmarks_list[tip_ids[tip_id] - 2][1]:
            thumb_status.append(1)
        else:
            thumb_status.append(0)

    return thumb_status


def rect_check(lm, left_top, right_bottom):
    wrist_x, wrist_y = lm[0][1], lm[0][2]
    if (left_top[0] <= wrist_x < right_bottom[0]) and (left_top[1] < wrist_y < right_bottom[1]):
        if lm[0][-1] == 'Left':
            return 'Left'
        else:
            return 'Right'


def is_media_player_open():
    for media_player in media_players:
        try:
            if window is not None:
                window_name = window.title
                # print(window_name)
                if media_player in window_name:
                    return True
        except Exception as ex:
            print(f"Error Checking media player: {ex}")

    return False


# Volume Controlling function
def volume_control(index_x, index_y, thumb_x, thumb_y):
    # drawing circles on index and thumb tips
    cv2.circle(img_resized, (index_x, index_y), 8, (0, 0, 0), 6)
    cv2.circle(img_resized, (thumb_x, thumb_y), 8, (0, 0, 0), 6)

    # draw line
    cv2.line(img_resized, (index_x, index_y), (thumb_x, thumb_y), (0, 0, 0), 6)

    # calculate center of fingers
    center_x, center_y = (index_x + thumb_x) // 2, (index_y + thumb_y) // 2

    # draw circle at center
    cv2.circle(img_resized, (center_x, center_y), 8, (0, 0, 0), cv2.FILLED)

    length = hypot(index_x - thumb_x, index_y - thumb_y)
    # print(length)
    global msg

    if length > 80:
        msg = "Increasing Volume"
        platform_utils.volume_up()
        time.sleep(0.1)
    else:
        msg = "Decreasing Volume"
        platform_utils.volume_down()
        time.sleep(0.1)


# Brightness Controlling function
def brightness_control(little_x, little_y, thumb_x, thumb_y):
    cv2.circle(img_resized, (little_x, little_y), 8, (0, 0, 0), 6)
    cv2.circle(img_resized, (thumb_x, thumb_y), 8, (0, 0, 0), 6)
    # draw line
    cv2.line(img_resized, (little_x, little_y), (thumb_x, thumb_y), (0, 0, 0), 6)

    # calculate center of fingers
    center_x, center_y = (little_x + thumb_x) // 2, (little_y + thumb_y) // 2
    # draw circle at center
    cv2.circle(img_resized, (center_x, center_y), 8, (0, 0, 0), cv2.FILLED)

    length = hypot(thumb_x - little_x, thumb_y - little_y)
    bright = np.interp(length, [15, 220], [0, 100])
    # print(bright, " ", length)

    global msg

    try:
        msg = "Setting Brightness"
        platform_utils.set_brightness(int(bright))
        time.sleep(0.1)
    except Exception as ex:
        print(f"Error in Brightness Control: {ex}")


cap = cv2.VideoCapture(0)
detector = HandDetector(detection_confidence=0.85)

screen_width, screen_height = pag.size()
screen_width_division = screen_width // 3
right_rect_x = screen_width_division * 2

color_left = color_right = (0, 0, 255)

# left top rect coordinates
left_top_left = (0, 0)
right_bottom_left = (screen_width_division, screen_height)

# right top rect coordinates
left_top_right = (right_rect_x, 0)
right_bottom_right = (screen_width, screen_height)


# miniplayer dimensions
miniplayer_height = 500
miniplayer_width = 500

screen_width_division_miniplayer = miniplayer_width // 3

# left top rect coordinates for miniplayer
left_top_miniplayer_left = (0, 0)
right_bottom_miniplayer_left = (screen_width_division_miniplayer, miniplayer_height)

# right top rect coordinates for miniplayer
left_top_miniplayer_right = (screen_width_division_miniplayer * 2, 0)
right_bottom_miniplayer_right = (miniplayer_height, miniplayer_width)


# Media Players
media_players = ["Media Player", "VLC", "VLC media player", "VLC Media Player", "YouTube", "Plex", "RealPlayer",
                 "GOM Media Player", "ACG Player", "Winamp", "PowerDVD", "iTunes", "Music", "QuickTime Player",
                 "Spotify"]

# Browsers
browsers = ["- Brave", "Brave Browser", "- Google Chrome", "Google Chrome", "Safari", "Opera", "- Microsoft​ Edge",
            "Microsoft Edge", "— Mozilla Firefox", "Mozilla Firefox", "Firefox"]

cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# print(screen_width, " ", screen_height)
# print(screen_width_division)

pag.FAILSAFE = False
cv2.namedWindow("Gesture Sync")

img = None

while cap.isOpened():

    try:
        success, img = cap.read()
        if not success:
            raise Exception("Error: Unable to read the Video")
    except Exception as e:
        print(f"Error: {e}")

    window = platform_utils.get_active_window()
    msg = " "
    img_flip = cv2.flip(img, 1)
    img = detector.find_hands(img_flip)

    img_resized = cv2.resize(img, (screen_width, screen_height), interpolation=cv2.INTER_AREA)
    miniplayer_size = cv2.resize(img, (miniplayer_width, miniplayer_height), interpolation=cv2.INTER_AREA)

    landmarks_list = detector.find_position(img_resized)

    if len(landmarks_list) != 0:

        finger = fingers(landmarks_list)

        is_left_thumb_open = (landmarks_list[4][1] > landmarks_list[3][1] > landmarks_list[2][1] >
                              landmarks_list[1][1] and landmarks_list[8][1] < landmarks_list[4][1])

        is_left_thumb_pointing_left = (landmarks_list[4][1] < landmarks_list[3][1] < landmarks_list[2][1] <
                                       landmarks_list[1][1] and landmarks_list[8][1] > landmarks_list[4][1])

        # Left Hand Gestures Detection
        if rect_check(landmarks_list, left_top_left, right_bottom_left) == 'Left':

            color_left = (0, 255, 0)

            if is_media_player_open():

                # print("Media Player is open")

                # Pause
                if finger[1] == 1 and finger[2] == 1 and (not is_left_thumb_open) and finger[3] == 0 and finger[4] == 0:
                    # window.activate()
                    # print("Two fingers are Open")
                    msg = "Pausing the Media"
                    pag.press('space')
                    time.sleep(2)
                # not (all([finger[1], finger[2], finger[3], finger[4]]))

                elif finger[4] == 0 and finger[3] == 0 and finger[2] == 0 and finger[1] == 0:

                    # forward
                    if is_left_thumb_open:
                        if window.title is not None:
                            window_title = window.title
                            # if "Spotify" in window_title:
                            #     pag.hotkey('shift', 'right')
                            if "Media Player" in window_title:
                                msg = "Skip Forward 30 Seconds"
                            elif "VLC" in window_title:
                                msg = "Skip Forward 10 Seconds"
                            else:
                                msg = "Skip Forward"
                            platform_utils.media_seek_forward(window_title)
                            time.sleep(1)

                    # rewind
                    elif is_left_thumb_pointing_left:
                        if window.title is not None:
                            window_title = window.title
                            # print(window_title)
                            # if "Spotify" in window_title:
                            #     pag.hotkey('shift', 'left')
                            if "Media Player" in window_title:
                                msg = "Skip Backward 30 Seconds"
                            elif "VLC" in window_title:
                                msg = "Skip Backward 10 Seconds"
                            else:
                                msg = "Skip Backward"
                            platform_utils.media_seek_backward(window_title)
                            time.sleep(1)

            if is_browser_open():

                # print("Browser is Open")

                if finger[4] == 0 and finger[3] == 0 and finger[2] == 0 and finger[1] == 0:

                    # next
                    if is_left_thumb_open:
                        # print("Next")
                        msg = "Moving to Next Page"
                        platform_utils.browser_forward()
                        time.sleep(1)

                    # previous
                    elif is_left_thumb_pointing_left:
                        # print("Previous")
                        msg = "Moving to Previous Page"
                        platform_utils.browser_back()
                        time.sleep(1)

            # Open desktop
            thumb_down = is_thumb_down()

            if thumb_down == [1, 1, 1, 1, 1]:
                # print("Thumb's Down")
                msg = "Opening Desktop"
                platform_utils.show_desktop()
                time.sleep(2)

            # print("Left hand in left rectangle")

        else:
            color_left = (0, 0, 255)

        # Right Hand Gestures Detection
        if rect_check(landmarks_list, left_top_right, right_bottom_right) == 'Right':

            color_right = (0, 255, 0)

            if finger[2] == 0 and finger[3] == 0 and finger[4] == 0 and finger[0] == 1 and finger[1] == 1:
                volume_control(landmarks_list[8][1], landmarks_list[8][2], landmarks_list[4][1], landmarks_list[4][2])

            if finger[1] == 0 and finger[2] == 0 and finger[3] == 0:
                brightness_control(landmarks_list[20][1], landmarks_list[20][2], landmarks_list[4][1],
                                   landmarks_list[4][2])

            if finger[1] == 1 and finger[2] == 1 and finger[0] == 0 and finger[3] == 0 and finger[4] == 0:
                msg = "Capturing Screenshot"
                platform_utils.screenshot()
                time.sleep(3)

            # print("Right hand in right rectangle")
        else:
            color_right = (0, 0, 255)

        # print("Thumb status: ", is_left_thumb_pointing_left)

    cv2.putText(img_resized, msg, (right_bottom_left[0] + 40, right_bottom_left[1] // 2), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 0), 3)

    cv2.rectangle(img_resized, left_top_left, right_bottom_left, color_left, 6)
    cv2.rectangle(img_resized, left_top_right, right_bottom_right, color_right, 6)

    cv2.rectangle(miniplayer_size, left_top_miniplayer_left, right_bottom_miniplayer_left, color_left, 6)
    cv2.rectangle(miniplayer_size, left_top_miniplayer_right, right_bottom_miniplayer_right, color_right, 6)

    cv2.putText(miniplayer_size, "Left Hand Gestures", (14, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                (0, 0, 0), 2)
    cv2.putText(miniplayer_size, "Right Hand Gestures", (347, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                (0, 0, 0), 2)

    # cv2.circle(img_resized, (right_rect_x, 0), 3, (255, 255, 0), 6)

    cv2.imshow("Gesture Sync", img_resized)
    # cv2.imshow("Gesture Sync", miniplayer_size)

    if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("Gesture Sync", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
