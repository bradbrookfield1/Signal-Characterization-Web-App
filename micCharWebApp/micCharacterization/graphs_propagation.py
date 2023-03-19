from matplotlib import pyplot as plt
import numpy as np
from .graphic_interfacing import get_abs_coeff_graph
from .calculations import calc_coeff, calc_snr_pred
from .constants import freqs, distance, p_bar, p_ref
from .constants import temperature, temp_array, relative_humidity, rel_hum_array

fig_size = (6, 4.5)

def prop_snr_pred_dist(dist_array):
    dist_snr_pred = []
    if not type(dist_array) == np.ndarray:
        dist_array = [dist_array]
    for dist in dist_array:
        snr_pred_db = calc_snr_pred(freqs, 87.5, 100, 2, dist, [0, 18, 0], temperature, relative_humidity, p_bar, p_ref)
        dist_snr_pred.append(snr_pred_db)
    plt.figure(1, figsize=fig_size).clf()
    plt.title('SNR Prediction\nVarying Distance')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Signal-to-Noise Ratio (dB)')
    plt.grid(True)
    for i in range(len(dist_snr_pred)):
        plt.plot(freqs, dist_snr_pred[i], label=str(dist_array[i]) + ' m', lw=0.75, alpha=0.75)
    plt.legend()
    plt.tight_layout()
    return get_abs_coeff_graph()

def get_spec_prop_abs_coeff_hum():
    rel_hum_abs_coeff = []
    for rel_hum in rel_hum_array:
        abs_coeff_db, _, _ = calc_coeff(freqs, distance, temperature, rel_hum, p_bar, p_ref)
        rel_hum_abs_coeff.append(abs_coeff_db)
    plt.figure(1, figsize=fig_size).clf()
    plt.title('Spectral Sound Absorption Coefficient\nVarying Relative Humidity')
    plt.xlabel(r'Frequency/Pressure $\left(\frac{Hz}{atm}\right)$')
    plt.ylabel(r'Absorption Coefficient $\left(\frac{dB}{100m \cdot atm}\right)$')
    plt.grid(True)
    for i in range(len(rel_hum_abs_coeff)):
        plt.loglog(freqs, rel_hum_abs_coeff[i], label=str(rel_hum_array[i]*100) + ' %', lw=0.75, alpha=0.75)
    plt.legend()
    plt.tight_layout()
    return get_abs_coeff_graph()

def get_spec_prop_abs_coeff_temp():
    temp_abs_coeff = []
    for temp in temp_array:
        abs_coeff_db, _, _ = calc_coeff(freqs, distance, temp, relative_humidity, p_bar, p_ref)
        temp_abs_coeff.append(abs_coeff_db)
    plt.figure(1, figsize=fig_size).clf()
    plt.title('Spectral Sound Absorption Coefficient\nVarying Temperature')
    plt.xlabel(r'Frequency/Pressure $\left(\frac{Hz}{atm}\right)$')
    plt.ylabel(r'Absorption Coefficient $\left(\frac{dB}{100m \cdot atm}\right)$')
    plt.grid(True)
    for i in range(len(temp_abs_coeff)):
        plt.loglog(freqs, temp_abs_coeff[i], label=str(temp_array[i] - 273.15) + ' C', lw=0.75, alpha=0.75)
    plt.legend()
    plt.tight_layout()
    return get_abs_coeff_graph()

def get_spec_prop_abs_coeff_dist(dist_array):
    dist_abs_coeff = []
    for dist in dist_array:
        abs_coeff_db, _, _ = calc_coeff(freqs, dist, temperature, relative_humidity, p_bar, p_ref)
        dist_abs_coeff.append(abs_coeff_db)
    plt.figure(1, figsize=fig_size).clf()
    plt.title('Spectral Sound Absorption Coefficient\nVarying Distance')
    plt.xlabel(r'Frequency/Pressure $\left(\frac{Hz}{atm}\right)$')
    plt.ylabel(r'Absorption Coefficient $\left(\frac{dB}{\_\_\_\_ m \cdot atm}\right)$')
    plt.grid(True)
    for i in range(len(dist_abs_coeff)):
        plt.loglog(freqs, dist_abs_coeff[i], label=str(dist_array[i]) + ' m', lw=0.75, alpha=0.75)
    plt.legend()
    plt.tight_layout()
    return get_abs_coeff_graph()

def get_spec_prop_abs_coeff_p(p_bar_array, p_ref):
    p_bar_abs_coeff = []
    plt.figure(1, figsize=fig_size).clf()
    if isinstance(p_ref, np.ndarray):
        plt.title('Spectral Sound Absorption Coefficient\nVarying Barometric & Reference Pressure Together')
        for p_bar, p_r in zip(p_bar_array, p_ref):
            abs_coeff_db, _, _ = calc_coeff(freqs, distance, temperature, relative_humidity, p_bar, p_r)
            p_bar_abs_coeff.append(abs_coeff_db)
    else:
        plt.title('Spectral Sound Absorption Coefficient\nVarying Barometric Pressure')
        for p_bar in p_bar_array:
            abs_coeff_db, _, _ = calc_coeff(freqs, distance, temperature, relative_humidity, p_bar, p_ref)
            p_bar_abs_coeff.append(abs_coeff_db)
    plt.xlabel(r'Frequency/Pressure $\left(\frac{Hz}{atm}\right)$')
    plt.ylabel(r'Absorption Coefficient $\left(\frac{dB}{100m \cdot atm}\right)$')
    plt.grid(True)
    for i in range(len(p_bar_abs_coeff)):
        plt.loglog(freqs, p_bar_abs_coeff[i], label=str(p_bar_array[i]) + ' Pa', lw=0.75, alpha=0.75)
    plt.legend()
    plt.tight_layout()
    return get_abs_coeff_graph()