@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Definicje kolorów
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)
call :colorEffect 0a "green"
call :colorEffect 0c "red" 
call :colorEffect 0e "yellow"
call :colorEffect 0b "aqua"
call :colorEffect 0d "purple"
call :colorEffect 07 "white"
call :colorEffect 08 "gray"

:: Funkcja kolorowego tekstu
:color
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%~1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1
exit /b

:: Funkcja efektów kolorów
:colorEffect
for /F "tokens=1,2" %%a in ("%~1 %~2") do set "%~2=%%a"
exit /b

:: Funkcja animowanego tekstu
:animate
setlocal
set "text=%~1"
set "delay=%~2"
if "!delay!"=="" set "delay=50"

for /l %%i in (0,1,1000) do (
    set "char=!text:~%%i,1!"
    if "!char!"=="" goto :end_animate
    <nul set /p "=!char!"
    ping -n 1 -w !delay! 127.0.0.1 >nul 2>&1
)
:end_animate
echo.
endlocal
exit /b

:: Funkcja progress bara
:progress
setlocal
set "width=50"
set "steps=%~1"
set "current=%~2"
set /a "percent=(current*100)/steps"
set /a "bars=(percent*width)/100"

set "progress="
for /l %%i in (1,1,!bars!) do set "progress=!progress!█"
for /l %%i in (1,1,!width!) do if %%i gtr !bars! set "progress=!progress!░"

call :color !green! "green"
call :color !aqua! "aqua"
<nul set /p "=!green!!progress!!aqua! !percent!%%"
echo.
endlocal
exit /b

:: Funkcja sprawdzania errora
:checkError
if !errorlevel! neq 0 (
    call :color !red! "red"
    echo ❌ Blad instalacji
    call :color !gray! "gray"
    pause
    exit /b 1
)
exit /b 0

cls
call :color !purple! "purple"
echo ========================================
echo.
call :color !aqua! "aqua"
echo        ███████╗███████╗████████╗██╗   ██╗██████╗ 
echo        ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
echo        ███████╗█████╗     ██║   ██║   ██║██████╔╝
echo        ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
echo        ███████║███████╗   ██║   ╚██████╔╝██║     
echo        ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
echo.
call :color !purple! "purple"
echo ========================================
echo.
call :color !yellow! "yellow"
call :animate "📦  INSTALATOR BOTA DISCORD - Python 3.11" 20
echo.

call :color !white! "white"
echo 📦 Sprawdzanie wersji Python...
python --version > nul 2>&1
if errorlevel 1 (
    call :color !red! "red"
    echo ❌ Python nie jest zainstalowany!
    call :color !yellow! "yellow"
    echo 🔗 Pobierz Python 3.11 z: https://www.python.org/downloads/release/python-3110/
    echo 📌 Pamietaj o zaznaczeniu "Add Python to PATH" podczas instalacji
    call :color !gray! "gray"
    pause
    exit /b 1
)

:: Sprawdź czy to Python 3.11
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set "python_version=%%I"
for /f "tokens=1,2 delims=." %%I in ("%python_version%") do (
    if not "%%I"=="3" (
        call :color !red! "red"
        echo ❌ Wymagany Python 3.x, znaleziono: %python_version%
        call :color !gray! "gray"
        pause
        exit /b 1
    )
    if not "%%J"=="11" (
        call :color !yellow! "yellow"
        echo ⚠️  Zalecany Python 3.11, znaleziono: %python_version%
        echo 📌 Moze wystapic problem z kompatybilnoscia bibliotek
        timeout /t 2 /nobreak > nul
    )
)

call :color !green! "green"
echo ✅ Znaleziono Python: %python_version%
echo.

call :color !aqua! "aqua"
echo 📦 Instalowanie bibliotek dla Python 3.11...
echo.

set "total_steps=9"
set "current_step=0"

call :color !white! "white"
echo 📦 Instalowanie discord.py 2.3.2...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "discord.py==2.3.2" >nul 2>&1
call :checkError

call :color !white! "white"
echo 📦 Instalowanie pyautogui...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "pyautogui==0.9.54" >nul 2>&1
call :checkError

call :color !white! "white"
echo 📦 Instalowanie psutil...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "psutil==5.9.5" >nul 2>&1
call :checkError

call :color !white! "white"
echo 📦 Instalowanie requests...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "requests==2.31.0" >nul 2>&1
call :checkError

call :color !white! "white"
echo 📦 Instalowanie screen-brightness-control...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "screen-brightness-control==0.9.0" >nul 2>&1
call :checkError

call :color !white! "white"
echo 📦 Instalowanie pygetwindow...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "pygetwindow==0.0.9" >nul 2>&1
call :checkError

call :color !white! "white"
echo 📦 Instalowanie pycaw...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "pycaw==20200826" >nul 2>&1
call :checkError

call :color !white! "white"
echo 📦 Instalowanie comtypes...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "comtypes==1.2.0" >nul 2>&1
call :checkError

call :color !white! "white"
echo 📦 Instalowanie pillow...
call :color !gray! "gray"
set /a "current_step+=1"
call :progress !total_steps! !current_step!
pip install "pillow==9.5.0" >nul 2>&1
call :checkError

echo.
call :color !yellow! "yellow"
echo 🔍 Weryfikacja instalacji...
call :color !gray! "gray"

python -c "import discord; print('✅ discord.py ' + discord.__version__)" 2>&1
python -c "import pyautogui; print('✅ pyautogui')" 2>&1
python -c "import psutil; print('✅ psutil')" 2>&1
python -c "import requests; print('✅ requests ' + requests.__version__)" 2>&1

echo.
call :color !green! "green"
echo ========================================
call :color !aqua! "aqua"
echo ✅ Instalacja zakonczona pomyslnie!
echo 📦 Zainstalowano 9 bibliotek
echo 🐍 Wersja Python: %python_version%
echo.
call :color !yellow! "yellow"
echo 📁 Plik config.json juz istnieje w zip
echo 🚀 Uruchom bota: python bot.py
echo.
call :color !purple! "purple"
echo ========================================
call :color !gray! "gray"

echo.
pause