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
- [Licença](#licença)

---

# Objetivo

Demonstrar experimentalmente algumas das principais vantagens da Transformada de Fourier em relação à análise exclusivamente no domínio do tempo:

- Simplificação computacional de operações de convolução;
- Identificação das frequências presentes em um sinal;
- Filtragem de ruídos no domínio da frequência;
- Visualização e interpretação do espectro de sinais.

Os experimentos implementados permitem relacionar diretamente a teoria estudada em Processamento de Sinais e Equações Diferenciais com resultados obtidos por simulação computacional.

---

# Requisitos

- Python 3.7 ou superior
- NumPy ≥ 1.20
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
│   ├── convolucao.py
│   └── simu_teo.py
│
├── outputs/
│
├── docs/
│   ├── README.md
│   └── LICENSE
│
├── requirements.txt
├── instalar_dependencias.bat
└── .gitignore
```

---

# Como Executar

## Executar todos os experimentos

```bash
cd src

python transformada.py
python convolucao.py
python simu_teo.py
```

## Executar individualmente

### Transformada de Fourier

```bash
python src/transformada.py
```

### Convolução

```bash
python src/convolucao.py
```

### Simulações Teóricas

```bash
python src/simu_teo.py
```

Todos os gráficos gerados serão exibidos na tela e, caso implementado nos scripts, poderão ser salvos automaticamente na pasta `outputs/`.

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

---

# Observações

- Todos os tempos de execução são medidos utilizando `time.perf_counter()`.
- Os valores obtidos podem variar dependendo do hardware utilizado.
- Para sinais pequenos, a convolução direta pode ser competitiva; para sinais maiores, métodos baseados em FFT tendem a apresentar melhor desempenho.
- Os gráficos gerados possuem identificação completa dos eixos e das unidades utilizadas.

---

# Licença

Este projeto foi desenvolvido para fins acadêmicos.

Consulte o arquivo `LICENSE` para informações adicionais.