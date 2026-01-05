# 🚀 WEATHER WIDGET v2.1.0 - UPLOAD PACKAGE

## 📦 Sadržaj paketa:

### Glavni fajlovi:
- `weather_widget.pyw` - Glavni widget fajl (spreman za upload)
- `README.md` - Dokumentacija projekta
- `CHANGELOG.md` - Lista promena za v2.1.0
- `RELEASE_NOTES.md` - Tekst za GitHub Release
- `requirements.txt` - Python dependencies

### Screenshot-ovi (`screenshots/` folder):
- `main_widget.png` - Widget na srpskom jeziku
- `main_widget_english.png` - Widget na engleskom jeziku ⭐ NOVA FIČURA
- `alert_tooltip.png` - Tooltip sa upozorenjima
- `pollution_tooltip.png` - Tooltip sa kvalitetom vazduha
- `tray_menu.png` - System tray menu
- `language_menu.png` - Language selection menu

---

## 🎯 UPLOAD PLAN - 3 KORAKA:

### Korak 1: Upload glavnih fajlova (5 minuta)

1. Idi na: https://github.com/malkosvetnik/desktop-weather-widget
2. Klikni: **"Add file" → "Upload files"**
3. Prevuci ove fajlove:
   - `weather_widget.pyw`
   - `README.md` (opciono - ako želiš da zaminieš stari)
   - `CHANGELOG.md`
   - `requirements.txt` (ako već nemaš)

4. **Commit message:**
   ```
   v2.1.0 - English language support + precipitation fixes
   ```

5. **Extended description:**
   ```
   - Added full English language translation
   - Fixed real-time precipitation detection
   - Fixed time rounding (1.9h → 2h)
   - Fixed translation issues
   - Improved error messages
   ```

6. Klikni **"Commit changes"**

---

### Korak 2: Upload screenshot-ova (3 minuta)

1. Idi u **`screenshots`** folder na GitHub-u (ili ga kreiraj ako ne postoji)
2. Klikni: **"Upload files"**
3. Prevuci SVE fajlove iz `screenshots/` foldera:
   - main_widget.png
   - main_widget_english.png
   - alert_tooltip.png
   - pollution_tooltip.png
   - tray_menu.png
   - language_menu.png

4. **Commit message:**
   ```
   Add v2.1.0 screenshots - English language support
   ```

5. Klikni **"Commit changes"**

---

### Korak 3: Kreiraj GitHub Release (5 minuta)

1. Idi na: https://github.com/malkosvetnik/desktop-weather-widget/releases
2. Klikni: **"Draft a new release"**

3. Popuni formu:

   **Choose a tag:** `v2.1.0` (create new tag)
   
   **Release title:** 
   ```
   🌤️ Weather Widget v2.1.0 - English Language Support
   ```

   **Description:** (kopiraj iz RELEASE_NOTES.md ili koristi ovo):
   ```markdown
   # 🌤️ Weather Widget v2.1.0

   ## 🌐 New Feature: Full English Language Support!

   The widget now speaks both Serbian and English! Switch languages via tray menu.

   ### What's New

   ✅ **Full English translation** - All UI, menus, tooltips, messages  
   ✅ **Real-time precipitation alerts** - Shows "Rain NOW!" when raining  
   ✅ **Accurate time calculations** - 1h 56min → "Rain in 2h" (was "1h")  
   ✅ **Proper translations** - All text translates correctly  
   ✅ **Better API data** - Requests rain/precipitation values  

   ### Screenshots

   <table>
   <tr>
   <td><img src="screenshots/main_widget_english.png" width="250"></td>
   <td><img src="screenshots/main_widget.png" width="250"></td>
   </tr>
   <tr>
   <td align="center"><b>English</b></td>
   <td align="center"><b>Serbian (Srpski)</b></td>
   </tr>
   </table>

   ### Installation

   ```bash
   pip install PyQt5 requests
   python weather_widget.pyw
   ```

   ### Full Changelog

   See [CHANGELOG.md](CHANGELOG.md) for complete list of changes.

   ---

   **Weather data by [Open-Meteo](https://open-meteo.com)**
   ```

4. **Attach binaries** (opciono):
   - Ako imaš .exe fajl, prevuci ga ovde

5. Klikni **"Publish release"**

---

## ✅ Finalna provera:

Nakon upload-a, proveri:

- [ ] Fajlovi vidljivi na GitHub-u
- [ ] Screenshot-ovi se otvaraju i prikazuju
- [ ] Release v2.1.0 kreiran
- [ ] README prikazuje screenshot-ove (ako si ga ažurirao)
- [ ] Tag v2.1.0 postoji

---

## 🎉 Gotovo!

Nakon upload-a:
1. ✅ Projekat je ažuriran na v2.1.0
2. ✅ Release je objavljen
3. ✅ Screenshot-ovi pokazuju nove fičure
4. ✅ Ljudi mogu da preuzmu i testiraju

---

## 📞 Pomoć

Ako imaš problema:
1. Proveri da li si ulogovan na GitHub
2. Proveri da li imaš write pristup repozitorijumu
3. Proveri da li su fajlovi ispod GitHub limite (100MB po fajlu)

---

**Srećno sa objavom! 🚀**

Made with ❤️ for malkosvetnik
