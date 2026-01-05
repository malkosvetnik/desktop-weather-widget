# 🌤️ Weather Widget v2.1.0

## 🌐 New Feature: Full English Language Support!

The widget now speaks both Serbian and English! Switch languages via tray menu.

### 📥 Download

**Complete Package (ZIP):**
[Download Weather Widget v2.1.0.zip](https://drive.google.com/file/d/1eWuVGHb4fkctejAOMBK0h0mhyV26XHjo/view?usp=drive_link)

**What's included:**
- `weather_widget.pyw` - Main widget file
- `requirements.txt` - Python dependencies
- Complete documentation
- All screenshots

**Installation:**
```bash
# Extract ZIP, then:
pip install PyQt5 requests
python weather_widget.pyw
```

---

## ✨ What's New in v2.1.0

✅ **Full English translation** - All UI, menus, tooltips, and error messages  
✅ **Real-time precipitation alerts** - Shows "Rain NOW!" when it's actively raining  
✅ **Accurate time calculations** - Fixed rounding (1h 56min → "Rain in 2h", was "1h")  
✅ **Proper translations** - All text now translates correctly between Serbian/English  
✅ **Better API data** - Now requests rain/precipitation values from API  

---

## 🌐 Language Support

Switch between languages via tray menu!

**Serbian (Srpski):**
- 🌧️ Kiša SADA!
- ❄️ Sneg za 2h
- ☀️ Nema padavina
- ⚠️ Greška

**English:**
- 🌧️ Rain NOW!
- ❄️ Snow in 2h
- ☀️ No precipitation
- ⚠️ Error

---

## 📸 Screenshots

### Widget in English (NEW!)
![English Widget](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/screenshots/main_widget_english.png?raw=true)
*New English translation with "Rain NOW!" feature*

### Widget in Serbian
![Serbian Widget](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/screenshots/main_widget.png?raw=true)

---

<details>
<summary>📸 More Screenshots (Click to expand)</summary>

### Precipitation Alert - Rain NOW!
![Rain NOW Closeup](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/screenshots/rain_now_closeup.png?raw=true)
*Real-time precipitation detection showing "Rain NOW!"*

### Hourly Forecast Tooltip
![Hourly Forecast](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/screenshots/hourly_forecast_tooltip.png?raw=true)
*12-hour forecast with temperature, weather conditions, and rain probability*

### Language Selection Menu
![Language Menu](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/screenshots/language_menu.png?raw=true)
*Easy language switching via tray menu*

### Weather Alert Tooltip
![Alert Tooltip](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/screenshots/alert_tooltip.png?raw=true)
*Detailed weather warnings and temperature alerts*

### Air Quality Details
![Pollution Tooltip](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/screenshots/pollution_tooltip.png?raw=true)
*Detailed pollutant breakdown: CO, NO₂, O₃, SO₂, PM2.5, PM10, NH₃*

### System Tray Menu
![Tray Menu](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/screenshots/tray_menu.png?raw=true)
*Complete settings and control menu*

</details>

---

## 🐛 Bug Fixes in v2.1.0

### Major Fixes:
- **Fixed precipitation timing calculation** - Changed from `int()` to `round()` for proper rounding
  - Example: 1h 56min now correctly shows "Rain in 2h" (previously showed "1h")
- **Fixed current weather check** - Now detects if it's raining NOW before checking future rain
- **Fixed "Error" messages** - All error messages now properly translate between Serbian/English
- **Fixed tooltip text translation** - "Hover na ikonicu za detalje" now translates to "Hover on icon for details"
- **Fixed API data requests** - Added `rain`, `precipitation`, and `showers` parameters to API calls

### Technical Improvements:
- Improved precipitation detection logic (checks both weather_code AND actual rain values)
- Better error handling with translated messages
- Enhanced debug logging (invisible in normal use)
- Sleep mode recovery maintained

---

## 🎨 Features

### Weather Information:
- 🌡️ Current temperature and "feels like"
- 🌧️ Real-time precipitation alerts
- 💨 Wind speed and direction
- 💧 Humidity percentage
- ☁️ Cloud cover
- 👁️ Visibility distance
- 🌡️ Atmospheric pressure

### Additional Data:
- ☀️ UV Index with color-coded severity
- 🏭 Air Quality Index (AQI) with pollutant details
- 📅 5-Day Forecast
- ⏰ 12-Hour Hourly Forecast (tooltip)
- 🌅 Sunrise & Sunset times

### Customization:
- 🌐 Bilingual: Serbian (Latin) and English
- 📍 Auto-location or manual city selection
- ⏱️ Adjustable refresh: 5, 10, 15, 30, or 60 minutes
- 🖥️ Resolution presets (XGA to 8K UHD)
- 👻 Click-through mode
- 🔒 Position locking
- 🚀 Startup with Windows (optional)

### Advanced:
- 😴 Sleep mode detection & auto-refresh
- 🔄 Network retry logic (3 attempts)
- 💾 Persistent settings
- 🎨 System tray integration

---

## 🔧 Requirements

- **Operating System:** Windows 10/11
- **Python:** 3.8 or higher
- **Libraries:** PyQt5, requests

## 📦 Installation

1. Download the ZIP file from the link above
2. Extract to your desired location
3. Open terminal/command prompt in extracted folder
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the widget:
   ```bash
   python weather_widget.pyw
   ```

---

## 📋 Full Changelog

See [CHANGELOG.md](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/CHANGELOG.md) for complete list of all changes.

---

## 🙏 Credits

- **Weather data:** [Open-Meteo API](https://open-meteo.com) (free, no API key required)
- **Air quality data:** [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)
- **Framework:** PyQt5
- **Icons:** Unicode emoji

---

## 🐛 Found a Bug?

Please report issues at: https://github.com/malkosvetnik/desktop-weather-widget/issues

---

## 🌟 Support the Project

If you find this widget useful, please ⭐ star the repository!

---

**Made with ❤️ by malkosvetnik**
