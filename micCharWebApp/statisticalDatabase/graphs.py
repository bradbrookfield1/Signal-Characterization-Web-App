from scipy import stats
from matplotlib import pyplot as plt
from acoustics import Signal
import numpy as np
import pandas as pd
import librosa
from micCharacterization.graphic_interfacing import get_graph
from micCharacterization.preprocessing import charts_preprocess, apply_norm

fig_size = (6, 4.5)

# stats.probplot

def assign_hpss_arrays(context, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record):
    context['noisy_Signal_Harmonics'] = mic_Data_Record.noisy_Signal_Harmonics if norm_noisy_sig else None
    context['noisy_Signal_Percussives'] = mic_Data_Record.noisy_Signal_Percussives if norm_noisy_sig else None
    context['measured_Signal_Harmonics'] = mic_Data_Record.measured_Signal_Harmonics if norm_sig else None
    context['measured_Signal_Percussives'] = mic_Data_Record.measured_Signal_Percussives if norm_sig else None
    context['noise_Harmonics'] = mic_Data_Record.noise_Harmonics if norm_noise else None
    context['noise_Percussives'] = mic_Data_Record.noise_Percussives if norm_noise else None
    context['true_Signal_Harmonics'] = mic_Data_Record.true_Signal_Harmonics if true_sig else None
    context['true_Signal_Percussives'] = mic_Data_Record.true_Signal_Percussives if true_sig else None
    
    ns_harm_name = './Uploads/' + context['noisy_Signal_Harmonics'].name if context['noisy_Signal_Harmonics'] else None
    s_harm_name = './Uploads/' + context['measured_Signal_Harmonics'].name if context['measured_Signal_Harmonics'] else None
    n_harm_name = './Uploads/' + context['noise_Harmonics'].name if context['noise_Harmonics'] else None
    ts_harm_name = './Uploads/' + context['true_Signal_Harmonics'].name if context['true_Signal_Harmonics'] else None
    ns_perc_name = './Uploads/' + context['noisy_Signal_Percussives'].name if context['noisy_Signal_Percussives'] else None
    s_perc_name = './Uploads/' + context['measured_Signal_Percussives'].name if context['measured_Signal_Percussives'] else None
    n_perc_name = './Uploads/' + context['noise_Percussives'].name if context['noise_Percussives'] else None
    ts_perc_name = './Uploads/' + context['true_Signal_Percussives'].name if context['true_Signal_Percussives'] else None
    
    ns_harm, s_harm, n_harm, ts_harm = charts_preprocess([ns_harm_name, s_harm_name, n_harm_name, ts_harm_name])
    ns_perc, s_perc, n_perc, ts_perc = charts_preprocess([ns_perc_name, s_perc_name, n_perc_name, ts_perc_name])
    hpss_array = [ns_harm, ns_perc, s_harm, s_perc, n_harm, n_perc, ts_harm, ts_perc]
    return context, hpss_array

def get_original_PDFs(noisy_sig, noise, pdf_type, graph_type, name, mic_Data_Record, hpss_array=None, stat_norm=True):
    ns = noisy_sig[1]
    n = noise[1]
    if hpss_array:
        if graph_type == 'harmonic_HPSS_PDF_Graph':
            ns = apply_norm(hpss_array[0][0][1]) if stat_norm == True else hpss_array[0][0][1]
            n = apply_norm(hpss_array[4][0][1]) if stat_norm == True else hpss_array[4][0][1]
        elif graph_type == 'percussive_HPSS_PDF_Graph':
            ns = apply_norm(hpss_array[1][0][1]) if stat_norm == True else hpss_array[1][0][1]
            n = apply_norm(hpss_array[5][0][1]) if stat_norm == True else hpss_array[5][0][1]
    
    plt.figure(1, figsize=fig_size).clf()
    plt.hist(ns, bins=100, density=True, label='PDF Noisy Signal', lw=1, alpha=0.5)
    plt.hist(n, bins=100, density=True, label='PDF Noise', lw=1, alpha=0.5)
    plt.title(name + '\n' + pdf_type + ' PDFs')
    plt.xlabel('Signal Value')
    plt.ylabel('PDF')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return get_graph('Statistical Graphs', graph_type, mic_Data_Record)

