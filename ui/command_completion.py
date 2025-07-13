"""
Система автодополнения команд для XSS Game 0.3.0
Совместимая версия для Windows и других ОС
"""

from typing import List, Optional, Tuple

from ui.colors import XSSColors as Colors

# Попытка импорта readline с fallback для Windows
HAS_READLINE = True
readline = None  # Инициализируем переменную

try:
    import readline

    print(f"{Colors.SUCCESS}✅ Модуль readline доступен{Colors.RESET}")
except ImportError:
    HAS_READLINE = False
    readline = None  # Явно устанавливаем None
    print(f"{Colors.WARNING}⚠️ Модуль readline недоступен. Автодополнение ограничено.{Colors.RESET}")

    # Для Windows можем попробовать pyreadline
    try:
        import pyreadline as readline

        HAS_READLINE = True
        print(f"{Colors.SUCCESS}✅ Найден pyreadline - автодополнение доступно{Colors.RESET}")
    except ImportError:
        readline = None  # ДОБАВЛЕНО: определяем readline в except блоке
        print(f"{Colors.INFO}💡 Для полного автодополнения установите: pip install pyreadline3{Colors.RESET}")


class CommandCompleter:
    """Класс для автодополнения команд с поддержкой разных ОС"""
    
    def __init__(self):
        self.base_commands = {
            # === ОСНОВНЫЕ КОМАНДЫ ===
            "status": "Показать профиль и статистику",
            "forum": "Просмотр форума",
            "missions": "Доступные задания",
            "market": "Теневой рынок",
            "contacts": "Список контактов",
            "crypto": "Криптовалютная биржа",
            "training": "Тренировочный центр",
            "train": "Тренировочный центр (алиас)",
            "faction": "Информация о фракции",
            "chat": "Глобальный чат",

            # === ДЕЙСТВИЯ С МИССИЯМИ ===
            "take": "Взять миссию [ID]",
            "work": "Выполнить активную миссию",
            "abort_mission": "Прервать текущую миссию",
            "mission_status": "Подробный статус миссии",
            "team_status": "Статус команды",
            "recruit": "Набрать команду для миссии",
            "recruit_team": "Набрать команду (алиас)",

            # === ПОКУПКИ И ТОРГОВЛЯ ===
            "buy": "Купить предмет [ID]",
            "sell": "Продать криптовалюту",
            "info": "Информация о предмете [ID]",
            "item_info": "Информация о предмете (алиас)",

            # === КОММУНИКАЦИИ ===
            "pm": "Личное сообщение [контакт]",
            "private_message": "Личное сообщение (алиас)",
            "message": "Отправить сообщение",

            # === ФРАКЦИИ ===
            "join_faction": "Присоединиться к фракции",
            "change_faction": "Сменить фракцию",
            "faction_status": "Статус во фракции",
            "defect": "Покинуть фракцию",

            # === ВАЛЮТЫ И ФИНАНСЫ ===
            "exchange_btc_usd": "Обменять BTC на USD",
            "exchange_usd_btc": "Обменять USD на BTC",
            "portfolio": "Криптопортфель",
            "invest": "Инвестировать в криптовалюту",
            "convert": "Конвертер валют",

            # === СЕТЕВЫЕ КОМАНДЫ ===
            "network": "Показать карту сети",
            "connect": "Подключиться к узлу [адрес]",
            "disconnect": "Отключиться от узла",
            "scan": "Сканировать сеть",
            "traceroute": "Трассировка маршрута [адрес]",

            # === ИНСТРУМЕНТЫ ХАКИНГА ===
            "nmap": "Сканирование портов [цель] [тип]",
            "wireshark": "Перехват трафика [интерфейс] [время]",
            "metasploit": "Запуск эксплойта [цель] [эксплойт]",

            # === VPN И АНОНИМНОСТЬ ===
            "vpn": "Управление VPN",
            "vpn_connect": "Подключиться к VPN [номер]",
            "vpn_disconnect": "Отключиться от VPN",

            # === БОТНЕТЫ И DDOS ===
            "botnet": "Управление ботнетами",
            "buy_botnet": "Купить ботнет [номер]",
            "ddos": "Запустить DDoS атаку [цель]",

            # === ПРОДВИНУТЫЕ МИССИИ ===
            "mission_stats": "Статистика миссий",
            "mission_statistics": "Детальная статистика миссий",
            "notifications": "Показать уведомления",
            "show_notifications": "Показать уведомления (алиас)",
            "clear_notifications": "Очистить уведомления",
            "mission_history": "История миссий",
            "team_details": "Детали команды",
            "moral_profile": "Моральный профиль",
            "mission_choices": "История моральных выборов",
            "show_mission_choices": "Показать моральные выборы",

            # === ПОИСК И ИНФОРМАЦИЯ ===
            "search": "Поиск по игре",
            "tips": "Советы новичкам",
            "about": "О игре",
            "commands": "Список всех команд",

            # === НАСТРОЙКИ ===
            "settings": "Настройки игры",
            "audio": "Настройки звука",
            "music": "Переключить музыку",
            "sound": "Переключить звуки",
            "theme": "Сменить тему оформления",

            # === СИСТЕМА ===
            "save": "Сохранить игру",
            "load": "Загрузить игру",
            "help": "Показать справку",
            "exit": "Выйти из игры",
            "quit": "Выйти из игры",
            "debug": "Режим отладки",
            "reset": "Сброс персонажа",

            # === ТЕСТОВЫЕ И ОТЛАДОЧНЫЕ ===
            "test_event": "Тестировать событие (отладка)",
            "simulate_mission": "Симулировать миссию (отладка)",

            # === АЛИАСЫ И СОКРАЩЕНИЯ ===
            "ls": "Статус (алиас)",
            "dir": "Статус (алиас)",
            "cat": "Информация (алиас)",
            "cd": "Контекст (алиас)",
            "pwd": "Текущий контекст",
            "clear": "Очистить экран",
            "cls": "Очистить экран",
            "man": "Справка (алиас)",
            "sudo": "Режим администратора",
            "ssh": "Подключиться (алиас)",
            "ping": "Сканировать (алиас)",
            "nc": "Подключиться (алиас)",
            "wget": "Скачать",
            "curl": "API запрос"
        }

        # Контекстные команды для разных разделов
        self.context_commands = {
            "market": {
                "browse": "Просмотр товаров по категориям",
                "search": "Поиск товаров по названию или функции",
                "wishlist": "Список желаемых предметов",
                "history": "История покупок и продаж",
                "compare": "Сравнение характеристик товаров",
                "reviews": "Отзывы покупателей о товарах",
                "categories": "Показать все категории",
                "special": "Специальные предложения",
                "filter": "Фильтровать товары",
                "sort": "Сортировать по цене/рейтингу"
            },
            "crypto": {
                "rates": "Текущие курсы всех криптовалют",
                "chart": "График изменения цен",
                "convert": "Конвертер между валютами",
                "analyze": "Анализ трендов рынка",
                "alerts": "Настройка ценовых уведомлений",
                "mining": "Информация о майнинге криптовалют",
                "portfolio": "Анализ портфеля",
                "buy": "Купить криптовалюту",
                "sell": "Продать криптовалюту",
                "history": "История операций"
            },
            "forum": {
                "read": "Читать пост по ID",
                "reply": "Ответить на выбранный пост",
                "create": "Создать новую тему",
                "subscribe": "Подписаться на обновления темы",
                "report": "Пожаловаться на нарушение",
                "bookmark": "Добавить в личные закладки",
                "search": "Поиск по форуму",
                "latest": "Последние посты",
                "hot": "Популярные темы",
                "private": "Личные сообщения"
            },
            "missions": {
                "filter": "Фильтрация миссий по критериям",
                "difficulty": "Сортировка по уровню сложности",
                "rewards": "Сортировка по размеру награды",
                "progress": "Прогресс текущей миссии",
                "abort": "Отменить активную миссию",
                "history": "История выполненных заданий",
                "status": "Подробный статус активной миссии",
                "team": "Управление командой для миссии",
                "choices": "Просмотр сделанных моральных выборов",
                "recruit": "Набор участников в команду",
                "events": "Просмотр активных событий миссии",
                "available": "Показать доступные миссии",
                "completed": "Показать завершенные миссии",
                "faction": "Фракционные миссии"
            },
            "faction": {
                "reputation": "Репутация во всех фракциях",
                "missions": "Специальные фракционные задания",
                "wars": "Текущие конфликты между фракциями",
                "defect": "Смена фракции (с последствиями)",
                "loyalty": "Проверка уровня лояльности",
                "status": "Детальный статус во фракции",
                "info": "Информация о фракции",
                "bonuses": "Фракционные бонусы",
                "members": "Участники фракции"
            },
            "network": {
                "map": "Показать карту сети",
                "status": "Статус подключения",
                "history": "История подключений",
                "scan": "Сканировать доступные узлы",
                "trace": "Трассировка маршрута",
                "tools": "Сетевые инструменты",
                "vpn": "Управление VPN",
                "proxy": "Настройки прокси",
                "logs": "Журнал сетевой активности"
            },
            "training": {
                "stats": "Статистика тренировок",
                "recommendations": "Рекомендации по развитию",
                "help": "Справка по мини-играм",
                "history": "История тренировок",
                "skills": "Анализ навыков",
                "difficulty": "Настройка сложности",
                "rewards": "Информация о наградах"
            }
        }

        # Добавляем новый контекст для миссий
        self.context_commands["missions"].update({
            "status": "Подробный статус миссии",
            "abort": "Прервать текущую миссию",
            "team": "Управление командой",
            "choices": "Просмотр моральных выборов",
            "recruit": "Набор команды",
            "events": "Активные события миссии"
        })
        
        # История команд
        self.command_history = []
        self.history_index = -1
        
        # Текущий контекст
        self.current_context = None
        
        # Инициализируем readline если доступен
        if HAS_READLINE:
            self._setup_readline()
        else:
            self._setup_fallback()
    
    def _setup_readline(self) -> None:
        """Настройка модуля readline для автодополнения"""
        try:
            # Настраиваем автодополнение
            readline.set_completer(self.complete)
            readline.parse_and_bind("tab: complete")
            
            # Настраиваем историю команд
            readline.parse_and_bind("\\e[A: previous-history")  # Стрелка вверх
            readline.parse_and_bind("\\e[B: next-history")     # Стрелка вниз
            
            # Настраиваем разделители
            readline.set_completer_delims(" \t\n`!@#$%^&*()=+[{]}\\|;:'\",<>?")
            
            print(f"{Colors.SUCCESS}✅ Автодополнение команд активировано (TAB){Colors.RESET}")
            print(f"{Colors.INFO}💡 Используйте стрелки ↑↓ для навигации по истории команд{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.WARNING}⚠️ Ошибка настройки автодополнения: {e}{Colors.RESET}")
            self._setup_fallback()
    
    def _setup_fallback(self) -> None:
        """Настройка fallback режима без readline"""
        print(f"{Colors.INFO}📝 Базовый режим ввода команд{Colors.RESET}")
        print(f"{Colors.INFO}💡 Используйте 'commands' для списка доступных команд{Colors.RESET}")
    
    def complete(self, text: str, state: int) -> Optional[str]:
        """Основная функция автодополнения (только если readline доступен)"""
        if not HAS_READLINE:
            return None
            
        if state == 0:
            # Первый вызов - генерируем список совпадений
            try:
                line = readline.get_line_buffer()
                self.matches = self._get_matches(text, line)
            except:
                self.matches = []
        
        try:
            return self.matches[state]
        except IndexError:
            return None



    def _get_matches(self, text: str, line: str) -> List[str]:
        """Получает список совпадений для автодополнения"""
        # Разбираем строку на части
        parts = line.split()
        
        if not parts or (len(parts) == 1 and not line.endswith(' ')):
            # Дополняем команду
            return self._complete_command(text)
        else:
            # Дополняем аргументы команды
            command = parts[0]
            return self._complete_arguments(command, text, parts[1:])

    def _complete_network_addresses(self, text: str) -> List[str]:
        """Дополняет сетевые адреса"""
        sample_addresses = [
            "localhost", "127.0.0.1", "192.168.1.1", "10.0.0.1",
            "target.com", "bank.example.com", "secure.gov",
            "darkweb.onion", "anonymous.onion", "market.onion"
        ]
        return [addr for addr in sample_addresses if addr.startswith(text)]

    def _complete_command(self, text: str) -> List[str]:
        """Дополняет основные команды"""
        matches = []
        
        # Основные команды
        for cmd in self.base_commands.keys():
            if cmd.startswith(text.lower()):
                matches.append(cmd)
        
        # Контекстные команды
        if self.current_context and self.current_context in self.context_commands:
            for cmd in self.context_commands[self.current_context].keys():
                if cmd.startswith(text.lower()):
                    matches.append(cmd)
        
        return sorted(matches)

    def _complete_arguments(self, command: str, text: str, args: List[str]) -> List[str]:
        """Дополняет аргументы команд с расширенным набором"""
        matches = []

        # === МИССИИ ===
        if command in ["take", "mission_info", "abort"]:
            matches = self._complete_mission_ids(text)

        # === ПРЕДМЕТЫ И ПОКУПКИ ===
        elif command in ["buy", "info", "item_info", "sell_item"]:
            matches = self._complete_item_ids(text)

        # === КОНТАКТЫ И СООБЩЕНИЯ ===
        elif command in ["pm", "message", "private_message", "contact"]:
            matches = self._complete_contact_names(text)

        # === ФРАКЦИИ ===
        elif command in ["join_faction", "change_faction", "defect_to"]:
            matches = self._complete_faction_names(text)

        # === СЕТЕВЫЕ КОМАНДЫ ===
        elif command in ["connect", "ssh", "traceroute", "ping"]:
            matches = self._complete_network_addresses(text)

        elif command in ["nmap"]:
            if len(args) == 0:
                matches = self._complete_network_addresses(text)
            elif len(args) == 1:
                matches = ["basic", "full", "stealth", "vuln"]

        elif command in ["wireshark"]:
            if len(args) == 0:
                matches = ["eth0", "wlan0", "lo", "any"]
            elif len(args) == 1:
                matches = ["10", "30", "60", "120"]

        elif command in ["metasploit"]:
            if len(args) == 0:
                matches = self._complete_network_addresses(text)
            elif len(args) == 1:
                matches = ["buffer_overflow", "sql_injection", "weak_password", "rce", "privilege_escalation"]

        # === VPN КОМАНДЫ ===
        elif command in ["vpn_connect"]:
            matches = ["1", "2", "3", "4", "5"]  # Номера VPN провайдеров

        elif command in ["buy_botnet"]:
            matches = ["1", "2", "3", "4"]  # Номера ботнетов

        elif command in ["ddos"]:
            if len(args) == 0:
                matches = self._complete_network_addresses(text)
            elif len(args) == 1:
                matches = ["1", "2", "3", "4"]  # Номера ботнетов

        # === ФОРУМ ===
        elif command in ["forum"]:
            if len(args) == 0:
                matches = ["public", "private", "read", "create", "search"]
            elif len(args) == 1 and args[0] in ["public", "private"]:
                matches = self._complete_post_ids(text, args[0])

        # === КРИПТОВАЛЮТЫ ===
        elif command in ["crypto", "convert"]:
            matches = ["buy", "sell", "convert", "portfolio", "rates", "analyze"]

        elif command in ["exchange_btc_usd", "exchange_usd_btc"]:
            if len(args) == 0:
                matches = ["10", "50", "100", "500", "1000", "all"]

        # === РЫНОК ===
        elif command in ["market"]:
            matches = ["browse", "search", "category", "wishlist", "compare", "special"]

        # === ПОИСК ===
        elif command in ["search"]:
            matches = ["missions", "items", "contacts", "posts", "help", "commands"]

        # === НАСТРОЙКИ ===
        elif command in ["theme"]:
            matches = self._complete_themes(text)

        elif command in ["settings"]:
            matches = ["audio", "display", "gameplay", "interface", "reset"]

        elif command in ["audio"]:
            matches = ["on", "off", "music", "sounds", "volume"]

        # === ТРЕНИРОВКИ ===
        elif command in ["training", "train"]:
            matches = ["stats", "recommendations", "help"]

        # === ПРОДВИНУТЫЕ МИССИИ ===
        elif command in ["abort_mission"]:
            matches = ["confirm", "cancel"]

        elif command in ["recruit", "recruit_team"]:
            if len(args) == 0:
                matches = ["hacker", "social_engineer", "lookout", "specialist", "all"]

        elif command in ["mission_status"]:
            matches = ["full", "brief", "team", "events", "timer"]

        elif command in ["faction"]:
            matches = ["missions", "status", "info", "reputation", "wars"]

        # === ПОМОЩЬ ===
        elif command in ["help", "man"]:
            # Автодополнение для help <команда>
            all_commands = list(self.base_commands.keys())
            matches = [cmd for cmd in all_commands if cmd.startswith(text.lower())]

        return [match for match in matches if match.startswith(text.lower())]
    
    def _complete_mission_ids(self, text: str) -> List[str]:
        """Дополняет ID миссий"""
        # В реальной игре здесь будет обращение к системе миссий
        sample_missions = [
            "port_scan", "info_gather", "web_vuln", "phishing_simple",
            "database_breach", "crypto_theft", "gov_hack", "zero_day"
        ]
        return [mid for mid in sample_missions if mid.startswith(text)]
    
    def _complete_item_ids(self, text: str) -> List[str]:
        """Дополняет ID предметов"""
        # В реальной игре здесь будет обращение к системе магазина
        sample_items = [
            "basic_port_scanner", "proxy_network", "phishing_kit",
            "pro_vuln_scanner", "gpu_cracker", "keylogger",
            "elite_proxy", "zero_day_info", "ai_cracker"
        ]
        return [iid for iid in sample_items if iid.startswith(text)]
    
    def _complete_contact_names(self, text: str) -> List[str]:
        """Дополняет имена контактов"""
        # В реальной игре здесь будет обращение к системе контактов
        sample_contacts = ["shadow", "nexus", "ghost", "admin", "broker"]
        return [contact for contact in sample_contacts if contact.startswith(text)]
    
    def _complete_faction_names(self, text: str) -> List[str]:
        """Дополняет названия фракций"""
        factions = ["whitehats", "blackhats", "grayhats"]
        return [faction for faction in factions if faction.startswith(text)]
    
    def _complete_post_ids(self, text: str, section: str) -> List[str]:
        """Дополняет ID постов форума"""
        # В реальной игре здесь будет обращение к системе форума
        if section == "public":
            return [str(i) for i in range(1, 11) if str(i).startswith(text)]
        else:  # private
            return [str(i) for i in range(1, 6) if str(i).startswith(text)]
    
    def _complete_themes(self, text: str) -> List[str]:
        """Дополняет названия тем оформления"""
        themes = ["classic_green", "matrix_green", "neon_cyber", "ice_blue", "custom"]
        return [theme for theme in themes if theme.startswith(text)]
    
    def add_to_history(self, command: str) -> None:
        """Добавляет команду в историю"""
        if command and (not self.command_history or command != self.command_history[-1]):
            self.command_history.append(command)
            
            # Ограничиваем размер истории
            if len(self.command_history) > 100:
                self.command_history = self.command_history[-100:]
            
            # Добавляем в readline history если доступен
            if HAS_READLINE:
                try:
                    readline.add_history(command)
                except:
                    pass
    
    def set_context(self, context: str) -> None:
        """Устанавливает текущий контекст для автодополнения"""
        self.current_context = context
        
        if context and context in self.context_commands:
            context_cmds = self.context_commands[context]
            print(f"\n{Colors.INFO}📝 Доступные команды в {context}:{Colors.RESET}")
            for cmd, desc in list(context_cmds.items())[:5]:  # Показываем первые 5
                print(f"   {Colors.WARNING}{cmd}{Colors.RESET} - {desc}")
            if len(context_cmds) > 5:
                print(f"   {Colors.INFO}... и еще {len(context_cmds) - 5} команд{Colors.RESET}")
                if HAS_READLINE:
                    print(f"   {Colors.INFO}(используйте TAB для автодополнения){Colors.RESET}")
    
    def clear_context(self) -> None:
        """Очищает текущий контекст"""
        self.current_context = None
    
    def get_command_help(self, command: str) -> str:
        """Получает справку по команде"""
        # Проверяем основные команды
        if command in self.base_commands:
            return self.base_commands[command]
        
        # Проверяем контекстные команды
        for context_cmds in self.context_commands.values():
            if command in context_cmds:
                return context_cmds[command]
        
        return "Неизвестная команда"

    def show_all_commands(self) -> None:
        """Показывает все доступные команды с полными описаниями"""
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━ СПРАВОЧНИК КОМАНД ━━━━━━━━━━━━━━━━{Colors.RESET}")

        # Группируем команды по категориям
        categories = {
            "Основные": ["status", "forum", "missions", "market", "contacts", "crypto", "training"],
            "Действия": ["take", "work", "buy", "sell", "pm", "info", "search"],
            "Фракции": ["faction", "join_faction", "change_faction", "faction_status"],
            "Валюты": ["exchange_btc_usd", "exchange_usd_btc", "portfolio", "invest"],
            "Система": ["save", "load", "settings", "audio", "music", "sound", "theme"],
            "Справка": ["help", "commands", "tips", "about"],
            "Выход": ["exit", "quit"]
        }

        for category, commands in categories.items():
            print(f"\n{Colors.WARNING}📁 {category}:{Colors.RESET}")
            for cmd in commands:
                if cmd in self.base_commands:
                    desc = self.base_commands[cmd]
                    print(f"   {Colors.SUCCESS}{cmd:<20}{Colors.RESET} {desc}")

        # Показываем контекстные команды - ПОЛНОСТЬЮ
        print(f"\n{Colors.INFO}🎯 КОНТЕКСТНЫЕ КОМАНДЫ (доступны в соответствующих разделах):{Colors.RESET}")

        # Детальное описание для каждого контекста
        context_details = {
            "market": {
                "title": "Теневой рынок",
                "commands": {
                    "browse": "Просмотр товаров по категориям",
                    "search": "Поиск товаров по названию или функции",
                    "wishlist": "Список желаемых предметов",
                    "history": "История покупок и продаж",
                    "compare": "Сравнение характеристик товаров",
                    "reviews": "Отзывы покупателей о товарах"
                }
            },
            "crypto": {
                "title": "Криптовалютная биржа",
                "commands": {
                    "rates": "Текущие курсы всех криптовалют",
                    "chart": "График изменения цен",
                    "convert": "Конвертер между валютами",
                    "analyze": "Анализ трендов рынка",
                    "alerts": "Настройка ценовых уведомлений",
                    "mining": "Информация о майнинге криптовалют"
                }
            },
            "forum": {
                "title": "Хакерский форум",
                "commands": {
                    "read": "Читать пост по ID",
                    "reply": "Ответить на выбранный пост",
                    "create": "Создать новую тему",
                    "subscribe": "Подписаться на обновления темы",
                    "report": "Пожаловаться на нарушение",
                    "bookmark": "Добавить в личные закладки"
                }
            },
            "missions": {
                "title": "Система заданий",
                "commands": {
                    "filter": "Фильтрация миссий по критериям",
                    "difficulty": "Сортировка по уровню сложности",
                    "rewards": "Сортировка по размеру награды",
                    "progress": "Прогресс текущей миссии",
                    "abort": "Отменить активную миссию",
                    "history": "История выполненных заданий",
                    "status": "Подробный статус активной миссии",
                    "team": "Управление командой для миссии",
                    "choices": "Просмотр сделанных моральных выборов",
                    "recruit": "Набор участников в команду",
                    "events": "Просмотр активных событий миссии"
                }
            },
            "faction": {
                "title": "Фракционная система",
                "commands": {
                    "reputation": "Репутация во всех фракциях",
                    "missions": "Специальные фракционные задания",
                    "wars": "Текущие конфликты между фракциями",
                    "defect": "Смена фракции (с последствиями)",
                    "loyalty": "Проверка уровня лояльности"
                }
            }
        }

        for context, details in context_details.items():
            title = details["title"]
            commands = details["commands"]

            print(f"\n   {Colors.WARNING}🔹 В разделе '{context}' ({title}):{Colors.RESET}")

            for cmd, desc in commands.items():
                print(f"      {Colors.INFO}{cmd:<15}{Colors.RESET} {desc}")

        # Дополнительная информация
        print(f"\n{Colors.SUCCESS}🌟 ПРОДВИНУТЫЕ КОМАНДЫ:{Colors.RESET}")
        advanced_commands = {
            "mission_stats": "Подробная статистика выполнения миссий",
            "notifications": "Просмотр активных уведомлений",
            "mission_history": "Полная история всех миссий",
            "team_details": "Детальная информация о текущей команде",
            "moral_profile": "Анализ вашего морального профиля",
            "abort_mission": "Прервать текущую миссию с штрафами",
            "recruit_team": "Набрать команду для командной миссии"
        }

        for cmd, desc in advanced_commands.items():
            print(f"   {Colors.SUCCESS}{cmd:<20}{Colors.RESET} {desc}")

        # Сетевые команды
        print(f"\n{Colors.WARNING}🌐 СЕТЕВЫЕ КОМАНДЫ:{Colors.RESET}")
        network_commands = {
            "network": "Показать карту сети и подключения",
            "connect": "Подключиться к удаленному узлу [адрес]",
            "disconnect": "Отключиться от текущего узла",
            "scan": "Сканировать текущую сеть на уязвимости",
            "traceroute": "Трассировка маршрута до цели [адрес]",
            "nmap": "Продвинутое сканирование портов [цель] [тип]",
            "wireshark": "Перехват сетевого трафика [интерфейс] [время]",
            "metasploit": "Запуск эксплойта [цель] [эксплойт]",
            "vpn": "Управление VPN подключениями",
            "vpn_connect": "Подключиться к VPN [номер провайдера]",
            "vpn_disconnect": "Отключиться от текущего VPN",
            "botnet": "Управление ботнетами для DDoS",
            "buy_botnet": "Приобрести ботнет [номер]",
            "ddos": "Запустить DDoS атаку [цель] [ботнет]"
        }

        for cmd, desc in network_commands.items():
            print(f"   {Colors.WARNING}{cmd:<20}{Colors.RESET} {desc}")

        # Советы по использованию
        print(f"\n{Colors.INFO}💡 СОВЕТЫ ПО ИСПОЛЬЗОВАНИЮ:{Colors.RESET}")
        print(f"   • Многие команды имеют сокращения (например: 's' вместо 'status')")
        print(f"   • Контекстные команды работают только в соответствующих разделах")
        print(f"   • Используйте 'команда help' для справки по конкретной команде")
        print(f"   • Некоторые команды требуют дополнительные параметры")
        print(f"   • Продвинутые команды становятся доступны по мере прогресса")

        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

        if HAS_READLINE:
            print(f"{Colors.INFO}💡 Используйте TAB для автодополнения команд и аргументов{Colors.RESET}")
            print(f"{Colors.INFO}💡 Используйте ↑↓ для навигации по истории команд{Colors.RESET}")
        else:
            print(f"{Colors.INFO}💡 Для полного автодополнения установите: pip install pyreadline3{Colors.RESET}")

        print(f"{Colors.INFO}💡 Введите 'help [команда]' для подробной справки по команде{Colors.RESET}")
    
    def smart_suggestions(self, failed_command: str) -> List[str]:
        """Умные предложения для неизвестных команд"""
        suggestions = []
        
        # Поиск похожих команд по расстоянию Левенштейна
        def levenshtein_distance(s1: str, s2: str) -> int:
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)
            
            if len(s2) == 0:
                return len(s1)
            
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            
            return previous_row[-1]
        
        # Ищем похожие команды
        all_commands = list(self.base_commands.keys())
        for context_cmds in self.context_commands.values():
            all_commands.extend(context_cmds.keys())
        
        for cmd in all_commands:
            distance = levenshtein_distance(failed_command.lower(), cmd.lower())
            if distance <= 2:  # Максимум 2 отличия
                suggestions.append((cmd, distance))
        
        # Сортируем по релевантности
        suggestions.sort(key=lambda x: x[1])
        return [cmd for cmd, _ in suggestions[:5]]

    def show_command_help(self, command: str) -> None:
        """Показывает подробную справку по конкретной команде"""

        # Детальные описания команд
        detailed_help = {
            "status": {
                "desc": "Показывает полную информацию о вашем хакере",
                "usage": "status",
                "details": [
                    "• Никнейм и уровень репутации",
                    "• Текущие навыки (cracking, stealth, scanning)",
                    "• Финансовое состояние (BTC, USD)",
                    "• Активная миссия и прогресс",
                    "• Уровень Heat (подозрений правоохранительных органов)",
                    "• Инвентарь и доступные инструменты"
                ]
            },
            "missions": {
                "desc": "Открывает центр заданий для хакеров",
                "usage": "missions",
                "details": [
                    "• Просмотр доступных миссий",
                    "• Фильтрация по сложности и награде",
                    "• Информация о требованиях к навыкам",
                    "• Возможность взять новое задание",
                    "• Прогресс текущей миссии"
                ]
            },
            "market": {
                "desc": "Теневой рынок хакерских инструментов",
                "usage": "market",
                "details": [
                    "• Покупка специализированного ПО",
                    "• Просмотр по категориям (сканеры, крекеры, прокси)",
                    "• Сравнение характеристик товаров",
                    "• История покупок",
                    "• Специальные предложения"
                ]
            },
            "crypto": {
                "desc": "Криптовалютная биржа для отмывания денег",
                "usage": "crypto",
                "details": [
                    "• Обмен BTC ↔ USD и другие валюты",
                    "• Мониторинг курсов в реальном времени",
                    "• Графики изменения цен",
                    "• Анализ трендов рынка",
                    "• Настройка ценовых уведомлений"
                ]
            },
            "training": {
                "desc": "Тренировочный центр для развития навыков",
                "usage": "training",
                "details": [
                    "• Мини-игры для прокачки навыков",
                    "• Награды в виде BTC и репутации",
                    "• Статистика тренировок",
                    "• Персональные рекомендации",
                    "• Различные уровни сложности"
                ]
            },
            "forum": {
                "desc": "Подпольный форум хакерского сообщества",
                "usage": "forum",
                "details": [
                    "• Общение с другими хакерами",
                    "• Поиск информации и контактов",
                    "• Обмен опытом и советами",
                    "• Частные сообщения",
                    "• Новости из мира кибербезопасности"
                ]
            },
            "network": {
                "desc": "Сетевые инструменты и карта подключений",
                "usage": "network",
                "details": [
                    "• Карта доступных узлов сети",
                    "• Информация о текущем подключении",
                    "• Статус VPN и прокси",
                    "• Уровень анонимности",
                    "• История подключений"
                ]
            },
            "take": {
                "desc": "Взять миссию по ID",
                "usage": "take <mission_id>",
                "details": [
                    "• Укажите ID миссии из списка",
                    "• Проверьте требования к навыкам",
                    "• Только одна активная миссия одновременно",
                    "• Некоторые миссии требуют команду"
                ],
                "examples": [
                    "take web_vuln_scan",
                    "take database_breach",
                    "take social_engineering"
                ]
            },
            "buy": {
                "desc": "Купить предмет с рынка",
                "usage": "buy <item_id>",
                "details": [
                    "• Укажите ID предмета из магазина",
                    "• Проверьте наличие средств",
                    "• Предметы улучшают эффективность",
                    "• Некоторые требуют определенный уровень навыков"
                ],
                "examples": [
                    "buy basic_port_scanner",
                    "buy proxy_network",
                    "buy elite_cracking_suite"
                ]
            },
            "nmap": {
                "desc": "Сканирование портов и служб",
                "usage": "nmap <target> [scan_type]",
                "details": [
                    "• target: IP адрес или домен",
                    "• scan_type: basic, full, stealth, vuln",
                    "• Разные типы дают разную информацию",
                    "• Может повысить Heat Level"
                ],
                "examples": [
                    "nmap 192.168.1.1",
                    "nmap target.com stealth",
                    "nmap 10.0.0.5 vuln"
                ]
            },
            "vpn": {
                "desc": "Управление VPN для анонимности",
                "usage": "vpn [action]",
                "details": [
                    "• Без параметров - показать список VPN",
                    "• vpn_connect <id> - подключиться",
                    "• vpn_disconnect - отключиться",
                    "• Снижает риск обнаружения"
                ],
                "examples": [
                    "vpn",
                    "vpn_connect 1",
                    "vpn_disconnect"
                ]
            }
        }

        if command in detailed_help:
            info = detailed_help[command]

            print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━ СПРАВКА: {command.upper()} ━━━━━━━━━━━━━━━━{Colors.RESET}")
            print(f"\n{Colors.INFO}📋 ОПИСАНИЕ:{Colors.RESET}")
            print(f"   {info['desc']}")

            print(f"\n{Colors.WARNING}💻 ИСПОЛЬЗОВАНИЕ:{Colors.RESET}")
            print(f"   {Colors.SUCCESS}{info['usage']}{Colors.RESET}")

            if 'details' in info:
                print(f"\n{Colors.INFO}📝 ПОДРОБНОСТИ:{Colors.RESET}")
                for detail in info['details']:
                    print(f"   {detail}")

            if 'examples' in info:
                print(f"\n{Colors.SUCCESS}💡 ПРИМЕРЫ:{Colors.RESET}")
                for example in info['examples']:
                    print(f"   {Colors.WARNING}{example}{Colors.RESET}")

            print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

        else:
            print(f"{Colors.ERROR}❌ Справка по команде '{command}' не найдена{Colors.RESET}")
            print(f"{Colors.INFO}💡 Используйте 'commands' для списка всех команд{Colors.RESET}")


    def _get_command_description(self, command: str) -> str:
        """Безопасно получает описание команды"""
        # Проверяем основные команды
        if hasattr(self, 'base_commands') and command in self.base_commands:
            return self.base_commands[command]

        # Проверяем контекстные команды
        if hasattr(self, 'context_commands'):
            for context_cmds in self.context_commands.values():
                if command in context_cmds:
                    return context_cmds[command]

        return "Описание недоступно"

    # ============================================================================
    # ФАЙЛ: command_completion.py
    # КЛАСС: CommandCompleter
    # МЕСТО: После метода show_command_suggestions() (примерно строка 300-350)
    # ============================================================================

    class CommandCompleter:

        def show_command_suggestions(self, failed_command: str) -> None:
            """Показывает предложения для неправильно введенной команды (исправленная версия)"""
            suggestions = self.smart_suggestions(failed_command)

            if suggestions:
                print(f"{Colors.WARNING}❓ Возможно, вы имели в виду:{Colors.RESET}")
                for i, suggestion in enumerate(suggestions, 1):
                    # ИСПРАВЛЕНО: Используем безопасное получение описания
                    if hasattr(self, 'get_command_help'):
                        try:
                            desc = self.get_command_help(suggestion)
                        except:
                            desc = "Команда игры"
                    else:
                        desc = "Команда игры"

                    print(f"   {i}. {Colors.SUCCESS}{suggestion}{Colors.RESET} - {desc}")
            else:
                print(f"{Colors.INFO}💡 Используйте 'help' или 'commands' для списка доступных команд{Colors.RESET}")

        def smart_suggestions(self, failed_command: str) -> List[str]:
            """Улучшенные предложения для неизвестных команд с полной совместимостью"""

            # Полный список всех команд игры (статический для надежности)
            all_game_commands = [
                # === ОСНОВНЫЕ КОМАНДЫ ===
                "status", "forum", "missions", "market", "contacts", "crypto",
                "training", "train", "faction", "chat",

                # === ДЕЙСТВИЯ С МИССИЯМИ ===
                "take", "work", "abort_mission", "mission_status", "team_status",
                "recruit", "recruit_team",

                # === ПОКУПКИ И ТОРГОВЛЯ ===
                "buy", "sell", "info", "item_info",

                # === КОММУНИКАЦИИ ===
                "pm", "private_message", "message",

                # === ФРАКЦИИ ===
                "join_faction", "change_faction", "faction_status", "defect",

                # === ВАЛЮТЫ ===
                "exchange_btc_usd", "exchange_usd_btc", "portfolio", "invest", "convert",

                # === СЕТЕВЫЕ КОМАНДЫ ===
                "network", "connect", "disconnect", "scan", "traceroute",

                # === ИНСТРУМЕНТЫ ХАКИНГА ===
                "nmap", "wireshark", "metasploit",

                # === VPN И АНОНИМНОСТЬ ===
                "vpn", "vpn_connect", "vpn_disconnect",

                # === БОТНЕТЫ ===
                "botnet", "buy_botnet", "ddos",

                # === ПРОДВИНУТЫЕ МИССИИ ===
                "mission_stats", "mission_statistics", "notifications",
                "show_notifications", "clear_notifications", "mission_history",
                "team_details", "moral_profile", "mission_choices",

                # === ПОИСК И ИНФОРМАЦИЯ ===
                "search", "tips", "about", "commands",

                # === НАСТРОЙКИ ===
                "settings", "audio", "music", "sound", "theme",

                # === СИСТЕМА ===
                "save", "load", "help", "exit", "quit", "debug", "reset",

                # === АЛИАСЫ ===
                "ls", "dir", "cat", "cd", "pwd", "clear", "cls", "man",
                "sudo", "ssh", "ping", "nc", "wget", "curl"
            ]

            # Добавляем команды из атрибутов класса (если они есть)
            try:
                if hasattr(self, 'base_commands') and isinstance(self.base_commands, dict):
                    all_game_commands.extend(self.base_commands.keys())

                if hasattr(self, 'context_commands') and isinstance(self.context_commands, dict):
                    for context_dict in self.context_commands.values():
                        if isinstance(context_dict, dict):
                            all_game_commands.extend(context_dict.keys())
            except Exception:
                # Игнорируем ошибки доступа к атрибутам
                pass

            # Удаляем дубликаты и сортируем
            unique_commands = sorted(list(set(all_game_commands)))

            # Нормализуем ввод пользователя
            failed_lower = failed_command.lower().strip()

            if not failed_lower:
                return []

            suggestions_with_priority = []

            # ========================================================================
            # УРОВЕНЬ 1: Точное начало (высший приоритет)
            # ========================================================================
            for cmd in unique_commands:
                if cmd.lower().startswith(failed_lower):
                    suggestions_with_priority.append((cmd, 0, len(cmd)))  # (команда, приоритет, длина)

            # ========================================================================
            # УРОВЕНЬ 2: Содержит подстроку (средний приоритет)
            # ========================================================================
            for cmd in unique_commands:
                if failed_lower in cmd.lower() and not any(s[0] == cmd for s in suggestions_with_priority):
                    # Позиция вхождения влияет на приоритет
                    position = cmd.lower().find(failed_lower)
                    suggestions_with_priority.append((cmd, 1 + position * 0.1, len(cmd)))

            # ========================================================================
            # УРОВЕНЬ 3: Похожие команды (алгоритм расстояния)
            # ========================================================================
            if len(suggestions_with_priority) < 3:  # Добавляем только если мало точных совпадений
                for cmd in unique_commands:
                    if not any(s[0] == cmd for s in suggestions_with_priority):
                        distance = self._calculate_similarity_score(failed_lower, cmd.lower())
                        if distance <= 3:  # Максимальное расстояние
                            suggestions_with_priority.append((cmd, 2 + distance, len(cmd)))

            # ========================================================================
            # УРОВЕНЬ 4: Специальные паттерны и сокращения
            # ========================================================================
            special_patterns = {
                'mi': ['missions', 'mission_status', 'mission_stats'],
                'st': ['status', 'stats'],
                'ma': ['market', 'man'],
                'cr': ['crypto', 'cracking'],
                'tr': ['training', 'train', 'traceroute'],
                'fo': ['forum'],
                'he': ['help'],
                'ex': ['exit', 'exchange_btc_usd', 'exchange_usd_btc'],
                'sa': ['save', 'scan'],
                'lo': ['load'],
                'ne': ['network', 'nmap'],
                'co': ['connect', 'commands', 'contacts'],
                'vp': ['vpn', 'vpn_connect'],
                'fa': ['faction', 'faction_status'],
                'bu': ['buy', 'buy_botnet'],
                'ta': ['take'],
                'wo': ['work'],
                'dd': ['ddos'],
                'ab': ['about', 'abort_mission']
            }

            for pattern, commands in special_patterns.items():
                if failed_lower.startswith(pattern):
                    for cmd in commands:
                        if cmd in unique_commands and not any(s[0] == cmd for s in suggestions_with_priority):
                            suggestions_with_priority.append((cmd, 0.5, len(cmd)))  # Высокий приоритет для паттернов

            # ========================================================================
            # СОРТИРОВКА И ВОЗВРАТ РЕЗУЛЬТАТА
            # ========================================================================
            if not suggestions_with_priority:
                return []

            # Сортируем по приоритету (меньше = лучше), затем по длине (короче = лучше)
            suggestions_with_priority.sort(key=lambda x: (x[1], x[2]))

            # Возвращаем только уникальные команды (первые 5)
            seen = set()
            final_suggestions = []

            for cmd, _, _ in suggestions_with_priority:
                if cmd not in seen and len(final_suggestions) < 5:
                    seen.add(cmd)
                    final_suggestions.append(cmd)

            return final_suggestions

        def _calculate_similarity_score(self, s1: str, s2: str) -> float:
            """Вычисляет оценку похожести между строками (упрощенная версия)"""
            if not s1 or not s2:
                return float('inf')

            # Простая метрика: разница в длине + количество общих символов
            len_diff = abs(len(s1) - len(s2))

            # Подсчет общих символов
            common_chars = 0
            s1_chars = list(s1)
            s2_chars = list(s2)

            for char in s1_chars:
                if char in s2_chars:
                    common_chars += 1
                    s2_chars.remove(char)  # Убираем чтобы не считать дважды

            # Чем больше общих символов, тем меньше "расстояние"
            max_len = max(len(s1), len(s2))
            similarity = common_chars / max_len if max_len > 0 else 0

            # Возвращаем инвертированную похожесть + штраф за разницу в длине
            return (1 - similarity) * 3 + len_diff * 0.5

        def _levenshtein_distance(self, s1: str, s2: str) -> int:
            """Вычисляет расстояние Левенштейна между строками"""
            if len(s1) < len(s2):
                return self._levenshtein_distance(s2, s1)

            if len(s2) == 0:
                return len(s1)

            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]
    
    def get_enhanced_input(self, prompt: str) -> str:
        """Улучшенный ввод с автодополнением и историей"""
        try:
            # Используем обычный input - readline автоматически добавит функциональность если доступен
            user_input = input(prompt).strip()
            
            if user_input:
                self.add_to_history(user_input)
            
            return user_input
            
        except (EOFError, KeyboardInterrupt):
            return "exit"
        except Exception as e:
            print(f"{Colors.ERROR}Ошибка ввода: {e}{Colors.RESET}")
            return ""
    
    def show_context_help(self) -> None:
        """Показывает справку по текущему контексту"""
        if not self.current_context:
            print(f"{Colors.INFO}Вы находитесь в главном меню{Colors.RESET}")
            return
        
        if self.current_context not in self.context_commands:
            return
        
        commands = self.context_commands[self.current_context]
        context_names = {
            "market": "Теневой рынок",
            "crypto": "Криптобиржа", 
            "forum": "Форум",
            "missions": "Система миссий",
            "faction": "Фракционное меню"
        }
        
        context_name = context_names.get(self.current_context, self.current_context)
        
        print(f"\n{Colors.INFO}📍 Контекст: {context_name}{Colors.RESET}")
        print(f"{Colors.INFO}Доступные команды:{Colors.RESET}")
        
        for cmd, desc in commands.items():
            print(f"   {Colors.WARNING}{cmd:<15}{Colors.RESET} {desc}")
        
        if HAS_READLINE:
            print(f"\n{Colors.INFO}💡 Используйте TAB для автодополнения{Colors.RESET}")


