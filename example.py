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

    if accel:
        print(f"Accel: X={accel[0]:.3f}, Y={accel[1]:.3f}, Z={accel[2]:.3f}")
    if gyro:
        print(f"Gyro : X={gyro[0]:.3f}, Y={gyro[1]:.3f}, Z={gyro[2]:.3f}")
    time.sleep(0.05)
