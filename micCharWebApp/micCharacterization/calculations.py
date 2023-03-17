import numpy as np
import pandas as pd
from scipy import signal
from .constants import freqs, window, speed_noise_spl_dict, spl_speed, spl_src, vel_array, dir_fact
from .constants import tunnel_dist, temperature, relative_humidity, p_bar, p_ref

def calc_coeff(freqs, distance, temperature, rel_hum, p_bar, p_ref):
    p_sat_ref = p_sat_ref_easy(temperature)
    mol_conc_wv = mol_conc_water_vapor(rel_hum, p_sat_ref, p_bar, p_ref)
    oxy_freq = oxy_relax_freq(p_bar, p_ref, 100*mol_conc_wv)
    nit_freq = nit_relax_freq(temperature, p_bar, p_ref, 100*mol_conc_wv)
    abs_coeff_db = distance*absorption_coeff(temperature, p_bar, p_ref, freqs, oxy_freq, nit_freq)
    
    mol_mix = mol_mass_mix(mol_conc_wv)
    hcr_mix = heat_cap_ratio_mix(mol_conc_wv)
    sound_speed = speed_of_sound(temperature, mol_mix, hcr_mix)
    air_dens = air_density(temperature, p_bar, mol_mix)
    return abs_coeff_db, sound_speed, air_dens

def calc_snr_pred(freqs, noise_spl, src_spl, dir_fact, distance, vel_array, temperature, rel_hum, p_bar, p_ref):
    # vel_array = [src_wind_vel, uav_vel, uav_wind_vel]
    abs_coeff_db, sound_speed_const, air_dens = calc_coeff(freqs, 1, temperature, rel_hum, p_bar, p_ref)
    # sos_wind = sound_speed_const + vel_array[0] (src_wind_vel)
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

def db_array_to_mean(db_array):
    avg_ratio = np.mean(value_db_conv(db_array, 'ratio', 'power', 'value'))
    return value_db_conv(avg_ratio, 'ratio', 'power', 'db')

def find_avg_snr_db_dist_array(dist_array, name, snr_db=None, special_dist=tunnel_dist):
    if (name == None) or not ('13' in name or '15' in name or '18' in name or '20' in name):
        speed_spl = speed_noise_spl_dict['20']
    else:
        if '13' in name:
            speed_spl = speed_noise_spl_dict['13']
            # speed_spl = 76
        elif '15' in name:
            speed_spl = speed_noise_spl_dict['15']
            # speed_spl = 80
        elif '18' in name:
            speed_spl = speed_noise_spl_dict['18']
            # speed_spl = 86
        else:
            speed_spl = speed_noise_spl_dict['20']
            # speed_spl = 90
    if not type(dist_array) == np.ndarray:
        dist_array = [dist_array]
    snr_pred_db = calc_snr_pred(freqs, speed_spl, spl_src, dir_fact, special_dist, vel_array, temperature, relative_humidity, p_bar, p_ref)
    if snr_db and special_dist:
        diff = db_array_to_mean(snr_pred_db) - snr_db
    else:
        diff = 0
    
    snr_avg_db_dist_model = []
    snr_avg_db_dist = []
    for dist in dist_array:
        snr_avg_db_model = db_array_to_mean(calc_snr_pred(freqs, speed_spl, spl_src, dir_fact, dist, vel_array, temperature, relative_humidity, p_bar, p_ref))
        snr_avg_db_dist_model.append(snr_avg_db_model)
        snr_avg_db_dist.append(snr_avg_db_model - diff)
    if diff == 0:
        snr_avg_db_dist = None
    return dist_array, snr_avg_db_dist, snr_avg_db_dist_model

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
    # return (100*rel_hum*(p_sat_ref*p_ref/(p_bar)))/100

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
    # return (1/p_ref)*(24 + 40400*mol_conc_water_vapor*((0.02 + mol_conc_water_vapor)/(0.391 + mol_conc_water_vapor)))

# def nit_relax_freq(temperature, p_ref, mol_conc_water_vapor):
#     return (1/(p_ref/101325))*np.power(293.15/temperature, 0.5)*(9 + 280*mol_conc_water_vapor*np.exp(-4.17*(np.power(293.15/temperature, 1/3) - 1)))

def nit_relax_freq(temperature, p_bar, p_ref, mol_conc_water_vapor):
    return (p_bar/p_ref)*np.power(temperature/293.15, -0.5)*(9 + 280*mol_conc_water_vapor*np.exp(-4.17*(np.power(temperature/293.15, -1/3) - 1)))
    # return (1/p_ref)*np.power(temperature/293.15, -0.5)*(9 + 280*mol_conc_water_vapor*np.exp(-4.17*(np.power(temperature/293.15, -1/3) - 1)))

