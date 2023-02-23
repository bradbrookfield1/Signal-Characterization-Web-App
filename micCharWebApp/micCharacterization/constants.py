import numpy as np

speed_noise_spl_dict = {'13': 80, '15': 84, '18': 87.5, '20': 90}   # m/s: dB SPL
spl_speed = speed_noise_spl_dict['18']
spl_src = 100
dir_fact = 2
vel_array = [0, 18, 0]
# vel_array = [src_wind_vel, uav_vel, uav_wind_vel]

window = 13
freqs = np.linspace(1, 1000, 100)                                   # Hz
p_bar = 101425                                                      # Pascals
p_ref = 101325                                                      # Pascals
relative_humidity = 0.5                                             # Decimal
temperature = 20                                                    # Celcius
distance = 2.5                                                      # Meters
tunnel_dist = 2.5                                                   # Meters

rel_hum_array = [i/10 for i in range(11)]                   # Decimal (0, 0.1, 0.2, ..., 1)
temp_array = [((i*5 - 20) + 273.15) for i in range(9)]      # Kelvin (-20, -15, -10, ..., 20 deg C)
dist_array_lin = np.linspace(1, 15, 10)                     # Meters
dist_array_log = np.logspace(0, 2, 10)
dist_array_big = np.linspace(1, 100, 100)
p_bar_array = np.linspace(101325, 151325, 11)

temperature = temperature + 273.15                          # To Kelvin
# freqs = freqs/(p_bar/101325)                                # Normalized by barometric pressure