"""
Comparação de desempenho:
- Convolução direta (NumPy)
- FFT (Transformada de Fourier)

Aplicada a sistemas de Amplificadores Operacionais.

Autor: Felipe Resende
"""

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pathlib import Path
from scipy import signal
from scipy.fft import fft, ifft

from time import perf_counter


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


# ==========================================================
# Geração de sinal de teste
# ==========================================================

def gerar_sinal(fs, duracao, ruido=False):

    t = np.arange(0, duracao, 1/fs)

    x = (
        np.sin(2*np.pi*100*t)
        + 0.5*np.sin(2*np.pi*3000*t)
    )

    if ruido:
        x += 0.3*np.random.randn(len(t))

    return t, x


# ==========================================================
# Sistema simples
# H(s)=1/(tau*s+1)
# ==========================================================

def sistema_simples():

    R = 1e3
    C = 100e-9

    tau = R * C

    num = [1]
    den = [tau, 1]

    return signal.TransferFunction(num, den)


# ==========================================================
# Sistema complexo
# Butterworth de 4ª ordem
# ==========================================================

def sistema_complexo():

    fc = 1000

    wc = 2*np.pi*fc

    num, den = signal.butter(
        N=4,
        Wn=wc,
        analog=True
    )

    return signal.TransferFunction(num, den)


# ==========================================================
# Resposta impulsiva
# ==========================================================

def resposta_impulsiva(sys, t):

    _, h = signal.impulse(sys, T=t)

    return h


# ==========================================================
# Convolução direta
# ==========================================================

def convolucao_direta(x, h):

    inicio = perf_counter()

    y = np.convolve(x, h, mode="same")

    tempo = perf_counter() - inicio

    return y, tempo


# ==========================================================
# Convolução usando FFT
# ==========================================================

def convolucao_fft(x, h):

    inicio_tempo = perf_counter()

    tamanho = len(x) + len(h) - 1

    nfft = 2**int(np.ceil(np.log2(tamanho)))

    X = fft(x, nfft)
    H = fft(h, nfft)

    Y = X * H

    y_full = np.real(ifft(Y))

    inicio = (len(h) - 1) // 2
    fim = inicio + len(x)

    y = y_full[inicio:fim]

    tempo = perf_counter() - inicio_tempo

    return y, tempo


# ==========================================================
# Erro RMS
# ==========================================================

def erro_rms(y1, y2):

    return np.sqrt(
        np.mean((y1-y2)**2)
    )


# ==========================================================
# Espectro
# ==========================================================

def espectro(x, fs):

    X = np.fft.fft(x)

    freq = np.fft.fftfreq(
        len(x),
        d=1/fs
    )

    return freq, np.abs(X)


# ==========================================================
# Salvar gráficos
# ==========================================================

def salvar_grafico(fig, nome, duracao):

    OUTPUT_DIR.mkdir(exist_ok=True)

    nome_sanitizado = (
        nome.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
        .replace("-", "_")
    )

    caminho = OUTPUT_DIR / f"amp_op_{nome_sanitizado}_{duracao:.2f}s.png"

    fig.savefig(
        caminho,
        dpi=150,
        bbox_inches="tight"
    )

    return caminho


# ==========================================================
# Benchmark
# ==========================================================

