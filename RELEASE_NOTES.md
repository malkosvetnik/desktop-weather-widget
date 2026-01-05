# 🌤️ Desktop Weather Widget v2.1.0

## What's New

### 🌐 Full English Language Support! (NEW!)

Switch between Serbian (Latin) and English via the tray menu!

**Serbian:**
- 🌧️ Kiša SADA!
- ❄️ Sneg za 2h
- ☀️ Nema padavina

**English:**
- 🌧️ Rain NOW!
- ❄️ Snow in 2h
- ☀️ No precipitation

### 🎯 Major Fix: Real-Time Precipitation Detection

### 🔧 Improved Time Calculations

**Before:**
- 1h 56min away → "Rain in 1h" (wrong!) ❌

**After:**  
- 1h 56min away → "Rain in 2h" (correct!) ✅

### 🌐 Better Translations

All error messages and tooltips now properly translate between Serbian and English.

---

## 📥 Installation

1. Download `weather_widget_ABSOLUTE_FINAL.pyw`
2. Install dependencies:
   ```bash
   pip install PyQt5 requests
   ```
3. Run:
   ```bash
   python weather_widget_ABSOLUTE_FINAL.pyw
   ```

**Or download the compiled `.exe` (no Python required!)**

---

## 🎨 Features

✅ Current weather with live updates  
✅ 5-day forecast  
✅ Hourly forecast (12h) with tooltip  
✅ **Real-time precipitation alerts** (NEW!)  
✅ UV Index & Air Quality monitoring  
✅ Sunrise/Sunset times  
✅ Sleep mode detection & recovery  
✅ Click-through mode  
✅ Position locking  
✅ Auto-location or manual city selection  
✅ Serbian & English language support  
✅ Customizable refresh intervals  
✅ System tray integration  

---

## 🐛 Bug Fixes in v2.0.0

- Fixed precipitation timing calculation (now uses `round()` instead of `int()`)
- Fixed "Error" message not translating properly
- Fixed tooltip text hardcoded in English
- Fixed API not requesting rain/precipitation data
- Fixed widget ignoring current weather when checking for rain

---

## 📸 Screenshots

See `screenshots/` folder for examples of the widget in action!

---

## 🙏 Credits

Weather data provided by [Open-Meteo API](https://open-meteo.com)  
Air quality data provided by [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)

