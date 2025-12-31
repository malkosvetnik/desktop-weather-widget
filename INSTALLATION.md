# 📦 Installation Guide

Detaljno uputstvo za instalaciju Weather Widget-a.

---

## 🎯 Metod 1: Pre-built EXE (Preporučeno za početnike)

### Korak 1: Download
1. Idi na [Releases](../../releases)
2. Download latest `Weather-Widget-v1.0.0.zip`
3. Extract ZIP fajl

### Korak 2: Dobij API Key
1. Poseti [OpenWeatherMap](https://openweathermap.org/api)
2. Klikni **"Sign Up"**
3. Napravi besplatan nalog
4. Potvrdi email adresu
5. Login → **"API Keys"** tab
6. Kopiraj svoj API key (npr. `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

**⚠️ NAPOMENA:** API key može da traje 10-15 minuta da se aktivira!

### Korak 3: Pokreni Widget
1. Dvostruki klik na `Weather Widget.exe`
2. Pojavi se **API Key Setup** dialog
3. Zalep API key → Klikni **OK**
4. Widget se pokreće! 🎉

---

## 🐍 Metod 2: Python Source (Za developere)

### Preduslov
- **Python 3.8+** instaliran
- **pip** package manager

### Korak 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/desktop-weather-widget.git
cd desktop-weather-widget
```

### Korak 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Korak 3: Pokreni Widget
```bash
python weather_widget_final.py
```

Pri prvom pokretanju će se tražiti API key.

---

## 🔨 Metod 3: Build Your Own EXE

### Preduslov
- Python 3.8+
- PyInstaller

### Koraci
```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/desktop-weather-widget.git
cd desktop-weather-widget

# 2. Install dependencies + PyInstaller
pip install -r requirements.txt
pip install pyinstaller pillow

# 3. Kreiraj ikonu (optional)
python create_icon.py

# 4. Build EXE
build_exe.bat

# 5. EXE je u dist/ folderu
cd dist
```

---

## ⚙️ Startup sa Windows-om

### Automatski (preko widget-a)
1. Desni klik na tray ikonu
2. Klikni **"✓ Pokreni sa Windows-om"**
3. Gotovo! ✅

### Manuelno
1. Pritisni `Win + R`
2. Otkucaj: `shell:startup`
3. Kopiraj shortcut od `Weather Widget.exe` u taj folder

---

## 🔑 Kako Dobiti API Key

### Detaljni Koraci sa Screenshots

#### 1. Registracija
- Idi na https://openweathermap.org/api
- Klikni **"Sign Up"** (gornji desni ugao)
- Popuni:
  - Username
  - Email
  - Password
- Klikni **"Create Account"**

#### 2. Potvrda Email-a
- Otvori inbox
- Potraži email od OpenWeatherMap
- Klikni **"Verify your email"**

#### 3. Dobij API Key
- Login na OpenWeatherMap
- Klikni svoje ime (gornji desni ugao)
- Izaberi **"My API Keys"**
- Kopiraj default key (ili kreiraj novi)

#### 4. Čekaj Aktivaciju
- ⏱️ **10-15 minuta** može da potraje
- Posle možeš koristiti key

---

## 🛠️ Troubleshooting

### "API key nije validan" (401 error)
**Rešenje:**
1. Proveri da li je key **tačno kopiran** (bez razmaka)
2. **Sačekaj 15 minuta** od kreiranja key-a
3. Proveri da li je nalog **potvrđen** (verify email)

### Widget ne prikazuje vreme
**Rešenje:**
1. Proveri **internet konekciju**
2. Desni klik tray → **"Osveži Vreme"**
3. Promeni API key: Desni klik → **"Promeni API Key"**

### Widget je nevidljiv
**Rešenje:**
1. Desni klik na tray ikonu (sistemski tray, donji desni ugao)
2. Klikni **"Prikaži Widget"**

### Widget je premali/preveliki
**Rešenje:**
1. Desni klik tray → **"Rezolucija Monitora"**
2. Izaberi svoju rezoluciju (npr. Full HD za 1920x1080)

### Startup ne radi
**Rešenje:**
1. Proveri: Settings → Apps → Startup
2. Omogući **"Weather Widget"**

---

## 📊 System Requirements

### Minimum
- **OS:** Windows 10
- **RAM:** 100 MB free
- **Disk:** 50 MB free
- **Internet:** Da (za API pozive)

### Recommended
- **OS:** Windows 10/11
- **RAM:** 500 MB+ free
- **Internet:** Broadband (minimum)
- **Display:** Full HD (1920x1080)

---

## 🆘 Need Help?

- 🐛 **Bug Report:** [GitHub Issues](../../issues)
- 💡 **Feature Request:** [GitHub Issues](../../issues)
- 📧 **Email:** your.email@example.com
- 💬 **Discord:** [Link to Discord] (optional)

---

## ✅ Verification

Posle instalacije, proveri da li sve radi:

- [ ] Widget se pojavljuje na desktop-u
- [ ] Prikazuje trenutnu temperaturu
- [ ] Prikazuje grad/lokaciju
- [ ] Prikazuje sunrise/sunset
- [ ] 5-day forecast je vidljiv
- [ ] Tray ikona pokazuje temperaturu
- [ ] Desni klik na tray otvara menu

Ako sve ✅ - uspešno si instalirao! 🎉

---

**Enjoy your weather widget!** 🌤️
