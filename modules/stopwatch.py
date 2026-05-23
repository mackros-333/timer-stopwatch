# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtCore import QTimer, Qt
from styles import AppStyles

class StopwatchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.time_elapsed = 0
        self.is_running = False
        self.lap_count = 0
        self.last_lap_time = 0
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        self.display = QLabel("00:00:00.00")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet(AppStyles.timer_display())
        layout.addWidget(self.display)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("СТАРТ")
        self.pause_btn = QPushButton("ПАУЗА")
        self.reset_btn = QPushButton("СБРОС")
        
        for b in [self.start_btn, self.pause_btn, self.reset_btn]: btn_layout.addWidget(b)
        layout.addLayout(btn_layout)

        self.lap_btn = QPushButton("ФИКСАЦИЯ")
        layout.addWidget(self.lap_btn)

        self.laps_list = QListWidget()
        self.laps_list.setStyleSheet("background: rgba(255,255,255,0.05); border-radius: 15px; color: white; border: none;")
        layout.addWidget(self.laps_list)

        # Коннекты
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.start_btn.clicked.connect(self.start)
        self.pause_btn.clicked.connect(self.pause)
        self.reset_btn.clicked.connect(self.reset)
        self.lap_btn.clicked.connect(self.add_lap)

    def start(self): 
        self.timer.start(10); self.is_running = True
    def pause(self): 
        self.timer.stop(); self.is_running = False
    def reset(self):
        self.timer.stop(); self.time_elapsed = 0; self.laps_list.clear(); self.update_display()
    def add_lap(self):
        self.lap_count += 1
        txt = f"LAP {self.lap_count:02d} | {self.format_time(self.time_elapsed)}"
        self.laps_list.addItem(QListWidgetItem(txt))
        if self.window() and hasattr(self.window(), 'save_settings'):
            self.window().save_settings()

    def update_timer(self):
        self.time_elapsed += 10
        self.update_display()
    def update_display(self):
        self.display.setText(self.format_time(self.time_elapsed))
    def format_time(self, ms):
        s, ms = divmod(ms, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}.{ms//10:02d}"
