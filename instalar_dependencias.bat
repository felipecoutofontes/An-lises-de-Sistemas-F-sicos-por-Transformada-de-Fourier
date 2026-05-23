@echo off
REM Script para instalar dependências no Windows
REM Autor: Felipe Resende e Felipe Couto - UFMG - 2026
REM Descrição: Instala as bibliotecas Python necessárias para rodar transformada.py e convolucao.py

echo.
echo ================================
echo Instalando Dependencias Python
echo ================================
echo.

REM Verificar se Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado no PATH
    echo Certifique-se de que Python está instalado e adicionado ao PATH do sistema
    pause
    exit /b 1
)

echo Python encontrado:
python --version
echo.

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo AVISO: Falha ao atualizar pip, continuando mesmo assim...
)
echo.

REM Instalar dependências do requirements.txt
echo Instalando dependências do requirements.txt...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependências
    pause
    exit /b 1
)

echo.
echo ================================
echo Instalação Concluída com Sucesso!
echo ================================
echo.
echo Você pode agora executar:
echo   python transformada.py
echo   python convolucao.py
echo.
pause
