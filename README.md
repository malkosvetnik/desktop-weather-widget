# 🌤️ Desktop Weather Widget v2.2.3

**Elegantan, minimalistički desktop weather widget sa Windows Location podrškom, multi-jezičnom lokalizacijom i naprednim funkcijama.**

![Main Widget - Serbian](screenshots/main_widget_serbian.png)

---

## ✨ Glavne karakteristike

### 🌍 **Lokacija**
- 🔄 **API Auto-detekcija** (IP geolocation)
- 📍 **Windows Location API** (GPS/Wi-Fi triangulacija)
- 🔍 **Manualna pretraga** gradova širom sveta
- 🌐 **Reverse geocoding** za prikaz naziva grada

### 🌡️ **Vremenski podaci**
- 🌤️ **Trenutno vreme** sa detaljnim podacima
- 📊 **5-dnevna prognoza** (min/max temperatura)
- 🕐 **Satna prognoza** za narednih 12 sati (tooltip)
- 🌧️ **Padavine** sa preciznim predviđanjima (minutely_15)
- 🌫️ **Kvalitet vazduha** (European AQI) sa detaljnim polutantima
- ☀️ **UV Index** sa bojom prema nivou
- 👁️ **Vidljivost**, pritisak, oblačnost, vetar sa pravcem
- 🌅 **Izlazak/zalazak** sunca

### 🌐 **Lokalizacija**
- 🇷🇸 **Srpski** (latinica + ćirilica)
- 🇬🇧 **English**
- 🔤 **Automatska konverzija** ćirilice u latinicu
- 📅 **Lokalizovani datumi** i dani u nedelji

### ⚙️ **Podešavanja**
- 🌡️ **Celsius / Fahrenheit** (nezavisno od ostatka)
- 🕐 **12h / 24h** format vremena
- 📏 **Metric / Imperial** jedinice (vetar, pritisak, vidljivost)
- 📍 **API / Windows Location** izvori
- 🔄 **Refresh interval** (5min, 10min, 15min, 30min, 60min)
- 📐 **Rezolucija monitora** (8 presets: XGA → 8K UHD)

### 🎨 **UI/UX**
- 🔒 **Lock/Unlock** pozicija widgeta
- 👻 **Click-Through Mode** (prozirnost za miša)
- 🖥️ **Widget-only Mode** (bez tray ikonice)
- 🚀 **Auto-start** sa Windows-om
- 🔋 **Battery status** (samo na laptopovima)
- 🕐 **Live sat** sa sekundama
- 💡 **Tooltips** sa detaljnim podacima
- 🌙 **Tamna tema** sa poludprovidnim pozadinama

---

## 📸 Screenshots

### 🇷🇸 Srpski jezik
![Main Widget - Serbian](screenshots/main_widget_serbian.png)
*Glavni prikaz sa svim podacima*

![Main Widget - 24h format](screenshots/main_widget_24h.png)
*24-časovni format vremena*

![Main Widget - Celsius](screenshots/main_widget_celsius.png)
*Celsius temperatura (default)*

![Main Widget - Fahrenheit](screenshots/main_widget_fahrenheit.png)
*Fahrenheit temperatura*

![Main Widget - Imperial](screenshots/main_widget_imperial.png)
*Imperial jedinice (mph, inHg)*

### 🇬🇧 English Language
![Main Widget - English](screenshots/main_widget_english.png)
*English language interface*

### 📊 Tooltips
![Hourly Forecast Tooltip](screenshots/hourly_forecast_tooltip.png)
*Satna prognoza za 12 sati sa tooltipom*

![Hourly Forecast 12h](screenshots/hourly_forecast_tooltip_12h.png)
*Satna prognoza u 12h formatu*

![Air Quality Tooltip](screenshots/air_quality_tooltip.png)
*Detaljni polutanti vazduha*

![Precipitation Alert](screenshots/precipitation_alert.png)
*Upozorenje o padavinama*

### ⚙️ Meniji
![Tray Menu - Full](screenshots/tray_menu_full.png)
*Kompletan tray meni*

![Tray Menu](screenshots/tray_menu.png)
*Standardni tray meni*

![Tray Menu - English](screenshots/tray_menu_english.png)
*Tray meni na engleskom*

![Language Menu](screenshots/language_menu.png)
*Izbor jezika*

