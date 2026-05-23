import time
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir, "outputs"))


def fft_convolve(a, b):
    """Convolution using FFT"""
    n = len(a) + len(b) - 1
    N = 1 << (n - 1).bit_length()
    A = np.fft.fft(a, N)
    B = np.fft.fft(b, N)
    c = np.fft.ifft(A * B)
    return np.real(c)[:n]


def plot_three_convolutions(output_dir=None):
    """Plot three convolution examples"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    t = np.linspace(-1.0, 1.0, 2048, endpoint=False)
    dt = t[1] - t[0]

    x1 = np.sin(2 * np.pi * 5 * t)
    x2 = np.sign(np.sin(2 * np.pi * 3 * t))
    sigma = 0.05
    x3 = np.exp(-t ** 2 / (2 * sigma ** 2))

    pairs = [
        (x1, x3, "sine5_conv_gauss"),
        (x2, x3, "square3_conv_gauss"),
        (x3, x3, "gauss_conv_gauss"),
    ]

    os.makedirs(output_dir, exist_ok=True)
    total_start = time.perf_counter()

    for a, b, name in pairs:
        start_np = time.perf_counter()
        conv_time = np.convolve(a, b, mode="same") * dt
        np_time = time.perf_counter() - start_np

        start_fft = time.perf_counter()
        conv_fft = fft_convolve(a, b) * dt
        fft_time = time.perf_counter() - start_fft

        n_full = len(a) + len(b) - 1
        t_full = np.arange(n_full) * dt + (t[0] + t[0])

        fig, axes = plt.subplots(3, 1, figsize=(8, 8))
        axes[0].plot(t, a)
        axes[0].set_title("input a")
        axes[1].plot(t, b)
        axes[1].set_title("input b")

        axes[2].plot(t, conv_time, label="np.convolve (same)")
        center = (n_full // 2) - (len(t) // 2)
        if center < 0:
            center = 0
        start = center
        end = start + len(t)
        c_center = conv_fft[start:end]
        axes[2].plot(t, c_center, '--', label="fft conv (center)")
        axes[2].set_title(f"convolution: {name}")
        axes[2].legend()

        plt.tight_layout()
        out_path = os.path.join(output_dir, f"convolucao_{name}.png")
        fig.savefig(out_path)
        print(f"Saved {out_path}")
        print(f"np.convolve({name}) took {np_time:.6f} seconds")
        print(f"fft_convolve({name}) took {fft_time:.6f} seconds")
        plt.close(fig)

    total_time = time.perf_counter() - total_start
    print(f"Total convolution runtime: {total_time:.6f} seconds")


if __name__ == "__main__":
    plot_three_convolutions()
