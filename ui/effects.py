"""
Визуальные эффекты и анимации для XSS Game
"""

import sys
import time
import textwrap
from typing import Optional

from ui.colors import XSSColors
from systems.audio import audio_system


def typing_effect(text: str, delay: float = 0.03) -> None:
    """Эффект печати текста с задержкой"""
    # Воспроизводим звук печати для длинных текстов
    if len(text) > 20:
        audio_system.play_sound("typing")
    
    lines = text.split('\n')
    
    for line_num, line in enumerate(lines):
        # Для каждой строки делаем эффект печати
        for i in range(len(line) + 1):
            sys.stdout.write('\r' + line[:i])
            sys.stdout.flush()
            
            if i < len(line):
                time.sleep(delay)
        
        # После каждой строки (кроме последней) добавляем перевод
        if line_num < len(lines) - 1:
            print()  # Переход на новую строку
    
    # Финальный перевод строки
    print()


def print_banner() -> None:
    """Печать баннера игры"""
    banner = f"""
{XSSColors.DANGER}
    ╔═══════════════════════════════════════════════════════════╗
    ║                      XSS.IS FORUM                         ║
    ║              {XSSColors.WARNING}⚠ WARNING: UNAUTHORIZED ACCESS ⚠{XSSColors.DANGER}             ║
    ║                                                           ║
    ║  {XSSColors.SYSTEM}System: TOR Browser 13.0.1{XSSColors.DANGER}                               ║
    ║  {XSSColors.SYSTEM}Connection: Encrypted{XSSColors.DANGER}                                    ║
    ║  {XSSColors.SYSTEM}Location: [REDACTED]{XSSColors.DANGER}                                     ║
    ║                                                           ║
    ║       {XSSColors.INFO}Terminal Access Granted - Use with caution{XSSColors.DANGER}          ║
    ╚═══════════════════════════════════════════════════════════╝
{XSSColors.RESET}"""
    print(banner)


def show_ascii_art(art_type: str) -> None:
    """Показывает ASCII арт для различных событий"""
    arts = {
        "hack": f"""
{XSSColors.SUCCESS}
    ┌─┐┬ ┬┌─┐┌─┐┌─┐┌─┐┌─┐
    └─┐│ ││  │  ├┤ └─┐└─┐
    └─┘└─┘└─┘└─┘└─┘└─┘└─┘
{XSSColors.RESET}""",
        "warning": f"""
{XSSColors.DANGER}
    ╱╲╱╲╱╲╱╲╱╲╱╲╱╲
    ⚠  ВНИМАНИЕ  ⚠
    ╲╱╲╱╲╱╲╱╲╱╲╱╲╱
{XSSColors.RESET}""",
        "level_up": f"""
{XSSColors.SUCCESS}
    ╔═╗╦  ╦╔═╗╦    ╦ ╦╔═╗┬
    ║  ╚╗╔╝║╣ ║    ║ ║╠═╝│
    ╚═╝ ╚╝ ╚═╝╩═╝  ╚═╝╩  o
{XSSColors.RESET}""",
        "money": f"""
{XSSColors.MONEY}
    ╔╗ ╦╔╦╗╔═╗╔═╗╦╔╗╔
    ╠╩╗║ ║ ║  ║ ║║║║║
    ╚═╝╩ ╩ ╚═╝╚═╝╩╝╚╝
{XSSColors.RESET}""",
        "skull": f"""
{XSSColors.DANGER}
        ░░░░░░░░░
        ░▄▀▀▀▀▀▄░
        ░█░░░░░░█
        █░▄░░▄░░█
        █░▀░░▀░░█
        █░░▄▄░░░█
        ░▀▄▄▄▄▄▀░
{XSSColors.RESET}""",
        "shield": f"""
{XSSColors.SUCCESS}
        ╔═══╗
        ║░░░║
        ║░█░║
        ║░░░║
        ╚═▀═╝
{XSSColors.RESET}""",
        "explosion": f"""
{XSSColors.ERROR}
    ░░░▄▄▄▄▄▄▄░░░
    ░▄█▀▀░░░░▀▀█▄
    █▀░░░░░░░░░░▀█
    █░░░░░▄▄▄░░░░█
    █░░░░█░░░█░░░█
    █░░░░░▀▀▀░░░░█
    ▀█░░░░░░░░░░█▀
    ░▀█▄▄▄▄▄▄▄█▀░
{XSSColors.RESET}"""
    }
    
    if art_type in arts:
        print(arts[art_type])


