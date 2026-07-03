$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$pythonCommand = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCommand = 'python'
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCommand = 'py'
}
else {
    Write-Host 'Python nao foi encontrado no seu sistema.' -ForegroundColor Red
    Write-Host 'Instale o Python em https://www.python.org/downloads/ e confirme se o comando python ou py esta no PATH.' -ForegroundColor Yellow
    Read-Host 'Pressione Enter para sair'
    exit 1
}

Write-Host 'Instalando dependencias...' -ForegroundColor Cyan
if ($pythonCommand -eq 'py') {
    & py -3 -m pip install -r requirements.txt
} else {
    & python -m pip install -r requirements.txt
}
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host 'Se ainda nao tiver uma conta no Kaggle, crie uma em https://www.kaggle.com/' -ForegroundColor Yellow
Write-Host 'E gere um token em Account > Create New API Token.' -ForegroundColor Yellow
Write-Host 'Depois coloque o arquivo kaggle.json em %USERPROFILE%\.kaggle\kaggle.json' -ForegroundColor Yellow

Write-Host 'Baixando dados do Olist...' -ForegroundColor Cyan
if ($pythonCommand -eq 'py') {
    & py -3 .\src\download_olist_data.py
} else {
    & python .\src\download_olist_data.py
}
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host 'Processo concluido.' -ForegroundColor Green
Read-Host 'Pressione Enter para sair'
