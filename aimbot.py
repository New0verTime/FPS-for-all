import cv2
import mss
import numpy as np
from ultralytics import YOLO
import mousekey
import pyautogui
is_q_pressed = False
def on_press(key):
    global is_q_pressed
    try:
        if key.char == 'q' and is_q_pressed == False:
            is_q_pressed = True
        elif key.char == 'q' and is_q_pressed == True:
            is_q_pressed = False
    except AttributeError:
        pass
def on_release(key):
    global is_q_pressed
    try:
        e = 0
    except AttributeError:
        pass
monitor = {"top": 220, "left": 640, "width": 640, "height": 640}
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if len(results[0].boxes) > 0:
            boxes_near = []
            boxes_far = []
            current_pos = pyautogui.position()
            
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy() 
                area = (x2 - x1) * (y2 - y1)
                print(area)
                bbox_center_x = int((x1 + x2) / 2)
                bbox_center_y = int((y1 + y2) / 2)
                
                # Tính khoảng cách từ con trỏ chuột tới trung tâm của bounding box
                distance = np.sqrt((bbox_center_x - current_pos.x) ** 2 + (bbox_center_y - current_pos.y) ** 2)

                # Chia vật thể thành 2 nhóm: gần và xa
                if area > area_threshold:
                    boxes_near.append((box, distance))
                else:
                    boxes_far.append((box, distance))

            # Sắp xếp theo khoảng cách (gần nhất trước)
            if boxes_near:
                boxes_near.sort(key=lambda x: x[1])  # Sắp xếp theo khoảng cách
                selected_box = boxes_near[0][0]  # Chọn vật thể gần nhất
            else:
                boxes_far.sort(key=lambda x: x[1])  # Sắp xếp theo khoảng cách
                selected_box = boxes_far[0][0]  # Chọn vật thể xa nhất nếu không có vật thể gần

            # Lấy tọa độ vật thể được chọn
            x1, y1, x2, y2 = selected_box.xyxy[0].cpu().numpy()
            bbox_center_x = int((x1 + x2) / 2) + 640
            bbox_center_y = int((y1 + y2) / 2) + 220

            # Di chuyển chuột
            mousekey.move_rel((int)((bbox_center_x - current_pos.x) / 6), (int)((bbox_center_y - current_pos.y) / 6))
    cv2.destroyAllWindows()