# -*- coding: utf-8 -*-

class AppStyles:
    COLORS = {
        'bg_gradient': 'qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, stop:0 #3a7bd5, stop:1 #001f3f)',
        'glass_bg': 'rgba(255, 255, 255, 0.12)',
        'glass_border': 'rgba(255, 255, 255, 0.15)',
    }
    
    MAIN_STYLE = f"""
        QMainWindow, QWidget {{
            background: {COLORS['bg_gradient']};
            font-family: 'Segoe UI', sans-serif;
        }}
        QLabel {{ color: white; }}
        
        /* Стеклянные кнопки */
        QPushButton {{
            background-color: {COLORS['glass_bg']};
            color: white;
            border: 1px solid {COLORS['glass_border']};
            border-radius: 12px;
            font-size: 13px;
            letter-spacing: 1px;
            padding: 10px 20px;
            text-transform: uppercase;
        }}
        QPushButton:hover {{ background-color: rgba(255, 255, 255, 0.2); }}
        QPushButton:disabled {{ color: rgba(255, 255, 255, 0.2); border-color: transparent; }}

        /* Заголовок в стиле референса */
        QLabel#header_label {{
            font-size: 32px;
            letter-spacing: 10px;
            font-weight: 200;
            margin: 20px;
        }}
    """
    
    @staticmethod
    def timer_display():
        return "QLabel { font-size: 72px; font-weight: 200; background: rgba(255,255,255,0.12); " \
               "border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 30px; }"

    @staticmethod
    def tab_button(active=False):
        if active: return "QPushButton { background: rgba(255,255,255,0.25); border: 1px solid white; }"
        return "QPushButton { background: rgba(255,255,255,0.08); border: 1px solid transparent; }"

    @staticmethod
    def footer_info():
        return "QLabel { color: rgba(255,255,255,0.4); font-size: 11px; letter-spacing: 1px; }"

    @staticmethod
    def stop_alarm_button():
        """Кнопка в общем стиле Glassmorphism, но чуть заметнее"""
        return """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.25); /* Более плотное стекло */
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 12px;
                /*font-weight: bold;*/
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.45);
                border: 1px solid #ffffff;
                /* Легкое свечение при наведении */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """


    @staticmethod
    def exit_button():
        """Кнопка выхода"""
        return """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255, 77, 77, 0.2);
                color: #ff4d4d;
                border: 1px solid #ff4d4d;
            }
        """
