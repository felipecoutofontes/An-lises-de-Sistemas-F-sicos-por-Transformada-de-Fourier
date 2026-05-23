import time
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir, "outputs"))


def compute_fft_and_plot(t, x, name, output_dir=None):
    """Compute FFT and save plot to outputs directory"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    dt = t[1] - t[0]
    N = len(t)
    X = np.fft.fftshift(np.fft.fft(x)) * dt
    freq = np.fft.fftshift(np.fft.fftfreq(N, d=dt))
    omega = 2 * np.pi * freq

    fig, axes = plt.subplots(2, 1, figsize=(8, 6))
    axes[0].plot(t, x)
    axes[0].set_title(f"x(t): {name}")
    axes[0].set_xlabel("t")

    axes[1].plot(omega, np.abs(X))
    axes[1].set_title(f"|X(omega)|: {name}")
    axes[1].set_xlabel("omega (rad/s)")

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"transformada_{name}.png")
    fig.savefig(out_path)
    print(f"Saved {out_path}")
    plt.close(fig)


def main():
    # time vector
    t = np.linspace(-1.0, 1.0, 2048, endpoint=False)

    # 3 example signals
    s1 = np.sin(2 * np.pi * 5 * t)  # sine 5 Hz
    s2 = np.sign(np.sin(2 * np.pi * 3 * t))  # square-ish 3 Hz
    sigma = 0.05
    s3 = np.exp(-t ** 2 / (2 * sigma ** 2))  # gaussian pulse

    signals = [(s1, "sine_5Hz"), (s2, "square_3Hz"), (s3, "gaussian_pulse")]

    total_start = time.perf_counter()
    for x, name in signals:
        start = time.perf_counter()
        compute_fft_and_plot(t, x, name)
        elapsed = time.perf_counter() - start
        print(f"FFT {name} took {elapsed:.6f} seconds")

    total_time = time.perf_counter() - total_start
    print(f"Total FFT runtime: {total_time:.6f} seconds")


if __name__ == "__main__":
    main()
