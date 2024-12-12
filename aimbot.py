import cv2
import mss
import numpy as np
from ultralytics import YOLO
import mousekey
import pyautogui
from ui import MouseControlApp
import keyboard
import os
import sys

class MouseDetection:
    def __init__(self, model_path):
        screen_width, screen_height = pyautogui.size()
        self.monitor = {
            "top": (int)((screen_height - 640) / 2),
            "left": (int)((screen_width - 640) / 2),
            "width": 640,
            "height": 640
        }
        
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        model_path = resource_path("best.pt")
        self.model = YOLO(model_path).to('cuda')
        self.area_threshold = 2500
        self.is_running = False

    def run_detection(self, sensitivity):
        if not self.is_running:
            return

        with mss.mss() as sct:
            results = self.model(cv2.cvtColor(np.array(sct.grab(self.monitor)), cv2.COLOR_BGRA2BGR), conf=0.5)[0].boxes
            if len(results):
                boxes_near = []
                boxes_far = []
                current_pos = pyautogui.position()
                for box in results:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    dx = (x1 + x2) // 2 - current_pos.x + self.monitor["left"]
                    dy = (3 * y1 + y2) // 4 - current_pos.y + self.monitor["top"]
                    distance = dx ** 2 + dy ** 2
                    if (x2 - x1) * (y2 - y1) - self.area_threshold > 0:
                        boxes_near.append((distance, dx, dy))
                    else:
                        boxes_far.append((distance, dx, dy))
                
                if boxes_near:
                    s = min(boxes_near, key=lambda x: x[0])
                elif boxes_far:
                    s = min(boxes_far, key=lambda x: x[0])
                else:
                    return
                
                d, dx, dy = s
                adj = sensitivity
              
                if d < 7000:
                    mousekey.move_rel((int)(dx // adj), (int)(dy // adj))
                elif d < 70000:
                    mousekey.move_rel((int)(dx // (adj + 2)), (int)(dy // (adj + 2)))
                else:
                    mousekey.move_rel((int)(dx // (adj + 7)), (int)(dy //(adj + 7)))

class App:
    def __init__(self):
        self.mouse_detection = MouseDetection("best.pt")
        self.ui = MouseControlApp()
        self.ui.detection_handler = self
        
        # Hotkeys
        keyboard.add_hotkey('F5', self.decrease_sensitivity)
        keyboard.add_hotkey('F6', self.increase_sensitivity)
        keyboard.add_hotkey('F7', self.start_with_effect)  # Sửa lại thành gọi phương thức
        keyboard.add_hotkey('F8', self.stop_with_effect)

    def start_with_effect(self):
        self.ui.simulate_button_press(self.ui.start_button)  # Mô phỏng nhấn nút Bắt Đầu

    def stop_with_effect(self):
        self.ui.simulate_button_press(self.ui.stop_button)  # Mô phỏng nhấn nút Dừng
        
    def start_program(self):
        self.mouse_detection.is_running = True
        self.detect_loop()
        
    def stop_program(self):
        self.mouse_detection.is_running = False
        
    def detect_loop(self):
        if not self.mouse_detection.is_running:
            return
        self.mouse_detection.run_detection(self.ui.value.get())
        self.ui.popup.after(100, self.detect_loop)
        
    def increase_sensitivity(self):
        current = self.ui.value.get()
        if current < 10:
            new_value = float(f"{min(current + 0.5, 10):.1f}")
            self.ui.value.set(new_value)
    def decrease_sensitivity(self):
        current = self.ui.value.get()
        if current > 1:
            new_value =  float(f"{max(current - 0.5, 1):.1f}")
            self.ui.value.set(new_value)
    def run(self):
        self.ui.run()

# Run the application
if __name__ == "__main__":
    app = App()
    app.run()