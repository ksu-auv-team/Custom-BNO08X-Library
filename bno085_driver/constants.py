# I2C bus & address
I2C_BUS = 1
I2C_ADDR = 0x4B

# SH-2 channel numbers
CH_EXEC = 1
CH_CONTROL = 2
CH_REPORTS = 3

# SH-2 Report IDs
REPORT_ACCEL = 0x05
REPORT_GYRO = 0x07

# SH-2 Command IDs
CMD_SET_FEATURE = 0xFD
CMD_COMMAND_REQUEST = 0xF2
CMD_SAVE_DCD = 0x06
CMD_ME_CALIBRATE = 0x07
ME_CAL_CONFIG = 0x00

# Report timing
REPORT_INTERVAL = 20000  # 20 ms

# Scaling factors
Q8 = 2 ** -8
Q9 = 2 ** -9

# Buffer size
DATA_BUFFER_SIZE = 512