def progress_bar(current: int, total: int, length: int = 20, 
                filled_char: str = "█", empty_char: str = "░",
                color: str = XSSColors.SUCCESS) -> str:
    """Создает прогресс бар"""
    if total == 0:
        return f"[{empty_char * length}]"
    
    progress = min(current / total, 1.0)
    filled_length = int(length * progress)
    empty_length = length - filled_length
    
    bar = filled_char * filled_length + empty_char * empty_length
    return f"[{color}{bar}{XSSColors.RESET}]"


def animate_text(text: str, frames: int = 3, delay: float = 0.5) -> None:
    """Анимация мигающего текста"""
    for _ in range(frames):
        print(f"\r{text}", end='', flush=True)
        time.sleep(delay)
        print(f"\r{' ' * len(text)}", end='', flush=True)
        time.sleep(delay)
    print(f"\r{text}")


def loading_animation(text: str, duration: float = 3.0) -> None:
    """Анимация загрузки с точками"""
    start_time = time.time()
    dots = 0
    
    while time.time() - start_time < duration:
        dots_str = "." * (dots % 4)
        spaces = " " * (3 - len(dots_str))
        print(f"\r{XSSColors.INFO}{text}{dots_str}{spaces}{XSSColors.RESET}", end='', flush=True)
        time.sleep(0.5)
        dots += 1
    
    print(f"\r{XSSColors.SUCCESS}{text} завершено!{XSSColors.RESET}")


def connection_animation() -> None:
    """Анимация установления соединения"""
    steps = [
        "Инициализация TOR соединения",
        "Поиск узлов сети",
        "Установка зашифрованного канала",
        "Аутентификация",
        "Подключение к xss.is"
    ]
    
    for step in steps:
        loading_animation(f"{step}...", 1.5)
        time.sleep(0.3)


def matrix_effect(lines: int = 5, duration: float = 2.0) -> None:
    """Эффект матрицы (упрощенный)"""
    import random
    
    chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for _ in range(lines):
            line = ''.join(random.choice(chars) for _ in range(40))
            print(f"{XSSColors.SUCCESS}{line}{XSSColors.RESET}")
        time.sleep(0.1)


def glitch_effect(text: str, iterations: int = 3) -> None:
    """Эффект глитча текста"""
    import random
    
    for _ in range(iterations):
        # Создаем глитчевую версию
        glitched = ""
        for char in text:
            if random.random() < 0.3:  # 30% шанс глитча
                glitched += random.choice("@#$%&*!?")
            else:
                glitched += char
        
        print(f"\r{XSSColors.ERROR}{glitched}{XSSColors.RESET}", end='', flush=True)
        time.sleep(0.1)
    
    # Показываем оригинальный текст
    print(f"\r{text}{XSSColors.RESET}")


def boxed_text(text: str, width: Optional[int] = None, 
               box_char: str = "═", corner_char: str = "╔╗╚╝",
               side_char: str = "║", color: str = XSSColors.INFO) -> None:
    """Выводит текст в рамке"""
    lines = text.split('\n')
    if width is None:
        width = max(len(line) for line in lines) + 4
    
    # Символы рамки
    top_left, top_right, bottom_left, bottom_right = corner_char
    
    # Верхняя граница
    print(f"{color}{top_left}{box_char * (width - 2)}{top_right}{XSSColors.RESET}")
    
    # Содержимое
    for line in lines:
        padding = width - len(line) - 4
        left_pad = padding // 2
        right_pad = padding - left_pad
        print(f"{color}{side_char}{XSSColors.RESET} {' ' * left_pad}{line}{' ' * right_pad} {color}{side_char}{XSSColors.RESET}")
    
    # Нижняя граница
    print(f"{color}{bottom_left}{box_char * (width - 2)}{bottom_right}{XSSColors.RESET}")


