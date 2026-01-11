# Changelog

All notable changes to the Desktop Weather Widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v2.2.0] - 2026-01-11

### 🎨 CUSTOMIZATION UPDATE - Major Feature Release

#### ✨ New Features

##### Temperature Unit System
- **Celsius/Fahrenheit selection**: Full temperature unit customization via tray menu
- **Instant conversion**: All temperature displays convert in real-time
  - Main temperature display
  - "Feels like" temperature
  - 5-day forecast (min/max temps)
  - Hourly forecast tooltip
  - Tray icon tooltip
- **Persistent storage**: Temperature preference saved in Windows Registry
- **API integration**: Direct Celsius/Fahrenheit parameter support from Open-Meteo
- **Bilingual labels**: "Celsius (°C)" / "Fahrenheit (°F)" in both languages

##### Time Format System
- **12-hour/24-hour selection**: User choice for time display format
- **Comprehensive updates**: Affects all time displays:
  - Main clock (with seconds)
  - Sunrise/Sunset times
  - Hourly forecast times
  - "Last updated" timestamp
  - Weather alert timestamps
- **Dynamic AM/PM**: Proper AM/PM display in 12-hour mode
- **Format examples**: 
  - 24-hour: `17:30:45`
  - 12-hour: `05:30:45 PM`

##### Measurement Unit System (Metric/Imperial)
- **Wind speed units**: km/h ↔ mph
  - API parameter integration (`wind_speed_unit=mph`)
  - Direct API conversion (no manual calculation)
- **Pressure units**: mbar ↔ inHg
  - Conversion: `mbar × 0.02953 = inHg`
  - Example: 1003 mbar = 29.62 inHg
- **Visibility units**: km ↔ mi  
  - API provides different values per unit system
  - No manual conversion needed
- **Consistent display**: All units update simultaneously

##### Battery Status (Laptop Support)
- **Real-time battery monitoring**: Shows percentage and charging status
- **Smart detection**: Automatically detects laptop vs desktop
  - Desktop: Battery label hidden (no battery present)
  - Laptop: Battery displayed next to clock
- **Visual indicators**:
  - 🔌 Green: Charging (any %)
  - 🔋 White: 30%+ (normal operation)
  - 🔋 Orange: 15-29% (low battery warning)
  - 🪫 Red: <15% (critical battery)
- **Update frequency**: Refreshes every 30 seconds
- **Position**: Displayed beside main clock without increasing widget height
- **Library**: Uses `psutil.sensors_battery()` for cross-platform compatibility

#### 🛠️ Bug Fixes

##### Visibility Data Handling
- **Fixed API inconsistency**: Open-Meteo returns different visibility values for metric vs imperial
  - Metric mode: ~28 km
  - Imperial mode: ~92 mi (API internal conversion)
- **Removed double conversion**: No longer manually converting km → mi
- **Solution**: Display API-provided values directly with correct unit symbol
- **Result**: Accurate visibility readings in both unit systems

##### Menu Translation System
- **Fixed untranslated menu titles**: Temperature, Time, Units menus now translate
- **Dynamic updates**: Menu titles change with language selection
- **Implementation**: 
  ```python
  self.temp_unit_menu.setTitle(f"🌡️ {self.t('temperature_unit')}")
  self.time_format_menu.setTitle(f"🕐 {self.t('time_format')}")
  self.unit_system_menu.setTitle(f"📏 {self.t('unit_system')}")
  ```
- **Menu option translation**: All submenu items now properly localized:
  - English: "24-hour (17:30)", "12-hour (05:30 PM)"
  - Serbian: "24-satni (17:30)", "12-satni (05:30 PM)"

##### Clock Display
- **Fixed visual artifacts**: Removed border/frame around clock when battery hidden
- **Solution**: Wrapper QWidget with transparent background
- **Result**: Clean, seamless clock display on desktop PCs

#### 🔧 Technical Improvements

##### API Parameter Integration
```python
# Temperature unit
temp_unit_param = "fahrenheit" if unit == 'fahrenheit' else "celsius"
weather_url += f"&temperature_unit={temp_unit_param}"

# Wind speed unit
wind_unit_param = "mph" if unit == 'imperial' else "kmh"
weather_url += f"&wind_speed_unit={wind_unit_param}"

# Precipitation unit (future-proofing)
precip_unit_param = "inch" if unit == 'imperial' else "mm"
weather_url += f"&precipitation_unit={precip_unit_param}"
```

