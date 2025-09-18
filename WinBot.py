import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import platform
import subprocess
import time
import json
import pyautogui
import webbrowser
import psutil
import ctypes
import socket
import shutil
import screen_brightness_control as sbc
import pygetwindow as gw
import pycaw.pycaw as pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from discord.app_commands import Choice

# Konfiguracja
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"token": "TWÓJ_TOKEN_BOTA", "admin_ids": [], "allowed_roles": ["Admin"]}

config = load_config()

# Bot TYLKO do slash commands - bez prefixu!
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

def is_admin(interaction):
    return (interaction.user.id in config.get("admin_ids", []) or 
            any(role.name in config.get("allowed_roles", []) for role in interaction.user.roles))

@bot.event
async def on_ready():
    print(f'✅ Zalogowano jako {bot.user.name}')
    
    # Synchronizacja slash commands
    try:
        synced = await bot.tree.sync()
        print(f'✅ Zsynchronizowano {len(synced)} slash commands:')
        for cmd in synced:
            print(f'   ➤ /{cmd.name}')
    except Exception as e:
        print(f'❌ Błąd synchronizacji: {e}')

# ========== 🎮 PODSTAWOWE KOMENDY ==========
@bot.tree.command(name="pomoc", description="Wyświetla wszystkie komendy")
async def pomoc(interaction: discord.Interaction):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    embed = discord.Embed(title="⚡ FSOCIETY CONTROL PANEL", color=0x00ff00)
    embed.description = "**Dostępne komendy:**\n\n"
    
    embed.add_field(name="🔧 System", 
                   value="• `/shutdown` - Wyłącza komputer\n• `/restart` - Restartuje komputer\n• `/lock` - Blokuje komputer\n• `/systeminfo` - Informacje o systemie\n• `/tasklist` - Lista procesów\n• `/killprocess` - Zakończ proces", 
                   inline=False)
    
    embed.add_field(name="🖥️ Kontrola", 
                   value="• `/screenshot` - Zrób zrzut ekranu\n• `/volume` - Kontrola głośności\n• `/brightness` - Kontrola jasności\n• `/window` - Zarządzanie oknami\n• `/type` - Wpisuje tekst\n• `/click` - Symuluj kliknięcie", 
                   inline=False)
    
    embed.add_field(name="🌐 Sieć", 
                   value="• `/ipconfig` - Informacje o sieci\n• `/ping` - Test połączenia\n• `/portscan` - Skanowanie portów\n• `/download` - Pobierz plik", 
                   inline=False)
    
    embed.add_field(name="📁 Pliki", 
                   value="• `/explorer` - Otwórz eksplorator\n• `/dir` - Lista plików\n• `/readfile` - Czytaj plik\n• `/delete` - Usuń plik\n• `/execute` - Uruchom plik", 
                   inline=False)
    
    embed.add_field(name="⚙️ Urządzenia", 
                   value="• `/usb` - Kontrola USB\n• `/bluetooth` - Kontrola Bluetooth\n• `/wifi` - Zarządzanie WiFi", 
                   inline=False)
    
    embed.add_field(name="🎮 Inne", 
                   value="• `/ptoszek` - Automatyzacja ptoszek.pl\n• `/cmd` - Wykonuje komendę\n• `/sync` - Synchronizuje komendy", 
                   inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="shutdown", description="Wyłącza komputer")
@app_commands.describe(potwierdzenie="Potwierdź 'tak'")
async def shutdown(interaction: discord.Interaction, potwierdzenie: str = "nie"):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    if potwierdzenie != "tak":
        await interaction.response.send_message("⚠️ Wpisz: `/shutdown potwierdzenie: tak`")
        return
        
    await interaction.response.send_message("🔴 Wyłączanie...")
    os.system("shutdown /s /f /t 0")

@bot.tree.command(name="restart", description="Restartuje komputer")
@app_commands.describe(potwierdzenie="Potwierdź 'tak'")
async def restart(interaction: discord.Interaction, potwierdzenie: str = "nie"):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    if potwierdzenie != "tak":
        await interaction.response.send_message("⚠️ Wpisz: `/restart potwierdzenie: tak`")
        return
        
    await interaction.response.send_message("🔄 Restartowanie...")
    os.system("shutdown /r /f /t 0")

@bot.tree.command(name="lock", description="Blokuje komputer")
async def lock(interaction: discord.Interaction):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    await interaction.response.send_message("🔒 Blokowanie...")
    os.system("rundll32.exe user32.dll,LockWorkStation")

