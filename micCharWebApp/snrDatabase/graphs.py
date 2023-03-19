from matplotlib import pyplot as plt
from micCharacterization.graphic_interfacing import get_graph, get_abs_coeff_graph
from micCharacterization.calculations import get_SNR_arrays, find_avg_snr_db_dist_array
from micCharacterization.constants import tunnel_dist

fig_size = (6, 4.5)

def get_SNR(list_1, list_2, snr_type, graph_type, name, mic_Data_Record):
    freq, db_plain, db_rolled_before, db_rolled_both = get_SNR_arrays(list_1, list_2, snr_type)
    plt.figure(1, figsize=fig_size).clf()
    plt.plot(freq, db_plain, label='Raw SNR', lw=1, alpha=0.75)
    plt.plot(freq, db_rolled_before, label='Before', lw=1, alpha=0.75)
    # plt.plot(freq, db_rolled_after, label='After', lw=1, alpha=0.75)
    plt.plot(freq, db_rolled_both, label='Both', lw=1, alpha=0.75)
    
    plt.title(name + '\nSNR ' + snr_type)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('SNR (dB)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return get_graph('SNR Graphs', graph_type, mic_Data_Record)

def get_avg_snr_vs_dist(dist_array, name=None, mic_Data_Record=None, snr_db=None, special_dist=tunnel_dist):
    dist_array, snr_avg_db_dist, snr_avg_db_dist_model = find_avg_snr_db_dist_array(dist_array, name, snr_db, special_dist)
    plt.figure(1, figsize=fig_size).clf()
    titl = 'Average SNR per Distance' if name == None else name + '\nAverage SNR per Distance'
    plt.title(titl)
    plt.xlabel('Distance (m)')
    plt.ylabel('Signal-to-Noise Ratio (dB)')
    plt.grid(True)
    # plt.plot(dist_array, snr_avg_db_dist_model, label=(r'$v_{wind} = 0$ $\frac{m}{s}, v_{UAV} = 18$ $\frac{m}{s},$ SPL$_{src} = 100$ dB'), lw=0.75, alpha=0.75)
    plt.plot(dist_array, snr_avg_db_dist_model, label='Model', lw=0.75, alpha=0.75)
    if snr_avg_db_dist:
        plt.plot(dist_array, snr_avg_db_dist, label='Measured', lw=0.75, alpha=0.75)
        plt.legend()
    plt.tight_layout()
    ret = get_abs_coeff_graph() if mic_Data_Record == None else get_graph('SNR Graphs', 'average_SNR_Distance_Graph', mic_Data_Record)
    return ret