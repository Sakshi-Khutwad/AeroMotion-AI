import cv2
import numpy as np
import os
import pyautogui as pag
from HandTrackingModule import HandDetector, fingers
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import customtkinter as ctk


class ImageHolder:
    def __init__(self, img_path):
        self.img = PhotoImage(file=img_path)


def take_user_input():
    def cancel_button_pressed():
        nonlocal user_input
        user_input = ''
        # print(user_input)
        text_root.destroy()

    def add_button_pressed():
        nonlocal user_text_entry, user_input
        user_input = user_text_entry.get()
        text_root.destroy()

    # root
    text_root = ctk.CTk()
    text_root.config(bg='#FF149F')

    text_root.overrideredirect(True)

    text_root_width = 400
    text_root_height = 230
    text_root_x = int((screen_width / 1.7) - (text_root_width / 2))
    text_root_y = int((screen_height / 1.8) - (text_root_height / 2))

    text_root.geometry(f'{text_root_width}x{text_root_height}+{text_root_x}+{text_root_y}')

    # variables
    user_text_entry = ctk.StringVar()
    user_input = ''

    # Components
    text_label = ctk.CTkLabel(
        text_root,
        text='Enter text',
        text_color='#343434',
        bg_color='#FF149F',
        font=('Poppins', 24)
    )

    text_entry = ctk.CTkEntry(
        text_root,
        width=280,
        corner_radius=10,
        text_color='white',
        fg_color='#E7B023',
        bg_color='#FF149F',
        font=('Poppins', 20),
        border_width=3,
        border_color='#F9D476',
        textvariable=user_text_entry
    )

    cancel_button = ctk.CTkButton(
        text_root,
        width=90,
        corner_radius=10,
        fg_color='#FFDA7B',
        text='CANCEL',
        font=('Poppins Medium', 15),
        text_color='black',
        bg_color='#FF149F',
        hover_color='#E7B023',
        border_color='#F9D476',
        border_width=3,
        command=cancel_button_pressed
    )

    add_button = ctk.CTkButton(
        text_root,
        width=90,
        corner_radius=10,
        fg_color='#FFDA7B',
        text='ADD',
        font=('Poppins Medium', 15),
        text_color='black',
        bg_color='#FF149F',
        hover_color='#E7B023',
        border_color='#F9D476',
        border_width=3,
        command=add_button_pressed
    )

    # grid
    text_root.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
    text_root.rowconfigure((0, 1, 2, 3, 4, 6, 7), weight=1)
    text_root.rowconfigure(5, weight=2)

    # placing widgets
    text_label.grid(row=1, column=1, sticky='ws')
    text_entry.grid(row=2, column=1, rowspan=2, columnspan=6, sticky='nsew')
    cancel_button.grid(row=5, column=0, columnspan=2, sticky='ne')
    add_button.grid(row=5, column=3, columnspan=2, sticky='ne')

    text_root.mainloop()

    return user_input


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(title="Select File",
                                           filetypes=[("Image files", ".png;.jpg;*.jpeg"),
                                                      ("Text files", "*.txt"),
                                                      ("PDF files", "*.pdf"),
                                                      ("All files", ".")])
    root.destroy()  # Close the Tkinter window
    return file_path


# Save
def save_canvas():
    global img_canvas
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if filename:
        cv2.imwrite(filename, img_canvas)
        # print("Canvas saved as:", filename)


def clear_canvas():
    global userText, thickness, draw_color, img_canvas
    draw_color = (255, 255, 255)
    thickness = 5
    userText = []
    img_canvas = np.zeros((screen_height, screen_width, 3), np.uint8)


def calculate_distance(a1, b1, a2, b2):
    return int(np.sqrt((a2 - a1) ** 2 + (b2 - b1) ** 2))

# Create black canvas
screen_width, screen_height = pag.size()
img_canvas = np.zeros((screen_height, screen_width, 3), np.uint8)

# Set size of Video captured image
cap = cv2.VideoCapture(0, cv2.CAP_ANY)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# Load header image
folderPath = "Header"
mylist = os.listdir(folderPath)
overLay = []


for imPath in mylist:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLay.append(image)

header_colors = overLay[0]

# Load Thickness image
thickness_path = "SideBar"
mylist3 = os.listdir(thickness_path)

Thick = []
for imPath3 in mylist3:
    image = cv2.imread(f'{thickness_path}/{imPath3}')
    Thick.append(image)

side_thickness = Thick[0]

# Eraser and TextBox
eraser_path = "Eraser_Thickness"
mylist4 = os.listdir(eraser_path)
EraserLay = []

