from bno085_driver.bno085 import BNO085
from bno085_driver.constants import REPORT_ACCEL, REPORT_GYRO
import time

bno = BNO085()
bno.initialize()
time.sleep(2)
bno.enable_feature(REPORT_ACCEL)
bno.enable_feature(REPORT_GYRO)

bno.begin_calibration()
time.sleep(5)
bno.save_calibration()

while True:
    data = bno.read_sensor()
    if data:
        print(f"Accel: {data['accel'] if 'accel' in data else None}, Gyro: {data['gyro'] if 'gyro' in data else None}")
    else:
        print("No data received")
    time.sleep(0.05)
