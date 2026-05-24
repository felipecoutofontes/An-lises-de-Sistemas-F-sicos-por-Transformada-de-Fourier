import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
from time import perf_counter
from pathlib import Path
import os

# ==========================================================
# FUNÇÃO PRINCIPAL (EXECUTA SIMULAÇÃO)
# ==========================================================

def main():
    # ----------------------------
    # PARÂMETROS DO FILTRO RC
    # ----------------------------
    R = 1e3
    C = 10e-6
    tau = R * C

    # ----------------------------
    # SINAL
    # ----------------------------
    fs = 1000
    dt = 1 / fs
    T = 2

    t = np.arange(0, T, dt)
    N = len(t)

    x = (
        np.sin(2 * np.pi * 10 * t) +
        0.5 * np.sin(2 * np.pi * 20 * t)
    )

    x_ruido = x + 0.4 * np.random.randn(len(t))

    # ----------------------------
    # RESPOSTA IMPULSIVA
    # ----------------------------
    h = (1 / tau) * np.exp(-t / tau)
    h = h * dt

    # ----------------------------
    # CONVOLUÇÃO DIRETA
    # ----------------------------
    inicio = perf_counter()
    y_conv = np.convolve(x_ruido, h, mode="full")[:N]
    tempo_conv = perf_counter() - inicio

    # ----------------------------
    # FFT
    # ----------------------------
    inicio = perf_counter()

    nfft = 2 ** int(np.ceil(np.log2(len(x_ruido) + len(h) - 1)))

    X = fft(x_ruido, nfft)
    H = fft(h, nfft)

    Y = X * H
    y_fft_full = np.real(ifft(Y))

    inicio_cut = (len(h) - 1) // 2
    y_fft = y_fft_full[inicio_cut:inicio_cut + N]

    tempo_fft = perf_counter() - inicio

    # ----------------------------
    # ERRO E SPEEDUP
    # ----------------------------
    erro = np.sqrt(np.mean((y_conv - y_fft) ** 2))
    speedup = tempo_conv / tempo_fft

    BASE_DIR = Path(__file__).resolve().parents[1]
    OUTPUT_DIR = BASE_DIR / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)

    # ----------------------------
    # GRÁFICOS
    # ----------------------------
    freqs = fftfreq(nfft, dt)
    w = 2 * np.pi * freqs
    H_w = 1 / (1 + 1j * w * tau)

    X_f = np.abs(fft(x_ruido, nfft)) / N
    Y_f = np.abs(Y) / N
    Y_conv_f = np.abs(fft(y_conv, nfft)) / N

    pos = freqs >= 0

    plt.figure(figsize=(14, 10))

    plt.subplot(3, 2, 1)
    plt.plot(t, x_ruido)
    plt.title("Entrada com Ruído")
    plt.grid()

    plt.subplot(3, 2, 2)
    plt.plot(freqs[pos], X_f[pos])
    plt.title("Espectro da Entrada")
    plt.grid()
    plt.xlim(0, 100)

    plt.subplot(3, 2, 3)
    plt.plot(t, y_conv, label="Convolução")
    plt.plot(t, y_fft, "--", label="FFT")
    plt.title("Saída do Filtro RC")
    plt.legend()
    plt.grid()

    plt.subplot(3, 2, 4)
    plt.plot(freqs[pos], Y_f[pos], label="FFT saída")
    plt.plot(freqs[pos], Y_conv_f[pos], "--", label="Conv saída")
    plt.title("Espectro da Saída")
    plt.legend()
    plt.grid()
    plt.xlim(0, 100)

    plt.subplot(3, 2, 5)
    plt.plot(freqs[pos], np.abs(H_w)[pos])
    plt.title("Resposta em Frequência |H(f)|")
    plt.grid()
    plt.xlim(0, 100)

    plt.subplot(3, 2, 6)
    plt.plot(t, x_ruido, alpha=0.4, label="Entrada")
    plt.plot(t, y_fft, label="Saída filtrada")
    plt.title("Filtragem RC")
    plt.legend()
    plt.grid()

    plt.tight_layout()

    # SALVAR ANTES DE MOSTRAR
    BASE_DIR = Path(__file__).resolve().parents[1]
    OUTPUT_DIR = BASE_DIR / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)

    caminho_saida = OUTPUT_DIR / "rc_simulacao.png"
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")

    plt.show()

    return {
        "sistema": "RC",
        "amostras": N,
        "tempo_conv": tempo_conv,
        "tempo_fft": tempo_fft,
        "speedup": speedup,
        "erro_rms": erro,
        "numerador": [1],
        "denominador": [tau, 1],
        "entrada": x_ruido,
        "saida_conv": y_conv,
        "saida_fft": y_fft,
        "impulso": h
    }


# ==========================================================
# FUNÇÃO USADA PELO SEU GUI
# ==========================================================

def executar_testes():
    return [main()]


# ==========================================================
# EXECUÇÃO DIRETA (FORA DO GUI)
# ==========================================================

if __name__ == "__main__":
    main()