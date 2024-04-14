from tkinter import *
from customtkinter import *
import subprocess
from random import choice
import pygame
import pyautogui as pag
from PIL import Image, ImageTk

main_window = 0

main_canvas = 0

current_page = 1

virtual_mouse = None
virtual_mouse_running = 0
air_canvas = None
air_canvas_running = 0
hand_gesture = None
hand_gesture_running = 0

vm_module_name = ''
ac_module_name = ''
hg_module_name = ''

vm_tagline = ''
ac_tagline = ''
hg_tagline = ''

start_button = 0
vm_hover_start_image = 0
ac_hover_start_image = 0
hg_hover_start_image = 0
vm_start_button_image = 0
ac_start_button_image = 0
hg_start_button_image = 0

stop_button = 0
vm_hover_stop_image = 0
ac_hover_stop_image = 0
hg_hover_stop_image = 0
vm_stop_button_image = 0
ac_stop_button_image = 0
hg_stop_button_image = 0

ac_hover_left_swipe_image = 0
hg_hover_left_swipe_image = 0

left_swipe_button_x = 0
left_swipe_button_y = 0
left_swipe_button = 0
left_swipe_button_image = 0
move_left_count = 0

right_swipe_button_x = 0
right_swipe_button_y = 0
right_swipe_button = 0
right_swipe_button_image = 0
vm_hover_right_swipe_image = 0
ac_hover_right_swipe_image = 0
move_right_count = 0

module_name = 0
module_image = 0
vm_image = 0
ac_image = 0
hg_image = 0
tagline = 0

vm_help_button_image = 0
vm_hover_help_image = 0
ac_help_button_image = 0
ac_hover_help_image = 0
hg_help_button_image = 0
hg_hover_help_image = 0
help_button = 0

help_image_x = 0
help_image_y = 0
help_image = 0
vm_help_image = 0
ac_help_image = 0
hg_help_image = 0

back_button_x = 0
back_button_y = 0
back_button_image = 0
back_button = 0
move_back_count = 0


# start button functions
def start_button_entered(event):
    if current_page == 1:
        main_canvas.itemconfig(start_button, image=vm_hover_start_image)
    elif current_page == 2:
        main_canvas.itemconfig(start_button, image=ac_hover_start_image)
    elif current_page == 3:
        main_canvas.itemconfig(start_button, image=hg_hover_start_image)


def start_button_left(event):
    if current_page == 1:
        main_canvas.itemconfig(start_button, image=vm_start_button_image)
    elif current_page == 2:
        main_canvas.itemconfig(start_button, image=ac_start_button_image)
    elif current_page == 3:
        main_canvas.itemconfig(start_button, image=hg_start_button_image)


def start_button_pressed(event):
    global virtual_mouse, air_canvas, hand_gesture

    if current_page == 1:
        virtual_mouse = subprocess.Popen(["python", "VirtualMouse.py"])
    elif current_page == 2:
        air_canvas = subprocess.Popen(["python", "MagicCanvas.py"])
    elif current_page == 3:
        hand_gesture = subprocess.Popen(["python", "HandGestureModule.py"])


# stop button functions
def stop_button_entered(event):
    if current_page == 1:
        main_canvas.itemconfig(stop_button, image=vm_hover_stop_image)
    elif current_page == 2:
        main_canvas.itemconfig(stop_button, image=ac_hover_stop_image)
    elif current_page == 3:
        main_canvas.itemconfig(stop_button, image=hg_hover_stop_image)


def stop_button_left(event):
    if current_page == 1:
        main_canvas.itemconfig(stop_button, image=vm_stop_button_image)
    elif current_page == 2:
        main_canvas.itemconfig(stop_button, image=ac_stop_button_image)
    elif current_page == 3:
        main_canvas.itemconfig(stop_button, image=hg_stop_button_image)


def stop_button_pressed(event):
    if current_page == 1 and virtual_mouse is not None:
        virtual_mouse.terminate()
    elif current_page == 2 and air_canvas is not None:
        air_canvas.terminate()
    elif current_page == 3 and hand_gesture is not None:
        hand_gesture.terminate()


