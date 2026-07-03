@echo off
setlocal
cd /d "%~dp0"

where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
  echo Git nao encontrado. Instale Git e certifique-se de que esteja no PATH.
  pause
  exit /b 1
)

echo Preparando para commitar as mudancas...
git add -A
set /p COMMITMSG=Mensagem do commit (Enter para usar padrao): 
if "%COMMITMSG%"=="" set COMMITMSG=chore: add data ingestion, DuckDB setup and SQL helpers
git commit -m "%COMMITMSG%"
if %ERRORLEVEL% EQU 0 (
  echo Commit criado com sucesso.
) else (
  echo Nao houve mudancas para commitar ou ocorreu um erro no commit.
)

git rev-parse --abbrev-ref HEAD 2>nul > .git_current_branch.txt
set /p BRANCH=<.git_current_branch.txt
del .git_current_branch.txt 2>nul
if "%BRANCH%"=="" set BRANCH=main

echo Branch atual: %BRANCH%

git remote get-url origin >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
  echo Nenhum remote 'origin' encontrado.
  set /p REMOTE_URL=Informe a URL do remote (por ex. https://github.com/usuario/repo.git) ou pressione Enter para cancelar: 
  if "%REMOTE_URL%"=="" (
    echo Push cancelado.
    pause
    exit /b 0
  )
  git remote add origin %REMOTE_URL%
)

echo Enviando para origin/%BRANCH% ...
git push -u origin %BRANCH%
if %ERRORLEVEL% EQU 0 (
  echo Push concluido com sucesso.
) else (
  echo Erro ao enviar para o remote. Verifique a mensagem acima.
)
pause
