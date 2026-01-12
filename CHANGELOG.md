# Changelog

All notable changes to Desktop Weather Widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.2.3] - 2025-01-12

### 🔥 CRITICAL FIX

#### Fixed
- **Windows Location now works properly!** 
  - Previous implementation used non-existent `geocoder.windows()` method
  - New implementation uses **PowerShell + .NET System.Device.Location API**
  - Provides real GPS/Wi-Fi triangulation (not IP geolocation)
  - Displays accuracy in meters (e.g., "Accuracy: 106m")
  - No external dependencies required (removed `geocoder` dependency)
  
  **Technical details:**
  ```
  Old: geocoder.windows('me') → AttributeError (method doesn't exist)
  New: PowerShell → System.Device.Location API → JSON → Python parsing
  ```
  
  **Output example:**
  ```
  🔍 Pokušavam da dobijem Windows Location (PowerShell)...
  ✅ Windows Location uspešno: (43.9134, 22.2777)
     Accuracy: 106m
  ✅ Windows Location: Zaječar (43.9134, 22.2777)
  ```

- **JSON parsing with regex fallback**
  - PowerShell `ConvertTo-Json` adds extra whitespace
  - Added `-Compress` flag to PowerShell script
  - Regex fallback if standard JSON parsing fails
  - Handles both compressed and pretty-printed JSON

- **Automatic fallback to API location**
  - If Windows Location is disabled, widget automatically switches to API
  - Shows warning popup with instructions (localized SR/EN)
  - Prevents repeated popups during same session

### Added
- Windows Location status check via Registry
  - Checks both HKLM and HKCU registry keys
  - Detects "Allow" vs "Deny" status
  - Shows popup with Settings instructions if disabled

### Changed
- Removed dependency on `geocoder` library
- Windows Location now uses native Windows API only
- Improved error messages for location failures

---

## [2.2.2] - 2025-01-11

### Fixed
- **Visibility data now from `current` block**
  - Previous: Used `hourly[0]` which could be inconsistent
  - Now: Uses `current['visibility']` for real-time data
  
- **API parameter consistency**
  - Added `temperature_unit` parameter to API request
  - Ensures correct temperature scale from API
  - Fixes Celsius/Fahrenheit conversion issues

- **Pressure unit display**
  - Fixed mbar → inHg conversion for Imperial units
  - Proper rounding to 2 decimal places

### Changed
- Visibility always displayed in appropriate units (km or mi)
- Temperature conversion happens at API level (more accurate)

---

## [2.2.1] - 2025-01-10

### Fixed
- **Wind speed unit consistency**
  - API always returns m/s → convert to km/h → convert to mph if Imperial
  - Previous: Direct API parameter caused inconsistencies
  - Now: Manual conversion for accurate display

- **Precipitation unit consistency**
  - API always returns mm → convert to inches if Imperial
  - Fixes mm vs inches display mismatches

### Changed
- All unit conversions now happen in Python (not via API parameters)
- More reliable and consistent across different unit systems

---

## [2.2.0] - 2025-01-09

### Added
- **Multi-language support**
  - 🇷🇸 Serbian (Latin script)
  - 🇬🇧 English
  - All UI elements, tooltips, and messages localized
  - Automatic Cyrillic → Latin conversion for city names

- **Temperature unit selection**
  - Celsius (°C)
  - Fahrenheit (°F)
  - Independent from other unit systems

- **Time format selection**
  - 12-hour format with AM/PM
  - 24-hour format
  - Affects clock, sunrise/sunset, hourly forecast

- **Unit system selection**
  - Metric (km/h, mbar, km, mm)
  - Imperial (mph, inHg, mi, in)
  - Affects wind, pressure, visibility, precipitation

- **Location source selection**
  - API Location (IP geolocation)
  - Windows Location (GPS/Wi-Fi)
  - Tray menu toggle between sources

- **Battery status display**
  - Shows on laptops only (auto-detected)
  - Icons: 🔌 (charging), 🔋 (full), 🪫 (low/critical)
  - Dynamic colors: green/white/orange/red
  - Real-time updates every 5 seconds

- **Resolution presets**
  - 8 monitor resolution presets (XGA → 8K UHD)
  - Manual widget size selection
  - Automatic scaling for different monitors

### Changed
- Tray menu now organized with submenus
- All settings saved to QSettings (persistent)
- Language-aware date and time formatting

