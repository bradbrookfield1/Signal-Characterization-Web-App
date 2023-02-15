import numpy as np

def calc_coeff(freqs, distance, temperature, rel_hum, p_bar, p_ref):
    p_sat_ref = p_sat_ref_easy(temperature)
    mol_conc_wv = mol_conc_water_vapor(rel_hum, p_sat_ref, p_bar, p_ref)
    oxy_freq = oxy_relax_freq(p_bar, p_ref, mol_conc_wv)
    nit_freq = nit_relax_freq(temperature, p_bar, p_ref, mol_conc_wv)
    abs_coeff_db = distance*absorption_coeff(temperature, p_bar, p_ref, freqs, oxy_freq, nit_freq)
    
    mol_mix = mol_mass_mix(mol_conc_wv)
    hcr_mix = heat_cap_ratio_mix(mol_conc_wv)
    sound_speed = speed_of_sound(temperature, mol_mix, hcr_mix)
    air_dens = air_density(temperature, p_bar, mol_mix)
    return abs_coeff_db, sound_speed, air_dens

def calc_snr_pred(freqs, noise_spl, src_spl, dir_fact, distance, vel_array, temperature, rel_hum, p_bar, p_ref):
    # vel_array = [src_wind_vel, uav_vel, uav_wind_vel]
    abs_coeff_db, sound_speed_const, air_dens = calc_coeff(freqs, 1, temperature, rel_hum, p_bar, p_ref)
    # sos_wind = sound_speed_const + vel_array[0]
    src_p_acc = value_db_conv(src_spl, 'value', 'pressure', 'value')
    src_intensity = p_acc_intensity_conv(src_p_acc, 'pressure', sound_speed_const, air_dens)
    src_pwr = pwr_intensity_conv(src_intensity, 'intensity', 1, dir_fact)
    src_pwr_db = value_db_conv(src_pwr, 'value', 'power', 'db')
    
    src_spl_from_dist = src_pwr_db - 10*np.log10(4*np.pi*(distance**2)/dir_fact) - abs_coeff_db*distance
    src_p_acc_dist = value_db_conv(src_spl_from_dist, 'value', 'pressure', 'value')
    src_int_dist = p_acc_intensity_conv(src_p_acc_dist, 'pressure', sound_speed_const, air_dens)
    src_pwr_dist = pwr_intensity_conv(src_int_dist, 'intensity', 1, dir_fact)
    src_pwr_db_dist = value_db_conv(src_pwr_dist, 'value', 'power', 'db')

    new_noise_spl = noise_spl + 50*np.log10((vel_array[1] + vel_array[2])/vel_array[1])
    noise_p_acc = value_db_conv(new_noise_spl, 'value', 'pressure', 'value')
    noise_intensity = p_acc_intensity_conv(noise_p_acc, 'pressure', sound_speed_const, air_dens)
    noise_pwr = pwr_intensity_conv(noise_intensity, 'intensity', 1, dir_fact)
    noise_pwr_db = value_db_conv(noise_pwr, 'value', 'power', 'db')
    
    return src_pwr_db_dist - noise_pwr_db
    
def value_db_conv(val, val_rat, val_type, result_type, ref=10**-12):
    # val_rat options: value, ratio
    # val_type options: intensity, power, pressure, voltage, current
    # result_type options: db, value
    factor = 10
    if val_type == 'pressure' or val_type == 'voltage' or val_type == 'current':
        factor = 20
        ref = 2*(10**-5) if val_type == 'pressure' else ref
    if result_type == 'value' and val_rat == 'value':
        return (10**(val/factor))*ref
    elif result_type == 'value' and val_rat == 'ratio':
        return 10**(val/factor)
    elif result_type == 'db' and val_rat == 'value':
        return factor*np.log10(val/ref)
    else: # result_type == 'db' and val_rat == 'ratio'
        return factor*np.log10(val)

def p_acc_intensity_conv(val, in_type, sound_speed, air_dens):
    if in_type == 'pressure':
        return np.power(val, 2)/(air_dens*sound_speed)
    else: # in_type == 'intensity'
        return np.sqrt(val*air_dens*sound_speed)

def pwr_intensity_conv(val, in_type, distance, dir_fact):
    if in_type == 'power':
        return val*dir_fact/(4*np.pi*(distance**2))
    else: # in_type == 'intensity'
        return val*4*np.pi*(distance**2)/dir_fact

def p_sat_ref_easy(temperature):
    return np.power(10, -6.8346*np.power(273.16/temperature, 1.261) + 4.6151)