![Location Menu - Serbian](screenshots/location_menu_serbian.png)
*Meni za izbor lokacije (srpski)*

![Location Menu - English](screenshots/location_menu_english.png)
*Meni za izbor lokacije (engleski)*

![Temperature Menu - Celsius](screenshots/temperature_menu_celsius.png)
*Izbor temperature jedinice*

![Time Format Menu](screenshots/time_format_menu.png)
*Izbor formata vremena*

![Unit System Menu](screenshots/unit_system_menu.png)
*Izbor sistema jedinica*

---

## 🚀 Instalacija

### Preduslov: Python 3.8+

```bash
# Proveri Python verziju
python --version
```

### Instalacija dependencija

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
PyQt5>=5.15.0
requests>=2.25.0
psutil>=5.8.0
```

### Pokretanje

```bash
python weather_widget_final.pyw
```

---

## 🔧 Konfiguracija

### Windows Location Setup

Za korišćenje Windows Location API-ja:

1. Otvori **Settings** (⊞ Win + I)
2. Idi na **Privacy & Security → Location**
3. Uključi **Location services**
4. Omogući **Let apps access your location**

Widget će automatski detektovati Windows Location status.

### Auto-start sa Windows-om

Desni klik na tray ikonu → **✓ Pokreni sa Windows-om**

Widget će dodati entry u Windows Registry:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

---

## 📋 Changelog - v2.2.3 (2025-01-12)

### 🔥 **KRITIČNE IZMENE:**

#### ✅ **Windows Location FIX**
- **Problem:** `geocoder.windows()` metod ne postoji → padao na IP geolocation
- **Rešenje:** Implementiran **PowerShell + .NET System.Device.Location API**
- **Rezultat:** 100% prava Windows Location sa GPS/Wi-Fi triangulacijom
- **Accuracy:** Prikazuje preciznost lokacije u metrima
- **No dependencies:** Nema potrebe za `geocoder` bibliotekom

**Detalji:**
```python
# Stari kod (NE RADI):
import geocoder
g = geocoder.windows('me')  # ❌ Ne postoji!

# Novi kod (RADI):
PowerShell → .NET System.Device.Location API → JSON → Python
```

**Output:**
```
🔍 Pokušavam da dobijem Windows Location (PowerShell)...
✅ Windows Location uspešno: (43.9134, 22.2777)
   Accuracy: 106m
