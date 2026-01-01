# 🚀 GitHub Update Instructions

Step-by-step uputstvo za upload nove verzije na GitHub.

## 📋 Pre nego što počneš

Proveri da imaš:
- ✅ Git instaliran
- ✅ GitHub nalog
- ✅ Repo: https://github.com/malkosvetnik/desktop-weather-widget

---

## 🔄 Metoda 1: Command Line (Preporučeno)

### 1. Otvori Git Bash ili Command Prompt

### 2. Navigiraj do tvog lokalnog repo foldera:
```bash
cd path/to/desktop-weather-widget
```

### 3. Proveri trenutni status:
```bash
git status
```

### 4. Kopiraj nove fajlove u repo:

Zameni stare fajlove sa novim:
- `weather_widget_final.pyw` → Glavni fajl
- `README.md` → Ažurirani README
- `CHANGELOG.md` → Novi fajl
- `CONTRIBUTING.md` → Novi fajl
- `LICENSE` → Novi fajl
- `.gitignore` → Novi fajl
- `cleanup_registry.py` → Novi fajl

### 5. Dodaj sve izmene:
```bash
git add .
```

### 6. Commit sa jasnom porukom:
```bash
git commit -m "Version 2.0.0 - Advanced Features Update

- Add dynamic alert colors (green/yellow/red)
- Add interactive tooltips for alerts and pollution
- Add complete Serbian translation
- Add precise hourly precipitation alerts
- Add smart text formatting (auto font-sizing)
- Improve sleep/wake detection
- Fix translation bugs
- Update documentation"
```

### 7. Push na GitHub:
```bash
git push origin main
```
(ili `master` ako je tvoj branch `master`)

---

## 🖱️ Metoda 2: GitHub Web Interface

### 1. Idi na tvoj repo:
https://github.com/malkosvetnik/desktop-weather-widget

### 2. Za svaki fajl:

#### Postojeći fajlovi (weather_widget_final.pyw, README.md):
1. Klikni na fajl
2. Klikni **Edit** (olovka ikona)
3. Obriši stari sadržaj
4. Kopiraj/paste novi sadržaj
5. Scroll dole, dodaj commit message: `Update to version 2.0.0`
6. Klikni **Commit changes**

#### Novi fajlovi (CHANGELOG.md, CONTRIBUTING.md, LICENSE, itd.):
1. Klikni **Add file** > **Create new file**
2. Unesi ime fajla (npr. `CHANGELOG.md`)
3. Kopiraj/paste sadržaj
4. Scroll dole, dodaj commit message: `Add CHANGELOG for version 2.0.0`
5. Klikni **Commit new file**

---

## 🏷️ Kreiranje Release-a (Opciono ali preporučeno)

### 1. Idi na Releases:
https://github.com/malkosvetnik/desktop-weather-widget/releases

### 2. Klikni **Draft a new release**

### 3. Popuni:
- **Tag version**: `v2.0.0`
- **Release title**: `Version 2.0.0 - Advanced Features`
- **Description**: Kopiraj iz CHANGELOG.md

```markdown
## 🎉 Major Update - Advanced Features

### New Features
- 🎨 Dynamic Alert Colors (green/yellow/red based on severity)
- 🖱️ Interactive Tooltips for Weather Alerts
- 🌧️ Precise Hourly Precipitation Alerts
- 🇷🇸 Complete Serbian Translation
- 📏 Smart Text Formatting with Auto Font-Sizing

### Improvements
- Better sleep/wake detection
- Enhanced API error handling
- Improved location detection
- UI consistency upgrades

### Bug Fixes
- Translation bugs in alert descriptions
- Font size consistency
- Tooltip positioning issues

See [CHANGELOG.md](CHANGELOG.md) for full details.
```

### 4. Attach files (opciono):
- Možeš priložiti `.exe` ako napraviš build

### 5. Klikni **Publish release**

---

## ✅ Provera

Nakon upload-a, proveri:
1. ✅ Svi fajlovi su ažurirani
2. ✅ README se pravilno prikazuje
3. ✅ Links rade
4. ✅ Screenshots se vide (ako si dodao)
5. ✅ Release je kreiran (ako si ga pravio)

---

## 🎯 Dodatni Koraci (Opciono)

### Dodaj Screenshots:

1. **Kreiraj `screenshots` folder:**
```bash
mkdir screenshots
```

2. **Dodaj screenshot-e:**
- `main_widget.png` - Glavni widget
- `alert_tooltip.png` - Tooltip za upozorenja
- `pollution_tooltip.png` - Tooltip za zagađenje

3. **Upload na GitHub:**
```bash
git add screenshots/
git commit -m "Add screenshots"
git push
```

### Kreiraj .exe Build (za release):

Koristi PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico weather_widget_final.pyw
```

Upload `dist/weather_widget_final.exe` u GitHub Release.

---

## 🆘 Problemi?

### "Permission denied"
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### "Nothing to commit"
Proveri da si zaista kopirao nove fajlove u repo folder.

### "Conflict"
```bash
git pull origin main
# Reši konflikte ručno
git add .
git commit -m "Resolve conflicts"
git push origin main
```

---

## 📞 Help

Ako zapneš, otvori Issue na GitHub-u ili proveri [Git dokumentaciju](https://git-scm.com/doc).

---

**Happy coding!** 🎉