##### Helper Functions
```python
# Temperature
def celsius_to_fahrenheit(celsius): return (celsius * 9/5) + 32
def get_temp_symbol(): return "°F" if unit == 'fahrenheit' else "°C"

# Time
def format_time(time_obj): 
    return time_obj.strftime('%I:%M %p') if format == '12h' else time_obj.strftime('%H:%M')

# Units
def get_wind_symbol(): return "mph" if system == 'imperial' else "km/h"
def format_pressure(pressure_mbar):
    if system == 'imperial': return f"{pressure_mbar * 0.02953:.2f} inHg"
    else: return f"{pressure_mbar} mbar"
def format_visibility(visibility_km):
    # API handles conversion internally, just change symbol
    return f"{visibility_km:.1f} mi" if system == 'imperial' else f"{visibility_km:.1f} km"
```

##### Settings Persistence
```python
# Save to Windows Registry
settings.setValue('temperature_unit', 'celsius' | 'fahrenheit')
settings.setValue('time_format', '12h' | '24h')
settings.setValue('unit_system', 'metric' | 'imperial')

# Load on startup
self.temperature_unit = settings.value('temperature_unit', 'celsius', type=str)
self.time_format = settings.value('time_format', '24h', type=str)
self.unit_system = settings.value('unit_system', 'metric', type=str)
```

##### Battery Detection
```python
import psutil

def updateBatteryStatus():
    if not PSUTIL_AVAILABLE: return
    
    battery = psutil.sensors_battery()
    if battery is None:
        # Desktop PC - hide battery label
        self.battery_label.hide()
        return
    
    # Laptop - show battery status
    percent = int(battery.percent)
    is_charging = battery.power_plugged
    icon = "🔌" if is_charging else ("🔋" if percent >= 15 else "🪫")
    color = "#4CAF50" if is_charging else ("#FFC107" if percent < 15 else "white")
    
    self.battery_label.setText(f"{icon} {percent}%")
    self.battery_label.setStyleSheet(f"color: {color};")
    self.battery_label.show()
```

##### Translation System Enhancement
```python
# updateLanguageUI() now includes:
if self.current_language == "sr":
    self.time_format_actions["24h"].setText("24-satni (17:30)")
    self.time_format_actions["12h"].setText("12-satni (05:30 PM)")
    self.unit_system_actions["metric"].setText("Metrički (km/h, mbar)")
    self.unit_system_actions["imperial"].setText("Imperijalni (mph, inHg)")
else:
    self.time_format_actions["24h"].setText("24-hour (17:30)")
    self.time_format_actions["12h"].setText("12-hour (05:30 PM)")
    self.unit_system_actions["metric"].setText("Metric (km/h, mbar)")
    self.unit_system_actions["imperial"].setText("Imperial (mph, inHg)")
```

#### 📊 Conversion Accuracy

| Parameter | Metric | Imperial | Formula | Example |
|-----------|--------|----------|---------|---------|
| **Temperature** | -4.0°C | 24.8°F | `(C × 9/5) + 32` | -4 × 9/5 + 32 = 24.8 ✅ |
| **Wind Speed** | 38.2 km/h | 23.8 mph | API direct | 38.2 ÷ 1.609 = 23.7 ✅ |
| **Pressure** | 1003 mbar | 29.62 inHg | `mbar × 0.02953` | 1003 × 0.02953 = 29.62 ✅ |
| **Visibility** | 28.0 km | 91.7 mi | API direct | API provides different values ✅ |

#### 🎯 User Experience Enhancements

##### Instant Feedback
- **Notification on change**: Toast notification shows new setting
  - "Temperature Unit Changed: Celsius (°C)"
  - "Time Format Changed: 12-hour (AM/PM)"
  - "Unit System Changed: Metric (km/h, mbar)"
- **Visual confirmation**: Checkmark updates in menu
- **No restart required**: All changes apply immediately

