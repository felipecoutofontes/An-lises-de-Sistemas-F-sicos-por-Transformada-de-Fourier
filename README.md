# Estudo da Transformada de Fourier e Convolução para Análise de Sinais

Trabalho acadêmico de Engenharia dedicado ao estudo da **Transformada de Fourier** e da **Convolução** aplicadas ao processamento de sinais. O projeto utiliza simulações computacionais para demonstrar as principais vantagens da análise no domínio da frequência, incluindo redução da complexidade computacional, identificação de componentes espectrais e filtragem de ruídos.

---

# 📋 Sumário

- [Objetivo](#objetivo)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Descrição dos Scripts](#descrição-dos-scripts)
- [Resultados Esperados](#resultados-esperados)
- [Fundamentação Teórica](#fundamentação-teórica)
- [Discussão dos Resultados](#discussão-dos-resultados)
- [Observações](#observações)
- [Licença](#licença)

---

# Objetivo

Demonstrar experimentalmente algumas das principais vantagens da Transformada de Fourier em relação à análise exclusivamente no domínio do tempo:

- Simplificação computacional de operações de convolução;
- Identificação das frequências presentes em um sinal;
- Filtragem de ruídos no domínio da frequência;
- Visualização e interpretação do espectro de sinais;
- Comparação entre convolução direta e convolução via FFT com métricas de erro e desempenho.

Os experimentos implementados permitem relacionar diretamente a teoria estudada em Processamento de Sinais e Equações Diferenciais com resultados obtidos por simulação computacional.

---

# Requisitos

- Python 3.7 ou superior
- NumPy ≥ 1.20
- SciPy ≥ 1.11
- Matplotlib ≥ 3.3

---

# Instalação

## Windows (Automático)

```bash
instalar_dependencias.bat
```

## Windows, Linux ou macOS

```bash
pip install -r requirements.txt
```

---

# Estrutura do Projeto

```text
Trabalho_EDB/
│
├── src/
│   ├── transformada.py
│   └── convolucao.py
│
├── Simulações/
│   ├── Amp_Op.py
│   └── simu_teo.py
│
├── outputs/
│   └── interface.py
│
├── requirements.txt
├── instalar_dependencias.bat
└── README.md
```

---

# Como Executar

## Executar os scripts principais

### Transformada de Fourier

```bash
python src/transformada.py
```

### Convolução

```bash
python src/convolucao.py
```

### Benchmark com FFT e convolução direta

```bash
python Simulações/Amp_Op.py
```

### Simulações teóricas adicionais

```bash
python Simulações/simu_teo.py
```

### Interface para visualizar os resultados do Amp_Op

```bash
python outputs/interface.py
```

Todos os gráficos gerados serão exibidos na tela. O script `Amp_Op.py` imprime os resultados do benchmark em texto, enquanto a interface em `outputs/interface.py` permite executar esse benchmark em uma janela gráfica.

---

# Descrição dos Scripts

## transformada.py

### Objetivo

Demonstrar a Transformada Discreta de Fourier (DFT) através da implementação da FFT.

### Funcionalidades

- Geração de sinais no domínio do tempo;
- Aplicação da FFT usando `numpy.fft.fft`;
- Cálculo do espectro de magnitude;
- Visualização simultânea do sinal e de seu espectro;
- Medição do tempo de execução da transformada.

### Sinais analisados

1. Onda senoidal de 5 Hz;
2. Onda quadrada de 3 Hz;
3. Pulso Gaussiano.

### Resultados obtidos

- Representação temporal dos sinais;
- Espectro de magnitude;
- Comparação visual entre diferentes sinais e seus conteúdos espectrais.

---

## convolucao.py

### Objetivo

Demonstrar o cálculo da convolução e comparar a implementação direta com a implementação baseada em Fourier.

### Funcionalidades

- Geração de pares de sinais;
- Convolução direta utilizando `numpy.convolve`;
- Convolução utilizando FFT;
- Comparação visual entre os métodos;
- Medição dos tempos de execução.

### Casos analisados

1. Senoidal × Gaussiano;
2. Quadrada × Gaussiano;
3. Gaussiano × Gaussiano.

### Resultados obtidos

- Sinais de entrada;
- Resultado da convolução;
- Comparação de desempenho entre os métodos.

---

## Amp_Op.py

### Objetivo

Comparar a convolução direta com a convolução realizada via FFT em sistemas lineares representados por filtros e avaliar o erro entre os métodos.

### Funcionalidades

- Geração de sinal composto por senoides e ruído;
- Resposta impulsiva de filtros RC e Butterworth;
- Convolução direta com `numpy.convolve`;
- Convolução via FFT usando `scipy.fft`;
- Cálculo do erro RMS entre os métodos;
- Medição do speedup obtido com o uso da FFT.

### Resultados obtidos

- Tempo de execução da convolução direta;
- Tempo de execução da convolução via FFT;
- Valor do speedup;
- Erro RMS entre as saídas.

---

## simu_teo.py

### Objetivo

Validar experimentalmente as vantagens da Transformada de Fourier apresentadas na fundamentação teórica.

### Experimento 1 – Operações menos complexas

Compara:

- Convolução direta;
- Convolução realizada via Transformada de Fourier.

São medidos os tempos de execução de ambas as abordagens e gerado um gráfico de barras para comparação.

### Experimento 2 – Análise das frequências presentes no sinal

Gera um sinal composto por múltiplas componentes senoidais e aplica a FFT.

São exibidos:

- O sinal no domínio do tempo;
- O espectro de frequência;
- As frequências dominantes identificadas.

### Experimento 3 – Filtragem de ruído

Gera um sinal contaminado por ruído de alta frequência.

A Transformada de Fourier é utilizada para:

- Identificar a frequência do ruído;
- Remover componentes indesejadas do espectro;
- Reconstruir o sinal filtrado.

São exibidos:

- Sinal original com ruído;
- Espectro de frequência;
- Sinal após filtragem.

---

## interface.py

### Objetivo

Disponibilizar uma interface gráfica simples para executar o benchmark do `Amp_Op.py` e visualizar o resultado diretamente na tela.

### Funcionalidades

- Botão para executar o benchmark;
- Campo de texto com a saída do script;
- Botão para limpar a saída;
- Execução em background para não travar a interface.

---

# Resultados Esperados

## Transformada de Fourier

Os espectros obtidos devem apresentar picos nas frequências presentes nos sinais originais.

Por exemplo:

- Senoide de 5 Hz → pico em 5 Hz;
- Sinal composto por 5 Hz e 20 Hz → picos em 5 Hz e 20 Hz.

---

## Convolução

Os resultados obtidos pela convolução direta e pela convolução via FFT devem ser praticamente idênticos, diferindo apenas por pequenos erros numéricos inerentes ao cálculo computacional.

---

## Benchmark Amp_Op

O script `Amp_Op.py` deve apresentar:

- erro RMS muito pequeno entre as saídas;
- ganho de desempenho da FFT em relação à convolução direta;
- valores consistentes para diferentes durações de sinal.

---

## Filtragem de Ruído

Após a remoção das componentes espectrais indesejadas:

- O ruído de alta frequência desaparece;
- O sinal útil é preservado;
- O espectro apresenta apenas as frequências desejadas.

---

# Fundamentação Teórica

## Transformada Discreta de Fourier (DFT)

A DFT converte um sinal do domínio do tempo para o domínio da frequência:

\[
X[k] =
\sum_{n=0}^{N-1}
x[n]
e^{-j2\pi kn/N}
\]

onde:

- \(x[n]\) representa o sinal no tempo;
- \(X[k]\) representa suas componentes espectrais;
- \(N\) é o número de amostras.

---

## Convolução Discreta

A convolução descreve a resposta de sistemas lineares invariantes no tempo:

\[
y[n]
=
\sum_{k=-\infty}^{\infty}
x[k]h[n-k]
\]

onde:

- \(x[n]\) é o sinal de entrada;
- \(h[n]\) é a resposta ao impulso;
- \(y[n]\) é a saída do sistema.

Em implementações computacionais o somatório é limitado ao tamanho dos vetores utilizados.

---

## Teorema da Convolução

Um dos resultados mais importantes da Transformada de Fourier é:

\[
y(t)=x(t)*h(t)
\]

no domínio do tempo equivale a

\[
Y(f)=X(f)\cdot H(f)
\]

no domínio da frequência.

Esse resultado permite substituir uma convolução por uma multiplicação, reduzindo significativamente o custo computacional para sinais grandes.

---

# Discussão dos Resultados

Os experimentos realizados demonstram que:

1. A convolução pode ser substituída por uma multiplicação no domínio da frequência, reduzindo o custo computacional para sinais de grande porte.

2. A Transformada de Fourier permite identificar claramente as frequências presentes em um sinal, informação que não é facilmente observável diretamente no domínio do tempo.

3. Ruídos concentrados em determinadas faixas de frequência podem ser removidos por filtragem espectral de forma simples e eficiente.

4. A análise no domínio da frequência constitui uma ferramenta fundamental em aplicações de telecomunicações, controle, eletrônica, processamento digital de sinais e análise de sistemas físicos.

5. A implementação do benchmark em `Amp_Op.py` e a interface em `outputs/interface.py` tornam os resultados mais acessíveis e fáceis de comparar.

---

# Observações

- Todos os tempos de execução são medidos utilizando `time.perf_counter()`.
- Os valores obtidos podem variar dependendo do hardware utilizado.
- Para sinais pequenos, a convolução direta pode ser competitiva; para sinais maiores, métodos baseados em FFT tendem a apresentar melhor desempenho.
- Os gráficos gerados possuem identificação completa dos eixos e das unidades utilizadas.
- O script `Amp_Op.py` utiliza `scipy` para a implementação da FFT e da resposta impulsiva de filtros.

---

# Licença

Este projeto foi desenvolvido para fins acadêmicos.