def get_fft_PDFs(noisy_sig, noise, pdf_type, graph_type, name, mic_Data_Record):
    if graph_type == 'magnitude_FFT_Spectrum_Graph' or graph_type == 'magnitude_FFT_Time_Graph' or graph_type == 'phase_FFT_Spectrum_Graph' or graph_type == 'phase_FFT_Time_Graph':
        noisy_sig_fft = librosa.stft(noisy_sig[1])
        noise_fft = librosa.stft(noise[1])
    elif graph_type == 'magnitude_FMT_Spectrum_Graph' or graph_type == 'magnitude_FMT_Time_Graph' or graph_type == 'phase_FMT_Spectrum_Graph' or graph_type == 'phase_FMT_Time_Graph':
        noisy_sig_fft = librosa.feature.melspectrogram(noisy_sig[1], sr=noisy_sig[0])
        noise_fft = librosa.feature.melspectrogram(noise[1], sr=noise[0])
    noisy_sig_mag, _ = librosa.magphase(noisy_sig_fft, power=1)
    noise_mag, _ = librosa.magphase(noise_fft, power=1)    
    noisy_sig_ph = np.remainder(np.angle(noisy_sig_fft) + 2*np.pi, 2*np.pi)
    noise_ph = np.remainder(np.angle(noise_fft) + 2*np.pi, 2*np.pi)    
    noisy_sig_mag_pd = pd.DataFrame(noisy_sig_mag)
    noise_mag_pd = pd.DataFrame(noise_mag)
    noisy_sig_ph_pd = pd.DataFrame(noisy_sig_ph)
    noise_ph_pd = pd.DataFrame(noise_ph)
    
    avg_axis = 'index' if graph_type == 'magnitude_FFT_Spectrum_Graph' or graph_type == 'phase_FFT_Spectrum_Graph' or graph_type == 'magnitude_FMT_Spectrum_Graph' or graph_type == 'phase_FMT_Spectrum_Graph' else 'columns'
    if graph_type == 'magnitude_FFT_Spectrum_Graph' or graph_type == 'magnitude_FFT_Time_Graph' or graph_type == 'magnitude_FMT_Spectrum_Graph' or graph_type == 'magnitude_FMT_Time_Graph':
        noisy_sig_pd = noisy_sig_mag_pd[1:][1:].mean(axis=avg_axis)
        noise_pd = noise_mag_pd[1:][1:].mean(axis=avg_axis)
    elif graph_type == 'phase_FFT_Spectrum_Graph' or graph_type == 'phase_FFT_Time_Graph' or graph_type == 'phase_FMT_Spectrum_Graph' or graph_type == 'phase_FMT_Time_Graph':
        noisy_sig_pd = noisy_sig_ph_pd[1:][1:].mean(axis=avg_axis)
        noise_pd = noise_ph_pd[1:][1:].mean(axis=avg_axis)

    plt.figure(1, figsize=fig_size).clf()
    plt.hist(noisy_sig_pd, bins=100, density=True, label='PDF Noisy Signal', lw=1, alpha=0.5)
    plt.hist(noise_pd, bins=100, density=True, label='PDF Noise', lw=1, alpha=0.5)    
    plt.title(name + '\n' + pdf_type + ' PDFs')
    plt.xlabel('Signal Value')
    plt.ylabel('PDF')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return get_graph('Statistical Graphs', graph_type, mic_Data_Record)

def get_Signal_PDFs(noisy_sig, noise, pdf_type, graph_type, name, mic_Data_Record, stat_norm=True):
    if graph_type == 'hilbert_PDF_Graph':
        ns = np.asarray(Signal(apply_norm(np.asarray(noisy_sig[1])), fs=noisy_sig[0]).amplitude_envelope()) if stat_norm else np.asarray(noisy_sig[1].amplitude_envelope())
        n = np.asarray(Signal(apply_norm(np.asarray(noise[1])), fs=noise[0]).amplitude_envelope()) if stat_norm else np.asarray(noise[1].amplitude_envelope())
    elif graph_type == 'inst_Phase_PDF_Graph':
        ns = np.asarray(Signal(apply_norm(np.asarray(noisy_sig[1])), fs=noisy_sig[0]).instantaneous_phase()) if stat_norm else np.asarray(noisy_sig[1].instantaneous_phase())
        ns = np.remainder(ns + 2*np.pi, 2*np.pi)
        n = np.asarray(Signal(apply_norm(np.asarray(noise[1])), fs=noise[0]).instantaneous_phase()) if stat_norm else np.asarray(noise[1].instantaneous_phase())
        n = np.remainder(n + 2*np.pi, 2*np.pi)
    plt.figure(1, figsize=fig_size).clf()
    plt.hist(ns, bins=100, density=True, label='PDF Noisy Signal', lw=1, alpha=0.5)
    plt.hist(n, bins=100, density=True, label='PDF Noise', lw=1, alpha=0.5)    
    plt.title(name + '\n' + pdf_type + ' PDFs')
    plt.xlabel('Signal Value')
    plt.ylabel('PDF')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return get_graph('Statistical Graphs', graph_type, mic_Data_Record)