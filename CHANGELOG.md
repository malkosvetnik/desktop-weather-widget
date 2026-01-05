# Changelog

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

## [v1.0.0] - Previous Release
- Initial release with basic weather widget functionality

### 🌐 Language Support
- **NEW: Full English translation** - All UI elements, menus, tooltips, and error messages
- **Serbian (Latin)** - Complete translation maintained
- **Dynamic language switching** - Change language via tray menu without restart
- **Translated elements**:
  - All weather descriptions
  - Precipitation alerts ("Rain NOW!", "Kiša SADA!")
  - Error messages
  - Tooltips and hover text
  - Menu items
  - Days of week and months
  - All UI labels

