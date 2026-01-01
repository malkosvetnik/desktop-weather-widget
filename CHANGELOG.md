# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-01-01

### 🎉 Major Update - Advanced Features

#### Added
- 🎨 **Dynamic Alert Colors** - Alerts now change background color based on severity:
  - Green (No alerts)
  - Yellow (Standard warnings)
  - Red (Extreme warnings/emergencies)
- 🖱️ **Interactive Tooltips** for Weather Alerts
  - Hover over alerts to see full text
  - Shows alert duration (start/end time)
  - Displays detailed description
- 🌧️ **Precise Precipitation Alerts**
  - Hour-by-hour accuracy (instead of 3-hour intervals)
  - Shows exact time until rain/snow
  - Better forecasting with real-time data
- 🇷🇸 **Complete Serbian Translation**
  - All UI elements translated
  - Weather descriptions in Serbian
  - Alert descriptions automatically translated
  - Fixed API typos in translation
- 📏 **Smart Text Formatting**
  - Auto font-sizing for long alert text
  - Always displays in exactly 2 lines
  - Intelligent text truncation with "..."
  - Preserves readability

#### Improved
- 🖱️ **Air Quality Tooltips** - Enhanced clickable label system
- 🔄 **Better Sleep/Wake Detection** - 30s delay after system wake
- 🌐 **Improved API Error Handling** - Retry logic with progressive delays
- 📍 **Location Detection** - Better city name mapping for Serbian cities
- 🎯 **UI Consistency** - Unified tooltip styling across all elements

#### Fixed
- Translation bugs in alert descriptions
- Font size consistency in alert box
- Tooltip positioning issues
- Registry cleanup on fresh install
- MSL altitude references in weather data

### Technical Changes
- Refactored `translateAlertDescription()` to use regex patterns
- Added `formatAlertText()` for smart text fitting
- Implemented `getAlertColorLevel()` for dynamic styling
- Enhanced `ClickableLabel` class for tooltips
- Improved `updateRainAlert()` precision with hourly data
- Added `current_alert_data` storage for tooltips

## [1.0.0] - 2025-12-XX

### Initial Release

#### Features
- ⏰ Real-time clock with date
- 🌡️ Current weather conditions
- 💨 Wind speed and direction
- 🌅 Sunrise/sunset times
- 📊 Atmospheric data (pressure, humidity, visibility, cloudiness)
- ☀️ UV Index with color coding
- 🌫️ Air Quality Index (AQI)
- 🖱️ Interactive pollution tooltips
- 📅 5-day weather forecast
- 📍 Auto-location or manual city selection
- 🔄 Configurable refresh intervals (5-60 min)
- 🔒 Lock position feature
- 👻 Click-through mode
- 🚀 Windows startup option
- 📐 Multi-resolution support (XGA to 8K)
- 💾 Persistent settings in Windows Registry
- 🎯 Always-on-bottom window placement
- 🌙 System tray integration
- 🔔 Tray notifications

#### Technical Details
- Built with PyQt5
- OpenWeatherMap API integration
- Windows Registry for settings storage
- Session-based HTTP requests
- Automatic geocoding for cities
- Serbian city name mapping

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-01-01 | Advanced features update |
| 1.0.0 | 2025-12-XX | Initial release |

---

## Upgrade Notes

### From 1.x to 2.0

**Breaking Changes:**
- None - fully backward compatible

**New Dependencies:**
- No new dependencies required

**Settings Migration:**
- All existing settings preserved
- New settings added with defaults
- Registry structure unchanged

**Recommended Actions:**
1. Close the widget completely
2. Update to new version
3. Restart the application
4. Test new tooltip features
5. Check alert color coding

---

## Future Plans

### Planned for 2.1.0
- [ ] Weather radar integration
- [ ] Historical data charts
- [ ] Custom notification sounds
- [ ] Multiple location support

### Planned for 3.0.0
- [ ] Executable (.exe) build
- [ ] Full English language support
- [ ] Custom theme system
- [ ] Weather icon packs
- [ ] Mini/compact mode
