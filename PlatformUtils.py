import platform
import subprocess
from dataclasses import dataclass

import pyautogui as pag
import screen_brightness_control as sbc


SYSTEM = platform.system()
IS_MAC = SYSTEM == "Darwin"
IS_WINDOWS = SYSTEM == "Windows"


@dataclass
class ActiveWindow:
    title: str = ""


def _get_windows_active_window():
    try:
        import pygetwindow as pgw

        window = pgw.getActiveWindow()
        if window is not None:
            return ActiveWindow(window.title or "")
    except Exception as ex:
        print(f"Error getting active window on Windows: {ex}")

    return None


def _get_macos_active_window():
    title = ""

    try:
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGNullWindowID,
            kCGWindowListOptionOnScreenOnly,
        )

        windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        for window in windows:
            if window.get("kCGWindowLayer") != 0:
                continue

            owner = window.get("kCGWindowOwnerName", "")
            window_name = window.get("kCGWindowName", "")
            title = f"{window_name} - {owner}" if window_name else owner
            if title:
                return ActiveWindow(title)
    except Exception as ex:
        print(f"Error getting macOS window title from Quartz: {ex}")

    try:
        from AppKit import NSWorkspace

        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        if app is not None:
            title = app.localizedName() or ""
    except Exception as ex:
        print(f"Error getting frontmost macOS app: {ex}")

    return ActiveWindow(title) if title else None


def get_active_window():
    if IS_MAC:
        return _get_macos_active_window()
    if IS_WINDOWS:
        return _get_windows_active_window()

    return _get_windows_active_window()


def hotkey(*keys):
    pag.hotkey(*keys)


def browser_forward():
    hotkey("command", "right") if IS_MAC else hotkey("alt", "right")


def browser_back():
    hotkey("command", "left") if IS_MAC else hotkey("alt", "left")


def show_desktop():
    hotkey("command", "f3") if IS_MAC else hotkey("win", "d")


def screenshot():
    hotkey("command", "shift", "3") if IS_MAC else pag.press("printscreen")


def volume_up():
    return _change_macos_volume(6) if IS_MAC else _press_volume_key("volumeup")


def volume_down():
    return _change_macos_volume(-6) if IS_MAC else _press_volume_key("volumedown")


def _press_volume_key(key):
    try:
        pag.press(key)
        return True
    except Exception as ex:
        print(f"Volume key press failed: {ex}")
        return False


def _change_macos_volume(delta):
    script = (
        "set currentVolume to output volume of (get volume settings)\n"
        f"set targetVolume to currentVolume + ({delta})\n"
        "if targetVolume > 100 then set targetVolume to 100\n"
        "if targetVolume < 0 then set targetVolume to 0\n"
        "set volume output volume targetVolume"
    )

    try:
        subprocess.run(
            ["osascript", "-e", script],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except Exception as ex:
        print(f"macOS volume fallback failed: {ex}")
        return _press_volume_key("volumeup" if delta > 0 else "volumedown")


def media_seek_forward(window_title):
    if "Media Player" in window_title:
        hotkey("ctrl", "right")
    elif "VLC" in window_title:
        hotkey("command", "right") if IS_MAC else hotkey("alt", "right")
    else:
        pag.press("right")


def media_seek_backward(window_title):
    if "Media Player" in window_title:
        hotkey("ctrl", "left")
    elif "VLC" in window_title:
        hotkey("command", "left") if IS_MAC else hotkey("alt", "left")
    else:
        pag.press("left")


def set_brightness(value):
    brightness = max(0, min(100, int(value)))

    try:
        sbc.set_brightness(brightness)
        return True
    except Exception as ex:
        print(f"screen_brightness_control failed: {ex}")

    if IS_MAC:
        return _set_macos_brightness_with_osascript(brightness)

    return False


def _set_macos_brightness_with_osascript(target):
    try:
        current = sbc.get_brightness(display=0)
        current = current[0] if isinstance(current, list) else current
    except Exception:
        current = 50

    key_code = 144 if target > current else 145
    steps = max(1, min(16, abs(target - int(current)) // 6))
    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                'tell application "System Events"',
                "-e",
                f"repeat {steps} times",
                "-e",
                f"key code {key_code}",
                "-e",
                "end repeat",
                "-e",
                "end tell",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except Exception as ex:
        print(f"macOS brightness fallback failed: {ex}")
        return False
