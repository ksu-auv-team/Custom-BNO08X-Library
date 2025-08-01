from smbus2 import SMBus, i2c_msg
from .constants import DATA_BUFFER_SIZE

class I2CInterface:
    def __init__(self, bus, address):
        self.bus = SMBus(bus)
        self.address = address
        self.buffer = bytearray(DATA_BUFFER_SIZE)
        self.sequence = [0] * 6  # One per channel

    def send_packet(self, channel, data):
        length = len(data) + 4
        self.buffer[0:4] = bytearray([0, 0, channel, self.sequence[channel]])
        self.buffer[0:2] = (length).to_bytes(2, 'little')
        self.buffer[4:4+len(data)] = data
        self.sequence[channel] = (self.sequence[channel] + 1) % 256
        write = i2c_msg.write(self.address, self.buffer[:length])
        self.bus.i2c_rdwr(write)

    def read_packet(self):
        # Read 4-byte header
        header = i2c_msg.read(self.address, 4)
        self.bus.i2c_rdwr(header)
        header_bytes = bytes(header)
        length = int.from_bytes(header_bytes[0:2], 'little') & ~0x8000
        if length == 0:
            return None
        # Read rest of packet
        data = i2c_msg.read(self.address, length)
        self.bus.i2c_rdwr(data)
        return bytes(data)
