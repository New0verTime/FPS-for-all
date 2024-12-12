import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import keyboard
import os
import sys

class MouseControlApp:
    def __init__(self):
        # Sử dụng ttkbootstrap để tạo root window
        self.root = ttk.Window(themename="flatly")
        self.root.withdraw()

        # Cửa sổ popup với giao diện hiện đại
        self.popup = ttk.Toplevel(self.root)
        self.popup.title("Intelligent Mouse Control")
        self.popup.geometry("550x650")
        self.popup.resizable(False, False)
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Fonts
        self.title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        self.label_font = font.Font(family="Segoe UI", size=10)
        self.button_font = font.Font(family="Segoe UI", size=11, weight="bold")
        self.detection_handler = None

        # Variables
        self.value = tk.DoubleVar(value=5.5)
        self.status_text = tk.StringVar(value="Ready")
        self.is_running = False

        # Create UI
        self.create_detailed_ui()

    def create_detailed_ui(self):
        # Main container
        main_frame = ttk.Frame(self.popup)
        main_frame.pack(expand=True, fill=BOTH, padx=20, pady=20)

        # Tạo Notebook
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill=BOTH)

        # Tab Giới Thiệu
        intro_frame = ttk.Frame(notebook)
        notebook.add(intro_frame, text="Giới Thiệu")
        
        # Tiêu đề giới thiệu
        intro_title = ttk.Label(
            intro_frame, 
            text="Intelligent Mouse Control", 
            font=self.title_font,
            bootstyle="primary"
        )
        intro_title.pack(pady=20)

        # Mô tả chức năng
        intro_desc = ttk.Label(
        intro_frame, 
        text="🎯 Intelligent Mouse Control 🖱️\n\n"
        "🚀 Ứng dụng điều khiển chuột thông minh\n"
        "💡 Sử dụng AI để theo dõi và điều khiển con trỏ chuột\n\n"
        "✨ Bỏ chuột xuống đi, chúng ta có Aim Assistant rồi! \n"
        "🎮 FPS bình đẳng cho tất cả, ngay cả khi bạn không có tay phải!\n\n"
        "🤖 Aim Assistant tích hợp AI thông minh: \n"
        "   • Tự động khóa mục tiêu với độ chính xác tuyệt đối\n" 
        "   • Biến bạn thành tay thiện xạ chỉ trong tích tắc!\n\n"
        "🌟 Cảm biến chuyển động tiên tiến: \n"
        "   • Điều khiển dễ dàng chỉ với một vài cử động đầu\n"
        "   • Giữ sự thoải mái trong suốt trận chiến",
        font=self.label_font,
        justify='center'  # Thêm thuộc tính này để căn giữa văn bản
        )   
        intro_desc.pack(pady=10)
       

        # Tab Hướng Dẫn
        guide_frame = ttk.Frame(notebook)
        notebook.add(guide_frame, text="Hướng Dẫn")

        guide_title = ttk.Label(
            guide_frame, 
            text="Cách Sử Dụng", 
            font=self.title_font,
            bootstyle="primary"
        )
        guide_title.pack(pady=20)

        guide_steps = [
            "1. Mở ứng dụng",
            "2. Điều chỉnh độ nhạy nếu cần",
            "3. Nhấn F8 để bắt đầu điều khiển",
            "4. Di chuyển để xem hiệu quả",
            "5. Nhấn F9 để dừng điều khiển"
        ]

        for step in guide_steps:
            ttk.Label(guide_frame, text=step, font=self.label_font).pack(anchor='w', padx=50, pady=5)
        hotkey_label_intro = ttk.Label(guide_frame, text="Phím tắt", font = self.title_font)
        hotkey_label_intro.pack(pady=10)
        hotkey_frame = ttk.Frame(guide_frame)
        hotkey_frame.pack(pady=10)

        hotkey_info = [
            ("F5", "Giảm độ nhạy", "info"),
            ("F6", "Tăng độ nhạy", "info"),
            ("F7", "Bắt đầu điều khiển", "success"),
            ("F8", "Dừng điều khiển", "danger")
        ]

        for key, desc, style in hotkey_info:
            hotkey_label = ttk.Frame(hotkey_frame)
            hotkey_label.pack(fill=X, pady=5 , padx=50)
            
            ttk.Label(hotkey_label, text=key, 
                    bootstyle=style, 
                    width=6).pack(side=LEFT)
            
            ttk.Label(hotkey_label, text=desc).pack(side=LEFT)
            
        # Tab Điều Chỉnh
        adjustment_frame = ttk.Frame(notebook)
        notebook.add(adjustment_frame, text="Điều Chỉnh")

        # Tiêu đề độ nhạy
        ttk.Label(
            adjustment_frame, 
            text="Độ Nhạy Chuột", 
            font=self.title_font,
            bootstyle="primary"
        ).pack(pady=20)

        # Thanh trượt độ nhạy
        sensitivity_frame = ttk.Frame(adjustment_frame)
        sensitivity_frame.pack(pady=10)

        # Sử dụng ttk.Scale
        sensitivity_scale = ttk.Scale(
            sensitivity_frame, 
            from_=1, 
            to=10, 
            variable=self.value,
            length=400
        )
        sensitivity_scale.pack(pady=10)

        # Hiển thị giá trị độ nhạy
        sensitivity_value_label = ttk.Label(
            sensitivity_frame, 
            textvariable=self.value,
            font=self.label_font
        )
        sensitivity_value_label.pack()

        # Nút điều khiển
        button_frame = ttk.Frame(adjustment_frame)
        button_frame.pack(pady=20)

        # Nút Bắt Đầu
        self.start_button = ttk.Button(
            button_frame, 
            text="Bắt Đầu Điều Khiển", 
            command=self.start_program,
            bootstyle="success"
        )
        self.start_button.pack(side=LEFT, padx=10)
        
        # Nút Dừng
        self.stop_button = ttk.Button(
            button_frame, 
            text="Dừng Điều Khiển", 
            command=self.stop_program,
            bootstyle="danger"
        )
        self.stop_button.pack(side=LEFT, padx=10)

        # Trạng thái
        self.status_label = ttk.Label(
            adjustment_frame, 
            textvariable=self.status_text, 
            bootstyle="secondary",
            font=self.label_font
        )
        self.status_label.pack(pady=(20, 0))
    def start_program(self):
        if hasattr(self, 'detection_handler'):
            self.detection_handler.start_program()
        self.is_running = True
        self.status_text.set("Tracking Started ✓")
        self.show_overlay_message("Đã bắt đầu sử dụng aimbot")
    def update_value(self, _):
        # update giá trị của thanh trượt 
        rounded_value = round(self.value.get() * 2) / 2
        self.value.set(rounded_value)
        self.label.config(text=f"Current value: {rounded_value}")
    def stop_program(self):
        if hasattr(self, 'detection_handler'):
            self.detection_handler.stop_program()
        self.is_running = False
        self.status_text.set("Tracking Stopped ✗")
        self.show_overlay_message("Đã dừng sử dụng aimbot")
    def simulate_button_press(self, button):
        # Đưa focus vào nút
        button.focus()
        # Mô phỏng trạng thái nhấn nút
        button.state(['pressed'])
        # Gọi lệnh của nút
        button.invoke()
        # Sau một khoảng thời gian ngắn, trả lại trạng thái bình thường
        self.popup.after(100, lambda: [button.state(['!pressed']), button.focus_set()])
    def show_overlay_message(self, message,duration=2000):
        # Tạo cửa sổ thông báo không có viền
        overlay = tk.Toplevel(self.root)
        overlay.overrideredirect(True)  # Loại bỏ viền và thanh tiêu đề
        overlay.attributes('-topmost', True)  # Hiển thị trên tất cả các cửa sổ

        # Đặt kích thước và vị trí
        overlay.geometry('300x150+{}+{}'.format(
            self.root.winfo_screenwidth() // 2 -150  ,
           0
        ))

        # Tạo khung chứa thông báo
        if message == "Đã bắt đầu sử dụng aimbot":
            frame = ttk.Frame(overlay, bootstyle="success")
            label = ttk.Label(
                frame, 
                text=message, 
                font=("Segoe UI", 14, "bold"),
                bootstyle="inverse-success"
            )
            sublabel = ttk.Label(
                frame, 
                text="Ấn F9 để dừng", 
                font=("Segoe UI", 10, "bold"),
                bootstyle="inverse-success"
            )
        else:
            frame = ttk.Frame(overlay, bootstyle="danger")
            label = ttk.Label(
                frame, 
                text=message, 
                font=("Segoe UI", 14, "bold"),
                bootstyle="inverse-danger"
            )
            sublabel = ttk.Label(
                frame, 
                text="Ấn F8 để bắt đầu lại", 
                font=("Segoe UI", 10, "bold"),
                bootstyle="inverse-danger"
            )
        frame.pack(fill=tk.BOTH, expand=True)

        # Nhãn thông báo
       
        label.pack(fill=tk.X, padx=20, pady=(20, 10)) 
        sublabel.pack(fill=tk.X, padx=20, pady=(10, 20)) 
        # Hẹn giờ đóng thông báo
        def close_overlay():
            overlay.destroy()

        overlay.after(duration, close_overlay)

    def on_closing(self):
        # Stop the program and close the window
        self.is_running = False
        self.popup.destroy()
        self.root.quit()

    def run(self):
        self.popup.mainloop()

# Khởi chạy ứng dụng
if __name__ == "__main__":
    app = MouseControlApp()
    app.run()