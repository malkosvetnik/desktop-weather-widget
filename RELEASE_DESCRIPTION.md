# 🌤️ Weather Widget v2.2.0 - Customization Update

## 🎨 New Feature: Complete Unit Control!

Get weather **YOUR way** - choose temperature units, time format, measurement system, and see battery status!

### 📥 Download

**Python Source (Recommended):**
```bash
pip install PyQt5 requests geocoder psutil
python weather_widget_final.pyw
```

**EXE (Coming Soon!):**
*Pre-compiled executable will be available shortly*

---

## ✨ What's New in v2.2.0

### 🌡️ Temperature Unit Selection
✅ **Celsius or Fahrenheit** - Full temperature customization  
✅ **Instant conversion** - All displays update in real-time  
✅ **API integration** - Direct parameter support  
✅ **Persistent storage** - Preference saved in Registry  

**Example:**
```
Celsius:    -4.1°C (feels like -8.7°C)
Fahrenheit: 24.8°F (feels like 16.3°F)
```

### 🕐 Time Format Selection
✅ **12-hour or 24-hour** - User choice for all time displays  
✅ **Comprehensive updates** - Clock, sunrise/sunset, timestamps  
✅ **Proper AM/PM** - Clear indicators in 12-hour mode  

**Example:**
```
24-hour: 17:30:45  |  Sunrise: 07:03  |  Sunset: 16:13
12-hour: 05:30:45 PM  |  Sunrise: 07:03 AM  |  Sunset: 04:13 PM
```

### 📏 Measurement Unit System
✅ **Metric or Imperial** - Wind, pressure, visibility units  
✅ **Accurate conversions** - API-level parameter support  
✅ **Instant switching** - All units update simultaneously  

| Parameter | Metric | Imperial |
|-----------|--------|----------|
| **Wind** | 38.2 km/h | 23.8 mph |
| **Pressure** | 1003 mbar | 29.62 inHg |
| **Visibility** | 28.0 km | 91.7 mi |

### 🔋 Battery Status (Laptops)
✅ **Real-time monitoring** - Percentage and charging status  
✅ **Smart detection** - Auto-hides on desktop PCs  
✅ **Color-coded warnings** - Green/white/orange/red indicators  
✅ **Seamless integration** - Displayed beside clock  

**Indicators:**
- 🔌 Green: Charging (any %)
- 🔋 White: 30%+ (normal)
- 🔋 Orange: 15-29% (low)
- 🪫 Red: <15% (critical)

---

## 🐛 Bug Fixes

### Fixed Visibility Data Handling
- ✅ API returns different values for metric vs imperial (not a bug!)
- ✅ Removed double conversion
- ✅ Now displays accurate values for both unit systems

### Fixed Menu Translations
- ✅ All menu titles now properly translate (English/Serbian)
- ✅ Menu options fully localized
- ✅ Dynamic updates when changing language

### Fixed Clock Display
- ✅ Removed border artifacts on desktop PCs
- ✅ Clean, seamless appearance

---

## 📸 Screenshots

### Temperature Units
<table>
<tr>
<td><b>Celsius</b></td>
<td><b>Fahrenheit</b></td>
</tr>
<tr>
<td>-4.1°C</td>
<td>24.8°F</td>
</tr>
<tr>
<td>Feels like: -8.7°C</td>
<td>Feels like: 16.3°F</td>
</tr>
</table>

### Time Formats
<table>
<tr>
<td><b>24-hour</b></td>
<td><b>12-hour</b></td>
</tr>
<tr>
<td>17:30:45</td>
<td>05:30:45 PM</td>
</tr>
<tr>
<td>Sunrise: 07:03</td>
<td>Sunrise: 07:03 AM</td>
</tr>
</table>

### Unit Systems
<table>
<tr>
<td><b>Metric</b></td>
<td><b>Imperial</b></td>
</tr>
<tr>
<td>Wind: 38.2 km/h</td>
<td>Wind: 23.8 mph</td>
</tr>
<tr>
<td>Pressure: 1003 mbar</td>
<td>Pressure: 29.62 inHg</td>
</tr>
<tr>
<td>Visibility: 28.0 km</td>
<td>Visibility: 91.7 mi</td>
</tr>
</table>

---

## 🔧 Requirements

**Basic:**
- Windows 10/11
- Python 3.8+
- Internet connection

**Dependencies:**
```
PyQt5>=5.15.0
requests>=2.25.0
geocoder>=1.38.1
psutil>=5.8.0  # NEW!
```

---

## 🚀 Quick Start

### New Installation
```bash
# 1. Clone repository
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget

# 2. Install dependencies
pip install PyQt5 requests geocoder psutil

# 3. Run widget
python weather_widget_final.pyw

# 4. Configure via tray menu:
#    - Temperature Unit (Celsius/Fahrenheit)
#    - Time Format (12h/24h)
#    - Measurement Units (Metric/Imperial)
```

### Upgrade from v2.1.7
```bash
# 1. Install new dependency
pip install psutil

# 2. Update files
git pull
# Or download latest weather_widget_final.pyw

# 3. Restart widget - all settings preserved!
```

---

## 📋 Changelog Summary

### New Features
- 🌡️ Celsius/Fahrenheit temperature selection
- 🕐 12-hour/24-hour time format selection
- 📏 Metric/Imperial measurement system
- 🔋 Battery status for laptops
- 🌐 Complete menu translation system

