# 🌤️ Desktop Weather Widget

Elegantan, funkcionalan desktop weather widget za Windows sa transparentnim pozadinama, live podacima i naprednim features-ima.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎨 Core Features
- ⏰ **Real-time Clock** - Sat koji se ažurira svake sekunde
- 🌡️ **Current Weather** - Trenutna temperatura, oseća se kao, vlažnost
- 💨 **Wind Information** - Brzina vetra sa pravcem (S, SI, I, JI, J, JZ, Z, SZ)
- 🌅 **Sun Times** - Vreme izlaska i zalaska sunca
- 📊 **Atmospheric Data** - Pritisak, oblačnost, vidljivost
- ☀️ **UV Index** - Sa color-coded indikatorom
- 🌫️ **Air Quality (AQI)** - Kvalitet vazduha sa detaljnim polutantima
- 📅 **5-Day Forecast** - Prognoza za narednih 5 dana

### 🆕 Advanced Features
- 🎨 **Dynamic Alert Colors** - Upozorenja menjaju boju prema nivou opasnosti:
  - 🟢 Zeleno - Bez upozorenja
  - 🟡 Žuto - Standardna upozorenja
  - 🔴 Crveno - Ekstremna upozorenja
- 🌧️ **Precipitation Alerts** - Precizne informacije o padavinama (na sat tačno)
- ⚠️ **Weather Alerts** - Vremenska upozorenja sa tooltip-ima
- 🖱️ **Interactive Tooltips** - Hover preko zagađenja ili upozorenja za detalje
- 🇷🇸 **Serbian Translation** - Potpun prevod svih tekstova i upozorenja
- 📏 **Smart Text Formatting** - Automatsko prilagođavanje veličine fonta
- 🔄 **Auto-refresh** - Postavke od 5-60 minuta
- 💾 **Persistent Settings** - Automatsko čuvanje pozicije i postavki

### ⚙️ Customization
- 📍 **Auto-location ili Manual** - GPS bazirana ili ručna lokacija
- 🔒 **Lock Position** - Zaključaj poziciju widgeta
- 👻 **Click-through Mode** - Widget ne blokira klikove
- 🚀 **Startup with Windows** - Automatsko pokretanje
- 📐 **Multi-resolution Support** - Predefinirane veličine za sve ekrane (XGA do 8K)
- 🎯 **Always-on-Bottom** - Widget uvek ispod prozora

## 📸 Screenshots

![Main Widget](screenshots/main_widget.png)
*Glavni interfejs sa svim informacijama*

![Tray Menu](screenshots/tray_menu.png)
*Tray menu sa svim opcijama*

![Alert Tooltip](screenshots/alert_tooltip.png)
*Detaljan tooltip za upozorenja sa vremenom trajanja*

![Pollution Details](screenshots/pollution_tooltip.png)
*Detaljni podaci o zagađenju vazduha (CO, NO₂, O₃, SO₂, PM2.5, PM10, NH₃)*

## 🚀 Installation

### Prerequisites
- Python 3.8 ili noviji
- Windows 10/11
- OpenWeatherMap API key (besplatan)

### Setup

1. **Clone repository:**
```bash
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Get FREE OpenWeatherMap API Key:**
   - Idi na [OpenWeatherMap](https://openweathermap.org/api)
   - Napravi besplatan nalog
   - Kopiraj svoj API key
   - Aplikacija će te pitati za API key pri prvom pokretanju

4. **Run the widget:**
```bash
python weather_widget_final.pyw
```

## 🔧 Configuration

### First Run
Pri prvom pokretanju aplikacija će:
1. Zatražiti OpenWeatherMap API key
2. Postaviti podrazumevanu lokaciju (Belgrade)
3. Omogućiti auto-lokaciju

### Settings (Tray Menu)
- **Refresh Interval** - 5/10/15/30/60 minuta
- **Resolution Preset** - Optimizovane veličine za tvoj ekran
- **Click-Through Mode** - Omogući klikove kroz widget
- **Lock Position** - Zaključaj widget na mestu
- **Startup with Windows** - Automatsko pokretanje

### Manual Configuration
Podešavanja se čuvaju u Windows Registry:
```
HKEY_CURRENT_USER\Software\WeatherWidget
```

Za potpuno brisanje:
```cmd
reg delete "HKCU\Software\WeatherWidget" /f
```

## 📋 Requirements

```txt
PyQt5>=5.15.0
requests>=2.31.0
```

## 🎯 Usage Tips

### Interactive Features
- **Hover over AQI** - Prikaži detaljne podatke o polutantima (CO, NO₂, O₃, SO₂, PM2.5, PM10, NH₃)
- **Hover over Alerts** - Prikaži pun tekst upozorenja sa trajanjem i opisom
- **Double-click tray icon** - Prikaži/sakrij widget
- **Drag widget** - Pomeri na novu poziciju (kad nije zaključan)

### Keyboard Shortcuts
Trenutno nisu implementirani - sve kontrole kroz GUI

## 🌍 Supported Languages
- 🇷🇸 **Serbian (Latinica)** - Glavni jezik
- 🇬🇧 English - API fallback

## 🐛 Known Issues

- **One Call API 3.0** - Weather alerts zahtevaju plaćenu pretplatu ($40/mesec)
  - Bez pretplate, widget će raditi ali bez detaljnih upozorenja
- **API Activation** - Novi API key može da traje 10-15 minuta za aktivaciju
- **Sleep/Wake** - Widget čeka 30s nakon buđenja pre osvežavanja

## 🔮 Roadmap

- [ ] Executable (.exe) build
- [ ] Multi-language support (pun engleski)
- [ ] Custom themes
- [ ] Weather icons
- [ ] Mini mode (kompaktna verzija)
- [ ] Widget na više monitora

## 🤝 Contributing

Pull requests su dobrodošli! Za velike izmene, prvo otvori issue da diskutujemo šta želiš da promeniš.

### Development Setup
```bash
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget
pip install -r requirements.txt
python weather_widget_final.pyw
```

## 📝 License

[MIT License](LICENSE)

## 👨‍💻 Author

**Marko Svetnik**
- GitHub: [@malkosvetnik](https://github.com/malkosvetnik)

## 🙏 Acknowledgments

- Weather data powered by [OpenWeatherMap API](https://openweathermap.org/)
- Built with [PyQt5](https://riverbankcomputing.com/software/pyqt/)
- Icons: Unicode emoji

## 📞 Support

Ako naiđeš na probleme:
1. Proveri [Issues](https://github.com/malkosvetnik/desktop-weather-widget/issues)
2. Otvori novi Issue sa detaljima
3. Uključi verziju Python-a i OS-a

---

⭐ **Ako ti se dopada projekat, ostavi star!** ⭐
