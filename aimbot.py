import cv2
import mss
import numpy as np
from ultralytics import YOLO
import mousekey
import pyautogui

screen_width, screen_height = pyautogui.size()
monitor = {"top": (int)((screen_height - 640)/2), "left": (int)((screen_width - 640)/2), "width": 640, "height": 640}
model = YOLO("best.pt").to('cuda')
area_threshold = 2500
with mss.mss() as sct:
    while True:
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        results = model(img, conf=0.5)
        if len(results[0].boxes):
            boxes_near = []
            boxes_far = []
            current_pos = pyautogui.position()
            #convert position sang he toa do cua mat phang detect
            current_posx = current_pos.x - monitor["left"]
            current_posy = current_pos.y - monitor["top"]
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                area = (x2 - x1) * (y2 - y1)
                bbox_center_x = int((x1 + x2) / 2)
                bbox_center_y = int((3*y1 + y2) / 4)
                distance = (bbox_center_x - current_posx) ** 2 + (bbox_center_y - current_posy) ** 2
                if area > area_threshold:
                    boxes_near.append((box, distance))
                else:
                    boxes_far.append((box, distance))
            if boxes_near:
                s = min(boxes_near, key=lambda x: x[1])
                selected_box = s[0]  # Box gần nhất
                d = s[1]
            else:
                s = min(boxes_far, key=lambda x: x[1])
                selected_box = s[0]  # Box gần nhất
                d = s[1]
            # Lấy tọa độ vật thể được chọn
            x1, y1, x2, y2 = selected_box.xyxy[0].cpu().numpy()
            bbox_center_x = int((x1 + x2) / 2)
            bbox_center_y = int((3*y1 + y2) / 4)
            if d < 7000:
                mousekey.move_rel((int)((bbox_center_x - current_posx) / 5.5), (int)((bbox_center_y - current_posy) / 5.5))
            elif d < 70000:
                mousekey.move_rel((int)((bbox_center_x - current_posx) / 7), (int)((bbox_center_y - current_posy) / 7))
            else:
                mousekey.move_rel((int)((bbox_center_x - current_posx) / 12), (int)((bbox_center_y - current_posy) / 12))

                