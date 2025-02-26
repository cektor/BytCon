import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QRadioButton, QPushButton, 
                            QGroupBox, QProgressBar, QMessageBox, QToolButton)
from PyQt5.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, QSettings, QTranslator, QLocale
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QFontDatabase, QKeySequence, QPixmap
from PyQt5.QtWidgets import QShortcut, QToolTip, QMenu, QAction
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

def get_logo_path():
    """Logo dosyasının yolunu döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "bytconlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/bytconlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/bytconlo.png"
    home_dir = os.path.expanduser("~/.local/share/icons/bytconlo.png")
    if os.path.exists(home_dir):
        return home_dir
    return "bytconlo.png"

def get_icon_path():
    """İkon dosyasının yolunu döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "bytconlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/bytconlo.png"):
        return os.path.join("/usr/share/icons/hicolor/48x48/apps/bytconlo.png")
    return None

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Platform bağımsız yol işlemleri için
        self.app_path = Path(os.path.dirname(os.path.abspath(__file__)))
        
        # Platform tespiti
        self.platform = sys.platform
        
        # QSettings için platform bağımsız yapılandırma
        if self.platform == 'darwin':  # macOS
            self.settings = QSettings(QSettings.NativeFormat, QSettings.UserScope,
                                    'BytCon', 'Settings')
        else:  # Windows ve Linux
            self.settings = QSettings('BytCon', 'Settings')

        # Font ayarları
        self.setup_fonts()
        
        self.translator = QTranslator()
        
        # Kaydedilmiş dil ayarını yükle, yoksa varsayılan 'tr' kullan
        self.current_language = self.settings.value('language', defaultValue='tr', type=str)
        
        self.setup_language()
        self.setupUI()
        self.setupShortcuts()
        
        # Başlangıçta dil ayarını uygula
        self.update_texts()
        
    def setup_fonts(self):
        """Platform bağımsız font ayarları"""
        if self.platform == 'darwin':  # macOS
            default_font = 'SF Pro Display'
            default_size = 13
        elif self.platform == 'win32':  # Windows
            default_font = 'Segoe UI'
            default_size = 9
        else:  # Linux
            default_font = 'Ubuntu'
            default_size = 10
            
        app = QApplication.instance()
        font = QFont(default_font, default_size)
        app.setFont(font)

    def setupShortcuts(self):
        """Platform bağımsız kısayol tuşları"""
        if self.platform == 'darwin':  # macOS
            QShortcut(QKeySequence("Cmd+Q"), self, self.close)
            QShortcut(QKeySequence("Cmd+C"), self, self.copy_result)
        else:  # Windows ve Linux
            QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
            QShortcut(QKeySequence("Ctrl+C"), self, self.copy_result)
        
        # Platform bağımsız kısayollar
        QShortcut(QKeySequence("Return"), self, self.convert)
        QShortcut(QKeySequence("Enter"), self, self.convert)

    def setup_language(self):
        self.translations = {
            'tr': {
                'window_title': 'BytCon',
                'enter_value': 'Bir Değer Girin:',
                'convert': 'Dönüştür',
                'copy_success': 'Sonuç başarıyla kopyalandı!',
                'error': 'Hata',
                'success': 'Başarılı',
                'invalid_number': 'Lütfen geçerli bir sayı giriniz!',
                'positive_number': 'Pozitif bir değer giriniz!',
                'conversion_unit': 'Dönüşüm Birimi',
                'result_placeholder': 'Sonuç gösterilecek',
                'language': 'Dil',
                'example_placeholder': 'Örnek: 1024',
                'about_title': 'Hakkında',
                'close': 'Kapat'
            },
            'en': {
                'window_title': 'BytCon',
                'enter_value': 'Enter a Value:',
                'convert': 'Convert',
                'copy_success': 'Result copied successfully!',
                'error': 'Error',
                'success': 'Success',
                'invalid_number': 'Please enter a valid number!',
                'positive_number': 'Please enter a positive value!',
                'conversion_unit': 'Conversion Unit',
                'result_placeholder': 'Result will be shown here',
                'language': 'Language',
                'example_placeholder': 'Example: 1024',
                'about_title': 'About',
                'close': 'Close'
            }
        }
        
    def create_language_menu(self):
        language_menu = QMenu(self)
        
        tr_action = QAction('Türkçe', self)
        tr_action.setData('tr')
        # Mevcut dil seçiliyse işaretle
        tr_action.setCheckable(True)
        tr_action.setChecked(self.current_language == 'tr')
        
        en_action = QAction('English', self)
        en_action.setData('en')
        en_action.setCheckable(True)
        en_action.setChecked(self.current_language == 'en')
        
        language_menu.addAction(tr_action)
        language_menu.addAction(en_action)
        
        # Dil değiştirme butonu
        self.language_button = QPushButton(self.tr('Dil'))
        self.language_button.setMenu(language_menu)
        self.language_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #2d2d2d;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        
        # Dil değiştirme aksiyonları
        tr_action.triggered.connect(lambda: self.change_language('tr'))
        en_action.triggered.connect(lambda: self.change_language('en'))
        
        return self.language_button

    def change_language(self, lang):
        # Dil değiştiğinde ayarları kaydet
        self.current_language = lang
        self.settings.setValue('language', lang)
        self.settings.sync()  # Ayarların hemen kaydedilmesini sağla
        self.update_texts()
        
    def update_texts(self):
        # Tüm metinleri güncelle
        texts = self.translations[self.current_language]
        
        self.setWindowTitle(texts['window_title'])
        self.title_label.setText(texts['window_title'])
        self.entry_label.setText(texts['enter_value'])
        self.convert_button.setText(texts['convert'])
        self.radio_group.setTitle(texts['conversion_unit'])
        self.result_label.setText(texts['result_placeholder'])
        self.entry.setPlaceholderText(texts['example_placeholder'])

    def setupUI(self):
        try:
            # Platform bağımsız icon yolu
            icon_path = self.app_path / "bytconlo.png"
            
            # Ana pencere ayarları
            self.setWindowTitle("BytCon")
            self.setFixedSize(500, 680)
            
            if icon_path.exists():
                self.setWindowIcon(QIcon(str(icon_path)))

            # Platform özel stil ayarları
            if self.platform == 'darwin':  # macOS
                self.setStyleSheet(self.get_macos_style())
            elif self.platform == 'win32':  # Windows
                self.setStyleSheet(self.get_windows_style())
            else:  # Linux
                self.setStyleSheet(self.get_linux_style())

            # Logo widget'ı
            self.logo_label = QLabel()
            logo_pixmap = QPixmap(LOGO_PATH)
            if not logo_pixmap.isNull():
                scaled_logo = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(scaled_logo)
                self.logo_label.setAlignment(Qt.AlignCenter)
            
            # Başlık Etiketi
            self.title_label = QLabel("BytCon")
            self.title_label.setStyleSheet("""
                font-size: 28px;
                font-weight: bold;
                color: #4a9eff;
                padding: 20px;
                qproperty-alignment: AlignCenter;
            """)

            # Değer Girişi
            self.entry_label = QLabel("Bir Değer Girin:")
            self.entry_label.setStyleSheet("font-size: 14px; margin-bottom: 5px;")
            
            self.entry = QLineEdit()
            self.entry.setPlaceholderText("Örnek: 1024")
            self.entry.setStyleSheet("""
                QLineEdit {
                    padding: 12px;
                    border: 2px solid #333333;
                    border-radius: 10px;
                    background-color: #2d2d2d;
                    color: #ffffff;
                    font-size: 16px;
                    transition: all 0.3s ease;
                }
                QLineEdit:focus {
                    border: 2px solid #4a9eff;
                    background-color: #363636;
                }
            """)
            self.entry.setToolTip("Dönüştürmek istediğiniz değeri girin")

            # Dönüşüm tipi için Radyo Butonları
            self.conversion_type = "MB"
            self.mb_radio = QRadioButton("MB")
            self.mb_radio.setChecked(True)
            self.mb_radio.toggled.connect(self.set_conversion_type)
            
            self.gb_radio = QRadioButton("GB")
            self.gb_radio.toggled.connect(self.set_conversion_type)

            self.tb_radio = QRadioButton("TB")
            self.tb_radio.toggled.connect(self.set_conversion_type)

            # Radyo butonları grubu
            self.radio_group = QGroupBox("Dönüşüm Birimi")
            radio_layout = QHBoxLayout()
            radio_layout.addWidget(self.mb_radio)
            radio_layout.addWidget(self.gb_radio)
            radio_layout.addWidget(self.tb_radio)
            radio_layout.setSpacing(20)
            self.radio_group.setLayout(radio_layout)

            # Dönüştür Butonu
            self.convert_button = QPushButton("Dönüştür")
            self.convert_button.setCursor(Qt.PointingHandCursor)
            self.convert_button.clicked.connect(self.convert)
            self.convert_button.setToolTip("Dönüşümü başlat (Enter)")

            # İlerleme Çubuğu
            self.progress_bar = QProgressBar()
            self.progress_bar.setFixedHeight(15)
            self.progress_bar.setValue(0)
            self.progress_bar.setTextVisible(False)

            # Layout düzenlemesi
            layout = QVBoxLayout()
            layout.addWidget(self.logo_label)  # Logo widget'ı
            layout.addWidget(self.title_label)  # Sadece başlık etiketi
            
            input_layout = QVBoxLayout()
            input_layout.addWidget(self.entry_label)
            input_layout.addWidget(self.entry)
            layout.addLayout(input_layout)
            
            layout.addWidget(self.radio_group)
            layout.addWidget(self.convert_button)
            layout.addWidget(self.progress_bar)
            layout.addWidget(self.create_result_widget())
            layout.addWidget(self.create_language_menu())
            layout.addWidget(self.create_about_button())
            
            # Kenar boşlukları
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(15)

            self.setLayout(layout)
        except Exception as e:
            self.handle_error(str(e))

    def get_macos_style(self):
        """macOS özel stilleri"""
        return """
            QWidget {
                background-color: #f5f5f7;
                color: #000000;
                font-family: 'SF Pro Display';
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #dedede;
                border-radius: 6px;
                background-color: #ffffff;
                color: #000000;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 8px;
                border-radius: 6px;
            }
            /* Diğer macOS stilleri */
        """

    def get_windows_style(self):
        """Windows özel stilleri"""
        return """
            QWidget {
                background-color: #f0f0f0;
                color: #000000;
                font-family: 'Segoe UI';
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #ffffff;
                color: #000000;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            /* Diğer Windows stilleri */
        """

    def get_linux_style(self):
        """Linux özel stilleri - Mevcut karanlık tema"""
        return """
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Ubuntu';
            }
            /* Mevcut Linux stilleri devam edecek */
        """

    def set_conversion_type(self):
        if self.mb_radio.isChecked():
            self.conversion_type = "MB"
        elif self.gb_radio.isChecked():
            self.conversion_type = "GB"
        elif self.tb_radio.isChecked():
            self.conversion_type = "TB"

    def convert(self):
        try:
            # Boş giriş kontrolü
            text = self.entry.text().strip()
            if not text:
                self.show_error_message(self.translations[self.current_language]['invalid_number'])
                return

            try:
                value = float(text)
            except ValueError:
                self.show_error_message(self.translations[self.current_language]['invalid_number'])
                return

            if value < 0:
                self.show_error_message(self.translations[self.current_language]['positive_number'])
                return

            # Animasyonlu dönüşüm
            self.progress_bar.setValue(0)
            animation = QPropertyAnimation(self.progress_bar, b"value")
            animation.setDuration(1000)
            animation.setStartValue(0)
            animation.setEndValue(100)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # Animasyonu başlat
            animation.start()
            QTimer.singleShot(500, lambda: self.calculate_conversion(value))
            
        except Exception as e:
            # Genel hata yakalama
            self.handle_error(str(e))

    def handle_error(self, error_message):
        """Genel hata işleme metodu"""
        try:
            self.show_error_message(f"{self.translations[self.current_language]['error']}: {error_message}")
            self.progress_bar.setValue(0)
            self.result_label.setText(self.translations[self.current_language]['invalid_number'])
        except Exception as e:
            # En kötü durumda İngilizce mesaj göster
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def calculate_conversion(self, value):
        try:
            # Sıfıra bölme kontrolü
            if value == 0:
                result = "0 MB = 0 GB = 0 TB"
                self.result_label.setText(result)
                self.progress_bar.setValue(100)
                return

            if self.conversion_type == "MB":
                gb_result = value / 1024
                tb_result = value / (1024 * 1024)
                result = f"{value:,.0f} MB = {gb_result:,.2f} GB\n{value:,.0f} MB = {tb_result:,.4f} TB"
            elif self.conversion_type == "GB":
                mb_result = value * 1024
                tb_result = value / 1024
                result = f"{value:,.2f} GB = {mb_result:,.0f} MB\n{value:,.2f} GB = {tb_result:,.4f} TB"
            elif self.conversion_type == "TB":
                mb_result = value * (1024 * 1024)
                gb_result = value * 1024
                result = f"{value:,.2f} TB = {mb_result:,.0f} MB\n{value:,.2f} TB = {gb_result:,.0f} GB"

            self.progress_bar.setValue(100)
            self.result_label.setText(result)

        except Exception as e:
            self.handle_error(str(e))

    def show_error_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(self.translations[self.current_language]['error'])
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QMessageBox QPushButton {
                padding: 5px 20px;
                margin: 10px;
            }
        """)
        msg_box.exec_()

    def show_success_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(self.translations[self.current_language]['success'])
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QMessageBox QPushButton {
                padding: 5px 20px;
                margin: 10px;
                background-color: #4a9eff;
            }
        """)
        msg_box.exec_()

    def create_result_widget(self):
        # Sonuç container widget
        result_container = QWidget()
        result_layout = QHBoxLayout(result_container)
        result_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sonuç etiketi
        self.result_label = QLabel("Sonuç gösterilecek")
        self.result_label.setStyleSheet("""
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            qproperty-alignment: AlignCenter;
        """)
        self.result_label.setCursor(Qt.PointingHandCursor)
        self.result_label.mousePressEvent = self.copy_result
        
        # Kopyalama butonu
        self.copy_button = QToolButton()
        self.copy_button.setText("📋")  # Unicode kopyalama ikonu
        self.copy_button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 5px;
                font-size: 16px;
                color: #4a9eff;
            }
            QToolButton:hover {
                background-color: #4a9eff;
                color: white;
                border-radius: 4px;
            }
        """)
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_result)
        self.copy_button.setToolTip("Sonucu kopyala (Ctrl+C)")
        
        # Layout düzenlemesi
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.copy_button)
        
        return result_container

    def copy_result(self, event=None):
        """Sonucu panoya kopyala"""
        try:
            result_text = self.result_label.text()
            if result_text and result_text != self.translations[self.current_language]['result_placeholder']:
                clipboard = QApplication.clipboard()
                clipboard.setText(result_text)
                
                # Gelişmiş kopyalama animasyonu
                try:
                    original_style = self.result_label.styleSheet()
                    animation = QPropertyAnimation(self.result_label, b"styleSheet")
                    animation.setDuration(500)
                    animation.setStartValue(original_style + "background-color: #3a7fcf;")
                    animation.setEndValue(original_style)
                    animation.start()
                except Exception:
                    pass  # Animasyon hatası kritik değil
                
                self.show_success_message(self.translations[self.current_language]['copy_success'])
        except Exception as e:
            self.handle_error(str(e))

    def create_about_button(self):
        about_button = QPushButton("...", self)  # Üç nokta karakteri
        about_button.setFixedSize(40,40 )
        about_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4a9eff;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #2d2d2d;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
        """)
        about_button.setCursor(Qt.PointingHandCursor)
        about_button.clicked.connect(self.show_about_dialog)
        about_button.setToolTip("Hakkında")
        return about_button

    def show_about_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.translations[self.current_language]['about_title'])
        dialog.setFixedSize(400, 600)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4a9eff;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a7fcf;
            }
        """)

        layout = QVBoxLayout()
        
        # Logo
        about_logo = QLabel()
        logo_pixmap = QPixmap(LOGO_PATH)
        if not logo_pixmap.isNull():
            scaled_logo = logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            about_logo.setPixmap(scaled_logo)
            about_logo.setAlignment(Qt.AlignCenter)
        
        # Logo veya başlık
        title = QLabel("BytCon")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4a9eff;
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        
       
        # Açıklama
        description = QLabel(
            "BytCon (Byte Converter), MB, GB ve TB birimleri arasında\n"
            "kolay dönüşüm yapmanızı sağlayan bir araçtır.\n\n"

        )
        description.setAlignment(Qt.AlignCenter)
        
        # Geliştirici bilgisi
        developer = QLabel(
        "\nGeliştirici: ALG Yazılım Inc.©\n"
        "www.algyazilim.com | info@algyazilim.com\n"
        "Fatih ÖNDER (CekToR) | fatih@algyazilim.com\n\n"
        "GitHub: https://github.com/cektor\n\n"
        "Sürüm: 1.0\n\n"
        "ALG Yazılım Pardus'a Göç'ü Destekler.\n\n"
        "Telif Hakkı © 2025 GNU\n\n"
        )
        developer.setAlignment(Qt.AlignCenter)
        
        # Kapatma butonu
        close_button = QPushButton(self.translations[self.current_language]['close'])
        close_button.clicked.connect(dialog.close)
        
        # Elementleri layout'a ekle
        layout.addWidget(about_logo)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(developer)
        layout.addWidget(close_button)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        dialog.setLayout(layout)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # QSettings için organizasyon ve uygulama adını ayarla
    app.setOrganizationName("BytCon")
    app.setApplicationName("BytCon")
    
    LOGO_PATH = get_logo_path()
    ICON_PATH = get_icon_path()
    
    # Uygulama ikonu
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
        
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
