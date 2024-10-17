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
        results = model(cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2BGR), conf=0.5)[0].boxes
        if len(results):
            boxes_near = []
            boxes_far = []
            current_pos = pyautogui.position()
            for box in results:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                dx = (x1 + x2) // 2 - current_pos.x + monitor["left"]
                dy = (3 * y1 + y2) // 4 - current_pos.y + monitor["top"]
                distance = dx ** 2 + dy ** 2
                if (x2 - x1) * (y2 - y1) - area_threshold > 0:
                    boxes_near.append((distance, dx, dy))  # Lưu distance, dx, dy
                else:
                    boxes_far.append((distance, dx, dy))  # Lưu distance, dx, dy
            if boxes_near:
                s = min(boxes_near, key=lambda x: x[0])  # Chọn theo distance
            else:
                s = min(boxes_far, key=lambda x: x[0])  # Chọn theo distance
            d, dx, dy = s
            if d < 7000:
                mousekey.move_rel((int)(dx // 5.5), (int)(dy // 5.5))
            elif d < 70000:
                mousekey.move_rel((int)(dx // 7), (int)(dy // 
                                                        7))
            else:
                mousekey.move_rel((int)(dx // 12), (int)(dy // 12)) #magic number is magic