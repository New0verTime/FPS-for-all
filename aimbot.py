import cv2
import mss
import numpy as np
from ultralytics import YOLO
import mousekey
import pyautogui
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1280}
model = YOLO("best2.pt").to('cuda')
with mss.mss() as sct:
    while True:
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        results = model(img, conf=0.5)
        if len(results[0].boxes) > 0:
            # Get the bounding box coordinates and areas
            boxes_with_area = []
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy() 
                area = (x2 - x1) * (y2 - y1)
                boxes_with_area.append((box, area))
                boxes_with_area.sort(key=lambda x: x[1], reverse=True)
                largest_box = boxes_with_area[0][0]
                x1, y1, x2, y2 = largest_box.xyxy[0].cpu().numpy()
                bbox_center_x = int((x1 + x2) / 2)
                bbox_center_y = int((y1 + y2) / 2)
                current_pos = pyautogui.position()
                mousekey.move_rel((int)((bbox_center_x-current_pos.x)/6),(int)((bbox_center_y-current_pos.y)/6))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()