# left swipe button functions
def left_swipe_button_entered(event):
    if current_page == 2:
        main_canvas.itemconfig(left_swipe_button, image=ac_hover_left_swipe_image)
    elif current_page == 3:
        main_canvas.itemconfig(left_swipe_button, image=hg_hover_left_swipe_image)


def left_swipe_button_left(event):
    main_canvas.itemconfig(left_swipe_button, image=left_swipe_button_image)


def left_swipe_button_pressed(event):
    global current_page, right_swipe_button

    if current_page == 2:
        current_page = 1

        main_canvas.itemconfig(module_image, image=vm_image)

        main_canvas.itemconfigure(left_swipe_button, state=HIDDEN)

        main_canvas.itemconfig(module_name, text=vm_module_name)
        main_canvas.itemconfig(tagline, text=vm_tagline)

        main_canvas.itemconfig(start_button, image=vm_start_button_image)
        main_canvas.itemconfig(stop_button, image=vm_stop_button_image)

        main_canvas.itemconfig(help_button, image=vm_help_button_image)

    elif current_page == 3:
        current_page = 2

        main_canvas.itemconfig(left_swipe_button, image=ac_hover_left_swipe_image)
        right_swipe_button = main_canvas.create_image(
            right_swipe_button_x, right_swipe_button_y,
            image=right_swipe_button_image,
            anchor='center'
        )
        main_canvas.tag_bind(right_swipe_button, "<Enter>", right_swipe_button_entered)
        main_canvas.tag_bind(right_swipe_button, "<Leave>", right_swipe_button_left)
        main_canvas.tag_bind(right_swipe_button, "<ButtonPress-1>", right_swipe_button_pressed)
        move_right_image()

        main_canvas.itemconfig(module_image, image=ac_image)

        main_canvas.itemconfig(module_name, text=ac_module_name)
        main_canvas.itemconfig(tagline, text=ac_tagline)

        main_canvas.itemconfig(start_button, image=ac_start_button_image)
        main_canvas.itemconfig(stop_button, image=ac_stop_button_image)

        main_canvas.itemconfig(help_button, image=ac_help_button_image)


def move_left_image():
    global move_left_count
    lft_btn_move_time = 1000

    if move_left_count % 2 == 0:
        main_canvas.move(left_swipe_button, 10, 0)
    else:
        main_canvas.move(left_swipe_button, -10, 0)

    move_left_count += 1
    main_window.after(lft_btn_move_time, move_left_image)


# right swipe button functions
def right_swipe_button_entered(event):
    if current_page == 1:
        main_canvas.itemconfig(right_swipe_button, image=vm_hover_right_swipe_image)
    elif current_page == 2:
        main_canvas.itemconfig(right_swipe_button, image=ac_hover_right_swipe_image)


def right_swipe_button_left(event):
    main_canvas.itemconfig(right_swipe_button, image=right_swipe_button_image)


def right_swipe_button_pressed(event):
    global current_page, left_swipe_button

    if current_page == 1:
        current_page = 2

        main_canvas.itemconfig(right_swipe_button, image=ac_hover_right_swipe_image)

        left_swipe_button = main_canvas.create_image(
            left_swipe_button_x, left_swipe_button_y,
            image=left_swipe_button_image,
            anchor='center'
        )
        main_canvas.tag_bind(left_swipe_button, "<Enter>", left_swipe_button_entered)
        main_canvas.tag_bind(left_swipe_button, "<Leave>", left_swipe_button_left)
        main_canvas.tag_bind(left_swipe_button, "<ButtonPress-1>", left_swipe_button_pressed)
        # animation
        move_left_image()

        main_canvas.itemconfig(module_image, image=ac_image)

        main_canvas.itemconfig(module_name, text=ac_module_name)
        main_canvas.itemconfig(tagline, text=ac_tagline)

        main_canvas.itemconfig(start_button, image=ac_start_button_image)
        main_canvas.itemconfig(stop_button, image=ac_stop_button_image)

        main_canvas.itemconfig(help_button, image=ac_help_button_image)

    elif current_page == 2:
        current_page = 3

        main_canvas.itemconfigure(right_swipe_button, state=HIDDEN)

        main_canvas.itemconfig(module_image, image=hg_image)

        main_canvas.itemconfig(module_name, text=hg_module_name)
        main_canvas.itemconfig(tagline, text=hg_tagline)

        main_canvas.itemconfig(start_button, image=hg_start_button_image)
        main_canvas.itemconfig(stop_button, image=hg_stop_button_image)

        main_canvas.itemconfig(help_button, image=hg_help_button_image)


