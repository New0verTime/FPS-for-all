import cv2
import mss
import numpy as np
from ultralytics import YOLO
import mousekey
from pynput import keyboard
import pyautogui
is_q_pressed = False

def on_release(key):
    global is_q_pressed
    try:
        if key.char == 'q' and is_q_pressed == False:
            is_q_pressed = True
        elif key.char == 'q' and is_q_pressed == True:
            is_q_pressed = False
    except AttributeError:
        pass
listener = keyboard.Listener(on_release=on_release)
listener.start()
screen_width, screen_height = pyautogui.size()
monitor = {"top": (int)((screen_height - 640)/2), "left": (int)((screen_width - 640)/2), "width": 640, "height": 640}
model = YOLO("best2.pt").to('cuda')
model2 = YOLO("best.pt").to('cuda')
area_threshold = 2500
with mss.mss() as sct:
    while True:
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        if is_q_pressed == False:
            results = model(img, conf=0.5)
        else:
            results = model2(img, conf=0.5)
        if len(results[0].boxes):
            print(dir(results[0].boxes[0]))
            boxes_near = []
            boxes_far = []
            current_pos = pyautogui.position()
            
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                area = (x2 - x1) * (y2 - y1)
                bbox_center_x = int((x1 + x2) / 2)
                bbox_center_y = int((y1 + y2) / 2)
                distance = (bbox_center_x - current_pos.x) ** 2 + (bbox_center_y - current_pos.y) ** 2
                if area > area_threshold:
                    boxes_near.append((box, distance))
                else:
                    boxes_far.append((box, distance))
            if boxes_near:
                selected_box = min(boxes_near, key=lambda x: x[1])[0]  # Box gần nhất
            else:
                selected_box = min(boxes_far, key=lambda x: x[1])[0]  # Box xa nhất
            # Lấy tọa độ vật thể được chọn
            x1, y1, x2, y2 = selected_box.xyxy[0].cpu().numpy()
            bbox_center_x = int((x1 + x2) / 2) + monitor["left"]
            bbox_center_y = int((y1 + y2) / 2) + monitor["top"]

            # Di chuyển chuột
            mousekey.move_rel((int)((bbox_center_x - current_pos.x) / 6), (int)((bbox_center_y - current_pos.y) / 6))