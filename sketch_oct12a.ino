#include <Wire.h>
#include <MPU6050.h>
#include <SimpleKalmanFilter.h>  // Thêm thư viện SimpleKalmanFilter

MPU6050 mpu;
int16_t ax, ay, az, gx, gy, gz;
float vx, vy;

// Khởi tạo bộ lọc Kalman cho trục X và Y
SimpleKalmanFilter kalmanX(2.0, 1.0, 0.01);  // Q, R, P cho trục X
SimpleKalmanFilter kalmanY(2.0, 1.0, 0.01);  // Q, R, P cho trục Y


void setup() 
{
  Serial.begin(19200);
  pinMode(16, INPUT_PULLUP);  // LEFT CLICK
  pinMode(10, INPUT_PULLUP);  // Right click
  while (!Serial); // unless serial cable is connected, do nothing
  delay(4000);  // additional delay
  Wire.begin();
  mpu.initialize();
  if (!mpu.testConnection()) { while (1); }   // wait here infinitely till sensor initializes. 
  
  Serial.println("Sensor initialized");

}

void loop() 
{
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);


  // Chuyển đổi gx và gz thành vx và vy
  vx = -(gx + 260) / 150.0;
  vy = (gz + 100) / 150.0;

  // Lọc dữ liệu bằng bộ lọc Kalman
  vx = kalmanX.updateEstimate(vx);  // Dùng bộ lọc Kalman cho trục X
  vy = kalmanY.updateEstimate(vy);  // Dùng bộ lọc Kalman cho trục Y

  // In ra kết quả
  Serial.println(vx);
  Serial.println("a");
  Serial.println(vy);

  delay(5);
}
