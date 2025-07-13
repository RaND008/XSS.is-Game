"""
Система миссий для XSS Game
"""

import random
import time
from typing import Dict, List, Optional, Tuple

from ui.colors import XSSColors as Colors
from ui.effects import typing_effect, show_ascii_art, progress_bar, pulse_text, animate_text, boxed_text
from core.game_state import game_state
from systems.audio import audio_system
from gameplay.minigames import minigame_hub
from config.game_data import MISSIONS


class MissionSystem:
    """Система управления миссиями"""

    def __init__(self):
        self.missions = MISSIONS
        self.active_teams = {}  # Для командных миссий
        self.mission_timers = {}  # Для отслеживания времени
        self.mission_events = {}  # Активные события миссий

    def get_available_missions(self) -> Dict[str, dict]:
        """Получает список доступных миссий"""
        available = {}
        player_stage = game_state.get_stat("story_stage", 0)
        player_faction = game_state.get_stat("faction")

        for mission_id, mission_data in self.missions.items():
            # Проверяем сюжетный этап
            if mission_data.get("story_stage", 0) > player_stage:
                continue

            # Проверяем фракцию
            req_faction = mission_data.get("req_faction")
            if req_faction and req_faction != player_faction:
                continue

            # Проверяем, не выполнена ли уже миссия
            if game_state.is_mission_completed(mission_id):
                continue

            available[mission_id] = mission_data

        return available

    def check_requirements(self, mission_data: dict) -> bool:
        """Проверяет требования для миссии"""
        # Проверяем репутацию
        req_rep = mission_data.get("req_rep", 0)
        if game_state.get_stat("reputation", 0) < req_rep:
            return False

        # Проверяем навыки
        req_skills = mission_data.get("req_skills", {})
        for skill, level in req_skills.items():
            if game_state.get_skill(skill) < level:
                return False

        return True

    def show_missions(self) -> None:
        """Показывает доступные миссии"""
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━ ДОСКА ЗАДАНИЙ ━━━━━━━━━━━━━━━━━{Colors.RESET}")

        # Проверка активной миссии
        active_mission = game_state.get_stat("active_mission")
        if active_mission:
            self._show_active_mission(active_mission)
            return

        available_missions = self.get_available_missions()

        if not available_missions:
            print(f"\n{Colors.WARNING}📭 Нет доступных миссий на данный момент{Colors.RESET}")
            print(f"\n{Colors.INFO}Повысьте репутацию или прокачайте навыки для новых заданий{Colors.RESET}")
            return

        # Группируем миссии по сложности
        easy_missions = []
        medium_missions = []
        hard_missions = []
        elite_missions = []

        for m_id, m_data in available_missions.items():
            risk = m_data.get('risk', 0)
            if risk < 20:
                easy_missions.append((m_id, m_data))
            elif risk < 40:
                medium_missions.append((m_id, m_data))
            elif risk < 70:
                hard_missions.append((m_id, m_data))
            else:
                elite_missions.append((m_id, m_data))

        # Выводим миссии по категориям
        if easy_missions:
            print(f"\n{Colors.SUCCESS}🟢 ЛЕГКИЕ ЗАДАНИЯ (Риск < 20%){Colors.RESET}")
            for m_id, m_data in easy_missions:
                self._print_mission(m_id, m_data)

        if medium_missions:
            print(f"\n{Colors.WARNING}🟡 СРЕДНИЕ ЗАДАНИЯ (Риск 20-40%){Colors.RESET}")
            for m_id, m_data in medium_missions:
                self._print_mission(m_id, m_data)

        if hard_missions:
            print(f"\n{Colors.ERROR}🟠 СЛОЖНЫЕ ЗАДАНИЯ (Риск 40-70%){Colors.RESET}")
            for m_id, m_data in hard_missions:
                self._print_mission(m_id, m_data)

        if elite_missions:
            print(f"\n{Colors.DANGER}🔴 ЭЛИТНЫЕ ЗАДАНИЯ (Риск > 70%){Colors.RESET}")
            for m_id, m_data in elite_missions:
                self._print_mission(m_id, m_data)

        # Добавляем информацию о специальных миссиях
        for mission_id, mission_data in available_missions.items():
            mission_type = mission_data.get("type", "normal")

            if mission_type == "multi_stage":
                stages_count = len(mission_data.get("stages", []))
                print(f"   🔗 Многоэтапная миссия ({stages_count} этапов)")

            elif mission_type == "team_mission":
                team_size = mission_data.get("team_size", 1)
                print(f"   👥 Командная миссия (команда из {team_size})")

            elif mission_type == "time_critical":
                time_limit = mission_data.get("time_limit", 24)
                print(f"   ⏰ Ограничено по времени ({time_limit}ч)")

            elif mission_type == "moral_choice":
                print(f"   🤔 Содержит моральные дилеммы")

            # Показываем активные таймеры
            if mission_id in self.mission_timers:
                start_time, time_limit = self.mission_timers[mission_id]
                elapsed = (time.time() - start_time) / 3600
                remaining = time_limit - elapsed
                print(f"   ⏱️ Осталось времени: {remaining:.1f}ч")

        print(f"\n{Colors.INFO}💡 Используйте 'take [ID миссии]' для принятия задания{Colors.RESET}")
        print(f"{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    def _show_active_mission(self, mission_id: str) -> None:
        """Показывает активную миссию"""
        if mission_id not in self.missions:
            print(f"{Colors.ERROR}Ошибка: активная миссия не найдена{Colors.RESET}")
            return

        mission = self.missions[mission_id]
        progress = game_state.get_stat("mission_progress", 0)
        duration = mission.get("duration", 1)

        print(f"\n{Colors.WARNING}⚡ АКТИВНАЯ МИССИЯ ⚡{Colors.RESET}")
        print(f"\n   {Colors.WARNING}{mission['name']}{Colors.RESET}")

        # Прогресс бар
        bar = progress_bar(progress, duration, length=30)
        print(f"   Прогресс: {bar} {progress}/{duration}")

        print(f"\n   {Colors.INFO}💡 Используйте 'work' для продолжения выполнения{Colors.RESET}")
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    def _print_mission(self, mission_id: str, mission_data: dict) -> None:
        """Вспомогательная функция для вывода информации о миссии"""
        # Проверяем требования
        can_take = self.check_requirements(mission_data)

        # Определяем статус и цвета
        if can_take:
            status_icon = "✅"
            id_color = Colors.WARNING
        else:
            status_icon = "🔒"
            id_color = Colors.ERROR

        # Риск с цветовой индикацией
        risk = mission_data.get('risk', 0)
        if risk < 30:
            risk_color = Colors.SUCCESS
        elif risk < 60:
            risk_color = Colors.WARNING
        else:
            risk_color = Colors.DANGER

        print(f"\n   {status_icon} ID: {id_color}{mission_id}{Colors.RESET}")
        print(f"   📋 {mission_data['name']}")
        print(f"   {Colors.INFO}{mission_data.get('desc', 'Нет описания')}{Colors.RESET}")

        # Награды
        btc_reward = mission_data.get('reward_btc', 0)
        rep_reward = mission_data.get('reward_rep', 0)
        print(f"   💰 Награда: {Colors.MONEY}{btc_reward} BTC{Colors.RESET} + {Colors.REP}{rep_reward} REP{Colors.RESET}")

        # Дополнительная информация
        print(f"   ⚡ Риск: {risk_color}{risk}%{Colors.RESET}")
        print(f"   ⏱️  Длительность: {Colors.INFO}{mission_data.get('duration', 0)} ходов{Colors.RESET}")

        # Heat gain если есть
        heat_gain = mission_data.get('heat_gain', 0)
        if heat_gain > 0:
            heat_color = Colors.WARNING if heat_gain < 20 else Colors.DANGER
            print(f"   🔥 Heat gain: {heat_color}+{heat_gain}%{Colors.RESET}")

        # Требования если не выполнены
        if not can_take:
            print(f"   {Colors.ERROR}Требования:{Colors.RESET}")
            req_rep = mission_data.get('req_rep', 0)
            if req_rep > 0:
                current_rep = game_state.get_stat('reputation', 0)
                print(f"      • Репутация: {Colors.ERROR}{req_rep}{Colors.RESET} (у вас: {current_rep})")

            req_skills = mission_data.get('req_skills', {})
            for skill, level in req_skills.items():
                skill_name = skill.replace('_', ' ').title()
                current_level = game_state.get_skill(skill)
                print(f"      • {skill_name}: {Colors.ERROR}{level}{Colors.RESET} (у вас: {current_level})")

        # Фракционная миссия
        req_faction = mission_data.get('req_faction')
        if req_faction:
            print(f"   🏛️ Фракция: {Colors.INFO}{req_faction}{Colors.RESET}")

    def take_mission(self, mission_id: str) -> bool:
        """Взять миссию"""
        if game_state.get_stat("active_mission"):
            print(f"{Colors.ERROR}[ОШИБКА] У вас уже есть активная миссия{Colors.RESET}")
            return False

        if mission_id not in self.missions:
            print(f"{Colors.ERROR}[ОШИБКА] Миссия '{mission_id}' не найдена{Colors.RESET}")
            return False

        available_missions = self.get_available_missions()
        if mission_id not in available_missions:
            print(f"{Colors.ERROR}[ОШИБКА] Миссия '{mission_id}' недоступна{Colors.RESET}")
            return False

        mission_data = self.missions[mission_id]

        # Проверяем требования
        if not self.check_requirements(mission_data):
            print(f"{Colors.ERROR}[ОШИБКА] Не выполнены требования для миссии{Colors.RESET}")
            return False

        mission_type = mission_data.get("type", "normal")

        # Устанавливаем таймер для миссий с временными ограничениями
        if "time_limit" in mission_data:
            self.mission_timers[mission_id] = (time.time(), mission_data["time_limit"])
            print(
                f"{Colors.WARNING}⏰ Миссия имеет временное ограничение: {mission_data['time_limit']} часов{Colors.RESET}")

        # Инициализируем дополнительные данные
        if mission_type in ["multi_stage", "team_mission", "moral_choice"]:
            game_state.set_stat("current_mission_stage", 0)

        # Принимаем миссию
        print(f"\n{Colors.WARNING}[ПОДКЛЮЧЕНИЕ] Установка зашифрованного канала...{Colors.RESET}")
        time.sleep(1)
        typing_effect(f"{Colors.INFO}[ЗАКАЗЧИК] {mission_data['desc']}", 0.03)
        time.sleep(0.5)

        game_state.set_stat("active_mission", mission_id)
        game_state.set_stat("mission_progress", 0)

        audio_system.play_sound("mission_start")
        show_ascii_art("hack")
        print(f"{Colors.SUCCESS}[УСПЕХ] Миссия '{mission_data['name']}' активирована{Colors.RESET}")
        print(f"{Colors.INFO}Используйте 'work' для выполнения{Colors.RESET}")

        return True

    def work_mission(self) -> bool:
        """Выполнение миссии с мини-играми и стоимостью работы"""
        # Сначала проверяем наличие активной миссии
        active_mission = game_state.get_stat("active_mission")
        if not active_mission:
            print(f"{Colors.ERROR}[ОШИБКА] У вас нет активной миссии{Colors.RESET}")
            return False

        if active_mission not in self.missions:
            print(f"{Colors.ERROR}[ОШИБКА] Активная миссия не найдена в базе данных{Colors.RESET}")
            return False

        # Проверяем временные ограничения
        if not self.check_mission_time_limit(active_mission):
            return False

        mission_data = self.missions[active_mission]
        mission_type = mission_data.get("type", "normal")

        if mission_type == "multi_stage":
            return self._work_multi_stage_mission(active_mission, mission_data)
        elif mission_type == "team_mission":
            return self._work_team_mission(active_mission, mission_data)
        elif mission_type == "time_critical":
            return self._work_time_critical_mission(active_mission, mission_data)
        elif mission_type == "moral_choice":
            return self._work_moral_choice_mission(active_mission, mission_data)

        # Стандартная логика для обычных миссий
        progress = game_state.get_stat("mission_progress", 0)
        duration = mission_data.get("duration", 1)

        # Проверяем, не завершена ли уже миссия
        if progress >= duration:
            print(f"{Colors.WARNING}[!] Миссия уже выполнена. Используйте другую команду для завершения.{Colors.RESET}")
            return False

        # Рассчитываем стоимость выполнения на основе риска миссии
        base_cost = 5  # Базовая стоимость в BTC
        risk = mission_data.get("risk", 0)

        if risk >= 80:
            mission_cost = base_cost * 4  # 20 BTC для очень опасных
        elif risk >= 60:
            mission_cost = base_cost * 3  # 15 BTC для опасных
        elif risk >= 40:
            mission_cost = base_cost * 2  # 10 BTC для средних
        else:
            mission_cost = base_cost  # 5 BTC для легких

        # Проверяем, может ли игрок позволить себе работу
        if not game_state.can_afford(mission_cost, "btc_balance"):
            print(f"{Colors.ERROR}[ОШИБКА] Недостаточно BTC для работы над миссией{Colors.RESET}")
            print(
                f"{Colors.INFO}Требуется: {mission_cost} BTC | У вас: {game_state.get_stat('btc_balance', 0):.2f} BTC{Colors.RESET}")
            print(f"{Colors.WARNING}💡 Совет: выполните более простые миссии или продайте криптовалюту{Colors.RESET}")
            return False

        # Списываем стоимость работы
        game_state.spend_currency(mission_cost, "btc_balance")
        print(f"{Colors.MONEY}[-] Потрачено {mission_cost} BTC на оборудование и ресурсы{Colors.RESET}")

        # Получаем сообщения для работы
        work_messages = self._get_work_messages(mission_data)

        # Отображаем процесс работы
        print(f"\n{Colors.INFO}[РАБОТА] Выполнение: {mission_data['name']}{Colors.RESET}")
        print(f"{Colors.INFO}Прогресс: {progress + 1}/{duration}{Colors.RESET}")
        typing_effect(f"{Colors.WARNING}[ПРОЦЕСС] {random.choice(work_messages)}{Colors.RESET}", 0.02)
        time.sleep(1)

        # Мини-игра на определенных этапах (середина и конец миссии)
        minigame_success = True
        if progress == duration // 2 or progress == duration - 1:
            print(f"\n{Colors.DANGER}⚠️ КРИТИЧЕСКИЙ МОМЕНТ МИССИИ!{Colors.RESET}")
            minigame_success = self._run_mission_minigame(mission_data)

        # Расчет шанса провала с учетом результата мини-игры
        fail_chance = self._calculate_fail_chance(mission_data, minigame_success)

        # Добавляем небольшую драматичность
        print(f"\n{Colors.INFO}Обработка результатов...{Colors.RESET}")
        time.sleep(1)

        # Бросок на успех/провал
        roll = random.randint(1, 100)

        if roll <= fail_chance:
            # Провал миссии
            print(f"{Colors.ERROR}[!] Критическая ошибка обнаружена!{Colors.RESET}")
            return self._handle_mission_failure(mission_data)
        else:
            # Успешный прогресс
            print(f"{Colors.SUCCESS}[✓] Этап выполнен успешно!{Colors.RESET}")
            return self._handle_mission_progress(mission_data)

    def _get_work_messages(self, mission_data: dict) -> List[str]:
        """Получает сообщения для работы над миссией"""
        mission_type = self._determine_mission_type(mission_data)

        work_messages = {
            "scanning": [
                "Сканирование портов целевой системы...",
                "Анализ сетевой топологии...",
                "Поиск открытых сервисов...",
                "Определение версий ПО..."
            ],
            "cracking": [
                "Подбор паролей к найденным сервисам...",
                "Эксплуатация найденных уязвимостей...",
                "Обход систем защиты...",
                "Внедрение бэкдора..."
            ],
            "stealth": [
                "Маскировка сетевой активности...",
                "Очистка логов...",
                "Создание ложных следов...",
                "Проверка на обнаружение..."
            ],
            "social_eng": [
                "Составление фишингового письма...",
                "Изучение целевой аудитории...",
                "Создание убедительной легенды...",
                "Отправка приманки..."
            ]
        }

        return work_messages.get(mission_type, work_messages["scanning"])

    def _determine_mission_type(self, mission_data: dict) -> str:
        """Определяет тип миссии по требуемым навыкам"""
        req_skills = mission_data.get("req_skills", {})
        if not req_skills:
            return "scanning"

        # Возвращаем навык с наибольшим требованием
        return max(req_skills.keys(), key=lambda k: req_skills[k])

    def _run_mission_minigame(self, mission_data: dict) -> bool:
        """Запускает мини-игру во время миссии"""
        print(f"\n{Colors.DANGER}⚠️ ТРЕБУЕТСЯ РУЧНОЕ ВМЕШАТЕЛЬСТВО!{Colors.RESET}")
        time.sleep(1)

        mission_type = self._determine_mission_type(mission_data)
        mission_name = mission_data.get("name", "").lower()

        # Выбираем подходящую мини-игру
        if "database" in mission_name or "crypto" in mission_name:
            game_id, game = minigame_hub.games["password_crack"], minigame_hub.games["password_crack"]
        elif "phishing" in mission_name or "social" in mission_name:
            game_id, game = minigame_hub.games["memory_sequence"], minigame_hub.games["memory_sequence"]
        elif "network" in mission_name or "сканирование" in mission_name:
            game_id, game = minigame_hub.games["network_trace"], minigame_hub.games["network_trace"]
        elif "web" in mission_name or "sql" in mission_name:
            game_id, game = minigame_hub.games["sql_injection"], minigame_hub.games["sql_injection"]
        else:
            # Случайная мини-игра
            game_id, game = minigame_hub.get_random_minigame()

        return game.play()

    def _calculate_fail_chance(self, mission_data: dict, minigame_success: bool) -> int:
        """Рассчитывает шанс провала миссии с учетом всех факторов"""
        # Базовый шанс провала из данных миссии
        base_fail_chance = mission_data.get("risk", 50)

        # Факторы, влияющие на шанс провала:

        # 1. Навыки игрока (снижают шанс провала)
        skill_reduction = 0
        req_skills = mission_data.get("req_skills", {})

        for skill, required_level in req_skills.items():
            player_skill = game_state.get_skill(skill)
            # Бонус за превышение требуемого уровня
            if player_skill > required_level:
                skill_reduction += (player_skill - required_level) * 3
            # Штраф за недостаток навыка (не должно быть, но на всякий случай)
            elif player_skill < required_level:
                skill_reduction -= (required_level - player_skill) * 5

        # Общий бонус от всех навыков
        total_skills = sum(game_state.get_skill(s) for s in ["scanning", "cracking", "stealth", "social_eng"])
        skill_reduction += total_skills  # 1% за каждый уровень навыка

        # 2. Снаряжение (снижает шанс провала)
        equipment_bonus = 0
        inventory = game_state.get_stat("inventory", [])

        # Специфичные предметы для разных типов миссий
        mission_type = self._determine_mission_type(mission_data)

        helpful_items = {
            "scanning": ["basic_port_scanner", "advanced_scanner", "pro_vuln_scanner"],
            "cracking": ["password_list", "ai_password_cracker", "quantum_decryptor"],
            "stealth": ["simple_proxy", "proxy_network", "elite_proxy"],
            "social_eng": ["fake_id_generator", "phishing_kit", "fake_documents"]
        }

        # Проверяем наличие полезных предметов
        for item in inventory:
            for skill_type, items_list in helpful_items.items():
                if item in items_list:
                    equipment_bonus += 5  # 5% за каждый полезный предмет

        # 3. Результат мини-игры (критически важен)
        minigame_penalty = 0
        if not minigame_success:
            minigame_penalty = 30  # +30% к шансу провала при провале мини-игры
        else:
            minigame_penalty = -10  # -10% при успехе мини-игры

        # 4. Heat Level (увеличивает шанс провала)
        heat_level = game_state.get_stat("heat_level", 0)
        heat_penalty = 0

        if heat_level > 80:
            heat_penalty = 25  # Критический уровень розыска
        elif heat_level > 60:
            heat_penalty = 15
        elif heat_level > 40:
            heat_penalty = 10
        elif heat_level > 20:
            heat_penalty = 5

        # 5. Количество предупреждений
        warnings = game_state.get_stat("warnings", 0)
        warning_penalty = warnings * 10  # +10% за каждое предупреждение

        # 6. Прогрессивная сложность (игра становится сложнее)
        completed_missions = len(game_state.get_stat("completed_missions", []))
        progression_penalty = 0

        if completed_missions > 30:
            progression_penalty = 20
        elif completed_missions > 20:
            progression_penalty = 15
        elif completed_missions > 10:
            progression_penalty = 10
        elif completed_missions > 5:
            progression_penalty = 5

        # 7. Фракционные бонусы/штрафы
        faction_modifier = 0
        player_faction = game_state.get_stat("faction")

        if player_faction:
            # WhiteHats получают бонус на легальных миссиях
            if player_faction == "whitehats" and mission_data.get("heat_gain", 0) < 10:
                faction_modifier = -10
            # BlackHats лучше в криминальных миссиях
            elif player_faction == "blackhats" and mission_data.get("heat_gain", 0) > 20:
                faction_modifier = -10
            # GrayHats универсальны
            elif player_faction == "grayhats":
                faction_modifier = -5

        # 8. VPN бонус через инвентарь (упрощенная версия)
        vpn_bonus = 0
        vpn_items = ["vpn_subscription", "elite_proxy", "proxy_network"]
        for item in inventory:
            if item in vpn_items:
                vpn_bonus -= 10  # -10% за каждый VPN/прокси предмет
                break  # Учитываем только один

        # 9. Время суток (случайный фактор для реализма)
        time_modifier = random.randint(-5, 5)

        # Итоговый расчет
        final_fail_chance = (
                base_fail_chance
                - skill_reduction
                - equipment_bonus
                + minigame_penalty
                + heat_penalty
                + warning_penalty
                + progression_penalty
                + faction_modifier
                + vpn_bonus
                + time_modifier
        )

        # Ограничиваем диапазон от 5% до 95%
        final_fail_chance = max(5, min(95, final_fail_chance))

        # Отладочная информация для сложных миссий
        if base_fail_chance >= 70:
            print(f"\n{Colors.INFO}📊 Анализ рисков:{Colors.RESET}")
            print(f"   Базовый риск: {base_fail_chance}%")
            print(f"   Бонус навыков: -{skill_reduction}%")
            print(f"   Бонус снаряжения: -{equipment_bonus}%")
            if minigame_penalty != 0:
                print(f"   Мини-игра: {minigame_penalty:+}%")
            if heat_penalty > 0:
                print(f"   Heat Level: +{heat_penalty}%")
            print(f"   {Colors.WARNING}Итоговый риск: {final_fail_chance}%{Colors.RESET}")

        return final_fail_chance

    def _handle_mission_failure(self, mission_data: dict) -> bool:
        """Обрабатывает провал миссии"""
        # Увеличиваем штрафы за провал
        heat_gain = mission_data.get("heat_gain", 10)
        heat_gain = int(heat_gain * 1.5)  # Увеличиваем на 50%

        # Добавляем накопительный эффект
        current_heat = game_state.get_stat("heat_level", 0)
        if current_heat > 50:
            heat_gain = int(heat_gain * 1.2)  # Еще +20% если уже высокий heat

        audio_system.play_sound("fail")
        audio_system.play_sound("alert")

        show_ascii_art("warning")
        print(f"{Colors.ERROR}[ПРОВАЛ] Миссия провалена! Вас обнаружили!{Colors.RESET}")

        # Наказания
        warnings = game_state.modify_stat("warnings", 1)
        new_heat = game_state.modify_stat("heat_level", heat_gain)

        rep_penalty = random.randint(5, 15)
        game_state.modify_stat("reputation", -rep_penalty)

        print(f"{Colors.WARNING}[-] Репутация -{rep_penalty}{Colors.RESET}")
        print(f"{Colors.DANGER}[!] Heat Level: {new_heat}%{Colors.RESET}")
        print(f"{Colors.ERROR}[!] Предупреждения: {warnings}/3{Colors.RESET}")

        # Сбрасываем миссию
        game_state.set_stat("active_mission", None)
        game_state.set_stat("mission_progress", 0)

        return False

    def _handle_mission_progress(self, mission_data: dict) -> bool:
        """Обрабатывает успешный прогресс миссии"""
        progress = game_state.modify_stat("mission_progress", 1)
        duration = mission_data.get("duration", 1)

        # Показываем прогресс
        bar = progress_bar(progress, duration, length=30)
        print(f"{Colors.SUCCESS}[ПРОГРЕСС] {bar} {progress}/{duration}{Colors.RESET}")

        if progress >= duration:
            return self._complete_mission(mission_data)

        return True

    def _complete_mission(self, mission_data: dict) -> bool:
        """Завершает миссию"""
        mission_id = game_state.get_stat("active_mission")

        audio_system.play_sound("mission_complete")
        audio_system.play_sound("coin")

        show_ascii_art("hack")
        print(f"\n{Colors.SUCCESS}╔═══════════════════ МИССИЯ ВЫПОЛНЕНА ═══════════════════╗{Colors.RESET}")
        print(f"{Colors.SUCCESS}║ {mission_data['name']:^54} ║{Colors.RESET}")
        print(f"{Colors.SUCCESS}╚════════════════════════════════════════════════════════╝{Colors.RESET}")

        # Награды
        btc_reward = mission_data.get("reward_btc", 0)
        rep_reward = mission_data.get("reward_rep", 0)

        game_state.earn_currency(btc_reward, "btc_balance")
        game_state.modify_stat("reputation", rep_reward)

        print(f"{Colors.MONEY}[+] {btc_reward} BTC{Colors.RESET}")
        print(f"{Colors.REP}[+] {rep_reward} репутации{Colors.RESET}")

        # Навыки
        reward_skills = mission_data.get("reward_skills", {})
        if reward_skills:
            audio_system.play_sound("skill_up")
            for skill, points in reward_skills.items():
                if skill == "all":
                    for s in ["scanning", "cracking", "stealth", "social_eng"]:
                        current = game_state.get_skill(s)
                        if current >= 8:
                            points = max(1, points // 2)  # Половина очков на 8+
                        elif current >= 6:
                            points = max(1, int(points * 0.75))  # -25% на 6+
                        game_state.modify_skill(s, points)
                    print(f"{Colors.SKILL}[+] Все навыки +{points}{Colors.RESET}")
                elif skill in ["scanning", "cracking", "stealth", "social_eng"]:
                    old_level = game_state.get_skill(skill)
                    new_level = game_state.modify_skill(skill, points)
                    print(f"{Colors.SKILL}[+] {skill} +{points} ({old_level} → {new_level}){Colors.RESET}")

        # Heat level
        heat_gain = mission_data.get("heat_gain", 0)
        if heat_gain > 0:
            new_heat = game_state.modify_stat("heat_level", heat_gain)
            heat_color = Colors.WARNING if new_heat < 50 else Colors.DANGER
            print(f"{heat_color}[!] Heat Level: {new_heat}%{Colors.RESET}")

        # Отмечаем как выполненную
        game_state.complete_mission(mission_id)

        # Сбрасываем активную миссию
        game_state.set_stat("active_mission", None)
        game_state.set_stat("mission_progress", 0)

        return True

    def get_mission_info(self, mission_id: str) -> Optional[dict]:
        """Получает информацию о миссии"""
        return self.missions.get(mission_id)

    def is_mission_available(self, mission_id: str) -> bool:
        """Проверяет доступность миссии"""
        available_missions = self.get_available_missions()
        return mission_id in available_missions

    def check_mission_time_limit(self, mission_id: str) -> bool:
        """Проверяет временные ограничения миссии"""
        if mission_id not in self.mission_timers:
            return True

        start_time, time_limit = self.mission_timers[mission_id]
        elapsed = (time.time() - start_time) / 3600  # в часах

        if elapsed > time_limit:
            self._handle_mission_timeout(mission_id)
            return False

        return True

    def _handle_mission_timeout(self, mission_id: str) -> None:
        """Обрабатывает истечение времени миссии"""
        mission_data = self.missions.get(mission_id, {})

        print(f"\n{Colors.ERROR}⏰ ВРЕМЯ ИСТЕКЛО!{Colors.RESET}")
        print(f"Миссия '{mission_data.get('name', mission_id)}' провалена")

        # Штрафы за просрочку
        rep_penalty = random.randint(10, 25)
        heat_gain = random.randint(15, 30)

        game_state.modify_stat("reputation", -rep_penalty)
        game_state.modify_stat("heat_level", heat_gain)

        # Сбрасываем миссию
        game_state.set_stat("active_mission", None)
        game_state.set_stat("mission_progress", 0)

        if mission_id in self.mission_timers:
            del self.mission_timers[mission_id]

    def _work_multi_stage_mission(self, mission_id: str, mission_data: dict) -> bool:
        """Обработка многоэтапных миссий"""
        current_stage = game_state.get_stat("current_mission_stage", 0)
        stages = mission_data.get("stages", [])

        if current_stage >= len(stages):
            return self._complete_multi_stage_mission(mission_id, mission_data)

        stage_data = stages[current_stage]

        print(f"\n{Colors.WARNING}📋 ЭТАП {current_stage + 1}/{len(stages)}: {stage_data['name']}{Colors.RESET}")
        print(f"{Colors.INFO}{stage_data['desc']}{Colors.RESET}")

        # Проверяем требования этапа
        if not self._check_stage_requirements(stage_data):
            return False

        # Обрабатываем случайные события
        self._check_random_events(mission_id, f"stage_{current_stage}")

        # Выполняем этап
        success = self._execute_mission_stage(stage_data)

        if success:
            # Применяем награды этапа
            self._apply_stage_rewards(stage_data)

            # Переходим к следующему этапу
            game_state.set_stat("current_mission_stage", current_stage + 1)

            print(f"{Colors.SUCCESS}✅ Этап завершен успешно!{Colors.RESET}")

            # Проверяем моральные выборы
            if "moral_choice" in stage_data:
                self._handle_moral_choice(stage_data["moral_choice"])

            return True
        else:
            return self._handle_mission_failure(mission_data)

    def _work_team_mission(self, mission_id: str, mission_data: dict) -> bool:
        """Обработка командных миссий"""
        if mission_id not in self.active_teams:
            return self._recruit_team(mission_id, mission_data)

        team = self.active_teams[mission_id]
        current_stage = game_state.get_stat("current_mission_stage", 0)
        stages = mission_data.get("stages", [])

        if current_stage >= len(stages):
            return self._complete_team_mission(mission_id, mission_data)

        stage_data = stages[current_stage]

        print(f"\n{Colors.WARNING}👥 КОМАНДНАЯ ОПЕРАЦИЯ - ЭТАП {current_stage + 1}{Colors.RESET}")
        print(f"{Colors.INFO}{stage_data['desc']}{Colors.RESET}")

        # Показываем состояние команды
        self._show_team_status(team)

        # Выполняем командное действие
        success = self._execute_team_action(stage_data, team)

        if success:
            game_state.set_stat("current_mission_stage", current_stage + 1)
            return True
        else:
            return self._handle_team_mission_failure(mission_data, team)

    def _work_time_critical_mission(self, mission_id: str, mission_data: dict) -> bool:
        """Обработка миссий с временными ограничениями"""
        # Получаем оставшееся время
        start_time, time_limit = self.mission_timers.get(mission_id, (time.time(), 24))
        elapsed = (time.time() - start_time) / 3600
        remaining = time_limit - elapsed

        print(f"\n{Colors.DANGER}⏱️ КРИТИЧЕСКОЕ ВРЕМЯ: {remaining:.1f} часов осталось{Colors.RESET}")

        if remaining <= 1:
            print(f"{Colors.ERROR}🚨 ПОСЛЕДНИЙ ЧАС! Операция под угрозой!{Colors.RESET}")

        # Увеличиваем сложность в зависимости от оставшегося времени
        time_pressure_multiplier = mission_data.get("time_pressure_multiplier", 1.0)
        if remaining < time_limit * 0.3:  # Меньше 30% времени
            time_pressure_multiplier *= 1.5

        return self._work_multi_stage_mission(mission_id, mission_data)

    def _work_moral_choice_mission(self, mission_id: str, mission_data: dict) -> bool:
        """Обработка миссий с моральными выборами"""
        current_stage = game_state.get_stat("current_mission_stage", 0)
        stages = mission_data.get("stages", [])

        stage_data = stages[current_stage]

        if "moral_choice" in stage_data:
            print(f"\n{Colors.STORY}🤔 МОРАЛЬНАЯ ДИЛЕММА{Colors.RESET}")
            return self._handle_moral_choice(stage_data["moral_choice"])
        else:
            return self._work_multi_stage_mission(mission_id, mission_data)

    def _handle_moral_choice(self, choice_data: dict) -> bool:
        """Обрабатывает моральный выбор"""
        print(f"\n{Colors.STORY}{choice_data['question']}{Colors.RESET}")

        choices = choice_data["choices"]
        choice_list = list(choices.items())

        print(f"\n{Colors.INFO}Ваши варианты:{Colors.RESET}")
        for i, (choice_id, choice_info) in enumerate(choice_list, 1):
            print(f"   {i}. {choice_info['desc']}")

        while True:
            try:
                user_choice = int(input(f"\n{Colors.PROMPT}Ваш выбор (1-{len(choices)}): {Colors.RESET}"))
                if 1 <= user_choice <= len(choices):
                    break
            except ValueError:
                pass
            print(f"{Colors.ERROR}Неверный выбор{Colors.RESET}")

        choice_id, choice_result = choice_list[user_choice - 1]

        print(f"\n{Colors.WARNING}Вы выбрали: {choice_result['desc']}{Colors.RESET}")

        # Применяем последствия выбора
        self._apply_moral_choice_consequences(choice_result)

        # Сохраняем выбор для истории
        choices_made = game_state.get_stat("moral_choices_made", {})
        choices_made[f"mission_{game_state.get_stat('active_mission')}"] = choice_id
        game_state.set_stat("moral_choices_made", choices_made)

        return not choice_result.get("mission_failure", False)

    def _apply_moral_choice_consequences(self, choice_result: dict) -> None:
        """Применяет последствия морального выбора"""
        # Изменение репутации
        if "rep_change" in choice_result:
            rep_change = choice_result["rep_change"]
            game_state.modify_stat("reputation", rep_change)
            if rep_change > 0:
                print(f"{Colors.SUCCESS}[+] Репутация +{rep_change}{Colors.RESET}")
            elif rep_change < 0:
                print(f"{Colors.ERROR}[-] Репутация {rep_change}{Colors.RESET}")

        # Изменение фракционных отношений
        if "faction_impact" in choice_result:
            for faction, impact in choice_result["faction_impact"].items():
                print(f"{Colors.INFO}[Фракция {faction}]: {'+' if impact > 0 else ''}{impact}{Colors.RESET}")

        # Бонусы/штрафы к валюте
        if "btc_bonus" in choice_result:
            bonus = choice_result["btc_bonus"]
            game_state.earn_currency(bonus, "btc_balance")
            print(f"{Colors.MONEY}[+] {bonus} BTC{Colors.RESET}")

        if "btc_penalty" in choice_result:
            penalty = choice_result["btc_penalty"]
            game_state.spend_currency(penalty, "btc_balance")
            print(f"{Colors.ERROR}[-] {penalty} BTC{Colors.RESET}")

        # Heat level изменения
        if "heat_gain" in choice_result:
            heat = choice_result["heat_gain"]
            game_state.modify_stat("heat_level", heat)
            print(f"{Colors.DANGER}[!] Heat Level +{heat}%{Colors.RESET}")

        # Специальные награды/последствия
        if "special_reward" in choice_result:
            reward = choice_result["special_reward"]
            game_state.add_to_inventory(reward)
            print(f"{Colors.SUCCESS}[+] Особая награда: {reward}{Colors.RESET}")

    def _check_random_events(self, mission_id: str, trigger: str) -> None:
        """Проверяет и обрабатывает случайные события"""
        mission_data = self.missions[mission_id]
        events = mission_data.get("random_events", [])

        for event_data in events:
            if event_data["trigger"] == trigger and random.random() < event_data["chance"]:
                self._trigger_mission_event(mission_id, event_data)

    def _trigger_mission_event(self, mission_id: str, event_data: dict) -> None:
        """Запускает случайное событие миссии"""
        print(f"\n{Colors.WARNING}⚡ НЕОЖИДАННОЕ СОБЫТИЕ!{Colors.RESET}")
        print(f"{Colors.ERROR}{event_data['desc']}{Colors.RESET}")

        # Применяем эффекты события
        effects = event_data.get("effects", {})

        if "heat_gain" in effects:
            game_state.modify_stat("heat_level", effects["heat_gain"])
            print(f"{Colors.DANGER}[!] Heat Level +{effects['heat_gain']}%{Colors.RESET}")

        if "time_pressure" in effects:
            # Сокращаем время миссии
            if mission_id in self.mission_timers:
                start_time, time_limit = self.mission_timers[mission_id]
                new_limit = time_limit * 0.7  # Сокращаем на 30%
                self.mission_timers[mission_id] = (start_time, new_limit)
                print(f"{Colors.ERROR}[!] Время миссии сокращено!{Colors.RESET}")

        # Сохраняем событие для отслеживания
        if mission_id not in self.mission_events:
            self.mission_events[mission_id] = []
        self.mission_events[mission_id].append(event_data["event"])

    def _recruit_team(self, mission_id: str, mission_data: dict) -> bool:
        """Набор команды для миссии"""
        team_size = mission_data.get("team_size", 3)
        required_roles = mission_data.get("team_roles", ["hacker", "social_engineer", "lookout"])

        print(f"\n{Colors.WARNING}👥 НАБОР КОМАНДЫ{Colors.RESET}")
        print(f"Требуется участников: {team_size}")
        print(f"Роли: {', '.join(required_roles)}")

        # Генерируем доступных кандидатов
        candidates = self._generate_team_candidates(required_roles)

        print(f"\n{Colors.INFO}Доступные кандидаты:{Colors.RESET}")
        for i, candidate in enumerate(candidates, 1):
            skill_color = Colors.SUCCESS if candidate['skill_level'] >= 7 else Colors.WARNING if candidate[
                                                                                                     'skill_level'] >= 4 else Colors.ERROR
            print(f"\n   {i}. {candidate['name']} ({candidate['role']})")
            print(f"      Навык: {skill_color}{candidate['skill_level']}/10{Colors.RESET}")
            print(f"      Лояльность: {candidate['loyalty']}%")
            print(f"      Стоимость: {candidate['cost']} BTC/этап")
            print(f"      Особенности: {candidate['traits']}")

        # Позволяем игроку выбрать команду
        team_members = []
        while len(team_members) < team_size:
            try:
                choice = int(input(
                    f"\n{Colors.PROMPT}Выберите участника {len(team_members) + 1}/{team_size} (1-{len(candidates)}): {Colors.RESET}"))
                if 1 <= choice <= len(candidates):
                    selected = candidates[choice - 1]
                    if selected not in team_members:
                        team_members.append(selected)
                        print(f"{Colors.SUCCESS}✅ {selected['name']} добавлен в команду{Colors.RESET}")
                    else:
                        print(f"{Colors.ERROR}Этот участник уже в команде{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}Неверный выбор{Colors.RESET}")
            except ValueError:
                print(f"{Colors.ERROR}Введите число{Colors.RESET}")

        # Рассчитываем стоимость команды
        total_cost = sum(member['cost'] for member in team_members)

        print(f"\n{Colors.INFO}💰 Стоимость команды: {total_cost} BTC за этап{Colors.RESET}")

        if not game_state.can_afford(total_cost, "btc_balance"):
            print(f"{Colors.ERROR}Недостаточно средств для найма команды{Colors.RESET}")
            return False

        confirm = input(f"{Colors.PROMPT}Нанять команду? (y/n): {Colors.RESET}").lower()

        if confirm == 'y':
            game_state.spend_currency(total_cost, "btc_balance")

            # Создаем команду
            team = {
                "members": team_members,
                "synergy": self._calculate_team_synergy(team_members),
                "total_cost": total_cost
            }

            self.active_teams[mission_id] = team

            print(f"\n{Colors.SUCCESS}✅ Команда собрана!{Colors.RESET}")
            print(f"Синергия команды: {team['synergy']}%")
            return True

        return False

    def _generate_team_candidates(self, required_roles: list) -> list:
        """Генерирует кандидатов для команды"""
        candidates = []

        # Имена и специализации
        names_pool = [
            "Phoenix", "Cipher", "Ghost", "Viper", "Raven", "Blade", "Storm", "Shadow",
            "Zero", "Matrix", "Nova", "Flux", "Echo", "Void", "Nexus", "Quantum"
        ]

        traits_pool = {
            "hacker": ["Эксперт по 0-day", "Специалист по мейнфреймам", "Мастер социальной инженерии"],
            "social_engineer": ["Манипулятор", "Мастер маскировки", "Психолог"],
            "lookout": ["Хорошая реакция", "Знание улиц", "Связи в полиции"]
        }

        for role in required_roles:
            # Генерируем 2-3 кандидата на каждую роль
            for _ in range(random.randint(2, 3)):
                name = random.choice(names_pool)
                skill_level = random.randint(3, 9)
                loyalty = random.randint(40, 90)

                # Стоимость зависит от навыка
                base_cost = 50
                cost = base_cost + (skill_level - 3) * 20 + random.randint(-10, 20)

                candidate = {
                    "name": name,
                    "role": role,
                    "skill_level": skill_level,
                    "loyalty": loyalty,
                    "cost": cost,
                    "traits": random.choice(traits_pool.get(role, ["Универсал"]))
                }

                candidates.append(candidate)
                names_pool.remove(name)  # Убираем чтобы не повторялись

        return candidates

    def _calculate_team_synergy(self, team_members: list) -> int:
        """Рассчитывает синергию команды"""
        base_synergy = 50

        # Бонус за высокие навыки
        avg_skill = sum(member['skill_level'] for member in team_members) / len(team_members)
        skill_bonus = int((avg_skill - 5) * 5)

        # Бонус за лояльность
        avg_loyalty = sum(member['loyalty'] for member in team_members) / len(team_members)
        loyalty_bonus = int((avg_loyalty - 50) / 2)

        # Штраф за дисбаланс навыков
        skill_levels = [member['skill_level'] for member in team_members]
        skill_variance = max(skill_levels) - min(skill_levels)
        balance_penalty = skill_variance * 2

        synergy = base_synergy + skill_bonus + loyalty_bonus - balance_penalty
        return max(20, min(100, synergy))

    def _show_team_status(self, team: dict) -> None:
        """Показывает статус команды"""
        print(f"\n{Colors.SUCCESS}👥 КОМАНДА:{Colors.RESET}")

        for member in team["members"]:
            status_icon = "😊" if member['loyalty'] >= 70 else "😐" if member['loyalty'] >= 40 else "😠"
            print(f"   {status_icon} {member['name']} ({member['role']}) - Навык: {member['skill_level']}/10")

        synergy_color = Colors.SUCCESS if team['synergy'] >= 80 else Colors.WARNING if team[
                                                                                           'synergy'] >= 60 else Colors.ERROR
        print(f"   🤝 Синергия: {synergy_color}{team['synergy']}%{Colors.RESET}")

    def _execute_team_action(self, stage_data: dict, team: dict) -> bool:
        """Выполняет командное действие"""
        action_type = stage_data.get("team_action", "default")

        print(f"\n{Colors.INFO}🎯 Командное действие: {action_type}{Colors.RESET}")

        # Рассчитываем шанс успеха на основе команды
        base_success = 0.5

        # Бонус от синергии команды
        synergy_bonus = team['synergy'] / 200  # 0-0.5 бонус

        # Бонус от навыков
        avg_skill = sum(member['skill_level'] for member in team['members']) / len(team['members'])
        skill_bonus = (avg_skill - 5) / 10  # -0.5 до +0.4 бонус

        # Штраф от низкой лояльности
        avg_loyalty = sum(member['loyalty'] for member in team['members']) / len(team['members'])
        loyalty_modifier = (avg_loyalty - 50) / 100  # -0.5 до +0.4

        success_chance = base_success + synergy_bonus + skill_bonus + loyalty_modifier
        success_chance = max(0.1, min(0.95, success_chance))

        print(f"{Colors.INFO}Шанс успеха: {int(success_chance * 100)}%{Colors.RESET}")

        # Мини-игра для командных действий
        if action_type == "execute":
            success = self._team_coordination_minigame(team)
        else:
            success = random.random() < success_chance

        if success:
            print(f"{Colors.SUCCESS}✅ Команда выполнила задачу отлично!{Colors.RESET}")
            # Повышаем лояльность
            for member in team['members']:
                member['loyalty'] = min(100, member['loyalty'] + random.randint(5, 15))
        else:
            print(f"{Colors.ERROR}❌ Команда не справилась с задачей{Colors.RESET}")
            # Снижаем лояльность
            for member in team['members']:
                member['loyalty'] = max(0, member['loyalty'] - random.randint(10, 25))

        # Оплачиваем команду
        stage_cost = team['total_cost']
        if game_state.can_afford(stage_cost, "btc_balance"):
            game_state.spend_currency(stage_cost, "btc_balance")
            print(f"{Colors.MONEY}[-] Оплачено команде: {stage_cost} BTC{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}Недостаточно средств для оплаты команды!{Colors.RESET}")
            success = False  # Неоплаченная команда саботирует миссию

        return success

    def _team_coordination_minigame(self, team: dict) -> bool:
        """Мини-игра координации команды"""
        print(f"\n{Colors.WARNING}⚡ КРИТИЧЕСКИЙ МОМЕНТ: Требуется координация!{Colors.RESET}")

        # Генерируем последовательность действий
        actions = ["HACKER", "SOCIAL", "LOOKOUT"]
        sequence = [random.choice(actions) for _ in range(5)]

        print(f"Введите последовательность ролей в правильном порядке:")
        print(f"H - Hacker, S - Social Engineer, L - Lookout")
        print(f"\nПоследовательность: {' -> '.join(sequence)}")

        user_input = input(f"{Colors.PROMPT}Ваш ввод (например: HSLHL): {Colors.RESET}").upper()

        expected = "".join([action[0] for action in sequence])

        if user_input == expected:
            print(f"{Colors.SUCCESS}✅ Отличная координация!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.ERROR}❌ Плохая координация! Ожидалось: {expected}{Colors.RESET}")
            return False

    def _analyze_moral_profile(self, choices: list) -> str:
        """Анализирует моральный профиль игрока"""
        if not choices:
            return "Неопределенный"

        # Упрощенный анализ на основе паттернов выборов
        profiles = {
            "Праведник": ["protect", "anonymous_leak", "minimize_damage", "leave_charity"],
            "Прагматик": ["sell_to_media", "use_and_abandon", "proceed"],
            "Макиавеллист": ["blackmail_officials", "steal_all", "abandon"],
            "Альтруист": ["donate_anonymous", "protect", "abort"]
        }

        scores = {}
        for profile, keywords in profiles.items():
            score = sum(1 for choice in choices if any(keyword in choice for keyword in keywords))
            scores[profile] = score

        if not any(scores.values()):
            return "Непредсказуемый"

        return max(scores, key=scores.get)

    # Дополнительные методы-заглушки для отсутствующих методов
    def _check_stage_requirements(self, stage_data: dict) -> bool:
        """Проверяет требования для этапа миссии"""
        req_skills = stage_data.get("req_skills", {})
        for skill, level in req_skills.items():
            if game_state.get_skill(skill) < level:
                print(f"{Colors.ERROR}Недостаточно навыка {skill}: требуется {level}{Colors.RESET}")
                return False

        req_items = stage_data.get("req_items", [])
        inventory = game_state.get_stat("inventory", [])
        for item in req_items:
            if item not in inventory:
                print(f"{Colors.ERROR}Требуется предмет: {item}{Colors.RESET}")
                return False

        return True

    def _execute_mission_stage(self, stage_data: dict) -> bool:
        """Выполняет этап миссии"""
        stage_type = stage_data.get("type", "normal")

        if stage_type == "minigame":
            minigame_type = stage_data.get("minigame", "random")
            if minigame_type == "random":
                _, game = minigame_hub.get_random_minigame()
            else:
                game = minigame_hub.games.get(minigame_type)

            if game:
                return game.play()

        # Обычное выполнение этапа
        difficulty = stage_data.get("difficulty", 50)

        # Расчет шанса успеха
        player_skills = sum(game_state.get_skill(s) for s in ["scanning", "cracking", "stealth", "social_eng"])
        success_chance = max(10, min(90, 100 - difficulty + player_skills))

        return random.randint(1, 100) <= success_chance

    def _apply_stage_rewards(self, stage_data: dict) -> None:
        """Применяет награды за этап"""
        rewards = stage_data.get("rewards", {})

        if "btc" in rewards:
            game_state.earn_currency(rewards["btc"], "btc_balance")
            print(f"{Colors.MONEY}[+] {rewards['btc']} BTC{Colors.RESET}")

        if "rep" in rewards:
            game_state.modify_stat("reputation", rewards["rep"])
            print(f"{Colors.REP}[+] {rewards['rep']} репутации{Colors.RESET}")

        if "items" in rewards:
            for item in rewards["items"]:
                game_state.add_to_inventory(item)
                print(f"{Colors.SUCCESS}[+] Получен предмет: {item}{Colors.RESET}")

    def _complete_multi_stage_mission(self, mission_id: str, mission_data: dict) -> bool:
        """Завершает многоэтапную миссию"""
        print(f"\n{Colors.SUCCESS}🎉 ВСЕ ЭТАПЫ МИССИИ ЗАВЕРШЕНЫ!{Colors.RESET}")
        return self._complete_mission(mission_data)

    def _complete_team_mission(self, mission_id: str, mission_data: dict) -> bool:
        """Завершает командную миссию"""
        team = self.active_teams.get(mission_id)
        if team:
            print(f"\n{Colors.SUCCESS}👥 КОМАНДНАЯ МИССИЯ ЗАВЕРШЕНА!{Colors.RESET}")

            # Бонус за хорошую синергию команды
            if team['synergy'] >= 80:
                bonus_btc = mission_data.get("reward_btc", 0) * 0.2
                game_state.earn_currency(bonus_btc, "btc_balance")
                print(f"{Colors.MONEY}[БОНУС] +{bonus_btc} BTC за отличную командную работу!{Colors.RESET}")

            # Убираем команду
            del self.active_teams[mission_id]

        return self._complete_mission(mission_data)

    def _handle_team_mission_failure(self, mission_data: dict, team: dict) -> bool:
        """Обрабатывает провал командной миссии"""
        print(f"{Colors.ERROR}👥 КОМАНДНАЯ МИССИЯ ПРОВАЛЕНА!{Colors.RESET}")

        # Дополнительные штрафы за провал команды
        betrayal_chance = 100 - team['synergy']
        if random.randint(1, 100) <= betrayal_chance:
            print(f"{Colors.DANGER}💔 Один из членов команды предал вас!{Colors.RESET}")
            additional_heat = random.randint(20, 40)
            game_state.modify_stat("heat_level", additional_heat)

        return self._handle_mission_failure(mission_data)


# Дополнительные функции для визуализации (статические методы)
def show_mission_timer(time_remaining: float, time_limit: float) -> None:
    """Показывает таймер миссии с визуальными эффектами"""
    percentage = (time_remaining / time_limit) * 100 if time_limit > 0 else 0

    if percentage > 50:
        color = Colors.SUCCESS
        icon = "⏰"
    elif percentage > 20:
        color = Colors.WARNING
        icon = "⚠️"
    else:
        color = Colors.ERROR
        icon = "🚨"

    bar_length = 20
    filled = int((percentage / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)

    print(f"\n{color}{icon} ВРЕМЯ: [{bar}] {time_remaining:.1f}ч / {time_limit}ч{Colors.RESET}")

    if percentage <= 10:
        pulse_text(f"КРИТИЧЕСКОЕ ВРЕМЯ!", Colors.ERROR, 2)

def show_team_coordination_visual(team_members: list, action: str) -> None:
    """Визуализация командной работы"""
    print(f"\n{Colors.INFO}👥 КОМАНДНАЯ КООРДИНАЦИЯ{Colors.RESET}")

    # Показываем участников
    roles_icons = {
        "hacker": "💻",
        "social_engineer": "🎭",
        "lookout": "👁️",
        "specialist": "⚡"
    }

    for member in team_members:
        icon = roles_icons.get(member['role'], "👤")
        loyalty_color = Colors.SUCCESS if member['loyalty'] >= 70 else Colors.WARNING if member[
                                                                                                   'loyalty'] >= 40 else Colors.ERROR

        print(f"   {icon} {member['name']} ({loyalty_color}{member['loyalty']}%{Colors.RESET})")

    # Анимация действия
    if action == "execute":
        animate_text(">>> ВЫПОЛНЕНИЕ ОПЕРАЦИИ <<<", 3, 0.8)
    elif action == "planning":
        typing_effect("Команда разрабатывает план атаки...", 0.05)
    elif action == "recruit":
        typing_effect("Поиск подходящих кандидатов...", 0.04)

def show_moral_choice_visual(choice_data: dict) -> None:
    """Визуализация морального выбора"""
    print(f"\n{Colors.STORY}━━━━━━━━━━━━━━━━ МОРАЛЬНАЯ ДИЛЕММА ━━━━━━━━━━━━━━━━{Colors.RESET}")

    # Обрамляем вопрос в рамку
    boxed_text(choice_data['question'], color=Colors.STORY)

    print(f"\n{Colors.INFO}🤔 Ваши варианты действий:{Colors.RESET}")

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
                print(f"      {Colors.SUCCESS}[+{rep_change} репутации]{Colors.RESET}")
            elif rep_change < 0:
                print(f"      {Colors.ERROR}[{rep_change} репутации]{Colors.RESET}")

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

    print(f"\n{Colors.DANGER}━━━━━━━━━━━━━━━━ НЕОЖИДАННОЕ СОБЫТИЕ ━━━━━━━━━━━━━━━━{Colors.RESET}")

    # Мигающее предупреждение
    pulse_text(f"{icon} {event_data['desc']}", Colors.WARNING, 3)

    # Показываем эффекты
    effects = event_data.get("effects", {})
    if effects:
        print(f"\n{Colors.INFO}📊 Влияние на миссию:{Colors.RESET}")

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
    print(f"\n{Colors.SUCCESS}━━━━━━━━━━━━━━━━ ЭТАП ЗАВЕРШЕН ━━━━━━━━━━━━━━━━{Colors.RESET}")

    # Прогресс бар этапов
    stage_bar = ""
    for i in range(total_stages):
        if i < stage_number:
            stage_bar += f"{Colors.SUCCESS}█{Colors.RESET}"
        elif i == stage_number:
            stage_bar += f"{Colors.WARNING}█{Colors.RESET}"
        else:
            stage_bar += f"{Colors.DARK_GRAY}░{Colors.RESET}"

    print(f"\n   ✅ {stage_name}")
    print(f"   Прогресс: [{stage_bar}] {stage_number + 1}/{total_stages}")

    if stage_number + 1 < total_stages:
        print(f"\n{Colors.INFO}🎯 Переход к следующему этапу...{Colors.RESET}")
    else:
        print(f"\n{Colors.SUCCESS}🎉 ВСЕ ЭТАПЫ ЗАВЕРШЕНЫ!{Colors.RESET}")

def show_team_recruitment_visual(candidates: list) -> None:
    """Визуализация набора команды"""
    print(f"\n{Colors.WARNING}━━━━━━━━━━━━━━━━ НАБОР КОМАНДЫ ━━━━━━━━━━━━━━━━{Colors.RESET}")

    for i, candidate in enumerate(candidates, 1):
        # Цвет в зависимости от навыка
        skill_level = candidate['skill_level']
        if skill_level >= 8:
            skill_color = Colors.SUCCESS
            skill_desc = "ЭЛИТНЫЙ"
        elif skill_level >= 6:
            skill_color = Colors.WARNING
            skill_desc = "ОПЫТНЫЙ"
        elif skill_level >= 4:
            skill_color = Colors.INFO
            skill_desc = "СРЕДНИЙ"
        else:
            skill_color = Colors.ERROR
            skill_desc = "НОВИЧОК"

        # Роль с иконкой
        role_icons = {
            "hacker": "💻",
            "social_engineer": "🎭",
            "lookout": "👁️",
            "specialist": "⚡"
        }
        role_icon = role_icons.get(candidate['role'], "👤")

        print(f"\n   {i}. {role_icon} {Colors.BRIGHT_GREEN}{candidate['name']}{Colors.RESET}")
        print(f"      Роль: {candidate['role']}")
        print(f"      Навык: {skill_color}{skill_level}/10 ({skill_desc}){Colors.RESET}")
        print(f"      Лояльность: {candidate['loyalty']}%")
        print(f"      Стоимость: {Colors.MONEY}{candidate['cost']} BTC/этап{Colors.RESET}")
        print(f"      Особенности: {Colors.INFO}{candidate['traits']}{Colors.RESET}")

def show_mission_failure_sequence(reason: str) -> None:
    """Визуализация провала миссии"""
    print(f"\n{Colors.ERROR}━━━━━━━━━━━━━━━━ МИССИЯ ПРОВАЛЕНА ━━━━━━━━━━━━━━━━{Colors.RESET}")

    # ASCII арт провала
    failure_art = f"""
    {Colors.ERROR}
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░██░░░░██░░░░░░░░░░░░░░░░░░░░░
        ░██░░██░░░░██░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░██████████░░░░░░░░░░░░░░
        ░░░░░██░░░░░░░░░░██░░░░░░░░░░░░
        ░░░░██░░░░░░░░░░░░░██░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    {Colors.RESET}"""

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
        print(f"\r{Colors.ERROR}💥 {message} 💥{Colors.RESET}", end='', flush=True)
        time.sleep(0.5)
        print(f"\r{' ' * (len(message) + 6)}", end='', flush=True)
        time.sleep(0.5)

    print(f"\r{Colors.ERROR}💥 {message} 💥{Colors.RESET}")

def show_mission_success_sequence(mission_name: str, rewards: dict) -> None:
    """Визуализация успешного завершения миссии"""
    print(f"\n{Colors.SUCCESS}━━━━━━━━━━━━━━━━ МИССИЯ ВЫПОЛНЕНА ━━━━━━━━━━━━━━━━{Colors.RESET}")

    # ASCII арт успеха
    success_art = f"""
    {Colors.SUCCESS}
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
            ░░░░░░░░░░██████░░░░░░░░░░░░░░
            ░░░░░░░░██░░░░░░██░░░░░░░░░░░░
            ░░░░░░██░░░░░░░░░░██░░░░░░░░░░
            ░░░░██░░░░██░░██░░░░██░░░░░░░░
            ░░░░██░░░░░░░░░░░░░░██░░░░░░░░
            ░░░░░░██░░██████░░██░░░░░░░░░░
            ░░░░░░░░██░░░░░░██░░░░░░░░░░░░
            ░░░░░░░░░░██████░░░░░░░░░░░░░░
    {Colors.RESET}"""

    print(success_art)

    # Анимированный заголовок
    animate_text(f"🎉 {mission_name.upper()} - ЗАВЕРШЕНО! 🎉", 2, 1.0)

    # Показываем награды с анимацией
    print(f"\n{Colors.MONEY}💰 ПОЛУЧЕННЫЕ НАГРАДЫ:{Colors.RESET}")

    for reward_type, value in rewards.items():
        time.sleep(0.5)
        if reward_type == "btc":
            print(f"   💎 {Colors.MONEY}+{value} BTC{Colors.RESET}")
        elif reward_type == "reputation":
            print(f"   📈 {Colors.REP}+{value} репутации{Colors.RESET}")
        elif reward_type == "items":
            for item in value if isinstance(value, list) else [value]:
                print(f"   📦 {Colors.INFO}Получен предмет: {item}{Colors.RESET}")
        elif reward_type == "contacts":
            for contact in value if isinstance(value, list) else [value]:
                print(f"   📱 {Colors.WARNING}Новый контакт: {contact}{Colors.RESET}")

def show_countdown_timer(seconds: int, message: str = "Начало операции через") -> None:
    """Обратный отсчет с визуальными эффектами"""
    for i in range(seconds, 0, -1):
        # Цвет меняется по мере приближения к нулю
        if i > 5:
            color = Colors.INFO
        elif i > 2:
            color = Colors.WARNING
        else:
            color = Colors.ERROR

        print(f"\r{color}{message}: {i}s{Colors.RESET}", end='', flush=True)

        # Звуковые эффекты для последних секунд
        if i <= 3:
            print("\a", end='')  # Системный звук

        time.sleep(1)

    print(f"\r{Colors.SUCCESS}🚀 СТАРТ!{' ' * 30}{Colors.RESET}")

def show_hacking_progress(target: str, progress_steps: list) -> None:
    """Показывает прогресс взлома с реалистичными этапами"""
    print(f"\n{Colors.INFO}🎯 Цель: {target}{Colors.RESET}")
    print(f"{Colors.HEADER}━━━━━━━━━━━━━━━━ ПРОЦЕСС ВЗЛОМА ━━━━━━━━━━━━━━━━{Colors.RESET}")

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

        print(f"\n{Colors.WARNING}[{i + 1}/{len(progress_steps)}] {icon} {description}{Colors.RESET}")

        # Прогресс бар для этапа
        for j in range(duration * 2):
            progress = (j + 1) / (duration * 2)
            bar_length = 30
            filled = int(progress * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)

            percentage = int(progress * 100)
            print(f"\r         [{Colors.SUCCESS}{bar}{Colors.RESET}] {percentage}%", end='', flush=True)
            time.sleep(0.5)

        print(f" {Colors.SUCCESS}✓{Colors.RESET}")

    print(f"\n{Colors.SUCCESS}🎉 ВЗЛОМ ЗАВЕРШЕН УСПЕШНО!{Colors.RESET}")


# Глобальный экземпляр системы миссий
mission_system = MissionSystem()