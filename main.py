"""
XSS Game 0.3.8.2 "NETWORK FOUNDATIONS" - Главный файл
"""

import os
import sys
import time
import json
from datetime import datetime
import random

# Добавляем текущую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Основные импорты
from ui.colors import XSSColors, print_xss_banner
from ui.effects import typing_effect, show_ascii_art, boxed_text
from ui.display import show_status, show_help
from ui.command_completion import command_completer, smart_prompt
from core.game_state import game_state
from core.character_creation import character_creator
from systems.audio import audio_system
from systems.network import network_system  # Новая система
from gameplay.missions import mission_system
from gameplay.forum import forum_system
from gameplay.minigames import minigame_hub
from gameplay.factions import faction_system
from systems.market import market_system
from systems.crypto import crypto_system
from systems.event_system import initialize_advanced_mission_systems, mission_statistics, mission_notifications


class XSSGame:
    """Основной класс игры версии 0.3.8"""

    def __init__(self):
        self.running = True
        self.version = "0.3.8"
        self.codename = "NETWORK FOUNDATIONS"
        self.commands = self._setup_commands()
        self.first_run = False

    def _setup_commands(self) -> dict:
        """Настройка команд игры с новыми возможностями"""
        return {
            # Основные команды
            "status": self._cmd_status,
            "forum": self._cmd_forum,
            "missions": self._cmd_missions,
            "market": self._cmd_market,
            "contacts": self._cmd_contacts,
            "crypto": self._cmd_crypto,
            "training": self._cmd_training,
            "train": self._cmd_training,
            "chat": self._cmd_chat,

            # Сетевые команды (НОВОЕ)
            "network": self._cmd_network,
            "connect": self._cmd_connect,
            "disconnect": self._cmd_disconnect,
            "scan": self._cmd_scan_network,
            "traceroute": self._cmd_traceroute,

            # Сетевые инструменты
            "nmap": self._cmd_nmap,
            "wireshark": self._cmd_wireshark,
            "metasploit": self._cmd_metasploit,

            # VPN команды
            "vpn": self._cmd_vpn,
            "vpn_connect": self._cmd_vpn_connect,
            "vpn_disconnect": self._cmd_vpn_disconnect,

            # Ботнет команды
            "botnet": self._cmd_botnet,
            "buy_botnet": self._cmd_buy_botnet,
            "ddos": self._cmd_ddos,

            # Фракции
            "faction": self._cmd_faction_info,
            "join_faction": self._cmd_join_faction,
            "change_faction": self._cmd_change_faction,
            "faction_status": self._cmd_faction_info,

            # Действия
            "take": self._cmd_take_mission,
            "work": self._cmd_work_mission,
            "buy": self._cmd_buy_item,
            "sell": self._cmd_sell_crypto,
            "pm": self._cmd_private_message,

            # Валюты
            "portfolio": self._cmd_portfolio,
            "invest": self._cmd_invest,
            "exchange_btc_usd": self._cmd_exchange_btc_usd,
            "exchange_usd_btc": self._cmd_exchange_usd_btc,

            # Информация
            "search": self._cmd_search,
            "commands": self._cmd_show_all_commands,
            "tips": self._cmd_show_tips,
            "about": self._cmd_about,
            "info": self._cmd_item_info,

            # Настройки
            "theme": self._cmd_change_theme,
            "settings": self._cmd_settings,
            "audio": self._cmd_audio,
            "music": self._cmd_toggle_music,
            "sound": self._cmd_toggle_sounds,

            # Система
            "save": self._cmd_save,
            "load": self._cmd_load,
            "help": self._cmd_help,
            "exit": self._cmd_exit,
            "quit": self._cmd_exit,
            "debug": self._cmd_debug_mode,
            "reset": self._cmd_reset_character,

            # Продвинутые команды миссий
            "mission_stats": self._cmd_mission_statistics,
            "notifications": self._cmd_show_notifications,
            "clear_notifications": self._cmd_clear_notifications,
            "mission_history": self._cmd_mission_history,
            "team_details": self._cmd_team_details,
            "moral_profile": self._cmd_moral_profile,

            # Команды для отладки и тестирования
            "test_event": self._cmd_test_event,
            "simulate_mission": self._cmd_simulate_mission,
        }

    def initialize(self) -> None:
        """Инициализация игры с проверкой нового игрока"""
        try:
            self._show_startup_banner()

            if audio_system.audio_available:
                audio_system.check_audio_files()
                if audio_system.music_enabled:
                    audio_system.start_background_music()

            save_exists = os.path.exists("xss_save.json")

            if save_exists:
                print(f"\n{XSSColors.INFO}ℹ️ Обнаружено сохранение игры.{XSSColors.RESET}")
                choice = command_completer.get_enhanced_input(
                    f"{XSSColors.PROMPT}Загрузить сохранение? (y/n/new): {XSSColors.RESET}"
                ).lower()

                if choice in ['y', 'yes', 'да']:
                    if game_state.load_game():
                        self._check_version_compatibility()
                    else:
                        self._start_new_game()
                else:
                    self._start_new_game()
            else:
                self._start_new_game()

            if not game_state.get_stat('character_created', False):
                self._run_character_creation()

            self._setup_command_completion()
            self._show_welcome_message()
            self._initialize_advanced_systems()
            self._update_story()

        except Exception as e:
            print(f"{XSSColors.ERROR}[КРИТИЧЕСКАЯ ОШИБКА] Инициализация: {e}{XSSColors.RESET}")
            self._handle_critical_error(e)

    def _initialize_advanced_systems(self) -> None:
        """Инициализирует продвинутые системы игры"""
        try:
            # Инициализируем продвинутые системы миссий
            self.mission_event_manager = initialize_advanced_mission_systems(mission_system)

            print(f"{XSSColors.SUCCESS}✅ Продвинутые системы миссий инициализированы{XSSColors.RESET}")

        except Exception as e:
            print(f"{XSSColors.WARNING}⚠️ Ошибка инициализации продвинутых систем: {e}{XSSColors.RESET}")
            # Игра должна работать и без продвинутых систем

    def _handle_critical_error(self, error: Exception) -> None:
        """Обработка критических ошибок"""
        import traceback

        error_log = f"""
=== CRITICAL ERROR LOG ===
Time: {datetime.now()}
Version: {self.version}
Error: {str(error)}
Traceback:
{traceback.format_exc()}
========================
"""

        try:
            with open("error_log.txt", "a", encoding="utf-8") as f:
                f.write(error_log)
            print(f"{XSSColors.INFO}Лог ошибки сохранен в error_log.txt{XSSColors.RESET}")
        except:
            pass

        print(f"{XSSColors.WARNING}Попытка аварийного сохранения...{XSSColors.RESET}")
        try:
            game_state.save_game("emergency_save.json")
            print(f"{XSSColors.SUCCESS}Аварийное сохранение создано: emergency_save.json{XSSColors.RESET}")
        except:
            print(f"{XSSColors.ERROR}Не удалось создать аварийное сохранение{XSSColors.RESET}")

    def _check_version_compatibility(self) -> None:
        """Проверяет совместимость версий сохранения"""
        save_version = game_state.get_stat("game_version", "0.2.9")
        if save_version != self.version:
            boxed_text("ОБНОВЛЕНИЕ СОХРАНЕНИЯ", color=XSSColors.WARNING)
            print(f"{XSSColors.LIGHT_GRAY}Версия сохранения: {save_version}{XSSColors.RESET}")
            print(f"{XSSColors.LIGHT_GRAY}Текущая версия: {self.version}{XSSColors.RESET}")
            self._migrate_save_data(save_version)
            game_state.set_stat("game_version", self.version)
            print(f"{XSSColors.SUCCESS}✅ Сохранение обновлено до версии {self.version}{XSSColors.RESET}")

    def _migrate_save_data(self, old_version: str) -> None:
        """Миграция данных сохранения между версиями"""
        migrations = {
            "0.2.9": self._migrate_from_029,
            "0.3.0": self._migrate_from_030
        }

        if old_version in migrations:
            try:
                migrations[old_version]()
                print(f"{XSSColors.SUCCESS}✅ Миграция с версии {old_version} завершена{XSSColors.RESET}")
            except Exception as e:
                print(f"{XSSColors.ERROR}❌ Ошибка миграции: {e}{XSSColors.RESET}")

    def _migrate_from_029(self) -> None:
        """Миграция с версии 0.2.9"""
        # Добавляем новые поля если их нет
        if not game_state.get_stat("network_nodes", None):
            game_state.set_stat("network_nodes", {})
        if not game_state.get_stat("current_node", None):
            game_state.set_stat("current_node", "localhost")

    def _migrate_from_030(self) -> None:
        """Миграция с версии 0.3.0"""
        # Пока нет специфичных изменений
        pass

    # Сетевые команды (НОВЫЕ)
    def _cmd_network(self, args: list) -> None:
        """Показать сетевую карту"""
        network_system.show_network_map()

    def _cmd_connect(self, args: list) -> None:
        """Подключиться к узлу с валидацией"""
        if not args:
            print(f"{XSSColors.ERROR}Укажите адрес узла{XSSColors.RESET}")
            return

        address = args[0].strip()

        # Валидация адреса
        if not address or len(address) > 100:
            print(f"{XSSColors.ERROR}Неверный адрес узла{XSSColors.RESET}")
            return

        # Базовая проверка формата (IP, домен, localhost)
        import re
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not (address == 'localhost' or
                re.match(ip_pattern, address) or
                re.match(domain_pattern, address) or
                address.endswith('.onion')):
            print(f"{XSSColors.WARNING}Предупреждение: неожиданый формат адреса{XSSColors.RESET}")

        network_system.connect_to_node(address)

    def _cmd_disconnect(self, args: list) -> None:
        """Отключиться от текущего узла"""
        network_system.disconnect()

    def _cmd_scan_network(self, args: list) -> None:
        """Сканировать сеть"""
        network_system.scan_network()

    def _cmd_traceroute(self, args: list) -> None:
        """Трассировка маршрута"""
        if not args:
            print(f"{XSSColors.ERROR}Укажите целевой узел{XSSColors.RESET}")
            return
        network_system.traceroute(args[0])

    def _cmd_chat(self, args: list) -> None:
        """Глобальный чат"""
        if not args:
            self._show_chat_room()
        elif args[0] == "send" and len(args) > 1:
            message = " ".join(args[1:])
            self._send_chat_message(message)
        else:
            print(f"{XSSColors.ERROR}Использование: chat или chat send <сообщение>{XSSColors.RESET}")

    def _show_chat_room(self) -> None:
        """Показывает чат-комнату"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━ ЧАТ XSS.IS ━━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Генерируем случайные сообщения в чате
        chat_messages = [
            "[Shadow_Master] Кто знает где достать новые 0-day?",
            "[CyberNinja] Сегодня полиция активна, будьте осторожны",
            "[DataMiner] Продаю базу данных банка, в личку",
            "[Anonymous] Heat level зашкаливает, ухожу в подполье",
            "[GhostHacker] Новый метод обхода 2FA, кому интересно?",
            "[QuantumCoder] BTC упал на 15%, хорошее время для покупки"
        ]

        print(f"\n{XSSColors.INFO}💬 Последние сообщения:{XSSColors.RESET}")
        for msg in random.sample(chat_messages, 4):
            print(f"   {msg}")

        print(f"\n{XSSColors.WARNING}Ваш никнейм: {game_state.get_stat('username')}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Команды: chat send <сообщение>{XSSColors.RESET}")

    def _send_chat_message(self, message: str) -> None:
        """Отправляет сообщение в чат"""
        username = game_state.get_stat('username')
        heat_level = game_state.get_stat('heat_level', 0)

        # Проверка на подозрительность сообщения
        suspicious_words = ["полиция", "фбр", "арест", "поймали", "взяли"]
        if any(word in message.lower() for word in suspicious_words):
            heat_gain = random.randint(5, 15)
            game_state.modify_stat("heat_level", heat_gain)
            print(f"{XSSColors.ERROR}⚠️ Подозрительное сообщение! Heat Level +{heat_gain}%{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}[{username}]: {message}{XSSColors.RESET}")

        # Случайные ответы
        if random.random() < 0.3:
            responses = [
                "[CyberGhost] Интересно...",
                "[Anonymous] Согласен",
                "[DarkWeb_Admin] Будь осторожнее с такими словами",
                "[InfoBroker] У меня есть информация по этому поводу",
                "[SecureCoder] Используй VPN!"
            ]
            time.sleep(1)
            print(f"{XSSColors.INFO}{random.choice(responses)}{XSSColors.RESET}")



    def _emergency_save(self) -> None:
        """Аварийное сохранение при критических ошибках"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            emergency_file = f"emergency_save_{timestamp}.json"

            if game_state.save_game(emergency_file):
                print(f"{XSSColors.SUCCESS}✅ Аварийное сохранение: {emergency_file}{XSSColors.RESET}")
            else:
                # Последняя попытка - простейшее сохранение
                with open(emergency_file, "w", encoding="utf-8") as f:
                    json.dump(game_state.player_stats, f)
                print(f"{XSSColors.SUCCESS}✅ Базовое аварийное сохранение: {emergency_file}{XSSColors.RESET}")
        except Exception as e:
            print(f"{XSSColors.ERROR}❌ Не удалось создать аварийное сохранение: {e}{XSSColors.RESET}")

    def _handle_runtime_error(self, error: Exception) -> None:
        """Обработка ошибок во время игры"""
        print(f"{XSSColors.WARNING}Произошла ошибка, но игра продолжается...{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Используйте 'save' для сохранения прогресса{XSSColors.RESET}")

        # Логируем ошибку
        try:
            with open("runtime_errors.log", "a", encoding="utf-8") as f:
                f.write(f"\n{datetime.now()}: {error}\n")
        except:
            pass

    def _get_dynamic_prompt(self) -> str:
        """Генерирует динамическую командную строку в стиле xss.is"""
        username = game_state.get_stat('username', 'user')
        heat_level = game_state.get_stat('heat_level', 0)
        current_node = game_state.get_stat('current_node', 'localhost')

        heat_indicator = XSSColors.heat_color(heat_level) + "●" + XSSColors.RESET

        # Показываем текущий узел если не localhost
        if current_node != 'localhost':
            return f"{heat_indicator} {XSSColors.BRIGHT_GREEN}{username}{XSSColors.DARK_GRAY}@{current_node}{XSSColors.WHITE}:~${XSSColors.RESET} "
        else:
            return f"{heat_indicator} {XSSColors.BRIGHT_GREEN}{username}{XSSColors.DARK_GRAY}@xss.is{XSSColors.WHITE}:~${XSSColors.RESET} "

    def _process_command(self, command: str, args: list) -> None:
        """Обрабатывает команду с улучшенной обработкой ошибок"""
        if command in self.commands:
            try:
                self.commands[command](args)
            except Exception as e:
                print(f"{XSSColors.ERROR}[ОШИБКА КОМАНДЫ] {command}: {e}{XSSColors.RESET}")
                # Не прерываем игру, продолжаем
        else:
            smart_prompt.handle_unknown_command(command)

    # Остальные методы остаются без изменений, но с заменой Colors на XSSColors
    def _cmd_status(self, args: list) -> None:
        show_status(game_state)

    def _cmd_forum(self, args: list) -> None:
        forum_system.browse_forum(args)

    def _cmd_missions(self, args: list) -> None:
        mission_system.show_missions()

    def _cmd_market(self, args: list) -> None:
        market_system.show_market()

    def _cmd_contacts(self, args: list) -> None:
        forum_system.show_contacts()

    def _cmd_crypto(self, args: list) -> None:
        crypto_system.show_crypto_market()

    def _cmd_training(self, args: list) -> None:
        """Тренировочный центр с информацией о наградах"""
        print(f"\n{XSSColors.INFO}🎯 ТРЕНИРОВОЧНЫЙ ЦЕНТР{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Награды за успешные тренировки:{XSSColors.RESET}")
        print(f"   • BTC: 5-20 (зависит от навыка)")
        print(f"   • Репутация: 2-8 (зависит от сложности)")
        print(f"   • Рост навыка: 30% шанс (уменьшается с ростом)")
        print(f"   • Экспертный бонус: до +10 репутации для мастеров")

        minigame_hub.show_hub()

    def _cmd_faction_info(self, args: list) -> None:
        if args and args[0] == "missions":
            faction_system.show_faction_missions()
        elif args and args[0] == "status":
            faction_system.show_faction_info()
        else:
            faction_system.show_faction_info()

    def _cmd_join_faction(self, args: list) -> None:
        faction_system.show_faction_selection()

    def _cmd_change_faction(self, args: list) -> None:
        if not args:
            print(f"{XSSColors.ERROR}Укажите новую фракцию: whitehats, blackhats, grayhats{XSSColors.RESET}")
        else:
            faction_system.change_faction(args[0].lower())

    def _cmd_take_mission(self, args: list) -> None:
        """Взять миссию с валидацией"""
        if not args:
            print(f"{XSSColors.ERROR}[ОШИБКА] Укажите ID миссии{XSSColors.RESET}")
            return

        mission_id = args[0].strip()

        # Валидация ID миссии
        if not mission_id or len(mission_id) > 50:
            print(f"{XSSColors.ERROR}[ОШИБКА] Неверный ID миссии{XSSColors.RESET}")
            return

        # Проверка на небезопасные символы
        if not mission_id.replace('_', '').replace('-', '').isalnum():
            print(f"{XSSColors.ERROR}[ОШИБКА] ID может содержать только буквы, цифры, _ и -{XSSColors.RESET}")
            return

        mission_system.take_mission(mission_id)

    def _cmd_work_mission(self, args: list) -> None:
        mission_system.work_mission()

    def _cmd_buy_item(self, args: list) -> None:
        """Купить предмет с валидацией"""
        if not args:
            print(f"{XSSColors.ERROR}[ОШИБКА] Укажите ID предмета{XSSColors.RESET}")
            return

        item_id = args[0].strip()

        # Валидация ID предмета
        if not item_id or len(item_id) > 50:
            print(f"{XSSColors.ERROR}[ОШИБКА] Неверный ID предмета{XSSColors.RESET}")
            return

        # Проверка на небезопасные символы
        if not item_id.replace('_', '').replace('-', '').isalnum():
            print(f"{XSSColors.ERROR}[ОШИБКА] ID может содержать только буквы, цифры, _ и -{XSSColors.RESET}")
            return

        market_system.buy_item(item_id)

    def _cmd_sell_crypto(self, args: list) -> None:
        print(f"{XSSColors.INFO}Используйте меню криптобиржи для продажи{XSSColors.RESET}")

    def _cmd_private_message(self, args: list) -> None:
        if not args:
            print(f"{XSSColors.ERROR}Укажите имя контакта{XSSColors.RESET}")
        else:
            forum_system.private_message(args[0])

    def _cmd_search(self, args: list) -> None:
        print(f"{XSSColors.INFO}Функция поиска в разработке{XSSColors.RESET}")

    def _cmd_portfolio(self, args: list) -> None:
        crypto_system.show_crypto_market()

    def _cmd_invest(self, args: list) -> None:
        crypto_system.show_crypto_market()

    def _cmd_exchange_btc_usd(self, args: list) -> None:
        """Обменять BTC на USD с валидацией"""
        if not args:
            print(f"{XSSColors.ERROR}Укажите сумму BTC{XSSColors.RESET}")
            return

        try:
            amount = float(args[0])

            # Проверка разумных пределов
            if amount <= 0:
                print(f"{XSSColors.ERROR}Сумма должна быть положительной{XSSColors.RESET}")
                return

            if amount > 1000000:  # Защита от слишком больших чисел
                print(f"{XSSColors.ERROR}Слишком большая сумма{XSSColors.RESET}")
                return

            # Проверка наличия средств
            current_btc = game_state.get_stat("btc_balance", 0)
            if amount > current_btc:
                print(f"{XSSColors.ERROR}Недостаточно BTC (у вас: {current_btc:.4f}){XSSColors.RESET}")
                return

            crypto_system.convert_btc_to_usd(amount)

        except (ValueError, OverflowError):
            print(f"{XSSColors.ERROR}Неверный формат суммы{XSSColors.RESET}")
        except Exception as e:
            print(f"{XSSColors.ERROR}Ошибка обмена: {e}{XSSColors.RESET}")

    def _cmd_exchange_usd_btc(self, args: list) -> None:
        if not args:
            print(f"{XSSColors.ERROR}Укажите сумму USD{XSSColors.RESET}")
        else:
            try:
                amount = float(args[0])
                crypto_system.convert_usd_to_btc(amount)
            except ValueError:
                print(f"{XSSColors.ERROR}Неверная сумма{XSSColors.RESET}")

    def _cmd_show_all_commands(self, args: list) -> None:
        command_completer.show_all_commands()

    def _cmd_show_tips(self, args: list) -> None:
        self._show_newbie_tips()

    def _cmd_about(self, args: list) -> None:
        boxed_text(f"XSS GAME {self.version} - \"{self.codename}\"", color=XSSColors.BRIGHT_GREEN)
        print(f"\n{XSSColors.WHITE}Продвинутый симулятор хакера{XSSColors.RESET}")
        print(f"{XSSColors.LIGHT_GRAY}Погрузитесь в мир киберпреступности и станьте легендой.{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}✨ Новое в версии {self.version}:{XSSColors.RESET}")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Базовая сетевая система")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Исправлены критические баги")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Улучшена стабильность")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Оптимизирована экономика")

    def _cmd_change_theme(self, args: list) -> None:
        print(f"{XSSColors.INFO}Смена темы в разработке{XSSColors.RESET}")

    def _cmd_settings(self, args: list) -> None:
        print(f"{XSSColors.INFO}Настройки в разработке{XSSColors.RESET}")

    def _cmd_audio(self, args: list) -> None:
        audio_system.audio_menu()

    def _cmd_toggle_music(self, args: list) -> None:
        audio_system.toggle_music()

    def _cmd_toggle_sounds(self, args: list) -> None:
        audio_system.toggle_sounds()

    def _cmd_item_info(self, args: list) -> None:
        if not args:
            print(f"{XSSColors.ERROR}Укажите ID предмета{XSSColors.RESET}")
        else:
            market_system.show_item_info(args[0])

    def _cmd_help(self, args: list) -> None:
        """Показать справку или справку по конкретной команде"""
        if args:
            # Справка по конкретной команде
            command = args[0].lower()
            command_completer.show_command_help(command)
        else:
            # Общая справка
            show_help()

    def _cmd_debug_mode(self, args: list) -> None:
        print(f"{XSSColors.INFO}Debug режим в разработке{XSSColors.RESET}")

    def _cmd_reset_character(self, args: list) -> None:
        print(f"{XSSColors.INFO}Сброс персонажа в разработке{XSSColors.RESET}")

    def _cmd_exit(self, args: list) -> None:
        print(f"\n{XSSColors.WARNING}Отключение от xss.is...{XSSColors.RESET}")

        if game_state.get_stat("autosave_enabled", True):
            game_state.save_game()
            print(f"{XSSColors.SUCCESS}💾 Игра автоматически сохранена{XSSColors.RESET}")

        audio_system.play_sound("logout")
        audio_system.stop_background_music()

        print(
            f"{XSSColors.LIGHT_GRAY}Увидимся в даркнете, {game_state.get_stat('username', 'хакер')}!{XSSColors.RESET}")

        self.running = False

    def _show_newbie_tips(self) -> None:
        """Показывает советы для новичков"""
        print(f"\n{XSSColors.INFO}💡 СОВЕТЫ ДЛЯ НОВИЧКОВ:{XSSColors.RESET}")
        print(
            f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Используйте {XSSColors.BRIGHT_GREEN}TAB{XSSColors.RESET} для автодополнения команд")
        print(
            f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Начните с команды {XSSColors.WARNING}'status'{XSSColors.RESET} для просмотра профиля")
        print(
            f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Изучите {XSSColors.WARNING}'forum'{XSSColors.RESET} для поиска первых заданий")
        print(
            f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} {XSSColors.WARNING}'help'{XSSColors.RESET} покажет все доступные команды")
        print(
            f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} {XSSColors.SUCCESS}НОВОЕ:{XSSColors.RESET} Используйте {XSSColors.WARNING}'network'{XSSColors.RESET} для просмотра сети")
        print(
            f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} {XSSColors.WARNING}'network'{XSSColors.RESET} покажет карту сети")
        print(
            f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} {XSSColors.WARNING}'nmap <target>'{XSSColors.RESET} для сканирования узлов")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} {XSSColors.WARNING}'vpn'{XSSColors.RESET} для анонимности")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} {XSSColors.WARNING}'botnet'{XSSColors.RESET} для DDoS атак")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Используйте VPN перед атаками!")

    def _show_startup_banner(self) -> None:
        """Показывает новый стартовый баннер в стиле xss.is"""
        print_xss_banner()
        print(f"\n{XSSColors.SUCCESS}🎉 ВЕРСИЯ {self.version} - {self.codename}{XSSColors.RESET}")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Базовая сетевая система")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Исправлены критические баги")
        print(f"   {XSSColors.DARK_GRAY}•{XSSColors.RESET} Улучшена экономика")

    def _start_new_game(self) -> None:
        """Запускает новую игру"""
        self.first_run = True
        print(
            f"\n{XSSColors.gradient_text('🌟 Добро пожаловать в мир киберпреступности!', (126, 211, 33), (100, 181, 246))}{XSSColors.RESET}")
        typing_effect(f"{XSSColors.LIGHT_GRAY}Вы вот-вот войдете в теневой мир хакеров...{XSSColors.RESET}")
        audio_system.play_sound("login")

    def _run_character_creation(self) -> None:
        """Запускает процесс создания персонажа"""
        boxed_text("СОЗДАНИЕ ПЕРСОНАЖА", color=XSSColors.WARNING)
        typing_effect(f"{XSSColors.INFO}Для начала игры необходимо создать хакера.{XSSColors.RESET}")

        creation_data = character_creator.start_creation()

        if creation_data:
            print(f"\n{XSSColors.SUCCESS}✅ Персонаж успешно создан!{XSSColors.RESET}")
        else:
            print(f"\n{XSSColors.ERROR}❌ Создание персонажа отменено{XSSColors.RESET}")
            self.running = False

    def _show_welcome_message(self) -> None:
        """Показывает приветственное сообщение"""
        username = game_state.get_stat('username', 'Unknown')
        faction = game_state.get_stat('faction')

        if self.first_run:
            typing_effect(f"{XSSColors.BRIGHT_GREEN}Инициализация терминала xss.is...{XSSColors.RESET}")
            typing_effect(f"{XSSColors.INFO}Установка защищенного соединения...{XSSColors.RESET}")
            time.sleep(1)

        print(f"\n{XSSColors.SUCCESS}✅ Авторизация успешна{XSSColors.RESET}")
        print(
            f"{XSSColors.WHITE}Добро пожаловать, {XSSColors.BRIGHT_GREEN}{username}{XSSColors.WHITE}!{XSSColors.RESET}")

        if faction:
            faction_name = faction_system.factions[faction]['name']
            print(f"{XSSColors.WHITE}Фракция: {XSSColors.SUCCESS}{faction_name}{XSSColors.RESET}")

        if self.first_run or game_state.get_stat("reputation", 0) < 25:
            self._show_newbie_tips()

    def _process_random_events(self) -> None:
        """Обрабатывает случайные события"""
        event_chance = random.random()

        if event_chance < 0.1:  # 10% шанс
            events = [
                self._network_intrusion_event,
                self._market_fluctuation_event,
                self._faction_conflict_event,
                self._data_leak_event
            ]

            event = random.choice(events)
            event()

    def _network_intrusion_event(self) -> None:
        """Событие вторжения в сеть"""
        if random.random() < 0.5:
            print(f"\n{XSSColors.DANGER}🚨 ОБНАРУЖЕНА ПОПЫТКА ВТОРЖЕНИЯ!{XSSColors.RESET}")
            print(f"{XSSColors.WARNING}Кто-то пытается взломать вашу систему...{XSSColors.RESET}")

            # Даем игроку шанс защититься
            if game_state.get_skill("stealth") >= 5:
                print(f"{XSSColors.SUCCESS}✅ Ваши навыки скрытности помогли отразить атаку{XSSColors.RESET}")
            else:
                heat_gain = random.randint(5, 15)
                game_state.modify_stat("heat_level", heat_gain)
                print(f"{XSSColors.ERROR}❌ Атака успешна! Heat Level +{heat_gain}%{XSSColors.RESET}")

    def _market_fluctuation_event(self) -> None:
        """Событие колебания рынка - ИСПРАВЛЕННОЕ"""
        if random.random() < 0.3:
            # ДОБАВЛЯЕМ ПРЯМОЙ ВЫЗОВ СОБЫТИЯ КРИПТОВАЛЮТЫ
            from systems.event_system import event_system, CryptoMarketChangeEvent

            # Выбираем случайную криптовалюту
            cryptos = ["BTC", "ETH", "LTC", "XRP", "DOGE"]
            symbol = random.choice(cryptos)

            old_price = crypto_system.get_crypto_price(symbol)

            # Применяем событие к рынку
            event_type = random.choice(["bull_run", "bear_market", "volatility"])
            crypto_system.simulate_market_event(event_type)

            new_price = crypto_system.get_crypto_price(symbol)
            change_percent = ((new_price - old_price) / old_price) * 100 if old_price > 0 else 0

            # Отправляем событие
            market_event = CryptoMarketChangeEvent(symbol, old_price, new_price, change_percent)
            event_system.dispatch(market_event)

    def _faction_conflict_event(self) -> None:
        """Событие конфликта фракций"""
        if game_state.get_stat("faction"):
            faction_system.faction_war_event()

    def _data_leak_event(self) -> None:
        """Событие утечки данных"""
        print(f"\n{XSSColors.INFO}📰 НОВОСТИ: Крупная утечка данных обнаружена в сети!{XSSColors.RESET}")
        print(f"{XSSColors.WARNING}Это может повлиять на рынок и миссии...{XSSColors.RESET}")


    def _update_story(self) -> None:
        """Обновляет сюжет"""
        current_stage = game_state.get_stat("story_stage", 0)
        reputation = game_state.get_stat("reputation", 0)

        # Проверяем условия перехода на следующий этап
        stage_requirements = {
            1: {"reputation": 50},
            2: {"reputation": 100, "completed_missions": 5},
            3: {"reputation": 200, "completed_missions": 10},
            4: {"reputation": 500, "completed_missions": 20}
        }

        next_stage = current_stage + 1
        if next_stage in stage_requirements:
            reqs = stage_requirements[next_stage]

            # Проверяем репутацию
            if reputation >= reqs.get("reputation", 0):
                # Проверяем количество миссий
                completed = len(game_state.get_stat("completed_missions", []))
                if completed >= reqs.get("completed_missions", 0):
                    game_state.set_stat("story_stage", next_stage)
                    self._show_story_advancement(next_stage)

    def _show_story_advancement(self, stage: int) -> None:
        """Показывает продвижение по сюжету"""
        audio_system.play_sound("achievement")
        show_ascii_art("level_up")

        stage_names = {
            1: "Признанный хакер",
            2: "Элитный специалист",
            3: "Легенда подполья",
            4: "Властелин даркнета"
        }

        print(f"\n{XSSColors.SUCCESS}{'=' * 60}{XSSColors.RESET}")
        print(f"{XSSColors.STORY}📖 НОВЫЙ СЮЖЕТНЫЙ ЭТАП: {stage_names.get(stage, 'Неизвестно')}{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}{'=' * 60}{XSSColors.RESET}")

        # Награды за этап
        rewards = {
            1: {"btc": 100, "rep": 25},
            2: {"btc": 250, "rep": 50, "item": "elite_toolkit"},
            3: {"btc": 500, "rep": 100, "contact": "shadow_broker"},
            4: {"btc": 1000, "rep": 200, "special": "admin_access"}
        }

        if stage in rewards:
            reward = rewards[stage]
            if "btc" in reward:
                game_state.earn_currency(reward["btc"], "btc_balance")
                print(f"{XSSColors.MONEY}[+] {reward['btc']} BTC{XSSColors.RESET}")
            if "rep" in reward:
                game_state.modify_stat("reputation", reward["rep"])
                print(f"{XSSColors.REP}[+] {reward['rep']} репутации{XSSColors.RESET}")
            if "item" in reward:
                game_state.add_to_inventory(reward["item"])
                print(f"{XSSColors.INFO}[+] Получен предмет: {reward['item']}{XSSColors.RESET}")
            if "contact" in reward:
                game_state.add_contact(reward["contact"])
                print(f"{XSSColors.WARNING}[+] Новый контакт: {reward['contact']}{XSSColors.RESET}")

    def _check_game_over(self) -> bool:
        """Проверяет условия конца игры"""
        warnings = game_state.get_stat("warnings", 0)
        heat_level = game_state.get_stat("heat_level", 0)

        if warnings >= 3:
            self._show_ending("banned")
            return True

        if heat_level >= 100:
            self._show_ending("burned")
            return True

        return False

    def _show_ending(self, ending_type: str) -> None:
        """Показывает концовку игры"""
        audio_system.stop_background_music()
        audio_system.play_sound("logout")

        boxed_text("КОНЕЦ ИГРЫ", color=XSSColors.ERROR)

        if ending_type == "burned":
            show_ascii_art("skull")
            print(f"{XSSColors.ERROR}Вы привлекли слишком много внимания!{XSSColors.RESET}")
            print(f"{XSSColors.WARNING}Правоохранительные органы вышли на ваш след...{XSSColors.RESET}")
        elif ending_type == "banned":
            print(f"{XSSColors.ERROR}Слишком много нарушений!{XSSColors.RESET}")
            print(f"{XSSColors.WARNING}Ваш аккаунт заблокирован администрацией...{XSSColors.RESET}")

        self._show_final_statistics()

        choice = input(f"\n{XSSColors.PROMPT}Начать новую игру? (y/n): {XSSColors.RESET}").lower()
        if choice in ['y', 'yes']:
            self._restart_game()
        else:
            self.running = False

    def _show_final_statistics(self) -> None:
        """Показывает финальную статистику"""
        print(f"\n{XSSColors.INFO}📊 ФИНАЛЬНАЯ СТАТИСТИКА:{XSSColors.RESET}")

        stats = game_state.get_summary()
        print(f"   Никнейм: {stats['username']}")
        print(f"   Репутация: {stats['reputation']}")
        print(f"   Выполнено миссий: {stats['completed_missions']}")
        print(f"   Достижений: {stats['achievements']}")
        print(f"   Сюжетный этап: {stats['story_stage']}")

    def _restart_game(self) -> None:
        """Перезапускает игру"""
        game_state.reset_game()
        self.first_run = True
        self.initialize()

    def _handle_interrupt(self) -> None:
        """Обработка прерывания (Ctrl+C)"""
        print(f"\n\n{XSSColors.WARNING}Прерывание обнаружено...{XSSColors.RESET}")

        try:
            save_choice = input(f"{XSSColors.PROMPT}Сохранить игру перед выходом? (y/n): {XSSColors.RESET}").lower()
            if save_choice in ['y', 'yes']:
                game_state.save_game()
        except:
            # Если пользователь снова нажал Ctrl+C
            pass

        self.running = False

    def _setup_command_completion(self) -> None:
        """Настраивает автодополнение команд с полным набором"""

        # Проверяем что command_completer доступен
        if not hasattr(command_completer, 'base_commands'):
            print(f"{XSSColors.WARNING}⚠️ Автодополнение не может быть настроено{XSSColors.RESET}")
            return

        # Добавляем команды которых может не быть в базовом списке
        additional_commands = {
            # Сетевые команды
            "network": "Показать карту сети",
            "connect": "Подключиться к узлу [адрес]",
            "disconnect": "Отключиться от текущего узла",
            "scan": "Сканировать текущую сеть",
            "traceroute": "Трассировка маршрута [адрес]",
            "nmap": "Сканирование портов [цель] [тип]",
            "wireshark": "Перехват трафика [интерфейс] [время]",
            "metasploit": "Запуск эксплойта [цель] [эксплойт]",

            # VPN команды
            "vpn": "Управление VPN",
            "vpn_connect": "Подключиться к VPN [номер]",
            "vpn_disconnect": "Отключиться от VPN",

            # Ботнет команды
            "botnet": "Управление ботнетами",
            "buy_botnet": "Купить ботнет [номер]",
            "ddos": "DDoS атака [цель]",

            # Продвинутые команды миссий
            "mission_stats": "Статистика выполнения миссий",
            "mission_statistics": "Детальная статистика миссий",
            "notifications": "Показать активные уведомления",
            "show_notifications": "Показать уведомления (алиас)",
            "clear_notifications": "Очистить все уведомления",
            "mission_history": "История всех миссий",
            "team_details": "Детали текущей команды",
            "moral_profile": "Моральный профиль игрока",
            "abort_mission": "Прервать активную миссию",
            "recruit_team": "Набрать команду для миссии",
            "mission_choices": "История моральных выборов",

            # Команды чата
            "chat": "Глобальный чат",

            # Отладочные команды
            "test_event": "Тестировать событие (отладка)",
            "simulate_mission": "Симулировать миссию (отладка)",

            # Дополнительные алиасы
            "train": "Тренировочный центр (алиас)",
            "ls": "Статус (алиас)",
            "dir": "Статус (алиас)",
            "man": "Справка (алиас)"
        }

        # Безопасно добавляем команды
        try:
            command_completer.base_commands.update(additional_commands)
            total_commands = len(command_completer.base_commands)
            print(f"{XSSColors.SUCCESS}✅ Автодополнение настроено для {total_commands} команд{XSSColors.RESET}")

            # Проверяем наличие контекстных команд
            if hasattr(command_completer, 'context_commands'):
                context_count = sum(len(cmds) for cmds in command_completer.context_commands.values())
                print(f"{XSSColors.INFO}📋 Контекстных команд: {context_count}{XSSColors.RESET}")

        except Exception as e:
            print(f"{XSSColors.ERROR}❌ Ошибка настройки автодополнения: {e}{XSSColors.RESET}")
    def _cmd_nmap(self, args: list) -> None:
        """Nmap сканирование"""
        if not args:
            print(f"{XSSColors.ERROR}Укажите цель для сканирования{XSSColors.RESET}")
            print(f"{XSSColors.INFO}Использование: nmap <target> [scan_type]{XSSColors.RESET}")
            print(f"{XSSColors.INFO}Типы сканирования: basic, full, stealth, vuln{XSSColors.RESET}")
            return

        target = args[0]
        scan_type = args[1] if len(args) > 1 else "basic"

        if scan_type not in ["basic", "full", "stealth", "vuln"]:
            print(f"{XSSColors.ERROR}Неверный тип сканирования{XSSColors.RESET}")
            return

        network_system.network_tools.nmap_scan(target, scan_type)

    def _cmd_wireshark(self, args: list) -> None:
        """Перехват трафика Wireshark"""
        interface = args[0] if args else "eth0"
        duration = int(args[1]) if len(args) > 1 else 10

        if duration > 60:
            print(f"{XSSColors.WARNING}Максимальная длительность: 60 секунд{XSSColors.RESET}")
            duration = 60

        network_system.network_tools.wireshark_capture(interface, duration)

    def _cmd_metasploit(self, args: list) -> None:
        """Metasploit эксплойт"""
        if len(args) < 2:
            print(f"{XSSColors.ERROR}Укажите цель и эксплойт{XSSColors.RESET}")
            print(f"{XSSColors.INFO}Использование: metasploit <target> <exploit>{XSSColors.RESET}")
            print(f"{XSSColors.INFO}Эксплойты: buffer_overflow, sql_injection, weak_password{XSSColors.RESET}")
            return

        target = args[0]
        exploit = args[1]

        exploits = ["buffer_overflow", "sql_injection", "weak_password", "rce", "privilege_escalation"]
        if exploit not in exploits:
            print(f"{XSSColors.ERROR}Неизвестный эксплойт{XSSColors.RESET}")
            print(f"{XSSColors.INFO}Доступные: {', '.join(exploits)}{XSSColors.RESET}")
            return

        network_system.network_tools.metasploit_exploit(target, exploit)

    def _cmd_vpn(self, args: list) -> None:
        """Управление VPN"""
        network_system.vpn_manager.show_vpn_list()

    def _cmd_vpn_connect(self, args: list) -> None:
        """Подключиться к VPN"""
        if not args:
            print(f"{XSSColors.ERROR}Укажите номер VPN провайдера{XSSColors.RESET}")
            return

        try:
            vpn_index = int(args[0])
            network_system.vpn_manager.connect_vpn(vpn_index)
        except ValueError:
            print(f"{XSSColors.ERROR}Неверный номер VPN{XSSColors.RESET}")

    def _cmd_vpn_disconnect(self, args: list) -> None:
        """Отключиться от VPN"""
        network_system.vpn_manager.disconnect_vpn()

    def _cmd_botnet(self, args: list) -> None:
        """Управление ботнетами"""
        network_system.botnet_manager.show_botnet_market()

    def _cmd_buy_botnet(self, args: list) -> None:
        """Купить ботнет"""
        if not args:
            print(f"{XSSColors.ERROR}Укажите номер ботнета{XSSColors.RESET}")
            return

        try:
            botnet_index = int(args[0])
            network_system.botnet_manager.buy_botnet(botnet_index)
        except ValueError:
            print(f"{XSSColors.ERROR}Неверный номер ботнета{XSSColors.RESET}")

    def _cmd_ddos(self, args: list) -> None:
        """Запустить DDoS атаку"""
        if not args:
            print(f"{XSSColors.ERROR}Укажите цель для атаки{XSSColors.RESET}")
            return

        target = args[0]
        botnet_index = int(args[1]) if len(args) > 1 else None

        network_system.botnet_manager.launch_ddos(target, botnet_index)

    def _cmd_mission_status(self, args: list) -> None:
        """Подробный статус текущей миссии"""
        active_mission = game_state.get_stat("active_mission")
        if not active_mission:
            print(f"{XSSColors.WARNING}У вас нет активной миссии{XSSColors.RESET}")
            return

        mission_data = mission_system.missions.get(active_mission, {})
        mission_type = mission_data.get("type", "normal")

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ СТАТУС МИССИИ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")
        print(f"\n{XSSColors.WARNING}📋 {mission_data.get('name', active_mission)}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Тип: {mission_type}{XSSColors.RESET}")

        # Показываем временные ограничения
        if active_mission in mission_system.mission_timers:
            start_time, time_limit = mission_system.mission_timers[active_mission]
            elapsed = (time.time() - start_time) / 3600
            remaining = time_limit - elapsed

            if remaining > 0:
                color = XSSColors.SUCCESS if remaining > time_limit * 0.5 else XSSColors.WARNING if remaining > time_limit * 0.2 else XSSColors.ERROR
                print(f"⏰ Осталось времени: {color}{remaining:.1f} часов{XSSColors.RESET}")
            else:
                print(f"{XSSColors.ERROR}⏰ ВРЕМЯ ИСТЕКЛО!{XSSColors.RESET}")

        # Многоэтапные миссии
        if mission_type in ["multi_stage", "team_mission", "moral_choice"]:
            current_stage = game_state.get_stat("current_mission_stage", 0)
            stages = mission_data.get("stages", [])

            print(f"\n{XSSColors.INFO}📊 Прогресс:{XSSColors.RESET}")
            print(f"   Этап: {current_stage + 1}/{len(stages)}")

            if current_stage < len(stages):
                stage_data = stages[current_stage]
                print(f"   Текущий этап: {stage_data.get('name', 'Неизвестно')}")
                print(f"   Описание: {stage_data.get('desc', 'Нет описания')}")

        # Командные миссии
        if mission_type == "team_mission" and active_mission in mission_system.active_teams:
            team = mission_system.active_teams[active_mission]
            print(f"\n{XSSColors.SUCCESS}👥 КОМАНДА:{XSSColors.RESET}")
            for member in team.get("members", []):
                print(f"   • {member['name']} ({member['role']}) - Навык: {member['skill_level']}/10")

        # Активные события
        if active_mission in mission_system.mission_events:
            events = mission_system.mission_events[active_mission]
            print(f"\n{XSSColors.WARNING}⚡ АКТИВНЫЕ СОБЫТИЯ:{XSSColors.RESET}")
            for event in events:
                print(f"   • {event}")

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    def _cmd_team_status(self, args: list) -> None:
        """Показать статус команды"""
        active_mission = game_state.get_stat("active_mission")

        if not active_mission or active_mission not in mission_system.active_teams:
            print(f"{XSSColors.WARNING}У вас нет активной командной миссии{XSSColors.RESET}")
            return

        team = mission_system.active_teams[active_mission]
        mission_data = mission_system.missions.get(active_mission, {})

        print(f"\n{XSSColors.SUCCESS}━━━━━━━━━━━━━━━━ СТАТУС КОМАНДЫ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")
        print(f"\n{XSSColors.WARNING}Миссия: {mission_data.get('name', active_mission)}{XSSColors.RESET}")
        print(f"Размер команды: {len(team.get('members', []))}/{mission_data.get('team_size', 1)}")

        print(f"\n{XSSColors.INFO}👥 УЧАСТНИКИ:{XSSColors.RESET}")
        total_skill = 0
        for member in team.get("members", []):
            skill_color = XSSColors.SUCCESS if member['skill_level'] >= 7 else XSSColors.WARNING if member[
                                                                                                        'skill_level'] >= 4 else XSSColors.ERROR
            loyalty_color = XSSColors.SUCCESS if member['loyalty'] >= 70 else XSSColors.WARNING if member[
                                                                                                       'loyalty'] >= 40 else XSSColors.ERROR

            print(f"   • {member['name']}")
            print(f"     Роль: {member['role']}")
            print(f"     Навык: {skill_color}{member['skill_level']}/10{XSSColors.RESET}")
            print(f"     Лояльность: {loyalty_color}{member['loyalty']}%{XSSColors.RESET}")
            print(f"     Стоимость: {member['cost']} BTC/этап")

            total_skill += member['skill_level']

        avg_skill = total_skill / len(team.get("members", [1]))
        print(f"\n{XSSColors.INFO}📊 Общий уровень команды: {avg_skill:.1f}/10{XSSColors.RESET}")

        # Показываем синергию команды
        synergy = team.get("synergy", 50)
        synergy_color = XSSColors.SUCCESS if synergy >= 80 else XSSColors.WARNING if synergy >= 60 else XSSColors.ERROR
        print(f"🤝 Синергия команды: {synergy_color}{synergy}%{XSSColors.RESET}")

    def _cmd_abort_mission(self, args: list) -> None:
        """Прервать текущую миссию"""
        active_mission = game_state.get_stat("active_mission")
        if not active_mission:
            print(f"{XSSColors.WARNING}У вас нет активной миссии{XSSColors.RESET}")
            return

        mission_data = mission_system.missions.get(active_mission, {})

        print(f"\n{XSSColors.WARNING}⚠️ ПРЕРЫВАНИЕ МИССИИ{XSSColors.RESET}")
        print(f"Миссия: {mission_data.get('name', active_mission)}")
        print(f"\n{XSSColors.ERROR}Последствия прерывания:{XSSColors.RESET}")
        print("   • Потеря репутации (-15)")
        print("   • Увеличение Heat Level (+10%)")
        print("   • Потеря вложенных ресурсов")

        confirm = input(f"\n{XSSColors.PROMPT}Точно прервать миссию? (yes/no): {XSSColors.RESET}").lower()

        if confirm in ['yes', 'y']:
            # Применяем штрафы
            game_state.modify_stat("reputation", -15)
            game_state.modify_stat("heat_level", 10)

            # Штрафы для командных миссий
            if active_mission in mission_system.active_teams:
                team = mission_system.active_teams[active_mission]
                # Команда недовольна
                for member in team.get("members", []):
                    member["loyalty"] = max(0, member["loyalty"] - 30)
                print(f"{XSSColors.ERROR}[-] Лояльность команды снижена{XSSColors.RESET}")

            # Очищаем миссию
            game_state.set_stat("active_mission", None)
            game_state.set_stat("mission_progress", 0)
            game_state.set_stat("current_mission_stage", 0)

            # Очищаем таймеры и события
            if active_mission in mission_system.mission_timers:
                del mission_system.mission_timers[active_mission]
            if active_mission in mission_system.mission_events:
                del mission_system.mission_events[active_mission]
            if active_mission in mission_system.active_teams:
                del mission_system.active_teams[active_mission]

            print(f"\n{XSSColors.SUCCESS}Миссия прервана{XSSColors.RESET}")
        else:
            print(f"{XSSColors.INFO}Прерывание отменено{XSSColors.RESET}")

    def _cmd_show_mission_choices(self, args: list) -> None:
        """Показать сделанные моральные выборы"""
        choices = game_state.get_stat("moral_choices_made", {})

        if not choices:
            print(f"{XSSColors.INFO}Вы еще не делали моральных выборов в миссиях{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.STORY}━━━━━━━━━━━━━━━━ ВАШИ ВЫБОРЫ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        for mission_key, choice in choices.items():
            mission_name = mission_key.replace("mission_", "")
            print(f"\n{XSSColors.WARNING}📋 {mission_name}:{XSSColors.RESET}")
            print(f"   Выбор: {choice}")

        # Анализ морального профиля
        choice_values = list(choices.values())
        if choice_values:
            moral_profile = mission_system._analyze_moral_profile(choice_values)
            print(f"\n{XSSColors.INFO}🎭 Ваш моральный профиль: {moral_profile}{XSSColors.RESET}")

    def _cmd_recruit_team(self, args: list) -> None:
        """Набрать команду для миссии"""
        active_mission = game_state.get_stat("active_mission")
        if not active_mission:
            print(f"{XSSColors.ERROR}Сначала возьмите командную миссию{XSSColors.RESET}")
            return

        mission_data = mission_system.missions.get(active_mission, {})
        if mission_data.get("type") != "team_mission":
            print(f"{XSSColors.ERROR}Эта миссия не требует команды{XSSColors.RESET}")
            return

        if active_mission in mission_system.active_teams:
            print(f"{XSSColors.WARNING}У вас уже есть команда для этой миссии{XSSColors.RESET}")
            return

        mission_system._recruit_team(active_mission, mission_data)

    def _cmd_mission_statistics(self, args: list) -> None:
        """Показать статистику миссий"""
        mission_statistics.show_detailed_stats()

    def _cmd_show_notifications(self, args: list) -> None:
        """Показать активные уведомления"""
        mission_notifications.show_active_notifications()

    def _cmd_clear_notifications(self, args: list) -> None:
        """Очистить все уведомления"""
        mission_notifications.clear_all_notifications()

    def _cmd_mission_history(self, args: list) -> None:
        """Показать историю миссий"""
        history = mission_statistics.mission_history

        if not history:
            print(f"{XSSColors.INFO}История миссий пуста{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ ИСТОРИЯ МИССИЙ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Показываем последние 10 миссий
        recent_missions = history[-10:]

        for i, mission in enumerate(recent_missions, 1):
            success_icon = "✅" if mission.get("success") else "❌"
            status_color = XSSColors.SUCCESS if mission.get("success") else XSSColors.ERROR

            timestamp = datetime.fromtimestamp(mission["timestamp"]).strftime("%d.%m %H:%M")

            print(f"\n   {i}. {success_icon} {status_color}{mission['mission_id']}{XSSColors.RESET}")
            print(f"      Время: {timestamp}")

            if mission.get("success"):
                rewards = mission.get("rewards", {})
                if "btc" in rewards:
                    print(f"      Награда: {XSSColors.MONEY}{rewards['btc']} BTC{XSSColors.RESET}")
            else:
                print(f"      Причина провала: {mission.get('reason', 'Неизвестно')}")

        if len(history) > 10:
            print(f"\n{XSSColors.INFO}Показаны последние 10 из {len(history)} миссий{XSSColors.RESET}")

    def _cmd_team_details(self, args: list) -> None:
        """Показать подробности о команде"""
        active_mission = game_state.get_stat("active_mission")

        if not active_mission or active_mission not in mission_system.active_teams:
            print(f"{XSSColors.WARNING}У вас нет активной командной миссии{XSSColors.RESET}")
            return

        team = mission_system.active_teams[active_mission]
        mission_data = mission_system.missions.get(active_mission, {})

        print(f"\n{XSSColors.SUCCESS}━━━━━━━━━━━━━━━━ ДЕТАЛИ КОМАНДЫ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")
        print(f"\n{XSSColors.WARNING}Миссия: {mission_data.get('name', active_mission)}{XSSColors.RESET}")

        # Подробная информация о каждом участнике
        total_cost = 0
        total_skill = 0
        total_loyalty = 0

        for i, member in enumerate(team.get("members", []), 1):
            print(f"\n   {i}. {XSSColors.BRIGHT_GREEN}{member['name']}{XSSColors.RESET}")
            print(f"      🎭 Роль: {member['role']}")
            print(f"      🎯 Навык: {member['skill_level']}/10")
            print(f"      ❤️  Лояльность: {member['loyalty']}%")
            print(f"      💰 Стоимость: {member['cost']} BTC/этап")
            print(f"      ✨ Особенности: {member['traits']}")

            total_cost += member['cost']
            total_skill += member['skill_level']
            total_loyalty += member['loyalty']

        # Статистика команды
        member_count = len(team.get("members", []))
        if member_count > 0:
            avg_skill = total_skill / member_count
            avg_loyalty = total_loyalty / member_count

            print(f"\n{XSSColors.INFO}📊 СТАТИСТИКА КОМАНДЫ:{XSSColors.RESET}")
            print(f"   Средний навык: {avg_skill:.1f}/10")
            print(f"   Средняя лояльность: {avg_loyalty:.1f}%")
            print(f"   Общая стоимость: {total_cost} BTC/этап")
            print(f"   Синергия: {team.get('synergy', 0)}%")

    def _cmd_moral_profile(self, args: list) -> None:
        """Показать моральный профиль игрока"""
        choices = game_state.get_stat("moral_choices_made", {})

        if not choices:
            print(f"{XSSColors.INFO}Вы еще не делали моральных выборов{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.STORY}━━━━━━━━━━━━━━━━ МОРАЛЬНЫЙ ПРОФИЛЬ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Анализируем выборы
        choice_values = list(choices.values())
        moral_profile = mission_system._analyze_moral_profile(choice_values)

        # Определяем цвет профиля
        profile_colors = {
            "Праведник": XSSColors.SUCCESS,
            "Альтруист": XSSColors.SUCCESS,
            "Прагматик": XSSColors.WARNING,
            "Макиавеллист": XSSColors.ERROR,
            "Непредсказуемый": XSSColors.INFO
        }

        profile_color = profile_colors.get(moral_profile, XSSColors.INFO)

        print(f"\n{XSSColors.INFO}🎭 Ваш моральный профиль: {profile_color}{moral_profile}{XSSColors.RESET}")

        # Описания профилей
        profile_descriptions = {
            "Праведник": "Вы всегда выбираете путь справедливости и защиты невинных",
            "Альтруист": "Вы готовы жертвовать ради блага других",
            "Прагматик": "Вы принимаете решения основываясь на практической выгоде",
            "Макиавеллист": "Цель оправдывает средства - ваш главный принцип",
            "Непредсказуемый": "Ваши решения сложно предугадать"
        }

        description = profile_descriptions.get(moral_profile, "Ваш профиль уникален")
        print(f"\n{XSSColors.LIGHT_GRAY}{description}{XSSColors.RESET}")

        # Статистика выборов
        print(f"\n{XSSColors.INFO}📊 СТАТИСТИКА ВЫБОРОВ:{XSSColors.RESET}")
        print(f"   Всего решений: {len(choices)}")

        # Анализируем тенденции
        positive_choices = sum(
            1 for choice in choice_values if any(word in choice for word in ["protect", "help", "donate", "save"]))
        negative_choices = sum(
            1 for choice in choice_values if any(word in choice for word in ["steal", "abandon", "betray", "harm"]))

        if positive_choices > 0:
            print(f"   Альтруистических: {XSSColors.SUCCESS}{positive_choices}{XSSColors.RESET}")
        if negative_choices > 0:
            print(f"   Эгоистических: {XSSColors.ERROR}{negative_choices}{XSSColors.RESET}")

    def _cmd_test_event(self, args: list) -> None:
        """Тестовая команда для проверки событий (только для отладки)"""
        if not args:
            print(f"{XSSColors.ERROR}Укажите тип события для тестирования{XSSColors.RESET}")
            return

        event_type = args[0]
        active_mission = game_state.get_stat("active_mission")

        if not active_mission:
            print(f"{XSSColors.ERROR}Нет активной миссии для тестирования{XSSColors.RESET}")
            return

        # Тестовые события
        if event_type == "stage":
            mission_system.event_manager.trigger_event(
                "stage_completed",
                mission_id=active_mission,
                stage_name="Тестовый этап",
                stage_number=1,
                total_stages=3
            )
        elif event_type == "time":
            mission_system.event_manager.trigger_event(
                "time_warning",
                mission_id=active_mission,
                time_remaining=1.5,
                warning_level="critical"
            )
        elif event_type == "random":
            mission_system.event_manager.trigger_event(
                "random_event",
                mission_id=active_mission,
                event_type="security_upgrade",
                description="Система безопасности была обновлена!",
                effects={"risk_increase": 20}
            )
        else:
            print(f"{XSSColors.ERROR}Неизвестный тип события: {event_type}{XSSColors.RESET}")

    def _cmd_simulate_mission(self, args: list) -> None:
        """Симуляция завершения миссии (для тестирования)"""
        active_mission = game_state.get_stat("active_mission")

        if not active_mission:
            print(f"{XSSColors.ERROR}Нет активной миссии{XSSColors.RESET}")
            return

        mission_data = mission_system.missions.get(active_mission, {})

        # Симулируем награды
        test_rewards = {
            "btc": random.randint(100, 500),
            "reputation": random.randint(10, 30)
        }

        # Записываем в статистику
        mission_statistics.record_mission_completion(
            active_mission,
            mission_data,
            random.uniform(1.0, 5.0),  # Время выполнения
            test_rewards
        )

        # Применяем награды
        game_state.earn_currency(test_rewards["btc"], "btc_balance")
        game_state.modify_stat("reputation", test_rewards["reputation"])

        # Отмечаем как выполненную
        game_state.complete_mission(active_mission)
        game_state.set_stat("active_mission", None)

        print(f"{XSSColors.SUCCESS}✅ Миссия симулирована как завершенная{XSSColors.RESET}")
        print(f"Награды: {test_rewards['btc']} BTC, {test_rewards['reputation']} REP")

    # Добавить в метод _update_game_systems():

    def _update_game_systems(self) -> None:
        """Обновляет игровые системы с продвинутыми возможностями"""
        try:
            # Существующие обновления...
            market_system.update_special_offers()

            if random.random() < 0.05:
                market_system.generate_random_offer()

            crypto_system.update_crypto_prices()

            turn = game_state.get_stat('turn_number', 0)
            if turn % 5 == 0:
                game_state.decay_heat_level()

            # НОВОЕ: Обновления продвинутых систем
            if hasattr(self, 'mission_event_manager'):
                # Проверяем временные ограничения
                self.mission_event_manager.check_time_limits()

                # Обновляем уведомления
                mission_notifications.update_notifications()

                # Случайные события миссий
                if random.random() < 0.02:  # 2% шанс
                    self._trigger_random_mission_event()

        except Exception as e:
            print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Ошибка обновления продвинутых систем: {e}{XSSColors.RESET}")

    def _trigger_random_mission_event(self) -> None:
        """Запускает случайное событие миссии"""
        active_mission = game_state.get_stat("active_mission")
        if not active_mission:
            return

        # Список возможных событий
        random_events = [
            {
                "type": "competitor_interference",
                "description": "Другие хакеры пытаются помешать операции",
                "effects": {"risk_increase": 15}
            },
            {
                "type": "insider_help",
                "description": "Инсайдер предлагает помощь",
                "effects": {"risk_decrease": 20}
            },
            {
                "type": "security_alert",
                "description": "Системы безопасности повышают бдительность",
                "effects": {"heat_gain": 10}
            },
            {
                "type": "equipment_malfunction",
                "description": "Техническая неисправность замедляет операцию",
                "effects": {"time_pressure": True}
            },
            {
                "type": "opportunity_window",
                "description": "Неожиданная возможность ускорить операцию",
                "effects": {"bonus_progress": 1}
            }
        ]

        # Выбираем случайное событие
        event = random.choice(random_events)

        # Запускаем событие
        if hasattr(self, 'mission_event_manager'):
            self.mission_event_manager.trigger_event(
                "random_event",
                mission_id=active_mission,
                event_type=event["type"],
                description=event["description"],
                effects=event["effects"]
            )

    # Добавить в метод run() проверку уведомлений:

    def run(self) -> None:
        """Основной игровой цикл с поддержкой продвинутых миссий"""
        try:
            self.initialize()
        except Exception as e:
            print(f"{XSSColors.ERROR}❌ Не удалось инициализировать игру: {e}{XSSColors.RESET}")
            self._handle_critical_error(e)
            return

        consecutive_errors = 0
        max_consecutive_errors = 3

        while self.running:
            try:
                game_state.update_last_seen()
                turn = game_state.increment_turn()

                if self._check_game_over():
                    break

                # Системные обновления с защитой от ошибок
                try:
                    if turn % 5 == 0:
                        self._process_random_events()
                    if turn % 3 == 0:
                        network_system.update_network_state()

                    # НОВОЕ: Показываем важные уведомления
                    if hasattr(self, 'mission_event_manager') and turn % 2 == 0:
                        self._show_priority_notifications()

                except Exception as e:
                    print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Ошибка системного обновления: {e}{XSSColors.RESET}")

                prompt = self._get_dynamic_prompt()

                try:
                    user_input = command_completer.get_enhanced_input(prompt)
                except (EOFError, KeyboardInterrupt):
                    self._handle_interrupt()
                    break
                except Exception as e:
                    print(f"{XSSColors.ERROR}[ОШИБКА] Проблема с вводом: {e}{XSSColors.RESET}")
                    continue

                if not user_input:
                    continue

                command, args = smart_prompt.process_input(user_input, {})
                if command:
                    self._process_command(command, args)
                else:
                    smart_prompt.handle_unknown_command(user_input.split()[0] if user_input.split() else "")

                try:
                    self._update_game_systems()
                except Exception as e:
                    print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Ошибка обновления систем: {e}{XSSColors.RESET}")

                # Сброс счетчика ошибок при успешном выполнении
                consecutive_errors = 0

            except KeyboardInterrupt:
                self._handle_interrupt()
                break
            except Exception as e:
                consecutive_errors += 1
                print(f"\n{XSSColors.ERROR}[ОШИБКА] {e}{XSSColors.RESET}")

                if consecutive_errors >= max_consecutive_errors:
                    print(
                        f"{XSSColors.DANGER}[КРИТИЧНО] Слишком много ошибок подряд. Аварийное сохранение...{XSSColors.RESET}")
                    self._emergency_save()
                    break

                self._handle_runtime_error(e)

    def _show_priority_notifications(self) -> None:
        """Показывает приоритетные уведомления"""
        if not hasattr(self, 'mission_event_manager'):
            return

        # Показываем только высокоприоритетные уведомления
        high_priority = [n for n in mission_notifications.active_notifications
                         if n["priority"] == "high"]

        for notification in high_priority[:2]:  # Максимум 2 уведомления за раз
            mission_notifications._display_notification(notification)

    # Добавить метод для расширенной справки:

    def _cmd_advanced_help(self, args: list) -> None:
        """Расширенная справка по продвинутым миссиям"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ ПРОДВИНУТЫЕ МИССИИ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🎯 ТИПЫ МИССИЙ:{XSSColors.RESET}")
        print(f"   {XSSColors.INFO}multi_stage{XSSColors.RESET} - Многоэтапные операции")
        print(f"   {XSSColors.INFO}team_mission{XSSColors.RESET} - Командные задания")
        print(f"   {XSSColors.INFO}time_critical{XSSColors.RESET} - Миссии с дедлайном")
        print(f"   {XSSColors.INFO}moral_choice{XSSColors.RESET} - Моральные дилеммы")

        print(f"\n{XSSColors.WARNING}⚡ ОСОБЕННОСТИ:{XSSColors.RESET}")
        print(f"   • Случайные события могут изменить ход миссии")
        print(f"   • Команды требуют управления лояльностью")
        print(f"   • Моральные выборы влияют на репутацию")
        print(f"   • Временные ограничения добавляют напряжение")

        print(f"\n{XSSColors.INFO}📋 ПОЛЕЗНЫЕ КОМАНДЫ:{XSSColors.RESET}")
        print(f"   {XSSColors.WARNING}mission_status{XSSColors.RESET} - Подробный статус миссии")
        print(f"   {XSSColors.WARNING}team_details{XSSColors.RESET} - Информация о команде")
        print(f"   {XSSColors.WARNING}recruit{XSSColors.RESET} - Набор участников")
        print(f"   {XSSColors.WARNING}abort_mission{XSSColors.RESET} - Прервать миссию")
        print(f"   {XSSColors.WARNING}mission_stats{XSSColors.RESET} - Статистика выполнения")
        print(f"   {XSSColors.WARNING}moral_profile{XSSColors.RESET} - Моральный профиль")
        print(f"   {XSSColors.WARNING}notifications{XSSColors.RESET} - Активные уведомления")

        print(f"\n{XSSColors.STORY}🎭 СОВЕТЫ:{XSSColors.RESET}")
        print(f"   • Балансируйте состав команды по навыкам")
        print(f"   • Следите за лояльностью участников")
        print(f"   • Обращайте внимание на временные рамки")
        print(f"   • Моральные выборы влияют на концовку игры")
        print(f"   • Случайные события можно обратить в свою пользу")

    # Добавить сохранение статистики в методы save/load:

    def _cmd_save(self, args: list) -> None:
        """Сохранить игру с продвинутыми данными"""
        try:
            # Сохраняем основное состояние
            if game_state.save_game():
                # Сохраняем дополнительные данные
                if hasattr(self, 'mission_event_manager'):
                    self._save_advanced_data()
                print(f"{XSSColors.SUCCESS}✅ Игра сохранена{XSSColors.RESET}")
            else:
                print(f"{XSSColors.ERROR}❌ Ошибка сохранения{XSSColors.RESET}")
        except Exception as e:
            print(f"{XSSColors.ERROR}❌ Ошибка сохранения: {e}{XSSColors.RESET}")

    def _save_advanced_data(self) -> None:
        """Сохраняет данные продвинутых систем"""
        try:
            advanced_data = {
                "mission_statistics": mission_statistics.stats,
                "mission_history": mission_statistics.mission_history,
                "active_teams": mission_system.active_teams,
                "mission_timers": mission_system.mission_timers,
                "mission_events": mission_system.mission_events
            }

            with open("advanced_save.json", "w", encoding="utf-8") as f:
                json.dump(advanced_data, f, indent=2, default=str)

        except Exception as e:
            print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Не удалось сохранить продвинутые данные: {e}{XSSColors.RESET}")

    def _cmd_load(self, args: list) -> None:
        """Загрузить игру с продвинутыми данными"""
        if os.path.exists("xss_save.json"):
            if game_state.load_game():
                # Загружаем дополнительные данные
                if hasattr(self, 'mission_event_manager'):
                    self._load_advanced_data()
                print(f"{XSSColors.SUCCESS}✅ Игра загружена{XSSColors.RESET}")
        else:
            print(f"{XSSColors.ERROR}Файл сохранения не найден{XSSColors.RESET}")

    def _load_advanced_data(self) -> None:
        """Загружает данные продвинутых систем"""
        try:
            if os.path.exists("advanced_save.json"):
                with open("advanced_save.json", "r", encoding="utf-8") as f:
                    advanced_data = json.load(f)

                # Восстанавливаем статистику
                if "mission_statistics" in advanced_data:
                    mission_statistics.stats.update(advanced_data["mission_statistics"])

                if "mission_history" in advanced_data:
                    mission_statistics.mission_history = advanced_data["mission_history"]

                # Восстанавливаем активные миссии
                if "active_teams" in advanced_data:
                    mission_system.active_teams.update(advanced_data["active_teams"])

                if "mission_timers" in advanced_data:
                    mission_system.mission_timers.update(advanced_data["mission_timers"])

                if "mission_events" in advanced_data:
                    mission_system.mission_events.update(advanced_data["mission_events"])

                print(f"{XSSColors.SUCCESS}✅ Продвинутые данные загружены{XSSColors.RESET}")

        except Exception as e:
            print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Не удалось загрузить продвинутые данные: {e}{XSSColors.RESET}")


def main():
    """Главная функция с улучшенной обработкой ошибок"""
    try:
        # Проверяем зависимости
        required_modules = ['colorama']
        missing_modules = []

        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)

        if missing_modules:
            print(f"[!] Отсутствуют необходимые модули: {', '.join(missing_modules)}")
            print(f"[!] Установите их командой: pip install {' '.join(missing_modules)}")
            return

        # Запускаем игру
        game = XSSGame()
        game.run()

    except KeyboardInterrupt:
        print(f"\n{XSSColors.WARNING}Игра прервана пользователем.{XSSColors.RESET}")
    except Exception as e:
        print(f"{XSSColors.ERROR}❌ Критическая ошибка: {e}{XSSColors.RESET}")

        # Сохраняем подробный лог
        import traceback
        with open("crash_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"Crash at {datetime.now()}\n")
            f.write(f"Error: {e}\n")
            f.write(f"Traceback:\n{traceback.format_exc()}\n")
            f.write(f"{'=' * 60}\n")

        print(f"{XSSColors.INFO}Подробности сохранены в crash_log.txt{XSSColors.RESET}")

if __name__ == "__main__":
    main()