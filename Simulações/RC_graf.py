"""
===========================================================
Comparação entre Convolução e Transformada de Fourier
Aplicada a um Circuito RC Passa-Baixa

Objetivos:
- Modelar um circuito RC passa-baixa
- Obter sua resposta impulsiva h(t)
- Simular a saída usando:
    1) Convolução no domínio do tempo
    2) Transformada de Fourier
- Mostrar que os resultados são equivalentes
- Plotar o espectro de frequência
- Adicionar ruído de alta frequência
- Demonstrar filtragem pelo circuito RC
===========================================================
"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import fft, ifft, fftfreq

# ===========================================================
# EXPLICAÇÃO TEÓRICA
# ===========================================================

# Circuito RC Passa-Baixa
#
# Pela Lei das Correntes de Kirchhoff:
#
#     RC * dy(t)/dt + y(t) = x(t)
#
# onde:
#     x(t) -> sinal de entrada
#     y(t) -> sinal de saída
#
#
# Resposta impulsiva:
#
#     h(t) = (1/RC) * exp(-t/RC) * u(t)
#
#
# Resposta em frequência:
#
#     H(jw) = 1 / (1 + jwRC)
#
#
# Relação entrada-saída:
#
# Domínio do tempo:
#
#     y(t) = x(t) * h(t)
#
#
# Domínio da frequência:
#
#     Y(jw) = X(jw) H(jw)
#
#
# O Teorema da Convolução afirma:
#
#     Convolução no tempo
#     equivale a
#     multiplicação na frequência
#
#
# Objetivos da simulação:
#
# - Mostrar que convolução e Fourier produzem
#   a mesma saída
#
# - Mostrar o espectro de frequência do sinal
#
# - Demonstrar como o filtro RC remove ruídos
#   de alta frequência

# ===========================================================
# PARÂMETROS DO SISTEMA
# ===========================================================

R = 1e3          # 1 kOhm
C = 1e-5         # 10 uF

tau = R * C

# ===========================================================
# EIXO TEMPORAL
# ===========================================================

fs = 1000                # Frequência de amostragem
dt = 1 / fs

T = 2

t = np.arange(0, T, dt)

N = len(t)

# ===========================================================
# RESPOSTA IMPULSIVA h(t)
# ===========================================================

h = (1 / tau) * np.exp(-t / tau)

# Ajuste discreto
h = h * dt

# ===========================================================
# SINAL DE ENTRADA (SEM RUÍDO)
# ===========================================================

# Entrada composta por:
# - senoide de 10 Hz
# - senoide de 20 Hz

f1 = 10
f2 = 20

x = (
    np.sin(2 * np.pi * f1 * t)
    + 0.5 * np.sin(2 * np.pi * f2 * t)
)

# ===========================================================
# CONVOLUÇÃO
# ===========================================================

# y(t) = x(t) * h(t)

y_conv = np.convolve(x, h, mode='full')

# Mesmo tamanho do sinal original
y_conv = y_conv[:N]

# ===========================================================
# FOURIER
# ===========================================================

# Para reproduzir a convolução linear,
# precisamos usar zero-padding

N_conv = len(x) + len(h) - 1

# FFT da entrada
X = fft(x, N_conv)

# FFT da resposta impulsiva
H_fft = fft(h, N_conv)

# Multiplicação espectral
Y = X * H_fft

# Transformada inversa
y_fft = np.real(ifft(Y))

# Mesmo tamanho do sinal original
y_fft = y_fft[:N]

# ===========================================================
# ESPECTRO DE FREQUÊNCIA
# ===========================================================

freqs = fftfreq(N_conv, dt)

X_mag = np.abs(X) / N
Y_mag = np.abs(Y) / N

# Apenas frequências positivas
positive = freqs >= 0

freqs_pos = freqs[positive]

X_mag_pos = X_mag[positive]
Y_mag_pos = Y_mag[positive]

# ===========================================================
# PLOTS - SEM RUÍDO
# ===========================================================

plt.figure(figsize=(14, 10))

# Entrada
plt.subplot(2, 2, 1)

plt.plot(t, x)

plt.title("Sinal de Entrada")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid()

# Espectro da entrada
plt.subplot(2, 2, 2)

plt.plot(freqs_pos, X_mag_pos)

plt.title("Espectro de Frequência da Entrada")

plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")

plt.xlim(0, 100)

plt.grid()

# Saída por convolução
plt.subplot(2, 2, 3)

plt.plot(t, y_conv)

plt.title("Saída por Convolução")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid()

# Saída por Fourier
plt.subplot(2, 2, 4)

plt.plot(t, y_fft)

plt.title("Saída por Fourier")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid()

plt.tight_layout()

# ===========================================================
# COMPARAÇÃO ENTRE OS MÉTODOS
# ===========================================================

plt.figure(figsize=(12, 5))

plt.plot(
    t,
    y_conv,
    linewidth=2,
    label="Convolução"
)

plt.plot(
    t,
    y_fft,
    '--',
    linewidth=2,
    label="Fourier"
)

plt.title("Comparação: Convolução vs Fourier")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.legend()

plt.grid()

# ===========================================================
# AGORA COM RUÍDO
# ===========================================================

# Ruído de alta frequência
# 100 Hz

f_noise = 100

noise = 0.4 * np.sin(
    2 * np.pi * f_noise * t
)

# Entrada com ruído
x_noise = x + noise

# ===========================================================
# CONVOLUÇÃO COM RUÍDO
# ===========================================================

y_conv_noise = np.convolve(
    x_noise,
    h,
    mode='full'
)

y_conv_noise = y_conv_noise[:N]

# ===========================================================
# FOURIER COM RUÍDO
# ===========================================================

X_noise = fft(x_noise, N_conv)

Y_noise = X_noise * H_fft

y_fft_noise = np.real(
    ifft(Y_noise)
)

y_fft_noise = y_fft_noise[:N]

# ===========================================================
# ESPECTROS COM RUÍDO
# ===========================================================

X_noise_mag = np.abs(X_noise) / N
Y_noise_mag = np.abs(Y_noise) / N

X_noise_mag_pos = X_noise_mag[positive]
Y_noise_mag_pos = Y_noise_mag[positive]

# ===========================================================
# PLOTS COM RUÍDO
# ===========================================================

plt.figure(figsize=(14, 10))

# Entrada com ruído
plt.subplot(2, 2, 1)

plt.plot(t, x_noise)

plt.title("Entrada com Ruído")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid()

# Espectro da entrada com ruído
plt.subplot(2, 2, 2)

plt.plot(freqs_pos, X_noise_mag_pos)

plt.title("Espectro da Entrada com Ruído")

plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")

plt.xlim(0, 150)

plt.grid()

# Saída filtrada
plt.subplot(2, 2, 3)

plt.plot(t, y_fft_noise)

plt.title("Saída Filtrada")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid()

# Espectro após filtragem
plt.subplot(2, 2, 4)

plt.plot(freqs_pos, Y_noise_mag_pos)

plt.title("Espectro Após Filtragem")

plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")

plt.xlim(0, 150)

plt.grid()

plt.tight_layout()

# ===========================================================
# COMPARAÇÃO FINAL
# ===========================================================

plt.figure(figsize=(12, 5))

plt.plot(
    t,
    x_noise,
    alpha=0.5,
    label="Entrada com Ruído"
)

plt.plot(
    t,
    y_fft_noise,
    linewidth=2,
    label="Saída Filtrada"
)

plt.title("Remoção de Ruído pelo Filtro RC")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.legend()

plt.grid()

# ===========================================================
# MOSTRAR TODOS OS GRÁFICOS
# ===========================================================

plt.show()