@bot.tree.command(name="usb", description="Kontrola USB")
@app_commands.describe(akcja="Wybierz akcję", czas="Czas w sekundach (tylko dla disable)")
@app_commands.choices(akcja=[
    Choice(name="disable", value="disable"),
    Choice(name="enable", value="enable"),
    Choice(name="list", value="list")
])
async def usb(interaction: discord.Interaction, akcja: str, czas: int = 5):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if akcja == "disable":
            await interaction.response.send_message(f"🔌 Wyłączam USB na {czas}s...")
            result = subprocess.run('pnputil /disable-device "USB\\ROOT_HUB30\\4&2e4d5c8c&0"', shell=True, capture_output=True, text=True)
            await asyncio.sleep(czas)
            subprocess.run('pnputil /enable-device "USB\\ROOT_HUB30\\4&2e4d5c8c&0"', shell=True)
            await interaction.followup.send("✅ USB włączone ponownie")
            
        elif akcja == "enable":
            await interaction.response.send_message("🔌 Włączam USB...")
            result = subprocess.run('pnputil /enable-device "USB\\ROOT_HUB30\\4&2e4d5c8c&0"', shell=True, capture_output=True, text=True)
            await interaction.followup.send("✅ USB włączone")
            
        elif akcja == "list":
            await interaction.response.send_message("📋 Lista urządzeń USB...")
            result = subprocess.run('pnputil /enum-devices /connected /class "USB"', shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            if len(output) > 1500:
                output = output[:1500] + "..."
            await interaction.followup.send(f"```{output}```")
            
    except Exception as e:
        await interaction.followup.send(f"❌ Błąd: {e}")

@bot.tree.command(name="type", description="Wpisuje tekst")
@app_commands.describe(tekst="Tekst do wpisania")
async def type_text(interaction: discord.Interaction, tekst: str):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    pyautogui.write(tekst)
    await interaction.response.send_message(f"⌨️ Wpisano: {tekst}")

@bot.tree.command(name="ptoszek", description="Automatyzacja ptoszek.pl")
async def ptoszek(interaction: discord.Interaction):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    await interaction.response.send_message("🌐 Uruchamiam ptoszek.pl...")
    try:
        webbrowser.open("https://ptoszek.pl")
        await asyncio.sleep(3)
        for _ in range(3):
            pyautogui.press('space')
            await asyncio.sleep(0.5)
        await interaction.followup.send("✅ Automatyzacja zakończona!")
    except Exception as e:
        await interaction.followup.send(f"❌ Błąd: {e}")

@bot.tree.command(name="tasklist", description="Lista procesów")
async def tasklist(interaction: discord.Interaction):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    processes = []
    for proc in psutil.process_iter(['name', 'pid', 'memory_info']):
        try: 
            memory_mb = proc.info['memory_info'].rss / 1024 / 1024
            processes.append(f"{proc.info['name']} (PID: {proc.info['pid']}, RAM: {memory_mb:.1f}MB)")
        except: 
            continue
    
    # Sort by memory usage
    processes.sort(key=lambda x: float(x.split("RAM: ")[1].replace("MB", "")), reverse=True)
    
    process_list = "\n".join(processes[:15])
    await interaction.response.send_message(f"📋 Top 15 procesów:\n```{process_list}```")

@bot.tree.command(name="killprocess", description="Zakończ proces")
@app_commands.describe(pid="ID procesu do zakończenia")
async def killprocess(interaction: discord.Interaction, pid: int):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        process = psutil.Process(pid)
        process_name = process.name()
        process.terminate()
        await interaction.response.send_message(f"✅ Zakończono proces: {process_name} (PID: {pid})")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="cmd", description="Wykonuje komendę CMD")
@app_commands.describe(komenda="Komenda do wykonania")
async def cmd(interaction: discord.Interaction, komenda: str):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        result = subprocess.run(komenda, shell=True, capture_output=True, text=True, timeout=15)
        output = result.stdout if result.stdout else result.stderr
        if len(output) > 1500: 
            output = output[:1500] + "..."
        await interaction.response.send_message(f"💻 Wynik:\n```{output}```")
    except subprocess.TimeoutExpired:
        await interaction.response.send_message("❌ Komenda przekroczyła limit czasu (15s)")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="screenshot", description="Robienie zrzutu ekranu")
