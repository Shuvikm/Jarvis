"""Bleach anime theme styling for J.A.R.V.I.S. UI."""

# Color Palette - Bleach Inspired
COLORS = {
    # Dark backgrounds
    'bg_primary': '#0a0e1a',      # Deep space blue
    'bg_secondary': '#151b2e',     # Slightly lighter
    'bg_tertiary': '#1f2937',      # Card backgrounds
    
    # Spiritual Energy Blues
    'spiritual_blue': '#00d9ff',   # Bright cyan (reishi)
    'spiritual_glow': '#4dd0e1',   # Lighter cyan
    'spiritual_dark': '#0097a7',   # Darker cyan
    
    # Accents
    'accent_gold': '#ffd700',      # Soul Society gold
    'accent_white': '#ffffff',     # Pure white
    'accent_gray': '#9ca3af',      # Muted gray
    
    # Status colors
    'success': '#10b981',          # Green
    'warning': '#f59e0b',          # Orange
    'error': '#ef4444',            # Red
    'listening': '#8b5cf6',        # Purple (active state)
}

# Fonts
FONTS = {
    'primary': 'Segoe UI',
    'secondary': 'Arial',
    'mono': 'Consolas',
}

FONT_SIZES = {
    'title': 24,
    'heading': 18,
    'body': 14,
    'small': 12,
    'tiny': 10,
}

# Animation settings
ANIMATION = {
    'particle_count': 30,
    'particle_speed': 1.0,
    'glow_intensity': 0.8,
    'fade_duration': 300,  # ms
    'pulse_duration': 1500,  # ms
}

# Window settings
WINDOW = {
    'border_radius': 10,
    'shadow_blur': 20,
    'padding': 20,
}

# Qt Stylesheet
QT_STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['bg_primary']};
    border-radius: {WINDOW['border_radius']}px;
}}

QWidget {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['accent_white']};
    font-family: {FONTS['primary']};
    font-size: {FONT_SIZES['body']}px;
}}

QPushButton {{
    background-color: {COLORS['bg_tertiary']};
    border: 2px solid {COLORS['spiritual_blue']};
    border-radius: 8px;
    padding: 10px 20px;
    color: {COLORS['accent_white']};
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {COLORS['spiritual_dark']};
    border-color: {COLORS['spiritual_glow']};
}}

QPushButton:pressed {{
    background-color: {COLORS['spiritual_blue']};
}}

QLabel {{
    background-color: transparent;
    color: {COLORS['accent_white']};
}}

.title {{
    font-size: {FONT_SIZES['title']}px;
    font-weight: bold;
    color: {COLORS['spiritual_blue']};
}}

.status {{
    font-size: {FONT_SIZES['small']}px;
    color: {COLORS['accent_gray']};
}}

.listening {{
    color: {COLORS['listening']};
    font-weight: bold;
}}

QTextEdit {{
    background-color: {COLORS['bg_secondary']};
    border: 1px solid {COLORS['bg_tertiary']};
    border-radius: 8px;
    padding: 10px;
    color: {COLORS['accent_white']};
}}

QScrollBar:vertical {{
    background-color: {COLORS['bg_secondary']};
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['spiritual_blue']};
    border-radius: 5px;
}}
"""
