# -*- coding: utf-8 -*-
import os
import winsound
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QSpinBox, QMessageBox,
                               QComboBox, QFileDialog, QGroupBox)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont

from styles import AppStyles

class TimerWidget(QWidget):
    """Таймер обратного отсчёта с выбором звука"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("TimerWidget")
        
        self.time_left = 0
        self.is_running = False
        self.selected_sound = None
        self.alarm_active = False
        
        self.init_ui()
        self.setup_timer()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Группа установки времени
        time_group = QGroupBox("Установка времени")
        time_layout = QVBoxLayout(time_group)
        
        spin_layout = QHBoxLayout()
        spin_layout.addStretch()
        
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(0, 23)
        self.hours_spin.setSuffix(" ч")
        self.hours_spin.setFixedWidth(80)
        spin_layout.addWidget(self.hours_spin)
        
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 59)
        self.minutes_spin.setSuffix(" мин")
        self.minutes_spin.setFixedWidth(80)
        spin_layout.addWidget(self.minutes_spin)
        
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 59)
        self.seconds_spin.setSuffix(" сек")
        self.seconds_spin.setFixedWidth(80)
        spin_layout.addWidget(self.seconds_spin)
        
        spin_layout.addStretch()
        time_layout.addLayout(spin_layout)
        
        self.set_btn = QPushButton("Установить время")
        self.set_btn.clicked.connect(self.set_time)
        time_layout.addWidget(self.set_btn)
        
        layout.addWidget(time_group)
        
        # Группа выбора звука
        sound_group = QGroupBox("Звук сигнала")
        sound_layout = QVBoxLayout(sound_group)
        
        sound_choice_layout = QHBoxLayout()
        self.sound_combo = QComboBox()
        self.update_sound_list()
        self.sound_combo.currentIndexChanged.connect(self.on_sound_selected)
        sound_choice_layout.addWidget(self.sound_combo)
        
        self.sound_path_label = QLabel("")
        self.sound_path_label.setStyleSheet("color: #888888; font-size: 10px;")
        sound_choice_layout.addWidget(self.sound_path_label)
        sound_choice_layout.addStretch()
        
        sound_layout.addLayout(sound_choice_layout)
        
        self.test_sound_btn = QPushButton("Тест звука")
        self.test_sound_btn.clicked.connect(self.test_sound)
        sound_layout.addWidget(self.test_sound_btn)
        
        layout.addWidget(sound_group)
        
        # Дисплей таймера
        self.display = QLabel("00:00:00")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setFont(QFont("Arial", 72, QFont.Bold))
        self.display.setStyleSheet(AppStyles.timer_display())
        layout.addWidget(self.display)
        
        # Кнопки управления
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Старт")
        self.start_btn.clicked.connect(self.start)
        self.start_btn.setEnabled(False)
        control_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("Пауза")
        self.pause_btn.clicked.connect(self.pause)
        self.pause_btn.setEnabled(False)
        control_layout.addWidget(self.pause_btn)
        
        self.reset_btn = QPushButton("Сброс")
        self.reset_btn.clicked.connect(self.reset)
        self.reset_btn.setEnabled(False)
        control_layout.addWidget(self.reset_btn)
        
        self.stop_alarm_btn = QPushButton("Отключить сигнал")
        self.stop_alarm_btn.setStyleSheet(AppStyles.stop_alarm_button())
        self.stop_alarm_btn.clicked.connect(self.stop_alarm)
        self.stop_alarm_btn.setEnabled(False)
        control_layout.addWidget(self.stop_alarm_btn)
        
        layout.addLayout(control_layout)
        
        # Информационная метка
        self.info_label = QLabel("Введите время и нажмите 'Установить'")
        self.info_label.setObjectName("info_label")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)
    
    def update_sound_list(self):
        """Обновить список доступных системных звуков Windows"""
        windows_media = "C:\\Windows\\Media"
        
        self.sound_combo.clear()
        self.sound_combo.addItem("🔇 Без звука", None)
        
        if os.path.exists(windows_media):
            wav_files = []
            for file in os.listdir(windows_media):
                if file.lower().endswith('.wav'):
                    wav_files.append(file)
            
            wav_files.sort()
            
            for filename in wav_files:
                full_path = os.path.join(windows_media, filename)
                display_name = filename.replace('.wav', '').replace('_', ' ')
                self.sound_combo.addItem(f"🔊 {display_name}", full_path)
            
            print(f"Найдено WAV файлов в системе: {len(wav_files)}")
        
        self.sound_combo.addItem("🎵 Выбрать свой WAV файл...", "custom")
    
    def on_sound_selected(self, index):
        """Обработка выбора звука"""
        sound_path = self.sound_combo.currentData()
        
        if sound_path == "custom":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите WAV файл для сигнала",
                "",
                "WAV файлы (*.wav);;Все файлы (*.*)"
            )
            if file_path:
                self.selected_sound = file_path
                self.sound_combo.addItem(f"📁 {os.path.basename(file_path)}", file_path)
                self.sound_combo.setCurrentIndex(self.sound_combo.count() - 1)
                self.sound_path_label.setText(file_path)
                self.sound_path_label.setStyleSheet("color: #4CAF50; font-size: 10px;")
            else:
                self.sound_combo.setCurrentIndex(0)
                self.selected_sound = None
        elif sound_path:
            self.selected_sound = sound_path
            self.sound_path_label.setText(os.path.basename(sound_path))
            self.sound_path_label.setStyleSheet("color: #888888; font-size: 10px;")
        else:
            self.selected_sound = None
            self.sound_path_label.setText("")
    
    def test_sound(self):
        """Тестирование выбранного звука"""
        if self.selected_sound and os.path.exists(self.selected_sound):
            try:
                winsound.PlaySound(self.selected_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
                self.info_label.setText("🔊 Звук проигрывается...")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось воспроизвести звук:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Ошибка", "Звуковой файл не найден!\nВыберите другой звук.")
    
    def play_alarm(self):
        """Воспроизведение зацикленного сигнала"""
        if self.selected_sound and os.path.exists(self.selected_sound):
            try:
                self.alarm_active = True
                self.stop_alarm_btn.setEnabled(True)
                winsound.PlaySound(self.selected_sound, 
                                  winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            except:
                self.beep_alarm()
        else:
            self.beep_alarm()
    
    def beep_alarm(self):
        """Повторяющийся писк"""
        self.alarm_active = True
        self.stop_alarm_btn.setEnabled(True)
        self.alarm_timer = QTimer()
        self.alarm_timer.timeout.connect(lambda: winsound.Beep(1000, 500))
        self.alarm_timer.start(1500)
    
    def stop_alarm(self):
        """Остановить сигнал"""
        self.alarm_active = False
        self.stop_alarm_btn.setEnabled(False)
        winsound.PlaySound(None, winsound.SND_PURGE)
        if hasattr(self, 'alarm_timer'):
            self.alarm_timer.stop()
        self.info_label.setText("Сигнал отключён")
    
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
    
    def set_time(self):
        total_seconds = (self.hours_spin.value() * 3600 + 
                        self.minutes_spin.value() * 60 + 
                        self.seconds_spin.value())
        
        if total_seconds <= 0:
            QMessageBox.warning(self, "Ошибка", "Введите время больше 0")
            return
        
        self.time_left = total_seconds
        self.update_display()
        
        self.start_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.set_btn.setEnabled(False)
        self.info_label.setText("Время установлено. Нажмите 'Старт'")
    
    def start(self):
        if self.time_left <= 0:
            return
        
        self.is_running = True
        self.timer.start(1000)
        
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.info_label.setText("Таймер запущен...")
    
    def pause(self):
        self.is_running = False
        self.timer.stop()
        
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.info_label.setText("Таймер на паузе")
    
    def reset(self):
        if self.alarm_active:
            self.stop_alarm()
        
        self.is_running = False
        self.timer.stop()
        
        self.time_left = 0
        self.update_display()
        
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)
        self.set_btn.setEnabled(True)
        
        self.info_label.setText("Время сброшено. Установите новое.")
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            
            if self.time_left == 0:
                self.timer.stop()
                self.is_running = False
                self.start_btn.setEnabled(False)
                self.pause_btn.setEnabled(False)
                self.info_label.setText("⏰ Время вышло! ⏰")
                self.play_alarm()
        else:
            self.pause()
    
    def update_display(self):
        hours = self.time_left // 3600
        minutes = (self.time_left % 3600) // 60
        seconds = self.time_left % 60
        self.display.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")