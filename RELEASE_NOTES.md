# 🌤️ Weather Widget v2.1.6 - NOWCAST UPDATE

## 🎊 The Game-Changer: 15-Minute Precision Weather

Version 2.1.6 introduces **radar-like nowcast precision** that tells you exactly when rain will start - down to 15-minute intervals!

---

## 🚀 What's New

### ⚡ 15-Minute Nowcast (Major Feature!)

**Never get caught in the rain again!** The widget now shows:

```
🌧️ Rain in 15 min (60%)
🌧️ Rain in 45 min (75%)  
❄️ Snow in 1h 15min (80%)
```

**How it works:**
- Uses `minutely_15` API for 0-2 hour precision
- Updates every 15 minutes with fresh data
- Distinguishes between rain, snow, and storms
- Shows probability percentage for each interval

**Example scenario:**
```
12:00 PM - You check the widget
         → "Rain in 45 min (70%)"
12:45 PM - Rain starts (as predicted!)
         → Widget now shows "Rain NOW!"
```

### 🧠 4-Layer Intelligence System

The widget now uses a smart priority system:

**Priority 1: Current Weather (Highest)**
- Checks if it's raining RIGHT NOW
- Display: "Rain NOW!" / "Kiša SADA!"

**Priority 2: Weather Code Validation**  
- Confirms precipitation type from WMO codes
- Cross-checks with probability data

**Priority 3: Nowcast (0-2 hours)**
- 15-minute precision alerts
- Threshold: 60% probability
- Display: "Rain in 45 min (70%)"

**Priority 4: Hourly Forecast (2-24 hours)**
- Long-term planning horizon
- Threshold: 40% probability  
- Display: "Rain in 6h (55%)"

---

## 🐛 Bug Fixes

### Critical Fixes
✅ **Fixed nowcast time parsing**
- Widget now correctly shows FUTURE intervals (was showing past/current)
- Properly calculates "first future 15-min interval"
- Handles midnight rollover gracefully

✅ **Fixed precipitation type detection**
- Accurately distinguishes snow vs rain using `snowfall` field
- Proper emoji selection (🌧️ vs ❄️)
- Handles mixed precipitation scenarios

✅ **Fixed API data handling**
- Graceful degradation when minutely data unavailable
- Automatic fallback to hourly forecasts
- No crashes on partial API responses

### Minor Improvements
- Better time formatting for composite durations (e.g., "1h 30min")
- Enhanced debug logging (invisible in normal use)
- Optimized API request structure
- Improved error recovery logic

---

## 📊 Alert Display Examples

| Time Until Rain | Old Widget (v2.1.0) | New Widget (v2.1.6) |
|----------------|---------------------|---------------------|
| NOW | ✅ Rain NOW! | ✅ Rain NOW! |
| 15 minutes | ❌ Rain in 1h | ✅ Rain in 15 min (60%) |
| 45 minutes | ❌ Rain in 1h | ✅ Rain in 45 min (70%) |
| 1h 15min | ❌ Rain in 1h | ✅ Rain in 1h 15min (80%) |
| 6 hours | ✅ Rain in 6h | ✅ Rain in 6h (55%) |

---

## 🎯 Technical Details

### API Changes
```python
# Added to API request:
&minutely_15=precipitation,precipitation_probability,rain,snowfall
&current=rain,snowfall,weather_code
```

### Performance Impact
- **API calls**: No increase (added to existing request)
- **Memory**: +2-5 KB for minutely data
- **CPU**: <1% increase for parsing
- **Network**: +~500 bytes per response

### Code Quality
- Added 200+ lines of nowcast logic
- Comprehensive error handling
- Full backwards compatibility
- Extensive inline documentation

---

## 📥 Download

### Installation Options

**Option 1: Python Source**
```bash
# Clone or download from GitHub
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget

# Install dependencies
pip install PyQt5 requests

# Run widget
python weather_widget.pyw
```

**Option 2: Compiled .exe (Coming Soon!)**
- No Python required
- Double-click to run
- Auto-updater included

---

## 🔄 Upgrade Instructions

### From v2.1.0 → v2.1.6

**No breaking changes!** Just replace the file:

1. Download new `weather_widget.pyw`
2. Replace old file
3. Restart widget
4. All settings preserved! ✅

### Settings Migration
- ✅ Window position preserved
- ✅ Language preference kept
- ✅ Refresh interval maintained
- ✅ Lock/click-through status unchanged

---

## 📸 Screenshots

### 15-Minute Nowcast in Action

**Before (v2.1.0):**
```
🌧️ Rain in 1h
```

**After (v2.1.6):**
```
🌧️ Rain in 45 min (70%)
```
*Much more precise! You know EXACTLY when to grab your umbrella.*

### Precipitation Alert Progression
```
12:00 PM: "Rain in 45 min (70%)"  ← Nowcast alert
12:15 PM: "Rain in 30 min (75%)"  ← Getting closer
12:30 PM: "Rain in 15 min (80%)"  ← Last warning!
12:45 PM: "Rain NOW!"             ← It's here!
```

