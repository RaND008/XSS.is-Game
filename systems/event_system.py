import collections
from typing import Callable, Any, Dict, Type
import time
from ui.colors import XSSColors
from core.game_state import game_state
class Event:
    """Базовый класс для всех событий в игре."""
    def __init__(self, event_type: str, data: Dict[str, Any] = None):
        self.event_type = event_type
        self.data = data if data is not None else {}

    def __repr__(self):
        return f"<{self.event_type} Event: {self.data}>"

# --- Примеры конкретных типов событий ---
class MissionCompletedEvent(Event):
    """Событие завершения миссии."""
    def __init__(self, mission_id: str, reward_btc: int, reward_exp: int, heat_gain: int):
        super().__init__("MissionCompleted", {
            "mission_id": mission_id,
            "reward_btc": reward_btc,
            "reward_exp": reward_exp,
            "heat_gain": heat_gain
        })

class NodeCompromisedEvent(Event):
    """Событие компрометации сетевого узла."""
    def __init__(self, node_address: str, node_name: str, security_level: int):
        super().__init__("NodeCompromised", {
            "node_address": node_address,
            "node_name": node_name,
            "security_level": security_level
        })

class CryptoMarketChangeEvent(Event):
    """Событие значительного изменения на крипто-рынке."""
    def __init__(self, symbol: str, old_price: float, new_price: float, change_percent: float):
        super().__init__("CryptoMarketChange", {
            "symbol": symbol,
            "old_price": old_price,
            "new_price": new_price,
            "change_percent": change_percent
        })

class PlayerNotificationEvent(Event):
    """Событие для отображения уведомления игроку."""
    def __init__(self, message: str, message_type: str = "info", duration: float = 3.0):
        super().__init__("PlayerNotification", {
            "message": message,
            "message_type": message_type, # e.g., "info", "warning", "success", "error"
            "duration": duration
        })

class EventSystem:
    """Центральный диспетчер событий."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventSystem, cls).__new__(cls)
            cls._instance._listeners = collections.defaultdict(list)
        return cls._instance

    def register_listener(self, event_type: Type[Event], listener: Callable[[Event], None]):
        """Регистрирует слушателя для определенного типа события."""
        if not issubclass(event_type, Event):
            raise ValueError("event_type должен быть подклассом Event")
        self._listeners[event_type].append(listener)
        # print(f"[EventSystem] Слушатель {listener.__name__} зарегистрирован для {event_type.__name__}")

    def unregister_listener(self, event_type: Type[Event], listener: Callable[[Event], None]):
        """Отменяет регистрацию слушателя."""
        if listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)
            # print(f"[EventSystem] Слушатель {listener.__name__} отменен для {event_type.__name__}")

    def dispatch(self, event: Event):
        """Отправляет событие всем зарегистрированным слушателям."""
        # print(f"[EventSystem] Отправка события: {event}")
        for listener in self._listeners[type(event)]:
            try:
                listener(event)
            except Exception as e:
                print(f"[{event.event_type} EventSystem ERROR] Ошибка в слушателе {listener.__name__}: {e}")


"""
Система событий и уведомлений для продвинутых миссий
Добавляем в event_system.py
"""


# Новые типы событий для миссий

class MissionStageCompletedEvent(Event):
    """Событие завершения этапа миссии"""

    def __init__(self, mission_id: str, stage_name: str, stage_number: int, total_stages: int):
        super().__init__("MissionStageCompleted", {
            "mission_id": mission_id,
            "stage_name": stage_name,
            "stage_number": stage_number,
            "total_stages": total_stages
        })


class TeamMemberRecruitedEvent(Event):
    """Событие найма участника команды"""

    def __init__(self, mission_id: str, member_name: str, role: str, skill_level: int):
        super().__init__("TeamMemberRecruited", {
            "mission_id": mission_id,
            "member_name": member_name,
            "role": role,
            "skill_level": skill_level
        })


class MoralChoiceMadeEvent(Event):
    """Событие морального выбора"""

    def __init__(self, mission_id: str, choice_id: str, reputation_impact: int):
        super().__init__("MoralChoiceMade", {
            "mission_id": mission_id,
            "choice_id": choice_id,
            "reputation_impact": reputation_impact
        })


class MissionTimeWarningEvent(Event):
    """Предупреждение о времени миссии"""

    def __init__(self, mission_id: str, time_remaining: float, warning_level: str):
        super().__init__("MissionTimeWarning", {
            "mission_id": mission_id,
            "time_remaining": time_remaining,
            "warning_level": warning_level  # "low", "critical", "expired"
        })


class RandomMissionEvent(Event):
    """Случайное событие во время миссии"""

    def __init__(self, mission_id: str, event_type: str, description: str, effects: dict):
        super().__init__("RandomMissionEvent", {
            "mission_id": mission_id,
            "event_type": event_type,
            "description": description,
            "effects": effects
        })


class TeamSynergyChangedEvent(Event):
    """Изменение синергии команды"""

    def __init__(self, mission_id: str, old_synergy: int, new_synergy: int, reason: str):
        super().__init__("TeamSynergyChanged", {
            "mission_id": mission_id,
            "old_synergy": old_synergy,
            "new_synergy": new_synergy,
            "reason": reason
        })


# Обработчики событий для UI и логики

def handle_mission_stage_completed(event: Event):
    """Обработчик завершения этапа миссии"""
    from ui.effects import show_stage_completion_visual
    from systems.audio import audio_system

    data = event.data
    show_stage_completion_visual(
        data["stage_name"],
        data["stage_number"],
        data["total_stages"]
    )

    audio_system.play_sound("stage_complete")


def handle_team_member_recruited(event: Event):
    """Обработчик найма участника команды"""
    from ui.colors import XSSColors

    data = event.data
    skill_color = XSSColors.SUCCESS if data["skill_level"] >= 7 else XSSColors.WARNING

    print(f"\n{XSSColors.SUCCESS}👥 В команду принят: {data['member_name']}{XSSColors.RESET}")
    print(f"   Роль: {data['role']}")
    print(f"   Навык: {skill_color}{data['skill_level']}/10{XSSColors.RESET}")


def handle_moral_choice_made(event: Event):
    """Обработчик морального выбора"""
    from ui.colors import XSSColors
    from systems.audio import audio_system

    data = event.data
    impact = data["reputation_impact"]

    if impact > 0:
        print(f"{XSSColors.SUCCESS}⚖️ Ваш выбор повысил вашу репутацию{XSSColors.RESET}")
        audio_system.play_sound("reputation_gain")
    elif impact < 0:
        print(f"{XSSColors.ERROR}⚖️ Ваш выбор понизил вашу репутацию{XSSColors.RESET}")
        audio_system.play_sound("reputation_loss")
    else:
        print(f"{XSSColors.INFO}⚖️ Ваш выбор не повлиял на репутацию{XSSColors.RESET}")


def handle_mission_time_warning(event: Event):
    """Обработчик предупреждений о времени"""
    from ui.colors import XSSColors
    from ui.effects import pulse_text
    from systems.audio import audio_system

    data = event.data
    warning_level = data["warning_level"]
    time_remaining = data["time_remaining"]

    if warning_level == "critical":
        pulse_text(f"⏰ КРИТИЧЕСКОЕ ВРЕМЯ: {time_remaining:.1f}ч!", XSSColors.ERROR, 3)
        audio_system.play_sound("alert")
    elif warning_level == "low":
        print(f"{XSSColors.WARNING}⚠️ Мало времени: {time_remaining:.1f}ч{XSSColors.RESET}")
        audio_system.play_sound("warning")
    elif warning_level == "expired":
        pulse_text("⏰ ВРЕМЯ ИСТЕКЛО!", XSSColors.ERROR, 5)
        audio_system.play_sound("fail")


def handle_random_mission_event(event: Event):
    """Обработчик случайных событий"""
    from ui.effects import show_mission_event_visual
    from systems.audio import audio_system

    show_mission_event_visual(event.data)
    audio_system.play_sound("event")


def handle_team_synergy_changed(event: Event):
    """Обработчик изменения синергии команды"""
    from ui.colors import XSSColors

    data = event.data
    old_synergy = data["old_synergy"]
    new_synergy = data["new_synergy"]
    reason = data["reason"]

    if new_synergy > old_synergy:
        color = XSSColors.SUCCESS
        arrow = "↗️"
    elif new_synergy < old_synergy:
        color = XSSColors.ERROR
        arrow = "↘️"
    else:
        color = XSSColors.INFO
        arrow = "➡️"

    print(f"\n{color}🤝 Синергия команды: {old_synergy}% {arrow} {new_synergy}%{XSSColors.RESET}")
    print(f"   Причина: {reason}")


def handle_crypto_market_change(event: Event):
    """Обработчик изменений криптовалютного рынка"""
    from ui.colors import XSSColors
    from systems.audio import audio_system

    data = event.data
    symbol = data["symbol"]
    change_percent = data["change_percent"]
    old_price = data["old_price"]
    new_price = data["new_price"]

    # Показываем только значительные изменения (больше 10%)
    if abs(change_percent) > 10:
        if change_percent > 0:
            color = XSSColors.SUCCESS
            icon = "📈"
            direction = "РОСТ"
            try:
                audio_system.play_sound("coin")
            except:
                pass  # Игнорируем ошибки звука
        else:
            color = XSSColors.ERROR
            icon = "📉"
            direction = "ПАДЕНИЕ"
            try:
                audio_system.play_sound("warning")
            except:
                pass  # Игнорируем ошибки звука

        print(f"\n{color}{icon} КРИПТО СОБЫТИЕ: {symbol} {direction} {abs(change_percent):.1f}%{XSSColors.RESET}")
        print(f"   Цена: ${old_price:.2f} → ${new_price:.2f}")

    # Для очень больших изменений (>20%) показываем дополнительную информацию
    if abs(change_percent) > 20:
        if change_percent > 0:
            print(f"   {XSSColors.SUCCESS}💰 Отличное время для продажи!{XSSColors.RESET}")
        else:
            print(f"   {XSSColors.WARNING}🛒 Возможность для покупки на низах!{XSSColors.RESET}")

# Регистрация обработчиков событий
def register_mission_event_handlers():
    """Регистрирует все обработчики событий миссий"""
    event_system.register_listener(MissionStageCompletedEvent, handle_mission_stage_completed)
    event_system.register_listener(TeamMemberRecruitedEvent, handle_team_member_recruited)
    event_system.register_listener(MoralChoiceMadeEvent, handle_moral_choice_made)
    event_system.register_listener(MissionTimeWarningEvent, handle_mission_time_warning)
    event_system.register_listener(RandomMissionEvent, handle_random_mission_event)
    event_system.register_listener(TeamSynergyChangedEvent, handle_team_synergy_changed)
    event_system.register_listener(CryptoMarketChangeEvent, handle_crypto_market_change)


# Система уведомлений для миссий
class MissionNotificationSystem:
    """Система уведомлений для миссий"""

    def __init__(self):
        self.active_notifications = []
        self.notification_history = []

    def add_notification(self, notification_type: str, message: str,
                         priority: str = "normal", duration: int = 10):
        """Добавляет уведомление"""
        notification = {
            "type": notification_type,
            "message": message,
            "priority": priority,
            "timestamp": time.time(),
            "duration": duration,
            "id": len(self.notification_history)
        }

        self.active_notifications.append(notification)
        self.notification_history.append(notification)

        # Показываем уведомление немедленно для высокого приоритета
        if priority == "high":
            self._display_notification(notification)

    def _display_notification(self, notification):
        """Отображает уведомление"""
        from ui.colors import XSSColors

        priority_colors = {
            "low": XSSColors.INFO,
            "normal": XSSColors.WARNING,
            "high": XSSColors.ERROR
        }

        type_icons = {
            "mission": "📋",
            "team": "👥",
            "time": "⏰",
            "event": "⚡",
            "choice": "⚖️"
        }

        color = priority_colors.get(notification["priority"], XSSColors.INFO)
        icon = type_icons.get(notification["type"], "ℹ️")

        print(f"\n{color}┌─ УВЕДОМЛЕНИЕ ─┐{XSSColors.RESET}")
        print(f"{color}│ {icon} {notification['message']:<20} │{XSSColors.RESET}")
        print(f"{color}└─────────────────┘{XSSColors.RESET}")

    def update_notifications(self):
        """Обновляет активные уведомления"""
        current_time = time.time()

        # Удаляем устаревшие уведомления
        self.active_notifications = [
            n for n in self.active_notifications
            if current_time - n["timestamp"] < n["duration"]
        ]

    def show_active_notifications(self):
        """Показывает все активные уведомления"""
        from ui.colors import XSSColors

        if not self.active_notifications:
            print(f"{XSSColors.INFO}Нет активных уведомлений{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ АКТИВНЫЕ УВЕДОМЛЕНИЯ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        for notification in sorted(self.active_notifications, key=lambda x: x["priority"], reverse=True):
            self._display_notification(notification)

    def clear_all_notifications(self):
        """Очищает все уведомления"""
        self.active_notifications.clear()
        print(f"{XSSColors.SUCCESS}✅ Все уведомления очищены{XSSColors.RESET}")


# Глобальный экземпляр системы уведомлений
mission_notifications = MissionNotificationSystem()


# Интеграция с системой миссий
class MissionEventManager:
    """Менеджер событий для миссий"""

    def __init__(self, mission_system):
        self.mission_system = mission_system
        self.event_handlers = {}
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        """Настраивает обработчики событий"""
        self.event_handlers = {
            "stage_completed": self._handle_stage_completed,
            "team_recruited": self._handle_team_recruited,
            "moral_choice": self._handle_moral_choice,
            "time_warning": self._handle_time_warning,
            "random_event": self._handle_random_event,
            "mission_failed": self._handle_mission_failed,
            "mission_completed": self._handle_mission_completed
        }

    def trigger_event(self, event_type: str, **kwargs):
        """Запускает событие"""
        if event_type in self.event_handlers:
            self.event_handlers[event_type](**kwargs)

        # Отправляем событие через глобальную систему событий
        self._dispatch_global_event(event_type, **kwargs)

    def _dispatch_global_event(self, event_type: str, **kwargs):
        """Отправляет событие через глобальную систему"""
        event_classes = {
            "stage_completed": MissionStageCompletedEvent,
            "team_recruited": TeamMemberRecruitedEvent,
            "moral_choice": MoralChoiceMadeEvent,
            "time_warning": MissionTimeWarningEvent,
            "random_event": RandomMissionEvent,
            "synergy_changed": TeamSynergyChangedEvent
        }

        if event_type in event_classes:
            event_class = event_classes[event_type]
            event = event_class(**kwargs)
            event_system.dispatch(event)

    def _handle_stage_completed(self, mission_id: str, stage_name: str,
                                stage_number: int, total_stages: int):
        """Обрабатывает завершение этапа"""
        mission_notifications.add_notification(
            "mission",
            f"Этап '{stage_name}' завершен",
            "normal"
        )

        # Проверяем прогресс миссии
        if stage_number + 1 >= total_stages:
            mission_notifications.add_notification(
                "mission",
                "Все этапы завершены! Миссия готова к финализации",
                "high"
            )

    def _handle_team_recruited(self, mission_id: str, member_name: str,
                               role: str, skill_level: int):
        """Обрабатывает найм участника команды"""
        mission_notifications.add_notification(
            "team",
            f"{member_name} ({role}) присоединился к команде",
            "normal"
        )

    def _handle_moral_choice(self, mission_id: str, choice_id: str,
                             reputation_impact: int):
        """Обрабатывает моральный выбор"""
        if abs(reputation_impact) >= 20:
            priority = "high"
        elif abs(reputation_impact) >= 10:
            priority = "normal"
        else:
            priority = "low"

        impact_text = "повысил" if reputation_impact > 0 else "понизил"
        mission_notifications.add_notification(
            "choice",
            f"Моральный выбор {impact_text} репутацию",
            priority
        )

    def _handle_time_warning(self, mission_id: str, time_remaining: float,
                             warning_level: str):
        """Обрабатывает предупреждения о времени"""
        priority_map = {
            "low": "normal",
            "critical": "high",
            "expired": "high"
        }

        mission_notifications.add_notification(
            "time",
            f"Времени осталось: {time_remaining:.1f}ч",
            priority_map.get(warning_level, "normal")
        )

    def _handle_random_event(self, mission_id: str, event_type: str,
                             description: str, effects: dict):
        """Обрабатывает случайные события"""
        mission_notifications.add_notification(
            "event",
            f"Событие: {description}",
            "high"
        )

    def _handle_mission_failed(self, mission_id: str, reason: str):
        """Обрабатывает провал миссии"""
        mission_notifications.add_notification(
            "mission",
            f"Миссия провалена: {reason}",
            "high",
            duration=30
        )

    def _handle_mission_completed(self, mission_id: str, rewards: dict):
        """Обрабатывает завершение миссии"""
        mission_notifications.add_notification(
            "mission",
            "Миссия успешно завершена!",
            "high",
            duration=20
        )

    def check_time_limits(self):
        """Проверяет временные ограничения активных миссий"""
        active_mission = game_state.get_stat("active_mission")
        if not active_mission:
            return

        if active_mission in self.mission_system.mission_timers:
            start_time, time_limit = self.mission_system.mission_timers[active_mission]
            elapsed = (time.time() - start_time) / 3600
            remaining = time_limit - elapsed

            # Предупреждения о времени
            if remaining <= 0:
                self.trigger_event("time_warning",
                                   mission_id=active_mission,
                                   time_remaining=0,
                                   warning_level="expired")
            elif remaining <= time_limit * 0.1:  # 10% времени
                self.trigger_event("time_warning",
                                   mission_id=active_mission,
                                   time_remaining=remaining,
                                   warning_level="critical")
            elif remaining <= time_limit * 0.3:  # 30% времени
                self.trigger_event("time_warning",
                                   mission_id=active_mission,
                                   time_remaining=remaining,
                                   warning_level="low")


# Система статистики миссий
class MissionStatistics:
    """Система статистики для отслеживания производительности"""

    def __init__(self):
        self.stats = {
            "missions_completed": 0,
            "missions_failed": 0,
            "total_btc_earned": 0,
            "total_reputation_gained": 0,
            "stages_completed": 0,
            "team_missions_completed": 0,
            "moral_choices_made": 0,
            "time_critical_missions": 0,
            "average_mission_time": 0,
            "success_rate": 0,
            "favorite_faction": None,
            "moral_profile": "Unknown"
        }
        self.mission_history = []

    def record_mission_completion(self, mission_id: str, mission_data: dict,
                                  completion_time: float, rewards: dict):
        """Записывает завершение миссии"""
        self.stats["missions_completed"] += 1
        self.stats["total_btc_earned"] += rewards.get("btc", 0)
        self.stats["total_reputation_gained"] += rewards.get("reputation", 0)

        if mission_data.get("type") == "team_mission":
            self.stats["team_missions_completed"] += 1

        if "time_limit" in mission_data:
            self.stats["time_critical_missions"] += 1

        # Записываем в историю
        self.mission_history.append({
            "mission_id": mission_id,
            "completion_time": completion_time,
            "rewards": rewards,
            "timestamp": time.time(),
            "success": True
        })

        self._update_derived_stats()

    def record_mission_failure(self, mission_id: str, reason: str):
        """Записывает провал миссии"""
        self.stats["missions_failed"] += 1

        self.mission_history.append({
            "mission_id": mission_id,
            "reason": reason,
            "timestamp": time.time(),
            "success": False
        })

        self._update_derived_stats()

    def record_stage_completion(self, mission_id: str, stage_name: str):
        """Записывает завершение этапа"""
        self.stats["stages_completed"] += 1

    def record_moral_choice(self, choice_id: str, impact: int):
        """Записывает моральный выбор"""
        self.stats["moral_choices_made"] += 1
        # Здесь можно добавить анализ морального профиля

    def _update_derived_stats(self):
        """Обновляет производные статистики"""
        total_missions = self.stats["missions_completed"] + self.stats["missions_failed"]
        if total_missions > 0:
            self.stats["success_rate"] = (self.stats["missions_completed"] / total_missions) * 100

        # Средняя продолжительность миссий
        successful_missions = [m for m in self.mission_history if m.get("success")]
        if successful_missions:
            total_time = sum(m.get("completion_time", 0) for m in successful_missions)
            self.stats["average_mission_time"] = total_time / len(successful_missions)

    def get_performance_rating(self) -> str:
        """Возвращает рейтинг производительности"""
        success_rate = self.stats["success_rate"]

        if success_rate >= 90:
            return "Легендарный"
        elif success_rate >= 75:
            return "Элитный"
        elif success_rate >= 60:
            return "Опытный"
        elif success_rate >= 40:
            return "Средний"
        else:
            return "Новичок"

    def show_detailed_stats(self):
        """Показывает подробную статистику"""
        from ui.colors import XSSColors

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ СТАТИСТИКА МИССИЙ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Основные показатели
        print(f"\n{XSSColors.INFO}📊 ОСНОВНЫЕ ПОКАЗАТЕЛИ:{XSSColors.RESET}")
        print(f"   Выполнено миссий: {XSSColors.SUCCESS}{self.stats['missions_completed']}{XSSColors.RESET}")
        print(f"   Провалено миссий: {XSSColors.ERROR}{self.stats['missions_failed']}{XSSColors.RESET}")
        print(f"   Процент успеха: {XSSColors.WARNING}{self.stats['success_rate']:.1f}%{XSSColors.RESET}")
        print(f"   Рейтинг: {XSSColors.SUCCESS}{self.get_performance_rating()}{XSSColors.RESET}")

        # Финансовые показатели
        print(f"\n{XSSColors.MONEY}💰 ФИНАНСЫ:{XSSColors.RESET}")
        print(f"   Заработано BTC: {XSSColors.MONEY}{self.stats['total_btc_earned']:.2f}{XSSColors.RESET}")
        print(f"   Получено репутации: {XSSColors.REP}{self.stats['total_reputation_gained']}{XSSColors.RESET}")

        # Специальные миссии
        print(f"\n{XSSColors.WARNING}🎯 СПЕЦИАЛИЗАЦИЯ:{XSSColors.RESET}")
        print(f"   Командных миссий: {self.stats['team_missions_completed']}")
        print(f"   Критичных по времени: {self.stats['time_critical_missions']}")
        print(f"   Моральных выборов: {self.stats['moral_choices_made']}")
        print(f"   Этапов завершено: {self.stats['stages_completed']}")

        # Временные показатели
        if self.stats['average_mission_time'] > 0:
            print(f"\n{XSSColors.INFO}⏱️ ВРЕМЯ:{XSSColors.RESET}")
            print(f"   Среднее время миссии: {self.stats['average_mission_time']:.1f} ч")

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")


# Глобальные экземпляры
mission_statistics = MissionStatistics()


# Функция для инициализации всех систем
def initialize_advanced_mission_systems(mission_system):
    """Инициализирует все продвинутые системы миссий"""
    # Регистрируем обработчики событий
    register_mission_event_handlers()

    # Создаем менеджер событий миссий
    mission_event_manager = MissionEventManager(mission_system)

    # Связываем с системой миссий
    mission_system.event_manager = mission_event_manager
    mission_system.statistics = mission_statistics
    mission_system.notifications = mission_notifications

    return mission_event_manager

# Инициализация синглтона
event_system = EventSystem()