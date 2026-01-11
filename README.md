# 🌤️ Desktop Weather Widget (Windows)

A lightweight, accurate, and customizable **desktop weather widget for Windows**.  
Built for users who want **precise short-term forecasts, reliability, and low system overhead** — without heavy frameworks like Rainmeter.

![Widget Preview](screenshots/main_widget_serbian.png)

[![Latest Release](https://img.shields.io/github/v/release/malkosvetnik/desktop-weather-widget?label=latest%20version)](https://github.com/malkosvetnik/desktop-weather-widget/releases)
[![Stars](https://img.shields.io/github/stars/malkosvetnik/desktop-weather-widget?style=social)](https://github.com/malkosvetnik/desktop-weather-widget/stargazers)
[![License](https://img.shields.io/github/license/malkosvetnik/desktop-weather-widget)](LICENSE)

---

## 📥 Download (Windows EXE)

👉 **[Download Windows EXE (ZIP – ~39 MB)](https://drive.google.com/file/d/1vexOriXVtBnVKlCsZ3aeeIHiNb0HAnIz/view?usp=drive_link)**

- ✅ Ready-to-run **`.exe` included**
- ❌ **No Python installation required**
- 📦 Just extract and double-click

> ℹ️ GitHub release assets are size-limited, so the compiled EXE is currently hosted on Google Drive.

---

## ✨ What’s New (v2.2.0)

- **12-hour (AM/PM) and 24-hour time format**
- **Celsius / Fahrenheit temperature units**
- **Optional battery percentage** (laptops only)
- Improved **15-minute precipitation nowcasting**
- Better error handling and automatic recovery
- More robust connection health checks
- Full **Serbian (Latin) / English** interface

> Several features were added directly based on user feedback.

---

## 🌦️ Key Features

### ⏱️ High-Precision Weather
- **15-minute nowcast** for short-term rain and snow
- Real-time alerts (e.g. *“Rain in 15 min (70%)”*)
- Powered by **Open-Meteo** (free, no API key)

### 📍 Dual Location System
- **IP-based geolocation** (works everywhere)
- **Windows Location API** (GPS / Wi-Fi, when enabled)
- Automatic fallback and easy switching

### 📊 Comprehensive Data
- Temperature and “feels like”
- Wind speed & direction
- Pressure, humidity, visibility
- UV index (color-coded)
- **Air Quality Index** (PM2.5, PM10, O₃, NO₂, SO₂, CO)

### 🖥️ Desktop-First Experience
- Always-on-top desktop widget
- Tray integration
- Auto-start with Windows
- Click-through & position lock
- Sleep / wake auto-recovery

---

## 🌍 Language Support

- 🇷🇸 **Serbian (Latin)** — fully translated
- 🇬🇧 **English**

All menus, tooltips, alerts, and messages are localized.

---

## 📸 Screenshots

![Serbian UI](screenshots/main_widget_serbian.png)  
![English UI](screenshots/main_widget_english.png)

---

## 🚀 Run from Source (Optional)

For developers who prefer running from source:

```bash
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget
pip install PyQt5 requests geocoder psutil
python weather_widget_final.pyw
