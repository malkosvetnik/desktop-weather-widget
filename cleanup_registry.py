"""
Weather Widget - Registry Cleanup Utility
==========================================

This script completely removes all Weather Widget data from Windows Registry.
Use this for:
- Fresh installation
- Troubleshooting
- Complete uninstall

WARNING: This will delete all your settings including:
- API Key
- Widget position
- All preferences
"""

import winreg
import sys

def clean_weather_widget():
    """
    Potpuno briše sve podatke Weather Widget-a iz Windows Registry-ja.
    """
    print("🧹 Weather Widget - Registry Cleanup")
    print("=" * 50)
    print()
    
    cleaned = False
    
    # 1. Obriši glavne postavke
    try:
        # Prvo obriši Settings subkey
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\WeatherWidget\Settings")
            print("✅ Postavke obrisane (Settings)")
        except FileNotFoundError:
            pass
        
        # Onda obriši glavni key
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\WeatherWidget")
        print("✅ Glavni registry key obrisan (WeatherWidget)")
        cleaned = True
    except FileNotFoundError:
        print("ℹ️  Registry postavke ne postoje")
    except PermissionError:
        print("❌ GREŠKA: Pokreni kao Administrator!")
        return False
    except Exception as e:
        print(f"⚠️  Greška pri brisanju postavki: {e}")
    
    # 2. Obriši startup entry
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            r"Software\Microsoft\Windows\CurrentVersion\Run", 
            0, 
            winreg.KEY_WRITE
        )
        try:
            winreg.DeleteValue(key, "WeatherWidget")
            print("✅ Startup entry obrisan")
            cleaned = True
        except FileNotFoundError:
            print("ℹ️  Startup entry ne postoji")
        finally:
            winreg.CloseKey(key)
    except PermissionError:
        print("❌ GREŠKA: Pokreni kao Administrator!")
        return False
    except Exception as e:
        print(f"⚠️  Greška pri brisanju startup-a: {e}")
    
    print()
    if cleaned:
        print("🎉 Čišćenje uspešno!")
        print()
        print("Sledeći podaci su obrisani:")
        print("  - API Key")
        print("  - Pozicija widgeta")
        print("  - Veličina widgeta")
        print("  - Lokacija")
        print("  - Sve postavke")
        print("  - Startup entry")
        print()
        print("Pri sledećem pokretanju, aplikacija će biti kao nova instalacija.")
    else:
        print("ℹ️  Nema šta da se obriše - već čisto!")
    
    return True

def verify_cleanup():
    """
    Proveri da li je čišćenje uspešno.
    """
    print()
    print("🔍 Verifikacija...")
    print()
    
    all_clean = True
    
    # Proveri glavni key
    try:
        winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\WeatherWidget")
        print("⚠️  WeatherWidget key još postoji!")
        all_clean = False
    except FileNotFoundError:
        print("✅ WeatherWidget key ne postoji")
    
    # Proveri startup
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run"
        )
        try:
            winreg.QueryValueEx(key, "WeatherWidget")
            print("⚠️  Startup entry još postoji!")
            all_clean = False
        except FileNotFoundError:
            print("✅ Startup entry ne postoji")
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        print(f"⚠️  Greška pri proveri: {e}")
    
    print()
    if all_clean:
        print("✅ Sve je potpuno očišćeno!")
    else:
        print("⚠️  Nešto nije obrisano - pokušaj ponovo kao Administrator")
    
    return all_clean

if __name__ == "__main__":
    print()
    response = input("Da li si siguran da želiš da obrišeš SVE podatke? (da/ne): ")
    
    if response.lower() in ['da', 'yes', 'y']:
        print()
        success = clean_weather_widget()
        
        if success:
            verify_cleanup()
        
        print()
        print("=" * 50)
    else:
        print()
        print("❌ Otkazano - ništa nije obrisano")
    
    print()
    input("Pritisni Enter za izlaz...")
