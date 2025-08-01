from bno085_driver.bno085 import BNO085
from bno085_driver.constants import REPORT_ACCEL, REPORT_GYRO
import time

bno = BNO085()
bno.initialize()
bno.enable_feature(REPORT_ACCEL)
bno.enable_feature(REPORT_GYRO)

bno.begin_calibration()
time.sleep(5)
bno.save_calibration()

while True:
    bno.update()
    accel = bno.get_acceleration()
    gyro = bno.get_angular_velocity()

    if accel and gyro:
        print(f"Acceleration: {accel}, Gyro: {gyro}")
    elif not accel and not gyro:
        print("No data available yet.")
    elif accel and not gyro:
        print(f"Acceleration: {accel}")
    elif gyro and not accel:
        print(f"Gyro: {gyro}")
    time.sleep(0.05)
