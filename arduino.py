import serial
import time
from pynput import keyboard
import mousekey  # Import thư viện mousekey

# Mở kết nối serial với Arduino
ser = serial.Serial('COM3', 9600)  # Thay 'COM3' bằng cổng của bạn
time.sleep(2)  # Chờ Arduino khởi động

# Đặt tốc độ di chuột dựa trên vx, vy
SPEED_FACTOR = 5  # Bạn có thể điều chỉnh hệ số tốc độ này
is_e_pressed = False

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
    try:
        if key.char == 'e':
            is_e_pressed = True  # Giữ phím 'e' thì không di chuyển chuột
    except AttributeError:
        pass

def on_release(key):
    global is_e_pressed
    try:
        if key.char == 'e':
            is_e_pressed = False  # Khi nhả phím 'e', chương trình di chuyển chuột lại
    except AttributeError:
        pass

print("Reading data and moving mouse...")
vx = 0
vy = 0
vx2 = 0
vy2 = 0
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

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
    print(vx)
    print(vy)
    
    if vy is not None and vx is not None and _ is None and not is_e_pressed:
        vx2 = abs(vx)
        vy2 = abs(vy)
        vx = int(vx)
        vy = int(vy)
        if vx2 + vy2 > 20:
            mousekey.move_rel(-vy * 3, vx * 3)  # Di chuyển chuột tương đối
        elif vx2 + vy2 > 10:
            mousekey.move_rel(-vy * 2, vx * 2)
        else:
            mousekey.move_rel(-vy, vx)
    
    time.sleep(0.005)  # Điều chỉnh tốc độ đọc dữ liệu

# Đừng quên đóng kết nối khi không dùng nữa
ser.close()
