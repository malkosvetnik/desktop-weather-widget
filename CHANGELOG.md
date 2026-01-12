# Changelog

All notable changes to the Desktop Weather Widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v2.2.2] - 2026-01-12

### 🐛 Critical Bug Fixes

#### Unit System Data Consistency
- **Problem**: Metric and Imperial modes displayed completely inconsistent values
  - Example: Visibility showed 44.4 km (metric) vs 90.6 mi (imperial) - mathematically impossible!
  - Root cause: Open-Meteo API returns different raw visibility data when `wind_speed_unit` parameter changes
  - API behavior: Changing unit parameters affects more than just the requested field

- **Solution**: Widget now **always requests metric data** from API, then performs manual conversions
  - API call hardcoded to: `&wind_speed_unit=kmh&precipitation_unit=mm`
  - Widget handles all imperial conversions internally
  - Ensures consistent source data across all unit system modes

- **Technical Changes**:
  ```python
  # API Request (always metric)
  weather_url = "...&wind_speed_unit=kmh&precipitation_unit=mm&..."
  
  # Widget Conversion (imperial mode)
  wind_speed_mph = wind_speed_kmh / 1.609344
  visibility_mi = visibility_km * 0.621371
  pressure_inhg = pressure_mbar * 0.02953
  ```

- **Result**: **Mathematically accurate conversions**
  - Wind: 26.6 km/h = 16.5 mph ✅
  - Pressure: 1005 mbar = 29.68 inHg ✅
  - Visibility: 44.4 km = 27.6 mi ✅

**Impact**: Critical fix - ensures data integrity and user trust in displayed values

---

## [v2.2.0] - 2026-01-11

### 🎨 CUSTOMIZATION UPDATE - Major Feature Release

#### ✨ New Features

##### Temperature Unit System
- **Celsius/Fahrenheit selection**: Full temperature unit customization via tray menu
- **Instant conversion**: All temperature displays convert in real-time
- **API integration**: Direct Celsius/Fahrenheit parameter support from Open-Meteo
- **Persistent storage**: Temperature preference saved in Windows Registry

##### Time Format System
- **12-hour/24-hour selection**: User choice for time display format
- **Comprehensive updates**: Affects all time displays (clock, sunrise/sunset, timestamps)
- **Dynamic AM/PM**: Proper AM/PM display in 12-hour mode

##### Measurement Unit System (Metric/Imperial)
- **Wind speed units**: km/h ↔ mph
- **Pressure units**: mbar ↔ inHg
- **Visibility units**: km ↔ mi
- **API integration**: Direct parameter support (note: later found unreliable for visibility)
- **Consistent display**: All units update simultaneously

##### Battery Status (Laptop Support)
- **Real-time battery monitoring**: Shows percentage and charging status
- **Smart detection**: Automatically detects laptop vs desktop
- **Visual indicators**:
  - 🔌 Green: Charging
  - 🔋 White: 30%+ (normal)
  - 🔋 Orange: 15-29% (low)
  - 🪫 Red: <15% (critical)
- **Update frequency**: Refreshes every 30 seconds
- **Position**: Displayed beside main clock, vertically centered
- **Auto-hide**: Hidden on desktop PCs

#### 🛠️ Bug Fixes

##### Menu Translation System
- Fixed: Menu titles and options now properly translate between Serbian and English
- Dynamic updates when language changes
- All submenu items fully localized

##### Battery Label Positioning
- Fixed: Battery icon vertically centered with clock
- Added: `Qt.AlignVCenter` for proper alignment
- Result: Clean, professional appearance

##### Clock Display
- Fixed: Removed border artifacts when battery hidden
- Solution: Transparent wrapper widget
- Result: Seamless integration

#### 🆕 Dependencies

- Added: `psutil>=5.8.0` for battery status detection

---

[Previous changelog entries remain unchanged...]
