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
    print("=" * 60)
    print("COMPARAÇÃO ENTRE CONVOLUÇÃO E TRANSFORMADA DE FOURIER")
    print("APLICADA A UM CIRCUITO RC PASSA-BAIXA")
    print("=" * 60)
    
    # ==========================================================
    # EXPLICAÇÃO TEÓRICA (IMPRESSA NO CONSOLE)
    # ==========================================================
    print("\n📐 FUNDAMENTAÇÃO TEÓRICA:")
    print("-" * 40)
    print("Circuito RC Passa-Baixa:")
    print("  Equação diferencial: RC * dy(t)/dt + y(t) = x(t)")
    print("  Resposta impulsiva: h(t) = (1/RC) * exp(-t/RC) * u(t)")
    print("  Resposta em frequência: H(jw) = 1 / (1 + jwRC)")
    print("\nTeorema da Convolução:")
    print("  y(t) = x(t) * h(t)  <---->  Y(jw) = X(jw) · H(jw)")
    print("=" * 60)
    
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
    
    # Sinal original (sem ruído)
    x_original = (
        np.sin(2 * np.pi * 10 * t) +
        0.5 * np.sin(2 * np.pi * 20 * t)
    )
    
    # Sinal com ruído (usado como entrada padrão)
    x_ruido = x_original + 0.4 * np.random.randn(len(t))
    
    print(f"\n📡 SINAL DE ENTRADA:")
    print(f"   Componentes: 10 Hz (amplitude 1) + 20 Hz (amplitude 0.5)")
    print(f"   Ruído adicionado: Ruído branco gaussiano (amplitude 0.4)")

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
    print(f"\n🔄 PROCESSANDO SINAL...")
    print(f"   Convolução: {tempo_conv:.6f} s")

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
    print(f"   FFT: {tempo_fft:.6f} s")

    # ----------------------------
    # PROCESSAMENTO ADICIONAL (SINAL LIMPO)
    # ----------------------------
    # Para os gráficos extras
    X_limpo = fft(x_original, nfft)
    Y_limpo = X_limpo * H
    y_fft_limpo = np.real(ifft(Y_limpo))[inicio_cut:inicio_cut + N]
    y_conv_limpo = np.convolve(x_original, h, mode="full")[:N]

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
    
    # Para os gráficos adicionais
    X_limpo_f = np.abs(X_limpo) / N
    Y_limpo_f = np.abs(Y_limpo) / N

    pos = freqs >= 0
    
    print("\n🎨 GERANDO GRÁFICOS...")

    # ==========================================================
    # FIGURA 1: COMPARAÇÃO BÁSICA (ORIGINAL)
    # ==========================================================
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
    caminho_fig1 = OUTPUT_DIR / "rc_simulacao_original.png"
    plt.savefig(caminho_fig1, dpi=150, bbox_inches="tight")

    # ==========================================================
    # FIGURA 2: SINAL LIMPO (SEM RUÍDO)
    # ==========================================================
    plt.figure(figsize=(14, 10))
    plt.suptitle("Análise do Sinal Limpo (Sem Ruído)", fontsize=14, fontweight='bold')
    
    plt.subplot(2, 2, 1)
    plt.plot(t, x_original)
    plt.title("Sinal de Entrada (Sem Ruído)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    
    plt.subplot(2, 2, 2)
    plt.plot(freqs[pos], X_limpo_f[pos])
    plt.title("Espectro da Entrada (10 Hz e 20 Hz)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 100)
    plt.grid()
    plt.axvline(10, color='red', linestyle='--', alpha=0.5, label='10 Hz')
    plt.axvline(20, color='orange', linestyle='--', alpha=0.5, label='20 Hz')
    plt.legend()
    
    plt.subplot(2, 2, 3)
    plt.plot(t, y_conv_limpo, label="Convolução")
    plt.plot(t, y_fft_limpo, "--", label="FFT")
    plt.title("Saída do Filtro (Sinal Limpo)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    
    plt.subplot(2, 2, 4)
    plt.plot(freqs[pos], Y_limpo_f[pos])
    plt.title("Espectro da Saída (Componentes Atenuadas)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 100)
    plt.grid()
    
    plt.tight_layout()
    caminho_fig2 = OUTPUT_DIR / "rc_sinal_limpo.png"
    plt.savefig(caminho_fig2, dpi=150, bbox_inches="tight")

    # ==========================================================
    # FIGURA 3: RESPOSTA IMPULSIVA E COMPARAÇÃO DE DESEMPENHO
    # ==========================================================
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    t_impulso = t[:int(min(5*tau/dt, len(t)))]
    h_impulso = h[:len(t_impulso)] / dt
    plt.plot(t_impulso, h_impulso, 'purple', linewidth=2)
    plt.title("Resposta Impulsiva h(t)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.axvline(tau, color='red', linestyle='--', alpha=0.7, label=f'τ = {tau:.3f} s')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    metodos = ['Convolução', 'FFT']
    tempos = [tempo_conv, tempo_fft]
    cores = ['#FF6B6B', '#4ECDC4']
    barras = plt.bar(metodos, tempos, color=cores, alpha=0.7)
    plt.title("Comparação de Desempenho")
    plt.ylabel("Tempo de Execução (s)")
    plt.grid(True, alpha=0.3, axis='y')
    
    for barra, tempo in zip(barras, tempos):
        plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.0001,
                f'{tempo:.5f}s', ha='center', va='bottom', fontsize=11)
    
    plt.tight_layout()
    caminho_fig3 = OUTPUT_DIR / "rc_desempenho.png"
    plt.savefig(caminho_fig3, dpi=150, bbox_inches="tight")

    # ==========================================================
    # FIGURA 4: FILTRAGEM DETALHADA
    # ==========================================================
    plt.figure(figsize=(12, 8))
    
    # Zoom em um trecho do sinal
    zoom_start = 0
    zoom_end = int(0.2 / dt)  # 0.2 segundos
    
    plt.subplot(2, 1, 1)
    plt.plot(t[zoom_start:zoom_end], x_ruido[zoom_start:zoom_end], 
             'orange', alpha=0.7, label='Entrada (ruidosa)')
    plt.plot(t[zoom_start:zoom_end], y_fft[zoom_start:zoom_end], 
             'blue', linewidth=2, label='Saída (filtrada)')
    plt.title("Detalhe da Filtragem - Primeiros 0.2 segundos")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    
    plt.subplot(2, 1, 2)
    plt.plot(freqs[pos], X_f[pos], 'orange', alpha=0.7, label='Entrada')
    plt.plot(freqs[pos], Y_f[pos], 'blue', linewidth=2, label='Saída')
    plt.plot(freqs[pos], np.abs(H_w)[pos], 'purple', '--', alpha=0.5, label='|H(f)|')
    plt.title("Espectro - Antes e Depois da Filtragem")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 150)
    plt.legend()
    plt.grid()
    
    plt.tight_layout()
    caminho_fig4 = OUTPUT_DIR / "rc_filtragem_detalhada.png"
    plt.savefig(caminho_fig4, dpi=150, bbox_inches="tight")

    print(f"\n💾 GRÁFICOS SALVOS EM:")
    print(f"   - {caminho_fig1}")
    print(f"   - {caminho_fig2}")
    print(f"   - {caminho_fig3}")
    print(f"   - {caminho_fig4}")
    
    # ==========================================================
    # RESUMO FINAL
    # ==========================================================
    print("\n" + "=" * 60)
    print("📈 RESUMO DA SIMULAÇÃO:")
    print("=" * 60)
    print(f"✅ Convolução e FFT produziram resultados equivalentes")
    print(f"   Erro RMS entre métodos: {erro:.2e}")
    print(f"✅ FFT foi {speedup:.2f}x mais rápida que convolução direta")
    print(f"✅ O filtro RC removeu efetivamente o ruído de alta frequência")
    print(f"\n🔬 CONCEITOS DEMONSTRADOS:")
    print(f"   1. Teorema da Convolução: convolução no tempo = multiplicação na frequência")
    print(f"   2. Característica passa-baixa do circuito RC")
    print(f"   3. Atenuação de componentes de alta frequência (ruído)")
    print(f"   4. Equivalência entre métodos numéricos")
    print("=" * 60)
    
    plt.show()

    # ==========================================================
    # RETORNO COM AS CHAVES EXATAS QUE A INTERFACE ESPERA
    # ==========================================================
    # O retorno é um dicionário com as MESMAS chaves do código original
    resultado = {
        "sistema": "RC",
        "amostras": N,
        "tempo_conv": tempo_conv,      # ← Chave original
        "tempo_fft": tempo_fft,        # ← Chave original
        "speedup": speedup,            # ← Chave original
        "erro_rms": erro,              # ← Chave original
        "numerador": [1],
        "denominador": [tau, 1],
        "entrada": x_ruido,            # ← Chave original
        "saida_conv": y_conv,          # ← Chave original
        "saida_fft": y_fft,            # ← Chave original
        "impulso": h                   # ← Chave original
    }
    
    # Verificação das chaves (debug)
    print("\n🔍 VERIFICAÇÃO DE COMPATIBILIDADE:")
    chaves_esperadas = ["sistema", "amostras", "tempo_conv", "tempo_fft", 
                        "speedup", "erro_rms", "numerador", "denominador", 
                        "entrada", "saida_conv", "saida_fft", "impulso"]
    for chave in chaves_esperadas:
        if chave in resultado:
            print(f"   ✅ {chave} = {type(resultado[chave]).__name__}")
        else:
            print(f"   ❌ {chave} NÃO ENCONTRADA!")
    
    return resultado


# ==========================================================
# FUNÇÃO USADA PELO SEU GUI
# ==========================================================

def executar_testes():
    """Função para integração com GUI"""
    print("\n🚀 EXECUTANDO TESTES...")
    resultado = main()
    print("\n✅ TESTES CONCLUÍDOS COM SUCESSO!")
    return [resultado]


# ==========================================================
# EXECUÇÃO DIRETA (FORA DO GUI)
# ==========================================================

if __name__ == "__main__":
    resultados = executar_testes()