# 🌤️ Weather Widget v2.1.7 - Windows Location Update

## 🛰️ New Feature: GPS/Wi-Fi Location Support!

Get **street-level accurate weather** for YOUR exact location - not your ISP's server!

### 📥 Download

**Python Source (Recommended):**
```bash
pip install PyQt5 requests geocoder
python weather_widget_windows_location_FIXED_FINAL.pyw
```

**Complete Package:**
*[Link to release files]*

---

## ✨ What's New

### 🛰️ Windows Location API Integration
✅ **GPS/Wi-Fi triangulation** - Street-level accuracy (±100m)  
✅ **Dual location system** - Choose IP or Windows Location  
✅ **Smart setup** - Clear instructions when needed  
✅ **Automatic fallback** - Works even if Location disabled  

### 🐛 Bug Fixes
✅ **Fixed city name localization** - Cyrillic → Latin  
✅ **Fixed wind direction** - SR ↔ EN translation  
✅ **Fixed silent errors** - Now shows helpful dialogs  

---

## 📊 Location Accuracy Comparison

| Method | Accuracy | Setup | Best For |
|--------|----------|-------|----------|
| **API Location (IP)** | ±20 km | None | Desktop without Wi-Fi |
| **Windows Location** | ±100 m | One-time | Laptops, accurate weather |

**Example:**
```
Your location:     Novi Beograd
IP shows:          Belgrade (20 km off)
Windows Location:  Novi Beograd ✅ (exact!)
```

---

## 📸 Screenshots

### Main Widget - With Windows Location
![Windows Location](screenshots/windows_location.png)

### Location Source Menu
![Location Menu](screenshots/location_menu.png)

### Setup Dialog
![Setup Dialog](screenshots/location_setup.png)

<details>
<summary>More Screenshots (click to expand)</summary>

### Accuracy Comparison
![Before/After](screenshots/accuracy_comparison.png)

### All Features
- 15-minute nowcast ✅
- Windows Location ✅ (NEW!)
- Bilingual support ✅
- 5-day forecast ✅
- Air quality ✅
- UV index ✅

</details>

---

## 🔧 Requirements

**Basic (API Location):**
- Windows 10/11
- Python 3.8+
- PyQt5, requests, geocoder

**For Windows Location:**
- Wi-Fi adapter
- Location services enabled
- One-time restart

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install PyQt5 requests geocoder

# 2. Run widget
python weather_widget_windows_location_FIXED_FINAL.pyw

# 3. (Optional) Enable Windows Location:
#    Tray → Location Source → Windows Location
#    Follow on-screen instructions if needed
```

---

## 📋 Changelog

### New Features
- 🛰️ Windows Location API support
- 📍 Dual location system (IP + Windows Location)
- ⚠️ Smart detection and setup dialogs
- 🔄 Automatic fallback mechanism

### Bug Fixes
- Fixed Cyrillic city names
- Fixed wind direction translation
- Fixed location error handling
- Improved user notifications

### Technical
- Added geocoder dependency
- Registry validation
- Menu system updates
- Bilingual dialogs

**Full details:** [CHANGELOG.md](CHANGELOG.md)

---

## 🌐 Language Support

**Serbian (Srpski):**
```
📍 Izvor Lokacije
  → API Lokacija (IP)
  → Windows Lokacija (GPS/Wi-Fi)
```

**English:**
```
📍 Location Source
  → API Location (IP)
  → Windows Location (GPS/Wi-Fi)
```

---

## 🛠️ Troubleshooting

### Windows Location Not Working?

**Solution:**
1. Settings → Privacy & Security → Location
2. Turn ON all 3 options
3. Restart computer
4. Try again

**No Wi-Fi?** Use API Location instead - works perfectly!

---

## 🎯 Why This Update?

### Problem (v2.1.6)
```
User in Novi Beograd
IP Location shows: "Belgrade" (wrong!)
User confused: "Why is weather different?"
```

### Solution (v2.1.7)
```
User enables Windows Location
Widget shows: "Novi Beograd" (exact!)
User happy: "Perfect! This is my area!" ✅
```

---

## 📦 What's Included

- Main application file (.pyw)
- Updated requirements.txt
- Comprehensive README
- Detailed CHANGELOG
- MIT License
- Screenshots

---

## 🌟 All Features (v2.1.7)

- ✅ 15-minute precipitation nowcast
- ✅ **Windows Location API** (NEW!)
- ✅ Dual location system (NEW!)
- ✅ Bilingual (Serbian/English)
- ✅ 5-day forecast
- ✅ Air Quality Index (AQI)
- ✅ UV Index
- ✅ System tray integration
- ✅ Sleep mode recovery
- ✅ Click-through mode
- ✅ Auto-start with Windows

---

## 💡 Use Cases

**Perfect for:**
- 🏢 Suburb residents (not city center weather)
- 💼 Commuters (home vs work weather)
- 🌤️ Weather enthusiasts (microclimate tracking)
- 🖥️ Desktop users (API Location works great)
- 💻 Laptop users (Windows Location super accurate)

---

## 🆚 Comparison

### vs. Windows Weather Widget
✅ **Dual location** (Windows: automatic only)  
✅ **15-min nowcast** (Windows: hourly)  
✅ **Always visible** (Windows: sidebar only)  
✅ **No telemetry** (Windows: tracks usage)  
✅ **Open source** (Windows: closed)  

---

## ⬆️ Upgrade from v2.1.6

**Super easy!**

1. `pip install geocoder` (new dependency)
2. Replace widget file
3. Restart - done! ✅

All settings preserved! 🎉

---

## 🙏 Credits

- **Weather**: [Open-Meteo](https://open-meteo.com)
- **Geocoding**: [Nominatim](https://nominatim.openstreetmap.org/)
- **Location**: Windows Location Services
- **Framework**: PyQt5

---

## 📞 Support

- 🐛 [Report Issues](https://github.com/malkosvetnik/desktop-weather-widget/issues)
- 💡 [Discussions](https://github.com/malkosvetnik/desktop-weather-widget/discussions)
- ⭐ [Star the repo!](https://github.com/malkosvetnik/desktop-weather-widget)

---

**Made with ❤️ by malkosvetnik**

*Get YOUR local weather, not your ISP's!* 🛰️

---

*If you find this useful, please ⭐ star the repository!*