##### Menu Organization
```
Tray Menu Structure (v2.2.0):
├── Show Widget
├── ✓ Run at Windows Startup
├── Widget Only (no tray)
├── Click-Through Mode
├── 🖥️ Monitor Resolution
│   ├── XGA (1024x768)
│   ├── Full HD (1920x1080)
│   └── 4K UHD (3840x2160)
├── 🌐 Jezik / Language
│   ├── 🇷🇸 Srpski
│   └── 🇬🇧 English
├── 🌡️ Temperature Unit ← NEW!
│   ├── Celsius (°C)
│   └── Fahrenheit (°F)
├── 🕐 Time Format ← NEW!
│   ├── 24-hour (17:30)
│   └── 12-hour (05:30 PM)
├── 📏 Measurement Units ← NEW!
│   ├── Metric (km/h, mbar)
│   └── Imperial (mph, inHg)
├── 📍 Location Source
│   ├── API Location (IP)
│   └── Windows Location (GPS/Wi-Fi)
├── Refresh Weather
└── Exit
```

##### Consistent Experience
- **All temperature displays**: Main temp, feels like, forecast, tooltip
- **All time displays**: Clock, sunrise/sunset, hourly, last updated
- **All unit displays**: Wind, pressure, visibility
- **Persistent across restarts**: Settings loaded from Registry

#### 🆕 Dependencies

##### New Requirement: psutil
```bash
pip install psutil
```
- **Purpose**: Battery status detection
- **Platform**: Cross-platform (Windows/macOS/Linux)
- **Size**: ~500 KB
- **License**: BSD-3-Clause (permissive)

##### Updated requirements.txt
```
PyQt5>=5.15.0
requests>=2.25.0
geocoder>=1.38.1
psutil>=5.8.0  # NEW!
```

#### ⚠️ Known Limitations

##### Battery Status
- **Desktop PCs**: No battery → Label hidden (expected behavior)
- **Laptops**: Battery displayed → Percentage and status shown
- **First read**: May take 1-2 seconds to appear on startup
- **Update frequency**: 30 seconds (configurable)

##### Visibility Data
- **API Quirk**: Open-Meteo returns different raw values for metric vs imperial
  - Not a bug - API internal behavior
  - Widget displays whatever API returns
  - Values are accurate for selected unit system

##### Time Format
- **System locale independence**: Widget uses its own time format setting
  - Not affected by Windows locale
  - User has full control
  - May differ from system tray clock

#### 💡 Use Cases

**Scenario 1: International User**
```
User from USA:
1. Selects Fahrenheit (familiar with °F)
2. Selects Imperial units (mph, inHg)
3. Selects 12-hour time (5:30 PM)
Result: Complete American-style weather display ✅
```

**Scenario 2: European User**
```
User from Serbia:
1. Selects Celsius (metric system)
2. Selects Metric units (km/h, mbar)
3. Selects 24-hour time (17:30)
4. Selects Serbian language
Result: Complete localized experience ✅
```

**Scenario 3: Laptop User**
```
User on laptop:
1. Battery automatically detected
2. Shows 85% with charging icon 🔌
3. Color-coded warnings when low
Result: Power awareness integrated into weather widget ✅
```

**Scenario 4: Mixed Preferences**
```
User wants:
- Fahrenheit (grew up with °F)
- Metric wind speed (races in km/h)
- 12-hour time (easier to read)
Result: Full flexibility - any combination works! ✅
```

---

## [v2.1.7] - 2026-01-10

### 🛰️ WINDOWS LOCATION UPDATE - Major Feature Release

#### ✨ New Features

##### Dual Location System
- **Windows Location API integration**: Use GPS/Wi-Fi triangulation for accurate positioning
- **Location Source selector**: Easy switching via tray menu between:
  - 📡 API Location (IP-based) - Default, works everywhere, city-level accuracy
  - 🛰️ Windows Location (GPS/Wi-Fi) - Accurate street-level positioning
- **Smart detection**: Automatically checks if Windows Location services are enabled
- **Bilingual setup guides**: Step-by-step instructions in Serbian and English
- **Graceful fallback**: Automatically switches to API Location if Windows Location unavailable
- **Registry validation**: Checks Windows Location service status before attempting connection

[... rest of CHANGELOG continues as before ...]
