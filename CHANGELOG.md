# Changelog

All notable changes to the Desktop Weather Widget will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v2.1.6] - 2026-01-09

### 🎊 NOWCAST UPDATE - Major Feature Release

#### ✨ New Features

##### 15-Minute Precision Nowcast
- **Minutely forecasts**: Added `minutely_15` API integration for 0-2 hour nowcast
- **8 intervals × 15min**: Provides radar-like precision for immediate precipitation
- **Smart time parsing**: Always shows future intervals, skips past timestamps
- **Intelligent alerts**: 
  - "Rain in 15 min (60%)"
  - "Rain in 45 min (70%)"
  - "Rain in 1h 30min (85%)"
- **Type detection**: Accurately distinguishes rain vs snow in nowcast

##### 4-Layer Priority System
Implemented intelligent weather alert prioritization:

1. **Priority 1 - Current Weather** (highest)
   - Checks `current.rain` and `current.snowfall` values
   - Shows: "Rain NOW!" / "Snow NOW!" / "Storm NOW!"
   
2. **Priority 2 - Weather Code Validation**
   - Validates precipitation type from WMO codes
   - Cross-references with probability data
   
3. **Priority 3 - Minutely Nowcast (0-2h)**
   - Uses `minutely_15` API for 15-minute precision
   - Threshold: 60% probability OR 0.1mm+ precipitation
   - Shows immediate-term alerts
   
4. **Priority 4 - Hourly Forecast (2-24h)**
   - Falls back to hourly data for longer-term forecasts
   - Threshold: 40% probability OR any precipitation
   - Shows planning-horizon alerts

#### 🐛 Bug Fixes

##### Minutely Forecast Parsing
- Fixed: Now correctly identifies first **future** interval (was including current/past)
- Fixed: Properly iterates through 8 future intervals (not from index 0)
- Fixed: Handles API timestamp comparison with local time correctly

##### Time Display
- Fixed: Minutes calculation for composite times (e.g., "1h 30min")
- Fixed: Proper formatting for < 60 min vs ≥ 60 min scenarios
- Fixed: Edge case at midnight rollover (23:45 → 00:15)

##### Precipitation Type Detection
- Fixed: Snow vs rain differentiation using `snowfall` field
- Fixed: Handles mixed precipitation scenarios
- Fixed: Proper emoji selection (🌧️ vs ❄️) based on type

##### API Data Handling
- Fixed: Graceful degradation when `minutely_15` data unavailable
- Fixed: Fallback to hourly when nowcast missing
- Fixed: Handles partial API responses without crashes

#### 🔧 Technical Improvements

##### Code Optimizations
```python
# OLD (v2.1.0):
for i in range(len(times)):  # Started from 0
    forecast_time = datetime.fromisoformat(times[i])
    # Could include past times!

# NEW (v2.1.6):
start_index = None
for idx, time_str in enumerate(times):
    if forecast_time >= current_time:
        start_index = idx  # Find first FUTURE interval
        break

for i in range(8):
    idx = start_index + i  # Iterate from future only
```

##### Enhanced Logging
- Added debug output for minutely parsing (invisible in .exe)
- Logs first future interval detection
- Tracks precipitation type decisions
- Shows priority system flow

##### API Request Optimization
```python
# Added to API URL:
&minutely_15=precipitation,precipitation_probability,rain,snowfall
&current=rain,snowfall,weather_code
```

##### Error Recovery
- Better handling of missing `minutely_15` data
- Automatic fallback to hourly forecasts
- No crashes on incomplete API responses
- Maintains last known state during errors

#### 📊 Alert Display Logic

| Scenario | Time Until | Display |
|----------|-----------|---------|
| Rain detected in current conditions | NOW | 🌧️ Rain NOW! |
| Rain in next 15 min | 15 min | 🌧️ Rain in 15 min (70%) |
| Rain in next 45 min | 45 min | 🌧️ Rain in 45 min (65%) |
| Rain in 1h 15min | 75 min | 🌧️ Rain in 1h 15min (80%) |
| Rain in 6 hours | 6h | 🌧️ Rain in 6h (55%) |
| Snow in 30 min | 30 min | ❄️ Snow in 30 min (75%) |
| No precipitation | N/A | ☀️ No precipitation |

#### 🎯 Performance Impact
- API calls: No increase (minutely_15 added to existing request)
- Memory: +2-5 KB for minutely data storage
- CPU: Negligible (<1% increase for parsing)
- Network: +~500 bytes per API response

#### ⚠️ Known Limitations
- Minutely forecasts available for most regions (not all)
- Graceful fallback to hourly if unavailable
- 2-hour nowcast window (API limitation)

