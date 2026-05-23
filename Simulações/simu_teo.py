# ============================================================
# SIMULAÇÃO DAS VANTAGENS DA TRANSFORMADA DE FOURIER
#
# Experimento 1:
# Operações menos complexas
# (Convolução direta x Método usando Fourier)
#
# Experimento 2:
# Análise das frequências presentes no sinal
#
# Experimento 3:
# Filtragem de ruído usando Fourier
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import time

# ============================================================
# EXPERIMENTO 1
# COMPARAÇÃO DE TEMPOS
# ============================================================

print("\n" + "="*70)
print("EXPERIMENTO 1 - OPERAÇÕES MENOS COMPLEXAS")
print("="*70)

N = 5000

x = np.random.rand(N)
h = np.random.rand(N)

# -------------------------
# Convolução direta
# -------------------------

inicio = time.perf_counter()

y_conv = np.convolve(x, h)

fim = time.perf_counter()

tempo_conv = fim - inicio

# -------------------------
# Convolução usando Fourier
# -------------------------

inicio = time.perf_counter()

tam_saida = len(x) + len(h) - 1

X = np.fft.fft(x, tam_saida)
H = np.fft.fft(h, tam_saida)

Y = X * H

y_fft = np.fft.ifft(Y)

fim = time.perf_counter()

tempo_fft = fim - inicio

print(f"Tempo da convolução direta : {tempo_conv:.6f} s")
print(f"Tempo usando Fourier       : {tempo_fft:.6f} s")

if tempo_fft > 0:
    print(
        f"\nMétodo usando Fourier foi "
        f"{tempo_conv/tempo_fft:.2f} vezes mais rápido."
    )

# -------------------------
# Gráfico de comparação
# -------------------------

plt.figure(figsize=(7,5))

metodos = [
    "Convolução\nDireta",
    "Via\nFourier"
]

tempos = [
    tempo_conv,
    tempo_fft
]

plt.bar(metodos, tempos)

plt.title(
    "Experimento 1 - Comparação de Tempo de Execução"
)

plt.ylabel("Tempo (s)")

plt.grid(axis='y')

plt.tight_layout()

# ============================================================
# EXPERIMENTO 2
# ANÁLISE DAS FREQUÊNCIAS
# ============================================================

print("\n" + "="*70)
print("EXPERIMENTO 2 - ANÁLISE DAS FREQUÊNCIAS")
print("="*70)

fs = 1000

t = np.arange(0, 1, 1/fs)

# sinal composto

x_freq = (
    np.sin(2*np.pi*5*t)
    +
    0.5*np.sin(2*np.pi*20*t)
)

X_freq = np.fft.fft(x_freq)

freq = np.fft.fftfreq(len(x_freq), 1/fs)

metade = len(freq)//2

plt.figure(figsize=(10,6))

plt.suptitle(
    "Experimento 2 - Frequências que compõem o sinal",
    fontsize=14
)

# -------------------------
# Sinal no tempo
# -------------------------

plt.subplot(2,1,1)

plt.plot(t, x_freq)

plt.title("Sinal composto por 5 Hz e 20 Hz")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid(True)

# -------------------------
# Fourier
# -------------------------

plt.subplot(2,1,2)

plt.plot(
    freq[:metade],
    np.abs(X_freq[:metade])
)

plt.axvline(5, linestyle='--')
plt.axvline(20, linestyle='--')

plt.text(
    5,
    max(np.abs(X_freq[:metade]))*0.9,
    "5 Hz"
)

plt.text(
    20,
    max(np.abs(X_freq[:metade]))*0.5,
    "20 Hz"
)

plt.title("Transformada de Fourier |X(f)|")

plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")

plt.grid(True)

plt.tight_layout()

# ============================================================
# EXPERIMENTO 3
# FILTRAGEM DE RUÍDO
# ============================================================

print("\n" + "="*70)
print("EXPERIMENTO 3 - FILTRAGEM DE RUÍDO")
print("="*70)

sinal_limpo = np.sin(2*np.pi*5*t)

ruido = 0.3*np.sin(2*np.pi*150*t)

sinal_ruidoso = sinal_limpo + ruido

X_ruido = np.fft.fft(sinal_ruidoso)

freq_ruido = np.fft.fftfreq(
    len(sinal_ruidoso),
    1/fs
)

# filtro passa-baixas

X_filtrado = X_ruido.copy()

X_filtrado[np.abs(freq_ruido) > 50] = 0

sinal_filtrado = np.fft.ifft(X_filtrado)

plt.figure(figsize=(10,8))

plt.suptitle(
    "Experimento 3 - Remoção de ruído usando Fourier",
    fontsize=14
)

# -------------------------
# Sinal ruidoso
# -------------------------

plt.subplot(3,1,1)

plt.plot(t, sinal_ruidoso)

plt.title("Sinal com ruído")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid(True)

# -------------------------
# Espectro
# -------------------------

plt.subplot(3,1,2)

plt.plot(
    freq_ruido[:metade],
    np.abs(X_ruido[:metade])
)

plt.axvline(5, linestyle='--')
plt.axvline(150, linestyle='--')

plt.text(
    5,
    max(np.abs(X_ruido[:metade]))*0.9,
    "Sinal útil (5 Hz)"
)

plt.text(
    150,
    max(np.abs(X_ruido[:metade]))*0.5,
    "Ruído (150 Hz)"
)

plt.title("Espectro do sinal")

plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")

plt.grid(True)

# -------------------------
# Sinal filtrado
# -------------------------

plt.subplot(3,1,3)

plt.plot(
    t,
    sinal_filtrado.real
)

plt.title("Sinal após filtragem")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid(True)

plt.tight_layout()

# ============================================================
# EXIBIR TODOS OS GRÁFICOS
# ============================================================

plt.show()

# ============================================================
# CONCLUSÕES
# ============================================================

print("\n" + "="*70)
print("CONCLUSÕES")
print("="*70)

print(
    "\n1) A convolução direta pode demandar mais tempo de "
    "processamento do que a multiplicação no domínio da frequência."
)

print(
    "\n2) A Transformada de Fourier permite identificar "
    "claramente as frequências presentes em um sinal."
)

print(
    "\n3) Ruídos podem ser removidos facilmente "
    "eliminando componentes indesejadas do espectro."
)