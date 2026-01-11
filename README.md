# 🌤️ Desktop Weather Widget

A beautiful, customizable desktop weather widget for Windows with real-time weather data, dual location systems, and comprehensive customization options.

[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](https://github.com/malkosvetnik/desktop-weather-widget/releases)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

![Main Widget](screenshots/main_widget_serbian.png)

---

## ✨ Features

### 🌡️ **NEW in v2.2.0: Complete Customization System**

#### Temperature Units
- **Celsius (°C)** or **Fahrenheit (°F)** selection
- Instant conversion across all displays
- Persistent preference storage

#### Time Format
- **12-hour (AM/PM)** or **24-hour** format
- Affects clock, timestamps, sunrise/sunset
- Applies to all time displays

#### Measurement Units
- **Metric** (km/h, mbar, km) or **Imperial** (mph, inHg, mi)
- Wind speed conversion
- Pressure conversion
- Visibility conversion

#### Battery Status (Laptops)
- Real-time battery percentage
- Charging indicator (🔌)
- Color-coded warnings:
  - 🔋 Green: Charging
  - 🔋 White: 30%+ (normal)
  - 🔋 Orange: 15-29% (low)
  - 🪫 Red: <15% (critical)
- Auto-hides on desktop PCs

### ⏱️ Precision Weather Forecasting

#### 15-Minute Nowcast
- Ultra-precise 0-2 hour precipitation forecast
- 8 intervals × 15 minutes = radar-like accuracy
- Real-time alerts: "Rain in 15 min (70%)"
- Smart type detection (rain vs snow)

#### Dual Location System
- **🔡 API Location (IP-based)**: Works everywhere, city-level accuracy
- **🛰️ Windows Location (GPS/Wi-Fi)**: Street-level accuracy (±100m)
- Easy switching via tray menu
- Automatic fallback if unavailable

### 📊 Comprehensive Weather Data

#### Current Conditions
- Temperature with "feels like"
- Weather description with emoji icons
- Humidity percentage
- Wind speed and direction (8 compass points)
- Atmospheric pressure
- Visibility distance
- Cloud cover percentage
- UV Index with color coding
- Air Quality Index (AQI)

#### Forecasts
- **5-Day Forecast**: Min/max temps, weather icons
- **Hourly Forecast (12h)**: Interactive tooltip with detailed data
- **Precipitation Nowcast**: 15-minute precision for 0-2 hours

#### Environmental Monitoring
- **UV Index**: Color-coded (Low/Moderate/High/Very High/Extreme)
- **Air Quality**: AQI with pollutant breakdown
  - PM2.5, PM10, O₃, NO₂, SO₂, CO levels
  - Health implications
  - Color-coded alerts

### 🎨 Customization

#### Display Options
- **Bilingual**: Full Serbian and English support
- **Resolution Presets**: XGA to 8K UHD (8 presets)
- **Position Locking**: Keep widget in place
- **Click-Through Mode**: Interact with desktop through widget
- **Temperature Units**: Celsius or Fahrenheit
- **Time Format**: 12-hour or 24-hour
- **Unit System**: Metric or Imperial

#### System Integration
- **System Tray**: Temperature display in tray icon
- **Auto-Start**: Run with Windows startup
- **Widget-Only Mode**: Hide tray, show widget only
- **Sleep Mode Recovery**: Auto-refresh after wake

### 🔄 Smart Updates

- Auto-refresh: 5-60 minute intervals
- Network retry logic (3 attempts)
- Offline graceful handling
- Sleep/hibernate detection
- Last updated timestamp

---

## 📸 Screenshots

### Main Widget - All Variations

<details>
<summary>Serbian Interface (Click to expand)</summary>

![Serbian Widget](screenshots/main_widget_serbian.png)
*Default Serbian interface with metric units*

</details>

<details>
<summary>English Interface (Click to expand)</summary>

![English Widget](screenshots/main_widget_english.png)
*Full English translation*

</details>

<details>
<summary>Temperature Units (Click to expand)</summary>

![Celsius](screenshots/main_widget_celsius.png)
*Celsius mode*

![Fahrenheit](screenshots/main_widget_fahrenheit.png)
*Fahrenheit mode*

</details>

<details>
<summary>Unit Systems (Click to expand)</summary>

![Metric](screenshots/main_widget_serbian.png)
*Metric: km/h, mbar, km*

![Imperial](screenshots/main_widget_imperial.png)
*Imperial: mph, inHg, mi*

</details>

### Interactive Features

![Hourly Forecast Tooltip](screenshots/hourly_forecast_tooltip.png)
*Interactive 12-hour forecast with detailed data*

![Precipitation Alert](screenshots/precipitation_alert.png)
*Real-time precipitation alerts*

![Air Quality Tooltip](screenshots/air_quality_tooltip.png)
*Detailed air quality breakdown*

### Tray Menu Options

![Tray Menu](screenshots/tray_menu.png)
*Complete tray menu with all options*

![Language Menu](screenshots/language_menu.png)
*Serbian/English language selector*

![Temperature Menu](screenshots/temperature_menu_celsius.png)
*Celsius/Fahrenheit selector*

![Time Format Menu](screenshots/time_format_menu.png)
*12h/24h time format selector*

![Unit System Menu](screenshots/unit_system_menu.png)
*Metric/Imperial unit selector*

![Location Menu Serbian](screenshots/location_menu_serbian.png)
*Location source selector (Serbian)*

![Location Menu English](screenshots/location_menu_english.png)
*Location source selector (English)*

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Windows 10/11**
- **Internet connection**

### Installation

#### Option 1: Run from Source (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget

# 2. Install dependencies
pip install PyQt5 requests geocoder psutil

# 3. Run the widget
python weather_widget_final.pyw
```

#### Option 2: Download EXE (Coming Soon!)

1. Download latest release from [Releases](https://github.com/malkosvetnik/desktop-weather-widget/releases)
2. Extract ZIP file
3. Run `WeatherWidget.exe`

### First-Time Setup

1. Widget appears on desktop
2. Right-click tray icon → Choose language (Serbian/English)
3. Select location source (API or Windows Location)
4. Choose temperature unit (Celsius/Fahrenheit)
5. Select time format (12h/24h)
6. Pick measurement system (Metric/Imperial)
7. Enjoy! 🎉

---

## 📖 Usage Guide

### Customization Options

#### Temperature Units
```
Tray → 🌡️ Temperature Unit
  → Celsius (°C)
  → Fahrenheit (°F)
```
- Converts all temperature displays instantly
- Affects: Current temp, feels like, 5-day forecast, hourly forecast

#### Time Format
```
Tray → 🕐 Time Format
  → 24-hour (17:30)
  → 12-hour (05:30 PM)
```
- Updates clock, timestamps, sunrise/sunset
- Applies to all time displays

#### Measurement Units
```
Tray → 📏 Measurement Units
  → Metric (km/h, mbar, km)
  → Imperial (mph, inHg, mi)
```
- Wind speed: km/h ↔ mph
- Pressure: mbar ↔ inHg
- Visibility: km ↔ mi

#### Language Selection
```
Tray → 🌐 Jezik / Language
  → 🇷🇸 Srpski
  → 🇬🇧 English
```
- Full UI translation
- Affects all text, menus, dialogs

#### Location Source
```
Tray → 📍 Izvor Lokacije / Location Source
  → 🔡 API Lokacija (IP)
  → 🛰️ Windows Lokacija (GPS/Wi-Fi)
```

**API Location (IP):**
- Works everywhere
- No setup required
- City-level accuracy (±20 km)

**Windows Location (GPS/Wi-Fi):**
- Street-level accuracy (±100m)
- Requires Wi-Fi adapter
- One-time setup (see below)

### Windows Location Setup

**Requirements:**
- Wi-Fi adapter (laptops have this)
- Windows 10/11

**Steps:**
1. Press `⊞ Win + I` → Settings
2. Privacy & Security → Location
3. Turn ON all 3 options:
   - Location services
   - Let apps access your location
   - Let desktop apps access your location
4. **Restart computer** (required!)
5. Tray → Location Source → Windows Location

**Troubleshooting:**
- Desktop without Wi-Fi? → Use API Location instead
- Still not working? → Check Windows Settings again
- Privacy concerns? → Use API Location

### Display Modes

#### Position Lock
```
Tray → ✓ Zaključaj poziciju / Lock position
```
- Prevents accidental dragging
- Unlock to reposition

#### Click-Through Mode
```
Tray → Prozirni režim / Click-Through Mode
```
- Interact with desktop through widget
- Widget becomes non-interactive

#### Widget-Only Mode
```
Tray → Widget Only (no tray)
```
- Hides tray icon
- Widget remains visible
- Use X button to close

#### Auto-Start
```
Tray → ✓ Pokreni sa Windows-om / Run at Windows Startup
```
- Launches with Windows
- Widget appears automatically

### Resolution Presets

```
Tray → Rezolucija Monitora / Monitor Resolution
  → XGA (1024x768)
  → Full HD (1920x1080)  ← Recommended
  → 4K UHD (3840x2160)
  → 8K UHD (7680x4320)
```
- Scales widget for your monitor
- Maintains aspect ratio
- Font sizes adjust automatically

### Refresh Interval

```
Header → Osvežavanje / Refresh dropdown
  → 5 min
  → 10 min
  → 15 min
  → 30 min (default)
  → 60 min
```
- Balances freshness vs API usage
- Lower = more current data
- Higher = less network traffic

### Manual Updates

```
Tray → Osvežitemp Vreme / Refresh Weather
```
- Instant data refresh
- Bypasses scheduled update
- Use if data seems stale

---

## 🌍 Language Support

### Serbian (Srpski) - Latin Script

```
🌡️ Jedinica temperature
  → Celzijus (°C)
  → Farenhajt (°F)

🕐 Format vremena
  → 24-satni (17:30)
  → 12-satni (05:30 PM)

📏 Sistem merenja
  → Metrički (km/h, mbar)
  → Imperijalni (mph, inHg)
```

### English

```
🌡️ Temperature Unit
  → Celsius (°C)
  → Fahrenheit (°F)

🕐 Time Format
  → 24-hour (17:30)
  → 12-hour (05:30 PM)

📏 Measurement Units
  → Metric (km/h, mbar)
  → Imperial (mph, inHg)
```

**All features fully translated:**
- UI labels
- Tray menus
- Tooltips
- Weather descriptions
- Dialog messages
- Error messages

---

## ⚙️ Configuration

### Settings Storage

All preferences saved in Windows Registry:
```
HKEY_CURRENT_USER\Software\WeatherWidget
```

**Stored settings:**
- Window position (x, y)
- Widget locked state
- Click-through mode
- Auto-location preference
- Current location
- Refresh interval
- Language (Serbian/English)
- Temperature unit (Celsius/Fahrenheit)
- Time format (12h/24h)
- Unit system (Metric/Imperial)
- Location source (API/Windows)

### Reset to Defaults

Run cleanup script:
```bash
python cleanup_registry.py
```

Or manually delete registry key:
```
regedit → HKEY_CURRENT_USER\Software\WeatherWidget → Delete
```

---

## 🔧 Technical Details

### Data Sources

**Weather Data:**
- [Open-Meteo API](https://open-meteo.com) (Free, no key required!)
- Updates: Every 15 minutes
- Coverage: Worldwide
- Data: Current conditions, hourly, daily, UV, air quality

**Location Services:**
- IP Geolocation: [ip-api.com](https://ip-api.com)
- Reverse Geocoding: [Nominatim](https://nominatim.openstreetmap.org/)
- Windows Location: Native Windows Location API

### API Endpoints

```
Weather: https://api.open-meteo.com/v1/forecast
  - Current conditions
  - Minutely (15-min) forecast
  - Hourly forecast
  - Daily forecast (5-day)
  - UV Index
  
Air Quality: https://air-quality-api.open-meteo.com/v1/air-quality
  - AQI
  - PM2.5, PM10
  - O₃, NO₂, SO₂, CO
```

### Dependencies

```
PyQt5>=5.15.0        # GUI framework
requests>=2.25.0     # HTTP client
geocoder>=1.38.1     # Windows Location API
psutil>=5.8.0        # Battery status
```

Install all:
```bash
pip install PyQt5 requests geocoder psutil
```

### Resource Usage

- **RAM**: ~50-100 MB
- **CPU**: <1% (idle), ~2% (updating)
- **Network**: ~10 KB per API call
- **Disk**: ~500 KB (application)
- **Battery impact**: Negligible (laptop)

### Performance

- **Startup**: <2 seconds
- **UI response**: Instant
- **API calls**: 3-5 seconds
- **Memory footprint**: Minimal
- **Sleep recovery**: <10 seconds

---

## 🛠️ Troubleshooting

### Common Issues

#### Widget not showing
**Solution:**
- Right-click tray icon (bottom-right)
- Click "Prikaži Widget" / "Show Widget"
- Check if widget is off-screen (unlock & drag)

#### Weather data not loading
**Solution:**
1. Check internet connection
2. Tray → Refresh Weather
3. Wait 30 seconds for API response
4. Check firewall (allow Python/widget)

#### Windows Location not working
**Solution:**
1. Desktop PC without Wi-Fi? → Use API Location instead
2. Check Settings → Privacy → Location (all ON)
3. Restart computer (required after enabling)
4. Wait 30 seconds for first Wi-Fi scan

#### Wrong city displayed
**Solutions:**
- **API Location**: Shows ISP location (±20 km)
  - Use manual city search
  - Or enable Windows Location
- **Windows Location**: Enable Wi-Fi, restart computer

#### Widget too small/large
**Solution:**
- Tray → Monitor Resolution
- Select your actual resolution
- Or closest match

#### Battery not showing
**Explanation:**
- Desktop PCs have no battery (normal!)
- Laptops will show battery automatically
- No action needed

#### High CPU/memory usage
**Solutions:**
- Increase refresh interval (30+ min)
- Check for multiple instances running
- Close and restart widget

---

## 🎯 Roadmap

### v2.3.0 (Next)
- [ ] Desktop notifications (Windows toast)
- [ ] Custom themes (dark/light/auto)
- [ ] Widget size presets (mini/compact/full)
- [ ] Weather radar integration

### v2.4.0 (Future)
- [ ] Multiple location tracking
- [ ] Weather alerts (severe weather)
- [ ] Moon phases display
- [ ] Customizable layout

### v3.0.0 (Long-term)
- [ ] macOS support
- [ ] Linux support
- [ ] Mobile companion app
- [ ] Smart home integration

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 🔀 Submit Pull Requests
- 📖 Improve documentation
- 🌍 Add translations

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

**TL;DR:**
- ✅ Use freely (personal/commercial)
- ✅ Modify as needed
- ✅ Distribute copies
- ⚠️ Include original license
- ⚠️ No warranty provided

---

## 🙏 Credits

### Data Providers (Free & Open!)
- **Weather**: [Open-Meteo](https://open-meteo.com)
- **Geocoding**: [Nominatim (OpenStreetMap)](https://nominatim.openstreetmap.org/)
- **IP Location**: [ip-api.com](https://ip-api.com)

### Technologies
- **Framework**: [PyQt5](https://riverbankcomputing.com/software/pyqt/)
- **Location**: [geocoder](https://github.com/DenisCarriere/geocoder)
- **Battery**: [psutil](https://github.com/giampaolo/psutil)
- **Icons**: Unicode emoji

### Special Thanks
- Open-Meteo team (free weather API!)
- PyQt5 contributors
- Open-source community
- All users and testers

---

## 📞 Support

### Get Help
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/malkosvetnik/desktop-weather-widget/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/malkosvetnik/desktop-weather-widget/discussions)
- 📖 **Documentation**: This README
- 📝 **Changelog**: [CHANGELOG.md](CHANGELOG.md)

### Community
- ⭐ Star this repo if useful!
- 🔀 Fork and contribute
- 💬 Share feedback
- 📢 Tell others!

---

## 📊 Comparison

### vs. Windows Built-in Weather Widget

| Feature | This Widget | Windows Weather |
|---------|-------------|-----------------|
| **Temperature units** | ✅ User choice (C/F) | ⚠️ Auto-detect only |
| **Time format** | ✅ 12h/24h choice | ⚠️ System default |
| **Unit system** | ✅ Metric/Imperial | ⚠️ Auto-detect only |
| **15-min nowcast** | ✅ Yes | ❌ No (hourly only) |
| **Location choice** | ✅ API or GPS | ⚠️ GPS only |
| **Bilingual** | ✅ Serbian/English | ❌ No |
| **Always visible** | ✅ Desktop widget | ❌ Sidebar only |
| **Customization** | ✅ Extensive | ⚠️ Limited |
| **Privacy** | ✅ No telemetry | ⚠️ Tracks usage |
| **Open source** | ✅ Yes | ❌ No |
| **Offline handling** | ✅ Graceful | ⚠️ Shows errors |
| **Setup** | ✅ One-time | ✅ None |

---

## 🌟 Why This Widget?

### 1. **Complete Control**
- Choose YOUR preferred units
- Select YOUR time format
- Pick YOUR location method
- Customize EVERYTHING

### 2. **Privacy-Focused**
- No telemetry
- No tracking
- No data collection
- Open source (verify yourself!)

### 3. **Bilingual from Day 1**
- Full Serbian support (Latin)
- Full English support
- Easy language switching
- All features translated

### 4. **Professional UX**
- Intuitive interface
- Helpful error messages
- Persistent settings
- Graceful degradation

### 5. **Feature-Rich**
- 15-minute nowcast
- Dual location system
- Complete customization
- Comprehensive data

---

## 📈 Statistics

**Version**: 2.2.0  
**Release Date**: January 11, 2026  
**Lines of Code**: ~4,000  
**Languages**: Serbian, English  
**Dependencies**: 4 (PyQt5, requests, geocoder, psutil)  
**Platforms**: Windows 10/11  
**License**: MIT (free forever!)  

**Development:**
- 🗓️ Started: December 2025
- 🔄 Updates: Active
- 🐛 Bugs: Actively fixed
- 💡 Features: Continuously added

---

## 🎉 Changelog Highlights

### v2.2.0 (2026-01-11) - Customization Update
- ✨ Added Celsius/Fahrenheit temperature units
- ✨ Added 12h/24h time format selection
- ✨ Added Metric/Imperial unit system
- ✨ Added battery status for laptops
- 🐛 Fixed visibility API handling
- 🐛 Fixed menu translations

### v2.1.7 (2026-01-10) - Windows Location Update
- ✨ Added Windows Location API (GPS/Wi-Fi)
- ✨ Added dual location system
- 🐛 Fixed Cyrillic city names
- 🐛 Fixed wind direction translation

### v2.1.6 (2026-01-09) - Nowcast Update
- ✨ Added 15-minute precision nowcast
- ✨ Improved precipitation alerts
- 🐛 Fixed time rounding

### v2.1.0 (2026-01-05) - English Translation
- ✨ Added full English support
- ✨ Bilingual interface
- 🐛 Fixed precipitation detection

**Full history**: [CHANGELOG.md](CHANGELOG.md)

---

## 📦 Files in This Repository

```
desktop-weather-widget/
├── weather_widget_final.pyw     # Main application (v2.2.0)
├── requirements.txt              # Python dependencies
├── cleanup_registry.py           # Settings cleanup utility
├── README.md                     # This file
├── CHANGELOG.md                  # Version history
├── CONTRIBUTING.md               # Contribution guidelines
├── INSTALLATION.md               # Detailed setup guide
├── RELEASE_NOTES.md              # Release notes
├── LICENSE                       # MIT License
└── screenshots/                  # UI screenshots
    ├── main_widget_serbian.png
    ├── main_widget_english.png
    ├── temperature_menu_celsius.png
    ├── time_format_menu.png
    ├── unit_system_menu.png
    ├── hourly_forecast_tooltip.png
    ├── air_quality_tooltip.png
    ├── precipitation_alert.png
    └── tray_menu.png
```

---

**Made with ❤️ and ☕ by [malkosvetnik](https://github.com/malkosvetnik)**

*Get accurate, customizable weather for YOUR location - YOUR way!* 🌤️

---

**If you find this useful, please ⭐ star the repository!**

---

*Version 2.2.0 - Released January 11, 2026*
