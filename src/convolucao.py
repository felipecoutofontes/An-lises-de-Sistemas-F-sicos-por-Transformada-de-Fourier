# convolucao.py

import numpy as np
import matplotlib.pyplot as plt
import time


def convolucao_manual(x, h):
    """
    Implementação da definição matemática da convolução.
    """

    N = len(x)
    M = len(h)

    y = np.zeros(N + M - 1)

    for n in range(N + M - 1):

        soma = 0

        for k in range(N):

            if 0 <= n-k < M:
                soma += x[k] * h[n-k]

        y[n] = soma

    return y


def convolucao_numpy(x, h):
    """
    Convolução utilizando NumPy.
    """

    return np.convolve(x, h)


def convolucao_fft(x, h):
    """
    Convolução utilizando FFT.
    """

    tamanho = len(x) + len(h) - 1

    X = np.fft.fft(x, tamanho)

    H = np.fft.fft(h, tamanho)

    Y = X * H

    y = np.fft.ifft(Y)

    return y.real


# --------------------------
# Entrada do sistema
# --------------------------

fs = 1000

t = np.arange(0, 1, 1/fs)

x = np.sin(2*np.pi*5*t)

# resposta ao impulso
h = np.exp(-20*t)

# --------------------------
# Convolução manual
# --------------------------

inicio = time.perf_counter()

y = convolucao_manual(x, h)

fim = time.perf_counter()

print()
print("Tempo da convolução manual:")
print(f"{fim-inicio:.6f} segundos")

# --------------------------
# Gráficos
# --------------------------

plt.figure(figsize=(10,8))

plt.subplot(3,1,1)
plt.plot(t,x)

plt.title("Sinal de entrada x(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(t,h)

plt.title("Resposta ao impulso h(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid(True)

tempo_saida = np.arange(len(y))/fs

plt.subplot(3,1,3)
plt.plot(tempo_saida,y)

plt.title("Saída do sistema y(t)=x(t)*h(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()