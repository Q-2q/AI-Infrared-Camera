#####################################
# MLX90640 Adafruit - Plotting Heatmap 1
#####################################

import time, board, busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt

print("Initializing MLX90640")
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)         # Setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c)                           # Begin MLX90640 with I2C comms
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ   # set refresh rate
mlx_shape = (24,32)
print("Initialized")

# Setting up the figure for plotting
plt.ion()                                                       # Enables Interacive plotting
fig,ax = plt.subplots(figsize=(12,7))
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60)          # Start plot with Zeros
cbar = fig.colorbar(therm1)                                     # Setup colorbar for temperatues
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14)         # Colorbar label

frame = np.zeros((24*32,))                                      # setup array for storing all 768 temperatures
t_array = []
while True:
    t1 = time.monotonic()
    try:
        mlx.getFrame(frame)                                     # Read MLX temperatures into frame var
        data_array = (np.reshape(frame,mlx_shape))              # Reshape to 24x32
        therm1.set_data(np.fliplr(data_array))                  # flip left to right
        therm1.set_clim(vmin=np.min(data_array),
                        vmax=np.max(data_array))                # set bounds
        cbar.update_normal(therm1)                              # Update colorbar range
        plt.pause(0.001)                                        # Required
        t_array.append(time.monotonic()-t1)
        print('Average MLX90640 Temperature: {0:2.1f}C'.format(np.mean(frame)))
        print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
    except ValueError:
        continue
