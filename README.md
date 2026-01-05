# 🌤️ Desktop Weather Widget

A beautiful, feature-rich desktop weather widget for Windows with real-time weather updates, precipitation alerts, and bilingual support (Serbian/English).

![Weather Widget Screenshot](screenshots/main_widget.png)

## ✨ Features

### 🌡️ Current Weather
- Real-time temperature and "feels like" temperature
- Weather description with emoji icons
- Humidity, wind speed & direction
- Atmospheric pressure
- Cloud cover percentage
- Visibility distance

### 🌧️ Precipitation Alerts (NEW in v2.0!)
- **Real-time detection**: Shows "Rain NOW!" when it's actively raining
- **Smart forecasting**: Accurate timing for upcoming rain, snow, or storms
- **Intelligent rounding**: 1h 56min shows as "2h" (not "1h")
- Supports rain, snow, and thunderstorms

### 📊 Additional Information
- **UV Index** with color-coded severity
- **Air Quality Index (AQI)** with detailed pollutant breakdown tooltip
- **5-Day Forecast** with min/max temperatures
- **Hourly Forecast** (12h) - click on "SATNA PROGNOZA" box to see detailed tooltip
- **Sunrise & Sunset** times

### 🎨 Customization
- **Bilingual**: Serbian (Latin) and English
- **Auto-location** or manual city selection
- **Adjustable refresh intervals**: 5, 10, 15, 30, or 60 minutes
- **Resolution presets**: From XGA (1024x768) to 8K UHD
- **Click-through mode**: Widget becomes transparent to clicks
- **Position locking**: Prevent accidental movement
- **System tray integration**: Minimize to tray

### 🛌 Advanced Features
- **Sleep mode detection**: Automatically refreshes after system wake
- **Network retry logic**: 3 attempts with 15s delays
- **Startup with Windows**: Optional auto-start
- **Persistent settings**: Remembers your preferences

---

## 📥 Installation

### Option 1: Run from Source
1. Install Python 3.8+ and dependencies:
   ```bash
   pip install PyQt5 requests
   ```

2. Download `weather_widget_ABSOLUTE_FINAL.pyw`

3. Get your **free** OpenWeatherMap API key:
   - Visit https://openweathermap.org/api
   - Sign up for a free account
   - Copy your API key

4. Run the widget:
   ```bash
   python weather_widget_ABSOLUTE_FINAL.pyw
   ```

5. On first run, paste your API key when prompted

### Option 2: Download Compiled .exe (Coming Soon!)
No Python installation required - just download and run!

---

## 🎮 Usage

### Basic Controls
- **Drag widget**: Click and drag anywhere to move (when unlocked)
- **🔒 Lock button**: Lock/unlock position
- **📍 Auto button**: Toggle automatic location detection
- **Search box**: Manually enter city name
- **✕ Close**: Hide widget (still runs in tray)

### Tray Menu
Right-click the tray icon for:
- Show/Hide widget
- Enable/disable startup with Windows
- Widget-only mode (no tray icon)
- Click-through mode
- Resolution presets
- Refresh weather
- Change API key
- Exit application

### Tooltips
- **Hover over Air Quality (Zagađenje)**: See detailed pollutant breakdown
- **Click on SATNA PROGNOZA box**: View 12-hour forecast table

---

## 🐛 Bug Fixes in v2.0.0

### Major Fixes
1. **Real-time precipitation detection**
   - Fixed: Widget now correctly shows "Rain NOW!" when it's actively raining
   - Previously showed future rain even during active precipitation

2. **Time calculation accuracy**
   - Fixed: Changed from `int()` to `round()` for proper rounding
   - Example: 1h 56min now correctly shows "Rain in 2h" (was "1h")

3. **Translation issues**
   - Fixed: Error messages now properly translate (Serbian/English)
   - Fixed: Tooltip text "Hover na ikonicu za detalje" now translates

4. **API data completeness**
   - Fixed: Added `rain`, `precipitation`, `showers` to API requests
   - Fixed: Now validates both weather_code AND actual rain values

### Technical Improvements
- Checks current weather BEFORE searching for future precipitation
- Better error handling with translated messages
- Comprehensive debug logging (invisible in .exe)

---

## 📸 Screenshots

### Main Widget
![Main View](screenshots/main_widget.png)

### Precipitation Alert - Rain NOW
![Rain Alert](screenshots/rain_now.png)

### Hourly Forecast Tooltip
![Tooltip](screenshots/hourly_tooltip.png)

### Air Quality Tooltip
![Air Quality](screenshots/pollution_tooltip.png)

### Tray Menu
![Tray Menu](screenshots/tray_menu.png)

---

## 🔧 Requirements

- **Python**: 3.8 or higher
- **PyQt5**: 5.15+
- **requests**: 2.25+
- **OpenWeatherMap API key** (free)

---

## 📝 Configuration

Settings are automatically saved in Windows Registry under:
```
HKEY_CURRENT_USER\Software\WeatherWidget\Settings
```

Stored settings:
- Window position
- Lock status
- Click-through mode
- Language preference
- Refresh interval
- API key
- Resolution preset

---

## 🌐 API Information

This widget uses:
- **Open-Meteo Weather API** (free, no key required)
  - Current weather, forecasts, UV index
  - https://open-meteo.com

- **Open-Meteo Air Quality API** (free)
  - AQI and pollutant data
  - https://open-meteo.com/en/docs/air-quality-api

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget
pip install -r requirements.txt
python weather_widget_ABSOLUTE_FINAL.pyw
```

---

## 📜 License

This project is open source and available under the MIT License.

---

## 🙏 Credits

- Weather data: [Open-Meteo](https://open-meteo.com)
- Icons: Unicode emoji
- Framework: PyQt5

---

## 📞 Support

Found a bug or have a suggestion?
- Open an issue: https://github.com/malkosvetnik/desktop-weather-widget/issues
- Check existing issues first!

---

## 🗺️ Roadmap

Future improvements:
- [ ] More language options
- [ ] Customizable themes
- [ ] Weather alerts from national services
- [ ] Radar map integration
- [ ] Multiple location tracking

---

**Made with ❤️ by malkosvetnik**
