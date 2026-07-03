@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=py -3
    ) else (
        echo Python nao foi encontrado no seu sistema.
        echo Instale o Python em https://www.python.org/downloads/ e certifique-se de que o comando python esteja no PATH.
        pause
        exit /b 1
    )
)

echo Instalando dependencias...
%PYTHON_CMD% -m pip install -r requirements.txt

echo Se ainda nao tiver uma conta no Kaggle, crie uma em https://www.kaggle.com/
echo E gere um token em Account > Create New API Token.
echo Depois coloque o arquivo kaggle.json em %%USERPROFILE%%\.kaggle\kaggle.json

echo Baixando dados do Olist...
%PYTHON_CMD% src\download_olist_data.py

if errorlevel 1 (
    echo Ocorreu um erro durante o download.
    pause
    exit /b 1
)

echo Processo concluido.
pause