def benchmark(
        nome,
        sistema,
        fs,
        duracao,
        mostrar_graficos=False
):

    print("\n" + "="*70)
    print(nome)
    print("="*70)

    t, x = gerar_sinal(
        fs,
        duracao
    )

    h = resposta_impulsiva(
        sistema,
        t
    )

    y_conv, tempo_conv = convolucao_direta(
        x,
        h
    )

    y_fft, tempo_fft = convolucao_fft(
        x,
        h
    )

    erro = erro_rms(
        y_conv,
        y_fft
    )

    speedup = tempo_conv / tempo_fft

    print("\nFunção de Transferência")

    print("Numerador:")
    print(sistema.num)

    print("\nDenominador:")
    print(sistema.den)

    print("\nEntrada utilizada:")

    print(
        "x(t)=sin(2π100t)"
        "+0.5sin(2π500t)"
        "+0.25sin(2π2000t)"
        "+ruído"
    )

    print("\nResultados")

    print(
        f"N amostras      : {len(x):,}"
    )

    print(
        f"Tempo Conv.     : {tempo_conv:.6f} s"
    )

    print(
        f"Tempo FFT       : {tempo_fft:.6f} s"
    )

    print(
        f"Speedup FFT     : {speedup:.2f}x"
    )

    print(
        f"Erro RMS        : {erro:.6e}"
    )

    print(
        "\nPrimeiras 10 amostras da saída:"
    )

    print(y_fft[:10])

    # ----------------------------------
    # gráficos apenas no último teste
    # ----------------------------------

    if mostrar_graficos:

        freq_x, mag_x = espectro(
            x,
            fs
        )

        freq_y, mag_y = espectro(
            y_fft,
            fs
        )

        metade = len(freq_x)//2

        fig = plt.figure(
            figsize=(12,10)
        )

        plt.subplot(4,1,1)

        plt.plot(t,x)

        plt.title(
            f"{nome} - Entrada"
        )

        plt.grid(True)

        plt.subplot(4,1,2)

        plt.plot(t,h)

        plt.title(
            "Resposta impulsiva h(t)"
        )

        plt.grid(True)

        plt.subplot(4,1,3)

        plt.plot(
            t,
            y_conv,
            label="Convolução"
        )

        plt.plot(
            t,
            y_fft,
            "--",
            label="FFT"
        )

        plt.legend()

        plt.title(
            "Saída do Sistema"
        )

        plt.grid(True)

        plt.subplot(4,1,4)

        plt.plot(
            freq_x[:metade],
            mag_x[:metade],
            label="Entrada"
        )

        plt.plot(
            freq_y[:metade],
            mag_y[:metade],
            label="Saída"
        )

        plt.legend()

        plt.title(
            "Espectro"
        )

        plt.xlabel("Frequência (Hz)")

        plt.grid(True)

        plt.tight_layout()

        caminho = salvar_grafico(
            fig,
            nome,
            duracao
        )

        print(f"\nGráfico salvo em: {caminho}")

        plt.close(fig)
    return {
        "sistema": nome,
        "amostras": len(x),

        "tempo_conv": tempo_conv,
        "tempo_fft": tempo_fft,
        "speedup": speedup,
        "erro_rms": erro,

        "numerador": sistema.num.tolist(),
        "denominador": sistema.den.tolist(),
        "funcao_transferencia":
            f"({sistema.num}) / ({sistema.den})",

        "tempo": t.tolist(),
        "entrada": x.tolist(),
        "saida_conv": y_conv.tolist(),
        "saida_fft": y_fft.tolist(),
        "impulso": h.tolist(),

        "fs": fs,
        "duracao": duracao
    }
# ==========================================================
# Função para a interface
# ==========================================================

def executar_testes():

    fs = 100_000

    tamanhos = [
        0.01,
        0.05,
        0.10,
        0.20,
        0.50
    ]

    resultados = []

    for duracao in tamanhos:

        resultado = benchmark(
            "Filtro RC (1ª ordem)",
            sistema_simples(),
            fs,
            duracao,
            mostrar_graficos=False
        )

        resultados.append(resultado)

        resultado = benchmark(
            "Filtro Butterworth (4ª ordem)",
            sistema_complexo(),
            fs,
            duracao,
            mostrar_graficos=False
        )

        resultados.append(resultado)

    return resultados

# ==========================================================
# Principal
# ==========================================================

def main():

    fs = 100_000

    tamanhos = [
        0.01,
        0.05,
        0.10,
        0.20,
        0.50
    ]

    print("\nCOMPARAÇÃO FFT x CONVOLUÇÃO")
    print("="*70)

    for duracao in tamanhos:

        print(
            f"\nDuração = {duracao} s"
        )

        benchmark(
            "Filtro RC (1ª ordem)",
            sistema_simples(),
            fs,
            duracao,
            mostrar_graficos=True
        )

        benchmark(
            "Filtro Butterworth (4ª ordem)",
            sistema_complexo(),
            fs,
            duracao,
            mostrar_graficos=True
        )


if __name__ == "__main__":
    main()