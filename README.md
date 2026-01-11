# 🌤️ Desktop Weather Widget (Windows)

A lightweight, accurate, and customizable **desktop weather widget for Windows**.  
Designed for users who want **precise forecasts, full control, and privacy** — without heavy frameworks like Rainmeter.

![Main Widget](screenshots/main_widget_serbian.png)

---

## 📥 Download (Windows EXE)

👉 **[Download Windows EXE (ZIP – ~39 MB)](https://drive.google.com/file/d/1vexOriXVtBnVKlCsZ3aeeIHiNb0HAnIz/view?usp=drive_link)**

- Ready-to-run **`.exe` included**
- **No Python installation required**
- Just extract and double-click

> ℹ️ GitHub release assets are size-limited, so the EXE is currently hosted on Google Drive.

---

## ✨ What’s New (v2.2.0)

- **12-hour (AM/PM) and 24-hour time format**
- **Celsius / Fahrenheit temperature units**
- **Optional battery percentage** (laptops only)
- Improved **15-minute precipitation nowcasting**
- Better error handling and auto-recovery
- Full **Serbian / English** interface

> Several features were added directly based on user feedback.

---

## 🌦️ Key Features

- **15-minute nowcast** for short-term rain & snow
- Real-time precipitation alerts
- Dual location system:
  - IP-based (works everywhere)
  - Windows Location API (GPS / Wi-Fi, when enabled)
- Temperature, feels-like, wind, pressure, humidity
- UV index and detailed **Air Quality (PM2.5, PM10, O₃, NO₂, SO₂, CO)**
- Desktop-first UX with tray integration
- Auto-start with Windows
- Click-through & position lock modes

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

```bash
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget
pip install PyQt5 requests geocoder psutil
python weather_widget_final.pyw
