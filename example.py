from bno085_driver.bno085 import BNO085
import time


bno = BNO085(bus_num=7)
bno.initialize()
bno.enable_sensor_reports()

while True:
    data = bno.get_sensor_data()
    ax, ay, az = data['accel']
    gx, gy, gz = data['gyro']
    print(f"Accel: X={ax:.3f} Y={ay:.3f} Z={az:.3f} | Gyro: Roll={gx:.3f} Pitch={gy:.3f} Yaw={gz:.3f}")
    time.sleep(0.1)
