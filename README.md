# Discord Windows Control Bot 🚀

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.3.2-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Development-yellow.svg)

## 📖 Opis

Zaawansowany bot Discord do zdalnego zarządzania komputerem z systemem Windows. Kontroluj swój komputer z dowolnego miejsca przez Discord - idealny do zdalnej administracji, automatyzacji i zarządzania systemem.

## ⚡ Funkcje

### 🖥️ System Operations
- **Wyłączanie/Restartowanie** komputera
- **Blokowanie** stacji roboczej
- **Informacje o systemie** (CPU, RAM, dyski)
- **Zarządzanie procesami** (lista, zabijanie)

### 🎮 Kontrola Komputera
- **Zrzuty ekranu** (screenshot)
- **Symulacja klawiatury** (wpisywanie tekstu)
- **Kontrola myszy** (kliknięcia)
- **Sterowanie głośnością**
- **Regulacja jasności** ekranu
- **Zarządzanie oknami** (minimalizacja, maksymalizacja)

### 🌐 Sieć i Internet
- **Informacje sieciowe** (ipconfig)
- **Testy połączenia** (ping)
- **Skanowanie portów**
- **Automatyzacja przeglądarki** (otwieranie stron)

### 📁 Zarządzanie Plikami
- **Przeglądanie katalogów**
- **Czytanie plików**
- **Usuwanie plików/folderów**
- **Uruchamianie programów**

### 🔌 Kontrola Urządzeń
- **Zarządzanie USB** (włączanie/wyłączanie)
- **Kontrola Bluetooth**
- **Zarządzanie WiFi**

## 🚀 Instalacja

### Wymagania
- Python 3.11
- Konto Discord
- Bot aplikacja na Discord Developer Portal

### Szybka instalacja (Windows)

1. **Pobierz i wypakuj projekt**
2. **Uruchom instalator**:
   ```cmd
   setup.bat
   ```

3. **Skonfiguruj bota**:
   - Edytuj plik `config.json`
   - Wstaw token swojego bota
   - Ustaw ID administratorów

4. **Uruchom bota**:
   ```cmd
   python bot.py
   ```

### Instalacja ręczna

```bash
# Klonuj repozytorium
git clone https://github.com/twoja_nazwa/discord-windows-bot.git
cd discord-windows-bot

# Instaluj zależności
pip install -r requirements.txt

# Skonfiguruj i uruchom
python bot.py
```

## ⚙️ Konfiguracja

### Plik config.json
```json
{
    "token": "TWÓJ_TOKEN_BOTA_DISCORD",
    "admin_ids": [123456789012345678],
    "allowed_roles": ["Admin"]
}
```

### Konfiguracja bota na Discordzie
1. Stwórz aplikację na [Discord Developer Portal](https://discord.com/developers/applications)
2. Włącz wszystkie **Privileged Gateway Intents**
3. Wygeneruj token i wklej do config.json
4. Zaproś bota na serwer z uprawnieniami:
   - `applications.commands`
   - `Send Messages`
   - `Read Message History`

## 🎮 Użycie

### Podstawowe komendy
```
/pomoc - Wyświetla wszystkie komendy
/shutdown - Wyłącza komputer
/restart - Restartuje komputer
/lock - Blokuje komputer
/screenshot - Robi zrzut ekranu
```

### Przykłady użycia
```bash
# Wyłączenie komputera
/shutdown potwierdzenie: tak

# Zrzut ekranu
/screenshot

# Lista procesów
/tasklist

# Wykonanie komendy systemowej
/cmd komenda: ipconfig
```

## 🌐 Kompatybilność sieciowa

Bot działa w **dowolnej sieci** - nie wymaga:
- ❌ Static IP
- ❌ Port forwarding
- ❌ VPN
- ❌ Dynamic DNS

Wystarczy połączenie internetowe i uruchomiony bot na komputerze docelowym.

## ⚠️ Ostrzeżenia

### Status projektu
🚧 **PROJEKT W ROZWOJU** 🚧
- Nie wszystkie funkcje mogą działać poprawnie
- Możliwe błędy i niestabilność
- Testowane na Windows 10/11

### Bezpieczeństwo
- 🔐 Używaj tylko na zaufanych serwerach
- 🔒 Ogranicz dostęp do zaufanych użytkowników
- ⚠️ Bot ma pełny dostęp do systemu!

## 🛠️ Rozwój

### Struktura projektu
```
discord-windows-bot/
├── bot.py              # Główny plik bota
├── config.json         # Konfiguracja
├── setup.bat           # Instalator Windows
├── requirements.txt    # Zależności Pythona
└── README.md          # Dokumentacja
```

### Dodawanie nowych komend
```python
@bot.tree.command(name="nowakomenda", description="Opis komendy")
async def nowakomenda(interaction: discord.Interaction):
    if not is_admin(interaction): 
        await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
        return
    
    # Tutaj twoja logika
    await interaction.response.send_message("✅ Wykonano!")
```

## 📞 Kontakt

- **Discord:** swaag.gg
- **GitHub:** [Twój profil GitHub]
- **Email:** [Twój email]

## 📜 Licencja

MIT License - szczegóły w pliku [LICENSE](LICENSE)

## 🤝 Wkład

Chcesz pomóc w rozwoju? 
1. Forkuj projekt
2. Stwórz branch dla swojej funkcji
3. Commituj zmiany
4. Stwórz Pull Request

## 🎯 Przyszłe funkcje

- [ ] Szyfrowanie komunikacji
- [ ] Więcej opcji sieciowych
- [ ] Panel webowy
- [ ] Wsparcie dla Linux/Mac
- [ ] Plugin system

---

**⚠️ Uwaga:** Używaj odpowiedzialnie. Twórcy nie ponoszą odpowiedzialności za szkody spowodowane niewłaściwym użyciem.