def status_indicator(status: str, value: any, 
                    good_threshold: float = 0.7, 
                    bad_threshold: float = 0.3) -> str:
    """Создает цветной индикатор статуса"""
    if isinstance(value, (int, float)):
        if value >= good_threshold:
            color = XSSColors.SUCCESS
            icon = "✓"
        elif value <= bad_threshold:
            color = XSSColors.ERROR
            icon = "✗"
        else:
            color = XSSColors.WARNING
            icon = "!"
    else:
        color = XSSColors.INFO
        icon = "•"
    
    return f"{color}{icon} {status}: {value}{XSSColors.RESET}"


def skill_bar(skill_name: str, level: int, max_level: int = 10,
              bar_length: int = 10) -> str:
    """Создает полосу навыка"""
    filled = "█" * level
    empty = "░" * (max_level - level)
    bar = filled + empty
    
    # Цвет уровня
    if level >= 8:
        level_color = XSSColors.SUCCESS
    elif level >= 5:
        level_color = XSSColors.WARNING
    else:
        level_color = XSSColors.INFO
    
    return f"{skill_name:<15} [{XSSColors.SUCCESS}{bar}{XSSColors.RESET}] {level_color}{level}/{max_level}{XSSColors.RESET}"


def format_currency(amount: float, currency: str = "BTC") -> str:
    """Форматирует валюту с цветом"""
    if currency == "BTC":
        return f"{XSSColors.MONEY}{amount:.4f} BTC{XSSColors.RESET}"
    elif currency == "USD":
        return f"{XSSColors.MONEY}${amount:.2f}{XSSColors.RESET}"
    else:
        return f"{XSSColors.MONEY}{amount:.4f} {currency}{XSSColors.RESET}"


def format_reputation(rep: int) -> str:
    """Форматирует репутацию с цветом"""
    if rep >= 100:
        color = XSSColors.SUCCESS
    elif rep >= 50:
        color = XSSColors.WARNING
    else:
        color = XSSColors.INFO
    
    return f"{color}{rep} REP{XSSColors.RESET}"


def wrap_text(text: str, width: int = 70, indent: str = "   ") -> str:
    """Переносит текст с отступом"""
    wrapped_lines = textwrap.wrap(text, width=width)
    return '\n'.join(indent + line for line in wrapped_lines)


def countdown(seconds: int, message: str = "Ожидание") -> None:
    """Обратный отсчет"""
    for i in range(seconds, 0, -1):
        print(f"\r{XSSColors.WARNING}{message}: {i}s{XSSColors.RESET}", end='', flush=True)
        time.sleep(1)
    print(f"\r{XSSColors.SUCCESS}{message}: завершено!{XSSColors.RESET}")


def pulse_text(text: str, color: str = XSSColors.WARNING, pulses: int = 3) -> None:
    """Пульсирующий текст"""
    for _ in range(pulses):
        print(f"\r{color}{text}{XSSColors.RESET}", end='', flush=True)
        time.sleep(0.5)
        print(f"\r{XSSColors.RESET}{text}", end='', flush=True)
        time.sleep(0.5)
    print()


