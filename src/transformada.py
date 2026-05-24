import numpy as np
import matplotlib.pyplot as plt
import time

def fft_sinal(x, fs):
    """
    FFT de um sinal.
    """

    X = np.fft.fft(x)

    freq = np.fft.fftfreq(len(x), 1/fs)

    return freq, X


def filtrar_passa_baixas(x, fs, fc):
    """
    Remove frequências acima de fc.
    """

    X = np.fft.fft(x)

    freq = np.fft.fftfreq(len(x), 1/fs)

    X_filtrado = X.copy()

    X_filtrado[np.abs(freq) > fc] = 0

    x_filtrado = np.fft.ifft(X_filtrado)

    return x_filtrado.real


def espectro_magnitude(x, fs):

    X = np.fft.fft(x)

    freq = np.fft.fftfreq(len(x), 1/fs)

    return freq, np.abs(X)

# ==================================================
# SINAL
# ==================================================

fs = 1000

t = np.arange(0,1,1/fs)

sinal_util = np.sin(2*np.pi*5*t)

ruido = 0.3*np.sin(2*np.pi*150*t)

x = sinal_util + ruido


# ==================================================
# FFT
# ==================================================

X = np.fft.fft(x)

freq = np.fft.fftfreq(len(x),1/fs)


# ==================================================
# FILTRAGEM
# ==================================================

X_filtrado = X.copy()

X_filtrado[np.abs(freq) > 50] = 0

x_filtrado = np.fft.ifft(X_filtrado)


# ==================================================
# COMPARAÇÃO DE TEMPOS
# ==================================================

h = np.exp(-20*t)

inicio = time.perf_counter()

y_conv = np.convolve(x,h)

fim = time.perf_counter()

tempo_conv = fim - inicio


inicio = time.perf_counter()

X1 = np.fft.fft(x,len(x)+len(h)-1)

H1 = np.fft.fft(h,len(x)+len(h)-1)

Y = X1*H1

y_fft = np.fft.ifft(Y)

fim = time.perf_counter()

tempo_fft = fim - inicio


print()
print("TEMPOS DE EXECUÇÃO")
print("-----------------------")
print(f"Convolução direta : {tempo_conv:.6f} s")
print(f"Via FFT           : {tempo_fft:.6f} s")

print()

if tempo_fft != 0:
    print(
        f"A abordagem via Fourier foi "
        f"{tempo_conv/tempo_fft:.2f} vezes mais rápida."
    )


# ==================================================
# GRÁFICOS
# ==================================================

plt.figure(figsize=(12,8))

plt.subplot(3,1,1)
plt.plot(t,x)

plt.title("Sinal no domínio do tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(freq[:500],np.abs(X[:500]))

plt.title("Transformada de Fourier |X(f)|")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(t,x_filtrado.real)

plt.title("Sinal após filtragem")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(3,1,2)

plt.plot(freq[:500], np.abs(X[:500]))

plt.axvline(5, linestyle='--')
plt.axvline(150, linestyle='--')

plt.text(5, max(np.abs(X[:500]))*0.9, "5 Hz")
plt.text(150, max(np.abs(X[:500]))*0.6, "150 Hz")

plt.title("Transformada de Fourier |X(f)|")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)

#pico em 5 Hz → sinal desejado;
#pico em 150 Hz → ruído;
#após remover as frequências acima de 50 Hz, o ruído desaparece.

plt.tight_layout()
plt.show()