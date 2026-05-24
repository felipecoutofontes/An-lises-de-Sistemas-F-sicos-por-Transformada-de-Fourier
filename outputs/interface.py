"""
interface.py
Interface gráfica para executar o benchmark do Amp_Op.py e
visualizar os resultados e gráficos gerados.

Autor: Felipe Resende e Felipe Couto - UFMG - 2026
"""

import importlib.util
import threading
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk


# ------------------------------------------------------------------
# Caminhos
# ------------------------------------------------------------------

BASE_DIR    = Path(__file__).resolve().parent.parent
AMP_OP_PATH = BASE_DIR / "Simulações" / "Amp_Op.py"


# ------------------------------------------------------------------
# Carregamento dinâmico do módulo Amp_Op
# ------------------------------------------------------------------

def carregar_amp_op():
    if not AMP_OP_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado:\n{AMP_OP_PATH}")

    spec = importlib.util.spec_from_file_location("amp_op", AMP_OP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Não foi possível carregar:\n{AMP_OP_PATH}")

    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# ------------------------------------------------------------------
# Interface principal
# ------------------------------------------------------------------

class InterfaceAmpOp:

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Benchmark FFT × Convolução")
        self.root.geometry("1200x800")

        self.modulo    = None
        self.resultados: list = []

        # Estado do visualizador de gráficos
        self._viewer_window  = None
        self._viewer_canvas  = None
        self._viewer_nome    = None
        self._viewer_imagem  = None
        self._viewer_graficos: list = []
        self._viewer_indice  = 0

        self._montar_interface()
        self._ativar_estado_espera()

    # ------------------------------------------------------------------
    # Listagem de gráficos gerados
    # ------------------------------------------------------------------

    def _listar_graficos(self) -> list:
        outputs = BASE_DIR / "outputs"
        return sorted(outputs.glob("amp_op_*.png"))

    # ------------------------------------------------------------------
    # Construção da interface (chamado UMA vez no __init__)
    # ------------------------------------------------------------------

    def _montar_interface(self) -> None:
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text="Benchmark FFT × Convolução para Sistemas Amp Op",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor=tk.W)

        ttk.Label(
            frame,
            text="Selecione uma linha para visualizar informações detalhadas do sistema.",
        ).pack(anchor=tk.W, pady=(0, 10))

        # --- Botões ---
        controles = ttk.Frame(frame)
        controles.pack(fill=tk.X, pady=(0, 10))

        self.btn_executar = ttk.Button(controles, text="Executar Benchmark", command=self.executar)
        self.btn_executar.pack(side=tk.LEFT)

        self.btn_graficos = ttk.Button(controles, text="Abrir Gráficos", command=self.abrir_graficos)
        self.btn_graficos.pack(side=tk.LEFT, padx=10)

        self.btn_limpar = ttk.Button(controles, text="Limpar", command=self.limpar)
        self.btn_limpar.pack(side=tk.LEFT)

        self.status = ttk.Label(controles, text="")
        self.status.pack(side=tk.LEFT, padx=20)

        # --- Tabela ---
        colunas = {
            "sistema" : "Sistema",
            "amostras": "Amostras",
            "conv"    : "Tempo Conv.",
            "fft"     : "Tempo FFT",
            "speedup" : "Speedup FFT",
            "erro"    : "Erro RMS",
        }

        self.tabela = ttk.Treeview(
            frame,
            columns=list(colunas.keys()),
            show="headings",
            height=12,
        )
        for col, titulo in colunas.items():
            self.tabela.heading(col, text=titulo)
        self.tabela.pack(fill=tk.X)
        self.tabela.bind("<<TreeviewSelect>>", self.mostrar_detalhes)

        # --- Painel de detalhes ---
        detalhes_frame = ttk.LabelFrame(frame, text="Detalhes do Sistema")
        detalhes_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.txt_detalhes = tk.Text(detalhes_frame, height=20, font=("Consolas", 10))
        self.txt_detalhes.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # Visualizador de gráficos
    # ------------------------------------------------------------------

    def _atualizar_visualizador(self) -> None:
        if not self._viewer_graficos:
            return
        if self._viewer_window is None or not self._viewer_window.winfo_exists():
            return

        caminho = self._viewer_graficos[self._viewer_indice]
        self._viewer_nome.configure(
            text=f"{self._viewer_indice + 1}/{len(self._viewer_graficos)} – {caminho.name}"
        )
        self._viewer_window.update_idletasks()

        canvas_w = max(700, self._viewer_canvas.winfo_width())
        canvas_h = max(500, self._viewer_canvas.winfo_height())
        resize_filter = getattr(Image, "Resampling", Image).LANCZOS

        with Image.open(caminho) as img:
            img = img.convert("RGB")
            escala = min((canvas_w - 40) / img.width, (canvas_h - 120) / img.height)
            if escala < 1:
                img = img.resize(
                    (max(1, int(img.width * escala)), max(1, int(img.height * escala))),
                    resample=resize_filter,
                )
            self._viewer_imagem = ImageTk.PhotoImage(img)

        self._viewer_canvas.delete("all")
        self._viewer_canvas.create_image(canvas_w / 2, canvas_h / 2, image=self._viewer_imagem)

    def _fechar_visualizador(self) -> None:
        if self._viewer_window is not None:
            self._viewer_window.destroy()
        self._viewer_window  = None
        self._viewer_canvas  = None
        self._viewer_nome    = None
        self._viewer_imagem  = None
        self._viewer_graficos = []
        self._viewer_indice  = 0

    def _mostrar_grafico_anterior(self) -> None:
        if not self._viewer_graficos:
            return
        self._viewer_indice = (self._viewer_indice - 1) % len(self._viewer_graficos)
        self._atualizar_visualizador()

    def _mostrar_grafico_proximo(self) -> None:
        if not self._viewer_graficos:
            return
        self._viewer_indice = (self._viewer_indice + 1) % len(self._viewer_graficos)
        self._atualizar_visualizador()

    def _abrir_visualizador_graficos(self, graficos: list) -> None:
        self._viewer_graficos = list(graficos)
        self._viewer_indice   = 0

        if self._viewer_window is None or not self._viewer_window.winfo_exists():
            self._viewer_window = tk.Toplevel(self.root)
            self._viewer_window.title("Visualização de Gráficos")
            self._viewer_window.geometry("900x700")
            self._viewer_window.minsize(700, 500)
            self._viewer_window.protocol("WM_DELETE_WINDOW", self._fechar_visualizador)

            topo = ttk.Frame(self._viewer_window, padding=(10, 10, 10, 0))
            topo.pack(fill=tk.X)

            self._viewer_nome = ttk.Label(topo, text="")
            self._viewer_nome.pack(side=tk.LEFT, expand=True)

            nav = ttk.Frame(self._viewer_window, padding=(10, 0))
            nav.pack(fill=tk.X)
            ttk.Button(nav, text="◀ Anterior", command=self._mostrar_grafico_anterior).pack(side=tk.LEFT)
            ttk.Button(nav, text="Próximo ▶",  command=self._mostrar_grafico_proximo).pack(side=tk.LEFT, padx=10)

            self._viewer_canvas = tk.Canvas(self._viewer_window, bg="white")
            self._viewer_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._atualizar_visualizador()

    # ------------------------------------------------------------------
    # Estados dos botões
    # ------------------------------------------------------------------

    def _ativar_estado_execucao(self) -> None:
        self.btn_executar.configure(state=tk.DISABLED)
        self.status.configure(text="Executando...")

    def _ativar_estado_espera(self) -> None:
        self.btn_executar.configure(state=tk.NORMAL)
        self.status.configure(text="Pronto.")

    # ------------------------------------------------------------------
    # Ações dos botões
    # ------------------------------------------------------------------

    def limpar(self) -> None:
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        self.txt_detalhes.delete("1.0", tk.END)

    def executar(self) -> None:
        self.limpar()
        self._ativar_estado_execucao()
        threading.Thread(target=self._executar_em_background, daemon=True).start()

    def abrir_graficos(self) -> None:
        self.status.configure(text="Gerando gráficos...")
        threading.Thread(target=self._gerar_graficos_em_background, daemon=True).start()

    # ------------------------------------------------------------------
    # Background workers
    # ------------------------------------------------------------------

    def _executar_em_background(self) -> None:
        try:
            self.modulo  = carregar_amp_op()
            resultados   = self.modulo.executar_testes()
            self.root.after(0, lambda: self._mostrar_resultados(resultados))
        except Exception as erro:
            self.root.after(0, lambda e=erro: self._mostrar_erro(str(e)))

    def _gerar_graficos_em_background(self) -> None:
        try:
            modulo = carregar_amp_op()
            fs = 100_000
            for duracao in [0.05, 0.10]:
                for nome, sys in [
                    ("Filtro RC (1ª ordem)",          modulo.sistema_simples()),
                    ("Filtro Butterworth (4ª ordem)",  modulo.sistema_complexo()),
                ]:
                    modulo.benchmark(nome, sys, fs, duracao, mostrar_graficos=True)

            graficos = self._listar_graficos()
            if not graficos:
                self.root.after(0, lambda: self._mostrar_erro("Nenhum gráfico foi gerado."))
                return
            self.root.after(0, lambda: self._abrir_visualizador_graficos(graficos))
            self.root.after(0, lambda: self.status.configure(text=f"{len(graficos)} gráfico(s) disponível(is)."))
        except Exception as erro:
            self.root.after(0, lambda e=erro: self._mostrar_erro(str(e)))

    # ------------------------------------------------------------------
    # Atualização da UI
    # ------------------------------------------------------------------

    def _mostrar_resultados(self, resultados: list) -> None:
        self.resultados = resultados
        for r in resultados:
            self.tabela.insert(
                "", tk.END,
                values=(
                    r["sistema"],
                    r["amostras"],
                    f"{r['tempo_conv']:.6f}",
                    f"{r['tempo_fft']:.6f}",
                    f"{r['speedup']:.2f}×",
                    f"{r['erro_rms']:.2e}",
                ),
            )
        self.status.configure(text=f"{len(resultados)} testes concluídos.")
        self._ativar_estado_espera()

    def mostrar_detalhes(self, event=None) -> None:
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        r = self.resultados[self.tabela.index(selecionado[0])]
        texto = (
            f"Sistema:                 {r['sistema']}\n"
            f"Amostras:                {r['amostras']}\n"
            f"Tempo Convolução:        {r['tempo_conv']:.6f} s\n"
            f"Tempo FFT:               {r['tempo_fft']:.6f} s\n"
            f"Speedup:                 {r['speedup']:.2f}×\n"
            f"Erro RMS:                {r['erro_rms']:.3e}\n\n"
            f"Função de Transferência\n"
            f"  Numerador  : {r['numerador']}\n"
            f"  Denominador: {r['denominador']}\n\n"
            f"Entrada:\n"
            f"  sin(2π·100t) + 0.5·sin(2π·500t) + 0.25·sin(2π·2000t) + ruído\n\n"
            f"Primeiras 10 amostras da entrada:\n  {r['entrada'][:10]}\n\n"
            f"Primeiras 10 amostras da saída (Convolução):\n  {r['saida_conv'][:10]}\n\n"
            f"Primeiras 10 amostras da saída (FFT):\n  {r['saida_fft'][:10]}\n\n"
            f"Primeiras 10 amostras da resposta impulsiva:\n  {r['impulso'][:10]}\n"
        )
        self.txt_detalhes.delete("1.0", tk.END)
        self.txt_detalhes.insert(tk.END, texto)

    def _mostrar_erro(self, mensagem: str) -> None:
        self._ativar_estado_espera()
        messagebox.showerror("Erro", mensagem)


# ------------------------------------------------------------------
# Ponto de entrada
# ------------------------------------------------------------------

def main() -> None:
    root = tk.Tk()
    InterfaceAmpOp(root)
    root.mainloop()


if __name__ == "__main__":
    main()