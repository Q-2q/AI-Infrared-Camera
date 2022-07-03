#####################################
# MLX90640 Adafruit - Interplotion
#####################################

import time, board, busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt

from scipy import ndimage

print("Initializing MLX90640")
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)         # Setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c)                           # Begin MLX90640 with I2C comms
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ   # set refresh rate
mlx_shape = (24,32)
print("Initialized")                                           

mlx_interp_val = 10                                             # Interpolate pixcel on each diemension
mlx_interp_shape = (mlx_shape[0]*mlx_interp_val,
                    mlx_shape[1]*mlx_interp_val)                # New Shape

# Setting up the figure for plotting
plt.ion()                                                       # Enables Interacive plotting
fig,ax = plt.subplots(figsize=(12,9))
ax = fig.add_subplot(111)                                       # Add subplot
fig.subplots_adjust(0.05,0.05,0.95,0.95)                        # Getting rid of unnecessary padding
therm1 = ax.imshow(np.zeros(mlx_interp_shape),
                   interpolation='none',cmap=plt.cm.bwr,
                   vmin=25,vmax=45)                             # preemptive image
cbar = fig.colorbar(therm1)                                     # Setup colorbar for temperatues
cbar.set_label('Temperature [$^{circ}$C]',fontsize=14)          # Colorbar label

fig.canvas.draw()                                               # draw figure to copy background
ax_background = fig.canvas.copy_from_bbox(ax.bbox)              # Copy background
fig.show()                                                      # show the figure before blitting

frame = np.zeros((24*32,))                                      # setup array for storing all 768 temperatures

t_array = []
while True:
    t1 = time.monotonic()
    try:
        fig.canvas.restore_region(ax_background)                # restore background
        mlx.getFrame(frame)                                     # Read MLX temperatures into frame var
        data_array = np.fliplr(np.reshape(frame,mlx_shape))     # Reshape, flip data
        data_array = ndimage.zoom(data_array,mlx_interp_val)    # Interpolate
        therm1.set_data(np.fliplr(data_array))                  # flip left to right
        therm1.set_data(data_array)
        therm1.set_clim(vmin=np.min(data_array),
                        vmax=np.max(data_array))                # set bounds
        cbar.update_normal(therm1)                              # Update colorbar range
        plt.pause(0.001)                                        # Required
        
        ax.draw_artist(therm1)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()
        
        t_array.append(time.monotonic()-t1)
        print('Highest MLX90640 Temperature: {0:2.1f}C'.format(np.amax(frame)))
        print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
    except ValueError:
        continue
