@echo off

REM Verifica se as bibliotecas estão instaladas
echo Verificando se as bibliotecas necessárias estão instaladas...

pip show colorama >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando colorama...
    pip install colorama
)

pip show gtts >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando gtts...
    pip install gtts
)

pip show psutil >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando psutil...
    pip install psutil
)

pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando pygame...
    pip install pygame
)

pip show pyaudio >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando pyaudio...
    pip install pyaudio
)

pip show SpeechRecognition >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando SpeechRecognition...
    pip install SpeechRecognition
)
:: Executa o arquivo Python FUC.py
if exist "FUC.py" (
    start FUC.py
)


