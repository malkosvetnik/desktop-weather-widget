# Contributing to Desktop Weather Widget

Hvala što razmišljaš o doprinosu! 🎉

## 🤝 Kako doprineti

### Prijavljivanje Bug-ova

Ako nađeš bug, otvori [Issue](https://github.com/malkosvetnik/desktop-weather-widget/issues) sa:

1. **Naslov** - Kratak opis problema
2. **Opis** - Detaljno objašnjenje šta ne radi
3. **Koraci za reprodukciju** - Kako da ponovo naiđem na problem
4. **Očekivano ponašanje** - Šta bi trebalo da se desi
5. **Actual behavior** - Šta se zapravo dešava
6. **Screenshots** - Ako je moguće
7. **Sistem info**:
   - OS verzija (npr. Windows 11)
   - Python verzija
   - PyQt5 verzija

### Predlaganje Features-a

Za nove features:
1. Proveri da već ne postoji [Issue](https://github.com/malkosvetnik/desktop-weather-widget/issues)
2. Otvori novi Issue sa:
   - Detaljnim opisom feature-a
   - Use case (zašto je potreban)
   - Moguću implementaciju (opciono)

### Pull Requests

1. **Fork** repo
2. **Clone** tvoj fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/desktop-weather-widget.git
   ```
3. **Kreiraj branch** za feature:
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Napravi izmene**
5. **Commit** sa jasnom porukom:
   ```bash
   git commit -m "Add: Amazing new feature"
   ```
6. **Push** na tvoj fork:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Otvori Pull Request** sa detaljima

## 📝 Code Style

### Python Code
- Koristi **4 spaces** za indentaciju (ne tabove)
- Prati [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Dodaj **docstrings** za funkcije
- Koristi **type hints** gde je moguće
- Dodaj **komentare** za kompleksnu logiku

### Primeri:

```python
def calculate_temperature(fahrenheit: float) -> float:
    """
    Konvertuje Fahrenheit u Celsius.
    
    Args:
        fahrenheit: Temperatura u Fahrenheit stepenima
        
    Returns:
        Temperatura u Celsius stepenima
    """
    return (fahrenheit - 32) * 5/9
```

### Commit Messages

Koristi **jasne i opisne** commit poruke:

✅ **Dobro:**
```
Add: Serbian translation for weather alerts
Fix: Tooltip positioning on high-DPI displays
Update: README with new features
```

❌ **Loše:**
```
fixed stuff
update
asdf
```

## 🧪 Testing

Pre Pull Request-a:
1. **Testiraj** sve nove features
2. **Proveri** da postojeće features još rade
3. **Pokreni** na različitim rezolucijama
4. **Testiraj** sa različitim lokacijama

## 📂 Project Structure

```
desktop-weather-widget/
├── weather_widget_final.pyw    # Main application
├── requirements.txt             # Dependencies
├── cleanup_registry.py          # Cleanup utility
├── README.md                    # Documentation
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # This file
├── LICENSE                      # MIT License
└── screenshots/                 # Screenshots folder
    ├── main_widget.png
    ├── alert_tooltip.png
    └── pollution_tooltip.png
```

## 🎯 Development Setup

```bash
# Clone
git clone https://github.com/malkosvetnik/desktop-weather-widget.git
cd desktop-weather-widget

# Install dependencies
pip install -r requirements.txt

# Run
python weather_widget_final.pyw
```

## 🐛 Debugging

Za debugging, koristi:
```python
print(f"🐛 DEBUG: {variable_name}")
```

Ili uključi verbose logging u kodu.

## 📋 TODO List

Proveri [Issues](https://github.com/malkosvetnik/desktop-weather-widget/issues) sa `good first issue` tag-om za lak start!

Trenutni prioriteti:
- [ ] Executable build (.exe)
- [ ] Puna engleska lokalizacija
- [ ] Custom themes
- [ ] Weather icon packs
- [ ] Mini mode

## ⚖️ License

Doprineći ovom projektu, slažeš se da će tvoj kod biti licenciran pod [MIT License](LICENSE).

## 💬 Pitanja?

Otvori [Discussion](https://github.com/malkosvetnik/desktop-weather-widget/discussions) ili Issue!

---

Hvala na doprinosu! 🙌
