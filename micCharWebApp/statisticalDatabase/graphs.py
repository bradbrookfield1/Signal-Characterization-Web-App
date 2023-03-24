from scipy import stats
from matplotlib import pyplot as plt
from acoustics import Signal
import numpy as np
import pandas as pd
import librosa
from micCharacterization.graphic_interfacing import get_graph
from micCharacterization.preprocessing import charts_preprocess, apply_norm_everywhere

fig_size = (6, 4.5)

# stats.probplot

def get_original_PDFs(noisy_sig, noise, pdf_type, graph_type, name, mic_Data_Record):    
    plt.figure(1, figsize=fig_size).clf()
    plt.hist(noisy_sig[0][1], bins=100, density=True, label='PDF Noisy Signal', lw=1, alpha=0.5)
    plt.hist(noise[0][1], bins=100, density=True, label='PDF Noise', lw=1, alpha=0.5)
    plt.title(name + '\n' + pdf_type + ' PDFs')
    plt.xlabel('Signal Value')
    plt.ylabel('PDF')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return get_graph('Statistical Graphs', graph_type, mic_Data_Record)

def get_fft_PDFs(noisy_sig, noise, pdf_type, graph_type, name, mic_Data_Record):
    if graph_type == 'magnitude_FFT_Spectrum_Graph' or graph_type == 'magnitude_FFT_Time_Graph' or graph_type == 'phase_FFT_Spectrum_Graph' or graph_type == 'phase_FFT_Time_Graph':
        noisy_sig_fft = librosa.stft(noisy_sig[0][1])
        noise_fft = librosa.stft(noise[0][1])
    elif graph_type == 'magnitude_FMT_Spectrum_Graph' or graph_type == 'magnitude_FMT_Time_Graph' or graph_type == 'phase_FMT_Spectrum_Graph' or graph_type == 'phase_FMT_Time_Graph':
        noisy_sig_fft = librosa.feature.melspectrogram(noisy_sig[0][1], sr=noisy_sig[0][0])
        noise_fft = librosa.feature.melspectrogram(noise[0][1], sr=noise[0][0])
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

def get_Signal_PDFs(noisy_sig, noise, pdf_type, graph_type, name, mic_Data_Record):
    if graph_type == 'hilbert_PDF_Graph':
        ns = np.asarray(noisy_sig[1].amplitude_envelope())
        n = np.asarray(noise[1].amplitude_envelope())
    elif graph_type == 'inst_Phase_PDF_Graph':
        ns = np.asarray(noisy_sig[1].instantaneous_phase())
        ns = np.remainder(ns + 2*np.pi, 2*np.pi)
        n = np.asarray(noise[1].instantaneous_phase())
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