import numpy as np
import matplotlib.pyplot as plt


# ==================================================
# PARÂMETROS DO CIRCUITO
# ==================================================

R = 1000          # 1 kΩ
C = 1e-3          # 1 mF

fc = 1/(2*np.pi*R*C)

print(f"Frequência de corte = {fc:.2f} Hz")


# ==================================================
# SINAL DE ENTRADA
# ==================================================

fs = 1000

t = np.arange(0,2,1/fs)

x = (
    np.sin(2*np.pi*5*t)
    +
    0.5*np.sin(2*np.pi*100*t)
)


# ==================================================
# FOURIER DO SINAL
# ==================================================

X = np.fft.fft(x)

freq = np.fft.fftfreq(len(x),1/fs)


# ==================================================
# FUNÇÃO DE TRANSFERÊNCIA
# ==================================================

w = 2*np.pi*freq

H = 1/(1 + 1j*w*R*C)


# ==================================================
# SAÍDA DO SISTEMA
# ==================================================

Y = X * H

y = np.fft.ifft(Y)


# ==================================================
# GRÁFICOS
# ==================================================

metade = len(freq)//2

plt.figure(figsize=(10,8))

plt.suptitle(
    "Filtro Passa-Baixas com Amplificador Operacional"
)

# ---------------------------------

plt.subplot(3,1,1)

plt.plot(t,x)

plt.title("Sinal de entrada")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid(True)

# ---------------------------------

plt.subplot(3,1,2)

plt.plot(
    freq[:metade],
    np.abs(X[:metade])
)

plt.axvline(5, linestyle='--')
plt.axvline(100, linestyle='--')

plt.title("Espectro da entrada")

plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")

plt.grid(True)

# ---------------------------------

plt.subplot(3,1,3)

plt.plot(t,y.real)

plt.title("Saída após o filtro")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

plt.grid(True)

plt.tight_layout()

plt.show()

# Foi modelado um filtro passa-baixas utilizando um amplificador operacional. 
# O sinal de entrada contém uma componente de 5 Hz e uma componente de 100 Hz. 
# Utilizando a Transformada de Fourier, identificamos as frequências presentes e aplicamos a função de transferência do circuito no domínio da frequência.
# Observa-se que a componente de 100 Hz é significativamente atenuada, enquanto a componente de 5 Hz é preservada,
# demonstrando uma aplicação prática da Transformada de Fourier na análise de sistemas físicos.
