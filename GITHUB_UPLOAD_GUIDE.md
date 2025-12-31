# 🚀 GITHUB UPLOAD GUIDE - Korak po Korak

## 📦 ŠTA IMAŠ SPREMNO:

✅ `weather_widget_final.py` - Main source code  
✅ `create_icon.py` - Icon generator  
✅ `build_exe.bat` - EXE builder  
✅ `README.md` - Main documentation  
✅ `INSTALLATION.md` - Setup guide  
✅ `CONTRIBUTING.md` - Contributor guide  
✅ `RELEASE_NOTES.md` - v1.0.0 changelog  
✅ `LICENSE` - MIT License  
✅ `requirements.txt` - Dependencies  
✅ `.gitignore` - Git ignore rules  
✅ `.github/ISSUE_TEMPLATE/` - Issue templates  

---

## 🎯 KORACI ZA UPLOAD:

### 1️⃣ KREIRAJ GITHUB REPO

1. Idi na https://github.com/new
2. **Repository name:** `desktop-weather-widget`
3. **Description:** `🌤️ Beautiful desktop weather widget for Windows - Better than Microsoft's built-in!`
4. **Public** ✅
5. **DON'T** initialize with README (već imaš)
6. Klikni **"Create repository"**

---

### 2️⃣ PRIPREMI LOKALNI FOLDER

```bash
# Kreiraj novi folder
mkdir C:\weather-widget-github
cd C:\weather-widget-github

# Kopiraj sve fajlove iz outputs foldera u ovaj folder
# (drag & drop iz /mnt/user-data/outputs/)
```

**Struktura treba da bude:**
```
C:\weather-widget-github\
├── weather_widget_final.py
├── create_icon.py
├── build_exe.bat
├── README.md
├── INSTALLATION.md
├── CONTRIBUTING.md
├── RELEASE_NOTES.md
├── LICENSE
├── requirements.txt
├── .gitignore
└── .github/
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

### 3️⃣ GIT SETUP (Ako nemaš Git instaliran)

**Download Git:**
https://git-scm.com/download/win

**Install**, pa nastavi...

---

### 4️⃣ UPLOAD NA GITHUB

```bash
# Otvori Command Prompt u C:\weather-widget-github
cd C:\weather-widget-github

# Initialize git repo
git init

# Add all files
git add .

# Commit
git commit -m "🎉 Initial release v1.0.0 - Desktop Weather Widget"

# Dodaj remote (PROMENI YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/desktop-weather-widget.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### 5️⃣ DODAJ SCREENSHOTS (VAŽNO!)

1. Napravi **screenshots** widgeta:
   - Full widget view
   - Tooltip sa polutantima
   - Tray menu
   - API key dialog

2. Kreiraj folder `screenshots/` u repo-u

3. Upload screenshots:
```bash
git add screenshots/
git commit -m "📸 Add screenshots"
git push
```

4. **Izmeni README.md** da uključi slike:
```markdown
## 📸 Screenshots

![Widget Overview](screenshots/widget-overview.png)
![Air Quality Tooltip](screenshots/tooltip.png)
![Tray Menu](screenshots/tray-menu.png)
```

---

### 6️⃣ KREIRAJ RELEASE (EXE)

**VAŽNO:** Prvo napravi EXE!

```bash
# Pokreni build_exe.bat
build_exe.bat

# EXE će biti u dist/ folderu
```

**Upload release:**

1. Idi na GitHub repo → **"Releases"** tab
2. Klikni **"Create a new release"**
3. **Tag:** `v1.0.0`
4. **Title:** `🌤️ Desktop Weather Widget v1.0.0`
5. **Description:** Copy-paste iz `RELEASE_NOTES.md`
6. **Attach files:**
   - ZIP ceo `dist/` folder → `Weather-Widget-v1.0.0.zip`
7. Klikni **"Publish release"** 🚀

---

### 7️⃣ UPDATE README SA TVOJIM INFO

**Otvori README.md i zameni:**

- `YOUR_USERNAME` → tvoj GitHub username
- `[Your Name]` → tvoje ime
- `[Your Email]` → tvoj email (optional)
- Dodaj screenshots linkove

**Commit:**
```bash
git add README.md
git commit -m "📝 Update README with personal info"
git push
```

---

### 8️⃣ DODAJ TOPICS (GitHub Tags)

1. Idi na GitHub repo
2. Klikni **⚙️ Settings** → General
3. Scroll do **"Topics"**
4. Dodaj:
   ```
   python, pyqt5, weather, desktop-widget, 
   windows, weather-api, openweathermap, 
   transparent-widget, desktop-app, serbian
   ```

---

### 9️⃣ DODAJ GITHUB ACTIONS (Optional - za CI/CD)

Kasnije možeš dodati GitHub Actions za automatsko testiranje!

---

### 🔟 SHARE NA SOCIAL MEDIA!

**Reddit:**
- r/Python
- r/opensource
- r/serbia 🇷🇸

**Post template:**
```
🌤️ I built a Desktop Weather Widget (better than Windows')

After getting frustrated with Microsoft's weather widget, 
I built my own in Python!

Features:
✅ 11 weather parameters (UV, AQI, wind direction)
✅ 5-day forecast
✅ Air quality with 7 pollutants
✅ Resolution scaling (XGA to 8K)
✅ Serbian language support
✅ Click-through mode
✅ Only 60-80MB RAM, 0.1% CPU

GitHub: [link]
Screenshots: [link]

Built with PyQt5 + OpenWeatherMap API
Completely free & open-source!

Feedback welcome! 🚀
```

---

## ✅ CHECKLIST PRE OBJAVE:

- [ ] Svi fajlovi kopirani u folder
- [ ] Git repo kreiran na GitHub
- [ ] Fajlovi pushed na GitHub
- [ ] Screenshots dodati
- [ ] README.md ažuriran sa tvojim info
- [ ] EXE napravljen
- [ ] Release kreiran sa ZIP-om
- [ ] Topics dodati
- [ ] LICENSE ima tvoje ime
- [ ] Sve testirao lokalno

---

## 🎉 READY TO GO!

Kad završiš sve korake:

1. **Proveri repo:** https://github.com/YOUR_USERNAME/desktop-weather-widget
2. **Deli link** sa prijateljima
3. **Post na Reddit/Twitter**
4. **Čekaj stars!** ⭐

---

## 📞 Ako Zaglavi:

- Git error? Google: "git [error message]"
- Upload failed? Check internet connection
- Can't create release? Make sure you have EXE first

**Javi mi ako treba pomoć!** 💪

---

**GOOD LUCK!** 🚀🌟