---

## [v2.1.0] - 2026-01-05

### 🎉 Major Updates

#### ✨ New Features
- **Full English language support** - Complete UI translation alongside Serbian (switch via tray menu)
- **Real-time precipitation detection**: Now correctly shows "Rain NOW!" / "Kiša SADA!" when it's actively raining
- **Improved precipitation forecasting**: Accurate timing for rain, snow, and storms
- **Enhanced tooltip system**: Hourly forecast tooltip with clickable labels

#### 🐛 Bug Fixes
- **Fixed "Error" translation issue**: Error messages now properly translate between Serbian/English
- **Fixed precipitation detection logic**: 
  - Changed from `int()` to `round()` for proper time rounding (1.9h → 2h instead of 1h)
  - Added validation for both weather_code AND actual rain values
  - Now checks current weather BEFORE searching for future precipitation
- **Fixed tooltip text translation**: "Hover na ikonicu za detalje" now translates properly
- **Fixed API data fetching**: Added `rain`, `precipitation`, and `showers` to API request

#### 🔧 Technical Improvements
- **Smarter time calculation**: 
  - 1h 56min → "Rain in 2h" (previously showed "1h")
  - 44min → "Rain in 1h" (correct)
- **Better sleep mode handling**: Maintains all functionality after system wake
- **Debug logging**: Added comprehensive debug output (invisible in .exe builds)

#### 📊 What Works Now
| Scenario | Display |
|----------|---------|
| Rain falling NOW | 🌧️ Kiša SADA! / Rain NOW! |
| Rain in 44 minutes | 🌧️ Kiša za 1h / Rain in 1h |
| Rain in 1h 56min | 🌧️ Kiša za 2h / Rain in 2h |
| Snow falling NOW | ❄️ Sneg SADA! / Snow NOW! |
| Storm in 3 hours | ⛈️ Oluja za 3h / Storm in 3h |
| No precipitation | ☀️ Nema padavina / No precipitation |

### 🌐 Language Support
- Full Serbian (Latin) translation
- Full English translation
- Dynamic language switching

### 📝 Notes
- All existing features preserved (5-day forecast, UV index, air quality, sleep mode, click-through, etc.)
- Debug logs included but invisible in compiled .exe
- Compatible with all previous settings

---

## [v2.0.0] - 2025-12-XX

### 🎉 Initial Public Release

#### ✨ Features
- Real-time weather display with emoji icons
- 5-day weather forecast
- Hourly forecast (12h) with tooltip
- UV Index with color coding
- Air Quality Index (AQI) with pollutant breakdown
- Precipitation alerts
- Wind speed and direction
- Humidity, pressure, visibility
- Cloud cover percentage
- Sunrise and sunset times

#### 🎨 Customization
- Serbian (Latin) language support
- Auto-location detection
- Manual city search
- Adjustable refresh intervals (5-60 min)
- Resolution presets (XGA to 8K UHD)
- Click-through mode
- Position locking
- System tray integration

#### 🛌 Advanced Features
- Sleep mode detection and recovery
- Network retry logic (3 attempts)
- Startup with Windows option
- Persistent settings via Windows Registry
- Graceful offline handling

#### 🔧 Technical Details
- Built with PyQt5
- Uses Open-Meteo API (free, no key required)
- Windows Registry for settings storage
- Unicode emoji for icons
- Minimal resource usage

---

## [Unreleased]

### Planned Features
- [ ] Desktop notifications (Windows toast)
- [ ] Customizable themes (dark/light/auto)
- [ ] More languages (German, French, Spanish)
- [ ] Widget size presets
- [ ] Multiple location tracking
- [ ] Weather radar integration
- [ ] Severe weather alerts from national services

### Under Consideration
- [ ] macOS/Linux support
- [ ] Microsoft Store release
- [ ] Mobile companion app
- [ ] Smart home integration

---

## Version Numbering

This project uses Semantic Versioning:
- **Major (X.0.0)**: Breaking changes, major redesigns
- **Minor (0.X.0)**: New features, backwards compatible
- **Patch (0.0.X)**: Bug fixes, minor improvements

---

## How to Read This Changelog

- **✨ New Features**: Major additions to functionality
- **🐛 Bug Fixes**: Corrections of incorrect behavior
- **🔧 Technical Improvements**: Under-the-hood enhancements
- **📊 Display Changes**: UI/UX modifications
- **⚠️ Breaking Changes**: Backwards-incompatible changes (avoid in minor versions)
- **🔒 Security**: Vulnerability patches

---

**For detailed release notes, see [RELEASE_NOTES.md](RELEASE_NOTES.md)**