### Bug Fixes
- 🐛 Fixed visibility data handling (API quirk)
- 🐛 Fixed menu translation issues
- 🐛 Fixed clock display artifacts

### Technical
- Added psutil dependency
- Enhanced API parameter integration
- Improved settings persistence
- Dynamic UI updates

**Full details:** [CHANGELOG.md](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/CHANGELOG.md)

---

## 🌐 Language Support

**All new features fully translated:**

### Serbian (Srpski)
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

---

## 💡 Use Cases

### International Users
🇺🇸 **USA:** Fahrenheit + Imperial + 12-hour  
🌍 **Europe:** Celsius + Metric + 24-hour  
✈️ **Aviation:** Fahrenheit + Imperial pressure + 24-hour  
🎯 **Custom:** ANY combination YOU prefer!

### Laptop Users
💻 **Mobile workers:** Battery integrated with weather  
🔋 **Power awareness:** Color-coded battery warnings  
⚡ **Charging status:** Clear visual indicator  

---

## 🆚 Comparison

### vs. v2.1.7 (Previous Version)
| Feature | v2.1.7 | v2.2.0 |
|---------|--------|--------|
| Temperature choice | ❌ Celsius only | ✅ Celsius/Fahrenheit |
| Time format | ❌ 24-hour only | ✅ 12h/24h |
| Units | ❌ Metric only | ✅ Metric/Imperial |
| Battery | ❌ No | ✅ Yes (laptops) |
| Customization | ⚠️ Limited | ✅ Complete |

### vs. Windows Weather Widget
| Feature | Windows | This Widget |
|---------|---------|-------------|
| Temperature choice | Auto | User selects |
| Time format | System | User selects |
| Units | Auto | User selects |
| 15-min nowcast | No | Yes |
| Location choice | GPS only | API or GPS |
| Bilingual | No | Yes (SR/EN) |
| Always visible | No | Yes |
| Open source | No | Yes |

---

## ⚠️ Known Limitations

### Battery Status
- Desktop PCs: Battery hidden (no hardware) - **expected behavior**
- Laptops: Battery displayed - **fully functional**
- Update frequency: 30 seconds (reasonable)

### Visibility Data
- API returns different raw values for metric vs imperial
- NOT a bug - API internal behavior
- Values are accurate for selected unit system

---

## 🛠️ Troubleshooting

### Battery not showing
**Explanation:** Desktop PCs have no battery (normal!)  
**Solution:** None needed - laptops will show automatically

### Wrong temperature/units
**Solution:** Tray menu → Select your preferred units  
**Note:** Settings saved automatically

### Menu in wrong language
**Solution:** Tray → 🌐 Jezik/Language → Select language  
**Note:** All menus will translate instantly

---

## 🗺️ Roadmap

### v2.3.0 (Next)
- Desktop notifications (Windows toast)
- Custom themes (dark/light/auto)
- Widget size presets (mini/compact/full)

### v2.4.0 (Future)
- Multiple location tracking
- Severe weather alerts
- Moon phases display

### v3.0.0 (Long-term)
- macOS support
- Linux support
- Mobile app

---

## 🎊 What Makes v2.2.0 Special?

### 1. **Complete Freedom**
Choose ANY combination:
- Fahrenheit + Metric wind + 12-hour? ✅
- Celsius + Imperial pressure + 24-hour? ✅
- YOUR preferences matter!

### 2. **International-First**
- Not forced to one standard
- Respects regional preferences
- Flexible for all users

### 3. **Professional UX**
- Instant feedback (toast notifications)
- Persistent settings (saved to Registry)
- No hidden options
- Intuitive interface

### 4. **Smart Integration**
- Battery auto-detects hardware
- API handles conversions
- Seamless experience

---

## 🙏 Credits

### Data Providers (Free!)
- **Weather:** [Open-Meteo](https://open-meteo.com)
- **Geocoding:** [Nominatim](https://nominatim.openstreetmap.org/)
- **IP Location:** [ip-api.com](https://ip-api.com)

### Technologies
- **Framework:** PyQt5
- **Location:** geocoder
- **Battery:** psutil
- **Icons:** Unicode emoji

---

## 📞 Support

- 🐛 **Bugs:** [GitHub Issues](https://github.com/malkosvetnik/desktop-weather-widget/issues)
- 💡 **Features:** [GitHub Discussions](https://github.com/malkosvetnik/desktop-weather-widget/discussions)
- ⭐ **Star if useful!**

---

## 🌟 All Features (v2.2.0)

- ✅ **NEW:** Celsius/Fahrenheit temperature units
- ✅ **NEW:** 12-hour/24-hour time format
- ✅ **NEW:** Metric/Imperial measurement system
- ✅ **NEW:** Battery status (laptops)
- ✅ 15-minute precipitation nowcast
- ✅ Windows Location API (GPS/Wi-Fi)
- ✅ Dual location system (API/Windows)
- ✅ Bilingual (Serbian/English)
- ✅ 5-day forecast
- ✅ Air Quality Index (AQI)
- ✅ UV Index
- ✅ System tray integration
- ✅ Sleep mode recovery
- ✅ Click-through mode
- ✅ Auto-start with Windows

---

**Made with ❤️ by [malkosvetnik](https://github.com/malkosvetnik)**

*Get weather YOUR way - YOUR units, YOUR format, YOUR language!* 🎨

---

*Version 2.2.0 released on January 11, 2026*

**If you find this useful, please ⭐ star the repository!**
