# 🌤️ Desktop Weather Widget

**A beautiful, customizable desktop weather widget for Windows - better than Microsoft's built-in weather app!**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

---

## ✨ Features

### 📊 Comprehensive Weather Data
- 🌡️ **Current Temperature** with "feels like"
- 💧 **Humidity** percentage
- 💨 **Wind Speed & Direction** (8-point compass)
- ☀️ **UV Index** with color coding
- 🌫️ **Air Quality Index** (AQI) with detailed pollutants
- 📊 **Atmospheric Pressure** (mbar)
- 👁️ **Visibility** (km)
- ☁️ **Cloud Coverage** (%)
- 🌅 **Sunrise & Sunset** times
- 📅 **5-Day Forecast** with min/max temperatures

### 🧪 Detailed Air Quality
Hover over "Zagađenje" to see 7 pollutants:
- CO (Carbon Monoxide)
- NO₂ (Nitrogen Dioxide)
- O₃ (Ozone)
- SO₂ (Sulfur Dioxide)
- PM2.5 (Fine Particles)
- PM10 (Coarse Particles)
- NH₃ (Ammonia)

### 🎨 Customization
- 📐 **Resolution Scaling** - Perfect size from XGA (1024x768) to 8K (7680x4320)
- 🌍 **Auto-Location** or manual city selection
- ⏱️ **Refresh Intervals** - 5, 10, 15, 30, or 60 minutes
- 🔒 **Lock Position** - Prevent accidental dragging
- 👻 **Click-Through Mode** - Use as desktop wallpaper
- 🚀 **Startup Option** - Launch with Windows

### 🇷🇸 Serbian Language
- Full Serbian (Latin) interface
- Localized weather descriptions
- Serbian day/month names

### ⚡ Performance
- **Lightweight**: Only 60-80 MB RAM
- **Efficient**: 0.0-0.1% CPU when idle
- **Gaming-Friendly**: Zero impact on game performance

---

## 📸 Screenshots

> **Note**: Add your screenshots here

---

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.8+ (or use pre-built EXE)
- Free OpenWeatherMap API key

### Option 1: Pre-built EXE (Recommended)
1. Download the latest release from [Releases](../../releases)
2. Extract `Weather Widget.exe`
3. Run the application
4. Enter your OpenWeatherMap API key when prompted

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/desktop-weather-widget.git
cd desktop-weather-widget

# Install dependencies
pip install -r requirements.txt

# Run the widget
python weather_widget_final.py
```

---

## 🔑 Getting an API Key

1. Visit [OpenWeatherMap API](https://openweathermap.org/api)
2. Click "Sign Up" and create a free account
3. Navigate to "API Keys" section
4. Copy your API key
5. Paste it when the widget asks for it on first run

**Note**: API activation may take 10-15 minutes.

---

## 📦 Building EXE

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller pillow

# Create icon (optional)
python create_icon.py

# Build EXE
build_exe.bat
```

The EXE will be in `dist/Weather Widget.exe`

---

## 🎮 Usage

### Tray Menu Options
- **Prikaži Widget** - Show/hide the widget
- **Pokreni sa Windows-om** - Auto-start with Windows
- **Click-Through Mode** - Make widget transparent to clicks
- **Rezolucija Monitora** - Adjust size for your display
- **Osveži Vreme** - Manually refresh weather data
- **Promeni API Key** - Update your API key
- **Izađi** - Close the application

### Widget Controls
- **🔍 Search** - Enter city name and search
- **📍 Auto** - Use automatic location detection
- **Osvežavanje** - Change refresh interval (5-60 min)
- **🔓/🔒** - Lock/unlock widget position
- **✕** - Hide widget (access from tray)

---

## 🛠️ Configuration

Settings are automatically saved in Windows Registry:
- Widget position
- Selected resolution
- Auto-location preference
- Refresh interval
- Lock status
- API key (encrypted)

---

## 🌍 Supported Resolutions

| Resolution | Dimensions | Use Case |
|------------|------------|----------|
| XGA (1024x768) | 273x585px | Old CRT monitors |
| WXGA (1280x800) | 315x675px | Old laptops |
| HD Ready (1366x768) | 336x720px | Budget displays |
| **Full HD (1920x1080)** | **420x900px** | **Most common** ✅ |
| QHD (2560x1440) | 559x1197px | 1440p displays |
| 4K UHD (3840x2160) | 840x1800px | 4K monitors |
| 5K (5120x2880) | 1121x2403px | 5K displays |
| 8K UHD (7680x4320) | 1260x2700px | 8K monitors |

**Physical size remains consistent across all resolutions!**

---

## 🐛 Troubleshooting

### Widget doesn't show weather
- Check your internet connection
- Verify your API key is correct
- Wait 10-15 minutes after creating new API key
- Try "Osveži Vreme" from tray menu

### Widget is too small/large
- Right-click tray icon → "Rezolucija Monitora"
- Select your monitor's native resolution

### Widget disappears after restart
- Enable "Pokreni sa Windows-om" in tray menu
- Check Windows Startup folder

### API errors (401)
- Your API key is invalid
- Right-click tray → "Promeni API Key"
- Get a new key from OpenWeatherMap

---

## 📋 Requirements

### Runtime (EXE)
- Windows 10/11
- Internet connection
- OpenWeatherMap API key (free)

### Development
```txt
Python 3.8+
PyQt5==5.15.9
requests==2.31.0
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Ideas for Contributions
- [ ] Translations to other languages
- [ ] Additional weather providers (WeatherStack, OpenMeteo)
- [ ] Custom themes/color schemes
- [ ] Moon phases
- [ ] Weather alerts/warnings
- [ ] Hourly forecast
- [ ] Historical data graphs

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

- **Weather Data**: [OpenWeatherMap API](https://openweathermap.org/)
- **UI Framework**: [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- **Icons**: Emoji (built-in)
- **Location**: [IP-API](https://ip-api.com/)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

## 📞 Support

- 🐛 **Bug Reports**: [Issues](../../issues)
- 💡 **Feature Requests**: [Issues](../../issues)
- 📧 **Contact**: [Your Email]

---

## 🔄 Changelog

### v1.0.0 (Initial Release)
- ✅ 11 weather parameters
- ✅ 5-day forecast
- ✅ Air quality with 7 pollutants
- ✅ Resolution scaling (XGA to 8K)
- ✅ Serbian language support
- ✅ Auto/manual location
- ✅ Click-through mode
- ✅ Windows startup option
- ✅ Lightweight & efficient

---

**Made with ❤️ for the open-source community**
