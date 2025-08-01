import time
from struct import unpack_from
from .constants import *
from .i2c_interface import I2CInterface


class BNO085:
    def __init__(self, bus=I2C_BUS, address=I2C_ADDR):
        self.i2c = I2CInterface(bus, address)
        self.accel = None
        self.gyro = None

    def initialize(self):
        """
        Soft reset the sensor and flush startup packets.
        """
        self.i2c.send_packet(CH_EXEC, bytearray([1]))
        time.sleep(0.5)
        self.i2c.send_packet(CH_EXEC, bytearray([1]))
        time.sleep(0.5)
        for _ in range(3):
            try:
                self.i2c.read_packet()
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
        """
        Enable a specific sensor data report.
        """
        packet = self._build_feature_enable(report_id)
        self.i2c.send_packet(CH_CONTROL, packet)
        time.sleep(0.5)

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
        """
        Start accelerometer and gyroscope calibration.
        """
        self._send_command_request(CMD_ME_CALIBRATE, [
            1, 1, 1, ME_CAL_CONFIG,
            0, 0, 0, 0, 0
        ])

    def save_calibration(self):
        """
        Save current calibration to flash memory.
        """
        self._send_command_request(CMD_SAVE_DCD)

    def _parse_packet(self, pkt):
        """
        Parse a raw SH-2 report packet into accel or gyro data.
        """
        if len(pkt) < 16:
            return

        report_id = pkt[4]
        accuracy = pkt[6] & 0x03
        raw = [unpack_from("<h", pkt, offset)[0] for offset in (8, 10, 12)]

        if report_id == REPORT_ACCEL:
            self.accel = tuple(x * Q8 for x in raw)
        elif report_id == REPORT_GYRO:
            self.gyro = tuple(x * Q9 for x in raw)

    def _poll_once(self):
        try:
            pkt = self.i2c.read_packet()
            if pkt:
                self._parse_packet(pkt)
        except (TimeoutError, OSError):
            pass

    def update(self, retries=5):
        """
        Poll the BNO085 for new packets.
        """
        for _ in range(retries):
            self._poll_once()
            if self.accel and self.gyro:
                break
            time.sleep(0.01)

    def get_acceleration(self):
        """
        Returns most recent acceleration data as (x, y, z) in m/s².
        """
        return self.accel

    def get_angular_velocity(self):
        """
        Returns most recent angular velocity as (x, y, z) in rad/s.
        """
        return self.gyro