✅ Windows Location: Zaječar (43.9134, 22.2777)
```

### 🌐 **Multi-jezik podrška:**
- 🇷🇸 Srpski (latinica)
- 🇬🇧 English
- ✅ Sve labele, meniji, tooltips, upozorenja lokalizovani
- ✅ Automatska konverzija ćirilice u latinicu

### 🌡️ **Temperature & Unit System:**
- ✅ Nezavisan izbor **Celsius/Fahrenheit** za temperaturu
- ✅ **Metric/Imperial** za ostale jedinice (vetar, pritisak, vidljivost)
- ✅ Konzistentnost između API poziva i prikaza

### 🕐 **Time Format:**
- ✅ 12-hour format sa AM/PM
- ✅ 24-hour format
- ✅ Lokalizovani datumi (Ponedeljak vs Monday)

### 🔋 **Battery Status:**
- ✅ Prikazuje se samo na laptopovima
- ✅ Različite ikonice: 🔌 (charging), 🔋 (full), 🪫 (low/critical)
- ✅ Dinamičke boje (zelena/bela/narandžasta/crvena)
- ✅ Real-time ažuriranje svakih 5 sekundi

### 🌧️ **Padavine (Precipitation):**
- ✅ Minutely_15 forecast (0-2h) za preciznost
- ✅ "Kiša SADA!" / "Sneg SADA!" upozorenja
- ✅ Predviđanje sa "Kiša za 15min" / "Snow in 15min"
- ✅ Precizni weather kodovi (71-77 = sneg, ostalo = kiša)

### 🕐 **Satna prognoza:**
- ✅ Prikazuje SLEDEĆI sat (trenutni je preskočen)
- ✅ Tooltip sa 12 budućih sati
- ✅ Ikonica, temperatura, verovatnoća padavina
- ✅ Automatska detekcija tipa padavina (kiša/sneg)

### 🌫️ **Air Quality:**
- ✅ European AQI standard
- ✅ Kategorije: Odličan/Dobar/Umeren/Loš/Veoma loš
- ✅ Tooltip sa detaljima: PM10, PM2.5, CO, NO₂, SO₂, O₃
- ✅ Dinamičke boje prema AQI nivou

### 🔄 **Sleep/Wake detekcija:**
- ✅ Detektuje laptop sleep/hibernate
- ✅ Čeka 30s pre prvog refresh-a posle wake-a
- ✅ Exponential backoff ako mreža nije spremna
- ✅ Ne ruši poslednje podatke tokom offline perioda

### 🎨 **UI Poboljšanja:**
- ✅ Konzistentne boje i font veličine
- ✅ Transparentne pozadine za sve labele
- ✅ Clickable labels sa hover efektima za tooltips
- ✅ Tamna tooltip tema

---

## 🐛 Bug Fixes

### v2.2.3:
- ✅ **KRITIČNO:** Windows Location sada radi (PowerShell implementacija)
- ✅ JSON parsing sa regex fallback-om za PowerShell whitespace
- ✅ Visibility API konzistentnost (uvek km, konverzija u mi kasnije)
- ✅ Precipitation API konzistentnost (uvek mm, konverzija u in kasnije)
- ✅ Wind speed API konzistentnost (m/s → km/h → mph)
- ✅ Automatski fallback na API location ako Windows Location nije dostupan

### v2.2.2:
- ✅ Visibility podatak sada dolazi iz `current` bloka (ne iz `hourly`)
- ✅ Pressure konzistentnost između Metric/Imperial
- ✅ Temperature_unit parameter u API pozivu

### v2.2.1:
- ✅ Precipitation unit konzistentnost
- ✅ Wind speed unit konzistentnost

### v2.2.0:
- ✅ Click-through mode sa Windows API transparent flag-om
- ✅ Widget-only mode sa tray-removal opcijom

---

## 🛠️ Tehnički detalji

### API korišćeni:
- **Weather:** [Open-Meteo](https://open-meteo.com/) (besplatno, bez API ključa)
- **Air Quality:** [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)
- **Geocoding:** [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)
- **Reverse Geocoding:** [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/)
- **IP Geolocation:** [ip-api.com](http://ip-api.com/)
- **Windows Location:** .NET System.Device.Location (via PowerShell)

### Arhitektura:
- **Framework:** PyQt5
- **Language:** Python 3.8+
- **Settings:** QSettings (persistent storage)
- **Networking:** requests library sa retry logikom
- **Sleep detection:** Timer-based sa exponential backoff

### Performanse:
- **Refresh rate:** 5-60 minuta (konfigurabilno)
- **Battery update:** Svakih 5 sekundi (samo laptop)
- **Clock update:** Svake sekunde
- **Memory footprint:** ~50-70 MB
- **CPU usage:** <1% (idle), ~5% (refresh)

---

## 📝 Licenca

MIT License - slobodno koristi, modifikuj i distribuiraj.

---

## 🤝 Doprinos

Pull requests su dobrodošli! Za velike izmene, prvo otvori issue da diskutujemo šta želiš da promeniš.

### Development setup:

```bash
# Clone repo
git clone https://github.com/malkosvetnik/Desktop-Weather-Widget.git
cd Desktop-Weather-Widget

# Install dependencies
pip install -r requirements.txt

# Run
python weather_widget_final.pyw
```

---

## 🙏 Zahvalnice

- [Open-Meteo](https://open-meteo.com/) za odličan besplatan Weather API
- [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) za reverse geocoding
- PyQt5 community za odličnu dokumentaciju
- Svim testerima i contributors-ima!

---

## 📞 Kontakt

- **GitHub:** [@malkosvetnik](https://github.com/malkosvetnik)
- **Project:** [Desktop Weather Widget](https://github.com/malkosvetnik/Desktop-Weather-Widget)

---

## 🔮 Planirane funkcionalnosti

- [ ] Skin system sa podrškom za custom dizajne
- [ ] Widget resize sa drag-and-drop
- [ ] Više API providera (AccuWeather, WeatherAPI)
- [ ] Notifikacije za ekstremno vreme
- [ ] Istorija vremena sa grafovima
- [ ] Export podataka u CSV/JSON

---

**Uživaj u widgetu! 🌤️**

---

*Version: 2.2.3 | Released: January 12, 2026*