def move_right_image():
    global move_right_count
    rgt_btn_move_time = 1000

    if main_canvas.itemcget(right_swipe_button, 'state') != 'disabled':
        if move_right_count % 2 == 0:
            main_canvas.move(right_swipe_button, 10, 0)
        else:
            main_canvas.move(right_swipe_button, -10, 0)

        move_right_count += 1
    main_window.after(rgt_btn_move_time, move_right_image)


# back button functions
def back_button_entered(event):
    if current_page == 1:
        main_canvas.itemconfig(back_button, image=ac_hover_left_swipe_image)
    elif current_page == 2:
        main_canvas.itemconfig(back_button, image=vm_hover_right_swipe_image)
    elif current_page == 3:
        main_canvas.itemconfig(back_button, image=ac_hover_right_swipe_image)


def back_button_left(event):
    main_canvas.itemconfig(back_button, image=back_button_image)


def back_button_pressed(event):
    main_canvas.itemconfigure(back_button, state=HIDDEN)
    main_canvas.itemconfigure(help_image, state=HIDDEN)


# help button functions
def help_button_entered(event):
    if current_page == 1:
        main_canvas.itemconfig(help_button, image=vm_hover_help_image)
    elif current_page == 2:
        main_canvas.itemconfig(help_button, image=ac_hover_help_image)
    elif current_page == 3:
        main_canvas.itemconfig(help_button, image=hg_hover_help_image)


def help_button_left(event):
    if current_page == 1:
        main_canvas.itemconfig(help_button, image=vm_help_button_image)
    elif current_page == 2:
        main_canvas.itemconfig(help_button, image=ac_help_button_image)
    elif current_page == 3:
        main_canvas.itemconfig(help_button, image=hg_help_button_image)


def help_button_pressed(event):
    global help_image, back_button

    if current_page == 1:
        help_image = main_canvas.create_image(
            help_image_x, help_image_y,
            image=vm_help_image,
            anchor='nw'
        )

        back_button = main_canvas.create_image(
            back_button_x, back_button_y,
            image=back_button_image,
            anchor='center'
        )
        main_canvas.tag_bind(back_button, "<Enter>", back_button_entered)
        main_canvas.tag_bind(back_button, "<Leave>", back_button_left)
        main_canvas.tag_bind(back_button, "<ButtonPress-1>", back_button_pressed)

    elif current_page == 2:
        help_image = main_canvas.create_image(
            help_image_x, help_image_y,
            image=ac_help_image,
            anchor='nw'
        )

        back_button = main_canvas.create_image(
            back_button_x, back_button_y,
            image=back_button_image,
            anchor='center'
        )
        main_canvas.tag_bind(back_button, "<Enter>", back_button_entered)
        main_canvas.tag_bind(back_button, "<Leave>", back_button_left)
        main_canvas.tag_bind(back_button, "<ButtonPress-1>", back_button_pressed)

    elif current_page == 3:
        help_image = main_canvas.create_image(
            help_image_x, help_image_y,
            image=hg_help_image,
            anchor='nw'
        )

        back_button = main_canvas.create_image(
            back_button_x, back_button_y,
            image=back_button_image,
            anchor='center'
        )
        main_canvas.tag_bind(back_button, "<Enter>", back_button_entered)
        main_canvas.tag_bind(back_button, "<Leave>", back_button_left)
        main_canvas.tag_bind(back_button, "<ButtonPress-1>", back_button_pressed)


