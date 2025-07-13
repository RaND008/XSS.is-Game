"""
Функции отображения интерфейса
"""

from typing import Dict, Any
from ui.colors import XSSColors
from ui.effects import skill_bar, format_currency, format_reputation, progress_bar
from config.settings import ITEM_CATEGORIES


def show_status(game_state) -> None:
    """Улучшенный вывод статуса игрока"""
    print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━ ВАШ ПРОФИЛЬ ━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    # Основная информация
    print(f"\n{XSSColors.INFO}👤 ИНФОРМАЦИЯ:{XSSColors.RESET}")
    print(f"   {XSSColors.PROMPT}Никнейм:{XSSColors.RESET} {game_state.get_stat('username')}")
    print(f"   {XSSColors.PROMPT}Дата регистрации:{XSSColors.RESET} {game_state.get_stat('join_date')}")
    print(f"   {XSSColors.PROMPT}Последний визит:{XSSColors.RESET} {game_state.get_stat('last_seen')}")
    
    faction_name = game_state.get_stat('faction', 'Нет')
    faction_color = XSSColors.SUCCESS if faction_name != 'Нет' else XSSColors.WARNING
    print(f"   {XSSColors.PROMPT}Фракция:{XSSColors.RESET} {faction_color}{faction_name}{XSSColors.RESET}")

    # Статистика
    print(f"\n{XSSColors.INFO}📊 СТАТИСТИКА:{XSSColors.RESET}")
    reputation = game_state.get_stat('reputation')
    print(f"   {format_reputation(reputation)}")

    # Heat Level с цветовой индикацией
    heat_level = game_state.get_stat("heat_level", 0)
    if heat_level < 30:
        heat_color = XSSColors.SUCCESS
        heat_status = "Низкий"
    elif heat_level < 70:
        heat_color = XSSColors.WARNING
        heat_status = "Средний"
    else:
        heat_color = XSSColors.DANGER
        heat_status = "КРИТИЧЕСКИЙ"
    print(f"   {XSSColors.INFO}Heat Level:{XSSColors.RESET} {heat_color}{heat_level}% ({heat_status}){XSSColors.RESET}")

    # Предупреждения
    warnings = game_state.get_stat('warnings', 0)
    if warnings == 0:
        warn_color = XSSColors.SUCCESS
    elif warnings == 1:
        warn_color = XSSColors.WARNING
    else:
        warn_color = XSSColors.ERROR
    print(f"   {XSSColors.INFO}Предупреждения:{XSSColors.RESET} {warn_color}{warnings}/3{XSSColors.RESET}")

    # Финансы
    print(f"\n{XSSColors.MONEY}💰 ФИНАНСЫ:{XSSColors.RESET}")
    btc_balance = game_state.get_stat('btc_balance', 0)
    usd_balance = game_state.get_stat('usd_balance', 0)
    print(f"   {format_currency(btc_balance, 'BTC')}")
    print(f"   {format_currency(usd_balance, 'USD')}")

    # Криптопортфель
    crypto_symbols = ["ETH", "LTC", "XRP", "DOGE"]
    has_crypto = any(game_state.get_stat(crypto, 0) > 0 for crypto in crypto_symbols)
    if has_crypto:
        print(f"\n{XSSColors.MONEY}📈 КРИПТОПОРТФЕЛЬ:{XSSColors.RESET}")
        for crypto in crypto_symbols:
            amount = game_state.get_stat(crypto, 0)
            if amount > 0:
                print(f"   {crypto}: {amount:.4f}")

    # Навыки
    print(f"\n{XSSColors.SKILL}🎯 НАВЫКИ:{XSSColors.RESET}")
    skills = game_state.get_stat('skills', {})
    for skill, level in skills.items():
        print(f"   {skill_bar(skill.replace('_', ' ').title(), level)}")

    # Снаряжение
    inventory = game_state.get_stat('inventory', [])
    inventory_count = len(inventory)
    print(f"\n{XSSColors.INFO}🎒 СНАРЯЖЕНИЕ: {inventory_count} предметов{XSSColors.RESET}")
    if inventory_count > 0:
        shown = min(5, inventory_count)
        for i in range(shown):
            print(f"   • {inventory[i]}")
        if inventory_count > 5:
            print(f"   ... и еще {inventory_count - 5} предметов")
    else:
        print(f"   {XSSColors.WARNING}Инвентарь пуст{XSSColors.RESET}")

    # Активная миссия
    print(f"\n{XSSColors.WARNING}📋 АКТИВНАЯ МИССИЯ:{XSSColors.RESET}")
    active_mission = game_state.get_stat("active_mission")
    if active_mission:
        progress = game_state.get_stat("mission_progress", 0)
        # Здесь нужно будет получить длительность миссии из системы миссий
        duration = 5  # Временно
        
        print(f"   {active_mission}")
        bar = progress_bar(progress, duration)
        print(f"   Прогресс: {bar} {progress}/{duration}")
    else:
        print(f"   {XSSColors.WARNING}Нет активной миссии{XSSColors.RESET}")

    # Достижения
    achievements = game_state.get_stat('achievements', [])
    achievements_count = len(achievements)
    total_achievements = 10  # Временно, нужно получать из системы достижений
    
    achievement_percent = int((achievements_count / total_achievements) * 100) if total_achievements > 0 else 0
    if achievement_percent >= 80:
        ach_color = XSSColors.SUCCESS
    elif achievement_percent >= 50:
        ach_color = XSSColors.WARNING
    else:
        ach_color = XSSColors.INFO

    print(f"\n{XSSColors.INFO}🏆 ДОСТИЖЕНИЯ: {ach_color}{achievements_count}/{total_achievements} ({achievement_percent}%){XSSColors.RESET}")

    # Сюжетный этап
    story_stage = game_state.get_stat("story_stage", 0)
    story_stages = {
        0: "Новичок на форуме",
        1: "Первые шаги", 
        2: "Доверенный участник",
        3: "Элитный хакер",
        4: "Легенда подполья"
    }
    stage_title = story_stages.get(story_stage, "Неизвестный этап")
    print(f"\n{XSSColors.STORY}📖 СЮЖЕТНЫЙ ЭТАП: {stage_title}{XSSColors.RESET}")

    print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")


