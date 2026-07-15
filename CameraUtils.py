import cv2
import numpy as np
import sys

# Maximum number of camera indices to scan
MAX_CAMERA_SCAN = 5


def show_status(window_name, message, color=(255, 255, 255)):
    """Display a centered status message in the OpenCV window."""
    status_img = np.zeros((300, 500, 3), np.uint8)
    status_img[:] = (40, 40, 40)

    text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
    text_x = (500 - text_size[0]) // 2
    text_y = (300 + text_size[1]) // 2
    cv2.putText(status_img, message, (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.imshow(window_name, status_img)
    cv2.waitKey(1)


def _scan_cameras(window_name):
    """Scan camera indices 0..MAX_CAMERA_SCAN-1 and return list of working indices."""
    available = []
    for idx in range(MAX_CAMERA_SCAN):
        show_status(window_name,
                    f"Scanning cameras... [{idx + 1}/{MAX_CAMERA_SCAN}]",
                    (0, 200, 255))
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available.append(idx)
            cap.release()
    return available


def _show_selection_screen(window_name, available_indices):
    """Show a camera selection screen and return the chosen index."""
    img = np.zeros((400, 500, 3), np.uint8)
    img[:] = (40, 40, 40)

    # Title
    cv2.putText(img, "Multiple cameras detected",
                (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 200, 255), 2)
    cv2.putText(img, "Press the number key to select:",
                (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # List cameras
    y = 120
    for i, cam_idx in enumerate(available_indices):
        label = f"[{i + 1}]  Camera {cam_idx}"
        if cam_idx == 0:
            label += "  (Built-in)"
        else:
            label += "  (External)"
        cv2.putText(img, label, (60, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        y += 45

    # Hint
    cv2.putText(img, "Press ESC to cancel",
                (130, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (120, 120, 120), 1)

    cv2.imshow(window_name, img)

    # Wait for user keypress
    while True:
        key = cv2.waitKey(0) & 0xFF

        if key == 27:  # ESC
            return None

        # Number keys 1-9 (ASCII 49-57)
        pressed_num = key - 48  # Convert ASCII to number (1-based)
        if 1 <= pressed_num <= len(available_indices):
            return available_indices[pressed_num - 1]


def open_camera(window_name, backend=None):
    """
    Detect and open a camera, showing status feedback in the OpenCV window.

    - If only one camera is found, it opens automatically.
    - If multiple cameras are found, the user picks one via keypress.
    - If no cameras are found, shows an error and exits.

    Returns an opened cv2.VideoCapture object.
    """
    cv2.namedWindow(window_name)
    show_status(window_name, "Detecting cameras...", (0, 200, 255))

    available = _scan_cameras(window_name)

    if len(available) == 0:
        show_status(window_name, "ERROR: No cameras found!", (0, 0, 255))
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        sys.exit(1)

    if len(available) == 1:
        chosen_idx = available[0]
        show_status(window_name,
                    f"Found Camera {chosen_idx}. Opening...", (0, 200, 255))
    else:
        chosen_idx = _show_selection_screen(window_name, available)
        if chosen_idx is None:
            # User pressed ESC
            cv2.destroyAllWindows()
            sys.exit(0)
        show_status(window_name,
                    f"Opening Camera {chosen_idx}...", (0, 200, 255))

    # Open the selected camera
    if backend is not None:
        cap = cv2.VideoCapture(chosen_idx, backend)
    else:
        cap = cv2.VideoCapture(chosen_idx)

    if not cap.isOpened():
        show_status(window_name,
                    f"ERROR: Camera {chosen_idx} failed to open!", (0, 0, 255))
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        sys.exit(1)

    show_status(window_name, "Camera Ready!", (0, 255, 0))
    cv2.waitKey(800)

    return cap