for imPath4 in mylist4:
    image = cv2.imread(f'{eraser_path}/{imPath4}')
    EraserLay.append(image)

side_eraser = EraserLay[0]

# Shapes

ShapesPath = "Shapes"
mylist2 = os.listdir(ShapesPath)

Shapes = []
for imPath2 in mylist2:
    image = cv2.imread(f'{ShapesPath}/{imPath2}')
    Shapes.append(image)

header_shapes = Shapes[0]

# Load Buttons

ButtonsPath = "Buttons"
mylist3 = os.listdir(ButtonsPath)

Buttons_lay = []
for imPath3 in mylist3:
    image = cv2.imread(f'{ButtonsPath}/{imPath3}')
    Buttons_lay.append(image)

# Set previous points of drawing

xp, yp = 0, 0

detector = HandDetector(detection_confidence=0.85)

img = None
draw_color = (255, 255, 255)
init_start = False
thickness = 5
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
text_x, text_y = 500, 300
fist = False
eraser_color = (0, 0, 0)
start_loc = False
text = None
text_size = 0
distance = 0

global first_x, first_y, next_x, next_y, center_x, center_y, first_rect_x, first_rect_y, next_rect_x, \
    next_rect_y, global_im

userText = []

while cap.isOpened():
    try:
        success, img = cap.read()
        if not success:
            raise Exception("Error: Unable to read the Video")
    except Exception as e:
        print(f"{e}")

    img_flip = cv2.flip(img, 1)
    img_resized = cv2.resize(img_flip, (screen_width, screen_height))

    img_resized = detector.find_hands(img_resized)

    landmarks_list = detector.find_position(img_resized)

    if len(landmarks_list) != 0:

        finger = fingers(landmarks_list)
        index_x, index_y = landmarks_list[8][1], landmarks_list[8][2]
        middle_x, middle_y = landmarks_list[12][1], landmarks_list[12][2]

        # Selection Mode
        if finger == [0, 1, 1, 0, 0]:

            xp, yp = 0, 0

            # Checking Colors and Shapes Selection
            if index_y < 75:

                if 10 < index_x < 100:
                    header_colors = overLay[1]
                    # print("White Selected")
                    draw_color = (255, 255, 255)  # white

                elif 200 < index_x < 260:
                    header_colors = overLay[2]
                    # print("Red Selected")
                    draw_color = (0, 0, 255)  # red

                elif 360 < index_x < 450:
                    header_colors = overLay[3]
                    draw_color = (0, 255, 0)  # green

                elif 500 < index_x < 600:
                    header_colors = overLay[4]
                    draw_color = (255, 0, 0)  # Blue

                elif 700 < index_x < 800:  # curve
                    header_shapes = Shapes[1]

                elif 820 < index_x < 940:  # line
                    header_shapes = Shapes[2]

                elif 1020 < index_x < 1100:  # Rectangle
                    header_shapes = Shapes[3]

                elif 1200 < index_x < 1280:  # circle
                    header_shapes = Shapes[4]

            # Checking for Thickness Selection
            if index_x < 75 <= index_y < 695:

                if 100 < index_y < 170:
                    side_thickness = Thick[1]
                    thickness = 5
                elif 200 < index_y < 270:
                    side_thickness = Thick[2]
                    thickness = 15
                elif 300 < index_y < 370:
                    side_thickness = Thick[3]
                    thickness = 40

                elif 470 < index_y < 570:               # Eraser
                    side_eraser = EraserLay[1]
                    header_shapes = Shapes[0]
                    header_colors = overLay[0]
                    side_thickness = Thick[0]

                elif 590 < index_y < 670:               # Text box
                    side_eraser = EraserLay[2]
                    user_text = str(take_user_input())
                    if user_text != '':
                        userText.append({'text': user_text, 'text_x': text_x, 'text_y': text_y})
                        cv2.putText(img_resized, userText[-1]['text'], (text_x, text_y), font, fontScale, draw_color, 2)
                        cv2.putText(img_canvas, userText[-1]['text'], (text_x, text_y), font, fontScale, draw_color, 2)
                        text_x, text_y = (text_x + 40), (text_y + 40)

            # Checking for Button Selection
            if index_x > screen_width-100:
                if 200 < index_y < 320:                 # Add Image Button
                    # print("Adding Image")

                    dialogImage = cv2.imread(select_file())
                    if dialogImage is not None:
                        # Resize the image to fit the screen
                        aspect_ratio = dialogImage.shape[1] / dialogImage.shape[0]  # width / height

                        # Resize the image based on the desired width while maintaining the aspect ratio
                        window_width = 500
                        window_height = int(window_width / aspect_ratio)
                        dialogImage_resized = cv2.resize(dialogImage, (window_width, window_height))

                        start_x = 130
                        start_y = 130
                        end_x = start_x + dialogImage_resized.shape[1]  # width
                        end_y = start_y + dialogImage_resized.shape[0]  # height

                        # Assign the resized image to the correct area
                        img_resized[start_y:end_y, start_x:end_x] = dialogImage_resized
                        img_canvas[start_y:end_y, start_x:end_x] = dialogImage_resized

                    key = cv2.waitKey(1)

                if 350 < index_y < 470:                 # Clear Screen Button
                    # print("Clear button")
                    side_eraser = EraserLay[0]
                    header_shapes = Shapes[0]
                    header_colors = overLay[0]
                    side_thickness = Thick[0]
                    text_x, text_y = 500, 300
                    clear_canvas()
                if 490 < index_y < 610:                 # Save Button
                    # print("Save button ")
                    save_canvas()

            xp, yp = index_x, index_y

        if finger == [0, 1, 0, 0, 0]:

            # Condition for Free Hand drawing
            if np.array_equal(header_shapes, Shapes[1]):
                side_eraser = EraserLay[0]
                if xp == 0 and yp == 0:
                    xp, yp = index_x, index_y

                cv2.line(img_resized, (xp, yp), (index_x, index_y), draw_color, thickness)
                cv2.line(img_canvas, (xp, yp), (index_x, index_y), draw_color, thickness)

            # Condition for Eraser
            if np.array_equal(side_eraser, EraserLay[1]):

                if xp == 0 and yp == 0:
                    xp, yp = index_x, index_y

                cv2.line(img_resized, (xp, yp), (index_x, index_y), eraser_color, thickness)
                cv2.line(img_canvas, (xp, yp), (index_x, index_y), eraser_color, thickness)

            xp, yp = index_x, index_y

        # Condition for drawing Line
        if np.array_equal(header_shapes, Shapes[2]):
            side_eraser = EraserLay[0]
            # print("Line selected")
            if finger == [0, 1, 0, 0, 0] or finger == [0, 1, 1, 0, 0]:

                if (not init_start and finger == [0, 1, 0, 0, 0] and
                        ((landmarks_list[5][2] - landmarks_list[8][2]) > 40)):
                    first_x, first_y = xp, yp
                    cv2.line(img_resized, (xp, yp), (xp, yp), draw_color, thickness)
                    cv2.line(img_canvas, (xp, yp), (xp, yp), draw_color, thickness)
                    init_start = True

                if init_start and finger == [0, 1, 1, 0, 0] and ((landmarks_list[9][2] - landmarks_list[12][2]) > 40):
                    # x2, y2 = index_x, index_y
                    if not first_x and not first_y:
                        first_x, first_y = xp, yp
                    # print("Drawing Line")
                    next_x, next_y = xp, yp
                    cv2.line(img_resized, (first_x, first_y), (next_x, next_y), draw_color, thickness)
                    cv2.line(img_canvas, (first_x, first_y), (next_x, next_y), draw_color, thickness)
                    init_start = False

        # Condition for drawing Rectangle
        if np.array_equal(header_shapes, Shapes[3]):
            side_eraser = EraserLay[0]
            # print("Rectangle Selected")
            if finger == [0, 1, 0, 0, 0] or finger == [0, 1, 1, 0, 0]:

                if (not init_start and finger == [0, 1, 0, 0, 0] and
                        ((landmarks_list[5][2] - landmarks_list[8][2]) > 40)):
                    first_rect_x, first_rect_y = xp, yp
                    cv2.line(img_resized, (xp, yp), (xp, yp), draw_color, thickness)
                    cv2.line(img_canvas, (xp, yp), (xp, yp), draw_color, thickness)
                    init_start = True

                if init_start and finger == [0, 1, 1, 0, 0] and (
                        (landmarks_list[9][2] - landmarks_list[12][2]) > 40):
                    # x2, y2 = index_x, index_y
                    if not first_rect_x and not first_rect_y:
                        first_rect_x, first_rect_y = xp, yp
                    # print("Drawing Line")
                    next_rect_x, next_rect_y = xp, yp
                    cv2.rectangle(img_resized, (first_rect_x, first_rect_y), (next_rect_x, next_rect_y), draw_color,
                                  thickness)
                    cv2.rectangle(img_canvas, (first_rect_x, first_rect_y), (next_rect_x, next_rect_y), draw_color,
                                  thickness)
                    init_start = False

        # Condition for Drawing Circle
        if np.array_equal(header_shapes, Shapes[4]):
            side_eraser = EraserLay[0]
            # print("Circle Selected")
            if finger == [0, 1, 0, 0, 0] or finger == [0, 1, 1, 0, 0]:
                if (not init_start and finger == [0, 1, 0, 0, 0] and
                        ((landmarks_list[5][2] - landmarks_list[8][2]) > 40)):
                    center_x, center_y = xp, yp
                    cv2.line(img_resized, (xp, yp), (xp, yp), draw_color, thickness)
                    cv2.line(img_canvas, (xp, yp), (xp, yp), draw_color, thickness)
                    init_start = True

                if init_start and finger == [0, 1, 1, 0, 0] and (
                        (landmarks_list[9][2] - landmarks_list[12][2]) > 40):
                    if not center_x and not center_y:
                        center_x, center_y = xp, yp
                    next_x, next_y = xp, yp
                    radius = calculate_distance(center_x, center_y, next_x, next_y)
                    cv2.circle(img_resized, (center_x, center_y), radius, draw_color, thickness)
                    cv2.circle(img_canvas, (center_x, center_y), radius, draw_color, thickness)
                    cv2.line(img_resized, (center_x, center_y), (center_x, center_y), (0, 0, 0), thickness)
                    cv2.line(img_canvas, (center_x, center_y), (center_x, center_y), (0, 0, 0), thickness)

                    init_start = False

        # Condition for Moving text
        if len(userText) != 0:
            if not start_loc and finger == [0, 0, 0, 0, 0]:
                for text_dict in userText:
                    distance = calculate_distance(text_dict['text_x'], text_dict['text_y'], landmarks_list[6][1],
                                                  landmarks_list[6][2])
                    text_size = cv2.getTextSize(text_dict['text'], font, fontScale, 2)[0]
                    if distance < text_size[0]:
                        init_loc_x, init_loc_y = text_dict['text_x'], text_dict['text_y']
                        # text_dict['text_x'], text_dict['text_y'] = text_x, text_y
                        text = text_dict
                        cv2.putText(img_resized, text['text'], (init_loc_x, init_loc_y), font, fontScale, (0, 0, 0), 2)
                        cv2.putText(img_canvas, text['text'], (init_loc_x, init_loc_y), font, fontScale, (0, 0, 0), 2)
                        cv2.putText(img_resized, text['text'], (landmarks_list[9][1], landmarks_list[9][2]), font,
                                    fontScale, draw_color, 2)
                        start_loc = True

            if start_loc and finger == [1, 1, 1, 1, 1]:
                start_loc = False
                final_loc_x, final_loc_y = landmarks_list[9][1], landmarks_list[9][2]
                text['text_x'], text['text_y'] = final_loc_x, final_loc_y
                cv2.putText(img_resized, text['text'], (landmarks_list[9][1], landmarks_list[9][2]), font, fontScale,
                            draw_color, 2)
                cv2.putText(img_resized, text['text'], (landmarks_list[9][1], landmarks_list[9][2]), font, fontScale,
                            draw_color, 2)
                cv2.putText(img_canvas, text['text'], (landmarks_list[9][1], landmarks_list[9][2]), font, fontScale,
                            draw_color, 2)

            if finger == [0, 0, 0, 0, 0]:
                if distance < text_size[0]:
                    cv2.putText(img_resized, text['text'], (landmarks_list[9][1], landmarks_list[9][2]), font,
                                fontScale, draw_color, 2)

    # resizing images
    header_colors_resized = cv2.resize(header_colors, (660, 75))
    header_shapes_resized = cv2.resize(header_shapes, (620, 75))
    SideBar_resized = cv2.resize(side_thickness, (75, 338))
    SideEraser_resized = cv2.resize(side_eraser, (75, 287))
    add_image_resized = cv2.resize(Buttons_lay[0], (100, 120))
    save_image_resized = cv2.resize(Buttons_lay[2], (100, 120))
    clear_image_resized = cv2.resize(Buttons_lay[1], (100, 120))

    # Placing Images on Canvas
    img_resized[0:75, 0:660] = header_colors_resized
    img_resized[0:75, 660:1280] = header_shapes_resized
    img_resized[75:413, 0:75] = SideBar_resized
    img_resized[413:700, 0:75] = SideEraser_resized
    img_resized[200:320, (screen_width - 100):screen_width] = add_image_resized
    img_resized[350:470, (screen_width - 100):screen_width] = clear_image_resized
    img_resized[500:620, (screen_width - 100):screen_width] = save_image_resized

    # Displaying Canvas
    img_overlay = cv2.addWeighted(img_canvas, 0.8, img_resized, 0.7, 0)
    cv2.imshow("Canvas", img_canvas)
    cv2.imshow("Image", img_overlay)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
