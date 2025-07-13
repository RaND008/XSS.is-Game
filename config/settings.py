"""
Настройки и константы игры XSS Game
"""

import sys
import os
from datetime import datetime

# Установка UTF-8 кодировки для Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

# Настройки аудио
AUDIO_SETTINGS = {
    'music_enabled': True,
    'sound_enabled': True,
    'music_volume': 0.3,
    'sound_volume': 0.5,
    'background_music': "music/cyberpunk_ambient.mp3"
}

# Пути к звуковым эффектам
SOUND_EFFECTS = {
    # Основные звуки
    "keypress": "sounds/key_press.mp3",
    "typing": "sounds/keyboard_typing.mp3",
    "success": "sounds/success.mp3",
    "fail": "sounds/fail.mp3",
    "error": "sounds/error.mp3",

    # Игровые события
    "mission_start": "sounds/mission_start.mp3",
    "mission_complete": "sounds/mission_complete.mp3",
    "hack_success": "sounds/hack_success.mp3",
    "alert": "sounds/alert.mp3",
    "warning": "sounds/warning.mp3",

    # Экономика
    "coin": "sounds/coin.mp3",
    "purchase": "sounds/purchase.mp3",
    "sell": "sounds/sell.mp3",

    # Система
    "login": "sounds/system_login.mp3",
    "logout": "sounds/system_logout.mp3",
    "message": "sounds/message.mp3",
    "notification": "sounds/notification.mp3",

    # Прогресс
    "level_up": "sounds/level_up.mp3",
    "skill_up": "sounds/skill_increase.mp3",
    "achievement": "sounds/achievement.mp3",

    # Мини-игры
    "minigame_start": "sounds/minigame_start.mp3",
    "minigame_win": "sounds/minigame_win.mp3",
    "minigame_lose": "sounds/minigame_lose.mp3"
}

# Основные настройки игры
GAME_VERSION = "0.3.5"
CODENAME = "RESTRUCTURED"

# Настройки игры
GAME_SETTINGS = {
    'save_file': 'xss_save.json',
    'typing_delay': 0.03,
    'max_skill_level': 10,
    'max_warnings': 3,
    'max_heat_level': 100,
    'event_check_frequency': 3,  # Проверка событий каждые N ходов
    'autosave_frequency': 10     # Автосохранение каждые N ходов
}

# Начальное состояние игрока
INITIAL_PLAYER_STATE = {
    "reputation": 15,
    "usd_balance": 500.0,
    "btc_balance": 20.0,
    "ETH": 0.0,
    "LTC": 0.0,
    "XRP": 0.0,
    "DOGE": 0.0,
    "skills": {
        "scanning": 1,
        "cracking": 1,
        "stealth": 1,
        "social_eng": 1
    },
    "active_mission": None,
    "mission_progress": 0,
    "story_stage": 0,
    "warnings": 0,
    "username": "rand",
    "join_date": "2024-05-30",
    "last_seen": datetime.now().strftime("%H:%M"),
    "inventory": [],
    "turn_number": 0,
    "contacts": [],
    "completed_missions": [],
    "story_choices": {},
    "faction": None,
    "heat_level": 0,
    "achievements": [],
    "seen_items": []
}

# Категории товаров в магазине
ITEM_CATEGORIES = {
    "software": {"name": "Софт", "icon": "💾", "color_key": "INFO"},
    "hardware": {"name": "Железо", "icon": "🔧", "color_key": "WARNING"},
    "service": {"name": "Сервисы", "icon": "🌐", "color_key": "SUCCESS"},
    "malware": {"name": "Малварь", "icon": "☠️", "color_key": "DANGER"},
    "exploits": {"name": "Эксплойты", "icon": "🔓", "color_key": "ERROR"},
    "documents": {"name": "Документы", "icon": "📄", "color_key": "PROMPT"},
    "access": {"name": "Доступы", "icon": "🔑", "color_key": "HEADER"}
}

# Настройки форматирования
DISPLAY_SETTINGS = {
    'banner_width': 60,
    'max_forum_posts': 10,
    'max_inventory_display': 5,
    'progress_bar_length': 20
}

# Валидаторы
VALIDATION_RULES = {
    'username_min_length': 3,
    'username_max_length': 20,
    'btc_min_amount': 0.0001,
    'usd_min_amount': 0.01,
    'skill_min': 0,
    'skill_max': 10
}