# def p_sat_ref_hard(temperature):
#     return np.power(10, 10.79586*(1 - (273.16/temperature)) - 5.02808*np.log10(temperature/273.16) + 1.50474*(10**-4)*(1 - np.power(10, -8.29692*((temperature/273.16) - 1))) - 4.2873*(10**-4)*(1 - np.power(10, -4.76955*((273.16/temperature) - 1))) - 2.2195983)

def mol_conc_water_vapor(rel_hum, p_sat_ref, p_bar, p_ref):
    return (100*rel_hum*(p_sat_ref/(p_bar/p_ref)))/100

def mol_mass_mix(mol_conc_water_vapor):
    return mol_conc_water_vapor*0.018016 + (1 - mol_conc_water_vapor)*0.02897

def heat_cap_ratio_mix(mol_conc_water_vapor):
    return 1/(mol_conc_water_vapor/(1.33 - 1) + (1 - mol_conc_water_vapor)/(1.4 - 1)) + 1

def speed_of_sound(temperature, mol_mass_mix, heat_cap_ratio_mix):
    return np.sqrt(heat_cap_ratio_mix*8.314462*temperature/mol_mass_mix)

def air_density(temperature, p_bar, mol_mass_mix):
    return mol_mass_mix*p_bar/(8.314462*temperature)

# def oxy_relax_freq(p_ref, mol_conc_water_vapor):
#     return (1/(p_ref/101325))*(24 + 40400*mol_conc_water_vapor*((0.02 + mol_conc_water_vapor)/(0.391 + mol_conc_water_vapor)))

def oxy_relax_freq(p_bar, p_ref, mol_conc_water_vapor):
    return (p_bar/p_ref)*(24 + 40400*mol_conc_water_vapor*((0.02 + mol_conc_water_vapor)/(0.391 + mol_conc_water_vapor)))

# def nit_relax_freq(temperature, p_ref, mol_conc_water_vapor):
#     return (1/(p_ref/101325))*np.power(293.15/temperature, 0.5)*(9 + 280*mol_conc_water_vapor*np.exp(-4.17*(np.power(293.15/temperature, 1/3) - 1)))

def nit_relax_freq(temperature, p_bar, p_ref, mol_conc_water_vapor):
    return (p_bar/p_ref)*np.power(293.15/temperature, 0.5)*(9 + 280*mol_conc_water_vapor*np.exp(-4.17*(np.power(293.15/temperature, 1/3) - 1)))

# def absorption_coeff(temperature, p_ref, freq, oxy_relax_freq, nit_relax_freq):
#     return (np.power(freq, 2)/(p_ref/101325))*(1.84*(10**-11)*np.power(temperature/293.15, 0.5) + np.power(temperature/293.15, -5/2)*(0.01278*(np.exp(-2239.1/temperature)/(oxy_relax_freq + np.power(freq, 2)/oxy_relax_freq)) + 0.1068*(np.exp(-3352/temperature)/(nit_relax_freq + np.power(freq, 2)/nit_relax_freq))))

def absorption_coeff(temperature, p_bar, p_ref, freq, oxy_relax_freq, nit_relax_freq):
    return 20*np.log10(np.exp(np.power(freq, 2)*np.power(temperature/293.15, 1/2)*(1.84*(10**-11)*(p_ref/p_bar) + np.power(temperature/293.15, -3)*(0.01275*(np.exp(-2239.1/temperature)/(oxy_relax_freq + np.power(freq, 2)/oxy_relax_freq)) + 0.1068*(np.exp(-3352/temperature)/(nit_relax_freq + np.power(freq, 2)/nit_relax_freq))))))

def fft_vectorized(sig, r_harmonic):
    sig = np.asarray(sig, dtype=float)
    big_N = sig.shape[0]
    if np.log2(big_N) % 1 > 0:
        raise ValueError("must be a power of 2")
    min_N = min(big_N, 2)
    n = np.arange(min_N)
    k = n[:, None]
    
    exp_term = np.exp(-2j * np.pi * n * k * r_harmonic / min_N)
    sig = sig.reshape(min_N, -1)
    sum_term = np.dot(exp_term, sig)
    while sum_term.shape[0] < big_N:
        even = sum_term[:, :int(sum_term.shape[1] / 2)]
        odd = sum_term[:, int(sum_term.shape[1] / 2):]
        terms = np.exp(-1j * np.pi * np.arange(sum_term.shape[0]) / sum_term.shape[0])[:, None]
        sum_term = np.vstack([even + terms * odd, even - terms * odd])
    return sum_term.ravel()