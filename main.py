# -*- coding: utf-8 -*-
import sys
import json
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel
from PySide6.QtCore import Qt

from styles import AppStyles
from modules.stopwatch import StopwatchWidget
from modules.timer import TimerWidget 

# Путь к файлу настроек в папке с проектом
SETTINGS_FILE = "settings.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glassmorphism Timer")
        self.resize(550, 750)
        self.setStyleSheet(AppStyles.MAIN_STYLE)
        
        self.init_ui()
        self.load_settings() # Загружаем данные при старте

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 50, 40, 40)

        self.header = QLabel("COMING SOON")
        self.header.setObjectName("header_label")
        self.header.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header)

        nav = QHBoxLayout()
        self.btn_t = QPushButton("Таймер")
        self.btn_s = QPushButton("Секундомер")
        
        nav.addStretch(); nav.addWidget(self.btn_t); nav.addWidget(self.btn_s); nav.addStretch()
        layout.addLayout(nav)

        self.stack = QStackedWidget()
        self.tw = TimerWidget() 
        self.sw = StopwatchWidget()
        self.stack.addWidget(self.tw); self.stack.addWidget(self.sw)
        layout.addWidget(self.stack)

        footer = QLabel("PRECISION & MINIMALISM\n2026 SMIRNOV ILYA")
        footer.setStyleSheet(AppStyles.footer_info())
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.btn_t.clicked.connect(lambda: self.switch(0))
        self.btn_s.clicked.connect(lambda: self.switch(1))

    def switch(self, i):
        self.stack.setCurrentIndex(i)
        self.btn_t.setStyleSheet(AppStyles.tab_button(i==0))
        self.btn_s.setStyleSheet(AppStyles.tab_button(i==1))
        self.header.setText("TIMER" if i==0 else "STOPWATCH")
        self.save_settings() # Сохраняем вкладку при каждом переключении

    def save_settings(self):
        """Записываем настройки в JSON файл"""
        data = {
            "last_tab": self.stack.currentIndex(),
            "width": self.width(),
            "height": self.height()
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_settings(self):
        """Читаем настройки из JSON файла"""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.switch(data.get("last_tab", 0))
                    self.resize(data.get("width", 550), data.get("height", 750))
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.switch(0)
        else:
            self.switch(0)

    def closeEvent(self, event):
        self.save_settings() # Сохраняем перед выходом
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