class SmartPrompt:
    """Умная командная строка с дополнительными возможностями"""
    
    def __init__(self, completer: CommandCompleter):
        self.completer = completer
        self.prompt_styles = {
            "default": "{}@xss.is:~$ ",
            "faction": "{}@xss.is[{}]:~$ ",
            "context": "{}@xss.is/{}:~$ ",
            "danger": "{}@xss.is[!]:~$ "
        }
        self.current_style = "default"
    
    def get_dynamic_prompt(self, username: str, faction: str = None, 
                          context: str = None, heat_level: int = 0) -> str:
        """Генерирует динамическую командную строку"""
        # Выбираем стиль в зависимости от состояния
        if heat_level > 80:
            style = "danger"
            prompt = self.prompt_styles[style].format(username)
            return f"{Colors.DANGER}{prompt}{Colors.RESET}"
        
        elif context:
            style = "context" 
            prompt = self.prompt_styles[style].format(username, context)
            return f"{Colors.INFO}{prompt}{Colors.RESET}"
        
        elif faction:
            style = "faction"
            prompt = self.prompt_styles[style].format(username, faction[:3].upper())
            
            # Цвет в зависимости от фракции
            faction_colors = {
                "whitehats": Colors.SUCCESS,
                "blackhats": Colors.DANGER,
                "grayhats": Colors.WARNING
            }
            color = faction_colors.get(faction, Colors.INFO)
            return f"{color}{prompt}{Colors.RESET}"
        
        else:
            prompt = self.prompt_styles["default"].format(username)
            return f"{Colors.PROMPT}{prompt}{Colors.RESET}"
    
    def process_input(self, user_input: str, game_context: dict) -> Tuple[str, List[str]]:
        """Обрабатывает пользовательский ввод и возвращает команду и аргументы"""
        if not user_input.strip():
            return "", []
        
        # Обрабатываем специальные команды
        if user_input.startswith("!"):
            # Команды истории
            if user_input == "!!":
                # Повторить последнюю команду
                if self.completer.command_history:
                    last_cmd = self.completer.command_history[-1]
                    print(f"{Colors.INFO}Повтор: {last_cmd}{Colors.RESET}")
                    return self.process_input(last_cmd, game_context)
            
            elif user_input.startswith("!"):
                try:
                    # Выполнить команду из истории по номеру
                    index = int(user_input[1:]) - 1
                    if 0 <= index < len(self.completer.command_history):
                        cmd = self.completer.command_history[index]
                        print(f"{Colors.INFO}Из истории: {cmd}{Colors.RESET}")
                        return self.process_input(cmd, game_context)
                except ValueError:
                    pass
        
        # Обрабатываем алиасы команд
        aliases = {
            "ls": "status",
            "dir": "status", 
            "cat": "info",
            "cd": "context",
            "pwd": "context",
            "clear": "cls",
            "cls": "clear_screen",
            "man": "help",
            "sudo": "admin_mode",
            "ssh": "connect",
            "ping": "scan",
            "nmap": "scan",
            "nc": "connect",
            "wget": "download",
            "curl": "api_call"
        }
        
        parts = user_input.split()
        command = parts[0].lower()
        
        # Заменяем алиас на реальную команду
        if command in aliases:
            command = aliases[command]
            parts[0] = command
        
        args = parts[1:] if len(parts) > 1 else []
        
        return command, args
    
    def show_command_preview(self, command: str, args: List[str]) -> None:
        """Показывает превью команды перед выполнением"""
        description = self.completer.get_command_help(command)
        
        if description != "Неизвестная команда":
            print(f"{Colors.INFO}💭 {description}{Colors.RESET}")

    def handle_unknown_command_simple(self, command: str) -> None:
        """Упрощенная обработка неизвестной команды"""
        print(f"{Colors.ERROR}❌ Неизвестная команда: '{command}'{Colors.RESET}")

        # Базовые предложения без сложной логики
        common_commands = [
            "status", "missions", "market", "crypto", "training", "forum",
            "take", "buy", "work", "help", "commands", "save", "exit"
        ]

        # Простой поиск по началу
        suggestions = [cmd for cmd in common_commands if cmd.startswith(command.lower())]

        # Если нет точных совпадений, ищем по содержанию
        if not suggestions:
            suggestions = [cmd for cmd in common_commands if command.lower() in cmd]

        if suggestions:
            print(f"{Colors.WARNING}❓ Возможно, вы имели в виду:{Colors.RESET}")
            for i, suggestion in enumerate(suggestions[:3], 1):
                print(f"   {i}. {Colors.SUCCESS}{suggestion}{Colors.RESET}")

        print(f"{Colors.INFO}💡 Для полного списка команд используйте: {Colors.SUCCESS}commands{Colors.RESET}")


# Глобальные экземпляры
command_completer = CommandCompleter()
smart_prompt = SmartPrompt(command_completer)