---

## [2.1.8] - 2025-01-08

### Added
- **Hourly forecast tooltip**
  - Shows next 12 hours when hovering over hourly forecast label
  - Displays time, icon, temperature, precipitation probability
  - Formatted according to selected time format

- **Air Quality tooltip**
  - Shows detailed pollutants when hovering over AQI label
  - Displays PM10, PM2.5, CO, NO₂, SO₂, O₃ levels
  - Color-coded by pollution level

### Changed
- Improved tooltip styling (dark theme, better padding)
- Tooltips appear on hover (no click required)

---

## [2.1.7] - 2025-01-07

### Added
- **Precipitation alerts with minutely_15 data**
  - Uses Open-Meteo minutely_15 forecast (0-2 hours)
  - "Rain NOW!" / "Snow NOW!" alerts
  - "Rain in 15min" / "Snow in 15min" predictions
  - Accurate detection of rain vs snow based on weather codes

- **Hourly forecast display**
  - Shows NEXT hour (current hour skipped)
  - Icon, temperature, precipitation probability
  - Automatically detects rain vs snow

### Fixed
- Weather description now matches current conditions
  - If rain detected: override weather_code with "Rain" 🌧️
  - If snow detected: override weather_code with "Snow" ❄️
  - Prevents mismatch between description and actual conditions

### Changed
- Weather alerts box repurposed for hourly forecast
- Precipitation alerts moved to separate box

---

## [2.1.6] - 2025-01-06

### Added
- **Sleep/Wake detection**
  - Detects laptop sleep/hibernate
  - Waits 30s before first refresh after wake
  - Exponential backoff if network not ready
  - Displays "💤 sleep detected" status

- **Offline status handling**
  - "🌐 offline – waiting for internet" message
  - Preserves last known weather data during offline
  - Auto-retry when connection restored

- **Last updated timestamp**
  - "🕒 Last update: HH:MM" always visible
  - Persists through offline/sleep periods
  - Updates on successful weather refresh

### Changed
- Improved network error handling
- No more widget crashes during internet outages
- Graceful degradation when APIs unavailable

---

## [2.1.5] - 2025-01-05

### Added
- **Air Quality monitoring**
  - European AQI standard
  - Categories: Excellent, Good, Moderate, Poor, Very Poor
  - Color-coded display
  - Detailed pollutants (PM10, PM2.5, CO, NO₂, SO₂, O₃)

- **5-day weather forecast**
  - Daily min/max temperatures
  - Weather icons and descriptions
  - Day names and dates

### Changed
- Widget layout reorganized for better information density
- Improved spacing and alignment

---

## [2.1.0] - 2025-01-04

### Added
- **Click-Through Mode**
  - Widget becomes transparent to mouse clicks
  - Can click through to applications behind widget
  - Toggle via tray menu

- **Widget-Only Mode**
  - Hides tray icon
  - Widget runs as standalone window
  - Close button (X) to exit

- **Lock Position**
  - Lock/unlock widget position
  - Prevents accidental dragging
  - Toggle button: 🔒 / 🔓

### Changed
- Improved tray icon with temperature display
- Better window flags for click-through functionality

---

## [2.0.0] - 2025-01-03

### Added
- **Auto-start with Windows**
  - Registry entry for startup
  - Toggle via tray menu
  - Automatic status check on launch

- **Persistent settings**
  - QSettings for configuration storage
  - Remembers position, size, location
  - Saves refresh interval and preferences

- **Tray icon menu**
  - Show/hide widget
  - Update weather manually
  - Exit application

- **Refresh interval selection**
  - 5, 10, 15, 30, 60 minutes
  - Configurable via dropdown

### Changed
- Complete UI redesign
- Dark theme with transparent backgrounds
- Modern emoji-based icons

---

## [1.0.0] - 2025-01-01

### Added
- **Initial release**
- Basic weather display
- Location search
- Current conditions
- Temperature, humidity, wind
- Manual refresh

---

## Legend

- 🔥 **CRITICAL** - Major bug fix or security update
- ✨ **Added** - New feature
- 🔧 **Changed** - Modification to existing feature
- 🐛 **Fixed** - Bug fix
- 🗑️ **Removed** - Feature removal
- 🔒 **Security** - Security improvement
- 📝 **Documentation** - Documentation update

---

*For more details, see the [README.md](README.md)*
