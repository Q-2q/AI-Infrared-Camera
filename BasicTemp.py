############################################
# MLX90640 Adafruit lib - Basic Temperature
############################################

import time, board, busio
import numpy as np
import adafruit_mlx90640

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)         # Setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c)                           # Begin MLX90640 with I2C comms
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ   # set refresh rate

frame = np.zeros((24*32,))                                      # setup array for storing all 768 temperatures
while True:
    try:
        mlx.getFrame(frame)                                     # Read MLX temperatures into frame var
        break 
    except ValueError:
        continue                                                # if error, read again
    
print('Average MLX90640 Temperature: {0:2.1f}C'.\
      format(np.mean(frame)))