def show_mission_timer(time_remaining: float, time_limit: float) -> None:
    """Показывает таймер миссии с визуальными эффектами"""
    percentage = (time_remaining / time_limit) * 100 if time_limit > 0 else 0

    if percentage > 50:
        color = XSSColors.SUCCESS
        icon = "⏰"
    elif percentage > 20:
        color = XSSColors.WARNING
        icon = "⚠️"
    else:
        color = XSSColors.ERROR
        icon = "🚨"

    bar_length = 20
    filled = int((percentage / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)

    print(f"\n{color}{icon} ВРЕМЯ: [{bar}] {time_remaining:.1f}ч / {time_limit}ч{XSSColors.RESET}")

    if percentage <= 10:
        pulse_text(f"КРИТИЧЕСКОЕ ВРЕМЯ!", XSSColors.ERROR, 2)


def show_team_coordination_visual(team_members: list, action: str) -> None:
    """Визуализация командной работы"""
    print(f"\n{XSSColors.INFO}👥 КОМАНДНАЯ КООРДИНАЦИЯ{XSSColors.RESET}")

    # Показываем участников
    roles_icons = {
        "hacker": "💻",
        "social_engineer": "🎭",
        "lookout": "👁️",
        "specialist": "⚡"
    }

    for member in team_members:
        icon = roles_icons.get(member['role'], "👤")
        loyalty_color = XSSColors.SUCCESS if member['loyalty'] >= 70 else XSSColors.WARNING if member[
                                                                                                   'loyalty'] >= 40 else XSSColors.ERROR

        print(f"   {icon} {member['name']} ({loyalty_color}{member['loyalty']}%{XSSColors.RESET})")

    # Анимация действия
    if action == "execute":
        animate_text(">>> ВЫПОЛНЕНИЕ ОПЕРАЦИИ <<<", 3, 0.8)
    elif action == "planning":
        typing_effect("Команда разрабатывает план атаки...", 0.05)
    elif action == "recruit":
        typing_effect("Поиск подходящих кандидатов...", 0.04)


def show_moral_choice_visual(choice_data: dict) -> None:
    """Визуализация морального выбора"""
    print(f"\n{XSSColors.STORY}━━━━━━━━━━━━━━━━ МОРАЛЬНАЯ ДИЛЕММА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    # Обрамляем вопрос в рамку
    boxed_text(choice_data['question'], color=XSSColors.STORY)

    print(f"\n{XSSColors.INFO}🤔 Ваши варианты действий:{XSSColors.RESET}")

    choices = choice_data["choices"]
    choice_icons = {
        "protect": "🛡️",
        "abandon": "💔",
        "profit": "💰",
        "justice": "⚖️",
        "mercy": "🕊️",
        "revenge": "⚔️"
    }

    for i, (choice_id, choice_info) in enumerate(choices.items(), 1):
        # Определяем иконку по ключевым словам
        icon = "•"
        for keyword, choice_icon in choice_icons.items():
            if keyword in choice_id or keyword in choice_info.get('desc', '').lower():
                icon = choice_icon
                break

        print(f"\n   {i}. {icon} {choice_info['desc']}")

        # Показываем потенциальные последствия
        if 'rep_change' in choice_info:
            rep_change = choice_info['rep_change']
            if rep_change > 0:
                print(f"      {XSSColors.SUCCESS}[+{rep_change} репутации]{XSSColors.RESET}")
            elif rep_change < 0:
                print(f"      {XSSColors.ERROR}[{rep_change} репутации]{XSSColors.RESET}")


def show_mission_event_visual(event_data: dict) -> None:
    """Визуализация случайного события миссии"""
    event_icons = {
        "government_trace": "🚨",
        "competitor_interference": "⚔️",
        "insider_help": "🤝",
        "security_upgrade": "🔒",
        "time_pressure": "⏰",
        "equipment_failure": "💥"
    }

    event_type = event_data.get("event", "unknown")
    icon = event_icons.get(event_type, "⚡")

    print(f"\n{XSSColors.DANGER}━━━━━━━━━━━━━━━━ НЕОЖИДАННОЕ СОБЫТИЕ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    # Мигающее предупреждение
    pulse_text(f"{icon} {event_data['desc']}", XSSColors.WARNING, 3)

    # Показываем эффекты
    effects = event_data.get("effects", {})
    if effects:
        print(f"\n{XSSColors.INFO}📊 Влияние на миссию:{XSSColors.RESET}")

        for effect, value in effects.items():
            if effect == "heat_gain":
                print(f"   🔥 Heat Level: +{value}%")
            elif effect == "risk_increase":
                print(f"   ⚠️ Риск провала: +{value}%")
            elif effect == "time_pressure":
                print(f"   ⏰ Ограничение времени активировано")
            elif effect == "difficulty_increase":
                print(f"   📈 Сложность: +{value}")


def show_stage_completion_visual(stage_name: str, stage_number: int, total_stages: int) -> None:
    """Визуализация завершения этапа"""
    print(f"\n{XSSColors.SUCCESS}━━━━━━━━━━━━━━━━ ЭТАП ЗАВЕРШЕН ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    # Прогресс бар этапов
    stage_bar = ""
    for i in range(total_stages):
        if i < stage_number:
            stage_bar += f"{XSSColors.SUCCESS}█{XSSColors.RESET}"
        elif i == stage_number:
            stage_bar += f"{XSSColors.WARNING}█{XSSColors.RESET}"
        else:
            stage_bar += f"{XSSColors.DARK_GRAY}░{XSSColors.RESET}"

    print(f"\n   ✅ {stage_name}")
    print(f"   Прогресс: [{stage_bar}] {stage_number + 1}/{total_stages}")

    if stage_number + 1 < total_stages:
        print(f"\n{XSSColors.INFO}🎯 Переход к следующему этапу...{XSSColors.RESET}")
    else:
        print(f"\n{XSSColors.SUCCESS}🎉 ВСЕ ЭТАПЫ ЗАВЕРШЕНЫ!{XSSColors.RESET}")


def show_team_recruitment_visual(candidates: list) -> None:
    """Визуализация набора команды"""
    print(f"\n{XSSColors.WARNING}━━━━━━━━━━━━━━━━ НАБОР КОМАНДЫ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    for i, candidate in enumerate(candidates, 1):
        # Цвет в зависимости от навыка
        skill_level = candidate['skill_level']
        if skill_level >= 8:
            skill_color = XSSColors.SUCCESS
            skill_desc = "ЭЛИТНЫЙ"
        elif skill_level >= 6:
            skill_color = XSSColors.WARNING
            skill_desc = "ОПЫТНЫЙ"
        elif skill_level >= 4:
            skill_color = XSSColors.INFO
            skill_desc = "СРЕДНИЙ"
        else:
            skill_color = XSSColors.ERROR
            skill_desc = "НОВИЧОК"

        # Роль с иконкой
        role_icons = {
            "hacker": "💻",
            "social_engineer": "🎭",
            "lookout": "👁️",
            "specialist": "⚡"
        }
        role_icon = role_icons.get(candidate['role'], "👤")

        print(f"\n   {i}. {role_icon} {XSSColors.BRIGHT_GREEN}{candidate['name']}{XSSColors.RESET}")
        print(f"      Роль: {candidate['role']}")
        print(f"      Навык: {skill_color}{skill_level}/10 ({skill_desc}){XSSColors.RESET}")
        print(f"      Лояльность: {candidate['loyalty']}%")
        print(f"      Стоимость: {XSSColors.MONEY}{candidate['cost']} BTC/этап{XSSColors.RESET}")
        print(f"      Особенности: {XSSColors.INFO}{candidate['traits']}{XSSColors.RESET}")


def show_mission_failure_sequence(reason: str) -> None:
    """Визуализация провала миссии"""
    print(f"\n{XSSColors.ERROR}━━━━━━━━━━━━━━━━ МИССИЯ ПРОВАЛЕНА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    # ASCII арт провала
    failure_art = f"""
{XSSColors.ERROR}
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░██░░░░██░░░░░░░░░░░░░░░░░░░░░
    ░██░░██░░░░██░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░██████████░░░░░░░░░░░░░░
    ░░░░░██░░░░░░░░░░██░░░░░░░░░░░░
    ░░░░██░░░░░░░░░░░░░██░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
{XSSColors.RESET}"""

    print(failure_art)

    failure_messages = {
        "detected": "ВАС ОБНАРУЖИЛИ!",
        "timeout": "ВРЕМЯ ИСТЕКЛО!",
        "team_betrayal": "КОМАНДА ПРЕДАЛА!",
        "security_breach": "ЗАЩИТА СРАБОТАЛА!",
        "insufficient_skills": "НЕДОСТАТОЧНО НАВЫКОВ!"
    }

    message = failure_messages.get(reason, "НЕИЗВЕСТНАЯ ОШИБКА!")

    # Мигающее сообщение об ошибке
    for _ in range(3):
        print(f"\r{XSSColors.ERROR}💥 {message} 💥{XSSColors.RESET}", end='', flush=True)
        time.sleep(0.5)
        print(f"\r{' ' * (len(message) + 6)}", end='', flush=True)
        time.sleep(0.5)

    print(f"\r{XSSColors.ERROR}💥 {message} 💥{XSSColors.RESET}")


def show_mission_success_sequence(mission_name: str, rewards: dict) -> None:
    """Визуализация успешного завершения миссии"""
    print(f"\n{XSSColors.SUCCESS}━━━━━━━━━━━━━━━━ МИССИЯ ВЫПОЛНЕНА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    # ASCII арт успеха
    success_art = f"""
{XSSColors.SUCCESS}
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░██████░░░░░░░░░░░░░░
        ░░░░░░░░██░░░░░░██░░░░░░░░░░░░
        ░░░░░░██░░░░░░░░░░██░░░░░░░░░░
        ░░░░██░░░░██░░██░░░░██░░░░░░░░
        ░░░░██░░░░░░░░░░░░░░██░░░░░░░░
        ░░░░░░██░░██████░░██░░░░░░░░░░
        ░░░░░░░░██░░░░░░██░░░░░░░░░░░░
        ░░░░░░░░░░██████░░░░░░░░░░░░░░
{XSSColors.RESET}"""

    print(success_art)

    # Анимированный заголовок
    animate_text(f"🎉 {mission_name.upper()} - ЗАВЕРШЕНО! 🎉", 2, 1.0)

    # Показываем награды с анимацией
    print(f"\n{XSSColors.MONEY}💰 ПОЛУЧЕННЫЕ НАГРАДЫ:{XSSColors.RESET}")

    for reward_type, value in rewards.items():
        time.sleep(0.5)
        if reward_type == "btc":
            print(f"   💎 {XSSColors.MONEY}+{value} BTC{XSSColors.RESET}")
        elif reward_type == "reputation":
            print(f"   📈 {XSSColors.REP}+{value} репутации{XSSColors.RESET}")
        elif reward_type == "items":
            for item in value if isinstance(value, list) else [value]:
                print(f"   📦 {XSSColors.INFO}Получен предмет: {item}{XSSColors.RESET}")
        elif reward_type == "contacts":
            for contact in value if isinstance(value, list) else [value]:
                print(f"   📱 {XSSColors.WARNING}Новый контакт: {contact}{XSSColors.RESET}")


def show_countdown_timer(seconds: int, message: str = "Начало операции через") -> None:
    """Обратный отсчет с визуальными эффектами"""
    for i in range(seconds, 0, -1):
        # Цвет меняется по мере приближения к нулю
        if i > 5:
            color = XSSColors.INFO
        elif i > 2:
            color = XSSColors.WARNING
        else:
            color = XSSColors.ERROR

        # Большие числа для драматичности
        big_number = f"""
{color}
     ███  
    █████ 
     ███  
     ███  
    █████ 
{XSSColors.RESET}""" if i == 1 else f"{color}{i}{XSSColors.RESET}"

        print(f"\r{color}{message}: {i}s{XSSColors.RESET}", end='', flush=True)

        # Звуковые эффекты для последних секунд
        if i <= 3:
            print("\a", end='')  # Системный звук

        time.sleep(1)

    print(f"\r{XSSColors.SUCCESS}🚀 СТАРТ!{' ' * 30}{XSSColors.RESET}")


def show_hacking_progress(target: str, progress_steps: list) -> None:
    """Показывает прогресс взлома с реалистичными этапами"""
    print(f"\n{XSSColors.INFO}🎯 Цель: {target}{XSSColors.RESET}")
    print(f"{XSSColors.HEADER}━━━━━━━━━━━━━━━━ ПРОЦЕСС ВЗЛОМА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    for i, step in enumerate(progress_steps):
        step_icons = {
            "scan": "🔍",
            "exploit": "💥",
            "payload": "📡",
            "access": "🔓",
            "extract": "📤",
            "cover": "🌫️"
        }

        step_type = step.get("type", "unknown")
        icon = step_icons.get(step_type, "⚡")
        description = step.get("description", "Выполнение...")
        duration = step.get("duration", 2)

        print(f"\n{XSSColors.WARNING}[{i + 1}/{len(progress_steps)}] {icon} {description}{XSSColors.RESET}")

        # Прогресс бар для этапа
        for j in range(duration * 2):
            progress = (j + 1) / (duration * 2)
            bar_length = 30
            filled = int(progress * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)

            percentage = int(progress * 100)
            print(f"\r         [{XSSColors.SUCCESS}{bar}{XSSColors.RESET}] {percentage}%", end='', flush=True)
            time.sleep(0.5)

        print(f" {XSSColors.SUCCESS}✓{XSSColors.RESET}")

    print(f"\n{XSSColors.SUCCESS}🎉 ВЗЛОМ ЗАВЕРШЕН УСПЕШНО!{XSSColors.RESET}")