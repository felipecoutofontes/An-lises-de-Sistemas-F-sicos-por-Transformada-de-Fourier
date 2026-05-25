import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq
from pathlib import Path
from time import perf_counter

# ==========================================================
# DIRETÓRIO DE SAÍDA
# ==========================================================

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================================
# SINAL DE TESTE
# ==========================================================

def gerar_sinal(fs, duracao):

    t = np.arange(0, duracao, 1 / fs)

    x = (
        np.sin(2 * np.pi * 100 * t)
        + 0.5 * np.sin(2 * np.pi * 500 * t)
    )

    x += 0.3 * np.random.randn(len(t))

    return t, x

# ==========================================================
# FILTRO BUTTERWORTH
# ==========================================================

def sistema_butter():

    fc = 1000
    wc = 2 * np.pi * fc

    num, den = signal.butter(
        4,
        wc,
        analog=True
    )

    return signal.TransferFunction(num, den)

# ==========================================================
# RESPOSTA IMPULSIVA
# ==========================================================

def resposta_impulsiva(sys, t):

    _, h = signal.impulse(sys, T=t)
    return h

# ==========================================================
# CONVOLUÇÃO DIRETA
# ==========================================================

def conv_direta(x, h):

    inicio = perf_counter()

    y = np.convolve(x, h, mode="full")[:len(x)]

    return y, perf_counter() - inicio

# ==========================================================
# CONVOLUÇÃO VIA FFT
# ==========================================================

def conv_fft(x, h):

    inicio = perf_counter()

    y = signal.fftconvolve(x, h, mode="full")[:len(x)]

    return y, perf_counter() - inicio

# ==========================================================
# ESPECTRO
# ==========================================================

def espectro(x, fs):

    X = fft(x)
    f = fftfreq(len(x), 1 / fs)

    return f, np.abs(X) / len(x)

# ==========================================================
# SALVAR FIGURA
# ==========================================================

def salvar(fig, nome):

    arquivo = nome.lower().replace(" ", "_")
    caminho = OUTPUT_DIR / f"amp_op_{arquivo}.png"

    fig.savefig(
        caminho,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

# ==========================================================
# BENCHMARK
# ==========================================================

def benchmark(nome, sistema, fs, duracao, plot=False):

    t, x = gerar_sinal(fs, duracao)

    h = resposta_impulsiva(sistema, t)

    y_conv, tempo_conv = conv_direta(x, h)
    y_fft, tempo_fft = conv_fft(x, h)

    erro_rms = np.sqrt(np.mean((y_conv - y_fft) ** 2))

    speedup = (
        tempo_conv / tempo_fft
        if tempo_fft > 0
        else 0
    )

    if plot:

        fig = plt.figure(figsize=(12, 8))

        plt.subplot(3, 1, 1)
        plt.plot(t, x)
        plt.title(f"{nome} - Entrada")
        plt.grid()

        plt.subplot(3, 1, 2)
        plt.plot(t, y_conv, label="Convolução")
        plt.plot(t, y_fft, "--", label="FFT")
        plt.title("Saída")
        plt.legend()
        plt.grid()

        plt.subplot(3, 1, 3)

        f, X = espectro(x, fs)

        metade = len(f) // 2

        plt.plot(
            f[:metade],
            X[:metade]
        )

        plt.title("Espectro da Entrada")
        plt.grid()

        plt.tight_layout()

        salvar(fig, nome)

    return {
        "sistema": nome,
        "amostras": len(x),

        "tempo_conv": tempo_conv,
        "tempo_fft": tempo_fft,
        "speedup": speedup,
        "erro_rms": erro_rms,

        "numerador": sistema.num.tolist(),
        "denominador": sistema.den.tolist(),

        "entrada": x.tolist(),
        "saida_conv": y_conv.tolist(),
        "saida_fft": y_fft.tolist(),
        "impulso": h.tolist(),

        "tempo": t.tolist(),
        "fs": fs,
        "duracao": duracao
    }

# ==========================================================
# EXECUÇÃO DOS TESTES
# ==========================================================

def executar_testes():

    fs = 100000

    duracoes = [
        0.01,
        0.05,
        0.10
    ]

    sistema = sistema_butter()

    resultados = []

    for duracao in duracoes:

        resultados.append(
            benchmark(
                "Filtro Butterworth (4ª ordem)",
                sistema,
                fs,
                duracao,
                plot=True
            )
        )

    return resultados

# ==========================================================
# MAIN
# ==========================================================

def main():

    executar_testes()

# ==========================================================

if __name__ == "__main__":
    main()