@echo off
echo Instalator WinBot - Python 3.11
echo ================================
echo.

python --version
if errorlevel 1 (
    echo BLAD: Python nie znaleziony!
    echo Pobierz Python 3.11 z python.org
    pause
    exit
)

echo Instalowanie bibliotek...
pip install discord.py==2.3.2
pip install pyautogui==0.9.54
pip install psutil==5.9.5
pip install requests==2.31.0
pip install screen-brightness-control==0.9.0
pip install pygetwindow==0.0.9
pip install pycaw==20200826
pip install comtypes==1.2.0
pip install pillow==9.5.0

echo.
echo Instalacja zakonczona!
echo Uruchom: python bot.py
pause
