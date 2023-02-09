import numpy as np

def calc_coeff(freqs, distance, temperature, rel_hum, p_bar, p_ref):
    p_sat_ref = p_sat_ref_easy(temperature)
    mol_conc_wv = mol_conc_water_vapor(rel_hum, p_sat_ref, p_bar, p_ref)
    oxy_freq = oxy_relax_freq(p_ref, mol_conc_wv)
    nit_freq = nit_relax_freq(temperature, p_ref, mol_conc_wv)
    abs_coeff_np = distance*absorption_coeff(temperature, p_ref, freqs, oxy_freq, nit_freq)
    abs_coeff = np.exp(abs_coeff_np)
    abs_coeff_db = 20*np.log10(abs_coeff)
    return abs_coeff_db

def p_sat_ref_easy(temperature):
    return np.power(10, -6.8346*np.power(273.16/temperature, 1.261) + 4.6151)

def p_sat_ref_hard(temperature):
    return np.power(10, 10.79586*(1 - (273.16/temperature)) - 5.02808*np.log10(temperature/273.16) + 1.50474*(10**-4)*(1 - np.power(10, -8.29692*((temperature/273.16) - 1))) - 4.2873*(10**-4)*(1 - np.power(10, -4.76955*((273.16/temperature) - 1))) - 2.2195983)

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

def oxy_relax_freq(p_ref, mol_conc_water_vapor):
    return (1/(p_ref/101325))*(24 + 4.04*np.power(10, 4)*mol_conc_water_vapor*((0.02 + mol_conc_water_vapor)/(0.391 + mol_conc_water_vapor)))

def nit_relax_freq(temperature, p_ref, mol_conc_water_vapor):
    return (1/(p_ref/101325))*np.power(293.15/temperature, 0.5)*(9 + 280*mol_conc_water_vapor*np.exp(-4.17*(np.power(293.15/temperature, 1/3) - 1)))

def absorption_coeff(temperature, p_ref, freq, oxy_relax_freq, nit_relax_freq):
    return (np.power(freq, 2)/(p_ref/101325))*(1.84*(10**-11)*np.power(temperature/293.15, 0.5) + np.power(temperature/293.15, -5/2)*(0.01278*(np.exp(-2239.1/temperature)/(oxy_relax_freq + np.power(freq, 2)/oxy_relax_freq)) + 0.1068*(np.exp(-3352/temperature)/(nit_relax_freq + np.power(freq, 2)/nit_relax_freq))))

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