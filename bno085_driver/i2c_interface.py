from smbus2 import SMBus, i2c_msg

class I2CInterface:
    def __init__(self, bus_num: int, device_address: int):
        self.bus = SMBus(bus_num)
        self.address = device_address

    def write(self, data: bytes):
        self.bus.write_i2c_block_data(self.address, 0, list(data))

    def read(self, length: int) -> bytes:
        read = i2c_msg.read(self.address, length)
        self.bus.i2c_rdwr(read)
        return bytes(list(read))
