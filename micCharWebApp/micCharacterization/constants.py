import numpy as np

speed_noise_spl_dict = {'13': 80, '15': 84, '18': 87.5, '20': 90}   # m/s: dB SPL
# speed_noise_spl_dict = {'13': 89, '15': 92, '18': 97, '20': 99}   # m/s: dB SPL
spl_speed = speed_noise_spl_dict['18']
spl_src = 100
dir_fact = 2
vel_array = [0, 18, 0]
# vel_array = [src_wind_vel, uav_vel, uav_wind_vel]

window = 13
# freqs = np.linspace(1, 1000000, 100000)                                   # Hz
freqs = np.logspace(1, 5, 100000)                                   # Hz
p_bar = 101425                                                      # Pascals
p_ref = 101325                                                      # Pascals
relative_humidity = 0.5                                             # Decimal
temperature = 20                                                    # Celcius
# distance = 2.5                                                      # Meters
distance = 100                                                      # Meters
tunnel_dist = 2.5                                                   # Meters

rel_hum_array = [i/10 for i in range(11)]                   # Decimal (0, 0.1, 0.2, ..., 1)
# rel_hum_array = np.logspace(0, 2, 5)/100                   # Decimal (0, 0.1, 0.2, ..., 1)
temp_array = [((i*5 - 20) + 273.15) for i in range(9)]      # Kelvin (-20, -15, -10, ..., 20 deg C)
# temp_array = [((i*14 - 20) + 273.15) for i in range(5)]      # Kelvin (-20, -15, -10, ..., 20 deg C)
dist_array_lin = np.linspace(1, 100, 10)                     # Meters
dist_array_log = np.logspace(0, 2, 10)
dist_array_big = np.linspace(1, 100, 100)
p_bar_array = np.linspace(101325, 151325, 11)

temperature = temperature + 273.15                          # To Kelvin
# freqs = freqs/(p_bar/101325)                                # Normalized by barometric pressure

# find_graphs()
pred_harm = 5
stat_norm = False
filter_sigs = False
low_high = [50, 3999]
order = 4

# Kernel functions
dim_mult = 10
# Kernel type list: 'additive_chi2', 'chi2', 'linear', 'poly' or 'polynomial', 'rbf', 'laplacian', 'sigmoid', 'cosine'
kernel_type = 'rbf'
gamma = 1.0
degree = 3.0
coeff = 1.0