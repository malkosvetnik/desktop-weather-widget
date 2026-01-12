# Release Notes v2.2.2

**Release Date**: January 12, 2026  
**Type**: Critical Bug Fix  
**Priority**: High - Recommended Update

---

## 🐛 Critical Bug Fix: Unit System Data Consistency

### What Was Fixed

**Problem**: Metric and Imperial measurement systems displayed mathematically inconsistent data.

**Example of the bug:**
```
Metric mode:   Visibility = 44.4 km
Imperial mode: Visibility = 90.6 mi

Mathematical check: 44.4 km × 0.621 = 27.6 mi (NOT 90.6 mi!)
Conclusion: Different source data, not proper conversion ❌
```

### Root Cause

Open-Meteo API exhibits unexpected behavior when the `wind_speed_unit` parameter changes:
- When requesting `wind_speed_unit=kmh`: Returns visibility = 44,420 meters
- When requesting `wind_speed_unit=mph`: Returns visibility = 145,734 meters

These are **completely different values**, not unit conversions of the same measurement.

### The Solution

Widget now **always requests metric units** from the API:
```python
# Fixed API call
weather_url = "...&wind_speed_unit=kmh&precipitation_unit=mm&..."
```

Then performs **manual, mathematically accurate conversions** for imperial display:
```python
# Imperial conversions (when needed)
wind_mph = wind_kmh / 1.609344
pressure_inhg = pressure_mbar * 0.02953
visibility_mi = visibility_km * 0.621371
```

### Verified Results

**Tested and confirmed accurate:**

| Parameter | Metric | Imperial | Conversion | Status |
|-----------|--------|----------|------------|--------|
| Wind | 26.6 km/h | 16.5 mph | 26.6 ÷ 1.609 = 16.53 | ✅ |
| Pressure | 1005 mbar | 29.68 inHg | 1005 × 0.02953 = 29.677 | ✅ |
| Visibility | 44.4 km | 27.6 mi | 44.4 × 0.621 = 27.59 | ✅ |

---

## 📥 Installation

### New Installation:
```bash
# Clone repository
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget

# Install dependencies
pip install PyQt5 requests geocoder psutil

# Run widget
python weather_widget_final.pyw
```

### Upgrade from v2.2.0 or v2.2.1:
```bash
# Simply replace the file
# Download weather_widget_final.pyw from v2.2.2 release
# Replace your existing file
# Restart widget

# All settings are preserved! ✅
```

---

## ⚙️ Technical Changes

### Modified Files:
- `weather_widget_final.pyw`
  - Line ~3347: API URL now hardcoded to metric units
  - Line ~3374-3380: Added manual wind speed conversion
  - Line ~2488-2495: Manual visibility conversion (already existed, now works correctly)
  - Added version header: `__version__ = "2.2.2"`

### API Request Changes:
```python
# BEFORE (v2.2.0-v2.2.1):
wind_unit_param = self.get_wind_unit_param()  # Returns "mph" or "kmh"
weather_url = f"...&wind_speed_unit={wind_unit_param}&..."

# AFTER (v2.2.2):
weather_url = f"...&wind_speed_unit=kmh&precipitation_unit=mm&..."  # Always metric
```

### Widget Conversion Logic:
```python
# Wind speed conversion
wind_speed_ms = current['wind_speed_10m']  # API returns m/s
wind_speed_kmh = wind_speed_ms * 3.6       # Convert to km/h

if self.unit_system == 'imperial':
    wind_speed = wind_speed_kmh / 1.609344  # Convert to mph
else:
    wind_speed = wind_speed_kmh             # Keep km/h

# Visibility conversion (in format_visibility function)
if self.unit_system == 'imperial':
    visibility_miles = visibility_km * 0.621371
    return f"{visibility_miles:.1f} mi"
else:
    return f"{visibility_km:.1f} km"
```

---

## 🎯 Impact Assessment

### User Impact:
- **Critical**: Users relying on Imperial mode had incorrect visibility readings
- **Data Integrity**: Fixed mathematical inconsistencies that could cause confusion
- **Trust**: Restores confidence in displayed measurements

### Compatibility:
- ✅ **No breaking changes**: All existing settings preserved
- ✅ **No new dependencies**: Uses existing requirements
- ✅ **Backward compatible**: Screenshots and documentation remain valid

---

## 🧪 Testing Performed

### Test Scenarios:
1. ✅ Metric mode: Verified all values display correctly
2. ✅ Imperial mode: Verified accurate conversions from metric source
3. ✅ Switch between modes: Values convert consistently
4. ✅ Refresh weather: Data remains consistent
5. ✅ Settings persistence: Unit preference saved correctly

### Test Results:
```
Test Environment: Windows 11, Python 3.11, Zaječar, Serbia
Test Date: January 12, 2026

Metric Mode Results:
  Wind: 26.6 km/h ✅
  Pressure: 1005 mbar ✅
  Visibility: 44.4 km ✅

Imperial Mode Results:
  Wind: 16.5 mph ✅ (26.6 ÷ 1.609 = 16.53)
  Pressure: 29.68 inHg ✅ (1005 × 0.02953 = 29.677)
  Visibility: 27.6 mi ✅ (44.4 × 0.621 = 27.59)

Conclusion: All conversions mathematically accurate within rounding tolerance.
```

---

## 📋 Known Issues

None identified in v2.2.2.

---

## 🔮 Future Improvements

Potential enhancements for future releases:
- Cross-platform support (Linux, macOS)
- Additional weather parameters
- Configurable themes/skins
- Widget size presets

---

## 🙏 Acknowledgments

- **Open-Meteo**: Free weather API with extensive data
- **Testing**: Extensive user testing revealed the inconsistency
- **Community**: Bug reports help improve quality

---

## 📞 Support & Feedback

- **Bug Reports**: [GitHub Issues](https://github.com/malkosvetnik/desktop-weather-widget/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/malkosvetnik/desktop-weather-widget/discussions)
- **Documentation**: [README.md](https://github.com/malkosvetnik/desktop-weather-widget)
- **Changelog**: [CHANGELOG.md](https://github.com/malkosvetnik/desktop-weather-widget/blob/main/CHANGELOG.md)

---

**Version**: 2.2.2  
**Release**: January 12, 2026  
**Status**: Stable  
**Recommended**: Yes - Critical bug fix

---

*Made with ❤️ by [malkosvetnik](https://github.com/malkosvetnik)*
