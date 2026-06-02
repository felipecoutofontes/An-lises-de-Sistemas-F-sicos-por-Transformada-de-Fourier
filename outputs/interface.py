import importlib.util
import os
import subprocess
import sys
import threading
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk


# ==========================================================
# Caminho do Amp_Op.py
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

SIMULACOES = {
    "RC": BASE_DIR / "Simulações" / "RC_graf.py",
    "Amp Op": BASE_DIR / "Simulações" / "Amp_Op.py",

}

MODULO_ATUAL = "Amp Op"


# ==========================================================
# Carregamento dinâmico
# ==========================================================

def carregar_amp_op():
    path = SIMULACOES[MODULO_ATUAL]
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado:\n{path}")

    module_name = (
        f"simulacao_{MODULO_ATUAL.lower().replace(' ', '_')}"
    )

    spec = importlib.util.spec_from_file_location(module_name, path)

    if spec is None or spec.loader is None:
        raise RuntimeError(f"Não foi possível carregar:\n{path}")

    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)

    return modulo


def _executar_script(path):
    processo = subprocess.Popen(
        [sys.executable, str(path)],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = processo.communicate()

    if processo.returncode != 0:
        raise RuntimeError(
            f"Erro ao executar {path.name}:\n{stderr.strip()}"
        )


# ==========================================================
# Interface
# ==========================================================

class InterfaceAmpOp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Benchmark FFT x Convolução"
        )

        self.root.geometry(
            "1200x800"
        )

        self.modulo = None

        self.resultados = []

        self._viewer_window = None
        self._viewer_canvas = None
        self._viewer_nome = None
        self._viewer_imagem = None
        self._viewer_graficos = []
        self._viewer_indice = 0

        self._montar_interface()

        self._ativar_estado_espera()

    # ------------------------------------------------------

    def _listar_graficos(self):

        outputs = BASE_DIR / "outputs"

        return sorted(outputs.glob("amp_op_*.png"))

    # ------------------------------------------------------

    def _montar_interface(self):

        frame = ttk.Frame(
            self.root,
            padding=10
        )

        frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        ttk.Label(
            frame,
            text="Benchmark FFT x Convolução para Sistemas Amp Op",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor=tk.W)

        ttk.Label(
            frame,
            text=(
                "Selecione uma linha para visualizar "
                "informações detalhadas do sistema."
            )
        ).pack(anchor=tk.W, pady=(0, 10))

        # --------------------------
        # Botões
        # --------------------------

        controles = ttk.Frame(frame)

        controles.pack(
            fill=tk.X,
            pady=(0, 10)
        )

        self.btn_executar = ttk.Button(
            controles,
            text="Executar Benchmark",
            command=self.executar
        )

        self.btn_executar.pack(
            side=tk.LEFT
        )

        self.btn_graficos = ttk.Button(
            controles,
            text="Abrir Gráficos",
            command=self.abrir_graficos
        )

        self.btn_graficos.pack(
            side=tk.LEFT,
            padx=10
        )

        self.btn_limpar = ttk.Button(
            controles,
            text="Limpar",
            command=self.limpar
        )

        self.btn_limpar.pack(
            side=tk.LEFT
        )

        self.status = ttk.Label(
            controles,
            text=""
        )

        self.status.pack(
            side=tk.LEFT,
            padx=20
        )
        self.seletor_modulo = ttk.Combobox(
            controles,
            values=list(SIMULACOES.keys()),
            state="readonly",
            width=20
        )

        self.seletor_modulo.set(MODULO_ATUAL)

        self.seletor_modulo.pack(side=tk.LEFT, padx=10)

        self.seletor_modulo.bind("<<ComboboxSelected>>", self._trocar_modulo)

        # --------------------------
        # Tabela
        # --------------------------

        self.tabela = ttk.Treeview(
            frame,
            columns=(
                "sistema",
                "amostras",
                "conv",
                "fft",
                "speedup",
                "erro"
            ),
            show="headings",
            height=12
        )

        colunas = {
            "sistema": "Sistema",
            "amostras": "Amostras",
            "conv": "Tempo Conv.",
            "fft": "Tempo FFT",
            "speedup": "Speedup FFT",
            "erro": "Erro RMS"
        }

        for coluna, titulo in colunas.items():

            self.tabela.heading(
                coluna,
                text=titulo
            )

        self.tabela.pack(
            fill=tk.X
        )

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.mostrar_detalhes
        )

        # --------------------------
        # Painel detalhes
        # --------------------------

        detalhes_frame = ttk.LabelFrame(
            frame,
            text="Detalhes do Sistema"
        )

        detalhes_frame.pack(
            fill=tk.BOTH,
            expand=True,
            pady=10
        )

        self.txt_detalhes = tk.Text(
            detalhes_frame,
            height=20,
            font=("Consolas", 10)
        )

        self.txt_detalhes.pack(
            fill=tk.BOTH,
            expand=True
        )

    # ------------------------------------------------------

    def _atualizar_visualizador(self):

        if not self._viewer_graficos:
            return

        if self._viewer_window is None or not self._viewer_window.winfo_exists():
            return

        caminho = self._viewer_graficos[self._viewer_indice]

        self._viewer_nome.configure(
            text=(
                f"{self._viewer_indice + 1}/{len(self._viewer_graficos)}"
                f" - {caminho.name}"
            )
        )

        self._viewer_window.update_idletasks()

        canvas_w = max(700, self._viewer_canvas.winfo_width())
        canvas_h = max(500, self._viewer_canvas.winfo_height())

        resize_filter = getattr(Image, "Resampling", Image).LANCZOS

        with Image.open(caminho) as img:
            img = img.convert("RGB")

            largura, altura = img.size

            escala = min(
                (canvas_w - 40) / largura,
                (canvas_h - 120) / altura
            )

            if escala < 1:
                nova_w = max(1, int(largura * escala))
                nova_h = max(1, int(altura * escala))
                img = img.resize((nova_w, nova_h), resample=resize_filter)

            self._viewer_imagem = ImageTk.PhotoImage(img)

        self._viewer_canvas.delete("all")

        self._viewer_canvas.create_image(
            canvas_w / 2,
            canvas_h / 2,
            image=self._viewer_imagem
        )

    # ------------------------------------------------------

    def _fechar_visualizador(self):

        if self._viewer_window is not None:
            self._viewer_window.destroy()

        self._viewer_window = None
        self._viewer_canvas = None
        self._viewer_nome = None
        self._viewer_imagem = None
        self._viewer_graficos = []
        self._viewer_indice = 0

    # ------------------------------------------------------

    def _mostrar_grafico_anterior(self):

        if not self._viewer_graficos:
            return

        self._viewer_indice = (
            self._viewer_indice - 1
        ) % len(self._viewer_graficos)

        self._atualizar_visualizador()

    # ------------------------------------------------------

    def _mostrar_grafico_proximo(self):

        if not self._viewer_graficos:
            return

        self._viewer_indice = (
            self._viewer_indice + 1
        ) % len(self._viewer_graficos)

        self._atualizar_visualizador()

    # ------------------------------------------------------

    def _abrir_visualizador_graficos(self, graficos):

        self._viewer_graficos = list(graficos)
        self._viewer_indice = 0

        if self._viewer_window is None or not self._viewer_window.winfo_exists():
            self._viewer_window = tk.Toplevel(self.root)
            self._viewer_window.title("Visualização de Gráficos")
            self._viewer_window.geometry("900x700")
            self._viewer_window.minsize(700, 500)

            topo = ttk.Frame(self._viewer_window, padding=(10, 10, 10, 0))
            topo.pack(fill=tk.X)

            self._viewer_nome = ttk.Label(
                topo,
                text="",
                anchor=tk.CENTER,
                font=("Segoe UI", 11, "bold")
            )
            self._viewer_nome.pack(fill=tk.X)

            controles = ttk.Frame(self._viewer_window, padding=(10, 0, 10, 10))
            controles.pack(fill=tk.X)

            ttk.Button(
                controles,
                text="◀ Anterior",
                command=self._mostrar_grafico_anterior
            ).pack(side=tk.LEFT)

            ttk.Button(
                controles,
                text="Próximo ▶",
                command=self._mostrar_grafico_proximo
            ).pack(side=tk.LEFT, padx=10)

            self._viewer_canvas = tk.Canvas(
                self._viewer_window,
                bg="#1f1f1f",
                highlightthickness=0
            )
            self._viewer_canvas.pack(
                fill=tk.BOTH,
                expand=True,
                padx=10,
                pady=(0, 10)
            )

            self._viewer_canvas.bind(
                "<Configure>",
                lambda event: self._atualizar_visualizador()
            )

            self._viewer_window.protocol(
                "WM_DELETE_WINDOW",
                self._fechar_visualizador
            )

        else:
            self._viewer_window.deiconify()
            self._viewer_window.lift()
            self._viewer_window.focus_set()

        self._atualizar_visualizador()

    # ------------------------------------------------------

    def _gerar_graficos_em_background(self):

        try:

            path = SIMULACOES[MODULO_ATUAL]

            if MODULO_ATUAL == "RC":
                _executar_script(path)
                self.root.after(
                    0,
                    lambda: self._finalizar_abertura_graficos(
                        [],
                        rc_only=True
                    )
                )
                return

            if self.modulo is None:
                self.modulo = carregar_amp_op()

            self.modulo.main()

            graficos = self._listar_graficos()

            self.root.after(
                0,
                lambda: self._finalizar_abertura_graficos(graficos)
            )

        except Exception as erro:

            self.root.after(
                0,
                lambda: self._mostrar_erro(str(erro))
        )

    # ------------------------------------------------------

    def abrir_graficos(self):

        self.status.configure(
            text="Gerando gráficos..."
        )

        threading.Thread(
            target=self._gerar_graficos_em_background,
            daemon=True
        ).start()

    # ------------------------------------------------------

    def _finalizar_abertura_graficos(self, graficos, rc_only=False):

        self.status.configure(
            text="Pronto."
        )

        if not graficos:
            if rc_only:
                messagebox.showinfo(
                    "RC Gerado",
                    "O módulo RC foi executado em uma janela separada."
                )
                return

            messagebox.showinfo(
                "Aviso",
                "Nenhum gráfico foi gerado."
            )

            return

        self._abrir_visualizador_graficos(graficos)

    # ------------------------------------------------------

    def _trocar_modulo(self, event=None):
        global MODULO_ATUAL

        MODULO_ATUAL = self.seletor_modulo.get()

        self.status.configure(
            text=f"Módulo selecionado: {MODULO_ATUAL}"
        )

        # opcional: limpar resultados ao trocar
        self.limpar()

    # ------------------------------------------------------

    def _ativar_estado_execucao(self):

        self.btn_executar.configure(
            state=tk.DISABLED
        )

        self.status.configure(
            text="Executando..."
        )

    # ------------------------------------------------------

    def _ativar_estado_espera(self):

        self.btn_executar.configure(
            state=tk.NORMAL
        )

        self.status.configure(
            text="Pronto."
        )

    # ------------------------------------------------------

    def limpar(self):

        for item in self.tabela.get_children():

            self.tabela.delete(item)

        self.txt_detalhes.delete(
            "1.0",
            tk.END
        )

    # ------------------------------------------------------

    def executar(self):

        self.limpar()

        self._ativar_estado_execucao()

        thread = threading.Thread(
            target=self._executar_em_background,
            daemon=True
        )

        thread.start()

    # ------------------------------------------------------

    def _executar_em_background(self):

        try:

            if MODULO_ATUAL == "RC":
                path = SIMULACOES[MODULO_ATUAL]
                _executar_script(path)
                self.root.after(
                    0,
                    lambda: [
                        self.status.configure(
                            text="RC executado em uma janela separada."
                        ),
                        self._ativar_estado_espera()
                    ]
                )
                return

            self.modulo = carregar_amp_op()

            resultados = (
                self.modulo.executar_testes()
            )

            self.root.after(
                0,
                lambda:
                self._mostrar_resultados(resultados)
            )

        except Exception as erro:

            self.root.after(
                0,
                lambda:
                self._mostrar_erro(str(erro))
            )

    # ------------------------------------------------------

    def _mostrar_resultados(self, resultados):

        self.resultados = resultados

        for r in resultados:

            self.tabela.insert(
                "",
                tk.END,
                values=(
                    r["sistema"],
                    r["amostras"],
                    f"{r['tempo_conv']:.6f}",
                    f"{r['tempo_fft']:.6f}",
                    f"{r['speedup']:.2f}x",
                    f"{r['erro_rms']:.2e}"
                )
            )

        self.status.configure(
            text=f"{len(resultados)} testes concluídos."
        )

        self._ativar_estado_espera()

    # ------------------------------------------------------

    def mostrar_detalhes(self, event=None):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        indice = self.tabela.index(
            selecionado[0]
        )

        r = self.resultados[indice]

        texto = f"""
Sistema:
{r['sistema']}

Número de amostras:
{r['amostras']}

Tempo convolução:
{r['tempo_conv']:.6f} s

Tempo FFT:
{r['tempo_fft']:.6f} s

Speedup:
{r['speedup']:.2f}x

Função de Transferência

Numerador:
{r['numerador']}

Denominador:
{r['denominador']}

Primeiras amostras da entrada:
{r['entrada'][:10]}

Primeiras amostras da saída (Convolução):
{r['saida_conv'][:10]}

Primeiras amostras da saída (FFT):
{r['saida_fft'][:10]}

Primeiras amostras da resposta impulsiva:
{r['impulso'][:10]}

Erro RMS:
{r['erro_rms']:.3e}

Entrada:
x(t)=sin(2π100t)
    +0.25sin(2π3000t)
    +ruído
"""

        self.txt_detalhes.delete(
            "1.0",
            tk.END
        )

        self.txt_detalhes.insert(
            tk.END,
            texto
        )

    # ------------------------------------------------------

    # ------------------------------------------------------

    def abrir_graficos(self):

        self.status.configure(
            text="Gerando gráficos..."
        )

        threading.Thread(
            target=self._gerar_graficos_em_background,
            daemon=True
        ).start()

    # ------------------------------------------------------

    def _mostrar_erro(self, mensagem):

        self._ativar_estado_espera()

        messagebox.showerror(
            "Erro",
            mensagem
        )


# ==========================================================
# Principal
# ==========================================================

def main():

    root = tk.Tk()

    InterfaceAmpOp(root)

    root.mainloop()


if __name__ == "__main__":
    main()