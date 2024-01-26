import time
import mediapipe as mp
import cv2


class HandDetector():

    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_confidence=0.5, track_confidence=0.5):

        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence
        self.results = 0
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity, self.detection_confidence,
                                         self.track_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]

    def find_hands(self, img, draw=True):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for h in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, h, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, draw=True):

        self.lm_list = []

        if self.results.multi_hand_landmarks:
            for h in self.results.multi_hand_landmarks:
                for id_lm, hand_lm in enumerate(h.landmark):
                    height, width, _ = img.shape
                    cx, cy = int(width * hand_lm.x), int(height * hand_lm.y)
                    self.lm_list.append([id_lm, cx, cy])

                    if draw:
                        cv2.circle(img, (cx, cy), 3, (255, 255, 0), 3)

        return self.lm_list



    def fingersUp(self):
        fingers=[]

        #Thumb
        if self.lm_list[self.tipIds[0]][1] < self.lm_list[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #4 fingers
        for id in range(1,5):
            if self.lm_list[self.tipIds[id]][2] < self.lm_list[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers