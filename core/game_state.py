"""
Управление состоянием игрока и сохранениями
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

from config.settings import INITIAL_PLAYER_STATE, GAME_SETTINGS
from ui.colors import XSSColors  # Изменено с Colors на XSSColors


class GameState:
    """Класс для управления состоянием игры"""

    def __init__(self):
        self.player_stats = INITIAL_PLAYER_STATE.copy()
        self._initialize_nested_dicts()

    def _initialize_nested_dicts(self):
        """Инициализирует вложенные словари если они отсутствуют"""
        if 'skills' not in self.player_stats:
            self.player_stats['skills'] = INITIAL_PLAYER_STATE['skills'].copy()
        if 'story_choices' not in self.player_stats:
            self.player_stats['story_choices'] = {}
        # Добавляем поля для сетевой системы
        if 'current_node' not in self.player_stats:
            self.player_stats['current_node'] = 'localhost'
        if 'network_nodes' not in self.player_stats:
            self.player_stats['network_nodes'] = {}

    def get_stat(self, key: str, default: Any = None) -> Any:
        """Получить статистику игрока"""
        return self.player_stats.get(key, default)

    def set_stat(self, key: str, value: Any) -> None:
        """Установить статистику игрока"""
        self.player_stats[key] = value

    def modify_stat(self, key: str, change: float) -> float:
        """Изменить статистику на указанное значение"""
        current = self.get_stat(key, 0)
        new_value = current + change
        self.set_stat(key, new_value)
        return new_value

    def get_skill(self, skill: str) -> int:
        """Получить уровень навыка"""
        return self.player_stats.get('skills', {}).get(skill, 0)

    def set_skill(self, skill: str, level: int) -> None:
        """Установить уровень навыка"""
        if 'skills' not in self.player_stats:
            self.player_stats['skills'] = {}
        self.player_stats['skills'][skill] = max(0, min(10, level))

    def modify_skill(self, skill: str, change: int) -> int:
        """Изменить навык на указанное значение"""
        current = self.get_skill(skill)
        new_level = max(0, min(10, current + change))
        self.set_skill(skill, new_level)
        return new_level

    def add_to_inventory(self, item_id: str) -> bool:
        """Добавить предмет в инвентарь"""
        if 'inventory' not in self.player_stats:
            self.player_stats['inventory'] = []

        if item_id not in self.player_stats['inventory']:
            self.player_stats['inventory'].append(item_id)
            return True
        return False

    def remove_from_inventory(self, item_id: str) -> bool:
        """Удалить предмет из инвентаря"""
        if 'inventory' in self.player_stats and item_id in self.player_stats['inventory']:
            self.player_stats['inventory'].remove(item_id)
            return True
        return False

    def has_item(self, item_id: str) -> bool:
        """Проверить наличие предмета в инвентаре"""
        return item_id in self.player_stats.get('inventory', [])

    def add_contact(self, contact_id: str) -> bool:
        """Добавить контакт"""
        if 'contacts' not in self.player_stats:
            self.player_stats['contacts'] = []

        if contact_id not in self.player_stats['contacts']:
            self.player_stats['contacts'].append(contact_id)
            return True
        return False

    def has_contact(self, contact_id: str) -> bool:
        """Проверить наличие контакта"""
        return contact_id in self.player_stats.get('contacts', [])

    def complete_mission(self, mission_id: str) -> None:
        """Отметить миссию как выполненную"""
        if 'completed_missions' not in self.player_stats:
            self.player_stats['completed_missions'] = []

        if mission_id not in self.player_stats['completed_missions']:
            self.player_stats['completed_missions'].append(mission_id)

    def decay_heat_level(self) -> None:
        """Постепенное снижение heat level со временем"""
        current_heat = self.get_stat("heat_level", 0)
        if current_heat > 0:
            # Снижаем на 1-3% за ход, но медленнее при высоком уровне
            decay_rate = 3 if current_heat < 30 else 2 if current_heat < 70 else 1
            new_heat = max(0, current_heat - decay_rate)
            self.set_stat("heat_level", new_heat)

    def is_mission_completed(self, mission_id: str) -> bool:
        """Проверить выполнена ли миссия"""
        return mission_id in self.player_stats.get('completed_missions', [])

    def add_achievement(self, achievement_id: str) -> bool:
        """Добавить достижение"""
        if 'achievements' not in self.player_stats:
            self.player_stats['achievements'] = []

        if achievement_id not in self.player_stats['achievements']:
            self.player_stats['achievements'].append(achievement_id)
            return True
        return False

    def has_achievement(self, achievement_id: str) -> bool:
        """Проверить наличие достижения"""
        return achievement_id in self.player_stats.get('achievements', [])

    def set_story_choice(self, choice_key: str, value: Any) -> None:
        """Сохранить выбор в сюжете"""
        if 'story_choices' not in self.player_stats:
            self.player_stats['story_choices'] = {}
        self.player_stats['story_choices'][choice_key] = value

    def get_story_choice(self, choice_key: str, default: Any = None) -> Any:
        """Получить выбор в сюжете"""
        return self.player_stats.get('story_choices', {}).get(choice_key, default)

    def update_last_seen(self) -> None:
        """Обновить время последнего визита"""
        self.player_stats['last_seen'] = datetime.now().strftime("%H:%M")

    def increment_turn(self) -> int:
        """Увеличить счетчик ходов"""
        current = self.get_stat('turn_number', 0)
        new_turn = current + 1
        self.set_stat('turn_number', new_turn)
        return new_turn

    def can_afford(self, cost: float, currency: str = 'btc_balance') -> bool:
        """Проверить может ли игрок позволить себе покупку"""
        balance = self.get_stat(currency, 0)
        return balance >= cost

    def spend_currency(self, amount: float, currency: str = 'btc_balance') -> bool:
        """Потратить валюту"""
        if self.can_afford(amount, currency):
            current = self.get_stat(currency, 0)
            self.set_stat(currency, current - amount)
            return True
        return False

    def earn_currency(self, amount: float, currency: str = 'btc_balance') -> None:
        """Заработать валюту"""
        current = self.get_stat(currency, 0)
        self.set_stat(currency, current + amount)

    def save_game(self, filename: Optional[str] = None) -> bool:
        """Сохранить игру с улучшенной обработкой ошибок"""
        filename = filename or GAME_SETTINGS['save_file']

        try:
            save_data = {
                "player_stats": self.player_stats,
                "save_timestamp": datetime.now().isoformat(),
                "game_version": "0.3.8"
            }

            # Сохраняем состояние сети с обработкой ошибок
            try:
                from systems.network import network_system
                network_state = network_system.save_network_state()
                save_data["network_state"] = network_state
            except ImportError:
                print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Модуль network недоступен{XSSColors.RESET}")
                pass
            except Exception as e:
                print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Не удалось сохранить состояние сети: {e}{XSSColors.RESET}")
                # Продолжаем сохранение без сетевого состояния
                pass

            # Создаем резервную копию если файл существует
            if os.path.exists(filename):
                try:
                    backup_name = f"{filename}.backup"
                    import shutil
                    shutil.copy2(filename, backup_name)
                except Exception as e:
                    print(
                        f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Не удалось создать резервную копию: {e}{XSSColors.RESET}")

            # Сохраняем во временный файл, затем переименовываем (атомарность)
            temp_filename = f"{filename}.tmp"

            # Используем custom JSON encoder для обработки сложных объектов
            import json

            class GameJSONEncoder(json.JSONEncoder):
                def default(self, obj):
                    # Если объект имеет метод to_dict, используем его
                    if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
                        return obj.to_dict()
                    # Для других неподдерживаемых объектов возвращаем строковое представление
                    try:
                        return super().default(obj)
                    except TypeError:
                        return str(obj)

            with open(temp_filename, "w", encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2, cls=GameJSONEncoder)

            # Атомарное переименование
            if os.name == 'nt':  # Windows
                if os.path.exists(filename):
                    os.remove(filename)
            os.rename(temp_filename, filename)

            print(f"{XSSColors.SUCCESS}[СИСТЕМА] Игра сохранена успешно!{XSSColors.RESET}")
            return True

        except PermissionError:
            print(f"{XSSColors.ERROR}[ОШИБКА] Нет прав на запись в файл {filename}{XSSColors.RESET}")
            return False
        except OSError as e:
            print(f"{XSSColors.ERROR}[ОШИБКА] Проблема с файловой системой: {e}{XSSColors.RESET}")
            return False
        except Exception as e:
            print(f"{XSSColors.ERROR}[ОШИБКА] Не удалось сохранить игру: {e}{XSSColors.RESET}")

            # Попытка упрощенного сохранения только основных данных игрока
            try:
                simple_save_data = {
                    "player_stats": self.player_stats,
                    "save_timestamp": datetime.now().isoformat(),
                    "game_version": "0.3.8"
                }

                with open(f"{filename}.simple", "w", encoding='utf-8') as f:
                    json.dump(simple_save_data, f, ensure_ascii=False, indent=2, default=str)

                print(f"{XSSColors.WARNING}[РЕЗЕРВ] Создано упрощенное сохранение: {filename}.simple{XSSColors.RESET}")
                return True

            except Exception as simple_error:
                print(
                    f"{XSSColors.ERROR}[КРИТИЧНО] Упрощенное сохранение тоже не удалось: {simple_error}{XSSColors.RESET}")
                return False

    def load_game(self, filename: Optional[str] = None) -> bool:
        """Загрузить игру"""
        filename = filename or GAME_SETTINGS['save_file']

        try:
            if not os.path.exists(filename):
                # Попробуем загрузить упрощенное сохранение
                simple_filename = f"{filename}.simple"
                if os.path.exists(simple_filename):
                    print(f"{XSSColors.WARNING}[СИСТЕМА] Загружается упрощенное сохранение{XSSColors.RESET}")
                    filename = simple_filename
                else:
                    print(f"{XSSColors.WARNING}[СИСТЕМА] Сохранение не найдено{XSSColors.RESET}")
                    return False

            with open(filename, "r", encoding='utf-8') as f:
                save_data = json.load(f)

            # Проверяем версию сохранения
            saved_version = save_data.get("game_version", "unknown")
            if saved_version not in ["0.3.0", "0.3.1", "0.3.8"]:
                print(f"{XSSColors.WARNING}[СИСТЕМА] Сохранение от другой версии: {saved_version}{XSSColors.RESET}")

            # Загружаем данные с проверкой целостности
            loaded_stats = save_data.get("player_stats", {})

            # Объединяем с базовым состоянием чтобы добавить новые поля
            self.player_stats = INITIAL_PLAYER_STATE.copy()
            self.player_stats.update(loaded_stats)

            # Убеждаемся что все навыки существуют
            for skill in INITIAL_PLAYER_STATE['skills']:
                if skill not in self.player_stats['skills']:
                    self.player_stats['skills'][skill] = 1

            # Добавляем новые поля если их нет
            if 'current_node' not in self.player_stats:
                self.player_stats['current_node'] = 'localhost'
            if 'network_nodes' not in self.player_stats:
                self.player_stats['network_nodes'] = {}

            # Загружаем состояние сети если есть
            if "network_state" in save_data:
                try:
                    from systems.network import network_system
                    network_system.load_network_state(save_data["network_state"])
                except ImportError:
                    print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Модуль network недоступен{XSSColors.RESET}")
                except Exception as e:
                    print(f"{XSSColors.WARNING}[ПРЕДУПРЕЖДЕНИЕ] Ошибка загрузки сети: {e}{XSSColors.RESET}")

            print(f"{XSSColors.SUCCESS}[СИСТЕМА] Игра загружена успешно!{XSSColors.RESET}")
            return True

        except Exception as e:
            print(f"{XSSColors.ERROR}[ОШИБКА] Не удалось загрузить игру: {e}{XSSColors.RESET}")
            return False

    def reset_game(self) -> None:
        """Сбросить игру к начальному состоянию"""
        self.player_stats = INITIAL_PLAYER_STATE.copy()
        self._initialize_nested_dicts()
        print(f"{XSSColors.WARNING}[СИСТЕМА] Игра сброшена к начальному состоянию{XSSColors.RESET}")

    def get_portfolio_value(self, crypto_prices: Dict[str, float]) -> float:
        """Получить общую стоимость портфеля"""
        total_value = self.get_stat('usd_balance', 0)

        # Добавляем BTC
        btc_value = self.get_stat('btc_balance', 0) * crypto_prices.get('BTC', 0)
        total_value += btc_value

        # Добавляем другие криптовалюты
        for symbol in ['ETH', 'LTC', 'XRP', 'DOGE']:
            amount = self.get_stat(symbol, 0)
            price = crypto_prices.get(symbol, 0)
            total_value += amount * price

        return total_value

    def get_summary(self) -> Dict[str, Any]:
        """Получить краткую сводку состояния"""
        return {
            'username': self.get_stat('username', 'unknown'),
            'reputation': self.get_stat('reputation', 0),
            'btc_balance': self.get_stat('btc_balance', 0),
            'faction': self.get_stat('faction', None),
            'story_stage': self.get_stat('story_stage', 0),
            'warnings': self.get_stat('warnings', 0),
            'heat_level': self.get_stat('heat_level', 0),
            'active_mission': self.get_stat('active_mission', None),
            'completed_missions': len(self.get_stat('completed_missions', [])),
            'achievements': len(self.get_stat('achievements', [])),
            'inventory_size': len(self.get_stat('inventory', [])),
            'current_node': self.get_stat('current_node', 'localhost')  # Добавлено
        }


# Глобальный экземпляр состояния игры
game_state = GameState()