# closing function
def on_close():
    if virtual_mouse is not None:
        if virtual_mouse.poll() is None:
            virtual_mouse.terminate()
    elif air_canvas is not None:
        if air_canvas.poll() is None:
            air_canvas.terminate()
    elif hand_gesture is not None:
        if hand_gesture.poll() is None:
            hand_gesture.terminate()
    main_window.destroy()


# main function
def main_screen():
    global main_window, screen_width, screen_height, main_canvas, background_image, current_page, vm_module_name
    global vm_image, module_image, ac_image, module_name, hg_image, tagline, start_button, stop_button, vm_tagline
    global vm_start_button_image, ac_start_button_image, hg_start_button_image, ac_hover_left_swipe_image, ac_tagline
    global vm_hover_start_image, ac_hover_start_image, hg_hover_start_image, hg_hover_left_swipe_image, ac_module_name
    global vm_stop_button_image, ac_stop_button_image, hg_stop_button_image, ac_hover_right_swipe_image, hg_tagline
    global vm_hover_stop_image, ac_hover_stop_image, hg_hover_stop_image, right_swipe_button, move_right_count
    global left_swipe_button_x, left_swipe_button_y, left_swipe_button_image, left_swipe_button, move_left_count
    global right_swipe_button_x, right_swipe_button_y, right_swipe_button_image, vm_hover_right_swipe_image
    global hg_module_name, vm_help_button_image, ac_help_button_image, hg_help_button_image, vm_hover_help_image
    global ac_hover_help_image, hg_hover_help_image, help_button, help_image_x, help_image_y, help_image
    global vm_help_image, ac_help_image, hg_help_image, back_button_x, back_button_y, back_button, back_button_image

    splash.destroy()

    main_window = CTk()

    main_window.title('AeroMotion')
    main_window.iconbitmap('assets/main-screen-commons/logo-24.ico')

    main_window.resizable(False, True)

    # setting geometry
    main_window._state_before_windows_set_titlebar_color = 'zoomed'

    screen_width, screen_height = pag.size()

    main_window.minsize(screen_width, screen_height)

    # creating canvas
    main_canvas = Canvas(main_window, width=screen_width, height=screen_height)
    main_canvas.pack(fill='both', expand=True)

    # setting geometry
    main_window._state_before_windows_set_titlebar_color = 'zoomed'

    # background image
    background_image = Image.open("assets/main-screen-commons/main-white.png")
    background_image = background_image.resize((screen_width, screen_height), Image.NEAREST)
    background_image = ImageTk.PhotoImage(background_image)
    main_canvas.create_image(0, 0, image=background_image, anchor='nw')

    # Main screen components

    # vm image
    vm_image_1 = PhotoImage(file='assets/virtual-mouse/vm-image-1.png')

    vm_images = [vm_image_1]
    vm_image = choice(vm_images)

    image_x = screen_width / 3.5
    image_y = screen_height / 2.44
    module_image = main_canvas.create_image(
        image_x, image_y,
        image=vm_image,
        anchor='center'
    )

    # ac image
    ac_image_1 = PhotoImage(file='assets/air-canvas/ac_image_1.png')
    ac_images = [ac_image_1]
    ac_image = choice(ac_images)

    # hg image
    hg_image_1 = PhotoImage(file='assets/hand-gesture/hg_image_1.png')
    hg_images = [hg_image_1]
    hg_image = choice(hg_images)

    # heading/module name
    module_name_x = screen_width / 2.17
    module_name_y = screen_height / 3.48
    module_name_size = int(screen_width / 35.3)
    vm_module_name = "VIRTUAL MOUSE"
    ac_module_name = "MAGIC CANVAS"
    hg_module_name = "GESTURES SYNC"
    module_name = main_canvas.create_text(
        module_name_x, module_name_y,
        text=vm_module_name,
        font=("Poppins ExtraBold", module_name_size),
        fill="#0E0E65",
        anchor='nw'
    )

    # tagline
    tagline_x = screen_width / 2.17
    tagline_y = screen_height / 2.5
    tagline_size = int(screen_width / 140)
    tagline_width = int(screen_width / 2.4)
    vm_tagline = ("Step into the future by controlling the cursor with a wave of your fingers. "
                  "It's beyond click and touch, it's AeroMotion.")
    ac_tagline = ("Unleash your artistic flow using air painting, where gestures meet imagination. "
                  "It's control redefined, it's AeroMotion.")
    hg_tagline = ("Elevate your experience with magical control over the gap between you and your computer. It's "
                  "all in your hands now.")
    tagline = main_canvas.create_text(
        tagline_x, tagline_y,
        text=vm_tagline,
        font=(" ", tagline_size),
        fill="#0E0E65",
        anchor='nw',
        width=tagline_width
    )

    # start button
    start_button_x = screen_width / 1.89
    start_button_y = screen_height / 1.75
    vm_start_button_image = PhotoImage(file='assets/virtual-mouse/vm-main-start-button.png')
    vm_hover_start_image = PhotoImage(file="assets/virtual-mouse/vm-hover-start-button.png")
    ac_start_button_image = PhotoImage(file='assets/air-canvas/ac-main-start-button.png')
    ac_hover_start_image = PhotoImage(file='assets/air-canvas/ac-hover-start-button.png')
    hg_start_button_image = PhotoImage(file='assets/hand-gesture/hg-main-start-button.png')
    hg_hover_start_image = PhotoImage(file='assets/hand-gesture/hg-hover-start-button.png')
    start_button = main_canvas.create_image(
        start_button_x, start_button_y,
        image=vm_start_button_image,
        anchor='center'
    )
    main_canvas.tag_bind(start_button, "<Enter>", start_button_entered)
    main_canvas.tag_bind(start_button, "<Leave>", start_button_left)
    main_canvas.tag_bind(start_button, "<ButtonPress-1>", start_button_pressed)

    # stop button
    stop_button_x = screen_width / 1.275
    stop_button_y = screen_height / 1.75
    vm_stop_button_image = PhotoImage(file='assets/virtual-mouse/vm-main-stop-button.png')
    vm_hover_stop_image = PhotoImage(file="assets/virtual-mouse/vm-hover-stop-button.png")
    ac_stop_button_image = PhotoImage(file='assets/air-canvas/ac-main-stop-button.png')
    ac_hover_stop_image = PhotoImage(file="assets/air-canvas/ac-hover-stop-button.png")
    hg_stop_button_image = PhotoImage(file='assets/hand-gesture/hg-main-stop-button.png')
    hg_hover_stop_image = PhotoImage(file='assets/hand-gesture/hg-hover-stop-button.png')
    stop_button = main_canvas.create_image(
        stop_button_x, stop_button_y,
        image=vm_stop_button_image,
        anchor='center'
    )
    main_canvas.tag_bind(stop_button, "<Enter>", stop_button_entered)
    main_canvas.tag_bind(stop_button, "<Leave>", stop_button_left)
    main_canvas.tag_bind(stop_button, "<ButtonPress-1>", stop_button_pressed)

    # left swipe button
    left_swipe_button_x = screen_width / 6.8
    left_swipe_button_y = screen_height / 4
    left_swipe_button_image = PhotoImage(file='assets/main-screen-commons/main-left-swipe-button.png')
    ac_hover_left_swipe_image = PhotoImage(file='assets/air-canvas/ac-hover-left-swipe-button.png')
    hg_hover_left_swipe_image = PhotoImage(file='assets/hand-gesture/hg-hover-left-swipe-button.png')
    left_swipe_button = 0
    move_left_count = 0

    # right swipe button
    right_swipe_button_x = screen_width / 1.181
    right_swipe_button_y = screen_height / 4
    right_swipe_button_image = PhotoImage(file='assets/main-screen-commons/main-right-swipe-button.png')
    vm_hover_right_swipe_image = PhotoImage(file="assets/virtual-mouse/vm-hover-right-swipe-button.png")
    ac_hover_right_swipe_image = PhotoImage(file='assets/air-canvas/ac-hover-right-swipe-button.png')
    right_swipe_button = main_canvas.create_image(
        right_swipe_button_x, right_swipe_button_y,
        image=right_swipe_button_image,
        anchor='center'
    )
    main_canvas.tag_bind(right_swipe_button, "<Enter>", right_swipe_button_entered)
    main_canvas.tag_bind(right_swipe_button, "<Leave>", right_swipe_button_left)
    main_canvas.tag_bind(right_swipe_button, "<ButtonPress-1>", right_swipe_button_pressed)
    # animation
    move_right_count = 0
    move_right_image()

    # help button
    help_button_x = screen_width / 3.45
    help_button_y = screen_height / 1.375
    vm_help_button_image = PhotoImage(file='assets/virtual-mouse/vm-help-button.png')
    vm_hover_help_image = PhotoImage(file="assets/virtual-mouse/vm-help-hover-button.png")
    ac_help_button_image = PhotoImage(file='assets/air-canvas/ac-help-button.png')
    ac_hover_help_image = PhotoImage(file='assets/air-canvas/ac-help-hover-button.png')
    hg_help_button_image = PhotoImage(file='assets/hand-gesture/hg-help-button.png')
    hg_hover_help_image = PhotoImage(file='assets/hand-gesture/hg-help-hover-button.png')
    help_button = main_canvas.create_image(
        help_button_x, help_button_y,
        image=vm_help_button_image,
        anchor='center'
    )
    main_canvas.tag_bind(help_button, "<Enter>", help_button_entered)
    main_canvas.tag_bind(help_button, "<Leave>", help_button_left)
    main_canvas.tag_bind(help_button, "<ButtonPress-1>", help_button_pressed)

    # documentation image
    help_image_x = 0
    help_image_y = 0

    vm_help_image = Image.open('assets/virtual-mouse-documentation/all.png')
    vm_help_image = vm_help_image.resize((screen_width, screen_height), Image.NEAREST)
    vm_help_image = ImageTk.PhotoImage(vm_help_image)

    ac_help_image = Image.open('assets/air-canvas-documentation/all.png')
    ac_help_image = ac_help_image.resize((screen_width, screen_height), Image.NEAREST)
    ac_help_image = ImageTk.PhotoImage(ac_help_image)

    hg_help_image = Image.open('assets/hand-gesture-documentation/all.png')
    hg_help_image = hg_help_image.resize((screen_width, screen_height), Image.NEAREST)
    hg_help_image = ImageTk.PhotoImage(hg_help_image)

    help_image = 0

    # back button
    back_button_x = screen_width / 9
    back_button_y = screen_height / 5
    back_button_image = PhotoImage(file='assets/main-screen-commons/main-left-swipe-button.png')
    back_button = 0

    main_window.protocol('WM_DELETE_WINDOW', on_close)

    main_window.mainloop()


