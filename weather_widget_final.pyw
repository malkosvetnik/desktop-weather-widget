import sys
import requests
import json
import os
import re
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QSystemTrayIcon,
                             QMenu, QAction, QLineEdit, QComboBox, QMessageBox, QToolTip,
                             QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer, QPoint, QSettings, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QCursor


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
        self.full_alert_text = ""  # ✅ Pun tekst upozorenja za tooltip

        # Proveri da li postoji API key
        saved_api_key = self.settings.value('api_key', '', type=str)

        if not saved_api_key:
            # First run - prikaži API key setup dialog
            api_key = self.showAPIKeyDialog()
            if not api_key:
                # Korisnik je zatvorio dialog bez unosa - izađi
                QMessageBox.critical(None, 'API Key Required',
                                     'Weather Widget zahteva OpenWeatherMap API key.\n\n'
                                     'Aplikacija će se zatvoriti.')
                sys.exit(0)
            self.api_key = api_key
            self.settings.setValue('api_key', api_key)
        else:
            self.api_key = saved_api_key

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

        self.initUI()
        self.initTray()

        # Učitaj poziciju
        self.restorePosition()

        self.updateWeather()

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

    def showAPIKeyDialog(self):
        """Prikaži dialog za unos API key-a (first run)"""
        custom_dialog = QDialog()
        custom_dialog.setWindowTitle('Weather Widget - API Key Setup')
        custom_dialog.setModal(True)
        custom_dialog.setMinimumWidth(500)

        layout = QVBoxLayout()

        # Naslov
        title = QLabel('<b>🌤️ Dobrodošli u Weather Widget!</b>')
        title.setStyleSheet('font-size: 16px; padding: 10px;')
        layout.addWidget(title)

        # Instrukcije
        instructions = QLabel(
            'Za korišćenje aplikacije potreban vam je <b>besplatan</b> OpenWeatherMap API ključ.<br><br>'
            '<b>Kako dobiti API key:</b><br>'
            '1. Posetite: <a href="https://openweathermap.org/api">https://openweathermap.org/api</a><br>'
            '2. Kliknite "Get API Key" i napravite besplatan nalog<br>'
            '3. Nakon prijave, idite u "API Keys" sekciju<br>'
            '4. Kopirajte vaš API ključ i zalepite ga ovde:<br>'
        )
        instructions.setWordWrap(True)
        instructions.setOpenExternalLinks(True)
        instructions.setTextFormat(Qt.RichText)
        instructions.setStyleSheet('padding: 10px; line-height: 1.5;')
        layout.addWidget(instructions)

        # Input field
        api_input = QLineEdit()
        api_input.setPlaceholderText('Zalepite vaš API key ovde...')
        api_input.setStyleSheet('''
            QLineEdit {
                padding: 10px;
                font-size: 13px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
            }
        ''')
        layout.addWidget(api_input)

        # Note
        note = QLabel(
            '<i>💡 Napomena: API key je potpuno besplatan. Aktivacija može potrajati 10-15 minuta.</i>'
        )
        note.setWordWrap(True)
        note.setStyleSheet('color: #666; padding: 10px; font-size: 11px;')
        layout.addWidget(note)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(custom_dialog.accept)
        button_box.rejected.connect(custom_dialog.reject)
        layout.addWidget(button_box)

        custom_dialog.setLayout(layout)

        # Prikaži dialog
        result = custom_dialog.exec_()

        if result == QDialog.Accepted:
            api_key = api_input.text().strip()
            if api_key:
                return api_key

        return None

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
        interval_label = QLabel("Osvežavanje:")
        interval_label.setStyleSheet("color: white; font-size: 12px;")

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

        header.addWidget(interval_label)
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

        # Sat
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        container_layout.addWidget(self.clock_label)

        # Datum
        self.date_label = QLabel(self.format_date_serbian(datetime.now()))
        self.date_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px;")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        container_layout.addWidget(self.date_label)

        container_layout.addSpacing(15)

        # Temperatura
        self.temp_label = QLabel("--°C")
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

        container_layout.addSpacing(15)

        # Info panel - PRVI RED (Oseća se, Vlažnost, Vetar sa pravcem)
        info_panel_1 = QHBoxLayout()

        # Oseća se kao
        feels_box = QVBoxLayout()
        self.feels_label = QLabel("--°C")
        self.feels_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.feels_label.setAlignment(Qt.AlignCenter)
        self.feels_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        feels_text = QLabel("Oseća se kao")
        feels_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        feels_text.setAlignment(Qt.AlignCenter)
        feels_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        feels_box.addWidget(self.feels_label)
        feels_box.addWidget(feels_text)

        # Vlažnost
        humid_box = QVBoxLayout()
        self.humid_label = QLabel("--%")
        self.humid_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.humid_label.setAlignment(Qt.AlignCenter)
        self.humid_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        humid_text = QLabel("Vlažnost")
        humid_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        humid_text.setAlignment(Qt.AlignCenter)
        humid_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        humid_box.addWidget(self.humid_label)
        humid_box.addWidget(humid_text)

        # Vetar SA PRAVCEM
        wind_box = QVBoxLayout()
        self.wind_label = QLabel("-- km/h")
        self.wind_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.wind_label.setAlignment(Qt.AlignCenter)
        self.wind_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        wind_text = QLabel("Vetar")
        wind_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        wind_text.setAlignment(Qt.AlignCenter)
        wind_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        wind_box.addWidget(self.wind_label)
        wind_box.addWidget(wind_text)

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
        uv_text = QLabel("☀️ UV Index")
        uv_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        uv_text.setAlignment(Qt.AlignCenter)
        uv_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        uv_box.addWidget(self.uv_label)
        uv_box.addWidget(uv_text)

        # Air Quality (Zagađenje) - sa interaktivnim tooltip-om
        aqi_box = QVBoxLayout()
        self.aqi_label = ClickableLabel("--")
        self.aqi_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.aqi_label.setAlignment(Qt.AlignCenter)
        self.aqi_label.clicked.connect(self.showPollutantsTooltip)
        aqi_text = QLabel("🌫️ Zagađenje")
        aqi_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        aqi_text.setAlignment(Qt.AlignCenter)
        aqi_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        aqi_box.addWidget(self.aqi_label)
        aqi_box.addWidget(aqi_text)

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
        pressure_text = QLabel("📊 Pritisak")
        pressure_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        pressure_text.setAlignment(Qt.AlignCenter)
        pressure_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        pressure_box.addWidget(self.pressure_label)
        pressure_box.addWidget(pressure_text)

        # Oblačnost
        clouds_box = QVBoxLayout()
        self.clouds_label = QLabel("--%")
        self.clouds_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.clouds_label.setAlignment(Qt.AlignCenter)
        self.clouds_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        clouds_text = QLabel("☁️ Oblačnost")
        clouds_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        clouds_text.setAlignment(Qt.AlignCenter)
        clouds_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        clouds_box.addWidget(self.clouds_label)
        clouds_box.addWidget(clouds_text)

        # Vidljivost
        visibility_box = QVBoxLayout()
        self.visibility_label = QLabel("-- km")
        self.visibility_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.visibility_label.setAlignment(Qt.AlignCenter)
        self.visibility_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        visibility_text = QLabel("👁️ Vidljivost")
        visibility_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        visibility_text.setAlignment(Qt.AlignCenter)
        visibility_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        visibility_box.addWidget(self.visibility_label)
        visibility_box.addWidget(visibility_text)

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
        sunrise_text = QLabel("🌅 Izlazak")
        sunrise_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        sunrise_text.setAlignment(Qt.AlignCenter)
        sunrise_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        sunrise_box.addWidget(self.sunrise_label)
        sunrise_box.addWidget(sunrise_text)

        # Sunset
        sunset_box = QVBoxLayout()
        self.sunset_label = QLabel("--:--")
        self.sunset_label.setStyleSheet("color: #FF6B35; font-size: 18px; font-weight: bold;")
        self.sunset_label.setAlignment(Qt.AlignCenter)
        self.sunset_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        sunset_text = QLabel("🌇 Zalazak")
        sunset_text.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        sunset_text.setAlignment(Qt.AlignCenter)
        sunset_text.setAttribute(Qt.WA_TransparentForMouseEvents)
        sunset_box.addWidget(self.sunset_label)
        sunset_box.addWidget(sunset_text)

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

        self.precip_alert_label = QLabel("Učitavam...")
        self.precip_alert_label.setStyleSheet("color: white; font-size: 11px;")
        self.precip_alert_label.setAlignment(Qt.AlignCenter)
        self.precip_alert_label.setWordWrap(True)
        self.precip_alert_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        precip_layout.addWidget(precip_title)
        precip_layout.addWidget(self.precip_alert_label)

        # KVADRAT 2: Weather Alerts
        self.alerts_box = QWidget()
        self.alerts_box.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 152, 0, 0.3);
                border-radius: 8px;
                border: 1px solid rgba(255, 152, 0, 0.5);
                padding: 8px;
            }
        """)
        alerts_layout = QVBoxLayout(self.alerts_box)
        alerts_layout.setContentsMargins(8, 8, 8, 8)
        alerts_layout.setSpacing(3)

        alerts_title = QLabel("⚠️ UPOZORENJA")
        alerts_title.setStyleSheet("color: #FFB74D; font-size: 11px; font-weight: bold;")
        alerts_title.setAlignment(Qt.AlignCenter)
        alerts_title.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.weather_alert_label = ClickableLabel("Učitavam...")
        self.weather_alert_label.setStyleSheet("color: white; font-size: 11px; line-height: 1.3;")
        self.weather_alert_label.setAlignment(Qt.AlignCenter)
        self.weather_alert_label.setWordWrap(True)
        self.weather_alert_label.setFixedHeight(32)  # ✅ FIKSNO 2 reda (11px * 1.3 line-height * 2)
        self.weather_alert_label.clicked.connect(self.showAlertTooltip)  # ✅ TOOLTIP!

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
        print("🖱️ Kliknut Zagađenje label!")  # Debug

        if not self.pollutants_data:
            tooltip_text = "<b>⚠️ Nema dostupnih podataka o polutantima</b>"
            QToolTip.showText(QCursor.pos(), tooltip_text, None)
            print("❌ Nema pollutants_data")
            return

        tooltip_text = "<div style='background-color: rgba(30, 35, 45, 0.95); padding: 10px; border-radius: 5px;'>"
        tooltip_text += "<b style='color: #4CAF50; font-size: 14px;'>🧪 Detaljni polutanti:</b><br><br>"

        pollutants = [
            ("CO", "Ugljen-monoksid", "μg/m³"),
            ("NO₂", "Azot-dioksid", "μg/m³"),
            ("O₃", "Ozon", "μg/m³"),
            ("SO₂", "Sumpor-dioksid", "μg/m³"),
            ("PM2.5", "Fine čestice", "μg/m³"),
            ("PM10", "Krupne čestice", "μg/m³"),
            ("NH₃", "Amonijak", "μg/m³")
        ]

        for code, name, unit in pollutants:
            key = code.replace("₂", "2").replace("₃", "3").replace(".", "_").lower()
            if key in self.pollutants_data:
                value = self.pollutants_data[key]
                tooltip_text += f"<b style='color: white;'>{code}</b> <span style='color: #AAA;'>({name}):</span> <span style='color: #4CAF50;'>{value:.1f} {unit}</span><br>"

        tooltip_text += "</div>"

        print(f"✅ Prikazujem tooltip sa {len(self.pollutants_data)} polutanata")
        # Tooltip će ostati dok je miš na labelu (bez timera)
        QToolTip.showText(QCursor.pos(), tooltip_text, self.aqi_label)

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
            start_time = datetime.fromtimestamp(alert['start']).strftime('%d.%m. %H:%M')
            end_time = datetime.fromtimestamp(alert['end']).strftime('%d.%m. %H:%M')
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
        directions = ['S', 'SI', 'I', 'JI', 'J', 'JZ', 'Z', 'SZ']
        index = round(degrees / 45) % 8
        return directions[index]

    def format_date_serbian(self, date):
        """Formatuj datum na srpsku latinicu"""
        days_sr = {
            'Monday': 'Ponedeljak',
            'Tuesday': 'Utorak',
            'Wednesday': 'Sreda',
            'Thursday': 'Četvrtak',
            'Friday': 'Petak',
            'Saturday': 'Subota',
            'Sunday': 'Nedelja'
        }

        months_sr = {
            'January': 'januar',
            'February': 'februar',
            'March': 'mart',
            'April': 'april',
            'May': 'maj',
            'June': 'jun',
            'July': 'jul',
            'August': 'avgust',
            'September': 'septembar',
            'October': 'oktobar',
            'November': 'novembar',
            'December': 'decembar'
        }

        day_name = date.strftime('%A')
        month_name = date.strftime('%B')
        day_sr = days_sr.get(day_name, day_name)
        month_sr = months_sr.get(month_name, month_name)

        return f"{day_sr}, {date.day} {month_sr} {date.year}"

    def updateClock(self):
        """Ažuriraj sat svake sekunde"""
        current_time = datetime.now().strftime("%H:%M:%S")
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

    def checkForSleepWake(self):
        """Proveri da li se računar probudio iz sleep moda"""
        now = datetime.now()
        time_diff = (now - self.last_update).total_seconds()

        if time_diff > 30:
            print("🔄 Detektovan sleep/wake - ČEKAM 30 SEKUNDI pre osvežavanja...")

            # Prikaži korisniku
            self.desc_label.setText("💤 Računar se probudio, čekam 30s...")

            # ČEKAJ 30 SEKUNDI pre nego što pokušaš
            QTimer.singleShot(30000, self.startWakeupRefresh)

        self.last_update = now

    def startWakeupRefresh(self):
        """Počni osvežavanje nakon što je prošlo dovoljno vremena"""
        print("🔄 30s prošlo, resetujem session i osvežavam...")

        # Resetuj session
        try:
            self.session.close()
            self.session = requests.Session()
            print("✅ Session resetovan")
        except Exception as e:
            print(f"⚠️ Greška pri resetovanju: {e}")

        self.desc_label.setText("🔄 Osvežavam...")

        # Sada pokušaj sa retry logikom
        self.retryUpdateWeather(attempt=1, max_attempts=3)

    def retryUpdateWeather(self, attempt=1, max_attempts=3):
        """Pokušaj da osvežiš vreme sa progresivnim čekanjem"""
        print(f"🔄 Pokušaj {attempt}/{max_attempts}...")

        try:
            self.updateWeather()
            print(f"✅ Uspešno osveženo na pokušaj {attempt}!")
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, Exception) as e:
            if attempt < max_attempts:
                # Čekaj 15 sekundi između pokušaja
                wait_time = 15000  # 15 sekundi
                print(f"⚠️ Pokušaj {attempt} neuspešan ({type(e).__name__}), čekam 15s...")
                self.desc_label.setText(f"🌐 Čekam network... ({attempt}/{max_attempts})")

                # Zakazi sledeći pokušaj
                QTimer.singleShot(wait_time, lambda: self.retryUpdateWeather(attempt + 1, max_attempts))
            else:
                print(f"❌ Svi pokušaji neuspešni! Greška: {e}")
                self.desc_label.setText("❌ Nema konekcije - pokreni ponovo")

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

        show_action = QAction("Prikaži Widget", self)
        show_action.triggered.connect(self.toggleWidget)

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

        update_action = QAction("Osveži Vreme", self)
        update_action.triggered.connect(self.updateWeather)

        change_api_action = QAction("Promeni API Key", self)
        change_api_action.triggered.connect(self.changeAPIKey)

        quit_action = QAction("Izađi", self)
        quit_action.triggered.connect(QApplication.quit)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.startup_action)
        tray_menu.addAction(self.widget_only_action)
        tray_menu.addAction(self.click_through_action)
        tray_menu.addMenu(self.size_menu)
        tray_menu.addSeparator()
        tray_menu.addAction(update_action)
        tray_menu.addAction(change_api_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.trayIconActivated)
        self.tray_icon.show()

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
            self.lock_btn.setToolTip("Otključaj poziciju")
            self.tray_icon.showMessage("Widget Zaključan", "Pozicija je fiksirana", QSystemTrayIcon.Information, 2000)
        else:
            self.lock_btn.setText("🔓")
            self.lock_btn.setToolTip("Zaključaj poziciju")
            self.tray_icon.showMessage("Widget Otključan", "Možeš pomerati widget", QSystemTrayIcon.Information, 2000)

        self.saveSettings()

    def toggleClickThrough(self):
        self.click_through = self.click_through_action.isChecked()

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
            except Exception as e:
                print(f"Windows style error: {e}")

            self.tray_icon.showMessage("Click-Through Aktivan", "Klikovi prolaze kroz widget", QSystemTrayIcon.Information, 3000)
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

            except Exception as e:
                print(f"Windows style error: {e}")

            self.tray_icon.showMessage("Click-Through Isključen", "Widget je sada klikabilan", QSystemTrayIcon.Information, 2000)

        self.saveSettings()

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
                self.tray_icon.showMessage("Startup", "Aplikacija će se pokretati sa Windows-om", QSystemTrayIcon.Information, 2000)
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                    self.tray_icon.showMessage("Startup", "Uklonjena iz startup-a", QSystemTrayIcon.Information, 2000)
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

    def changeAPIKey(self):
        """Promeni API key"""
        new_key = self.showAPIKeyDialog()
        if new_key:
            self.api_key = new_key
            self.settings.setValue('api_key', new_key)
            self.tray_icon.showMessage("API Key Promenjen", "Novi API key je sačuvan. Osvežavam vreme...", QSystemTrayIcon.Information, 2000)
            self.updateWeather()

    def loadSettings(self):
        self.widget_locked = self.settings.value('widget_locked', False, type=bool)
        self.click_through = self.settings.value('click_through', False, type=bool)
        self.use_auto_location = self.settings.value('use_auto_location', True, type=bool)
        self.current_location = self.settings.value('current_location', 'Belgrade', type=str)
        self.refresh_interval = self.settings.value('refresh_interval', 300000, type=int)

        self.widget_size_label = self.settings.value('widget_size', 'Full HD (1920x1080)', type=str)
        self.widget_width = self.settings.value('widget_width', 420, type=int)
        self.widget_height = self.settings.value('widget_height', 900, type=int)

        print(f"✅ Učitane postavke:")
        print(f"  - Locked: {self.widget_locked}")
        print(f"  - Click-through: {self.click_through}")
        print(f"  - Auto lokacija: {self.use_auto_location}")
        print(f"  - Lokacija: {self.current_location}")
        print(f"  - Size: {self.widget_size_label} ({self.widget_width}x{self.widget_height})")

    def saveSettings(self):
        self.settings.setValue('widget_locked', self.widget_locked)
        self.settings.setValue('click_through', self.click_through)
        self.settings.setValue('use_auto_location', self.use_auto_location)
        self.settings.setValue('current_location', self.current_location)
        self.settings.setValue('refresh_interval', self.refresh_interval)
        self.settings.setValue('window_x', self.x())
        self.settings.setValue('window_y', self.y())

        print(f"💾 Sačuvane postavke na poziciji: ({self.x()}, {self.y()})")

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

    def getCityCoordinates(self, city_name):
        try:
            serbian_cities = ['beograd', 'belgrade', 'novi sad', 'nis', 'niš', 'kragujevac',
                              'subotica', 'cacak', 'čačak', 'zajecar', 'zaječar', 'uzice', 'užice',
                              'sabac', 'šabac', 'pancevo', 'pančevo', 'krusevac', 'kruševac',
                              'knjazevac', 'knjaževac', 'zemun']

            search_query = city_name
            if city_name.lower() in serbian_cities:
                search_query = f"{city_name},RS"

            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={search_query}&limit=1&appid={self.api_key}"
            response = self.session.get(geo_url, timeout=10)

            if response.status_code == 200 and response.json():
                data = response.json()[0]

                sr_name = data.get('local_names', {}).get('sr', '')

                if sr_name and self.is_cyrillic(sr_name):
                    city_name = data['name']
                elif sr_name:
                    city_name = sr_name
                else:
                    city_name = data['name']

                city_map = {
                    'Belgrade': 'Beograd',
                    'Novi Sad': 'Novi Sad',
                    'Niš': 'Niš',
                    'Nis': 'Niš',
                    'Kragujevac': 'Kragujevac',
                    'Subotica': 'Subotica',
                    'Zrenjanin': 'Zrenjanin',
                    'Pančevo': 'Pančevo',
                    'Pancevo': 'Pančevo',
                    'Čačak': 'Čačak',
                    'Cacak': 'Čačak',
                    'Kruševac': 'Kruševac',
                    'Krusevac': 'Kruševac',
                    'Leskovac': 'Leskovac',
                    'Valjevo': 'Valjevo',
                    'Šabac': 'Šabac',
                    'Sabac': 'Šabac',
                    'Užice': 'Užice',
                    'Uzice': 'Užice',
                    'Zaječar': 'Zaječar',
                    'Zajecar': 'Zaječar',
                    'Smederevo': 'Smederevo',
                    'Sombor': 'Sombor',
                    'Stari Grad': 'Beograd',
                    'Semlin': 'Zemun',
                    'Zimony': 'Zemun'
                }

                if city_name in city_map:
                    city_name = city_map[city_name]

                return {'city': city_name, 'lat': data['lat'], 'lon': data['lon']}
        except Exception as e:
            print(f"Geocoding greška: {e}")
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

    def getHourlyForecast(self, lat, lon):
        """Dobij satnu prognozu - SVAKOG SATA do 24h (ne svakih 3h)"""
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=sr"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                hourly_data = []
                
                current_time = datetime.now()

                # API vraća podatke na svakih 3 sata, ali možemo interpolirati
                for item in data['list'][:8]:  # Prvih 24 sata (8 x 3h)
                    forecast_time = datetime.fromtimestamp(item['dt'])
                    hours_diff = int((forecast_time - current_time).total_seconds() / 3600)
                    
                    hourly_data.append({
                        'time': forecast_time.strftime('%H:%M'),
                        'temp': round(item['main']['temp']),
                        'weather': item['weather'][0]['main'],
                        'hours_until': hours_diff
                    })

                return hourly_data
        except Exception as e:
            print(f"❌ Hourly forecast greška: {e}")
        return []

    def getWeatherAlerts(self, lat, lon):
        """Dobij vremenska upozorenja iz One Call API 3.0"""
        try:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={self.api_key}&exclude=minutely,daily"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                alerts = []

                if 'alerts' in data:
                    for alert in data['alerts']:
                        alerts.append({
                            'event': alert.get('event', 'Upozorenje'),
                            'description': alert.get('description', ''),
                            'start': alert.get('start', 0),
                            'end': alert.get('end', 0)
                        })

                return alerts
            elif response.status_code == 401:
                print("ℹ️ One Call API nije dostupan (treba poseban plan)")
                return []
        except Exception as e:
            print(f"ℹ️ Weather alerts nisu dostupni: {e}")
        return []

    def updateWeather(self):
        try:
            location_data = None

            if self.use_auto_location:
                location_data = self.getAutoLocation()
                self.current_location = location_data['city']
            else:
                location_data = self.getCityCoordinates(self.current_location)
                if not location_data:
                    self.desc_label.setText(f"❌ Grad '{self.current_location}' nije pronađen")
                    return

            if location_data and 'lat' in location_data and 'lon' in location_data:
                url = f"http://api.openweathermap.org/data/2.5/weather?lat={location_data['lat']}&lon={location_data['lon']}&appid={self.api_key}&units=metric&lang=en"
                city_name = location_data['city']
            else:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={self.current_location}&appid={self.api_key}&units=metric&lang=en"
                city_name = self.current_location

            print(f"Učitavam vreme za: {city_name}")
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                data = response.json()

                temp = round(data['main']['temp'], 1)
                feels = round(data['main']['feels_like'], 1)
                humidity = data['main']['humidity']
                wind_speed = round(data['wind']['speed'] * 3.6, 1)
                wind_deg = data['wind'].get('deg', 0)
                wind_direction = self.getWindDirection(wind_deg)

                pressure = data['main']['pressure']
                visibility = data.get('visibility', 10000) / 1000
                cloudiness = data['clouds']['all']

                weather_info = self.translate_weather(data['weather'][0]['description'])
                desc = weather_info[0]
                weather_icon = weather_info[1]
                city = data['name']

                city_map = {
                    'Stari Grad': 'Beograd',
                    'Semlin': 'Zemun',
                    'Zimony': 'Zemun',
                    'Serbia': 'Beograd',
                    'Knjazevac': 'Knjaževac'
                }

                if city in city_map:
                    city = city_map[city]

                if city.lower() == 'serbia':
                    if location_data and 'city' in location_data:
                        city = location_data['city']
                    elif hasattr(self, 'current_location'):
                        city = self.current_location.capitalize()
                    else:
                        city = 'Belgrade'

                self.current_temp = f"{int(temp)}°"

                sunrise_time = datetime.fromtimestamp(data['sys']['sunrise'])
                sunset_time = datetime.fromtimestamp(data['sys']['sunset'])

                self.city_label.setText(city)
                self.temp_label.setText(f"{weather_icon} {temp}°C")
                self.desc_label.setText(desc)
                self.feels_label.setText(f"{feels}°C")
                self.humid_label.setText(f"{humidity}%")
                self.wind_label.setText(f"{wind_speed} km/h {wind_direction}")

                self.pressure_label.setText(f"{pressure} mbar")
                self.visibility_label.setText(f"{visibility:.1f} km")
                self.clouds_label.setText(f"{cloudiness}%")

                self.sunrise_label.setText(sunrise_time.strftime("%H:%M"))
                self.sunset_label.setText(sunset_time.strftime("%H:%M"))

                # UV
                try:
                    uv_url = f"http://api.openweathermap.org/data/2.5/uvi?lat={location_data['lat']}&lon={location_data['lon']}&appid={self.api_key}"
                    uv_response = self.session.get(uv_url, timeout=10)

                    if uv_response.status_code == 200:
                        uv_data = uv_response.json()
                        uv_value = round(uv_data.get('value', 0), 1)
                        uv_color = self.getUVColor(uv_value)
                        self.uv_label.setText(f"{uv_value}")
                        self.uv_label.setStyleSheet(f"color: {uv_color}; font-size: 16px; font-weight: bold;")
                        print(f"✅ UV Index: {uv_value}")
                    else:
                        self.uv_label.setText("--")
                        print(f"⚠️ UV API greška: {uv_response.status_code}")
                except Exception as uv_error:
                    self.uv_label.setText("--")
                    print(f"❌ UV greška: {uv_error}")

                # AQI + polutanti
                try:
                    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={location_data['lat']}&lon={location_data['lon']}&appid={self.api_key}"
                    aqi_response = self.session.get(aqi_url, timeout=10)

                    if aqi_response.status_code == 200:
                        aqi_data = aqi_response.json()
                        aqi_index = aqi_data['list'][0]['main']['aqi']
                        aqi_labels = ['Odličan', 'Dobar', 'Srednji', 'Loš', 'V. loš']
                        aqi_text = aqi_labels[aqi_index - 1]
                        aqi_color = self.getAQIColor(aqi_index)
                        self.aqi_label.setText(aqi_text)
                        self.aqi_label.setStyleSheet(f"color: {aqi_color}; font-size: 16px; font-weight: bold;")

                        self.pollutants_data = aqi_data['list'][0]['components']

                        print(f"✅ Air Quality: {aqi_text} (AQI: {aqi_index})")
                        print(f"   Polutanti: PM2.5={self.pollutants_data.get('pm2_5', 0):.1f}, PM10={self.pollutants_data.get('pm10', 0):.1f}")
                    else:
                        self.aqi_label.setText("--")
                        self.pollutants_data = {}
                        print(f"⚠️ AQI API greška: {aqi_response.status_code}")
                except Exception as aqi_error:
                    self.aqi_label.setText("--")
                    self.pollutants_data = {}
                    print(f"❌ AQI greška: {aqi_error}")

                self.updateTrayIcon()
                self.tray_icon.setToolTip(f"{city}: {temp}°C, {desc}")

                print("✅ Uspešno učitano!")

                self.update5DayForecast(location_data)

            elif response.status_code == 401:
                self.desc_label.setText("❌ Nevažeći API key")
                self.tray_icon.showMessage("API Key Problem", "API key nije validan", QSystemTrayIcon.Warning)
                print("❌ 401 - API key problem")
            elif response.status_code == 404:
                self.desc_label.setText(f"❌ Lokacija nije pronađena")
                print(f"❌ 404 - Lokacija nije pronađena")
            else:
                self.desc_label.setText(f"Greška: {response.status_code}")
                print(f"❌ Status kod: {response.status_code}")

        except Exception as e:
            self.desc_label.setText(f"Greška: {str(e)}")
            print(f"❌ Greška: {str(e)}")

    def update5DayForecast(self, location_data):
        try:
            if location_data and 'lat' in location_data and 'lon' in location_data:
                url = f"http://api.openweathermap.org/data/2.5/forecast?lat={location_data['lat']}&lon={location_data['lon']}&appid={self.api_key}&units=metric&lang=en"
            else:
                url = f"http://api.openweathermap.org/data/2.5/forecast?q={self.current_location}&appid={self.api_key}&units=metric&lang=en"

            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                data = response.json()
                daily_forecasts = {}

                for item in data['list']:
                    date = datetime.fromtimestamp(item['dt'])
                    day_key = date.strftime('%Y-%m-%d')

                    if day_key not in daily_forecasts:
                        daily_forecasts[day_key] = {'date': date, 'temps': [], 'descriptions': []}

                    daily_forecasts[day_key]['temps'].append(item['main']['temp'])
                    daily_forecasts[day_key]['descriptions'].append(item['weather'][0]['description'])

                for day_key in daily_forecasts:
                    temps = daily_forecasts[day_key]['temps']
                    descriptions = daily_forecasts[day_key]['descriptions']
                    daily_forecasts[day_key]['temp_min'] = round(min(temps), 1)
                    daily_forecasts[day_key]['temp_max'] = round(max(temps), 1)

                    weather_info = self.translate_weather(descriptions[len(descriptions)//2])
                    daily_forecasts[day_key]['desc'] = weather_info[0]
                    daily_forecasts[day_key]['icon'] = weather_info[1]

                days_list = sorted(daily_forecasts.values(), key=lambda x: x['date'])[:5]

                serbian_days_short = {
                    'Monday': 'Pon',
                    'Tuesday': 'Uto',
                    'Wednesday': 'Sre',
                    'Thursday': 'Čet',
                    'Friday': 'Pet',
                    'Saturday': 'Sub',
                    'Sunday': 'Ned'
                }

                for i, forecast in enumerate(days_list):
                    if i < len(self.forecast_labels):
                        day_name = forecast['date'].strftime('%A')
                        day_sr = serbian_days_short.get(day_name, day_name)
                        date_str = forecast['date'].strftime('%d.%m')

                        self.forecast_labels[i]['day'].setText(f"{day_sr} {date_str}")
                        self.forecast_labels[i]['desc'].setText(f"{forecast['icon']} {forecast['desc']}")
                        self.forecast_labels[i]['temp'].setText(f"{forecast['temp_min']}° / {forecast['temp_max']}°")

                print("✅ 5-day forecast učitan!")

                if location_data and 'lat' in location_data and 'lon' in location_data:
                    self.updateRainAlert(location_data)
                    self.updateWeatherAlertsBox(location_data)

            else:
                print(f"❌ Forecast greška: {response.status_code}")

        except Exception as e:
            print(f"❌ Forecast error: {e}")

    def updateRainAlert(self, location_data):
        """Proveri padavine i ažuriraj kvadrat - PRECIZNO do sata"""
        try:
            hourly_data = self.getHourlyForecast(location_data['lat'], location_data['lon'])

            print(f"🔍 Hourly data ({len(hourly_data)} perioda):")
            for hour in hourly_data:
                print(f"  {hour['hours_until']}h: {hour['weather']} - {hour['temp']}°")

            if hourly_data:
                for hour in hourly_data:
                    weather = hour['weather']

                    if weather in ['Rain', 'Drizzle', 'Thunderstorm', 'Snow']:
                        hours_until = hour['hours_until']

                        emoji_map = {
                            'Rain': '🌧️',
                            'Drizzle': '🌦️',
                            'Thunderstorm': '⛈️',
                            'Snow': '❄️'
                        }

                        text_map = {
                            'Rain': 'Kiša',
                            'Drizzle': 'Kiša',
                            'Thunderstorm': 'Oluja',
                            'Snow': 'Sneg'
                        }

                        emoji = emoji_map.get(weather, '🌧️')
                        text = text_map.get(weather, 'Kiša')

                        if hours_until <= 0:
                            alert_text = f"{emoji} {text} SADA!"
                        elif hours_until == 1:
                            alert_text = f"{emoji} {text} za 1h"
                        else:
                            alert_text = f"{emoji} {text} za {hours_until}h"

                        self.precip_alert_label.setText(alert_text)
                        print(f"✅ Precipitation alert: {alert_text}")
                        return

                print("ℹ️ Nema padavina u hourly, proveravam 5-day...")
                self.checkForecastForRain()
            else:
                self.precip_alert_label.setText("☀️ Bez padavina")

        except Exception as e:
            print(f"❌ Rain alert greška: {e}")
            self.precip_alert_label.setText("⚠️ Greška")

    def checkForecastForRain(self):
        """Proveri 5-day forecast za padavine"""
        try:
            days = ['Sutra', 'Prekosutra', 'za 3 dana', 'za 4 dana']

            for i, forecast in enumerate(self.forecast_labels[1:5]):
                desc = forecast['desc'].text().lower()

                if 'kiš' in desc or 'rain' in desc:
                    self.precip_alert_label.setText(f"🌧️ Kiša {days[i]}")
                    print(f"✅ Precipitation forecast: Kiša {days[i]}")
                    return
                elif 'sneg' in desc or 'snow' in desc:
                    self.precip_alert_label.setText(f"❄️ Sneg {days[i]}")
                    print(f"✅ Precipitation forecast: Sneg {days[i]}")
                    return
                elif 'oluj' in desc or 'storm' in desc:
                    self.precip_alert_label.setText(f"⛈️ Oluja {days[i]}")
                    print(f"✅ Precipitation forecast: Oluja {days[i]}")
                    return

            self.precip_alert_label.setText("☀️ Bez padavina")
            print("ℹ️ Nema padavina u narednih 5 dana")

        except Exception as e:
            print(f"❌ 5-day check greška: {e}")
            self.precip_alert_label.setText("☀️ Bez padavina")

    # ==============================
    # ✅ IZMENJENO: prevod upozorenja u box-u + DINAMIČKA BOJA
    # ==============================
    def updateWeatherAlertsBox(self, location_data):
        """Ažuriraj upozorenja kvadrat (BEZ tray notifikacija) + DINAMIČKA BOJA + AUTO FONT"""
        try:
            alerts = self.getWeatherAlerts(location_data['lat'], location_data['lon'])

            if alerts:
                first_alert = alerts[0]

                # ✅ OVDE JE IZMENJENO:
                alert_text = self.translate_alert_event(first_alert.get('event', 'Upozorenje'))

                if len(alerts) > 1:
                    alert_text += f" (+{len(alerts)-1})"

                # 🎨 DINAMIČKA BOJA na osnovu nivoa
                alert_level = self.getAlertColorLevel(first_alert.get('event', ''))
                
                if alert_level == 'red':
                    # CRVENO - ekstremno upozorenje
                    self.alerts_box.setStyleSheet("""
                        QWidget {
                            background-color: rgba(244, 67, 54, 0.4);
                            border-radius: 8px;
                            border: 2px solid rgba(244, 67, 54, 0.7);
                            padding: 8px;
                        }
                    """)
                    emoji = "🚨"
                elif alert_level == 'yellow':
                    # ŽUTO - upozorenje
                    self.alerts_box.setStyleSheet("""
                        QWidget {
                            background-color: rgba(255, 152, 0, 0.4);
                            border-radius: 8px;
                            border: 2px solid rgba(255, 152, 0, 0.7);
                            padding: 8px;
                        }
                    """)
                    emoji = "⚠️"
                else:
                    # ZELENO - nema upozorenja (fallback)
                    self.alerts_box.setStyleSheet("""
                        QWidget {
                            background-color: rgba(76, 175, 80, 0.3);
                            border-radius: 8px;
                            border: 1px solid rgba(76, 175, 80, 0.5);
                            padding: 8px;
                        }
                    """)
                    emoji = "✅"

                # 📏 INTELIGENTNO FORMATIRANJE - uvek 2 reda, čitljivo
                full_text = f"{emoji} {alert_text}"
                formatted_text, font_size = self.formatAlertText(full_text)
                
                # ✅ SAČUVAJ PUN TEKST za tooltip
                self.full_alert_text = full_text
                self.current_alert_data = first_alert  # Sačuvaj ceo alert objekat
                
                self.weather_alert_label.setStyleSheet(f"color: white; font-size: {font_size}px; line-height: 1.3;")
                self.weather_alert_label.setText(formatted_text)
                print(f"✅ Weather alert box: {formatted_text} (nivo: {alert_level}, font: {font_size}px)")
            else:
                # BEZ UPOZORENJA - zeleno
                self.full_alert_text = "✅ Bez upozorenja"
                self.current_alert_data = None
                
                self.alerts_box.setStyleSheet("""
                    QWidget {
                        background-color: rgba(76, 175, 80, 0.3);
                        border-radius: 8px;
                        border: 1px solid rgba(76, 175, 80, 0.5);
                        padding: 8px;
                    }
                """)
                self.weather_alert_label.setStyleSheet("color: white; font-size: 12px; line-height: 1.3;")
                self.weather_alert_label.setText("✅ Bez upozorenja")
                print("ℹ️ Nema weather alerts")

        except Exception as e:
            print(f"❌ Weather alerts box greška: {e}")
            # Greška - ostavi neutralno (žuto)
            self.full_alert_text = "⚠️ Greška"
            self.current_alert_data = None
            
            self.alerts_box.setStyleSheet("""
                QWidget {
                    background-color: rgba(255, 152, 0, 0.3);
                    border-radius: 8px;
                    border: 1px solid rgba(255, 152, 0, 0.5);
                    padding: 8px;
                }
            """)
            self.weather_alert_label.setStyleSheet("color: white; font-size: 12px; line-height: 1.3;")
            self.weather_alert_label.setText("⚠️ Greška")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    weather = WeatherWidget()
    weather.show()

    sys.exit(app.exec_())
