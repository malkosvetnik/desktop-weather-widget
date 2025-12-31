@echo off
echo ========================================
echo  KREIRANJE EXE FAJLA - Weather Widget
echo ========================================
echo.

echo [1/5] Proveravam PIL (Pillow) za kreiranje ikonice...
pip show pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo Pillow nije instaliran. Instaliram...
    pip install pillow
) else (
    echo Pillow je vec instaliran!
)

echo.
echo [2/5] Kreiram weather.ico fajl...
if exist weather.ico (
    echo weather.ico vec postoji, preskačem kreiranje.
) else (
    if exist create_icon.py (
        python create_icon.py
    ) else (
        echo ⚠️ create_icon.py ne postoji, preskačem ikonicu.
        echo EXE će biti bez custom ikonice.
    )
)

echo.
echo [3/5] Proveravam PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller nije instaliran. Instaliram...
    pip install pyinstaller
) else (
    echo PyInstaller je vec instaliran!
)

echo.
echo [4/5] Cistim stare build fajlove...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist weather_widget_final.spec del /q weather_widget_final.spec

echo.
echo [5/5] Kreiram EXE (bez DOS prozora, sa ikonicom)...
echo Molim sacekajte, ovo moze potrajati 1-2 minuta...
echo.

REM Proveri da li weather.ico postoji
if exist weather.ico (
    echo Koristim weather.ico kao ikonicu...
    pyinstaller --name="Weather Widget" ^
        --onefile ^
        --windowed ^
        --icon=weather.ico ^
        --noconsole ^
        weather_widget_final.pyw
) else (
    echo Ikonica ne postoji, kreiram EXE bez ikonice...
    pyinstaller --name="Weather Widget" ^
        --onefile ^
        --windowed ^
        --noconsole ^
        weather_widget_final.pyw
)

echo.
if exist "dist\Weather Widget.exe" (
    echo ========================================
    echo  USPESNO KREIRAN EXE!
    echo ========================================
    echo.
    echo EXE fajl: dist\Weather Widget.exe
    echo Velicina: 
    for %%A in ("dist\Weather Widget.exe") do echo %%~zA bytes
    echo.
    if exist weather.ico (
        echo Ikonica: weather.ico ✅
    ) else (
        echo Ikonica: Nema (default Python ikonica)
    )
    echo.
    echo Mozete sada pokrenuti: dist\Weather Widget.exe
    echo.
    echo NAPOMENA:
    echo - EXE nema DOS prozor (windowed mode)
    echo - Ima custom weather ikonicu
    echo - Kopirati Weather Widget.exe gde god hoces
    echo - Ostale fajlove (build, spec) mozes obrisati
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  GRESKA! EXE nije kreiran.
    echo ========================================
    echo Proveri da li weather_widget_final.pyw postoji.
)

echo.
pause