splash = Tk()

# fullscreen window with no title bar
splash.attributes('-fullscreen', True)

screen_width, screen_height = pag.size()

# canvas
splash_canvas = Canvas(splash, width=screen_width, height=screen_height)
splash_canvas.pack(fill='both', expand=True)

# adding background image
background_image = Image.open('assets/splash-screen/splash-white.png')
background_image_resized = background_image.resize((screen_width, screen_height), Image.NEAREST)
background_image_resized = ImageTk.PhotoImage(background_image_resized)
splash_canvas.create_image(0, 0, image=background_image_resized, anchor='nw')

# aeromotion text
text_x = (screen_width / 1.65)
text_y = (screen_height / 2)
splash_canvas.create_text(text_x, text_y, text="AEROMOTION", font=('Poppins Bold', 70), fill='#0B0B45', anchor='center')

# adding logo image
logo_image = PhotoImage(file='assets/splash-screen/logo-280.png')
logo_x = (screen_width / 3.4)
logo_y = (screen_height / 2.1)
splash_canvas.create_image(logo_x, logo_y, image=logo_image, anchor='center')

pygame.mixer.init()
pygame.mixer.music.load("assets/splash-screen/splash-screen-sound.mp3")
pygame.mixer.music.play()

splash.after(4000, main_screen)

mainloop()
