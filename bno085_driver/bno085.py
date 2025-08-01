import time
from struct import unpack_from
from .constants import *
from .i2c_interface import I2CInterface

class BNO085:
    def __init__(self, bus=I2C_BUS, address=I2C_ADDR):
        self.i2c = I2CInterface(bus, address)

    def initialize(self):
        """
        Soft reset the sensor and clear packet state.
        """
        self.i2c.send_packet(CH_EXEC, bytearray([1]))
        time.sleep(0.5)
        self.i2c.send_packet(CH_EXEC, bytearray([1]))
        time.sleep(0.5)
        for _ in range(3):
            try:
                pkt = self.i2c.read_packet()
                if pkt:
                    print(f'Startup packet: {pkt.hex()}')
                time.sleep(0.1)
            except:
                pass

    def _build_feature_enable(self, report_id):
        buf = bytearray(17)
        buf[0] = CMD_SET_FEATURE
        buf[1] = report_id
        buf[5:9] = REPORT_INTERVAL.to_bytes(4, 'little')
        return buf

    def enable_feature(self, report_id):
        packet = self._build_feature_enable(report_id)
        self.i2c.send_packet(CH_CONTROL, packet)
        time.sleep(0.5)  # allow time for internal processing
        print(f"Feature 0x{report_id:02X} enabled.")

    def _send_command_request(self, command_id, parameters=None):
        buf = bytearray(12)
        buf[0] = CMD_COMMAND_REQUEST
        buf[1] = self.i2c.sequence[CH_CONTROL]
        buf[2] = command_id
        if parameters:
            for i, val in enumerate(parameters[:9]):
                buf[3 + i] = val
        self.i2c.send_packet(CH_CONTROL, buf)
        time.sleep(0.2)

    def begin_calibration(self):
        self._send_command_request(CMD_ME_CALIBRATE, [
            1, 1, 1, ME_CAL_CONFIG,
            0, 0, 0, 0, 0
        ])
        print("Calibration started...")

    def save_calibration(self):
        self._send_command_request(CMD_SAVE_DCD)
        print("Calibration saved to flash.")

    def read_sensor(self, retries=5):
        """
        Attempt to read an accelerometer or gyroscope report from the BNO085.
        Retries up to `retries` times, and handles bus timeouts gracefully.
        """
        for attempt in range(retries):
            try:
                pkt = self.i2c.read_packet()
            except TimeoutError:
                print("I2C read timeout — BNO085 may have stalled.")
                # Optional: Attempt soft reset and reinit here
                # self.initialize()
                return None
            except OSError as e:
                print(f"I2C OSError: {e}")
                return None

            if pkt:
                # Ignore too-short packets
                if len(pkt) < 16:
                    print("Packet too short, skipping...")
                    continue

                report_id = pkt[4]
                accuracy = pkt[6] & 0x03
                raw = [unpack_from("<h", pkt, offset)[0] for offset in (8, 10, 12)]

                if report_id == REPORT_ACCEL:
                    data = tuple(x * Q8 for x in raw)
                    # print(f"Accel data: {data}, Accuracy: {accuracy}")
                    return {"accel": data, "accuracy": accuracy}

                elif report_id == REPORT_GYRO:
                    data = tuple(x * Q9 for x in raw)
                    # print(f"Gyro data: {data}, Accuracy: {accuracy}")
                    return {"gyro": data, "accuracy": accuracy}

            time.sleep(0.01)
        return None