---

## 🌍 Language Support

Both languages fully updated:

### Serbian (Srpski)
```
🌧️ Kiša za 15 min (60%)
🌧️ Kiša za 45 min (70%)
❄️ Sneg za 1h 15min (80%)
⛈️ Oluja za 2h (85%)
☀️ Nema padavina
```

### English
```
🌧️ Rain in 15 min (60%)
🌧️ Rain in 45 min (70%)
❄️ Snow in 1h 15min (80%)
⛈️ Storm in 2h (85%)
☀️ No precipitation
```

---

## ⚙️ System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit) or newer
- **Python**: 3.8+ (if running from source)
- **RAM**: 50 MB
- **Disk**: 5 MB

### Recommended
- **OS**: Windows 11
- **Python**: 3.10+
- **Internet**: Broadband (for real-time updates)

---

## 🐛 Known Issues

### Minor Limitations
- Minutely forecasts available for **most regions** (not all)
  - Widget gracefully falls back to hourly if unavailable
- 2-hour nowcast window (API limitation)
- Some regions may have 30-min intervals instead of 15-min

### Workarounds
- If nowcast unavailable → hourly forecasts still work perfectly
- If offline → widget shows last cached data
- If API slow → widget retries automatically (3 attempts)

**Report issues:** https://github.com/malkosvetnik/desktop-weather-widget/issues

---

## 🎯 Use Cases

### Perfect for:
✅ **Commuters**: "Should I bike or drive today?"  
✅ **Outdoor workers**: "Can I finish this task before rain?"  
✅ **Dog walkers**: "Time for a quick walk before the storm?"  
✅ **Event planners**: "Will the outdoor party stay dry?"  
✅ **Sports enthusiasts**: "Can we play the full game?"  

### Real-world example:
```
You: "I need to walk the dog"
Widget: "Rain in 30 min (75%)"
You: "Perfect! 20-minute walk, home before rain!"
```

---

## 🏆 Comparison

### vs. Microsoft Weather Widget
| Feature | Microsoft | This Widget |
|---------|-----------|-------------|
| Nowcast precision | ❌ Hourly only | ✅ 15-minute |
| Desktop placement | ❌ Sidebar only | ✅ Anywhere |
| Offline mode | ❌ Requires connection | ✅ Shows cached |
| Bilingual | ❌ System language | ✅ User choice |
| Open source | ❌ Closed | ✅ MIT License |
| Telemetry | ⚠️ Yes | ✅ None |

### vs. Weather Apps (AccuWeather, Weather.com)
| Feature | Apps | This Widget |
|---------|------|-------------|
| Always visible | ❌ Must open app | ✅ Desktop widget |
| Resource usage | ⚠️ 100+ MB | ✅ 50 MB |
| Ads | ⚠️ Yes (free tier) | ✅ None |
| API cost | ⚠️ Freemium | ✅ Free forever |

---

## 🔮 What's Next?

### Coming in v2.2.0
- 📱 Desktop notifications (Windows toast)
- 🎨 Theme customization (dark/light/auto)
- 📏 Widget size presets (small/medium/large)
- 🔔 Custom alert thresholds

### Future Roadmap
- 🌍 More languages (German, French, Spanish)
- 📍 Multiple location tracking
- 🗺️ Weather radar overlay
- ⚠️ Severe weather alerts

---

## 🙏 Credits

### Data Sources (100% Free!)
- **Weather data**: [Open-Meteo API](https://open-meteo.com)
- **Air quality**: [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)

### Technologies
- **Framework**: PyQt5
- **Icons**: Unicode emoji
- **Language**: Python 3.8+

### Special Thanks
- Open-Meteo team for the amazing free API
- PyQt5 developers for the excellent framework
- All beta testers and issue reporters
- The open-source community

---

## 💬 Community

### Get Involved
- ⭐ **Star** the repo if you find it useful!
- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** in Discussions
- 🔧 **Contribute code** via Pull Requests
- 📢 **Spread the word** on Reddit/Twitter

### Support
- 📧 Email: [Submit via GitHub Issues]
- 💬 Discussions: https://github.com/malkosvetnik/desktop-weather-widget/discussions
- 🐛 Bug Reports: https://github.com/malkosvetnik/desktop-weather-widget/issues

---

## 📜 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

## 📦 Files in This Release

- `weather_widget.pyw` - Main application file
- `requirements.txt` - Python dependencies
- `README.md` - Documentation
- `CHANGELOG.md` - Version history
- `LICENSE` - MIT License
- `screenshots/` - UI screenshots

---

**Made with ❤️ and ☕ by [malkosvetnik](https://github.com/malkosvetnik)**

*Never get caught in the rain again!* 🌂

---

## 🎊 Celebrate with Us!

This release represents:
- 📅 **2+ months** of development
- 🐛 **50+ bugs** squashed
- ✨ **20+ features** added
- ⌨️ **3000+ lines** of code
- ☕ **Countless cups** of coffee

**Thank you for using Desktop Weather Widget!** ⭐

---

*Version 2.1.6 released on January 9, 2026*