# def absorption_coeff(temperature, p_ref, freq, oxy_relax_freq, nit_relax_freq):
#     return (np.power(freq, 2)/(p_ref/101325))*(1.84*(10**-11)*np.power(temperature/293.15, 0.5) + np.power(temperature/293.15, -5/2)*(0.01278*(np.exp(-2239.1/temperature)/(oxy_relax_freq + np.power(freq, 2)/oxy_relax_freq)) + 0.1068*(np.exp(-3352/temperature)/(nit_relax_freq + np.power(freq, 2)/nit_relax_freq))))

def absorption_coeff(temperature, p_bar, p_ref, freq, oxy_relax_freq, nit_relax_freq):
    # return 10*np.log10(np.exp(np.power(freq, 2)*np.power(temperature/293.15, 1/2)*(1.84*(10**-11)*(p_ref/p_bar) + np.power(temperature/293.15, -3)*(0.01275*(np.exp(-2239.1/temperature)/(oxy_relax_freq + np.power(freq, 2)/oxy_relax_freq)) + 0.1068*(np.exp(-3352/temperature)/(nit_relax_freq + np.power(freq, 2)/nit_relax_freq))))))
    # return 10*np.log10(np.exp(np.power(freq/p_bar, 2)*(1.84*(10**-11)*np.power(p_bar/p_ref, -1)*np.power(temperature/293.15, 1/2) + np.power(temperature/293.15, -5/2)*(0.01275*(np.exp(-2239/temperature)/(oxy_relax_freq/p_bar + np.power(freq/p_bar, 2)/(oxy_relax_freq/p_bar))) + 0.1068*(np.exp(-3352/temperature)/(nit_relax_freq/p_bar + np.power(freq/p_bar, 2)/(nit_relax_freq/p_bar)))))))
    return 10*np.log10(np.exp(np.power(freq, 2)*(1.84*(10**-11)*np.power(p_bar/p_ref, -1)*np.power(temperature/293.15, 1/2) + np.power(temperature/293.15, -5/2)*(0.01275*np.exp(-2239/temperature)*(oxy_relax_freq/(np.power(freq, 2) + np.power(oxy_relax_freq, 2))) + 0.1068*np.exp(-3352/temperature)*(nit_relax_freq/(np.power(freq, 2) + np.power(nit_relax_freq, 2)))))))
    # return 10*np.log10(np.exp(np.power(freq/p_bar, 2)*(1.84*(10**-11)*np.power(p_bar/p_ref, -1)*np.power(temperature/293.15, 1/2) + np.power(temperature/293.15, -5/2)*(0.01275*np.exp(-2239/temperature)*((oxy_relax_freq/p_bar)/(np.power(freq/p_bar, 2) + np.power(oxy_relax_freq/p_bar, 2))) + 0.1068*np.exp(-3352/temperature)*((nit_relax_freq/p_bar)/(np.power(freq/p_bar, 2) + np.power(nit_relax_freq/p_bar, 2)))))))

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

def get_SNR_arrays(list_1, list_2, snr_type):
    # snr_type: Pure, Given Signal, Given Noise, System
    # list_1: sig, sig, noisy_sig, sig
    # list_2: noise, noisy_sig, noise, noisy_sig
    
    list_1_freq, list_1_data = signal.welch(x=list_1[1], fs=list_1[0])
    list_2_freq, list_2_data = signal.welch(x=list_2[1], fs=list_2[0])
    
    list_1_roll = pd.Series(list_1_data).rolling(window, center=True).mean().to_numpy()
    list_2_roll = pd.Series(list_2_data).rolling(window, center=True).mean().to_numpy()
    
    if snr_type == 'System':
        list_2_data = list_2_data - list_1_data
        list_2_roll = pd.Series(list_2_roll - list_1_roll).rolling(window, center=True).mean().to_numpy()
    
    snr_plain = []
    db_plain = []
    snr_rolled_before = []
    db_rolled_before = []
    for l1, l2, l1r, l2r in zip(list_1_data, list_2_data, list_1_roll, list_2_roll):
        if snr_type == 'Given Signal':
            this_data_ratio = 1/(((l2*1.25)/l1) - 1)
            this_roll_ratio = 1/(((l2r*1.25)/l1r) - 1)
        elif snr_type == 'Given Noise':
            this_data_ratio = ((l1*1.25)/l2) - 1
            this_roll_ratio = ((l1r*1.25)/l2r) - 1
        else:
            this_data_ratio = l1/l2
            this_roll_ratio = l1r/l2r
        snr_plain.append(this_data_ratio)
        db_plain.append(10*np.log10(this_data_ratio))
        snr_rolled_before.append(this_roll_ratio)
        db_rolled_before.append(10*np.log10(this_roll_ratio))
    
    # db_rolled_after = 10*np.log10(pd.Series(snr_plain).rolling(win, center=True).mean().to_numpy())
    db_rolled_both = 10*np.log10(pd.Series(snr_rolled_before).rolling(window, center=True).mean().to_numpy())
    
    return list_1_freq, db_plain, db_rolled_before, db_rolled_both