def show_help():
    """Показывает основную справку с ссылкой на полный список"""
    print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ СПРАВКА XSS GAME ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    print(f"\n{XSSColors.INFO}🎯 ОСНОВНЫЕ КОМАНДЫ:{XSSColors.RESET}")
    basic_commands = [
        ("status", "Ваш профиль и статистика"),
        ("missions", "Доступные задания"),
        ("market", "Теневой рынок"),
        ("training", "Развитие навыков"),
        ("forum", "Хакерский форум"),
        ("crypto", "Криптобиржа"),
        ("network", "Сетевые инструменты")
    ]

    for cmd, desc in basic_commands:
        print(f"   {XSSColors.SUCCESS}{cmd:<12}{XSSColors.RESET} {desc}")

    print(f"\n{XSSColors.WARNING}⚡ БЫСТРЫЕ КОМАНДЫ:{XSSColors.RESET}")
    quick_commands = [
        ("take <id>", "Взять миссию"),
        ("buy <id>", "Купить предмет"),
        ("work", "Работать над миссией"),
        ("connect <ip>", "Подключиться к узлу"),
        ("nmap <target>", "Сканировать цель"),
        ("save", "Сохранить игру"),
        ("exit", "Выйти из игры")
    ]

    for cmd, desc in quick_commands:
        print(f"   {XSSColors.WARNING}{cmd:<15}{XSSColors.RESET} {desc}")

    print(f"\n{XSSColors.INFO}🌐 СЕТЕВЫЕ ОПЕРАЦИИ:{XSSColors.RESET}")
    network_commands = [
        ("vpn", "Управление VPN"),
        ("scan", "Сканировать сеть"),
        ("botnet", "Управление ботнетами"),
        ("ddos <target>", "DDoS атака")
    ]

    for cmd, desc in network_commands:
        print(f"   {XSSColors.INFO}{cmd:<15}{XSSColors.RESET} {desc}")

    print(f"\n{XSSColors.SUCCESS}🎮 РАЗВИТИЕ И ПРОГРЕСС:{XSSColors.RESET}")
    progress_commands = [
        ("faction", "Информация о фракции"),
        ("join_faction", "Присоединиться к фракции"),
        ("mission_stats", "Статистика миссий"),
        ("moral_profile", "Моральный профиль")
    ]

    for cmd, desc in progress_commands:
        print(f"   {XSSColors.SUCCESS}{cmd:<15}{XSSColors.RESET} {desc}")

    print(f"\n{XSSColors.INFO}📚 ПОЛУЧИТЬ БОЛЬШЕ ПОМОЩИ:{XSSColors.RESET}")
    print(f"   {XSSColors.BRIGHT_GREEN}commands{XSSColors.RESET}        Полный список всех команд с описаниями")
    print(f"   {XSSColors.BRIGHT_GREEN}help <команда>{XSSColors.RESET}   Подробная справка по конкретной команде")
    print(f"   {XSSColors.BRIGHT_GREEN}tips{XSSColors.RESET}           Советы и рекомендации для новичков")

    # Проверяем доступность readline для автодополнения
    try:
        import readline
        has_readline = True
    except ImportError:
        has_readline = False

    if has_readline:
        print(f"\n{XSSColors.SUCCESS}💡 АВТОДОПОЛНЕНИЕ:{XSSColors.RESET}")
        print(f"   • Нажмите {XSSColors.WARNING}TAB{XSSColors.RESET} для автодополнения команд и аргументов")
        print(f"   • Используйте {XSSColors.WARNING}↑↓{XSSColors.RESET} для навигации по истории команд")
        print(f"   • Введите первые буквы команды и нажмите {XSSColors.WARNING}TAB{XSSColors.RESET}")
    else:
        print(f"\n{XSSColors.WARNING}💡 АВТОДОПОЛНЕНИЕ:{XSSColors.RESET}")
        print(f"   • Для полного автодополнения установите: pip install pyreadline3")
        print(f"   • Используйте 'commands' для просмотра всех доступных команд")

    print(f"\n{XSSColors.INFO}🔥 ПОЛЕЗНЫЕ СОВЕТЫ:{XSSColors.RESET}")
    tips = [
        "Начните с команды 'status' для просмотра профиля",
        "Используйте 'training' для развития навыков",
        "VPN снижает риск обнаружения при атаках",
        "Высокий Heat Level может привести к аресту",
        "Фракции дают бонусы к определенным действиям"
    ]

    for i, tip in enumerate(tips, 1):
        print(f"   {i}. {tip}")

    print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")
    print(f"{XSSColors.BRIGHT_GREEN}💡 Начните свой путь хакера с команды 'status'!{XSSColors.RESET}")


