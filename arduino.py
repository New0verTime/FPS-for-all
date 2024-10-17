import serial
import time
from pynput import keyboard, mouse
import mousekey

# Mở kết nối serial với Arduino
ser = serial.Serial('COM3', 9600)  # Thay 'COM3' bằng cổng của bạn
time.sleep(2)  # Chờ Arduino khởi động

# Đặt tốc độ di chuột dựa trên vx, vy
SPEED_FACTOR = 5  # Bạn có thể điều chỉnh hệ số tốc độ này
is_e_pressed = False
is_z_pressed = False
def read_value():
    while True:
        line = ser.readline().decode('latin-1').strip()  # Đọc một dòng dữ liệu từ Arduino
        if line == 'a':  # Dấu hiệu để phân biệt giữa các giá trị
            return None
        try:
            return float(line)
        except ValueError:
            return None

def on_press(key):
    global is_e_pressed
    global is_z_pressed
    try:
        if key.char == 'e':
            is_e_pressed = True  # Giữ phím 'e'
        if key.char == 'z':
            is_z_pressed = True
    except AttributeError:
        pass

def on_release(key):
    global is_e_pressed
    global is_z_pressed
    try:
        if key.char == 'e':
            is_e_pressed = False  # Khi nhả phím 'e', ngừng click chuột
        if key.char == 'z':
            is_z_pressed = False
    except AttributeError:
        pass

print("Reading data and moving mouse...")
vx = 0
vy = 0
vx2 = 0
vy2 = 0
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Khởi tạo đối tượng mouse để sử dụng click chuột
mouse_controller = mouse.Controller()

while True:
    vx = read_value()
    if vx is None:
        vx = read_value()
        vx = read_value()
    _ = read_value()  # Đây là để bỏ qua ký tự 'a'
    if _ is not None:
        vx = _
        _ = read_value()
    vy = read_value()
    
    if vy is not None and vx is not None and _ is None:
        vx2 = abs(vx)
        vy2 = abs(vy)
        vx = int(vx/1.5)
        vy = int(vy/1.5)
        if vx2 + vy2 > 1 and is_z_pressed == False:
            mousekey.move_rel(-vy, vx)
    
    # Thực hiện click chuột trái nếu phím 'e' đang được giữ
    if is_e_pressed:
        mousekey.left_click()  # Click chuột trái
    
    time.sleep(0.005)  # Điều chỉnh tốc độ đọc dữ liệu

# Đừng quên đóng kết nối khi không dùng nữa
ser.close()
