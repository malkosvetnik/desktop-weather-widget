# 🌤️ Desktop Weather Widget (Windows)

A lightweight, accurate, and customizable **desktop weather widget for Windows**.  
Built for users who want **precise short-term forecasts, reliability, and low system overhead** — without heavy frameworks like Rainmeter.

![Widget Preview](screenshots/main_widget_serbian.png)

[![Latest Release](https://img.shields.io/github/v/release/malkosvetnik/desktop-weather-widget?label=latest%20version)](https://github.com/malkosvetnik/desktop-weather-widget/releases)
[![Stars](https://img.shields.io/github/stars/malkosvetnik/desktop-weather-widget?style=social)](https://github.com/malkosvetnik/desktop-weather-widget/stargazers)
[![License](https://img.shields.io/github/license/malkosvetnik/desktop-weather-widget)](LICENSE)

---

## 📥 Download (Windows EXE)

👉 **[Download Windows EXE (ZIP – ~39 MB)](https://drive.google.com/file/d/1a-xjq2drBX9gmTIofVrEzDJ02tPTAQTX/view?usp=drive_link)**

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

---

## 🌦️ Key Features

- **15-minute nowcast** for short-term rain and snow
- Real-time precipitation alerts
- Dual location system (IP + Windows Location API)
- Comprehensive weather & air quality data
- Desktop-first UX with tray integration and auto-start

---

## 📸 Screenshots

![Serbian UI](screenshots/main_widget_serbian.png)  
![English UI](screenshots/main_widget_english.png)

---

## 🚀 Run from Source (Optional)

```bash
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget
pip install PyQt5 requests geocoder psutil
python weather_widget_final.pyw