def show_command_detailed_help(command: str) -> None:
    """Показывает подробную справку по конкретной команде"""

    # Детальные описания команд
    detailed_help = {
        "status": {
            "desc": "Показывает полную информацию о вашем хакере",
            "usage": "status",
            "details": [
                "• Никнейм и уровень репутации",
                "• Текущие навыки (cracking, stealth, scanning)",
                "• Финансовое состояние (BTC, USD, криптопортфель)",
                "• Активная миссия и прогресс выполнения",
                "• Уровень Heat (подозрений правоохранительных органов)",
                "• Инвентарь и доступные инструменты",
                "• Фракционная принадлежность и достижения"
            ]
        },
        "missions": {
            "desc": "Открывает центр заданий для хакеров",
            "usage": "missions",
            "details": [
                "• Просмотр всех доступных миссий",
                "• Фильтрация по сложности и размеру награды",
                "• Информация о требованиях к навыкам",
                "• Возможность взять новое задание командой 'take'",
                "• Отслеживание прогресса текущей миссии",
                "• Специальные фракционные задания"
            ]
        },
        "market": {
            "desc": "Теневой рынок хакерских инструментов и программ",
            "usage": "market",
            "details": [
                "• Покупка специализированного ПО и оборудования",
                "• Просмотр товаров по категориям (сканеры, крекеры, прокси)",
                "• Сравнение характеристик и цен товаров",
                "• История покупок и список желаемого",
                "• Специальные предложения и скидки",
                "• Отзывы других покупателей"
            ]
        },
        "training": {
            "desc": "Тренировочный центр для развития хакерских навыков",
            "usage": "training",
            "details": [
                "• Мини-игры для прокачки навыков cracking, stealth, scanning",
                "• Награды в виде BTC и репутации за успешные тренировки",
                "• Детальная статистика и аналитика тренировок",
                "• Персональные рекомендации по развитию",
                "• Различные уровни сложности в зависимости от навыка",
                "• Экспертные бонусы для мастеров (навык 8+)"
            ]
        },
        "crypto": {
            "desc": "Криптовалютная биржа для финансовых операций",
            "usage": "crypto",
            "details": [
                "• Обмен BTC ↔ USD и торговля альткоинами",
                "• Мониторинг курсов в реальном времени",
                "• Графики изменения цен и технический анализ",
                "• Портфельный анализ и отслеживание прибыли",
                "• Настройка ценовых уведомлений и алертов",
                "• Информация о майнинге криптовалют"
            ]
        },
        "forum": {
            "desc": "Подпольный форум хакерского сообщества",
            "usage": "forum",
            "details": [
                "• Общение с другими хакерами и обмен опытом",
                "• Поиск ценной информации и установка контактов",
                "• Чтение постов и участие в обсуждениях",
                "• Отправка частных сообщений",
                "• Получение новостей из мира кибербезопасности",
                "• Поиск партнеров для совместных операций"
            ]
        },
        "network": {
            "desc": "Сетевые инструменты и управление подключениями",
            "usage": "network",
            "details": [
                "• Интерактивная карта доступных узлов сети",
                "• Информация о текущем подключении и маршруте",
                "• Статус VPN, прокси и уровень анонимности",
                "• История подключений и активность",
                "• Мониторинг сетевого трафика",
                "• Управление множественными соединениями"
            ]
        },
        "take": {
            "desc": "Взять миссию из списка доступных заданий",
            "usage": "take <mission_id>",
            "details": [
                "• Укажите точный ID миссии из списка команды 'missions'",
                "• Проверьте соответствие требованиям к навыкам",
                "• Можно иметь только одну активную миссию одновременно",
                "• Некоторые миссии требуют формирования команды",
                "• Сложные миссии могут иметь временные ограничения",
                "• Моральные миссии влияют на ваш этический профиль"
            ],
            "examples": [
                "take web_vuln_scan     # Простое сканирование уязвимостей",
                "take database_breach   # Взлом базы данных",
                "take social_engineering # Социальная инженерия",
                "take team_bank_heist   # Командное ограбление банка"
            ]
        },
        "buy": {
            "desc": "Приобрести предмет или инструмент с теневого рынка",
            "usage": "buy <item_id>",
            "details": [
                "• Укажите точный ID предмета из магазина",
                "• Убедитесь в наличии достаточных средств (BTC/USD)",
                "• Предметы дают постоянные бонусы к навыкам",
                "• Некоторые инструменты требуют минимальный уровень навыков",
                "• Элитные предметы могут быть ограничены по количеству",
                "• Проверьте отзывы перед покупкой дорогих инструментов"
            ],
            "examples": [
                "buy basic_port_scanner    # Базовый сканер портов",
                "buy proxy_network         # Сеть прокси-серверов",
                "buy elite_cracking_suite  # Элитный набор для взлома",
                "buy social_eng_toolkit    # Инструменты социальной инженерии"
            ]
        },
        "nmap": {
            "desc": "Сканирование портов и служб целевой системы",
            "usage": "nmap <target> [scan_type]",
            "details": [
                "• target: IP адрес, доменное имя или адрес .onion",
                "• scan_type: basic (быстро), full (полно), stealth (скрытно), vuln (уязвимости)",
                "• Разные типы сканирования дают различную информацию",
                "• Интенсивное сканирование может повысить Heat Level",
                "• Результаты влияют на успешность последующих атак",
                "• Используйте VPN для снижения риска обнаружения"
            ],
            "examples": [
                "nmap 192.168.1.1          # Базовое сканирование локального роутера",
                "nmap target.com stealth    # Скрытное сканирование сайта",
                "nmap 10.0.0.5 vuln        # Поиск уязвимостей в системе",
                "nmap bank.example.com full # Полное сканирование банка"
            ]
        },
        "vpn": {
            "desc": "Управление VPN подключениями для анонимности",
            "usage": "vpn [команда]",
            "details": [
                "• Без параметров показывает список доступных VPN провайдеров",
                "• vpn_connect <id> - подключиться к выбранному VPN",
                "• vpn_disconnect - отключиться от текущего VPN",
                "• VPN существенно снижает риск обнаружения при атаках",
                "• Разные провайдеры имеют различные уровни защиты",
                "• Платные VPN обеспечивают лучшую анонимность"
            ],
            "examples": [
                "vpn                    # Показать список VPN",
                "vpn_connect 1          # Подключиться к первому VPN",
                "vpn_disconnect         # Отключить VPN",
                "vpn_connect 3          # Подключиться к премиум VPN"
            ]
        },
        "work": {
            "desc": "Продолжить работу над активной миссией",
            "usage": "work",
            "details": [
                "• Продвигает прогресс текущей активной миссии",
                "• Может запускать мини-игры в зависимости от типа миссии",
                "• Некоторые этапы требуют принятия моральных решений",
                "• Командные миссии требуют координации с участниками",
                "• Неудачи могут повысить Heat Level или провалить миссию",
                "• Успех приносит BTC, репутацию и развитие навыков"
            ]
        },
        "faction": {
            "desc": "Информация о вашей текущей фракции",
            "usage": "faction [подкоманда]",
            "details": [
                "• Без параметров показывает информацию о текущей фракции",
                "• faction missions - специальные фракционные задания",
                "• faction status - детальный статус во фракции",
                "• Фракции дают уникальные бонусы и возможности",
                "• White Hats: этичные хакеры, бонусы к репутации",
                "• Black Hats: киберпреступники, бонусы к доходам",
                "• Gray Hats: независимые, сбалансированные бонусы"
            ]
        }
    }

    if command in detailed_help:
        info = detailed_help[command]

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ СПРАВКА: {command.upper()} ━━━━━━━━━━━━━━━━{XSSColors.RESET}")
        print(f"\n{XSSColors.INFO}📋 ОПИСАНИЕ:{XSSColors.RESET}")
        print(f"   {info['desc']}")

        print(f"\n{XSSColors.WARNING}💻 ИСПОЛЬЗОВАНИЕ:{XSSColors.RESET}")
        print(f"   {XSSColors.SUCCESS}{info['usage']}{XSSColors.RESET}")

        if 'details' in info:
            print(f"\n{XSSColors.INFO}📝 ПОДРОБНОСТИ:{XSSColors.RESET}")
            for detail in info['details']:
                print(f"   {detail}")

        if 'examples' in info:
            print(f"\n{XSSColors.SUCCESS}💡 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:{XSSColors.RESET}")
            for example in info['examples']:
                if '#' in example:
                    cmd_part, comment = example.split('#', 1)
                    print(
                        f"   {XSSColors.WARNING}{cmd_part.strip()}{XSSColors.RESET} {XSSColors.DARK_GRAY}# {comment.strip()}{XSSColors.RESET}")
                else:
                    print(f"   {XSSColors.WARNING}{example}{XSSColors.RESET}")

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")
        print(f"{XSSColors.INFO}💡 Используйте 'commands' для списка всех команд{XSSColors.RESET}")

    else:
        print(f"\n{XSSColors.ERROR}❌ Справка по команде '{command}' не найдена{XSSColors.RESET}")
        print(f"{XSSColors.INFO}💡 Используйте 'commands' для списка всех доступных команд{XSSColors.RESET}")
        print(f"{XSSColors.INFO}💡 или 'help' для общей справки{XSSColors.RESET}")


def show_inventory(game_state, market_items: list = None) -> None:
    """Показать подробный инвентарь"""
    inventory = game_state.get_stat('inventory', [])
    
    print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━ ИНВЕНТАРЬ ━━━━━━━━━━━━━━━━━{XSSColors.RESET}")
    
    if not inventory:
        print(f"\n{XSSColors.WARNING}📭 Ваш инвентарь пуст{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Покупайте предметы в магазине для улучшения навыков{XSSColors.RESET}")
        return
    
    print(f"\n{XSSColors.SUCCESS}📦 Ваши предметы ({len(inventory)}):{XSSColors.RESET}\n")
    
    # Группируем по категориям если есть информация о предметах
    if market_items:
        categories = {}
        for item_id in inventory:
            item_data = next((item for item in market_items if item["id"] == item_id), None)
            if item_data:
                category = item_data.get("type", "other")
                if category not in categories:
                    categories[category] = []
                categories[category].append(item_data)
        
        # Показываем по категориям
        for category, items in categories.items():
            cat_info = ITEM_CATEGORIES.get(category, {"name": "Прочее", "icon": "📦"})
            print(f"{cat_info['icon']} {cat_info['name'].upper()}:")
            
            for item in items:
                print(f"   • {item['name']}")
                if 'desc' in item:
                    print(f"     {XSSColors.INFO}{item['desc']}{XSSColors.RESET}")
                
                # Показываем бонусы
                if 'bonus' in item:
                    bonus_str = []
                    for bonus, value in item['bonus'].items():
                        if bonus == "all_skills":
                            bonus_str.append(f"Все навыки +{value}")
                        elif bonus in ["scanning", "cracking", "stealth", "social_eng"]:
                            bonus_str.append(f"{bonus.title()} +{value}")
                    
                    if bonus_str:
                        print(f"     {XSSColors.SKILL}Бонусы: {', '.join(bonus_str)}{XSSColors.RESET}")
                print()
    else:
        # Простой список если нет данных о предметах
        for i, item_id in enumerate(inventory, 1):
            print(f"   {i}. {item_id}")
    
    print(f"{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")


def show_mission_progress(game_state) -> None:
    """Показать прогресс текущей миссии"""
    active_mission = game_state.get_stat("active_mission")
    
    if not active_mission:
        print(f"{XSSColors.WARNING}У вас нет активной миссии{XSSColors.RESET}")
        return
    
    progress = game_state.get_stat("mission_progress", 0)
    # Здесь нужно будет получить данные миссии из системы миссий
    duration = 5  # Временно
    
    print(f"\n{XSSColors.INFO}📋 ТЕКУЩАЯ МИССИЯ:{XSSColors.RESET}")
    print(f"   {XSSColors.WARNING}{active_mission}{XSSColors.RESET}")
    
    bar = progress_bar(progress, duration, length=30)
    percentage = int((progress / duration) * 100) if duration > 0 else 0
    
    print(f"   {bar} {progress}/{duration} ({percentage}%)")
    
    if progress < duration:
        print(f"\n{XSSColors.INFO}💡 Используйте 'work' для продолжения{XSSColors.RESET}")
    else:
        print(f"\n{XSSColors.SUCCESS}✅ Миссия готова к завершению!{XSSColors.RESET}")


def show_faction_info(faction_data: Dict[str, Any]) -> None:
    """Показать информацию о фракции"""
    if not faction_data:
        print(f"{XSSColors.WARNING}Вы не состоите ни в одной фракции{XSSColors.RESET}")
        return
    
    print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━ ВАША ФРАКЦИЯ ━━━━━━━━━━━━━━{XSSColors.RESET}")
    
    # Определяем цвет фракции
    faction_id = faction_data.get("id", "")
    if faction_id == "whitehats":
        color = XSSColors.SUCCESS
        icon = "🛡️"
    elif faction_id == "blackhats":
        color = XSSColors.DANGER
        icon = "💀"
    else:
        color = XSSColors.WARNING
        icon = "🎭"
    
    print(f"\n{icon} {color}{faction_data.get('name', 'Неизвестная фракция')}{XSSColors.RESET}")
    print(f"\n{XSSColors.INFO}{faction_data.get('desc', 'Нет описания')}{XSSColors.RESET}")
    
    # Бонусы фракции
    bonuses = faction_data.get("bonuses", {})
    if bonuses:
        print(f"\n{XSSColors.SUCCESS}🎁 БОНУСЫ ФРАКЦИИ:{XSSColors.RESET}")
        for bonus, value in bonuses.items():
            if bonus == "reputation":
                print(f"   📈 Репутация x{value} при выполнении миссий")
            elif bonus == "heat_reduction":
                print(f"   ❄️ Снижение Heat Level x{value}")
            elif bonus == "btc_multiplier":
                print(f"   💰 Награды BTC x{value}")
            elif bonus == "skill_boost":
                print(f"   ✨ Все навыки +{value}")
    
    print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")


def show_notification(message: str, notification_type: str = "info") -> None:
    """Показать уведомление"""
    type_XSSColors = {
        "info": XSSColors.INFO,
        "success": XSSColors.SUCCESS,
        "warning": XSSColors.WARNING,
        "error": XSSColors.ERROR,
        "danger": XSSColors.DANGER
    }
    
    type_icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "danger": "🚨"
    }
    
    color = type_XSSColors.get(notification_type, XSSColors.INFO)
    icon = type_icons.get(notification_type, "•")
    
    print(f"\n{color}{icon} {message}{XSSColors.RESET}")


def format_time_ago(seconds: int) -> str:
    """Форматирует время 'назад'"""
    if seconds < 60:
        return f"{seconds}с назад"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}м назад"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours}ч назад"
    else:
        days = seconds // 86400
        return f"{days}д назад"


def create_table(headers: list, rows: list, max_width: int = 80) -> str:
    """Создает таблицу в ASCII формате"""
    if not headers or not rows:
        return ""
    
    # Вычисляем ширину колонок
    col_widths = []
    for i, header in enumerate(headers):
        max_width_col = len(str(header))
        for row in rows:
            if i < len(row):
                max_width_col = max(max_width_col, len(str(row[i])))
        col_widths.append(min(max_width_col, max_width // len(headers)))
    
    # Создаем разделитель
    separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
    
    # Создаем таблицу
    table = [separator]
    
    # Заголовки
    header_row = "|"
    for i, header in enumerate(headers):
        header_row += f" {str(header):<{col_widths[i]}} |"
    table.append(header_row)
    table.append(separator)
    
    # Строки данных
    for row in rows:
        data_row = "|"
        for i, cell in enumerate(row):
            if i < len(col_widths):
                data_row += f" {str(cell):<{col_widths[i]}} |"
        table.append(data_row)
    
    table.append(separator)
    
    return "\n".join(table)