async def screenshot(interaction: discord.Interaction):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        
        await interaction.response.send_message("📸 Zrzut ekranu:", file=discord.File(screenshot_path))
        
        # Usuń plik po wysłaniu
        os.remove(screenshot_path)
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="systeminfo", description="Informacje o systemie")
async def systeminfo(interaction: discord.Interaction):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        # Pobierz informacje o systemie
        system_info = f"""
        🖥️ **System Information**
        • System: {platform.system()} {platform.release()}
        • Wersja: {platform.version()}
        • Architektura: {platform.architecture()[0]}
        • Procesor: {platform.processor()}
        • Hostname: {socket.gethostname()}
        • IP: {socket.gethostbyname(socket.gethostname())}
        
        💾 **Pamięć**
        • RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB
        • Dostępna RAM: {psutil.virtual_memory().available / (1024**3):.1f} GB
        • Użycie RAM: {psutil.virtual_memory().percent}%
        
        💿 **Dyski**
        """
        
        # Informacje o dyskach
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                system_info += f"• {partition.device}: {usage.total / (1024**3):.1f} GB ({usage.percent}% użyte)\n"
            except:
                continue
        
        await interaction.response.send_message(system_info)
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="ipconfig", description="Informacje o sieci")
async def ipconfig(interaction: discord.Interaction):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        result = subprocess.run('ipconfig /all', shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
        if len(output) > 1500:
            output = output[:1500] + "..."
        await interaction.response.send_message(f"🌐 Informacje sieciowe:\n```{output}```")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="ping", description="Test połączenia")
@app_commands.describe(host="Host do pingowania")
async def ping(interaction: discord.Interaction, host: str = "google.com"):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        result = subprocess.run(f'ping {host}', shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
        if len(output) > 1500:
            output = output[:1500] + "..."
        await interaction.response.send_message(f"📶 Ping {host}:\n```{output}```")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="volume", description="Kontrola głośności")
@app_commands.describe(poziom="Poziom głośności (0-100)")
async def volume(interaction: discord.Interaction, poziom: int):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if not 0 <= poziom <= 100:
            await interaction.response.send_message("❌ Poziom głośności musi być między 0 a 100")
            return
            
        # Ustaw głośność systemową
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(poziom/100, None)
        
        await interaction.response.send_message(f"🔊 Ustawiono głośność na {poziom}%")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="brightness", description="Kontrola jasności ekranu")
@app_commands.describe(poziom="Poziom jasności (0-100)")
async def brightness(interaction: discord.Interaction, poziom: int):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if not 0 <= poziom <= 100:
            await interaction.response.send_message("❌ Poziom jasności musi być między 0 a 100")
            return
            
        sbc.set_brightness(poziom)
        await interaction.response.send_message(f"💡 Ustawiono jasność na {poziom}%")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="window", description="Zarządzanie oknami")
@app_commands.describe(akcja="Wybierz akcję", tytul="Tytuł okna (dla focus/close)")
@app_commands.choices(akcja=[
    Choice(name="list", value="list"),
    Choice(name="focus", value="focus"),
    Choice(name="close", value="close"),
    Choice(name="minimize", value="minimize"),
    Choice(name="maximize", value="maximize")
])
async def window(interaction: discord.Interaction, akcja: str, tytul: str = ""):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if akcja == "list":
            windows = gw.getAllTitles()
            window_list = "\n".join([f"• {title}" for title in windows if title])
            if len(window_list) > 1500:
                window_list = window_list[:1500] + "..."
            await interaction.response.send_message(f"📋 Aktywne okna:\n```{window_list}```")
            
        elif akcja == "focus" and tytul:
            target_window = gw.getWindowsWithTitle(tytul)
            if target_window:
                target_window[0].activate()
                await interaction.response.send_message(f"🎯 Aktywowano okno: {tytul}")
            else:
                await interaction.response.send_message(f"❌ Nie znaleziono okna: {tytul}")
                
        elif akcja == "close" and tytul:
            target_window = gw.getWindowsWithTitle(tytul)
            if target_window:
                target_window[0].close()
                await interaction.response.send_message(f"❌ Zamknięto okno: {tytul}")
            else:
                await interaction.response.send_message(f"❌ Nie znaleziono okna: {tytul}")
                
        elif akcja == "minimize" and tytul:
            target_window = gw.getWindowsWithTitle(tytul)
            if target_window:
                target_window[0].minimize()
                await interaction.response.send_message(f"📋 Zminimalizowano okno: {tytul}")
            else:
                await interaction.response.send_message(f"❌ Nie znaleziono okna: {tytul}")
                
        elif akcja == "maximize" and tytul:
            target_window = gw.getWindowsWithTitle(tytul)
            if target_window:
                target_window[0].maximize()
                await interaction.response.send_message(f"📋 Maksymalizowano okno: {tytul}")
            else:
                await interaction.response.send_message(f"❌ Nie znaleziono okna: {tytul}")
                
        else:
            await interaction.response.send_message("❌ Nieprawidłowa akcja lub brak tytułu")
            
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="click", description="Symuluj kliknięcie myszą")
@app_commands.describe(button="Przycisk myszy", x="Pozycja X", y="Pozycja Y")
@app_commands.choices(button=[
    Choice(name="left", value="left"),
    Choice(name="right", value="right"),
    Choice(name="middle", value="middle")
])
async def click(interaction: discord.Interaction, button: str, x: int = None, y: int = None):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if x is not None and y is not None:
            pyautogui.click(x, y, button=button)
            await interaction.response.send_message(f"🖱️ Kliknięto {button} na pozycji ({x}, {y})")
        else:
            pyautogui.click(button=button)
            await interaction.response.send_message(f"🖱️ Kliknięto {button} na aktualnej pozycji")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="dir", description="Lista plików w katalogu")
