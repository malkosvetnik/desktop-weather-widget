# 🚀 Quick Start Guide

Get Desktop Weather Widget running in 5 minutes!

---

## 📋 Prerequisites

- **Windows 10 or 11**
- **Python 3.8+** ([Download](https://www.python.org/downloads/))

Check Python version:
```bash
python --version
```

---

## ⚡ Installation

### Step 1: Download

**Option A: Git Clone**
```bash
git clone https://github.com/malkosvetnik/Desktop-Weather-Widget.git
cd Desktop-Weather-Widget
```

**Option B: Download ZIP**
1. Go to [GitHub repo](https://github.com/malkosvetnik/Desktop-Weather-Widget)
2. Click **Code** → **Download ZIP**
3. Extract to a folder

---

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- PyQt5 (GUI framework)
- requests (HTTP library)
- psutil (system utilities)

---

### Step 3: Run

```bash
python weather_widget_final.pyw
```

**Widget appears on your desktop!** 🎉

---

## ⚙️ Initial Setup

### 1. Choose Language
Right-click tray icon → **🌐 Jezik / Language** → Select **🇷🇸 Srpski** or **🇬🇧 English**

### 2. Set Location Source
Right-click tray icon → **📍 Izvor Lokacije** → Choose:
- **API Lokacija** (automatic IP-based)
- **Windows Lokacija** (GPS/Wi-Fi, requires Location services ON)

### 3. Adjust Temperature Unit
Right-click tray icon → **🌡️ Temperature** → Choose **Celsius** or **Fahrenheit**

### 4. Set Time Format
Right-click tray icon → **🕐 Time Format** → Choose **12h** or **24h**

---

## 🔧 Optional Settings

### Enable Auto-Start with Windows
Right-click tray icon → Check **✓ Pokreni sa Windows-om**

Widget will start automatically on boot!

### Lock Widget Position
Click **🔓** button → Widget position locked (can't be moved accidentally)

### Enable Click-Through Mode
Right-click tray icon → Check **Click-Through Mode**

You can now click through widget to apps behind it!

---

## 🌐 Enable Windows Location (Optional)

For accurate GPS/Wi-Fi location:

1. Press **⊞ Win + I** (open Settings)
2. Go to **Privacy & Security** → **Location**
3. Turn ON **Location services**
4. Turn ON **Let apps access your location**
5. Restart widget if needed

Widget will show accuracy (e.g., "Accuracy: 106m")

---

## 🎨 Customization

### Change Widget Size
Right-click tray icon → **Rezolucija Monitora** → Select your screen resolution

Presets available:
- XGA (1024x768)
- HD Ready (1366x768)
- **Full HD (1920x1080)** ← Default
- QHD (2560x1440)
- 4K UHD (3840x2160)
- 8K UHD (7680x4320)

### Change Refresh Interval
Widget → **Osvežavanje** dropdown → Select **5min**, **10min**, **15min**, **30min**, or **60min**

### Switch Unit System
Right-click tray icon → **📏 Units** → Choose:
- **Metric** (km/h, mbar, km, mm)
- **Imperial** (mph, inHg, mi, in)

---

## 💡 Tips & Tricks

### Viewing Detailed Info
**Hover** over any label to see detailed tooltip:
- 🕐 **Hourly forecast** → Next 12 hours
- 🌫️ **Air Quality** → Detailed pollutants (PM10, PM2.5, CO, NO₂, SO₂, O₃)

### Manual Refresh
Right-click tray icon → **Osveži Vreme**

### Hide Tray Icon (Widget-Only Mode)
Right-click tray icon → **Samo Widget (bez tray-a)**

Widget runs standalone, close with X button.

### Moving Widget
- **Unlocked:** Click and drag anywhere on widget
- **Locked:** Click 🔒 button to unlock first

---

## 🐛 Troubleshooting

### Widget doesn't start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### No weather data
- Check internet connection
- Try manual refresh (right-click tray icon → Osveži Vreme)
- Check console for error messages

### Windows Location not working
1. Verify Location services are ON (Settings → Privacy → Location)
2. Restart widget after enabling Location
3. Try switching to API Location and back

### Widget disappears after restart
- Enable Auto-Start: Right-click tray icon → **✓ Pokreni sa Windows-om**
- Check if widget is off-screen (try resetting position in settings)

---

## 📞 Getting Help

- **Issues:** [GitHub Issues](https://github.com/malkosvetnik/Desktop-Weather-Widget/issues)
- **Documentation:** [README.md](README.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

## 🎉 You're All Set!

Enjoy your new weather widget! 🌤️

For advanced configuration, see [README.md](README.md)

---

*Quick Start Guide v2.2.3 | Updated: January 12, 2026*
