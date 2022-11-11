import numpy as np

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