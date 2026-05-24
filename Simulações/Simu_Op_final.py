import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
from scipy import signal
from pathlib import Path
from time import perf_counter

# ==========================================================
# OUTPUT DIR (compatível com interface)
# ==========================================================

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================================
# SINAL DE TESTE
# ==========================================================

def gerar_sinal(fs, duracao):

    t = np.arange(0, duracao, 1/fs)

    x = (
        np.sin(2*np.pi*100*t) +
        0.5*np.sin(2*np.pi*500*t)
    )

    x += 0.3 * np.random.randn(len(t))

    return t, x

# ==========================================================
# SISTEMA RC
# ==========================================================

def sistema_rc():

    R = 1e3
    C = 100e-9

    tau = R * C

    num = [1]
    den = [tau, 1]

    return signal.TransferFunction(num, den), tau

# ==========================================================
# SISTEMA BUTTERWORTH
# ==========================================================

def sistema_butter():

    fc = 1000
    wc = 2*np.pi*fc

    num, den = signal.butter(
        4,
        wc,
        analog=True
    )

    return signal.TransferFunction(num, den), None

# ==========================================================
# RESPOSTA IMPULSIVA (CONSISTENTE)
# ==========================================================

def resposta_impulsiva(sys, t, tau=None):

    if tau is not None:
        h = (1/tau) * np.exp(-t/tau)
        return h

    _, h = signal.impulse(sys, T=t)
    return h

# ==========================================================
# CONVOLUÇÃO DIRETA
# ==========================================================

def conv_direta(x, h):

    t0 = perf_counter()
    y = np.convolve(x, h, mode="full")[:len(x)]
    return y, perf_counter() - t0

# ==========================================================
# CONVOLUÇÃO FFT
# ==========================================================

def conv_fft(x, h):

    t0 = perf_counter()

    n = len(x) + len(h) - 1
    nfft = 2**int(np.ceil(np.log2(n)))

    X = fft(x, nfft)
    H = fft(h, nfft)

    Y = X * H
    y = np.real(ifft(Y))

    start = (len(h)-1)//2
    y = y[start:start+len(x)]

    return y, perf_counter() - t0

# ==========================================================
# ESPECTRO
# ==========================================================

def espectro(x, fs):

    X = fft(x)
    f = fftfreq(len(x), 1/fs)

    return f, np.abs(X)/len(x)

# ==========================================================
# GRÁFICOS
# ==========================================================

def salvar(fig, nome):

    nome = nome.lower().replace(" ", "_")

    path = OUTPUT_DIR / f"amp_op_{nome}.png"

    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

# ==========================================================
# BENCHMARK (INTERFACE USA ISSO)
# ==========================================================

def benchmark(nome, sistema, fs, duracao, plot=False):

    t, x = gerar_sinal(fs, duracao)

    sys, tau = sistema

    h = resposta_impulsiva(sys, t, tau)

    y1, t1 = conv_direta(x, h)
    y2, t2 = conv_fft(x, h)

    erro = np.sqrt(np.mean((y1 - y2)**2))

    speedup = t1 / t2 if t2 > 0 else 0

    if plot:

        fig = plt.figure(figsize=(12, 8))

        plt.subplot(3,1,1)
        plt.plot(t, x)
        plt.title(nome + " - Entrada")
        plt.grid()

        plt.subplot(3,1,2)
        plt.plot(t, y1, label="Conv")
        plt.plot(t, y2, "--", label="FFT")
        plt.title("Saída")
        plt.legend()
        plt.grid()

        plt.subplot(3,1,3)
        f, X = espectro(x, fs)
        plt.plot(f[:len(f)//2], X[:len(X)//2])
        plt.title("Espectro Entrada")
        plt.grid()

        salvar(fig, nome)

    return {
        "sistema": nome,
        "amostras": len(x),

        "tempo_conv": t1,
        "tempo_fft": t2,
        "speedup": speedup,
        "erro_rms": erro,

        "numerador": sys.num.tolist(),
        "denominador": sys.den.tolist(),

        "entrada": x.tolist(),
        "saida_conv": y1.tolist(),
        "saida_fft": y2.tolist(),
        "impulso": h.tolist(),

        "tempo": t.tolist(),
        "fs": fs,
        "duracao": duracao
    }

# ==========================================================
# EXECUÇÃO PARA INTERFACE
# ==========================================================

def executar_testes():

    fs = 100000

    tempos = [0.01, 0.05, 0.1, 0.2, 0.5]

    resultados = []

    for d in tempos:

        resultados.append(
            benchmark(
                "Filtro RC (1ª ordem)",
                sistema_rc(),
                fs,
                d,
                plot=True
            )
        )

        resultados.append(
            benchmark(
                "Filtro Butterworth (4ª ordem)",
                sistema_butter(),
                fs,
                d,
                plot=True
            )
        )

    return resultados

# ==========================================================
# MAIN (INTERFACE GRAFICOS)
# ==========================================================

def main():

    executar_testes()

# ==========================================================

if __name__ == "__main__":
    main()