import sys
import requests
import json
import os
import re
import socket
import time
import winreg
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QSystemTrayIcon,
                             QMenu, QAction, QLineEdit, QComboBox, QMessageBox, QToolTip,
                             QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer, QPoint, QSettings, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QCursor

# ✅ Import za battery status
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil nije instaliran - battery status neće biti dostupan")



# Klasa za klikabilni label (za tooltip)
class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Signal mora biti definisan NA NIVOU KLASE

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self.tooltip_visible = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("🖱️ ClickableLabel: MousePress detected!")
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        # Prikaži tooltip odmah kad uđeš
        if not self.tooltip_visible:
            self.tooltip_visible = True
            self.clicked.emit()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        # Sakrij tooltip kad izađeš
        if self.tooltip_visible:
            self.tooltip_visible = False
            QToolTip.hideText()
        super().leaveEvent(event)


class WeatherWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # Online/offline status (ne ruši widget kad nema interneta)
        self.is_online = True

        # QSettings za čuvanje postavki
        self.settings = QSettings('WeatherWidget', 'Settings')

        # Inicijalizuj click_through ODMAH (pre initUI)
        self.click_through = False
        self.widget_locked = False
        self.widget_visible = True
        self.startup_mode = False
        self.current_temp = "--"
        self.pollutants_data = {}  # Za čuvanje detaljnih polutanata
        self.weather_alerts = []  # Za čuvanje upozorenja
        self.hourly_forecast = []  # Za čuvanje satne prognoze
        self.hourly_forecast_data = []  # ✅ Za tooltip satne prognoze
        self.full_alert_text = ""  # ✅ Pun tekst upozorenja za tooltip
        self.current_language = "en"  # ✅ Default jezik: English (will be loaded from settings)
        self.temperature_unit = self.settings.value('temperature_unit', 'celsius', type=str)  # ✅ 'celsius' ili 'fahrenheit'
        self.time_format = self.settings.value('time_format', '24h', type=str)  # ✅ '12h' ili '24h'
        self.unit_system = self.settings.value('unit_system', 'metric', type=str)  # ✅ 'metric' ili 'imperial'
        self.location_source = self.settings.value('location_source', 'api', type=str)  # ✅ 'api' ili 'windows'
        # ✅ Prevent repeated popups if Windows Location is turned off while widget is running
        self._windows_location_warning_shown = False
        
        # ✅ Translation dictionary
        self.translations = {
            "sr": {
                # UI Elements - Static Labels
                "refresh_interval": "Osvežavanje:",
                "search_placeholder": "Unesi grad...",
                "feels_like": "Oseća se kao",
                "humidity": "Vlažnost",
                "wind": "Vetar",
                "uv_index": "☀️ UV Index",
                "air_quality": "🌫️ Zagađenje",
                "pressure": "📊 Pritisak",
                "cloudiness": "☁️ Oblačnost",
                "visibility": "👁️ Vidljivost",
                "sunrise": "🌅 Izlazak",
                "sunset": "🌇 Zalazak",

                # Status text
                "last_updated_fmt": "🕒 Poslednje ažuriranje: {}",
                "offline_waiting": "🌐 offline – čekam internet",
                "sleep_detected": "💤 sleep detektovan",
                # Buttons & Actions
                "auto_location": "📍 Auto",
                "unlock": "🔓 Otključaj",
                "lock": "🔒 Zaključaj",
                
                # Location search
                "location_search": "Pretraga lokacije...",
                "hourly_forecast_title": "🕐 SATNA PROGNOZA",
                "precipitation_title": "🌧️ PADAVINE",
                "forecast_5day_title": "Prognoza za 5 dana",
                "no_forecast": "Nema prognoze",
                "no_data": "Nema podataka",
                "loading": "Učitavam...",
                "error": "Greška",
                "refresh": "Osvežavam...",
                "computer_woke": "Računar se probudio, čekam 30s...",
                "waiting_network": "Čekam network...",
                "no_connection": "Nema konekcije",
                
                # Weather descriptions
                "clear": "vedro",
                "mostly_clear": "pretežno vedro",
                "partly_cloudy": "delimično oblačno",
                "cloudy": "oblačno",
                "fog": "magla",
                "fog_frost": "magla sa mrazom",
                "light_rain": "slaba kiša",
                "rain": "kiša",
                "heavy_rain": "jaka kiša",
                "freezing_rain": "ledena kiša",
                "heavy_freezing_rain": "jaka ledena kiša",
                "light_snow": "slab sneg",
                "snow": "sneg",
                "heavy_snow": "jak sneg",
                "snow_grains": "snežne pahulje",
                "light_showers": "slabi pljuskovi",
                "showers": "pljuskovi",
                "heavy_showers": "jaki pljuskovi",
                "snow_showers": "snežni pljuskovi",
                "thunderstorm": "oluja",
                "thunderstorm_hail": "oluja sa gradom",
                "heavy_thunderstorm_hail": "jaka oluja sa gradom",
                
                # Days of week
                "monday": "Pon",
                "tuesday": "Uto",
                "wednesday": "Sre",
                "thursday": "Čet",
                "friday": "Pet",
                "saturday": "Sub",
                "sunday": "Ned",
                
                # Months
                "january": "januar",
                "february": "februar",
                "march": "mart",
                "april": "april",
                "may": "maj",
                "june": "jun",
                "july": "jul",
                "august": "avgust",
                "september": "septembar",
                "october": "oktobar",
                "november": "novembar",
                "december": "decembar",
                
                # Precipitation alerts
                "rain_now": "Kiša SADA!",
                "rain_in": "Kiša za",
                "snow_now": "Sneg SADA!",
                "snow_in": "Sneg za",
                "storm_now": "Oluja SADA!",
                "storm_in": "Oluja za",
                "no_precipitation": "Nema padavina",
                "rain_today": "Kiša SADA!",
                
                # Tooltips
                "pollutants_title": "Detaljni polutanti:",
                "hourly_forecast_tooltip": "Prognoza za narednih 12h:",
                "hover_for_details": "Hover na ikonicu za detalje",
                
                # Pollutant names
                "carbon_monoxide": "Ugljen-monoksid",
                "nitrogen_dioxide": "Azot-dioksid",
                "ozone": "Ozon",
                "sulfur_dioxide": "Sumpor-dioksid",
                "fine_particles": "Fine čestice",
                "coarse_particles": "Krupne čestice",
                "ammonia": "Amonijak",
                
                # AQI Categories
                "aqi_excellent": "Odličan",
                "aqi_good": "Dobar",
                "aqi_moderate": "Srednji",
                "aqi_poor": "Loš",
                "aqi_very_poor": "V. loš",
                
                # Temperature units
                "temperature_unit": "Jedinica temperature:",
                "celsius": "Celzijus (°C)",
                "fahrenheit": "Farenhajt (°F)",
                
                # Time format
                "time_format": "Format vremena:",
                "time_12h": "12-satni (AM/PM)",
                "time_24h": "24-satni",
                
                # Unit system
                "unit_system": "Sistem merenja:",
                "metric": "Metrički (km/h, mbar)",
                "imperial": "Imperijalni (mph, inHg)",
                
                # Tray Menu
                "tray_show": "Prikaži Widget",
                "tray_startup": "✓ Pokreni sa Windows-om",
                "tray_widget_only": "Samo Widget (bez tray-a)",
                "tray_click_through": "Click-Through Mode",
                "tray_resolution": "Rezolucija Monitora",
                "tray_refresh": "Osveži Vreme",
                "tray_location_source": "📍 Izvor Lokacije",
                "location_api": "API Lokacija",
                "location_windows": "Windows Lokacija",
                "tray_exit": "Izađi",
                
                # Startup notifications
                "startup_enabled_title": "Startup",
                "startup_enabled_msg": "Aplikacija će se pokretati sa Windows-om",
                "startup_disabled_title": "Startup",
                "startup_disabled_msg": "Uklonjena iz startup-a",
                
                # Click-through notifications
                "clickthrough_enabled_title": "Click-Through Aktivan",
                "clickthrough_enabled_msg": "Klikovi prolaze kroz widget",
                "clickthrough_disabled_title": "Click-Through Isključen",
                "clickthrough_disabled_msg": "Widget je sada klikabilan",
                
                # Language change notifications
                "lang_changed_title": "Jezik Promenjen",
                "lang_changed_msg_sr": "Widget je sada na: Srpski",
                "lang_changed_msg_en": "Widget je sada na: English"
            },
            "en": {
                # UI Elements - Static Labels
                "refresh_interval": "Refresh:",
                "search_placeholder": "Enter city...",
                "feels_like": "Feels like",
                "humidity": "Humidity",
                "wind": "Wind",
                "uv_index": "☀️ UV Index",
                "air_quality": "🌫️ Air Quality",
                "pressure": "📊 Pressure",
                "cloudiness": "☁️ Cloudiness",
                "visibility": "👁️ Visibility",
                "sunrise": "🌅 Sunrise",
                "sunset": "🌇 Sunset",

                # Status text
                "last_updated_fmt": "🕒 Last updated: {}",
                "offline_waiting": "🌐 offline – waiting for internet",
                "sleep_detected": "💤 sleep detected",
                # Buttons & Actions
                "auto_location": "📍 Auto",
                "unlock": "🔓 Unlock",
                "lock": "🔒 Lock",
                
                # Location search
                "location_search": "Search location...",
                "hourly_forecast_title": "🕐 HOURLY FORECAST",
                "precipitation_title": "🌧️ PRECIPITATION",
                "forecast_5day_title": "5-Day Forecast",
                "no_forecast": "No forecast",
                "no_data": "No data",
                "loading": "Loading...",
                "error": "Error",
                "refresh": "Refreshing...",
                "computer_woke": "Computer woke up, waiting 30s...",
                "waiting_network": "Waiting for network...",
                "no_connection": "No connection",
                
                # Weather descriptions
                "clear": "clear",
                "mostly_clear": "mostly clear",
                "partly_cloudy": "partly cloudy",
                "cloudy": "cloudy",
                "fog": "fog",
                "fog_frost": "fog with frost",
                "light_rain": "light rain",
                "rain": "rain",
                "heavy_rain": "heavy rain",
                "freezing_rain": "freezing rain",
                "heavy_freezing_rain": "heavy freezing rain",
                "light_snow": "light snow",
                "snow": "snow",
                "heavy_snow": "heavy snow",
                "snow_grains": "snow grains",
                "light_showers": "light showers",
                "showers": "showers",
                "heavy_showers": "heavy showers",
                "snow_showers": "snow showers",
                "thunderstorm": "thunderstorm",
                "thunderstorm_hail": "thunderstorm with hail",
                "heavy_thunderstorm_hail": "heavy thunderstorm with hail",
                
                # Days of week
                "monday": "Mon",
                "tuesday": "Tue",
                "wednesday": "Wed",
                "thursday": "Thu",
                "friday": "Fri",
                "saturday": "Sat",
                "sunday": "Sun",
                
                # Months
                "january": "January",
                "february": "February",
                "march": "March",
                "april": "April",
                "may": "May",
                "june": "June",
                "july": "July",
                "august": "August",
                "september": "September",
                "october": "October",
                "november": "November",
                "december": "December",
                
                # Precipitation alerts
                "rain_now": "Rain NOW!",
                "rain_in": "Rain in",
                "snow_now": "Snow NOW!",
                "snow_in": "Snow in",
                "storm_now": "Storm NOW!",
                "storm_in": "Storm in",
                "no_precipitation": "No precipitation",
                "rain_today": "Rain NOW!",
                
                # Tooltips
                "pollutants_title": "Detailed pollutants:",
                "hourly_forecast_tooltip": "Forecast for next 12h:",
                "hover_for_details": "Hover on icon for details",
                
                # Pollutant names
                "carbon_monoxide": "Carbon monoxide",
                "nitrogen_dioxide": "Nitrogen dioxide",
                "ozone": "Ozone",
                "sulfur_dioxide": "Sulfur dioxide",
                "fine_particles": "Fine particles",
                "coarse_particles": "Coarse particles",
                "ammonia": "Ammonia",
                
                # AQI Categories
                "aqi_excellent": "Excellent",
                "aqi_good": "Good",
                "aqi_moderate": "Moderate",
                "aqi_poor": "Poor",
                "aqi_very_poor": "V. Poor",
                
                # Temperature units
                "temperature_unit": "Temperature Unit:",
                "celsius": "Celsius (°C)",
                "fahrenheit": "Fahrenheit (°F)",
                
                # Time format
                "time_format": "Time Format:",
                "time_12h": "12-hour (AM/PM)",
                "time_24h": "24-hour",
                
                # Unit system
                "unit_system": "Measurement Units:",
                "metric": "Metric (km/h, mbar)",
                "imperial": "Imperial (mph, inHg)",
                
                # Tray Menu
                "tray_show": "Show Widget",
                "tray_startup": "✓ Run at Windows Startup",
                "tray_widget_only": "Widget Only (no tray)",
                "tray_click_through": "Click-Through Mode",
                "tray_resolution": "Monitor Resolution",
                "tray_refresh": "Refresh Weather",
                "tray_location_source": "📍 Location Source",
                "location_api": "API Location",
                "location_windows": "Windows Location",
                "tray_exit": "Exit",
                
                # Startup notifications
                "startup_enabled_title": "Startup",
                "startup_enabled_msg": "App will run at Windows startup",
                "startup_disabled_title": "Startup",
                "startup_disabled_msg": "Removed from startup",
                
                # Click-through notifications
                "clickthrough_enabled_title": "Click-Through Enabled",
                "clickthrough_enabled_msg": "Clicks pass through widget",
                "clickthrough_disabled_title": "Click-Through Disabled",
                "clickthrough_disabled_msg": "Widget is now clickable",
                
                # Language change notifications
                "lang_changed_title": "Language Changed",
                "lang_changed_msg_sr": "Widget is now in: Serbian",
                "lang_changed_msg_en": "Widget is now in: English"
            }
        }

        # Open-Meteo ne zahteva API key! 🎉
        self.current_location = "Belgrade"
        self.use_auto_location = True

        # Kreiraj persistent session za requests
        self.session = requests.Session()

        # Učitaj sačuvane postavke
        self.loadSettings()

        # Timer za sat
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.updateClock)
        self.clock_timer.start(1000)
        
        # ✅ Timer za battery status (svaki 30 sekundi)
        if PSUTIL_AVAILABLE:
            self.battery_timer = QTimer()
            self.battery_timer.timeout.connect(self.updateBatteryStatus)
            self.battery_timer.start(30000)  # Update every 30 seconds

        self.initUI()
        self.initTray()
        
        # ✅ Update language menu checkmarks based on loaded language
        for code, action in self.language_actions.items():
            action.setChecked(code == self.current_language)
        
        # ✅ Update UI to loaded language before first weather update
        self.updateLanguageUI()

        # Učitaj poziciju
        self.restorePosition()

        self.updateWeather()
        
        # ✅ Inicijalna provera battery statusa
        if PSUTIL_AVAILABLE:
            self.updateBatteryStatus()

        # Timer za automatsko ažuriranje
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateWeather)
        self.refresh_interval = 300000
        self.timer.start(self.refresh_interval)

        # Detektuj buđenje iz sleep moda
        self.last_update = datetime.now()
        self.sleep_check_timer = QTimer()
        self.sleep_check_timer.timeout.connect(self.checkForSleepWake)
        self.sleep_check_timer.start(5000)
        
        # ✅ NOVO: Provera connection health-a (svaki 10 sekundi)
        self.connection_check_timer = QTimer()
        self.connection_check_timer.timeout.connect(self.checkConnectionHealth)
        self.connection_check_timer.start(10000)  # Proveri svaki 10 sekundi

        # --- Wake backoff / sleep-safe refresh ---
        self._sleep_detected = False
        self._wakeup_retry_in_progress = False
        self._wake_backoff = 5
        self._wake_backoff_max = 300
        self._wake_retry_timer = QTimer()
        self._wake_retry_timer.setSingleShot(True)
        self._wake_retry_timer.timeout.connect(self._wakeRetry)

        # --- Last successful update time ---
        self._last_updated_time = None

    def initUI(self):
        self.setWindowTitle('Vremenska Prognoza')
        # Koristi sačuvanu veličinu iz settings
        self.setGeometry(100, 100, self.widget_width, self.widget_height)

        # Transparentan prozor bez okvira - ISPOD svih prozora
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnBottomHint |
            Qt.SubWindow
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        # Centralni widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)

        # Glavni kontejner sa pozadinom
        self.main_container = QWidget()
        self.main_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(20, 25, 35, 0.85), stop:1 rgba(30, 35, 45, 0.85));
                border-radius: 20px;
                border: 1px solid rgba(70, 130, 180, 0.3);
            }
        """)
        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(15, 15, 15, 15)

        # Header sa kontrolama
        header = QHBoxLayout()

        # Interval dropdown
        self.interval_label = QLabel("Osvežavanje:")
        self.interval_label.setStyleSheet("color: white; font-size: 12px;")

        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["5 min", "10 min", "15 min", "30 min", "60 min"])
        self.interval_combo.setCurrentIndex(0)
        self.interval_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(50, 60, 75, 0.6);
                color: white;
                border: 1px solid rgba(70, 130, 180, 0.4);
                border-radius: 8px;
                padding: 5px;
                font-size: 12px;
                min-width: 70px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: rgba(30, 35, 45, 0.95);
                color: white;
                selection-background-color: rgba(70, 130, 180, 0.3);
            }
        """)
        self.interval_combo.currentIndexChanged.connect(self.changeRefreshInterval)

        header.addWidget(self.interval_label)
        header.addWidget(self.interval_combo)

        # Lokacija input
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Unesi grad...")
        self.location_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(50, 60, 75, 0.6);
                color: white;
                border: 1px solid rgba(70, 130, 180, 0.4);
                border-radius: 10px;
                padding: 8px;
                font-size: 12px;
            }
        """)

        # Auto lokacija dugme
        self.auto_btn = QPushButton("📍 Auto")
        self.auto_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 60, 75, 0.6);
                color: white;
                border: 1px solid rgba(70, 130, 180, 0.4);
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(70, 130, 180, 0.4);
            }
        """)
        self.auto_btn.clicked.connect(self.toggleAutoLocation)

        # Pretraga dugme
        search_btn = QPushButton("🔍")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 60, 75, 0.6);
                color: white;
                border: 1px solid rgba(70, 130, 180, 0.4);
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(70, 130, 180, 0.4);
            }
        """)
        search_btn.clicked.connect(self.searchLocation)

        header.addWidget(self.location_input)
        header.addWidget(self.auto_btn)
        header.addWidget(search_btn)

        # Close dugme
        close_btn = QPushButton("✕")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 0.5);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                max-width: 30px;
                max-height: 30px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.7);
            }
        """)
        close_btn.clicked.connect(self.hide)

        # Lock dugme
        self.lock_btn = QPushButton("🔓")
        self.lock_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 60, 75, 0.6);
                color: white;
                border: 1px solid rgba(70, 130, 180, 0.4);
                border-radius: 15px;
                font-size: 16px;
                max-width: 30px;
                max-height: 30px;
            }
            QPushButton:hover {
                background-color: rgba(70, 130, 180, 0.4);
            }
        """)
        self.lock_btn.clicked.connect(self.toggleLock)
        self.lock_btn.setToolTip("Zaključaj poziciju")

        header.addWidget(self.lock_btn)
        header.addWidget(close_btn)

        container_layout.addLayout(header)

        # Grad
        self.city_label = QLabel("Grad")
        self.city_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        container_layout.addWidget(self.city_label)

        # Sat i Battery status u istom redu - wrapper widget bez okvira
        clock_battery_widget = QWidget()
        clock_battery_widget.setStyleSheet("background: transparent; border: none;")
        clock_battery_layout = QHBoxLayout(clock_battery_widget)
        clock_battery_layout.setContentsMargins(0, 0, 0, 0)
        clock_battery_layout.setSpacing(10)
        
        # Spacer levo da centrira sat
        clock_battery_layout.addStretch()
        
        # Sat
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold; background: transparent;")
        self.clock_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # ✅ Dodato vertikalno centriranje
        self.clock_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        clock_battery_layout.addWidget(self.clock_label, alignment=Qt.AlignVCenter)  # ✅ Layout alignment
        
        # Battery status (prikazuje se samo na laptopu)
        self.battery_label = QLabel("")
        self.battery_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; background: transparent;")
        self.battery_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # ✅ Dodato vertikalno centriranje
        self.battery_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.battery_label.hide()  # Sakrij dok ne proverimo da li je laptop
        clock_battery_layout.addWidget(self.battery_label, alignment=Qt.AlignVCenter)  # ✅ Layout alignment
        
        # Spacer desno da održi balans
        clock_battery_layout.addStretch()
        
        container_layout.addWidget(clock_battery_widget)

        # Datum
        self.date_label = QLabel(self.format_date_serbian(datetime.now()))
        self.date_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px;")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        container_layout.addWidget(self.date_label)

        container_layout.addSpacing(6)

        # Temperatura
        temp_symbol = self.get_temp_symbol()
        self.temp_label = QLabel(f"--{temp_symbol}")
        self.temp_label.setStyleSheet("color: white; font-size: 60px; font-weight: bold;")
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        container_layout.addWidget(self.temp_label)

        # Opis vremena
        self.desc_label = QLabel("Učitavanje...")
        self.desc_label.setStyleSheet("color: white; font-size: 18px;")
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        container_layout.addWidget(self.desc_label)

        # Offline status (mali/sivi tekst) - ne briše poslednje podatke
        self.offline_status_label = QLabel("")
        self.offline_status_label.setAlignment(Qt.AlignCenter)
        self.offline_status_label.setStyleSheet("color: rgba(255, 255, 255, 0.55); font-size: 11px; font-style: italic;")
        self.offline_status_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.offline_status_label.hide()
        container_layout.addWidget(self.offline_status_label)

        # ✅ Last updated (stays even when offline/sleep)
        self.last_updated_label = QLabel(self.t("last_updated_fmt").format("--:--"))
        self.last_updated_label.setAlignment(Qt.AlignCenter)
        self.last_updated_label.setStyleSheet("color: rgba(255, 255, 255, 0.55); font-size: 11px;")
        self.last_updated_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        container_layout.addWidget(self.last_updated_label)

        container_layout.addSpacing(6)

        # Info panel - PRVI RED (Oseća se, Vlažnost, Vetar sa pravcem)
        info_panel_1 = QHBoxLayout()

        # Oseća se kao
        feels_box = QVBoxLayout()
        temp_symbol = self.get_temp_symbol()
        self.feels_label = QLabel(f"--{temp_symbol}")
        self.feels_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.feels_label.setAlignment(Qt.AlignCenter)
        self.feels_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.feels_text = QLabel("Oseća se kao")
        self.feels_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.feels_text.setAlignment(Qt.AlignCenter)
        self.feels_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        feels_box.addWidget(self.feels_label)
        feels_box.addWidget(self.feels_text)

        # Vlažnost
        humid_box = QVBoxLayout()
        self.humid_label = QLabel("--%")
        self.humid_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.humid_label.setAlignment(Qt.AlignCenter)
        self.humid_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.humid_text = QLabel("Vlažnost")
        self.humid_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.humid_text.setAlignment(Qt.AlignCenter)
        self.humid_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        humid_box.addWidget(self.humid_label)
        humid_box.addWidget(self.humid_text)

        # Vetar SA PRAVCEM
        wind_box = QVBoxLayout()
        self.wind_label = QLabel("-- km/h")
        self.wind_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.wind_label.setAlignment(Qt.AlignCenter)
        self.wind_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.wind_text = QLabel("Vetar")
        self.wind_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.wind_text.setAlignment(Qt.AlignCenter)
        self.wind_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        wind_box.addWidget(self.wind_label)
        wind_box.addWidget(self.wind_text)

        info_panel_1.addLayout(feels_box)
        info_panel_1.addLayout(humid_box)
        info_panel_1.addLayout(wind_box)

        container_layout.addLayout(info_panel_1)
        container_layout.addSpacing(8)

        # Info panel - DRUGI RED (UV Index, Zagađenje sa tooltip-om)
        info_panel_2 = QHBoxLayout()

        # UV Index
        uv_box = QVBoxLayout()
        self.uv_label = QLabel("--")
        self.uv_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.uv_label.setAlignment(Qt.AlignCenter)
        self.uv_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.uv_text = QLabel("☀️ UV Index")
        self.uv_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.uv_text.setAlignment(Qt.AlignCenter)
        self.uv_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        uv_box.addWidget(self.uv_label)
        uv_box.addWidget(self.uv_text)

        # Air Quality (Zagađenje) - sa interaktivnim tooltip-om
        aqi_box = QVBoxLayout()
        self.aqi_label = ClickableLabel("--")
        self.aqi_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.aqi_label.setAlignment(Qt.AlignCenter)
        self.aqi_label.clicked.connect(self.showPollutantsTooltip)
        self.aqi_text = QLabel("🌫️ Zagađenje")
        self.aqi_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.aqi_text.setAlignment(Qt.AlignCenter)
        self.aqi_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        aqi_box.addWidget(self.aqi_label)
        aqi_box.addWidget(self.aqi_text)

        info_panel_2.addLayout(uv_box)
        info_panel_2.addLayout(aqi_box)

        container_layout.addLayout(info_panel_2)
        container_layout.addSpacing(8)

        # Info panel - TREĆI RED (Pritisak, Oblačnost, Vidljivost) - 3 kolone
        info_panel_3 = QHBoxLayout()

        # Pritisak
        pressure_box = QVBoxLayout()
        self.pressure_label = QLabel("-- mbar")
        self.pressure_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.pressure_label.setAlignment(Qt.AlignCenter)
        self.pressure_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.pressure_text = QLabel("📊 Pritisak")
        self.pressure_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.pressure_text.setAlignment(Qt.AlignCenter)
        self.pressure_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        pressure_box.addWidget(self.pressure_label)
        pressure_box.addWidget(self.pressure_text)

        # Oblačnost
        clouds_box = QVBoxLayout()
        self.clouds_label = QLabel("--%")
        self.clouds_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.clouds_label.setAlignment(Qt.AlignCenter)
        self.clouds_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.clouds_text = QLabel("☁️ Oblačnost")
        self.clouds_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.clouds_text.setAlignment(Qt.AlignCenter)
        self.clouds_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        clouds_box.addWidget(self.clouds_label)
        clouds_box.addWidget(self.clouds_text)

        # Vidljivost
        visibility_box = QVBoxLayout()
        self.visibility_label = QLabel("-- km")
        self.visibility_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.visibility_label.setAlignment(Qt.AlignCenter)
        self.visibility_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.visibility_text = QLabel("👁️ Vidljivost")
        self.visibility_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.visibility_text.setAlignment(Qt.AlignCenter)
        self.visibility_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        visibility_box.addWidget(self.visibility_label)
        visibility_box.addWidget(self.visibility_text)

        info_panel_3.addLayout(pressure_box)
        info_panel_3.addLayout(clouds_box)
        info_panel_3.addLayout(visibility_box)

        container_layout.addLayout(info_panel_3)

        container_layout.addSpacing(12)

        # Sunrise/Sunset panel
        sun_panel = QHBoxLayout()

        # Sunrise
        sunrise_box = QVBoxLayout()
        self.sunrise_label = QLabel("--:--")
        self.sunrise_label.setStyleSheet("color: #FFD700; font-size: 18px; font-weight: bold;")
        self.sunrise_label.setAlignment(Qt.AlignCenter)
        self.sunrise_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.sunrise_text = QLabel("🌅 Izlazak")
        self.sunrise_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.sunrise_text.setAlignment(Qt.AlignCenter)
        self.sunrise_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        sunrise_box.addWidget(self.sunrise_label)
        sunrise_box.addWidget(self.sunrise_text)

        # Sunset
        sunset_box = QVBoxLayout()
        self.sunset_label = QLabel("--:--")
        self.sunset_label.setStyleSheet("color: #FF6B35; font-size: 18px; font-weight: bold;")
        self.sunset_label.setAlignment(Qt.AlignCenter)
        self.sunset_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.sunset_text = QLabel("🌇 Zalazak")
        self.sunset_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        self.sunset_text.setAlignment(Qt.AlignCenter)
        self.sunset_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        sunset_box.addWidget(self.sunset_label)
        sunset_box.addWidget(self.sunset_text)

        sun_panel.addLayout(sunrise_box)
        sun_panel.addSpacing(40)
        sun_panel.addLayout(sunset_box)

        container_layout.addLayout(sun_panel)

        container_layout.addSpacing(15)

        # Info Boxes - Padavine i Upozorenja (2 kvadrata u redu) - IZNAD 5-day!
        info_boxes_layout = QHBoxLayout()
        info_boxes_layout.setSpacing(8)

        # KVADRAT 1: Padavine Alert
        precip_box = QWidget()
        precip_box.setStyleSheet("""
            QWidget {
                background-color: rgba(33, 150, 243, 0.3);
                border-radius: 8px;
                border: 1px solid rgba(33, 150, 243, 0.5);
                padding: 8px;
            }
        """)
        precip_layout = QVBoxLayout(precip_box)
        precip_layout.setContentsMargins(8, 8, 8, 8)
        precip_layout.setSpacing(3)

        precip_title = QLabel("🌧️ PADAVINE")
        precip_title.setStyleSheet("color: #90CAF9; font-size: 11px; font-weight: bold;")
        precip_title.setAlignment(Qt.AlignCenter)
        precip_title.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.precip_title = precip_title  # ✅ Save reference

        self.precip_alert_label = QLabel("Učitavam...")
        self.precip_alert_label.setStyleSheet("color: white; font-size: 11px;")
        self.precip_alert_label.setAlignment(Qt.AlignCenter)
        self.precip_alert_label.setWordWrap(True)
        self.precip_alert_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        precip_layout.addWidget(precip_title)
        precip_layout.addWidget(self.precip_alert_label)

        # KVADRAT 2: Satna Prognoza (umesto Weather Alerts)
        self.alerts_box = QWidget()
        self.alerts_box.setStyleSheet("""
            QWidget {
                background-color: rgba(33, 150, 243, 0.3);
                border-radius: 8px;
                border: 1px solid rgba(33, 150, 243, 0.5);
                padding: 8px;
            }
        """)
        alerts_layout = QVBoxLayout(self.alerts_box)
        alerts_layout.setContentsMargins(8, 8, 8, 8)
        alerts_layout.setSpacing(3)

        alerts_title = QLabel("🕐 SATNA PROGNOZA")
        alerts_title.setStyleSheet("color: #90CAF9; font-size: 11px; font-weight: bold;")
        alerts_title.setAlignment(Qt.AlignCenter)
        alerts_title.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.hourly_forecast_title = alerts_title  # ✅ Save reference

        self.weather_alert_label = ClickableLabel("Učitavam...")
        self.weather_alert_label.setStyleSheet("color: white; font-size: 11px; line-height: 1.3;")
        self.weather_alert_label.setAlignment(Qt.AlignCenter)
        self.weather_alert_label.setWordWrap(True)
        self.weather_alert_label.setFixedHeight(32)  # ✅ FIKSNO 2 reda (11px * 1.3 line-height * 2)
        self.weather_alert_label.clicked.connect(self.showHourlyForecastTooltip)  # ✅ TOOLTIP!

        alerts_layout.addWidget(alerts_title)
        alerts_layout.addWidget(self.weather_alert_label)

        info_boxes_layout.addWidget(precip_box)
        info_boxes_layout.addWidget(self.alerts_box)

        container_layout.addLayout(info_boxes_layout)

        container_layout.addSpacing(10)

        # 5-day forecast naslov
        forecast_title = QLabel("Prognoza za 5 dana")
        forecast_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        forecast_title.setAlignment(Qt.AlignCenter)
        forecast_title.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.forecast_5day_title = forecast_title  # ✅ Save reference
        container_layout.addWidget(forecast_title)

        container_layout.addSpacing(8)

        # 5-day forecast container
        self.forecast_container = QVBoxLayout()
        self.forecast_container.setSpacing(6)

        # Kreiraj 5 redova za dane
        self.forecast_labels = []
        for i in range(5):
            day_widget = QWidget()
            day_widget.setStyleSheet("""
                QWidget {
                    background-color: rgba(50, 60, 75, 0.4);
                    border-radius: 10px;
                    padding: 8px;
                    border: 1px solid rgba(70, 130, 180, 0.2);
                }
            """)
            day_layout = QHBoxLayout(day_widget)
            day_layout.setContentsMargins(10, 5, 10, 5)

            # Dan
            day_label = QLabel("---")
            day_label.setStyleSheet("color: white; font-size: 13px; font-weight: bold; min-width: 70px;")
            day_label.setAttribute(Qt.WA_TransparentForMouseEvents)

            # Opis
            desc_label = QLabel("---")
            desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 12px;")
            desc_label.setAlignment(Qt.AlignLeft)
            desc_label.setWordWrap(True)
            desc_label.setAttribute(Qt.WA_TransparentForMouseEvents)

            # Temperatura
            temp_label = QLabel("--° / --°")
            temp_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; min-width: 95px;")
            temp_label.setAlignment(Qt.AlignRight)
            temp_label.setAttribute(Qt.WA_TransparentForMouseEvents)

            day_layout.addWidget(day_label)
            day_layout.addWidget(desc_label, 1)
            day_layout.addWidget(temp_label)

            self.forecast_labels.append({
                'day': day_label,
                'desc': desc_label,
                'temp': temp_label
            })

            self.forecast_container.addWidget(day_widget)

        container_layout.addLayout(self.forecast_container)
        container_layout.addStretch()

        layout.addWidget(self.main_container)

        # Omogući pomeranje prozora
        self.dragging = False
        self.offset = QPoint()

    def showPollutantsTooltip(self):
        """Prikaži detaljne podatke o polutantima"""
        print("🖱️ Kliknut Zagađenje label!")
        
        if not self.pollutants_data:
            tooltip_text = "<b>⚠️ Nema dostupnih podataka o polutantima</b>"
            QToolTip.showText(QCursor.pos(), tooltip_text, None)
            print("❌ Nema pollutants_data")
            return
        
        # ✅ Build HTML with proper translation
        tooltip_html = f"""
        <html>
        <head>
        <style>
        body {{
            background-color: #0F141E;
            color: #ECEFF1;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 12px;
            min-width: 300px;
        }}
        .header {{
            color: #4CAF50;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 12px;
        }}
        .pollutant-row {{
            margin-bottom: 6px;
            line-height: 1.5;
        }}
        .pollutant-code {{
            color: #ECEFF1;
            font-weight: bold;
        }}
        .pollutant-name {{
            color: #B0BEC5;
        }}
        .pollutant-value {{
            color: #81C784;
            font-weight: bold;
        }}
        </style>
        </head>
        <body>
        <div class="header">🧪 {self.t("pollutants_title")}</div>
        """
        
        pollutants = [
            ("CO", self.t("carbon_monoxide"), "μg/m³"),
            ("NO₂", self.t("nitrogen_dioxide"), "μg/m³"),
            ("O₃", self.t("ozone"), "μg/m³"),
            ("SO₂", self.t("sulfur_dioxide"), "μg/m³"),
            ("PM2.5", self.t("fine_particles"), "μg/m³"),
            ("PM10", self.t("coarse_particles"), "μg/m³"),
            ("NH₃", self.t("ammonia"), "μg/m³")
        ]
        
        for code, name, unit in pollutants:
            key = code.replace("₂", "2").replace("₃", "3").replace(".", "_").lower()
            if key in self.pollutants_data:
                value = self.pollutants_data[key]
                tooltip_html += f"""
        <div class="pollutant-row">
            <span class="pollutant-code">{code}</span> 
            <span class="pollutant-name">({name}):</span> 
            <span class="pollutant-value">{value:.1f} {unit}</span>
        </div>
                """
        
        tooltip_html += """
        </body>
        </html>
        """
        
        print(f"✅ Prikazujem tooltip sa {len(self.pollutants_data)} polutanata")
        QToolTip.showText(QCursor.pos(), tooltip_html, self.aqi_label)

    def showHourlyForecastTooltip(self):
        """Prikaži detaljnu satnu prognozu u tooltip-u"""
        print("🖱️ Kliknut Satna Prognoza label!")
        
        if not hasattr(self, 'hourly_forecast_data') or not self.hourly_forecast_data:
            tooltip_text = "<b>⚠️ Nema dostupnih satnih podataka</b>"
            QToolTip.showText(QCursor.pos(), tooltip_text, None)
            print("❌ Nema hourly_forecast_data")
            return
        
        # Translation variables
        time_header = "Vreme" if self.current_language == "sr" else "Time"
        weather_header = "Vreme" if self.current_language == "sr" else "Weather"
        rain_header = "Kiša%" if self.current_language == "sr" else "Rain%"
        
        # ✅ Build HTML with f-string for proper translation
        tooltip_html = f"""
        <html>
        <head>
        <style>
        body {{
            background-color: #0F141E;
            color: #ECEFF1;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 12px;
        }}
        .header {{
            color: #90CAF9;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 12px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            font-family: 'Consolas', monospace;
            font-size: 11px;
        }}
        th {{
            color: #78909C;
            font-size: 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid rgba(144, 202, 249, 0.3);
        }}
        td {{
            padding: 4px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .time-col {{ color: #CFD8DC; }}
        .icon-col {{ font-size: 16px; text-align: center; padding: 0 8px; }}
        .temp-col {{ font-weight: bold; text-align: right; }}
        .rain-col {{ text-align: right; padding-left: 12px; }}
        .footer {{
            color: #78909C;
            font-size: 9px;
            text-align: center;
            margin-top: 8px;
        }}
        </style>
        </head>
        <body>
        <div class="header">🕐 {self.t("hourly_forecast_tooltip")}</div>
        <table>
        <tr>
            <th align="left">{time_header}</th>
            <th align="center" style="padding: 0 8px;">{weather_header}</th>
            <th align="right">Temp</th>
            <th align="right" style="padding-left: 12px;">{rain_header}</th>
        </tr>
        """
        
        for hour_data in self.hourly_forecast_data[:12]:  # Prvih 12 sati
            time = hour_data['time']
            temp = hour_data['temp']
            weather_icon = hour_data['icon']
            weather_code = hour_data.get('weather_code', 0)  # ✅ Uzmi code
            desc = self.getWeatherDescription(weather_code)[1]  # ✅ Prevedi sada!
            precip_prob = hour_data.get('precip_prob', 0)
            
            temp_symbol = self.get_temp_symbol()
            
            # Boja temperature
            if temp > 25:
                temp_color = "#FF9E80"
            elif temp > 15:
                temp_color = "#A5D6A7"
            elif temp > 5:
                temp_color = "#81D4FA"
            else:
                temp_color = "#B3E5FC"
            
            # Boja padavina
            if precip_prob > 70:
                precip_color = "#FF8A80"
            elif precip_prob > 40:
                precip_color = "#FFD54F"
            else:
                precip_color = "#A5D6A7"
            
            tooltip_html += f"""
        <tr>
            <td class="time-col">{time}</td>
            <td class="icon-col" title="{desc}">{weather_icon}</td>
            <td class="temp-col" style="color: {temp_color};">{temp}{temp_symbol}</td>
            <td class="rain-col" style="color: {precip_color};">{precip_prob}%</td>
        </tr>
            """
        
        tooltip_html += f"""
        </table>
        <div class="footer">💡 {self.t("hover_for_details")}</div>
        </body>
        </html>
        """
        
        print(f"✅ Prikazujem satnu prognozu ({len(self.hourly_forecast_data[:12])} sati)")
        
        # ✅ POZICIONIRANJE: Prikaži ISPOD widgeta
        label_global_pos = self.weather_alert_label.mapToGlobal(self.weather_alert_label.rect().bottomLeft())
        tooltip_pos = label_global_pos + QPoint(0, 10)
        
        QToolTip.showText(tooltip_pos, tooltip_html, self.weather_alert_label)

    def showAlertTooltip(self):
        """Prikaži pun tekst upozorenja u tooltip-u"""
        print("🖱️ Kliknut Alert label!")  # Debug

        if not self.full_alert_text or self.full_alert_text in ["✅ Bez upozorenja", "⚠️ Greška", "Učitavam..."]:
            print("ℹ️ Nema upozorenja za prikaz")
            return

        # Ako nema weatheralerts podataka, prikaži samo osnovni tekst
        if not hasattr(self, 'current_alert_data') or not self.current_alert_data:
            tooltip_text = f"<div style='background-color: rgba(30, 35, 45, 0.95); padding: 10px; border-radius: 5px;'>"
            tooltip_text += f"<b style='color: #FFB74D; font-size: 14px;'>⚠️ Upozorenje:</b><br><br>"
            tooltip_text += f"<span style='color: white;'>{self.full_alert_text}</span>"
            tooltip_text += "</div>"
            QToolTip.showText(QCursor.pos(), tooltip_text, self.weather_alert_label)
            return

        # Prikaži detaljnije ako ima više podataka
        alert = self.current_alert_data
        
        tooltip_text = "<div style='background-color: rgba(30, 35, 45, 0.95); padding: 12px; border-radius: 5px; max-width: 350px;'>"
        tooltip_text += "<b style='color: #FFB74D; font-size: 14px;'>⚠️ Vremensko upozorenje:</b><br><br>"
        
        # Naslov upozorenja
        tooltip_text += f"<b style='color: white; font-size: 13px;'>{self.full_alert_text}</b><br><br>"
        
        # Vreme trajanja (ako postoji)
        if 'start' in alert and 'end' in alert:
            start_dt = datetime.fromtimestamp(alert['start'])
            end_dt = datetime.fromtimestamp(alert['end'])
            start_time = start_dt.strftime('%d.%m. ') + self.format_time_short(start_dt)
            end_time = end_dt.strftime('%d.%m. ') + self.format_time_short(end_dt)
            tooltip_text += f"<span style='color: #AAA;'>📅 Trajanje:</span> <span style='color: #90CAF9;'>{start_time} - {end_time}</span><br><br>"
        
        # Opis (ako postoji)
        if 'description' in alert and alert['description']:
            desc = alert['description'][:300]  # Ograniči na 300 karaktera
            if len(alert['description']) > 300:
                desc += "..."
            
            # ✅ PREVEDI NA SRPSKI
            desc_sr = self.translateAlertDescription(desc)
            
            tooltip_text += f"<span style='color: #CCC; font-size: 11px;'>{desc_sr}</span>"
        
        tooltip_text += "</div>"

        print(f"✅ Prikazujem alert tooltip: {self.full_alert_text}")
        QToolTip.showText(QCursor.pos(), tooltip_text, self.weather_alert_label)

    def translateAlertDescription(self, text: str) -> str:
        """
        Prevodi engleski opis upozorenja na srpski (latinica).
        Koristi regex i pametnije zamene za bolje rezultate.
        """
        if not text:
            return ""
        
        result = text
        
        # PRVO: Specifične fraze (pre pojedinačnih reči!)
        phrase_translations = [
            (r"Minimum temperature lower than", "Minimalna temperatura niža od"),
            (r"Minumim temperatur niz od", "Minimalna temperatura niža od"),  # Typo u originalnom tekstu
            (r"MSL lower than", "MSL niža od"),
            (r"MSL niz od", "MSL niža od"),
            (r"above \d+ MSL", lambda m: m.group(0).replace("above", "iznad").replace("MSL", "MSL")),
            (r"iznad \d+", lambda m: m.group(0)),  # Keep Serbian
        ]
        
        for pattern, replacement in phrase_translations:
            if callable(replacement):
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
            else:
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # DRUGO: Pojedinačne reči
        word_translations = {
            # Temperature
            r"\bMinimum\b": "Minimalna",
            r"\bMinumim\b": "Minimalna",  # Typo fix
            r"\bmaximum\b": "maksimalna",
            r"\bMaximum\b": "Maksimalna",
            r"\btemperature\b": "temperatura",
            r"\bTemperature\b": "Temperatura",
            r"\btemperatur\b": "temperatura",  # Typo
            
            # Comparison
            r"\blower than\b": "niža od",
            r"\bhigher than\b": "viša od",
            r"\bbelow\b": "ispod",
            r"\babove\b": "iznad",
            r"\bniz od\b": "niža od",  # Keep fixed
            
            # Weather
            r"\bfrost\b": "mraz",
            r"\bFrost\b": "Mraz",
            r"\bice\b": "led",
            r"\bIce\b": "Led",
            r"\bsnow\b": "sneg",
            r"\bSnow\b": "Sneg",
            r"\brain\b": "kiša",
            r"\bRain\b": "Kiša",
            r"\bwind\b": "vetar",
            r"\bWind\b": "Vetar",
            r"\bstorm\b": "oluja",
            r"\bStorm\b": "Oluja",
            
            # Common words
            r"\band\b": "i",
            r"\bor\b": "ili",
            r"\bwith\b": "sa",
            r"\bfrom\b": "od",
            r"\bto\b": "do",
            r"\buntil\b": "do",
            r"\bin\b": "u",
            r"\bon\b": "na",
            r"\bat\b": "u",
        }
        
        for pattern, replacement in word_translations.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # TREĆE: Očisti višestruke razmake
        result = re.sub(r'\s+', ' ', result).strip()
        
        return result

    def getWindDirection(self, degrees):
        """Pretvori stepene u pravac vetra (N, NE, E, SE, S, SW, W, NW)"""
        # Dvojezični pravci vetra (Serbian / English)
        if self.current_language == "sr":
            directions = ['S', 'SI', 'I', 'JI', 'J', 'JZ', 'Z', 'SZ']
        else:  # English
            directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        
        index = round(degrees / 45) % 8
        return directions[index]

    def format_date_serbian(self, date):
        """Formatuj datum prema trenutnom jeziku"""
        day_name = date.strftime('%A').lower()
        month_name = date.strftime('%B').lower()
        
        # Mapiranje English → translation key
        day_key_map = {
            'monday': 'monday',
            'tuesday': 'tuesday',
            'wednesday': 'wednesday',
            'thursday': 'thursday',
            'friday': 'friday',
            'saturday': 'saturday',
            'sunday': 'sunday'
        }
        
        month_key_map = {
            'january': 'january',
            'february': 'february',
            'march': 'march',
            'april': 'april',
            'may': 'may',
            'june': 'june',
            'july': 'july',
            'august': 'august',
            'september': 'september',
            'october': 'october',
            'november': 'november',
            'december': 'december'
        }
        
        # Prevedi na trenutni jezik
        day_key = day_key_map.get(day_name, day_name)
        month_key = month_key_map.get(month_name, month_name)
        
        # Za Srpski: puni naziv dana
        # Za English: skraćeni naziv (Mon, Tue...)
        if self.current_language == "sr":
            # Puni nazivi za srpski
            day_full_sr = {
                'monday': 'Ponedeljak',
                'tuesday': 'Utorak',
                'wednesday': 'Sreda',
                'thursday': 'Četvrtak',
                'friday': 'Petak',
                'saturday': 'Subota',
                'sunday': 'Nedelja'
            }
            day_translated = day_full_sr.get(day_name, day_name)
            month_translated = self.t(month_key).capitalize()  # ✅ VELIKO SLOVO
            return f"{day_translated}, {date.day} {month_translated} {date.year}"
        else:
            # Za engleski: "Monday, 3 January 2026"
            day_full_en = {
                'monday': 'Monday',
                'tuesday': 'Tuesday',
                'wednesday': 'Wednesday',
                'thursday': 'Thursday',
                'friday': 'Friday',
                'saturday': 'Saturday',
                'sunday': 'Sunday'
            }
            day_translated = day_full_en.get(day_name, day_name.capitalize())
            month_translated = self.t(month_key).capitalize()
            return f"{day_translated}, {date.day} {month_translated} {date.year}"

    def updateClock(self):
        """Ažuriraj sat svake sekunde"""
        current_time_obj = datetime.now()
        if self.time_format == '12h':
            current_time = current_time_obj.strftime("%I:%M:%S %p")
        else:
            current_time = current_time_obj.strftime("%H:%M:%S")
        self.clock_label.setText(current_time)

        # Proveri da li je promenjen datum (prošla ponoć)
        current_date = datetime.now().strftime("%Y-%m-%d")
        if not hasattr(self, '_last_date'):
            self._last_date = current_date

        if current_date != self._last_date:
            # Datum se promenio - osvežimo sve!
            print("🔄 Promenjen datum - osvežavam widget...")
            self.date_label.setText(self.format_date_serbian(datetime.now()))
            self.updateWeather()  # Osvežava i prognozu za 5 dana
            self._last_date = current_date
    
    def updateBatteryStatus(self):
        """Ažuriraj battery status (samo na laptopu)"""
        if not PSUTIL_AVAILABLE:
            return
        
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                # Nije laptop - sakrij battery label
                self.battery_label.hide()
                return
            
            # Jeste laptop - prikaži battery status
            percent = int(battery.percent)
            is_charging = battery.power_plugged
            
            # Odaberi ikonicu na osnovu procenta i charging statusa
            if is_charging:
                icon = "🔌"  # Charging
            elif percent >= 90:
                icon = "🔋"  # Full battery
            elif percent >= 60:
                icon = "🔋"  # Good battery
            elif percent >= 30:
                icon = "🔋"  # Medium battery
            elif percent >= 15:
                icon = "🪫"  # Low battery
            else:
                icon = "🪫"  # Critical battery
            
            # Boja na osnovu procenta
            if is_charging:
                color = "#4CAF50"  # Zelena za charging
            elif percent >= 30:
                color = "rgba(255, 255, 255, 0.8)"  # Bela
            elif percent >= 15:
                color = "#FFC107"  # Narandžasta
            else:
                color = "#F44336"  # Crvena
            
            # Postavi tekst i boju
            self.battery_label.setText(f"{icon} {percent}%")
            self.battery_label.setStyleSheet(f"color: {color}; font-size: 14px;")
            self.battery_label.show()
            
        except Exception as e:
            print(f"❌ Battery status greška: {e}")
            self.battery_label.hide()

    def checkForSleepWake(self):
        """Detektuje sleep/wake i radi safe refresh sa exponential backoff-om."""
        now = datetime.now()
        time_diff = (now - self.last_update).total_seconds()
        self.last_update = now

        # Ako je prošlo dosta vremena između tick-ova, verovatno je bio sleep/hibernation
        if time_diff > 60:
            self._sleep_detected = True
            self._wake_backoff = 5
            # Ne diramo glavne podatke (temp/desc/prognozu), samo mali status
            self.showSleepStatus("čekam stabilizaciju mreže")

            # Zaustavi standardni refresh timer da ne spamuje dok se sistem budi
            try:
                if hasattr(self, 'timer') and self.timer.isActive():
                    self.timer.stop()
            except Exception:
                pass

            # Zakaži prvi pokušaj posle wake-a
            self._scheduleWakeRetry()

    def _scheduleWakeRetry(self):
        """Zakaži wake retry (single-shot) ako već nije zakazan."""
        try:
            if not self._wake_retry_timer.isActive():
                self._wake_retry_timer.start(int(self._wake_backoff * 1000))
        except Exception:
            pass

    def _wakeRetry(self):
        """Pokuša osvežavanje posle wake-a uz exponential backoff."""
        # Pokušaj brzu DNS proveru pre API poziva
        try:
            socket.getaddrinfo('api.open-meteo.com', 443)
        except Exception:
            # DNS još nije spreman – ostani u sleep statusu i zakaži ponovo
            self.showSleepStatus("čekam mrežu")
            self._wake_backoff = min(self._wake_backoff * 2, self._wake_backoff_max)
            self._scheduleWakeRetry()
            return

        # DNS radi – pokušaj pravi refresh
        self._wakeup_retry_in_progress = True
        try:
            self.updateWeather()
        finally:
            self._wakeup_retry_in_progress = False

        if self.is_online:
            # Uspeh: skloni sleep status, resetuj backoff, vrati standardni timer
            self._sleep_detected = False
            self._wake_backoff = 5
            self.hideSleepStatus()
            try:
                if hasattr(self, 'timer') and not self.timer.isActive():
                    self.timer.start(self.refresh_interval)
            except Exception:
                pass
        else:
            # Još uvek offline: nastavi backoff
            self.showSleepStatus("offline nakon wake-a")
            self._wake_backoff = min(self._wake_backoff * 2, self._wake_backoff_max)
            self._scheduleWakeRetry()

    def showSleepStatus(self, reason: str = ""):
        """Prikaži mali sleep status (ne dira poslednje podatke)."""
        if hasattr(self, "offline_status_label"):
            txt = self.t("sleep_detected")
            if reason:
                txt += f" – {reason}"
            self.offline_status_label.setText(txt)
            self.offline_status_label.show()

    def hideSleepStatus(self):
        """Sakrij sleep status."""
        # Ne skrivamo ako smo još offline (tada showOfflineStatus može da ga drži)
        if hasattr(self, "offline_status_label") and self.is_online:
            self.offline_status_label.hide()

    def showOfflineStatus(self, reason: str = ""):
        """Prikaži mali offline status i zadrži poslednje prikazane podatke."""
        if getattr(self, '_sleep_detected', False):
            # Ne prepisuj sleep status dok traje wake recovery
            self.is_online = False
            return

        if hasattr(self, "offline_status_label"):
            txt = self.t("offline_waiting")
            if reason:
                txt += f" ({reason})"
            self.offline_status_label.setText(txt)
            self.offline_status_label.show()
        self.is_online = False

    def hideOfflineStatus(self):
        """Sakrij offline status (pozovi nakon prvog uspešnog osvežavanja)."""
        if hasattr(self, "offline_status_label"):
            self.offline_status_label.hide()
        self.is_online = True

    def checkConnectionHealth(self):
        """Diskretno proverava da li se internet vratio (bez rušenja UI-ja)."""
        try:
            # Brza DNS provera (ne blokira dugo)
            socket.getaddrinfo("api.open-meteo.com", 443)

            # Ako smo bili offline, čim DNS proradi – uradi jedno osvežavanje
            if not self.is_online:
                print("🌐 Internet se vratio – osvežavam vreme...")
                # Ne diramo postojeće labele dok ne dobijemo validan odgovor
                self.updateWeather()

        except Exception:
            # Nema DNS / nema interneta – samo prikaži status, NE briši stare podatke
            if self.is_online:
                print("🌐 Internet/DNS je nedostupan – prelazim u offline režim (zadržavam poslednje podatke).")
            self.showOfflineStatus()

    def retryUpdateWeather(self, attempt=1, max_attempts=3):
        """Pokušaj da osvežiš vreme sa progresivnim čekanjem"""
        print(f"🔄 Pokušaj {attempt}/{max_attempts}...")

        try:
            self.updateWeather()
            print(f"✅ Uspešno osveženo na pokušaj {attempt}!")
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < max_attempts:
                # Čekaj 15 sekundi između pokušaja
                wait_time = 15000  # 15 sekundi
                print(f"⚠️ Pokušaj {attempt} neuspešan (network), čekam 15s...")
                self.desc_label.setText(f"🌐 Čekam network... ({attempt}/{max_attempts})")

                # Zakazi sledeći pokušaj
                QTimer.singleShot(wait_time, lambda: self.retryUpdateWeather(attempt + 1, max_attempts))
            else:
                print(f"❌ Svi pokušaji neuspešni! Network greška: {e}")
                self.desc_label.setText("❌ Nema konekcije")
                # ✅ Prikazi bar nešto umesto praznog
                temp_symbol = self.get_temp_symbol()
                self.temp_label.setText(f"--{temp_symbol}")
                self.weather_alert_label.setText("⚠️ Nema podataka")

            # Last updated / status texts (also translate when language changes)
            try:
                if hasattr(self, 'last_updated_label'):
                    if getattr(self, '_last_updated_time', None):
                        self.last_updated_label.setText(self.t("last_updated_fmt").format(self.format_time_short(self._last_updated_time)))
                    else:
                        self.last_updated_label.setText(self.t("last_updated_fmt").format("--:--"))
                if hasattr(self, 'offline_status_label') and self.offline_status_label.isVisible():
                    # Preserve whether it is sleep or offline message
                    if getattr(self, '_sleep_detected', False):
                        self.offline_status_label.setText(self.t("sleep_detected"))
                    else:
                        self.offline_status_label.setText(self.t("offline_waiting"))
            except Exception:
                pass

        except Exception as e:
            # ✅ Neka druga greška (API parse, itd.)
            print(f"❌ Greška pri ažuriranju: {type(e).__name__}: {e}")
            if attempt < max_attempts:
                wait_time = 15000
                print(f"⚠️ Pokušavam ponovo za 15s...")
                self.desc_label.setText(f"⚠️ Greška, pokušavam ponovo... ({attempt}/{max_attempts})")
                QTimer.singleShot(wait_time, lambda: self.retryUpdateWeather(attempt + 1, max_attempts))
            else:
                print(f"❌ Konačna greška nakon {max_attempts} pokušaja")
                self.desc_label.setText("❌ Greška - osvežite ručno")
                # ✅ Prikazi bar nešto umesto praznog
                temp_symbol = self.get_temp_symbol()
                self.temp_label.setText(f"--{temp_symbol}")
                self.weather_alert_label.setText("⚠️ Nema podataka")

    def translate_weather(self, description):
        """Prevedi opis vremena na srpsku latinicu"""
        translations = {
            # Oblačnost
            'clear sky': ('vedro', '☀️'),
            'few clouds': ('malo oblaka', '🌤️'),
            'scattered clouds': ('umereno oblačno', '⛅'),
            'broken clouds': ('oblačno', '☁️'),
            'overcast clouds': ('veoma oblačno', '☁️'),

            # Kiša
            'light rain': ('slaba kiša', '🌧️'),
            'moderate rain': ('umerena kiša', '🌧️'),
            'heavy intensity rain': ('jaka kiša', '🌧️'),
            'very heavy rain': ('veoma jaka kiša', '🌧️'),
            'extreme rain': ('ekstremna kiša', '🌧️'),
            'freezing rain': ('ledena kiša', '🌧️'),
            'light intensity shower rain': ('slabi pljuskovi', '🌦️'),
            'shower rain': ('pljuskovi', '🌦️'),
            'heavy intensity shower rain': ('jaki pljuskovi', '🌦️'),
            'ragged shower rain': ('povremeni pljuskovi', '🌦️'),

            # Grmljavina
            'thunderstorm with light rain': ('grmljavina sa slabom kišom', '⛈️'),
            'thunderstorm with rain': ('grmljavina sa kišom', '⛈️'),
            'thunderstorm with heavy rain': ('grmljavina sa jakom kišom', '⛈️'),
            'light thunderstorm': ('slaba grmljavina', '⛈️'),
            'thunderstorm': ('grmljavina', '⛈️'),
            'heavy thunderstorm': ('jaka grmljavina', '⛈️'),
            'ragged thunderstorm': ('povremena grmljavina', '⛈️'),
            'thunderstorm with light drizzle': ('grmljavina sa rosuljicom', '⛈️'),
            'thunderstorm with drizzle': ('grmljavina sa kišom', '⛈️'),
            'thunderstorm with heavy drizzle': ('grmljavina sa krupnom kišom', '⛈️'),

            # Rosulja
            'light intensity drizzle': ('slaba rosulja', '🌦️'),
            'drizzle': ('rosulja', '🌦️'),
            'heavy intensity drizzle': ('jaka rosulja', '🌦️'),
            'light intensity drizzle rain': ('slaba kiša', '🌧️'),
            'drizzle rain': ('kiša', '🌧️'),
            'heavy intensity drizzle rain': ('jaka kiša', '🌧️'),
            'shower rain and drizzle': ('pljuskovi i rosulja', '🌦️'),
            'heavy shower rain and drizzle': ('jaki pljuskovi', '🌦️'),
            'shower drizzle': ('pljuskovi', '🌦️'),

            # Sneg
            'light snow': ('slab sneg', '🌨️'),
            'snow': ('sneg', '❄️'),
            'heavy snow': ('jak sneg', '❄️'),
            'sleet': ('susnežica', '🌨️'),
            'light shower sleet': ('slabi pljuskovi susnežice', '🌨️'),
            'shower sleet': ('pljuskovi susnežice', '🌨️'),
            'light rain and snow': ('kiša sa snegom', '🌨️'),
            'rain and snow': ('kiša i sneg', '🌨️'),
            'light shower snow': ('slabi snežni pljuskovi', '🌨️'),
            'shower snow': ('snežni pljuskovi', '❄️'),
            'heavy shower snow': ('jaki snežni pljuskovi', '❄️'),

            # Atmosfera
            'mist': ('magla', '🌫️'),
            'smoke': ('dim', '🌫️'),
            'haze': ('izmaglica', '🌫️'),
            'sand dust whirls': ('peščani vihor', '🌪️'),
            'fog': ('magla', '🌫️'),
            'sand': ('pesak', '🌫️'),
            'dust': ('prašina', '🌫️'),
            'volcanic ash': ('vulkanski pepeo', '🌋'),
            'squalls': ('olujni vetar', '💨'),
            'tornado': ('tornado', '🌪️')
        }

        desc_lower = description.lower()
        if desc_lower in translations:
            return translations[desc_lower]  # (text, emoji)

        return (description.capitalize(), '🌡️')  # Fallback

    def getUVColor(self, uv_value):
        """Vrati boju za UV index"""
        if uv_value < 3:
            return "#4CAF50"
        elif uv_value < 6:
            return "#FFEB3B"
        elif uv_value < 8:
            return "#FF9800"
        elif uv_value < 11:
            return "#F44336"
        else:
            return "#9C27B0"

    def getAQIColor(self, aqi_index):
        """Vrati boju za Air Quality Index"""
        colors = {
            1: "#4CAF50",
            2: "#8BC34A",
            3: "#FFEB3B",
            4: "#FF9800",
            5: "#F44336"
        }
        return colors.get(aqi_index, "#999999")

    # ==============================
    # ✅ NOVO: DINAMIČKE BOJE ZA UPOZORENJA
    # ==============================
    def formatAlertText(self, text: str, max_chars_per_line: int = 22) -> tuple:
        """
        Formatira tekst upozorenja da UVEK stane u 2 reda i bude čitljiv.
        Vraća (formatted_text, font_size)
        """
        # Pokušaj sa normalnim fontom (12px)
        if len(text) <= max_chars_per_line * 2:
            # Staje u 2 reda sa 12px
            return (text, 12)
        
        # Pokušaj sa malo manjim fontom (11px) - više karaktera po liniji
        if len(text) <= (max_chars_per_line + 3) * 2:
            return (text, 11)
        
        # Ako je i dalje predugačak, skrati i dodaj "..."
        if len(text) > (max_chars_per_line + 3) * 2:
            # Skrati tekst da stane u 2 reda
            max_length = (max_chars_per_line + 3) * 2 - 3  # -3 za "..."
            
            # Pokušaj da seče na razmaku (lepše)
            if ' ' in text[:max_length]:
                # Nađi poslednji razmak pre limita
                cut_point = text[:max_length].rfind(' ')
                shortened = text[:cut_point] + "..."
            else:
                # Nema razmaka, seci tvrdo
                shortened = text[:max_length] + "..."
            
            return (shortened, 11)
        
        return (text, 12)

    def getAlertColorLevel(self, event_text: str) -> str:
        """
        Odredi nivo upozorenja na osnovu teksta (zeleno/žuto/crveno)
        Returns: 'green', 'yellow', 'red'
        """
        if not event_text:
            return 'green'
        
        sl = event_text.lower()
        
        # CRVENO - ekstremna opasnost
        red_keywords = [
            'red', 'crveno', 'extreme', 'ekstrem', 'severe', 'jak', 'danger', 'opasn',
            'tornado', 'hurricane', 'uragan', 'blizzard', 'mećava', 'heavy'
        ]
        
        # ŽUTO - upozorenje
        yellow_keywords = [
            'yellow', 'žuto', 'orange', 'narandžasto', 'warning', 'upozorenje',
            'advisory', 'preporuka', 'watch', 'praćenje', 'alert', 'uzbuna'
        ]
        
        # Proveri crveno prvo (prioritet)
        for keyword in red_keywords:
            if keyword in sl:
                return 'red'
        
        # Onda žuto
        for keyword in yellow_keywords:
            if keyword in sl:
                return 'yellow'
        
        # Ako ima ikakvo upozorenje, ali nije klasifikovano - žuto
        if any(word in sl for word in ['temperatura', 'temperature', 'kiša', 'rain', 'sneg', 'snow', 'vetar', 'wind']):
            return 'yellow'
        
        return 'green'

    # ==============================
    # ✅ NOVO: PREVOD UPOZORENJA (event) NA SRPSKI
    # ==============================
    def translate_alert_event(self, event_text: str) -> str:
        """
        Univerzalni prevod 'event' stringa u srpski (latinica).
        - Prepoznaje boju (yellow/orange/red/green)
        - Prepoznaje tip upozorenja (hladnoća, vrućina, vetar, kiša, sneg, oluja...)
        - Ako je nepoznato: prevede ključne engleske reči (fallback dictionary)
        """
        if not event_text:
            return "Upozorenje"

        original = event_text.strip()
        sl = original.lower()

        # Ako već ima srpska slova, tretiraj kao već prevedeno (ali boju možemo dodati ako je prisutna)
        has_sr = any(ch in original for ch in "čćšžđČĆŠŽĐ")

        # 1) BOJA / NIVO
        color_map = {
            "yellow": "žuto",
            "orange": "narandžasto",
            "red": "crveno",
            "green": "zeleno",
            "amber": "narandžasto",
        }
        detected_color = None
        for k, v in color_map.items():
            if re.search(rf"\b{k}\b", sl):
                detected_color = v
                break

        # 2) NORMALIZACIJA (skini boje i generičke reči)
        norm = sl
        for k in color_map.keys():
            norm = re.sub(rf"\b{k}\b", " ", norm)
        norm = re.sub(r"\b(warning|alert|advisory|watch|statement|notice)\b", " ", norm)
        norm = re.sub(r"[-_/]+", " ", norm)
        norm = re.sub(r"\s+", " ", norm).strip()

        # 3) PRAVILA (poznati tipovi) — specifično prvo
        rules = [
            (r"\bextreme cold\b|\bsevere cold\b", "ekstremna hladnoća"),
            (r"\blow temperature\b|\bvery low temperature\b|\bfrost\b", "niska temperatura / mraz"),
            (r"\bcold wave\b", "hladni talas"),
            (r"\bextreme heat\b|\bsevere heat\b", "ekstremna vrućina"),
            (r"\bhigh temperature\b|\bheat wave\b", "toplotni talas / visoka temperatura"),

            (r"\bfreezing rain\b", "ledena kiša"),
            (r"\bheavy rain\b|\btorrential rain\b|\bintense rain\b", "jaka kiša"),
            (r"\brain\b|\bdownpour\b", "kiša"),
            (r"\bice\b|\bblack ice\b|\bfreezing\b|\bglaze\b", "poledica / led"),

            (r"\bthunderstorm\b|\blightning\b", "grmljavina"),
            (r"\bsevere storm\b|\bstorm\b", "oluja"),
            (r"\bgale\b|\bstrong wind\b|\bhigh wind\b|\bwind\b", "jak vetar"),
            (r"\btornado\b", "tornado"),
            (r"\bhail\b", "grad (ledena zrna)"),

            (r"\bblizzard\b|\bheavy snow\b", "jak sneg / mećava"),
            (r"\bsnow\b", "sneg"),
            (r"\bsleet\b|\bwintry mix\b", "susnežica"),
            (r"\bdrifting snow\b|\bblowing snow\b", "vejavica"),

            (r"\bfog\b|\bmist\b|\bhaze\b", "magla / izmaglica"),
            (r"\bflash flood\b|\bflood\b", "poplava"),
            (r"\blandslide\b", "klizište"),
            (r"\bavalanche\b", "lavina"),
            (r"\bdust\b|\bsand\b", "prašina / pesak"),
            (r"\bsmoke\b", "dim"),
        ]

        translated = None
        for pattern, sr in rules:
            if re.search(pattern, norm):
                translated = sr
                break

        # 4) FALLBACK DICTIONARY (ako nije pogođeno pravilima)
        if not translated:
            if has_sr:
                translated = original
            else:
                replacements = [
                    ("low temperature", "niska temperatura"),
                    ("high temperature", "visoka temperatura"),
                    ("extreme cold", "ekstremna hladnoća"),
                    ("extreme heat", "ekstremna vrućina"),
                    ("cold wave", "hladni talas"),
                    ("heat wave", "toplotni talas"),
                    ("freezing rain", "ledena kiša"),
                    ("heavy rain", "jaka kiša"),
                    ("thunderstorm", "grmljavina"),
                    ("strong wind", "jak vetar"),
                    ("high wind", "jak vetar"),
                    ("wind", "vetar"),
                    ("rain", "kiša"),
                    ("snow", "sneg"),
                    ("sleet", "susnežica"),
                    ("blizzard", "mećava"),
                    ("fog", "magla"),
                    ("mist", "izmaglica"),
                    ("haze", "izmaglica"),
                    ("ice", "led / poledica"),
                    ("hail", "grad"),
                    ("flood", "poplava"),
                    ("landslide", "klizište"),
                    ("avalanche", "lavina"),
                    ("dust", "prašina"),
                    ("smoke", "dim"),
                    ("tornado", "tornado"),

                    ("warning", "upozorenje"),
                    ("alert", "uzbuna"),
                    ("advisory", "preporuka"),
                    ("watch", "praćenje"),
                    ("statement", "saopštenje"),
                    ("notice", "obaveštenje"),
                ]

                out = sl
                out = re.sub(r"[-_/]+", " ", out)
                out = re.sub(r"\s+", " ", out).strip()

                for a, b in replacements:
                    out = out.replace(a, b)

                out = re.sub(r"\s+", " ", out).strip()
                translated = out[:1].upper() + out[1:] if out else original

        # 5) DODAJ BOJU (ako je nađena)
        if detected_color and f"({detected_color})" not in translated:
            translated = f"{translated} ({detected_color})"

        return translated

    def changeWidgetSize(self, width, height, label):
        """Promeni veličinu widgeta"""
        for action in self.size_actions.values():
            action.setChecked(False)

        self.size_actions[label].setChecked(True)
        self.resize(width, height)

        self.settings.setValue('widget_size', label)
        self.settings.setValue('widget_width', width)
        self.settings.setValue('widget_height', height)

        self.widget_width = width
        self.widget_height = height
        self.widget_size_label = label

        self.tray_icon.showMessage(
            "Veličina Promenjena",
            f"Widget: {label}\n({width}x{height}px)",
            QSystemTrayIcon.Information,
            2000
        )

        print(f"📐 Widget resized to: {width}x{height} ({label})")

    def initTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.updateTrayIcon()

        tray_menu = QMenu()

        self.show_action = QAction("Prikaži Widget", self)
        self.show_action.triggered.connect(self.toggleWidget)

        self.startup_action = QAction("✓ Pokreni sa Windows-om", self)
        self.startup_action.setCheckable(True)
        self.startup_action.setChecked(False)
        self.startup_action.triggered.connect(self.toggleStartup)

        self.widget_only_action = QAction("Samo Widget (bez tray-a)", self)
        self.widget_only_action.triggered.connect(self.setWidgetOnlyMode)

        self.click_through_action = QAction("Click-Through Mode", self)
        self.click_through_action.setCheckable(True)
        self.click_through_action.setChecked(False)
        self.click_through_action.triggered.connect(self.toggleClickThrough)

        # Size selector submenu - Manuelni izbor rezolucije monitora
        self.size_menu = QMenu("Rezolucija Monitora", self)

        self.base_width = 420
        self.base_height = 900

        resolution_presets = {
            "XGA (1024x768)": 0.65,
            "WXGA (1280x800)": 0.75,
            "HD Ready (1366x768)": 0.80,
            "Full HD (1920x1080)": 1.0,
            "QHD (2560x1440)": 1.33,
            "4K UHD (3840x2160)": 2.0,
            "5K (5120x2880)": 2.67,
            "8K UHD (7680x4320)": 3.0
        }

        self.size_presets = {}
        self.size_actions = {}

        for label, scale_factor in resolution_presets.items():
            scaled_width = int(self.base_width * scale_factor)
            scaled_height = int(self.base_height * scale_factor)

            self.size_presets[label] = (scaled_width, scaled_height)

            action_label = f"{label} → {scaled_width}x{scaled_height}px"
            action = QAction(action_label, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, w=scaled_width, h=scaled_height, lbl=label: self.changeWidgetSize(w, h, lbl))
            self.size_actions[label] = action
            self.size_menu.addAction(action)

        if self.widget_size_label in self.size_actions:
            self.size_actions[self.widget_size_label].setChecked(True)
        else:
            if "Full HD (1920x1080)" in self.size_actions:
                self.size_actions["Full HD (1920x1080)"].setChecked(True)

        # ✅ NOVI: Language selector submenu
        self.language_menu = QMenu("🌐 Jezik / Language", self)
        
        self.language_actions = {}
        languages = {
            "sr": "🇷🇸 Srpski",
            "en": "🇬🇧 English"
        }
        
        for lang_code, lang_name in languages.items():
            action = QAction(lang_name, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, code=lang_code: self.changeLanguage(code))
            self.language_actions[lang_code] = action
            self.language_menu.addAction(action)
        
        # Postavi default (srpski)
        self.language_actions[self.current_language].setChecked(True)

        # ✅ NOVI: Temperature Unit selector submenu
        self.temp_unit_menu = QMenu("", self)  # Prazan - biće ažuriran u updateTrayMenuLanguage
        
        self.temp_unit_actions = {}
        temp_units = {
            "celsius": "Celsius (°C)",
            "fahrenheit": "Fahrenheit (°F)"
        }
        
        for unit_code, unit_name in temp_units.items():
            action = QAction(unit_name, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, code=unit_code: self.changeTemperatureUnit(code))
            self.temp_unit_actions[unit_code] = action
            self.temp_unit_menu.addAction(action)
        
        # Postavi default (celsius)
        self.temp_unit_actions[self.temperature_unit].setChecked(True)

        # ✅ NOVI: Time Format selector submenu
        self.time_format_menu = QMenu("", self)  # Prazan - biće ažuriran u updateTrayMenuLanguage
        
        self.time_format_actions = {}
        time_formats = {
            "24h": "24-hour (17:30)",
            "12h": "12-hour (05:30 PM)"
        }
        
        for format_code, format_name in time_formats.items():
            action = QAction(format_name, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, code=format_code: self.changeTimeFormat(code))
            self.time_format_actions[format_code] = action
            self.time_format_menu.addAction(action)
        
        # Postavi default (24h)
        self.time_format_actions[self.time_format].setChecked(True)

        # ✅ NOVI: Unit System selector submenu
        self.unit_system_menu = QMenu("", self)  # Prazan - biće ažuriran u updateTrayMenuLanguage
        
        self.unit_system_actions = {}
        unit_systems = {
            "metric": "Metric (km/h, mbar)",
            "imperial": "Imperial (mph, inHg)"
        }
        
        for system_code, system_name in unit_systems.items():
            action = QAction(system_name, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, code=system_code: self.changeUnitSystem(code))
            self.unit_system_actions[system_code] = action
            self.unit_system_menu.addAction(action)
        
        # Postavi default (metric)
        self.unit_system_actions[self.unit_system].setChecked(True)

        # ✅ NOVI: Location Source selector submenu
        self.location_source_menu = QMenu("📍 Izvor Lokacije", self)
        
        self.location_api_action = QAction("API Lokacija", self)
        self.location_api_action.setCheckable(True)
        self.location_api_action.triggered.connect(lambda: self.set_location_source('api'))
        
        self.location_windows_action = QAction("Windows Lokacija", self)
        self.location_windows_action.setCheckable(True)
        self.location_windows_action.triggered.connect(lambda: self.set_location_source('windows'))
        
        # Postavi default (API)
        if self.location_source == 'api':
            self.location_api_action.setChecked(True)
        else:
            self.location_windows_action.setChecked(True)
        
        self.location_source_menu.addAction(self.location_api_action)
        self.location_source_menu.addAction(self.location_windows_action)

        self.update_action = QAction("Osveži Vreme", self)
        self.update_action.triggered.connect(self.updateWeather)


        self.quit_action = QAction("Izađi", self)
        self.quit_action.triggered.connect(QApplication.quit)

        tray_menu.addAction(self.show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.startup_action)
        tray_menu.addAction(self.widget_only_action)
        tray_menu.addAction(self.click_through_action)
        tray_menu.addMenu(self.size_menu)
        tray_menu.addMenu(self.language_menu)  # ✅ DODATO: Language menu
        tray_menu.addMenu(self.temp_unit_menu)  # ✅ DODATO: Temperature Unit menu
        tray_menu.addMenu(self.time_format_menu)  # ✅ DODATO: Time Format menu
        tray_menu.addMenu(self.unit_system_menu)  # ✅ DODATO: Unit System menu
        tray_menu.addMenu(self.location_source_menu)  # ✅ DODATO: Location Source menu
        tray_menu.addSeparator()
        tray_menu.addAction(self.update_action)
        tray_menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.trayIconActivated)
        self.tray_icon.show()
        
        # ✅ Inicijalno postavi naslove menija (biće ažurirani u updateLanguageUI)
        self.temp_unit_menu.setTitle("🌡️ Temperature")
        self.time_format_menu.setTitle("🕐 Time")
        self.unit_system_menu.setTitle("📏 Units")

    def updateTrayIcon(self):
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)

        painter.setBrush(QColor(30, 60, 114))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(4, 4, 56, 56)

        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 18, QFont.Bold)
        painter.setFont(font)

        temp_text = self.current_temp if self.current_temp != "--" else "☀"
        painter.drawText(pixmap.rect(), Qt.AlignCenter, temp_text)

        painter.end()
        self.tray_icon.setIcon(QIcon(pixmap))

    def trayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggleWidget()

    def toggleWidget(self):
        if self.isVisible():
            self.hide()
            self.widget_visible = False
        else:
            self.show()
            self.widget_visible = True

    def mousePressEvent(self, event):
        if self.click_through:
            return
        if event.button() == Qt.LeftButton and not self.widget_locked:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.click_through:
            return
        if self.dragging and not self.widget_locked:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if self.click_through:
            return
        if event.button() == Qt.LeftButton:
            self.dragging = False
            if not self.widget_locked:
                self.saveSettings()

    def mouseDoubleClickEvent(self, event):
        if self.click_through:
            return

    def event(self, event):
        if self.click_through:
            if event.type() in [
                event.MouseButtonPress,
                event.MouseButtonRelease,
                event.MouseButtonDblClick,
                event.MouseMove
            ]:
                return True
        return super().event(event)

    def toggleLock(self):
        self.widget_locked = not self.widget_locked

        if self.widget_locked:
            self.lock_btn.setText("🔒")
            tooltip_text = "Otključaj poziciju" if self.current_language == "sr" else "Unlock position"
            msg_title = "Widget Zaključan" if self.current_language == "sr" else "Widget Locked"
            msg_text = "Pozicija je fiksirana" if self.current_language == "sr" else "Position is fixed"
            self.lock_btn.setToolTip(tooltip_text)
            self.tray_icon.showMessage(msg_title, msg_text, QSystemTrayIcon.Information, 2000)
        else:
            self.lock_btn.setText("🔓")
            tooltip_text = "Zaključaj poziciju" if self.current_language == "sr" else "Lock position"
            msg_title = "Widget Otključan" if self.current_language == "sr" else "Widget Unlocked"
            msg_text = "Možeš pomerati widget" if self.current_language == "sr" else "You can move the widget"
            self.lock_btn.setToolTip(tooltip_text)
            self.tray_icon.showMessage(msg_title, msg_text, QSystemTrayIcon.Information, 2000)

        self.saveSettings()

    def toggleClickThrough(self):
        self.click_through = self.click_through_action.isChecked()
        self.applyClickThroughMode(show_notification=True)  # Prikaži notifikaciju kada korisnik ručno klikne
        self.saveSettings()

    def applyClickThroughMode(self, show_notification=False):
        """✅ FIX: Primeni click-through mode sa proverom"""
        if self.click_through:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

            try:
                import ctypes
                hwnd = int(self.winId())
                GWL_EXSTYLE = -20
                WS_EX_TRANSPARENT = 0x00000020
                WS_EX_LAYERED = 0x00080000

                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TRANSPARENT | WS_EX_LAYERED)

                ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0004 | 0x0020)
                print("✅ Click-through mode primenjen")
            except Exception as e:
                print(f"❌ Windows style error: {e}")

            # Prikaži notifikaciju samo ako je show_notification=True
            if show_notification and hasattr(self, 'tray_icon'):
                self.tray_icon.showMessage(
                    self.t("clickthrough_enabled_title"), 
                    self.t("clickthrough_enabled_msg"), 
                    QSystemTrayIcon.Information, 
                    3000
                )
        else:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

            try:
                import ctypes
                hwnd = int(self.winId())
                GWL_EXSTYLE = -20
                WS_EX_TRANSPARENT = 0x00000020
                WS_EX_LAYERED = 0x00080000

                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                new_style = (style & ~WS_EX_TRANSPARENT) | WS_EX_LAYERED
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)

                SWP_NOMOVE = 0x0002
                SWP_NOSIZE = 0x0001
                SWP_NOZORDER = 0x0004
                SWP_FRAMECHANGED = 0x0020
                ctypes.windll.user32.SetWindowPos(
                    hwnd, 0, 0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED
                )

                self.hide()
                QTimer.singleShot(50, self.show)
                print("✅ Click-through mode isključen")

            except Exception as e:
                print(f"❌ Windows style error: {e}")

            # Prikaži notifikaciju samo ako je show_notification=True
            if show_notification and hasattr(self, 'tray_icon'):
                self.tray_icon.showMessage(
                    self.t("clickthrough_disabled_title"), 
                    self.t("clickthrough_disabled_msg"), 
                    QSystemTrayIcon.Information, 
                    2000
                )

    def toggleAutoLocation(self):
        self.use_auto_location = not self.use_auto_location
        if self.use_auto_location:
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(76, 175, 80, 0.6);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 8px 15px;
                    font-size: 12px;
                }
            """)
            self.location_input.setEnabled(False)
            self.updateWeather()
        else:
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(50, 60, 75, 0.6);
                    color: white;
                    border: 1px solid rgba(70, 130, 180, 0.4);
                    border-radius: 10px;
                    padding: 8px 15px;
                    font-size: 12px;
                }
            """)
            self.location_input.setEnabled(True)

        self.saveSettings()

    def changeRefreshInterval(self, index):
        intervals = [300000, 600000, 900000, 1800000, 3600000]
        self.refresh_interval = intervals[index]
        self.timer.stop()
        self.timer.start(self.refresh_interval)

        interval_names = ["5 minuta", "10 minuta", "15 minuta", "30 minuta", "60 minuta"]
        self.tray_icon.showMessage("Interval Promenjen", f"Vreme se sada osvežava svakih {interval_names[index]}", QSystemTrayIcon.Information, 2000)

        self.saveSettings()

    def searchLocation(self):
        location = self.location_input.text().strip()
        if location:
            self.current_location = location
            self.use_auto_location = False
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(50, 60, 75, 0.6);
                    color: white;
                    border: 1px solid rgba(70, 130, 180, 0.4);
                    border-radius: 10px;
                    padding: 8px 15px;
                    font-size: 12px;
                }
            """)
            self.saveSettings()
            self.updateWeather()

    def t(self, key):
        """Translation helper - returns translated text for current language"""
        return self.translations[self.current_language].get(key, key)
    
    def celsius_to_fahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    
    def format_temperature(self, temp_celsius):
        """Format temperature according to selected unit"""
        if self.temperature_unit == 'fahrenheit':
            temp_f = self.celsius_to_fahrenheit(temp_celsius)
            return f"{round(temp_f)}°F"
        else:
            return f"{round(temp_celsius)}°C"
    
    def get_temp_unit_param(self):
        """Get API parameter for temperature unit"""
        return "fahrenheit" if self.temperature_unit == 'fahrenheit' else "celsius"
    
    def get_temp_symbol(self):
        """Get temperature symbol (°C or °F)"""
        return "°F" if self.temperature_unit == 'fahrenheit' else "°C"
    
    def format_time(self, time_obj):
        """Format time according to selected format (12h or 24h)"""
        if self.time_format == '12h':
            return time_obj.strftime('%I:%M %p')  # 05:30 PM
        else:
            return time_obj.strftime('%H:%M')  # 17:30
    
    def format_time_short(self, time_obj):
        """Format time for compact display (no seconds)"""
        if self.time_format == '12h':
            return time_obj.strftime('%I:%M %p')  # 05:30 PM
        else:
            return time_obj.strftime('%H:%M')  # 17:30
    
    # ✅ Unit system helper functions
    def get_wind_unit_param(self):
        """Get API parameter for wind speed unit"""
        return "mph" if self.unit_system == 'imperial' else "kmh"
    
    def get_precipitation_unit_param(self):
        """Get API parameter for precipitation unit"""
        return "inch" if self.unit_system == 'imperial' else "mm"
    
    def get_wind_symbol(self):
        """Get wind speed symbol"""
        return "mph" if self.unit_system == 'imperial' else "km/h"
    
    def format_pressure(self, pressure_mbar):
        """Format pressure according to unit system"""
        if self.unit_system == 'imperial':
            # Convert mbar to inHg
            pressure_inhg = pressure_mbar * 0.02953
            return f"{pressure_inhg:.2f} inHg"
        else:
            return f"{pressure_mbar} mbar"
    
    def format_visibility(self, visibility_km):
        """Format visibility according to unit system - NO conversion needed, API handles it"""
        if self.unit_system == 'imperial':
            # API already returns different values for imperial - just show with mi symbol
            return f"{visibility_km:.1f} mi"
        else:
            return f"{visibility_km:.1f} km"
    
    def changeLanguage(self, lang_code):
        """Change widget language"""
        try:
            print(f"🌐 Menjam jezik na: {lang_code}")
            
            # Update language
            self.current_language = lang_code
            
            # Update checkmarks in menu
            for code, action in self.language_actions.items():
                action.setChecked(code == lang_code)
            
            # Refresh all text elements
            self.updateLanguageUI()
            
            # Refresh weather to get new translations
            self.updateWeather()
            
            # ✅ Save language preference
            self.saveSettings()
            
            # Show notification (using NEW language)
            msg_key = "lang_changed_msg_sr" if lang_code == "sr" else "lang_changed_msg_en"
            if hasattr(self, 'tray_icon'):
                self.tray_icon.showMessage(
                    self.t("lang_changed_title"),
                    self.t(msg_key),
                    QSystemTrayIcon.Information,
                    2000
                )
        except Exception as e:
            print(f"❌ Greška u changeLanguage: {e}")
            import traceback
            traceback.print_exc()
    
    def changeTemperatureUnit(self, unit_code):
        """Change temperature unit (Celsius/Fahrenheit)"""
        try:
            print(f"🌡️ Menjam jedinicu temperature na: {unit_code}")
            
            # Update temperature unit
            self.temperature_unit = unit_code
            
            # Update checkmarks in menu
            for code, action in self.temp_unit_actions.items():
                action.setChecked(code == unit_code)
            
            # Refresh weather to show new units
            self.updateWeather()
            
            # Save preference
            self.saveSettings()
            
            # Show notification
            unit_name = "Celsius (°C)" if unit_code == "celsius" else "Fahrenheit (°F)"
            if hasattr(self, 'tray_icon'):
                self.tray_icon.showMessage(
                    "Temperature Unit Changed" if self.current_language == "en" else "Jedinica Temperature Promenjena",
                    f"Temperature unit: {unit_name}",
                    QSystemTrayIcon.Information,
                    2000
                )
        except Exception as e:
            print(f"❌ Greška u changeTemperatureUnit: {e}")
            import traceback
            traceback.print_exc()
    
    def changeTimeFormat(self, format_code):
        """Change time format (12h/24h)"""
        try:
            print(f"🕐 Menjam format vremena na: {format_code}")
            
            # Update time format
            self.time_format = format_code
            
            # Update checkmarks in menu
            for code, action in self.time_format_actions.items():
                action.setChecked(code == format_code)
            
            # Refresh clock immediately
            self.updateClock()
            
            # Refresh weather to show new time format
            self.updateWeather()
            
            # Save preference
            self.saveSettings()
            
            # Show notification
            format_name = "24-hour" if format_code == "24h" else "12-hour (AM/PM)"
            if hasattr(self, 'tray_icon'):
                self.tray_icon.showMessage(
                    "Time Format Changed" if self.current_language == "en" else "Format Vremena Promenjen",
                    f"Time format: {format_name}",
                    QSystemTrayIcon.Information,
                    2000
                )
        except Exception as e:
            print(f"❌ Greška u changeTimeFormat: {e}")
            import traceback
            traceback.print_exc()
    
    def changeUnitSystem(self, system_code):
        """Change unit system (metric/imperial)"""
        try:
            print(f"📏 Menjam sistem merenja na: {system_code}")
            
            # Update unit system
            self.unit_system = system_code
            
            # Update checkmarks in menu
            for code, action in self.unit_system_actions.items():
                action.setChecked(code == system_code)
            
            # Refresh weather to show new units
            self.updateWeather()
            
            # Save preference
            self.saveSettings()
            
            # Show notification
            system_name = "Metric (km/h, mbar)" if system_code == "metric" else "Imperial (mph, inHg)"
            if hasattr(self, 'tray_icon'):
                self.tray_icon.showMessage(
                    "Unit System Changed" if self.current_language == "en" else "Sistem Merenja Promenjen",
                    f"Units: {system_name}",
                    QSystemTrayIcon.Information,
                    2000
                )
        except Exception as e:
            print(f"❌ Greška u changeUnitSystem: {e}")
            import traceback
            traceback.print_exc()

    
    def updateLanguageUI(self):
        """Update all static UI text elements to current language"""
        try:
            # Header elements
            self.interval_label.setText(self.t("refresh_interval"))
            self.location_input.setPlaceholderText(self.t("search_placeholder"))
            # Translate dynamic labels too (last updated / offline / sleep)
            if hasattr(self, 'last_updated_label'):
                if getattr(self, '_last_updated_time', None):
                    self.last_updated_label.setText(self.t('last_updated_fmt').format(self.format_time_short(self._last_updated_time)))
                else:
                    self.last_updated_label.setText(self.t('last_updated_fmt').format('--:--'))
            if hasattr(self, 'offline_status_label') and self.offline_status_label.isVisible():
                if getattr(self, '_sleep_detected', False):
                    self.offline_status_label.setText(self.t('sleep_detected'))
                else:
                    self.offline_status_label.setText(self.t('offline_waiting'))

            
            # Info panel labels
            self.feels_text.setText(self.t("feels_like"))
            self.humid_text.setText(self.t("humidity"))
            self.wind_text.setText(self.t("wind"))
            self.uv_text.setText(self.t("uv_index"))
            self.aqi_text.setText(self.t("air_quality"))
            
            # Row 3 labels
            self.pressure_text.setText(self.t("pressure"))
            self.clouds_text.setText(self.t("cloudiness"))
            self.visibility_text.setText(self.t("visibility"))
            
            # Sunrise/Sunset
            self.sunrise_text.setText(self.t("sunrise"))
            self.sunset_text.setText(self.t("sunset"))
            
            # Box titles
            self.precip_title.setText(self.t("precipitation_title"))
            self.hourly_forecast_title.setText(self.t("hourly_forecast_title"))
            self.forecast_5day_title.setText(self.t("forecast_5day_title"))
            
            # Update date format
            self.date_label.setText(self.format_date_serbian(datetime.now()))
            
            # Tray menu items
            self.show_action.setText(self.t("tray_show"))
            self.startup_action.setText(self.t("tray_startup"))
            self.widget_only_action.setText(self.t("tray_widget_only"))
            self.click_through_action.setText(self.t("tray_click_through"))
            self.size_menu.setTitle(self.t("tray_resolution"))
            
            # ✅ Ažuriraj naslove temperature, time i unit menija
            temp_icon = "🌡️"
            time_icon = "🕐"
            unit_icon = "📏"
            self.temp_unit_menu.setTitle(f"{temp_icon} {self.t('temperature_unit').replace(':', '')}")
            self.time_format_menu.setTitle(f"{time_icon} {self.t('time_format').replace(':', '')}")
            self.unit_system_menu.setTitle(f"{unit_icon} {self.t('unit_system').replace(':', '')}")
            
            # ✅ Ažuriraj tekstove opcija u Time Format meniju
            if self.current_language == "sr":
                self.time_format_actions["24h"].setText("24-satni (17:30)")
                self.time_format_actions["12h"].setText("12-satni (05:30 PM)")
            else:
                self.time_format_actions["24h"].setText("24-hour (17:30)")
                self.time_format_actions["12h"].setText("12-hour (05:30 PM)")
            
            # ✅ Ažuriraj tekstove opcija u Unit System meniju
            if self.current_language == "sr":
                self.unit_system_actions["metric"].setText("Metrički (km/h, mbar)")
                self.unit_system_actions["imperial"].setText("Imperijalni (mph, inHg)")
            else:
                self.unit_system_actions["metric"].setText("Metric (km/h, mbar)")
                self.unit_system_actions["imperial"].setText("Imperial (mph, inHg)")
            
            self.location_source_menu.setTitle(self.t("tray_location_source"))
            self.location_api_action.setText(self.t("location_api"))
            self.location_windows_action.setText(self.t("location_windows"))
            self.update_action.setText(self.t("tray_refresh"))
            self.quit_action.setText(self.t("tray_exit"))
            
            # Lock button
            if hasattr(self, 'lock_btn'):
                if self.widget_locked:
                    tooltip_text = "Otključaj poziciju" if self.current_language == "sr" else "Unlock position"
                    self.lock_btn.setToolTip(tooltip_text)
                else:
                    tooltip_text = "Zaključaj poziciju" if self.current_language == "sr" else "Lock position"
                    self.lock_btn.setToolTip(tooltip_text)
            
            print(f"✅ UI ažuriran na jezik: {self.current_language}")
            # Last updated / status texts (translate when language changes)
            if hasattr(self, 'last_updated_label'):
                if getattr(self, '_last_updated_time', None):
                    self.last_updated_label.setText(self.t('last_updated_fmt').format(self.format_time_short(self._last_updated_time)))
                else:
                    self.last_updated_label.setText(self.t('last_updated_fmt').format('--:--'))
            if hasattr(self, 'offline_status_label') and self.offline_status_label.isVisible():
                # Preserve whether it is sleep or offline message
                if getattr(self, '_sleep_detected', False):
                    self.offline_status_label.setText(self.t('sleep_detected'))
                else:
                    self.offline_status_label.setText(self.t('offline_waiting'))

        except Exception as e:
            print(f"❌ Greška u updateLanguageUI: {e}")
            import traceback
            traceback.print_exc()

    # ==============================
    # ✅ WINDOWS LOCATION FUNCTIONS
    # ==============================
    
    def check_windows_location_enabled(self):
        """Proveri da li je Windows Location servis uključen"""
        try:
            # ✅ Windows Location može biti blokiran globalno (HKLM) ili po-korisniku (HKCU).
            # Proveravamo oba da bismo pouzdano detektovali kada je Location Services ugašen.
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location"

            def _read_value(root):
                try:
                    k = winreg.OpenKey(root, key_path)
                    v, _ = winreg.QueryValueEx(k, "Value")
                    winreg.CloseKey(k)
                    return str(v)
                except Exception:
                    return None

            v_lm = _read_value(winreg.HKEY_LOCAL_MACHINE)
            v_cu = _read_value(winreg.HKEY_CURRENT_USER)

            # Ako je globalno Deny, tretiramo kao OFF bez obzira na HKCU
            if v_lm and v_lm.lower() == "deny":
                return False

            # Ako HKCU postoji i Deny -> OFF
            if v_cu and v_cu.lower() == "deny":
                return False

            # Ako imamo barem jedan Allow, tretiramo kao ON
            if (v_lm and v_lm.lower() == "allow") or (v_cu and v_cu.lower() == "allow"):
                return True

            # Ako ne možemo da pročitamo ili nema vrednosti, ponašamo se konzervativno
            return False
        except Exception as e:
            print(f"❌ Greška pri proveri Location servisa: {e}")
            return False

    def show_windows_location_disabled_popup(self):
        """Prikaži uputstvo (SR/EN) kako da se uključi Windows Location."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)

        if self.current_language == "sr":
            msg.setWindowTitle("Windows lokacija nije uključena")
            msg.setText("⚠️ Windows lokacija (Location services) je isključena!")
            msg.setInformativeText(
                "<b>Ako želiš da koristiš Windows lokaciju u widgetu:</b><br><br>"
                "1) Otvori <b>Podešavanja</b> (⊞ Win + I)<br>"
                "2) Idi na <b>Privatnost i bezbednost → Lokacija</b><br>"
                "3) Uključi <b>Usluge lokacije</b> (Location services)<br>"
                "4) Uključi i <b>Dozvoli aplikacijama pristup lokaciji</b><br><br>"
                "<i>Napomena: Nekad je potreban restart widgeta nakon promene.</i>"
            )
        else:
            msg.setWindowTitle("Windows Location Not Enabled")
            msg.setText("⚠️ Windows Location (Location services) is turned off!")
            msg.setInformativeText(
                "<b>If you want the widget to use Windows Location:</b><br><br>"
                "1) Open <b>Settings</b> (⊞ Win + I)<br>"
                "2) Go to <b>Privacy & Security → Location</b><br>"
                "3) Turn on <b>Location services</b><br>"
                "4) Enable <b>Let apps access your location</b><br><br>"
                "<i>Note: A widget restart may be required after changing this.</i>"
            )

        msg.exec_()

    def get_windows_location(self):
        """Dobij lokaciju iz Windows Location API-ja koristeći geocoder"""
        try:
            import geocoder
            
            print("🔍 Pokušavam da dobijem Windows Location (bez IP fallback-a)...")
            
            # ✅ POKUŠAJ SAMO Windows Location (bez IP fallback-a)
            # Ako korisnik izabere Windows Location, želimo PRAVU Windows lokaciju, ne IP
            try:
                g = geocoder.windows('me')
                
                if g.ok and g.latlng:
                    lat = g.latlng[0]
                    lon = g.latlng[1]
                    
                    print(f"✅ Windows Location uspešno: ({lat:.4f}, {lon:.4f})")
                    
                    # Dobij naziv grada preko Reverse Geocoding
                    city_name = self.get_city_from_coords(lat, lon)
                    
                    return lat, lon, city_name
                else:
                    print(f"❌ Windows Location nije vratio validne koordinate")
                    print(f"   g.ok = {g.ok}")
                    print(f"   g.latlng = {g.latlng if hasattr(g, 'latlng') else 'N/A'}")
                    return None, None, None
                    
            except AttributeError as e:
                # geocoder.windows() ne postoji
                print(f"⚠️ geocoder.windows() metod ne postoji: {e}")
                print("   Koristim IP geolocation kao alternativu...")
                
                # Fallback na IP geolocation (ali prijaviti ćemo korisniku)
                g = geocoder.ip('me')
                
                if g.ok and g.latlng:
                    lat = g.latlng[0]
                    lon = g.latlng[1]
                    
                    print(f"⚠️ Koristim IP location umesto Windows Location: ({lat:.4f}, {lon:.4f})")
                    
                    # Dobij naziv grada preko Reverse Geocoding
                    city_name = self.get_city_from_coords(lat, lon)
                    
                    # Označi da je ovo zapravo IP location, ne Windows Location
                    return lat, lon, city_name
                else:
                    return None, None, None
                    
            except Exception as e:
                print(f"❌ Windows Location greška: {e}")
                return None, None, None
                
        except ImportError:
            print("❌ 'geocoder' biblioteka nije instalirana. Instaliraj sa: pip install geocoder")
            return None, None, None
        except Exception as e:
            print(f"❌ Opšta greška u get_windows_location: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None

    def get_city_from_coords(self, lat, lon):
        """Reverse geocoding - dobij ime grada iz koordinata"""
        try:
            # ✅ UVEK koristi engleski (accept-language=en) da bi dobio latinicu
            # normalizeCityName() će kasnije primeniti pravilnu lokalizaciju
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=en"
            headers = {'User-Agent': 'WeatherWidget/2.0'}
            response = self.session.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                city = address.get('city') or address.get('town') or address.get('village', 'Unknown')
                
                # ✅ KONVERZIJA IZ ĆIRILICE U LATINICU (ako API vrati ćirilicu)
                if self.is_cyrillic(city):
                    original_name = city
                    city = self.cyrillic_to_latin(city)
                    print(f"🔤 Konvertovano: {original_name} -> {city}")
                
                return city
        except Exception as e:
            print(f"❌ Reverse geocoding greška: {e}")
        return "Unknown Location"

    def set_location_source(self, source):
        """Promeni izvor lokacije (api ili windows)"""
        if source == 'windows':
            # Proveri da li je Windows Location uključen
            if not self.check_windows_location_enabled():
                self.show_windows_location_disabled_popup()
                
                # Ostavi na API opciji
                self.location_api_action.setChecked(True)
                self.location_windows_action.setChecked(False)
                return
        
        # Sačuvaj izbor
        self.location_source = source
        self.settings.setValue('location_source', source)
        
        # Ažuriraj checkmarks
        self.location_api_action.setChecked(source == 'api')
        self.location_windows_action.setChecked(source == 'windows')
        
        # Ažuriraj tekst menu akcija prema jeziku
        self.location_source_menu.setTitle(self.t("tray_location_source"))
        self.location_api_action.setText(self.t("location_api"))
        self.location_windows_action.setText(self.t("location_windows"))
        
        # Osveži vreme sa novim izvorom
        self.updateWeather()
        
        source_text = "Windows Location" if source == "windows" else "API Location"
        print(f"✅ Location source promenjen na: {source_text}")

    def toggleStartup(self):
        import winreg
        import sys

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "WeatherWidget"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)

            if self.startup_action.isChecked():
                app_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{app_path}"')
                self.tray_icon.showMessage(
                    self.t("startup_enabled_title"), 
                    self.t("startup_enabled_msg"), 
                    QSystemTrayIcon.Information, 
                    2000
                )
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                    self.tray_icon.showMessage(
                        self.t("startup_disabled_title"), 
                        self.t("startup_disabled_msg"), 
                        QSystemTrayIcon.Information, 
                        2000
                    )
                except FileNotFoundError:
                    pass

            winreg.CloseKey(key)
        except Exception as e:
            print(f"Startup greška: {e}")

    def checkStartupStatus(self):
        """Proveri da li je aplikacija u Windows startup-u i postavi checkbox"""
        import winreg

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "WeatherWidget"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, app_name)
                winreg.CloseKey(key)
                self.startup_action.setChecked(True)
                print("✅ Startup je aktivan - checkbox postavljen")
                return True
            except FileNotFoundError:
                self.startup_action.setChecked(False)
                print("❌ Startup nije aktivan - checkbox očišćen")
                return False
        except Exception as e:
            print(f"⚠️ Greška pri proveri startup-a: {e}")
            self.startup_action.setChecked(False)
            return False

    def setWidgetOnlyMode(self):
        reply = QMessageBox.question(None, 'Widget-only Mode',
                                     'Sakriti tray ikonu?\n\nAplikacija će raditi samo kao desktop widget.\nMožeš zatvoriti Widget klikom na X dugme.',
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.tray_icon.hide()
            self.show()
            QApplication.setQuitOnLastWindowClosed(True)

    def loadSettings(self):
        self.widget_locked = self.settings.value('widget_locked', False, type=bool)
        self.click_through = self.settings.value('click_through', False, type=bool)
        self.use_auto_location = self.settings.value('use_auto_location', True, type=bool)
        self.current_location = self.settings.value('current_location', 'Belgrade', type=str)
        self.refresh_interval = self.settings.value('refresh_interval', 300000, type=int)
        self.current_language = self.settings.value('language', 'en', type=str)  # ✅ Load saved language

        self.widget_size_label = self.settings.value('widget_size', 'Full HD (1920x1080)', type=str)
        self.widget_width = self.settings.value('widget_width', 420, type=int)
        self.widget_height = self.settings.value('widget_height', 900, type=int)

        print(f"✅ Učitane postavke:")
        print(f"  - Locked: {self.widget_locked}")
        print(f"  - Click-through: {self.click_through}")
        print(f"  - Auto lokacija: {self.use_auto_location}")
        print(f"  - Lokacija: {self.current_location}")
        print(f"  - Size: {self.widget_size_label} ({self.widget_width}x{self.widget_height})")
        print(f"  - Jezik: {self.current_language}")  # ✅ Log language

    def saveSettings(self):
        self.settings.setValue('widget_locked', self.widget_locked)
        self.settings.setValue('click_through', self.click_through)
        self.settings.setValue('use_auto_location', self.use_auto_location)
        self.settings.setValue('current_location', self.current_location)
        self.settings.setValue('refresh_interval', self.refresh_interval)
        self.settings.setValue('language', self.current_language)  # ✅ Save language
        self.settings.setValue('temperature_unit', self.temperature_unit)  # ✅ Save temperature unit
        self.settings.setValue('time_format', self.time_format)  # ✅ Save time format
        self.settings.setValue('unit_system', self.unit_system)  # ✅ Save unit system
        self.settings.setValue('location_source', self.location_source)  # ✅ Save location source
        self.settings.setValue('window_x', self.x())
        self.settings.setValue('window_y', self.y())

        print(f"💾 Sačuvane postavke na poziciji: ({self.x()}, {self.y()}), jezik: {self.current_language}, temp: {self.temperature_unit}, time: {self.time_format}, units: {self.unit_system}")

    def restorePosition(self):
        x = self.settings.value('window_x', 100, type=int)
        y = self.settings.value('window_y', 100, type=int)
        self.move(x, y)
        print(f"📍 Pozicija vraćena na: ({x}, {y})")

        if self.widget_locked:
            self.lock_btn.setText("🔒")
            self.lock_btn.setToolTip("Otključaj poziciju")

        if self.click_through:
            self.click_through_action.setChecked(True)
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

            try:
                import ctypes
                hwnd = int(self.winId())
                GWL_EXSTYLE = -20
                WS_EX_TRANSPARENT = 0x00000020
                WS_EX_LAYERED = 0x00080000

                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TRANSPARENT | WS_EX_LAYERED)
            except:
                pass

        interval_index = [300000, 600000, 900000, 1800000, 3600000].index(self.refresh_interval) if self.refresh_interval in [300000, 600000, 900000, 1800000, 3600000] else 0
        self.interval_combo.setCurrentIndex(interval_index)

        if not self.use_auto_location:
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(50, 60, 75, 0.6);
                    color: white;
                    border: 1px solid rgba(70, 130, 180, 0.4);
                    border-radius: 10px;
                    padding: 8px 15px;
                    font-size: 12px;
                }
            """)
            self.location_input.setEnabled(True)
            self.location_input.setText(self.current_location)
        else:
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(76, 175, 80, 0.6);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 8px 15px;
                    font-size: 12px;
                }
            """)
            self.location_input.setEnabled(False)

        self.checkStartupStatus()

    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    def is_cyrillic(self, text):
        cyrillic_chars = set('абвгдђежзијклљмнњопрстћуфхцчџш')
        cyrillic_chars.update('АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ')
        return any(char in cyrillic_chars for char in text)

    def cyrillic_to_latin(self, text):
        """Konvertuj srpsku ćirilicu u latinicu"""
        cyrillic_map = {
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Ђ': 'Đ', 'Е': 'E',
            'Ж': 'Ž', 'З': 'Z', 'И': 'I', 'Ј': 'J', 'К': 'K', 'Л': 'L', 'Љ': 'Lj',
            'М': 'M', 'Н': 'N', 'Њ': 'Nj', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S',
            'Т': 'T', 'Ћ': 'Ć', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'Č',
            'Џ': 'Dž', 'Ш': 'Š',
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ђ': 'đ', 'е': 'e',
            'ж': 'ž', 'з': 'z', 'и': 'i', 'ј': 'j', 'к': 'k', 'л': 'l', 'љ': 'lj',
            'м': 'm', 'н': 'n', 'њ': 'nj', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
            'т': 't', 'ћ': 'ć', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'č',
            'џ': 'dž', 'ш': 'š'
        }
        
        result = ''
        for char in text:
            result += cyrillic_map.get(char, char)
        return result


    def normalizeCityName(self, city_name):
        """Normalize city name for display (capitalize properly)"""
        # City name mappings (English translations)
        city_translations = {
            "beograd": "Belgrade" if self.current_language == "en" else "Beograd",
            "belgrade": "Belgrade" if self.current_language == "en" else "Beograd",
            "novi sad": "Novi Sad",
            "niš": "Niš" if self.current_language == "sr" else "Nis",
            "nis": "Niš" if self.current_language == "sr" else "Nis",
            "kragujevac": "Kragujevac",
            "subotica": "Subotica",
            "zaječar": "Zaječar" if self.current_language == "sr" else "Zajecar",
            "zajecar": "Zaječar" if self.current_language == "sr" else "Zajecar",
            "zaje\u010dar": "Zaječar" if self.current_language == "sr" else "Zajecar",  # Unicode č
            "leskovac": "Leskovac",
            "čačak": "Čačak" if self.current_language == "sr" else "Cacak",
            "cacak": "Čačak" if self.current_language == "sr" else "Cacak",
            "smederevo": "Smederevo",
            "novi pazar": "Novi Pazar",
            "pancevo": "Pančevo" if self.current_language == "sr" else "Pancevo",
            "pančevo": "Pančevo" if self.current_language == "sr" else "Pancevo",
        }
        
        # Try lowercase lookup first
        normalized = city_translations.get(city_name.lower())
        if normalized:
            return normalized
        
        # Otherwise capitalize each word
        return city_name.title()
    
    def getCityCoordinates(self, city_name):
        """Dobij koordinate grada koristeći Open-Meteo Geocoding API"""
        try:
            # ✅ TRAŽI VIŠE REZULTATA (count=5) da nađemo pravi grad
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=5&language=sr&format=json"
            response = self.session.get(geo_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    result = None
                    
                    # ✅ PRIORITIZUJ SRBIJU - traži prvo RS
                    for r in data['results']:
                        if r.get('country_code') == 'RS':
                            result = r
                            print(f"✅ Našao grad u Srbiji: {r['name']} ({r['latitude']}, {r['longitude']})")
                            break
                    
                    # Ako nema u Srbiji, uzmi prvi rezultat
                    if not result:
                        result = data['results'][0]
                        print(f"ℹ️ Grad nije u Srbiji, koristim: {result['name']}, {result.get('country', 'N/A')}")
                    
                    city_name = result['name']
                    
                    # ✅ KONVERZIJA IZ ĆIRILICE U LATINICU (ako API vrati ćirilicu)
                    if self.is_cyrillic(city_name):
                        original_name = city_name
                        city_name = self.cyrillic_to_latin(city_name)
                        print(f"🔤 Konvertovano: {original_name} -> {city_name}")
                    
                    # Kompletna mapa srpskih gradova (latinica)
                    city_map = {
                        # Glavni gradovi
                        'Belgrade': 'Beograd', 'Beograd': 'Beograd',
                        'Novi Sad': 'Novi Sad', 'Niš': 'Niš', 'Nis': 'Niš',
                        'Kragujevac': 'Kragujevac', 'Subotica': 'Subotica', 'Zrenjanin': 'Zrenjanin',
                        
                        # Gradovi sa č, ć, š, ž, đ
                        'Pančevo': 'Pančevo', 'Pancevo': 'Pančevo', 
                        'Čačak': 'Čačak', 'Cacak': 'Čačak',
                        'Kruševac': 'Kruševac', 'Krusevac': 'Kruševac',
                        'Šabac': 'Šabac', 'Sabac': 'Šabac',
                        'Užice': 'Užice', 'Uzice': 'Užice',
                        'Zaječar': 'Zaječar', 'Zajecar': 'Zaječar',
                        'Požarevac': 'Požarevac', 'Pozarevac': 'Požarevac',
                        'Knjaževac': 'Knjaževac', 'Knjazevac': 'Knjaževac',
                        'Sremska Mitrovica': 'Sremska Mitrovica',
                        
                        # Ostali gradovi
                        'Leskovac': 'Leskovac', 'Valjevo': 'Valjevo', 'Smederevo': 'Smederevo',
                        'Sombor': 'Sombor', 'Pirot': 'Pirot', 'Kraljevo': 'Kraljevo',
                        'Vranje': 'Vranje', 'Kikinda': 'Kikinda', 'Prokuplje': 'Prokuplje',
                        'Jagodina': 'Jagodina', 'Bor': 'Bor', 'Negotin': 'Negotin',
                        'Paraćin': 'Paraćin', 'Paracin': 'Paraćin',
                        'Loznica': 'Loznica', 'Aranđelovac': 'Aranđelovac', 'Arandjelovac': 'Aranđelovac',
                        'Ruma': 'Ruma', 'Inđija': 'Inđija', 'Indjija': 'Inđija',
                        'Vršac': 'Vršac', 'Vrsac': 'Vršac',
                        'Aleksandrovac': 'Aleksandrovac', 'Bečej': 'Bečej', 'Becej': 'Bečej',
                        'Kovačica': 'Kovačica', 'Kovacica': 'Kovačica',
                        'Bačka Palanka': 'Bačka Palanka', 'Backa Palanka': 'Bačka Palanka',
                        'Bačka Topola': 'Bačka Topola', 'Backa Topola': 'Bačka Topola',
                        'Novi Pazar': 'Novi Pazar', 'Senta': 'Senta', 'Apatin': 'Apatin',
                        'Stari Grad': 'Beograd',  # Deo Beograda
                        'Zemun': 'Zemun', 'Semlin': 'Zemun',
                        
                        # Ako API vrati samo "Serbia" 
                        'Serbia': 'Beograd'
                    }

                    if city_name in city_map:
                        city_name = city_map[city_name]

                    return {
                        'city': city_name,
                        'lat': result['latitude'],
                        'lon': result['longitude'],
                        'country': result.get('country_code', 'RS')
                    }
                    
        except Exception as e:
            print(f"❌ Greška geocoding: {e}")
        
        return None

    
    def getAutoLocation(self):
        try:
            response = self.session.get('http://ip-api.com/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                lat = data.get('lat')
                lon = data.get('lon')
                city = data.get('city', 'Belgrade')
                return {'city': city, 'lat': lat, 'lon': lon}
        except:
            pass
        return {'city': 'Belgrade', 'lat': 44.8167, 'lon': 20.4667}

    def updateWeather(self):
        """Ažuriraj vremenske podatke sa Open-Meteo API"""
        # Ako smo u sleep recovery modu, ne radi regularni refresh (osim wake retry-a)
        if getattr(self, '_sleep_detected', False) and not getattr(self, '_wakeup_retry_in_progress', False):
            return

        try:
            location_data = None

            # ✅ NOVI: Proveri izvor lokacije
            if self.location_source == 'windows':
                # ✅ Ako je Windows Location ugašen (npr. korisnik ga isključi u Settings),
                # prikaži uputstvo na izabranom jeziku i prebaci na API fallback.
                if not self.check_windows_location_enabled():
                    if not getattr(self, '_windows_location_warning_shown', False):
                        self.show_windows_location_disabled_popup()
                        self._windows_location_warning_shown = True

                    # Prebaci na API source da widget nastavi da radi
                    self.location_source = 'api'
                    self.settings.setValue('location_source', 'api')
                    try:
                        self.location_api_action.setChecked(True)
                        self.location_windows_action.setChecked(False)
                    except Exception:
                        pass

                    # Nastavi sa API logikom ispod
                else:
                    # Ako je uključeno, resetuj flag da sledeći put opet može da upozori
                    self._windows_location_warning_shown = False

                # Koristi Windows Location (samo ako je i dalje izabrano)
                lat = lon = city = None
                if self.location_source == 'windows':
                    lat, lon, city = self.get_windows_location()
                
                if lat is None or lon is None:
                    print("❌ Ne mogu da dobijem Windows lokaciju, prelazim na API fallback")
                    # Fallback na API ako Windows Location ne radi
                    if self.use_auto_location:
                        location_data = self.getAutoLocation()
                        if location_data:
                            self.current_location = location_data['city']
                            lat, lon = location_data['lat'], location_data['lon']
                            city_name = location_data['city']
                    else:
                        location_data = self.getCityCoordinates(self.current_location)
                        if location_data:
                            lat, lon = location_data['lat'], location_data['lon']
                            city_name = location_data['city']
                        else:
                            self.desc_label.setText(f"❌ Grad '{self.current_location}' nije pronađen")
                            return
                else:
                    # Uspešno dobio Windows lokaciju
                    city_name = self.normalizeCityName(city)
                    self.city_label.setText(city_name)
                    print(f"✅ Windows Location: {city_name} ({lat:.4f}, {lon:.4f})")
                    
                    # ✅ KREIRAJ location_data dictionary za Windows Location
                    location_data = {
                        'city': city_name,
                        'lat': lat,
                        'lon': lon
                    }
            else:
                # Koristi API Location (default)
                if self.use_auto_location:
                    location_data = self.getAutoLocation()
                    if location_data:
                        self.current_location = location_data['city']
                else:
                    location_data = self.getCityCoordinates(self.current_location)
                    if not location_data:
                        self.desc_label.setText(f"❌ Grad '{self.current_location}' nije pronađen")
                        return

                if not location_data or 'lat' not in location_data:
                    self.desc_label.setText("❌ Greška pri lociranju")
                    return

                lat, lon = location_data['lat'], location_data['lon']
                city_name = location_data['city']

            print(f"🔄 Učitavam vreme za: {city_name}")

            # Open-Meteo Weather API
            # ✅ v2.1.5: Dodato minutely_15 za "nowcast" preciznost (0-2h)
            # ✅ v2.1.8: Dodato temperature_unit za Celsius/Fahrenheit izbor
            # ✅ v2.1.9: Dodato wind_speed_unit i precipitation_unit za Metric/Imperial izbor
            temp_unit_param = self.get_temp_unit_param()
            wind_unit_param = self.get_wind_unit_param()
            precip_unit_param = self.get_precipitation_unit_param()
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure,cloud_cover,rain,snowfall&minutely_15=precipitation,precipitation_probability,rain,showers,snowfall&hourly=temperature_2m,weather_code,precipitation_probability,precipitation,rain,showers,visibility&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max&temperature_unit={temp_unit_param}&wind_speed_unit={wind_unit_param}&precipitation_unit={precip_unit_param}&timezone=auto"
            
            try:
                response = self.session.get(weather_url, timeout=15)
            except requests.exceptions.RequestException as e:
                # Offline / DNS / timeout – ne diraj poslednje podatke, samo pokaži status
                print(f"❌ Mrežna greška: {e}")
                self.showOfflineStatus()
                return


            if response.status_code == 200:
                data = response.json()
                self.hideOfflineStatus()
                # ✅ Last updated timestamp (stays visible even when offline/sleep)
                self._last_updated_time = datetime.now()
                if hasattr(self, 'last_updated_label'):
                    self.last_updated_label.setText(self.t('last_updated_fmt').format(self.format_time_short(self._last_updated_time)))
                # Ako smo bili u sleep recovery modu, skloni status
                if getattr(self, '_sleep_detected', False):
                    self._sleep_detected = False
                    self._wake_backoff = 5
                    self.hideSleepStatus()
                
                current = data['current']
                
                temp = round(current['temperature_2m'], 1)
                feels = round(current['apparent_temperature'], 1)
                humidity = current['relative_humidity_2m']
                wind_speed = round(current['wind_speed_10m'] * 3.6, 1)
                wind_deg = current.get('wind_direction_10m', 0)
                wind_direction = self.getWindDirection(wind_deg)
                pressure = round(current['surface_pressure'])
                cloudiness = current['cloud_cover']
                
                weather_code = current['weather_code']
                
                # ✅ PRIORITET 1: Proveri da li ZAISTA pada nešto
                # Ovo će se poklapati sa "Kiša SADA!" u Padavine box-u!
                current_rain = current.get('rain', 0)
                current_snow = current.get('snowfall', 0)
                
                if current_rain > 0:
                    # Pada kiša - override weather_code!
                    weather_icon = "🌧️"
                    desc = "Kiša" if self.current_language == "sr" else "Rain"
                    print(f"   ✅ OPIS: Kiša (rain={current_rain}mm mereno)")
                elif current_snow > 0:
                    # Pada sneg - override weather_code!
                    weather_icon = "❄️"
                    desc = "Sneg" if self.current_language == "sr" else "Snow"
                    print(f"   ✅ OPIS: Sneg (snowfall={current_snow}mm mereno)")
                else:
                    # Normalno - koristi weather_code
                    weather_icon, desc = self.getWeatherDescription(weather_code)
                
                visibility = data['hourly']['visibility'][0] / 1000 if 'visibility' in data['hourly'] and data['hourly']['visibility'] else 10.0
                
                daily = data['daily']
                sunrise_iso = daily['sunrise'][0]
                sunset_iso = daily['sunset'][0]
                sunrise_time = datetime.fromisoformat(sunrise_iso)
                sunset_time = datetime.fromisoformat(sunset_iso)
                
                uv_value = round(daily['uv_index_max'][0], 1)
                
                self.current_temp = f"{int(temp)}°"
                self.city_label.setText(self.normalizeCityName(city_name))
                temp_symbol = self.get_temp_symbol()
                self.temp_label.setText(f"{weather_icon} {temp}{temp_symbol}")
                self.desc_label.setText(desc.capitalize())  # ✅ VELIKO SLOVO (oblačno → Oblačno)
                self.feels_label.setText(f"{feels}{temp_symbol}")
                self.humid_label.setText(f"{humidity}%")
                wind_symbol = self.get_wind_symbol()
                self.wind_label.setText(f"{wind_speed} {wind_symbol} {wind_direction}")
                self.pressure_label.setText(self.format_pressure(pressure))
                self.visibility_label.setText(self.format_visibility(visibility))
                self.clouds_label.setText(f"{cloudiness}%")
                self.sunrise_label.setText(self.format_time_short(sunrise_time))
                self.sunset_label.setText(self.format_time_short(sunset_time))
                
                uv_color = self.getUVColor(uv_value)
                self.uv_label.setText(f"{uv_value}")
                self.uv_label.setStyleSheet(f"color: {uv_color}; font-size: 16px; font-weight: bold;")
                
                self.updateAirQuality(lat, lon)
                self.updateTrayIcon()
                # ✅ Normalize city name and use translated desc for tray tooltip
                normalized_city = self.normalizeCityName(city_name)
                self.tray_icon.setToolTip(f"{normalized_city}: {temp}{temp_symbol}, {desc}")
                
                print(f"✅ Uspešno: {temp}{temp_symbol} - {desc}")
                
                self.update5DayForecast(data, location_data)
                
            else:
                # API greška - resetuj sve labele
                self.desc_label.setText(f"❌ API greška: {response.status_code}")
                temp_symbol = self.get_temp_symbol()
                self.temp_label.setText(f"--{temp_symbol}")
                error_text = "Greška" if self.current_language == "sr" else "Error"
                self.precip_alert_label.setText(f"⚠️ {error_text}")
                no_data_text = "Nema podataka" if self.current_language == "sr" else "No data"
                self.weather_alert_label.setText(f"⚠️ {no_data_text}")
                
                # ✅ Resetuj i 5-day prognozu
                for i in range(5):
                    self.forecast_labels[i]['day'].setText("---")
                    self.forecast_labels[i]['desc'].setText("---")
                    self.forecast_labels[i]['temp'].setText("--- / ---")
                
                print(f"❌ API greška: HTTP {response.status_code}")

        except Exception as e:
            # Exception - resetuj sve labele
            self.desc_label.setText(f"❌ Greška: {str(e)}")
            temp_symbol = self.get_temp_symbol()
            self.temp_label.setText(f"--{temp_symbol}")
            error_text = "Greška" if self.current_language == "sr" else "Error"
            self.precip_alert_label.setText(f"⚠️ {error_text}")
            no_data_text = "Nema podataka" if self.current_language == "sr" else "No data"
            self.weather_alert_label.setText(f"⚠️ {no_data_text}")
            
            # ✅ Resetuj i 5-day prognozu
            for i in range(5):
                self.forecast_labels[i]['day'].setText("---")
                self.forecast_labels[i]['desc'].setText("---")
                self.forecast_labels[i]['temp'].setText("--- / ---")
            
            print(f"❌ Greška: {e}")

    
    def update5DayForecast(self, weather_data, location_data):
        """Ažuriraj 5-dnevnu prognozu iz Open-Meteo podataka"""
        try:
            daily = weather_data['daily']
            
            for i in range(min(5, len(daily['time']))):
                date_str = daily['time'][i]
                temp_max = round(daily['temperature_2m_max'][i], 1)
                temp_min = round(daily['temperature_2m_min'][i], 1)
                weather_code = daily['weather_code'][i]
                
                weather_icon, desc = self.getWeatherDescription(weather_code)
                
                date_obj = datetime.fromisoformat(date_str)
                day_name = date_obj.strftime('%A').lower()
                
                # Translation key mapping
                day_key_map = {
                    'monday': 'monday',
                    'tuesday': 'tuesday',
                    'wednesday': 'wednesday',
                    'thursday': 'thursday',
                    'friday': 'friday',
                    'saturday': 'saturday',
                    'sunday': 'sunday'
                }
                
                day_key = day_key_map.get(day_name, day_name)
                day_translated = self.t(day_key).capitalize()  # "Pon" ili "Mon"
                date_display = date_obj.strftime('%d.%m')
                
                # ✅ CAPITALIZE description (oblačno → Oblačno)
                desc_capitalized = desc.capitalize() if desc else desc
                
                temp_symbol = self.get_temp_symbol()
                self.forecast_labels[i]['day'].setText(f"{day_translated} {date_display}")
                self.forecast_labels[i]['desc'].setText(f"{weather_icon} {desc_capitalized}")
                self.forecast_labels[i]['temp'].setText(f"{temp_min}{temp_symbol} / {temp_max}{temp_symbol}")
            
            print("✅ 5-dnevna prognoza ažurirana")
            
            if location_data:
                self.updateRainAlert(weather_data)
                self.updateHourlyForecast(weather_data)  # ✅ NOVA FUNKCIJA
            
        except Exception as e:
            print(f"❌ Greška pri 5-day prognozi: {e}")
            # ✅ Resetuj 5-day labele na fallback vrednosti
            for i in range(5):
                self.forecast_labels[i]['day'].setText("---")
                self.forecast_labels[i]['desc'].setText("---")
                self.forecast_labels[i]['temp'].setText("--- / ---")
            
            # ✅ Resetuj i padavine/hourly
            error_text = "Greška" if self.current_language == "sr" else "Error"
            self.precip_alert_label.setText(f"⚠️ {error_text}")
            no_data_text = "Nema podataka" if self.current_language == "sr" else "No data"
            self.weather_alert_label.setText(f"⚠️ {no_data_text}")

    def checkRainSoon(self, minutely_data):
        """
        ✅ v2.1.5: Proveri padavine u sledećih 2h (8 intervala x 15min)
        Ovo daje "nowcast" preciznost - kao radar!
        """
        if not minutely_data:
            return None
        
        times = minutely_data.get('time', [])
        probs = minutely_data.get('precipitation_probability', [])
        precip = minutely_data.get('precipitation', [])
        rain = minutely_data.get('rain', [])
        snowfall = minutely_data.get('snowfall', [])
        
        if not times or not probs:
            return None
        
        # ✅ NAĐI PRVI BUDUĆI INTERVAL (trenutno vreme ili kasnije)
        from datetime import datetime
        current_time = datetime.now()
        start_index = None
        
        for idx, time_str in enumerate(times):
            try:
                forecast_time = datetime.fromisoformat(time_str)
                if forecast_time >= current_time:
                    start_index = idx
                    break
            except:
                continue
        
        if start_index is None:
            return None  # Nema budućih intervala
        
        # Prvih 8 BUDUĆIH intervala = 2h (8 x 15min)
        for i in range(8):
            idx = start_index + i
            if idx >= len(times):
                break  # Nema više podataka
            
            prob = probs[idx] if idx < len(probs) else 0
            rain_val = rain[idx] if idx < len(rain) else 0
            snow_val = snowfall[idx] if idx < len(snowfall) else 0
            precip_val = precip[idx] if idx < len(precip) else 0
            
            # PRECIPITATION SOON ako:
            # - Verovatnoća >= 60% ILI
            # - Precipitation >= 0.1mm (stvarno pada kiša/sneg)
            if prob >= 60 or precip_val >= 0.1:
                minutes = (i + 1) * 15
                
                # ✅ Razlikuj kišu od snega!
                if snow_val > 0:
                    # SNEG!
                    if self.current_language == "sr":
                        if minutes < 60:
                            text = f"Sneg za {minutes} min ({prob}%)"
                        else:
                            hours = minutes // 60
                            remaining_min = minutes % 60
                            if remaining_min == 0:
                                text = f"Sneg za {hours}h ({prob}%)"
                            else:
                                text = f"Sneg za {hours}h {remaining_min}min ({prob}%)"
                    else:
                        if minutes < 60:
                            text = f"Snow in {minutes} min ({prob}%)"
                        else:
                            hours = minutes // 60
                            remaining_min = minutes % 60
                            if remaining_min == 0:
                                text = f"Snow in {hours}h ({prob}%)"
                            else:
                                text = f"Snow in {hours}h {remaining_min}min ({prob}%)"
                    
                    return ("snow_soon", text, prob)
                else:
                    # KIŠA ili generalna padavina
                    if self.current_language == "sr":
                        if minutes < 60:
                            text = f"Kiša za {minutes} min ({prob}%)"
                        else:
                            hours = minutes // 60
                            remaining_min = minutes % 60
                            if remaining_min == 0:
                                text = f"Kiša za {hours}h ({prob}%)"
                            else:
                                text = f"Kiša za {hours}h {remaining_min}min ({prob}%)"
                    else:
                        if minutes < 60:
                            text = f"Rain in {minutes} min ({prob}%)"
                        else:
                            hours = minutes // 60
                            remaining_min = minutes % 60
                            if remaining_min == 0:
                                text = f"Rain in {hours}h ({prob}%)"
                            else:
                                text = f"Rain in {hours}h {remaining_min}min ({prob}%)"
                    
                    return ("rain_soon", text, prob)
        
        # Proveri da li ima MOGUĆE kiše (30-59%)
        max_prob = max(probs[start_index:start_index+8]) if start_index is not None and start_index < len(probs) else 0
        if max_prob >= 30:
            if self.current_language == "sr":
                text = f"Moguća kiša ({max_prob}%)"
            else:
                text = f"Possible rain ({max_prob}%)"
            return ("possible", text, max_prob)
        
        # NO RAIN u sledećih 2h
        return None
    
    def updateRainAlert(self, weather_data):
        """Proveri padavine iz Open-Meteo hourly podataka"""
        try:
            hourly = weather_data.get('hourly', {})
            current = weather_data.get('current', {})
            
            if not hourly:
                self.precip_alert_label.setText(f"☀️ {self.t('no_precipitation')}")
                return
            
            # ✅ PRIORITET 1: Proveri da li ZAISTA pada nešto (current precipitation)
            # Ovo je tačnije od weather_code!
            current_rain = current.get('rain', 0)
            current_snow = current.get('snowfall', 0)
            
            if current_rain > 0:
                rain_text = "Kiša SADA!" if self.current_language == "sr" else "Rain NOW!"
                self.precip_alert_label.setText(f"🌧️ {rain_text}")
                print(f"   ✅ TRENUTNA KIŠA: rain={current_rain}mm (mereno!)")
                return
            
            if current_snow > 0:
                snow_text = "Sneg SADA!" if self.current_language == "sr" else "Snow NOW!"
                self.precip_alert_label.setText(f"❄️ {snow_text}")
                print(f"   ✅ TRENUTNI SNEG: snowfall={current_snow}mm (mereno!)")
                return
            
            # ✅ PRIORITET 2: Proveri weather_code (fallback ako nema rain/snow data)
            current_code = current.get('weather_code', 0)
            
            # Kiša kodovi: 51,53,55,56,57,61,63,65,66,67,80,81,82
            if current_code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
                rain_text = "Kiša SADA!" if self.current_language == "sr" else "Rain NOW!"
                self.precip_alert_label.setText(f"🌧️ {rain_text}")
                print(f"   ✅ TRENUTNA KIŠA: weather_code={current_code}")
                return
            
            # Sneg kodovi: 71,73,75,77,85,86
            elif current_code in [71, 73, 75, 77, 85, 86]:
                snow_text = "Sneg SADA!" if self.current_language == "sr" else "Snow NOW!"
                self.precip_alert_label.setText(f"❄️ {snow_text}")
                print(f"   ✅ TRENUTNI SNEG: weather_code={current_code}")
                return
            
            # Oluja kodovi: 95,96,99
            elif current_code in [95, 96, 99]:
                storm_text = "Oluja SADA!" if self.current_language == "sr" else "Storm NOW!"
                self.precip_alert_label.setText(f"⛈️ {storm_text}")
                print(f"   ✅ TRENUTNA OLUJA: weather_code={current_code}")
                return
            
            # ✅ PRIORITET 3: Proveri minutely_15 (nowcast 0-2h)
            minutely = weather_data.get('minutely_15', {})
            rain_soon = self.checkRainSoon(minutely)
            
            if rain_soon:
                alert_type, text, prob = rain_soon
                
                if alert_type == "rain_soon":
                    # Kiša uskoro (visoka verovatnoća)
                    self.precip_alert_label.setText(f"🌧️ {text}")
                    print(f"   ✅ KIŠA USKORO (nowcast): {text}")
                    return
                elif alert_type == "snow_soon":
                    # Sneg uskoro (visoka verovatnoća)
                    self.precip_alert_label.setText(f"❄️ {text}")
                    print(f"   ✅ SNEG USKORO (nowcast): {text}")
                    return
                elif alert_type == "possible":
                    # Moguća kiša (30-59%)
                    self.precip_alert_label.setText(f"🌦️ {text}")
                    print(f"   ⚠️ MOGUĆA KIŠA (nowcast): {text}")
                    return
            
            # ✅ PRIORITET 4: Proveri hourly (2-24h)
            times = hourly.get('time', [])
            weather_codes = hourly.get('weather_code', [])
            
            print(f"🔍 updateRainAlert debug:")
            print(f"   Trenutno vreme: {datetime.now().strftime('%H:%M:%S')}")
            print(f"   Current weather_code: {current_code} (nema padavina sada)")
            
            # ✅ Fallback: ako hourly weather_code nije u odgovoru, nemoj da padne u grešku.
            if not weather_codes or len(weather_codes) < len(times):
                # Open-Meteo ponekad vrati samo precipitation/rain bez weather_code.
                # U tom slučaju tretiramo sate sa rain/precipitation > 0 kao kišu (61).
                rain_arr = hourly.get('rain', [])
                precip_arr = hourly.get('precipitation', [])
                weather_codes = []
                for i in range(len(times)):
                    r = rain_arr[i] if i < len(rain_arr) else 0
                    p = precip_arr[i] if i < len(precip_arr) else 0
                    weather_codes.append(61 if (r > 0 or p > 0) else 0)
            
            current_time = datetime.now()
            
            for i, time_str in enumerate(times[:24]):
                forecast_time = datetime.fromisoformat(time_str)
                hours_until = round((forecast_time - current_time).total_seconds() / 3600)  # ✅ round umesto int
                
                # 🔍 DEBUG za prvih 6 sati
                if i < 6:
                    rain_val = hourly.get('rain', [])[i] if i < len(hourly.get('rain', [])) else 0
                    print(f"   [{i}] {time_str} → rain={rain_val:.2f}mm, hours={hours_until}, code={weather_codes[i]}")
                
                if hours_until <= 0:
                    continue
                
                code = weather_codes[i]
                
                # ✅ POBOLJŠANO: Uzmi u obzir i verovatnoću padavina!
                rain_val = hourly.get('rain', [])[i] if i < len(hourly.get('rain', [])) else 0
                precip_val = hourly.get('precipitation', [])[i] if i < len(hourly.get('precipitation', [])) else 0
                precip_prob = hourly.get('precipitation_probability', [])[i] if i < len(hourly.get('precipitation_probability', [])) else 0
                
                # ✅ OPTIMIZOVANO: 40% threshold kao Today Weather!
                # Empirijski test pokazao: Today Weather prikazuje od ~43%
                has_rain_risk = (precip_prob > 40) or (rain_val > 0) or (precip_val > 0)
                
                # ✅ KLJUČNO: Relaksiraj code proveru za VISOKE verovatnoće!
                # Problem: API ponekad kaže 75% kiša ali code = 3 (oblačno)
                # Rešenje: Ako je prob > 50%, prikaži bez obzira na code!
                code_check_passed = (code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]) or (precip_prob > 50)
                
                if has_rain_risk and code_check_passed:
                    if hours_until == 1:
                        # Prikaži verovatnoću ako postoji
                        if precip_prob > 0:
                            text = f"{self.t('rain_in')} 1h ({precip_prob}%)"
                        else:
                            text = f"{self.t('rain_in')} 1h"
                    else:
                        if precip_prob > 0:
                            text = f"{self.t('rain_in')} {hours_until}h ({precip_prob}%)"
                        else:
                            text = f"{self.t('rain_in')} {hours_until}h"
                    print(f"   ✅ PRONAĐENA KIŠA: {time_str} (za {hours_until}h, prob={precip_prob}%, rain={rain_val:.2f}mm)")
                    self.precip_alert_label.setText(f"🌧️ {text}")
                    return
                
                # Sneg: relaksiran code check za visoke verovatnoće
                elif has_rain_risk and ((code in [71, 73, 75, 77, 85, 86]) or (precip_prob > 50)):
                    if hours_until == 1:
                        if precip_prob > 0:
                            text = f"{self.t('snow_in')} 1h ({precip_prob}%)"
                        else:
                            text = f"{self.t('snow_in')} 1h"
                    else:
                        if precip_prob > 0:
                            text = f"{self.t('snow_in')} {hours_until}h ({precip_prob}%)"
                        else:
                            text = f"{self.t('snow_in')} {hours_until}h"
                    print(f"   ✅ PRONAĐEN SNEG: {time_str} (za {hours_until}h, prob={precip_prob}%, precip={precip_val:.2f}mm)")
                    self.precip_alert_label.setText(f"❄️ {text}")
                    return
                
                # Oluja: relaksiran code check za visoke verovatnoće
                elif has_rain_risk and ((code in [95, 96, 99]) or (precip_prob > 70)):
                    if hours_until == 1:
                        if precip_prob > 0:
                            text = f"{self.t('storm_in')} 1h ({precip_prob}%)"
                        else:
                            text = f"{self.t('storm_in')} 1h"
                    else:
                        if precip_prob > 0:
                            text = f"{self.t('storm_in')} {hours_until}h ({precip_prob}%)"
                        else:
                            text = f"{self.t('storm_in')} {hours_until}h"
                    print(f"   ✅ PRONAĐENA OLUJA: {time_str} (za {hours_until}h, prob={precip_prob}%, rain={rain_val:.2f}mm)")
                    self.precip_alert_label.setText(f"⛈️ {text}")
                    return
            
            self.precip_alert_label.setText(f"☀️ {self.t('no_precipitation')}")
            
            
        except Exception as e:
            print(f"❌ Rain alert greška: {e}")
            error_text = "Greška" if self.current_language == "sr" else "Error"
            self.precip_alert_label.setText(f"⚠️ {error_text}")

    def updateHourlyForecast(self, weather_data):
        """Ažuriraj satnu prognozu iz Open-Meteo hourly podataka"""
        try:
            hourly = weather_data.get('hourly', {})
            
            if not hourly:
                no_data_text = "Nema podataka" if self.current_language == "sr" else "No data"
                self.weather_alert_label.setText(f"⚠️ {no_data_text}")
                self.hourly_forecast_data = []
                return
            
            times = hourly.get('time', [])
            temps = hourly.get('temperature_2m', [])
            weather_codes = hourly.get('weather_code', [])
            precip_probs = hourly.get('precipitation_probability', [])
            
            # ✅ DEBUG: Proveri šta API vraća
            print(f"📊 API vratilo {len(weather_codes)} weather kodova")
            if len(weather_codes) > 0:
                print(f"   Primeri: {weather_codes[:5]}")
            
            current_time = datetime.now()
            print(f"   Trenutno vreme: {current_time}")
            print(f"   Prva 3 vremena iz API: {times[:3]}")
            
            self.hourly_forecast_data = []
            
            # ✅ UZMI DOVOLJNO SATI da garantujemo bar 12 budućih
            # Ako je kasno uveče (23:00), trebaće nam sati iz sledećeg dana
            max_hours_to_check = min(48, len(times))  # Proveri do 48h unapred
            skipped_count = 0
            
            for i in range(max_hours_to_check):
                try:
                    forecast_time = datetime.fromisoformat(times[i])
                    
                    # ✅ PRESKOČI prošle sate I trenutni sat
                    # Ako je sad 03:47, preskoči sve do 04:00 (sledeći pun sat)
                    if forecast_time <= current_time:
                        skipped_count += 1
                        continue
                    
                    # ✅ SIGURNOST: proveri da li weather_code postoji
                    weather_code = weather_codes[i] if i < len(weather_codes) and weather_codes[i] is not None else 0
                    
                    # ✅ DEBUG: Loguj prvi sat
                    if len(self.hourly_forecast_data) == 0:
                        print(f"   Preskočeno {skipped_count} prošlih sati")
                        print(f"   Prvi budući sat ({forecast_time.strftime('%H:%M')}): code={weather_code}, i={i}")
                    
                    weather_icon, desc = self.getWeatherDescription(weather_code)
                    
                    # ✅ SIGURNOST: proveri temp
                    temp = temps[i] if i < len(temps) and temps[i] is not None else 0
                    
                    # ✅ SIGURNOST: proveri precipitation
                    precip_prob = precip_probs[i] if i < len(precip_probs) and precip_probs[i] is not None else 0
                    
                    # ✅ ČUVAJ weather_code umesto desc (za prevođenje kasnije!)
                    time_str = self.format_time_short(forecast_time)
                    self.hourly_forecast_data.append({
                        'time': time_str,
                        'temp': round(temp),
                        'icon': weather_icon,
                        'weather_code': weather_code,  # ✅ Čuvaj code!
                        'precip_prob': round(precip_prob)
                    })
                    
                    # ✅ PRESTANI kad skupiš 12 budućih sati
                    if len(self.hourly_forecast_data) >= 12:
                        break
                        
                except Exception as inner_e:
                    print(f"❌ Greška pri parsiranju sata {i}: {inner_e}")
                    continue
            
            # Prikaži SLEDEĆI sat u labelu (index 0 jer smo već preskočili trenutni)
            if self.hourly_forecast_data:
                next_hour = self.hourly_forecast_data[0]
                time_str = next_hour['time']
                temp = next_hour['temp']
                icon = next_hour['icon']
                precip = next_hour['precip_prob']
                code = next_hour['weather_code']  # ✅ Uzmi weather_code
                
                # ✅ Odredi tip padavine na osnovu weather_code
                snow_codes = [71, 73, 75, 77, 85, 86]
                
                if code in snow_codes:
                    # SNEG!
                    precip_label = "snow" if self.current_language == "en" else "sneg"
                else:
                    # KIŠA (default)
                    precip_label = "rain" if self.current_language == "en" else "kiša"
                
                # Tekst za label - kompaktan prikaz
                temp_symbol = self.get_temp_symbol()
                if precip > 50:
                    label_text = f"{time_str}: {icon} {temp}{temp_symbol} ({precip_label} {precip}%)"
                else:
                    label_text = f"{time_str}: {icon} {temp}{temp_symbol}"
                
                self.weather_alert_label.setText(label_text)
                print(f"✅ Satna prognoza: {label_text} (ukupno {len(self.hourly_forecast_data)} sati)")
            else:
                no_forecast_text = "Nema prognoze" if self.current_language == "sr" else "No forecast"
                self.weather_alert_label.setText(f"⚠️ {no_forecast_text}")
                
        except Exception as e:
            print(f"❌ Hourly forecast greška: {e}")
            error_text = "Greška" if self.current_language == "sr" else "Error"
            self.weather_alert_label.setText(f"⚠️ {error_text}")
            self.hourly_forecast_data = []

    

    # ==============================
    # ✅ IZMENJENO: prevod upozorenja u box-u + DINAMIČKA BOJA
    # ==============================
    def getWeatherDescription(self, code):
        """Prevedi WMO weather code u emoji i opis (prema trenutnom jeziku)"""
        # Mapping WMO code → translation key
        weather_key_map = {
            0: "clear",
            1: "mostly_clear",
            2: "partly_cloudy",
            3: "cloudy",
            45: "fog",
            48: "fog_frost",
            51: "light_rain",
            53: "rain",
            55: "heavy_rain",
            56: "freezing_rain",
            57: "heavy_freezing_rain",
            61: "light_rain",
            63: "rain",
            65: "heavy_rain",
            66: "freezing_rain",
            67: "heavy_freezing_rain",
            71: "light_snow",
            73: "snow",
            75: "heavy_snow",
            77: "snow_grains",
            80: "light_showers",
            81: "showers",
            82: "heavy_showers",
            85: "snow_showers",
            86: "snow_showers",
            95: "thunderstorm",
            96: "thunderstorm_hail",
            99: "heavy_thunderstorm_hail"
        }
        
        # Icon mapping (nezavisan od jezika)
        icon_map = {
            0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
            45: "🌫️", 48: "🌫️",
            51: "🌦️", 53: "🌧️", 55: "🌧️", 56: "🌧️", 57: "🌧️",
            61: "🌦️", 63: "🌧️", 65: "🌧️", 66: "🌧️", 67: "🌧️",
            71: "🌨️", 73: "❄️", 75: "❄️", 77: "❄️",
            80: "🌦️", 81: "🌧️", 82: "⛈️",
            85: "🌨️", 86: "❄️",
            95: "⛈️", 96: "⛈️", 99: "⛈️"
        }
        
        icon = icon_map.get(code, "🌤️")
        desc_key = weather_key_map.get(code, "clear")
        desc = self.t(desc_key)
        
        return (icon, desc)

    def updateAirQuality(self, lat, lon):
        """Ažuriraj kvalitet vazduha sa Open-Meteo Air Quality API"""
        try:
            aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
            
            response = self.session.get(aqi_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})
                
                aqi = current.get('european_aqi', None)
                
                if aqi is not None:
                    if aqi <= 20:
                        category, aqi_color = self.t("aqi_excellent"), "#4CAF50"
                    elif aqi <= 40:
                        category, aqi_color = self.t("aqi_good"), "#8BC34A"
                    elif aqi <= 60:
                        category, aqi_color = self.t("aqi_moderate"), "#FFC107"
                    elif aqi <= 80:
                        category, aqi_color = self.t("aqi_poor"), "#FF9800"
                    else:
                        category, aqi_color = self.t("aqi_very_poor"), "#F44336"
                    
                    self.aqi_label.setText(category)
                    self.aqi_label.setStyleSheet(f"color: {aqi_color}; font-size: 16px; font-weight: bold;")
                    
                    self.pollutants_data = {
                        'pm10': current.get('pm10', 0),
                        'pm2_5': current.get('pm2_5', 0),
                        'co': current.get('carbon_monoxide', 0),
                        'no2': current.get('nitrogen_dioxide', 0),
                        'so2': current.get('sulphur_dioxide', 0),
                        'o3': current.get('ozone', 0)
                    }
                    
                    print(f"✅ Kvalitet vazduha: {category} (AQI: {aqi})")
                else:
                    self.aqi_label.setText("--")
                    self.pollutants_data = {}
                    
        except Exception as e:
            print(f"❌ AQI greška: {e}")
            self.aqi_label.setText("--")
            self.pollutants_data = {}

    # updateWeatherAlertsBox više nije potrebna - koristimo updateHourlyForecast
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # ✅ POSTAVI TAMNU POZADINU ZA SVE TOOLTIPS
    app.setStyleSheet("""
        QToolTip {
            background-color: #0F141E;
            color: #ECEFF1;
            border: 1px solid #90CAF9;
            padding: 8px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 11px;
        }
    """)

    weather = WeatherWidget()
    weather.show()

    sys.exit(app.exec_())