"""
Система фракций для XSS Game 0.3.0
"""

import random
import time
from typing import Dict, List, Optional, Tuple

from ui.colors import XSSColors as Colors
from ui.effects import typing_effect, show_ascii_art, boxed_text
from core.game_state import game_state
from systems.audio import audio_system
from config.game_data import FACTIONS


class FactionSystem:
    """Система управления фракциями"""
    
    def __init__(self):
        self.factions = FACTIONS
        self.faction_reputation = {
            "whitehats": 0,
            "blackhats": 0,
            "grayhats": 0
        }
        self.faction_conflicts = {
            ("whitehats", "blackhats"): "hostile",
            ("whitehats", "grayhats"): "neutral", 
            ("blackhats", "grayhats"): "neutral"
        }
    
    def show_faction_selection(self) -> None:
        """Показывает экран выбора фракции"""
        if game_state.get_stat("faction"):
            print(f"{Colors.WARNING}Вы уже состоите во фракции: {game_state.get_stat('faction')}{Colors.RESET}")
            self.show_faction_info()
            return
        
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━ ВЫБОР ФРАКЦИИ ━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        typing_effect(f"{Colors.STORY}Настало время выбрать свой путь в мире хакинга...{Colors.RESET}")
        typing_effect(f"{Colors.INFO}Каждая фракция открывает уникальные возможности и миссии.{Colors.RESET}")
        
        # Показываем фракции
        faction_list = list(self.factions.items())
        for i, (faction_id, faction_data) in enumerate(faction_list, 1):
            self._display_faction_preview(i, faction_id, faction_data)
        
        print(f"\n{Colors.WARNING}⚠️ ВНИМАНИЕ: Выбор фракции повлияет на весь ваш путь в игре!{Colors.RESET}")
        print(f"{Colors.INFO}Вы сможете сменить фракцию позже, но это будет стоить репутации.{Colors.RESET}")
        
        while True:
            choice = audio_system.get_input_with_sound(
                f"\n{Colors.PROMPT}Выберите фракцию (1-3) или 'info [номер]' для подробностей: {Colors.RESET}"
            ).strip().lower()
            
            if choice.startswith('info '):
                try:
                    faction_num = int(choice.split()[1])
                    if 1 <= faction_num <= 3:
                        faction_id = list(self.factions.keys())[faction_num - 1]
                        self._show_detailed_faction_info(faction_id)
                    else:
                        print(f"{Colors.ERROR}Неверный номер фракции{Colors.RESET}")
                except (ValueError, IndexError):
                    print(f"{Colors.ERROR}Неверный формат команды{Colors.RESET}")
            
            elif choice in ['1', '2', '3']:
                faction_id = list(self.factions.keys())[int(choice) - 1]
                if self._confirm_faction_choice(faction_id):
                    self._join_faction(faction_id)
                    break
            
            elif choice == 'skip':
                print(f"{Colors.INFO}Вы можете выбрать фракцию позже командой 'faction'{Colors.RESET}")
                break
            
            else:
                print(f"{Colors.ERROR}Неверный выбор. Введите 1, 2, 3 или 'info [номер]'{Colors.RESET}")
    
    def _display_faction_preview(self, number: int, faction_id: str, faction_data: dict) -> None:
        """Отображает краткую информацию о фракции"""
        # Определяем иконку и цвет
        faction_icons = {
            "whitehats": "🛡️",
            "blackhats": "☠️", 
            "grayhats": "🎭"
        }
        
        faction_colors = {
            "whitehats": Colors.SUCCESS,
            "blackhats": Colors.DANGER,
            "grayhats": Colors.WARNING
        }
        
        icon = faction_icons.get(faction_id, "❓")
        color = faction_colors.get(faction_id, Colors.INFO)
        
        print(f"\n{color}═══ {number}. {icon} {faction_data['name']} ═══{Colors.RESET}")
        print(f"{Colors.INFO}{faction_data['desc']}{Colors.RESET}")
        
        # Ключевые особенности
        bonuses = faction_data.get('bonuses', {})
        if bonuses:
            print(f"{Colors.SKILL}Особенности:{Colors.RESET}")
            for bonus, value in bonuses.items():
                if bonus == "reputation_multiplier":
                    print(f"  • Репутация x{value}")
                elif bonus == "heat_reduction":
                    print(f"  • Снижение Heat Level на {value}%")
                elif bonus == "btc_multiplier":
                    print(f"  • Награды BTC x{value}")
                elif bonus == "skill_boost":
                    print(f"  • Все навыки +{value}")
                elif bonus == "special_market":
                    print(f"  • Доступ к специальному рынку")
    
    def _show_detailed_faction_info(self, faction_id: str) -> None:
        """Показывает подробную информацию о фракции"""
        faction_data = self.factions[faction_id]
        
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        # Большой ASCII арт для каждой фракции
        if faction_id == "whitehats":
            show_ascii_art("shield")
        elif faction_id == "blackhats":
            show_ascii_art("skull")
        else:
            show_ascii_art("hack")
        
        boxed_text(
            f"{faction_data['name']}\n\n{faction_data['desc']}\n\n"
            f"Философия: {faction_data.get('philosophy', 'Неизвестно')}",
            color=Colors.INFO
        )
        
        # Уникальные миссии
        unique_missions = faction_data.get('exclusive_missions', [])
        if unique_missions:
            print(f"\n{Colors.WARNING}🎯 ЭКСКЛЮЗИВНЫЕ МИССИИ:{Colors.RESET}")
            for mission in unique_missions[:3]:
                print(f"  • {mission}")
            if len(unique_missions) > 3:
                print(f"  • ...и еще {len(unique_missions) - 3} миссий")
        
        # Особые возможности
        special_features = faction_data.get('special_features', [])
        if special_features:
            print(f"\n{Colors.SKILL}✨ ОСОБЫЕ ВОЗМОЖНОСТИ:{Colors.RESET}")
            for feature in special_features:
                print(f"  • {feature}")
        
        # Враги и союзники
        enemies = faction_data.get('enemies', [])
        allies = faction_data.get('allies', [])
        
        if enemies:
            print(f"\n{Colors.ERROR}⚔️ ВРАГИ: {', '.join(enemies)}{Colors.RESET}")
        if allies:
            print(f"{Colors.SUCCESS}🤝 СОЮЗНИКИ: {', '.join(allies)}{Colors.RESET}")
        
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    
    def _confirm_faction_choice(self, faction_id: str) -> bool:
        """Подтверждение выбора фракции"""
        faction_data = self.factions[faction_id]
        
        print(f"\n{Colors.WARNING}╔══════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.WARNING}║           ПОДТВЕРЖДЕНИЕ              ║{Colors.RESET}")
        print(f"{Colors.WARNING}╚══════════════════════════════════════╝{Colors.RESET}")
        
        print(f"\nВы выбираете фракцию: {Colors.SUCCESS}{faction_data['name']}{Colors.RESET}")
        print(f"{Colors.INFO}Это решение повлияет на всю вашу игру.{Colors.RESET}")
        
        confirm = audio_system.get_input_with_sound(
            f"\n{Colors.PROMPT}Подтвердить выбор? (yes/no): {Colors.RESET}"
        ).lower()
        
        return confirm in ['yes', 'y', 'да', 'д']
    
    def _join_faction(self, faction_id: str) -> None:
        """Присоединение к фракции"""
        faction_data = self.factions[faction_id]
        
        # Анимация присоединения
        print(f"\n{Colors.INFO}Подключение к защищенному каналу фракции...{Colors.RESET}")
        time.sleep(1)
        
        audio_system.play_sound("faction_join")
        
        # Драматичное сообщение
        welcome_messages = {
            "whitehats": [
                "Добро пожаловать в ряды защитников киберпространства!",
                "Ваша миссия - защищать невинных от кибертеррористов.",
                "Помните: с великой силой приходит великая ответственность."
            ],
            "blackhats": [
                "Добро пожаловать в темную сторону интернета...",
                "Здесь правят только сила и хитрость.",
                "Доверяй только себе. Все остальные - лишь инструменты."
            ],
            "grayhats": [
                "Добро пожаловать в мир без границ.",
                "Ваш путь не ограничен чужой моралью.",
                "Свобода выбора - ваша главная сила."
            ]
        }
        
        messages = welcome_messages.get(faction_id, ["Добро пожаловать!"])
        for message in messages:
            typing_effect(f"{Colors.STORY}[ФРАКЦИЯ] {message}{Colors.RESET}", 0.03)
            time.sleep(1)
        
        # Устанавливаем фракцию
        game_state.set_stat("faction", faction_id)
        self.faction_reputation[faction_id] = 25  # Стартовая репутация
        
        # Стартовые бонусы
        self._apply_faction_bonuses(faction_id)
        
        # Специальные награды
        self._give_faction_starter_pack(faction_id)
        
        show_ascii_art("level_up")
        print(f"\n{Colors.SUCCESS}✅ Вы успешно присоединились к фракции {faction_data['name']}!{Colors.RESET}")
        print(f"{Colors.INFO}Новые миссии и возможности теперь доступны в меню.{Colors.RESET}")
    
    def _apply_faction_bonuses(self, faction_id: str) -> None:
        """Применяет бонусы фракции"""
        faction_data = self.factions[faction_id]
        bonuses = faction_data.get('bonuses', {})
        
        print(f"\n{Colors.SKILL}🎁 ПОЛУЧЕНЫ БОНУСЫ ФРАКЦИИ:{Colors.RESET}")
        
        for bonus, value in bonuses.items():
            if bonus == "skill_boost":
                for skill in ["scanning", "cracking", "stealth", "social_eng"]:
                    game_state.modify_skill(skill, value)
                print(f"  • Все навыки +{value}")
            
            elif bonus == "heat_reduction":
                current_heat = game_state.get_stat("heat_level", 0)
                new_heat = max(0, current_heat - value)
                game_state.set_stat("heat_level", new_heat)
                print(f"  • Heat Level -{value}% (текущий: {new_heat}%)")
            
            elif bonus == "reputation_bonus":
                game_state.modify_stat("reputation", value)
                print(f"  • Репутация +{value}")
    
    def _give_faction_starter_pack(self, faction_id: str) -> None:
        """Выдает стартовый набор фракции"""
        starter_packs = {
            "whitehats": {
                "items": ["ethical_hacker_toolkit", "bug_bounty_access"],
                "btc": 100,
                "contacts": ["corp_security_chief"]
            },
            "blackhats": {
                "items": ["dark_web_access", "anonymous_proxy"],
                "btc": 200,
                "contacts": ["underground_broker"]
            },
            "grayhats": {
                "items": ["flexible_toolkit", "neutral_contacts"],
                "btc": 150,
                "contacts": ["information_broker"]
            }
        }
        
        pack = starter_packs.get(faction_id, {})
        
        # Добавляем предметы
        items = pack.get('items', [])
        for item in items:
            game_state.add_to_inventory(item)
            print(f"  📦 Получен предмет: {item}")
        
        # Добавляем BTC
        btc_bonus = pack.get('btc', 0)
        if btc_bonus > 0:
            game_state.earn_currency(btc_bonus, 'btc_balance')
            print(f"  💰 Получено {btc_bonus} BTC")
        
        # Добавляем контакты
        contacts = pack.get('contacts', [])
        for contact in contacts:
            game_state.add_contact(contact)
            print(f"  📱 Новый контакт: {contact}")
    
    def show_faction_info(self) -> None:
        """Показывает информацию о текущей фракции"""
        current_faction = game_state.get_stat("faction")
        
        if not current_faction:
            print(f"{Colors.WARNING}Вы не состоите ни в одной фракции{Colors.RESET}")
            print(f"{Colors.INFO}Используйте команду 'join_faction' для выбора{Colors.RESET}")
            return
        
        faction_data = self.factions[current_faction]
        faction_rep = self.faction_reputation.get(current_faction, 0)
        
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━ ВАША ФРАКЦИЯ ━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        # Основная информация
        print(f"\n🏛️ {Colors.SUCCESS}{faction_data['name']}{Colors.RESET}")
        print(f"{Colors.INFO}{faction_data['desc']}{Colors.RESET}")
        
        # Репутация во фракции
        rep_color = Colors.SUCCESS if faction_rep >= 75 else Colors.WARNING if faction_rep >= 25 else Colors.ERROR
        print(f"\n📊 Репутация во фракции: {rep_color}{faction_rep}/100{Colors.RESET}")
        
        # Статус в других фракциях
        print(f"\n{Colors.INFO}Отношения с другими фракциями:{Colors.RESET}")
        for other_faction, other_data in self.factions.items():
            if other_faction != current_faction:
                other_rep = self.faction_reputation.get(other_faction, 0)
                
                # Определяем отношения
                conflict_key = tuple(sorted([current_faction, other_faction]))
                relationship = self.faction_conflicts.get(conflict_key, "neutral")
                
                if relationship == "hostile":
                    rel_color = Colors.ERROR
                    rel_icon = "⚔️"
                elif relationship == "allied":
                    rel_color = Colors.SUCCESS
                    rel_icon = "🤝"
                else:
                    rel_color = Colors.WARNING
                    rel_icon = "🤷"
                
                print(f"  {rel_icon} {other_data['name']}: {rel_color}{relationship.title()}{Colors.RESET} (Rep: {other_rep})")
        
        # Доступные бонусы
        bonuses = faction_data.get('bonuses', {})
        if bonuses:
            print(f"\n{Colors.SKILL}🎁 Активные бонусы:{Colors.RESET}")
            for bonus, value in bonuses.items():
                if bonus == "reputation_multiplier":
                    print(f"  • Репутация x{value} при выполнении миссий")
                elif bonus == "heat_reduction":
                    print(f"  • Снижение Heat Level на {value}% при провалах")
                elif bonus == "btc_multiplier":
                    print(f"  • Награды BTC x{value}")
                elif bonus == "skill_boost":
                    print(f"  • Постоянный бонус ко всем навыкам: +{value}")
        
        # Доступные эксклюзивные миссии
        exclusive_missions = faction_data.get('exclusive_missions', [])
        if exclusive_missions:
            print(f"\n{Colors.WARNING}🎯 Эксклюзивные миссии доступны:{Colors.RESET}")
            available_count = len([m for m in exclusive_missions if not game_state.is_mission_completed(m)])
            print(f"  • Доступно: {available_count}/{len(exclusive_missions)} миссий")
        
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    def show_faction_missions(self) -> None:
        """Показывает миссии текущей фракции"""
        current_faction = game_state.get_stat("faction")

        if not current_faction:
            print(f"{Colors.WARNING}Вы не состоите ни в одной фракции{Colors.RESET}")
            return

        # Импортируем mission_system (добавьте в начало файла)
        from gameplay.missions import mission_system

        faction_data = self.factions[current_faction]
        exclusive_missions = faction_data.get('exclusive_missions', [])

        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━ МИССИИ ФРАКЦИИ ━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"\n{Colors.SUCCESS}🏛️ {faction_data['name']}{Colors.RESET}")

        if not exclusive_missions:
            print(f"\n{Colors.WARNING}У вашей фракции нет эксклюзивных миссий{Colors.RESET}")
            return

        available_count = 0
        completed_count = 0

        print(f"\n{Colors.INFO}📋 ЭКСКЛЮЗИВНЫЕ МИССИИ:{Colors.RESET}")

        for mission_id in exclusive_missions:
            if mission_id in mission_system.missions:
                mission_data = mission_system.missions[mission_id]
                is_completed = game_state.is_mission_completed(mission_id)

                if is_completed:
                    completed_count += 1
                    status_icon = "✅"
                    status_color = Colors.SUCCESS
                else:
                    available_count += 1
                    status_icon = "📋"
                    status_color = Colors.WARNING

                print(f"\n   {status_icon} {status_color}{mission_id}{Colors.RESET}")
                print(f"      {mission_data.get('name', 'Неизвестная миссия')}")
                print(f"      Награда: {mission_data.get('reward_btc', 0)} BTC")

                if not is_completed:
                    req_rep = mission_data.get('req_rep', 0)
                    current_rep = game_state.get_stat('reputation', 0)
                    if current_rep >= req_rep:
                        print(f"      {Colors.SUCCESS}✓ Доступна для выполнения{Colors.RESET}")
                    else:
                        print(f"      {Colors.ERROR}✗ Требуется репутация: {req_rep}{Colors.RESET}")

        print(f"\n{Colors.INFO}📊 Статистика:{Colors.RESET}")
        print(f"   Доступно: {available_count}")
        print(f"   Выполнено: {completed_count}")
        print(f"   Всего: {len(exclusive_missions)}")

        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    
    def change_faction(self, new_faction_id: str) -> bool:
        """Смена фракции (с штрафами)"""
        current_faction = game_state.get_stat("faction")
        
        if not current_faction:
            print(f"{Colors.ERROR}Вы не состоите ни в одной фракции{Colors.RESET}")
            return False
        
        if current_faction == new_faction_id:
            print(f"{Colors.WARNING}Вы уже состоите в этой фракции{Colors.RESET}")
            return False
        
        if new_faction_id not in self.factions:
            print(f"{Colors.ERROR}Неизвестная фракция: {new_faction_id}{Colors.RESET}")
            return False
        
        # Проверяем требования для смены
        if not self._check_faction_change_requirements(current_faction, new_faction_id):
            return False
        
        # Предупреждаем о последствиях
        if not self._confirm_faction_change(current_faction, new_faction_id):
            return False
        
        # Применяем штрафы
        self._apply_faction_change_penalties(current_faction)
        
        # Меняем фракцию
        game_state.set_stat("faction", new_faction_id)
        self.faction_reputation[new_faction_id] = max(10, self.faction_reputation.get(new_faction_id, 0))
        
        print(f"\n{Colors.SUCCESS}✅ Вы перешли во фракцию {self.factions[new_faction_id]['name']}{Colors.RESET}")
        audio_system.play_sound("faction_change")
        
        return True
    
    def _check_faction_change_requirements(self, current_faction: str, new_faction_id: str) -> bool:
        """Проверяет требования для смены фракции"""
        # Базовые требования
        player_rep = game_state.get_stat("reputation", 0)
        required_rep = 50  # Минимальная репутация для смены
        
        if player_rep < required_rep:
            print(f"{Colors.ERROR}Недостаточно репутации для смены фракции (нужно: {required_rep}){Colors.RESET}")
            return False
        
        # Проверяем враждебность фракций
        conflict_key = tuple(sorted([current_faction, new_faction_id]))
        relationship = self.faction_conflicts.get(conflict_key, "neutral")
        
        if relationship == "hostile":
            faction_rep = self.faction_reputation.get(new_faction_id, 0)
            if faction_rep < 25:
                print(f"{Colors.ERROR}Враждебные фракции! Нужна репутация 25+ в целевой фракции{Colors.RESET}")
                return False
        
        return True
    
    def _confirm_faction_change(self, current_faction: str, new_faction_id: str) -> bool:
        """Подтверждение смены фракции"""
        current_name = self.factions[current_faction]['name']
        new_name = self.factions[new_faction_id]['name']
        
        print(f"\n{Colors.DANGER}⚠️ ПРЕДУПРЕЖДЕНИЕ О СМЕНЕ ФРАКЦИИ ⚠️{Colors.RESET}")
        print(f"{Colors.WARNING}Вы покидаете: {current_name}{Colors.RESET}")
        print(f"{Colors.WARNING}Вы вступаете в: {new_name}{Colors.RESET}")
        
        print(f"\n{Colors.ERROR}ШТРАФЫ:{Colors.RESET}")
        print(f"  • Потеря 50% репутации в старой фракции")
        print(f"  • Потеря доступа к эксклюзивным миссиям")
        print(f"  • Возможная враждебность со стороны бывших союзников")
        print(f"  • Штраф -25 к общей репутации")
        
        confirm = audio_system.get_input_with_sound(
            f"\n{Colors.PROMPT}Подтвердить смену фракции? (yes/no): {Colors.RESET}"
        ).lower()
        
        return confirm in ['yes', 'y']
    
    def _apply_faction_change_penalties(self, old_faction: str) -> None:
        """Применяет штрафы за смену фракции"""
        # Снижаем репутацию в старой фракции
        old_rep = self.faction_reputation.get(old_faction, 0)
        self.faction_reputation[old_faction] = max(0, old_rep // 2)
        
        # Общий штраф репутации
        game_state.modify_stat("reputation", -25)
        
        # Повышаем heat level
        game_state.modify_stat("heat_level", 15)
        
        print(f"\n{Colors.ERROR}[-] Применены штрафы за предательство{Colors.RESET}")
    
    def modify_faction_reputation(self, faction_id: str, amount: int) -> None:
        """Изменяет репутацию во фракции"""
        if faction_id in self.faction_reputation:
            old_rep = self.faction_reputation[faction_id]
            self.faction_reputation[faction_id] = max(0, min(100, old_rep + amount))
            
            if amount > 0:
                print(f"{Colors.SUCCESS}[+] Репутация в {faction_id}: +{amount}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}[-] Репутация в {faction_id}: {amount}{Colors.RESET}")
    
    def get_faction_missions(self, faction_id: str = None) -> List[str]:
        """Получает список миссий фракции"""
        if not faction_id:
            faction_id = game_state.get_stat("faction")
        
        if not faction_id or faction_id not in self.factions:
            return []
        
        return self.factions[faction_id].get('exclusive_missions', [])
    
    def is_mission_faction_exclusive(self, mission_id: str) -> bool:
        """Проверяет, является ли миссия эксклюзивной для фракции"""
        for faction_data in self.factions.values():
            if mission_id in faction_data.get('exclusive_missions', []):
                return True
        return False
    
    def get_faction_bonuses(self, faction_id: str = None) -> Dict:
        """Получает бонусы фракции"""
        if not faction_id:
            faction_id = game_state.get_stat("faction")
        
        if not faction_id or faction_id not in self.factions:
            return {}
        
        return self.factions[faction_id].get('bonuses', {})
    
    def check_faction_conflicts(self, action_type: str, target: str = None) -> bool:
        """Проверяет конфликты фракций при действиях"""
        current_faction = game_state.get_stat("faction")
        if not current_faction:
            return True
        
        # Примеры конфликтов:
        # - WhiteHats не могут атаковать госучреждения
        # - BlackHats получают штрафы за помощь правоохранителям
        # - GrayHats могут делать все, но с меньшими бонусами
        
        faction_restrictions = {
            "whitehats": {
                "forbidden_targets": ["government", "hospital", "school"],
                "forbidden_actions": ["ransomware", "ddos_attack"]
            },
            "blackhats": {
                "forbidden_targets": ["law_enforcement"],
                "forbidden_actions": ["bug_bounty", "white_hat_consulting"]
            }
        }
        
        restrictions = faction_restrictions.get(current_faction, {})
        
        # Проверяем запрещенные цели
        forbidden_targets = restrictions.get("forbidden_targets", [])
        if target and any(ft in target.lower() for ft in forbidden_targets):
            print(f"{Colors.ERROR}❌ Ваша фракция запрещает атаки на {target}{Colors.RESET}")
            return False
        
        # Проверяем запрещенные действия
        forbidden_actions = restrictions.get("forbidden_actions", [])
        if action_type in forbidden_actions:
            print(f"{Colors.ERROR}❌ Ваша фракция не одобряет {action_type}{Colors.RESET}")
            return False
        
        return True
    
    def faction_war_event(self) -> None:
        """Случайное событие войны фракций"""
        current_faction = game_state.get_stat("faction")
        if not current_faction:
            return
        
        # Определяем враждебную фракцию
        enemy_factions = []
        for faction_id in self.factions.keys():
            if faction_id != current_faction:
                conflict_key = tuple(sorted([current_faction, faction_id]))
                if self.faction_conflicts.get(conflict_key) == "hostile":
                    enemy_factions.append(faction_id)
        
        if not enemy_factions:
            return
        
        enemy_faction = random.choice(enemy_factions)
        enemy_name = self.factions[enemy_faction]['name']
        
        print(f"\n{Colors.DANGER}🚨 ФРАКЦИОННЫЙ КОНФЛИКТ! 🚨{Colors.RESET}")
        typing_effect(f"{Colors.WARNING}Фракция {enemy_name} атакует ваши интересы!{Colors.RESET}")
        
        # Случайные эффекты войны
        war_effects = [
            {"type": "reputation_loss", "value": -10, "desc": "Потеря репутации из-за атак"},
            {"type": "heat_gain", "value": 20, "desc": "Повышение Heat Level"},
            {"type": "btc_loss", "value": 100, "desc": "Финансовые потери"},
            {"type": "mission_block", "desc": "Блокировка некоторых миссий"}
        ]
        
        effect = random.choice(war_effects)
        
        if effect["type"] == "reputation_loss":
            game_state.modify_stat("reputation", effect["value"])
        elif effect["type"] == "heat_gain":
            game_state.modify_stat("heat_level", effect["value"])
        elif effect["type"] == "btc_loss":
            game_state.modify_stat("btc_balance", -effect["value"])
        
        print(f"{Colors.ERROR}💥 {effect['desc']}{Colors.RESET}")
        
        # Возможность ответить
        choice = audio_system.get_input_with_sound(
            f"\n{Colors.PROMPT}Ответить на атаку? (yes/no): {Colors.RESET}"
        ).lower()
        
        if choice in ['yes', 'y']:
            self._faction_retaliation(enemy_faction)
    
    def _faction_retaliation(self, enemy_faction: str) -> None:
        """Ответная атака на враждебную фракцию"""
        current_faction = game_state.get_stat("faction")
        
        print(f"\n{Colors.WARNING}⚔️ Подготовка ответного удара...{Colors.RESET}")
        time.sleep(1)
        
        # Успех зависит от навыков игрока
        player_power = sum(game_state.get_skill(skill) for skill in ["cracking", "stealth", "scanning"])
        success_chance = min(80, player_power * 2)
        
        if random.randint(1, 100) <= success_chance:
            # Успешная атака
            audio_system.play_sound("hack_success")
            print(f"{Colors.SUCCESS}✅ Успешная ответная атака!{Colors.RESET}")
            
            # Награды
            rep_gain = random.randint(10, 25)
            btc_gain = random.randint(50, 200)
            
            game_state.modify_stat("reputation", rep_gain)
            game_state.earn_currency(btc_gain, "btc_balance")
            self.modify_faction_reputation(current_faction, 15)
            
            print(f"{Colors.SUCCESS}[+] Репутация: +{rep_gain}{Colors.RESET}")
            print(f"{Colors.MONEY}[+] Награда: {btc_gain} BTC{Colors.RESET}")
            
        else:
            # Провал атаки
            audio_system.play_sound("fail")
            print(f"{Colors.ERROR}❌ Ответная атака провалилась!{Colors.RESET}")
            
            # Штрафы
            heat_gain = random.randint(15, 30)
            game_state.modify_stat("heat_level", heat_gain)
            self.modify_faction_reputation(current_faction, -10)
            
            print(f"{Colors.ERROR}[!] Heat Level: +{heat_gain}%{Colors.RESET}")
    
    def daily_faction_bonus(self) -> None:
        """Ежедневный бонус от фракции"""
        current_faction = game_state.get_stat("faction")
        if not current_faction:
            return
        
        faction_rep = self.faction_reputation.get(current_faction, 0)
        
        # Бонус зависит от репутации во фракции
        if faction_rep >= 75:
            bonus_btc = random.randint(50, 100)
            bonus_rep = random.randint(2, 5)
            
            game_state.earn_currency(bonus_btc, "btc_balance")
            game_state.modify_stat("reputation", bonus_rep)
            
            print(f"\n{Colors.SUCCESS}🎁 Ежедневный бонус фракции:{Colors.RESET}")
            print(f"{Colors.MONEY}[+] {bonus_btc} BTC{Colors.RESET}")
            print(f"{Colors.REP}[+] {bonus_rep} репутации{Colors.RESET}")


# Глобальный экземпляр системы фракций
faction_system = FactionSystem()