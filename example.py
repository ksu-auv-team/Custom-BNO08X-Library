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
    data = bno.read_sensor()
    if data:
        if "accel" in data:
            print("Accel:", data["accel"])
        if "gyro" in data:
            print("Gyro:", data["gyro"])
    else:
        print("No data received")
    time.sleep(0.05)