@app_commands.describe(sciezka="Ścieżka katalogu")
async def dir(interaction: discord.Interaction, sciezka: str = "."):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        files = os.listdir(sciezka)
        file_list = "\n".join([f"• {f}" for f in files])
        if len(file_list) > 1500:
            file_list = file_list[:1500] + "..."
        await interaction.response.send_message(f"📁 Pliki w {sciezka}:\n```{file_list}```")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="readfile", description="Czytaj zawartość pliku")
@app_commands.describe(sciezka="Ścieżka do pliku")
async def readfile(interaction: discord.Interaction, sciezka: str):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if not os.path.exists(sciezka):
            await interaction.response.send_message("❌ Plik nie istnieje!")
            return
            
        with open(sciezka, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        if len(content) > 1500:
            content = content[:1500] + "..."
            
        await interaction.response.send_message(f"📄 Zawartość {sciezka}:\n```{content}```")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="delete", description="Usuń plik lub folder")
@app_commands.describe(sciezka="Ścieżka do pliku/folderu")
async def delete(interaction: discord.Interaction, sciezka: str):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if not os.path.exists(sciezka):
            await interaction.response.send_message("❌ Plik/folder nie istnieje!")
            return
            
        if os.path.isfile(sciezka):
            os.remove(sciezka)
            await interaction.response.send_message(f"🗑️ Usunięto plik: {sciezka}")
        else:
            shutil.rmtree(sciezka)
            await interaction.response.send_message(f"🗑️ Usunięto folder: {sciezka}")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="execute", description="Uruchom plik")
@app_commands.describe(sciezka="Ścieżka do pliku")
async def execute(interaction: discord.Interaction, sciezka: str):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if not os.path.exists(sciezka):
            await interaction.response.send_message("❌ Plik nie istnieje!")
            return
            
        os.startfile(sciezka)
        await interaction.response.send_message(f"🚀 Uruchomiono: {sciezka}")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="explorer", description="Otwórz Eksplorator Plików")
@app_commands.describe(sciezka="Ścieżka do otwarcia")
async def explorer(interaction: discord.Interaction, sciezka: str = ""):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if sciezka and not os.path.exists(sciezka):
            await interaction.response.send_message("❌ Ścieżka nie istnieje!")
            return
            
        if sciezka:
            os.startfile(sciezka)
            await interaction.response.send_message(f"📂 Otworzono: {sciezka}")
        else:
            os.system("explorer")
            await interaction.response.send_message("📂 Otworzono Eksplorator Plików")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="download", description="Pobierz plik z URL")
@app_commands.describe(url="URL do pobrania", sciezka="Ścieżka zapisu (opcjonalnie)")
async def download(interaction: discord.Interaction, url: str, sciezka: str = ""):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        import requests
        from urllib.parse import urlparse
        
        await interaction.response.send_message(f"📥 Pobieranie: {url}")
        
        # Pobierz nazwę pliku z URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_file"
            
        # Ustaw ścieżkę zapisu
        if not sciezka:
            sciezka = filename
        elif os.path.isdir(sciezka):
            sciezka = os.path.join(sciezka, filename)
            
        # Pobierz plik
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(sciezka, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        await interaction.followup.send(f"✅ Pobrano: {sciezka}")
    except Exception as e:
        await interaction.followup.send(f"❌ Błąd pobierania: {e}")

@bot.tree.command(name="bluetooth", description="Kontrola Bluetooth")
@app_commands.describe(akcja="Wybierz akcję")
@app_commands.choices(akcja=[
    Choice(name="on", value="on"),
    Choice(name="off", value="off"),
    Choice(name="discoverable", value="discoverable")
])
async def bluetooth(interaction: discord.Interaction, akcja: str):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if akcja == "on":
            subprocess.run('powershell -command "Start-Process bluetoothsettings:"', shell=True)
            await interaction.response.send_message("📱 Włączono Bluetooth")
        elif akcja == "off":
            subprocess.run('powershell -command "Get-PnpDevice -Class Bluetooth | Disable-PnpDevice -Confirm:$false"', shell=True)
            await interaction.response.send_message("📱 Wyłączono Bluetooth")
        elif akcja == "discoverable":
            subprocess.run('powershell -command "Start-Process ms-settings:bluetooth"', shell=True)
            await interaction.response.send_message("📱 Ustawiono tryb wykrywalności Bluetooth")
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="wifi", description="Zarządzanie WiFi")
@app_commands.describe(akcja="Wybierz akcję", nazwa="Nazwa sieci (dla connect)")
@app_commands.choices(akcja=[
    Choice(name="list", value="list"),
    Choice(name="connect", value="connect"),
    Choice(name="disconnect", value="disconnect"),
    Choice(name="on", value="on"),
    Choice(name="off", value="off")
])
async def wifi(interaction: discord.Interaction, akcja: str, nazwa: str = ""):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        if akcja == "list":
            result = subprocess.run('netsh wlan show profiles', shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            if len(output) > 1500:
                output = output[:1500] + "..."
            await interaction.response.send_message(f"📶 Profile WiFi:\n```{output}```")
            
        elif akcja == "connect" and nazwa:
            result = subprocess.run(f'netsh wlan connect name="{nazwa}"', shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            await interaction.response.send_message(f"📶 Łączenie z {nazwa}:\n```{output}```")
            
        elif akcja == "disconnect":
            result = subprocess.run('netsh wlan disconnect', shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            await interaction.response.send_message(f"📶 Rozłączono WiFi:\n```{output}```")
            
        elif akcja == "on":
            result = subprocess.run('netsh interface set interface "Wi-Fi" enabled', shell=True, capture_output=True, text=True)
            await interaction.response.send_message("📶 Włączono WiFi")
            
        elif akcja == "off":
            result = subprocess.run('netsh interface set interface "Wi-Fi" disabled', shell=True, capture_output=True, text=True)
            await interaction.response.send_message("📶 Wyłączono WiFi")
            
        else:
            await interaction.response.send_message("❌ Nieprawidłowa akcja lub brak nazwy sieci")
            
    except Exception as e:
        await interaction.response.send_message(f"❌ Błąd: {e}")

@bot.tree.command(name="portscan", description="Skanowanie portów")
@app_commands.describe(host="Host do skanowania", porty="Zakres portów (np. 80-443)")
async def portscan(interaction: discord.Interaction, host: str = "localhost", porty: str = "1-1000"):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    try:
        await interaction.response.send_message(f"🔍 Skanowanie {host} porty {porty}...")
        
        start_port, end_port = map(int, porty.split('-'))
        open_ports = []
        
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
            
        if open_ports:
            await interaction.followup.send(f"✅ Otwarte porty na {host}: {', '.join(map(str, open_ports))}")
        else:
            await interaction.followup.send(f"❌ Brak otwartych portów w zakresie {porty}")
    except Exception as e:
        await interaction.followup.send(f"❌ Błąd: {e}")

@bot.tree.command(name="sync", description="Synchronizuje komendy")
async def sync(interaction: discord.Interaction):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
        
    await interaction.response.send_message("🔄 Synchronizacja...")
    try:
        synced = await bot.tree.sync()
        await interaction.followup.send(f"✅ Zsynchronizowano {len(synced)} komend!")
    except Exception as e:
        await interaction.followup.send(f"❌ Błąd: {e}")

# URUCHOMIENIE
if __name__ == "__main__":
    # Sprawdź wymagane biblioteki
    try:
        import screen_brightness_control
        import pygetwindow
        import requests
    except ImportError as e:
        print(f"❌ Brak wymaganej biblioteki: {e}")
        print("📦 Zainstaluj brakujące biblioteki:")
        print("pip install screen-brightness-control pygetwindow pycaw requests")
        exit(1)
    
    if config.get("token") and config["token"] != "TWÓJ_TOKEN_BOTA":
        try:
            bot.run(config["token"])
        except discord.LoginFailure:
            print("❌ Błąd logowania - sprawdź token!")
        except Exception as e:
            print(f"❌ Błąd: {e}")
    else:
        print("❌ Brak tokenu w config.json!")