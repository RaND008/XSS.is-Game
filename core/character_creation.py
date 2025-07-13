"""
Система создания персонажа для XSS Game 0.3.0
"""

import random
import re
import time
from typing import Dict, List, Optional, Tuple

from ui.colors import XSSColors as Colors
from ui.effects import typing_effect, show_ascii_art, boxed_text, progress_bar
from core.game_state import game_state
from systems.audio import audio_system


class CharacterCreator:
    """Система создания нового персонажа"""
    
    def __init__(self):
        self.creation_data = {}
        self.forbidden_names = [
            "admin", "root", "system", "administrator", "moderator",
            "null", "undefined", "test", "guest", "anonymous", "user"
        ]
        
        self.backgrounds = {
            "script_kiddie": {
                "name": "Script Kiddie",
                "desc": "Вы начинали с готовых скриптов и туториалов",
                "bonuses": {
                    "skills": {"scanning": 2, "cracking": 1},
                    "btc_balance": 25,
                    "items": ["basic_port_scanner"]
                },
                "story": "Ваш путь начался с форумов и YouTube-туториалов..."
            },
            "cs_student": {
                "name": "Студент Computer Science", 
                "desc": "Академическое образование в области компьютерных наук",
                "bonuses": {
                    "skills": {"scanning": 1, "cracking": 2},
                    "reputation": 10,
                    "items": ["programming_toolkit"]
                },
                "story": "Университетские знания открыли вам мир кибербезопасности..."
            },
            "sysadmin": {
                "name": "Системный администратор",
                "desc": "Опыт работы с серверами и сетевой инфраструктурой", 
                "bonuses": {
                    "skills": {"stealth": 2, "scanning": 1},
                    "usd_balance": 500,
                    "items": ["admin_tools"]
                },
                "story": "Годы работы с серверами научили вас их слабостям..."
            },
            "social_engineer": {
                "name": "Социальный инженер",
                "desc": "Мастер психологических манипуляций и обмана",
                "bonuses": {
                    "skills": {"social_eng": 2, "stealth": 1},
                    "contacts": ["insider_contact"],
                    "items": ["phishing_templates"]
                },
                "story": "Люди - самое слабое звено любой системы безопасности..."
            },
            "military": {
                "name": "Военный хакер",
                "desc": "Служба в кибервойсках или военная разведка",
                "bonuses": {
                    "skills": {"cracking": 1, "stealth": 1, "scanning": 1},
                    "reputation": 15,
                    "heat_reduction": 10,
                    "items": ["military_grade_tools"]
                },
                "story": "Государственная служба научила вас дисциплине и методичности..."
            },
            "black_hat": {
                "name": "Бывший криминал",
                "desc": "Темное прошлое в мире киберпреступности",
                "bonuses": {
                    "skills": {"cracking": 2, "stealth": 2},
                    "btc_balance": 100,
                    "heat_level": 20,
                    "contacts": ["underground_contact"]
                },
                "story": "Вы пытаетесь начать новую жизнь, но прошлое не отпускает..."
            }
        }
        
        self.starter_packs = {
            "hacker": {
                "name": "🔓 Пакет Хакера",
                "desc": "Для тех, кто предпочитает технический подход",
                "bonuses": {
                    "skills": {"cracking": 1, "scanning": 1},
                    "items": ["advanced_scanner", "password_cracker"],
                    "btc_balance": 50
                }
            },
            "ghost": {
                "name": "👻 Пакет Призрака", 
                "desc": "Для мастеров скрытности и анонимности",
                "bonuses": {
                    "skills": {"stealth": 2},
                    "items": ["elite_proxy", "trace_eraser"],
                    "heat_reduction": 15
                }
            },
            "social": {
                "name": "🎭 Пакет Социотехника",
                "desc": "Для специалистов по людям и психологии",
                "bonuses": {
                    "skills": {"social_eng": 2},
                    "items": ["social_toolkit", "fake_ids"],
                    "contacts": ["social_contact"]
                }
            },
            "entrepreneur": {
                "name": "💰 Пакет Предпринимателя",
                "desc": "Для тех, кто ценит финансовую выгоду",
                "bonuses": {
                    "usd_balance": 1000,
                    "btc_balance": 25,
                    "items": ["market_analyzer"],
                    "reputation": 5
                }
            }
        }
        
        self.terminal_themes = {
            "classic_green": {
                "name": "🟢 Классический зеленый",
                "desc": "Традиционная хакерская эстетика",
                "colors": {"primary": Colors.SUCCESS, "secondary": Colors.INFO}
            },
            "ice_blue": {
                "name": "🔵 Ледяной синий", 
                "desc": "Холодный и профессиональный стиль",
                "colors": {"primary": Colors.INFO, "secondary": Colors.WARNING}
            },
            "fire_red": {
                "name": "🔴 Огненный красный",
                "desc": "Агрессивный и опасный стиль",
                "colors": {"primary": Colors.DANGER, "secondary": Colors.ERROR}
            },
            "neon_purple": {
                "name": "🟣 Неоновый фиолетовый",
                "desc": "Киберпанк эстетика будущего",
                "colors": {"primary": Colors.HEADER, "secondary": Colors.STORY}
            },
            "matrix_mode": {
                "name": "💚 Режим Матрицы",
                "desc": "Как в фильме - зеленые символы на черном",
                "colors": {"primary": Colors.SUCCESS, "secondary": Colors.SKILL}
            }
        }
    
    def start_creation(self) -> Dict:
        """Запускает процесс создания персонажа"""
        print(f"\n{Colors.HEADER}╔══════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.HEADER}║              СОЗДАНИЕ ПЕРСОНАЖА                      ║{Colors.RESET}")
        print(f"{Colors.HEADER}║             XSS Game 0.3.0                           ║{Colors.RESET}")
        print(f"{Colors.HEADER}╚══════════════════════════════════════════════════════╝{Colors.RESET}")
        
        show_ascii_art("hack")
        
        typing_effect(f"{Colors.STORY}Добро пожаловать в мир подпольного хакинга...{Colors.RESET}")
        typing_effect(f"{Colors.INFO}Ваш путь к славе или падению начинается здесь.{Colors.RESET}")
        
        # Этап 1: Выбор никнейма
        self._step_1_nickname()
        
        # Этап 2: Предыстория
        self._step_2_background()
        
        # Этап 3: Стартовый пакет
        self._step_3_starter_pack()
        
        # Этап 4: Тема терминала
        self._step_4_terminal_theme()
        
        # Этап 5: Финализация
        self._step_5_finalization()
        
        return self.creation_data
    
    def _step_1_nickname(self) -> None:
        """Этап 1: Выбор никнейма"""
        print(f"\n{Colors.WARNING}━━━━━━━━━━━━━━━━ ЭТАП 1: НИКНЕЙМ ━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        typing_effect(f"{Colors.INFO}В мире хакинга имя - это ваша репутация.{Colors.RESET}")
        typing_effect(f"{Colors.INFO}Выберите никнейм, который будет известен по всему даркнету.{Colors.RESET}")
        
        while True:
            print(f"\n{Colors.INFO}Требования к никнейму:{Colors.RESET}")
            print(f"  • Длина: 3-20 символов")
            print(f"  • Только латинские буквы, цифры и _")
            print(f"  • Без пробелов и спецсимволов")
            print(f"  • Уникальность (не должен совпадать с системными именами)")
            
            nickname = input(f"\n{Colors.PROMPT}Введите ваш никнейм: {Colors.RESET}").strip()
            
            validation_result = self._validate_nickname(nickname)
            if validation_result["valid"]:
                # Показываем превью
                self._show_nickname_preview(nickname)
                
                confirm = input(f"\n{Colors.PROMPT}Подтвердить выбор '{nickname}'? (y/n): {Colors.RESET}").lower()
                if confirm in ['y', 'yes', 'да', 'д']:
                    self.creation_data["nickname"] = nickname
                    audio_system.play_sound("success")
                    print(f"{Colors.SUCCESS}✅ Никнейм '{nickname}' зарегистрирован!{Colors.RESET}")
                    break
            else:
                print(f"{Colors.ERROR}❌ {validation_result['error']}{Colors.RESET}")
                
                # Предлагаем варианты
                suggestions = self._generate_nickname_suggestions(nickname)
                if suggestions:
                    print(f"{Colors.INFO}💡 Предлагаемые варианты:{Colors.RESET}")
                    for i, suggestion in enumerate(suggestions, 1):
                        print(f"   {i}. {suggestion}")
                    
                    choice = input(f"{Colors.PROMPT}Выберите вариант (1-{len(suggestions)}) или введите новый: {Colors.RESET}")
                    if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
                        nickname = suggestions[int(choice) - 1]
                        self.creation_data["nickname"] = nickname
                        print(f"{Colors.SUCCESS}✅ Выбран никнейм '{nickname}'!{Colors.RESET}")
                        break

    def _validate_nickname(self, nickname: str) -> Dict:
        """Валидация никнейма с расширенными проверками"""
        try:
            if not nickname:
                return {"valid": False, "error": "Никнейм не может быть пустым"}

            # Проверка на тип данных
            if not isinstance(nickname, str):
                return {"valid": False, "error": "Никнейм должен быть текстом"}

            if len(nickname) < 3:
                return {"valid": False, "error": "Никнейм слишком короткий (минимум 3 символа)"}

            if len(nickname) > 20:
                return {"valid": False, "error": "Никнейм слишком длинный (максимум 20 символов)"}

            # Проверка на допустимые символы
            if not re.match(r'^[a-zA-Z0-9_]+$', nickname):
                return {"valid": False, "error": "Никнейм содержит недопустимые символы (только a-z, A-Z, 0-9, _)"}

            # Проверка на зарезервированные имена
            if nickname.lower() in [name.lower() for name in self.forbidden_names]:
                return {"valid": False, "error": "Этот никнейм зарезервирован системой"}

            # Проверка что никнейм не состоит только из цифр
            if nickname.isdigit():
                return {"valid": False, "error": "Никнейм не может состоять только из цифр"}

            # Проверка на подозрительные паттерны
            suspicious_patterns = ['admin', 'root', 'system', 'null', 'undefined']
            if any(pattern in nickname.lower() for pattern in suspicious_patterns):
                return {"valid": False, "error": "Никнейм содержит зарезервированные слова"}

            return {"valid": True}

        except Exception as e:
            return {"valid": False, "error": f"Ошибка валидации: {e}"}
    
    def _generate_nickname_suggestions(self, base_nickname: str) -> List[str]:
        """Генерирует предложения никнеймов"""
        suggestions = []
        
        # Убираем недопустимые символы
        clean_base = re.sub(r'[^a-zA-Z0-9_]', '', base_nickname)
        
        if clean_base:
            # Добавляем цифры
            for i in range(1, 6):
                suggestions.append(f"{clean_base}{i}")
                suggestions.append(f"{clean_base}_{i}")
            
            # Добавляем хакерские префиксы/суффиксы
            prefixes = ["x_", "dark_", "cyber_", "ghost_", "neo_"]
            suffixes = ["_x", "_dark", "_ghost", "_404", "_null"]
            
            for prefix in prefixes[:2]:
                suggestions.append(f"{prefix}{clean_base}")
            
            for suffix in suffixes[:2]:
                suggestions.append(f"{clean_base}{suffix}")
        
        # Случайные хакерские ники
        random_nicks = [
            "phantom_coder", "zero_day", "byte_hunter", "circuit_ghost",
            "data_reaper", "code_ninja", "cyber_wolf", "dark_bit"
        ]
        
        suggestions.extend(random.sample(random_nicks, 3))
        
        return suggestions[:5]
    
    def _show_nickname_preview(self, nickname: str) -> None:
        """Показывает превью никнейма"""
        print(f"\n{Colors.INFO}👁️ Превью вашего профиля:{Colors.RESET}")
        print(f"{Colors.SUCCESS}┌─────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.SUCCESS}│ Hacker Profile                  │{Colors.RESET}")
        print(f"{Colors.SUCCESS}├─────────────────────────────────┤{Colors.RESET}")
        print(f"{Colors.SUCCESS}│ Nickname: {nickname:<18}    │{Colors.RESET}")
        print(f"{Colors.SUCCESS}│ Status:   Newbie                │{Colors.RESET}")
        print(f"{Colors.SUCCESS}│ Faction:  None                  │{Colors.RESET}")
        print(f"{Colors.SUCCESS}└─────────────────────────────────┘{Colors.RESET}")
    
    def _step_2_background(self) -> None:
        """Этап 2: Выбор предыстории"""
        print(f"\n{Colors.WARNING}━━━━━━━━━━━━━━━━ ЭТАП 2: ПРЕДЫСТОРИЯ ━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        typing_effect(f"{Colors.INFO}Каждый хакер имеет свою предыстрию...{Colors.RESET}")
        typing_effect(f"{Colors.INFO}Ваше прошлое определит стартовые навыки и возможности.{Colors.RESET}")
        
        # Показываем доступные предыстории
        backgrounds_list = list(self.backgrounds.items())
        
        for i, (bg_id, bg_data) in enumerate(backgrounds_list, 1):
            print(f"\n{Colors.WARNING}{i}. {bg_data['name']}{Colors.RESET}")
            print(f"   {Colors.INFO}{bg_data['desc']}{Colors.RESET}")
            
            # Показываем бонусы
            bonuses = bg_data['bonuses']
            bonus_str = []
            if 'skills' in bonuses:
                for skill, value in bonuses['skills'].items():
                    bonus_str.append(f"{skill} +{value}")
            if 'btc_balance' in bonuses:
                bonus_str.append(f"{bonuses['btc_balance']} BTC")
            if 'usd_balance' in bonuses:
                bonus_str.append(f"${bonuses['usd_balance']} USD")
            if 'reputation' in bonuses:
                bonus_str.append(f"+{bonuses['reputation']} репутации")
            if 'items' in bonuses:
                bonus_str.append(f"{len(bonuses['items'])} предметов")
            
            if bonus_str:
                print(f"   {Colors.SKILL}Бонусы: {', '.join(bonus_str)}{Colors.RESET}")
        
        while True:
            choice = input(f"\n{Colors.PROMPT}Выберите предыстори (1-{len(backgrounds_list)}) или 'info [номер]': {Colors.RESET}").strip().lower()
            
            if choice.startswith('info '):
                try:
                    bg_num = int(choice.split()[1])
                    if 1 <= bg_num <= len(backgrounds_list):
                        bg_id = backgrounds_list[bg_num - 1][0]
                        self._show_background_details(bg_id)
                    else:
                        print(f"{Colors.ERROR}Неверный номер предыстории{Colors.RESET}")
                except (ValueError, IndexError):
                    print(f"{Colors.ERROR}Неверный формат. Используйте 'info [номер]'{Colors.RESET}")
            
            elif choice.isdigit() and 1 <= int(choice) <= len(backgrounds_list):
                bg_id = backgrounds_list[int(choice) - 1][0]
                bg_data = self.backgrounds[bg_id]
                
                # Подтверждение
                print(f"\n{Colors.INFO}Выбрана предыстория: {Colors.WARNING}{bg_data['name']}{Colors.RESET}")
                typing_effect(f"{Colors.STORY}{bg_data['story']}{Colors.RESET}", 0.02)
                
                confirm = input(f"\n{Colors.PROMPT}Подтвердить выбор? (y/n): {Colors.RESET}").lower()
                if confirm in ['y', 'yes']:
                    self.creation_data["background"] = bg_id
                    audio_system.play_sound("success")
                    print(f"{Colors.SUCCESS}✅ Предыстория выбрана!{Colors.RESET}")
                    break
            else:
                print(f"{Colors.ERROR}Неверный выбор{Colors.RESET}")
    
    def _show_background_details(self, bg_id: str) -> None:
        """Показывает подробности предыстории"""
        bg_data = self.backgrounds[bg_id]
        
        print(f"\n{Colors.HEADER}━━━━━━━━━━ {bg_data['name'].upper()} ━━━━━━━━━━{Colors.RESET}")
        
        boxed_text(f"{bg_data['desc']}\n\n{bg_data['story']}", color=Colors.INFO)
        
        # Детальные бонусы
        bonuses = bg_data['bonuses']
        print(f"\n{Colors.SKILL}🎁 ПОЛУЧАЕМЫЕ БОНУСЫ:{Colors.RESET}")
        
        if 'skills' in bonuses:
            print(f"   {Colors.SUCCESS}📈 Навыки:{Colors.RESET}")
            for skill, value in bonuses['skills'].items():
                skill_name = skill.replace('_', ' ').title()
                print(f"      • {skill_name}: +{value}")
        
        if 'btc_balance' in bonuses:
            print(f"   {Colors.MONEY}🟠 Bitcoin: +{bonuses['btc_balance']} BTC{Colors.RESET}")
        
        if 'usd_balance' in bonuses:
            print(f"   {Colors.MONEY}💵 USD: +${bonuses['usd_balance']}{Colors.RESET}")
        
        if 'reputation' in bonuses:
            print(f"   {Colors.REP}⭐ Репутация: +{bonuses['reputation']}{Colors.RESET}")
        
        if 'items' in bonuses:
            print(f"   {Colors.INFO}📦 Стартовые предметы:{Colors.RESET}")
            for item in bonuses['items']:
                print(f"      • {item}")
        
        if 'contacts' in bonuses:
            print(f"   {Colors.WARNING}📱 Стартовые контакты:{Colors.RESET}")
            for contact in bonuses['contacts']:
                print(f"      • {contact}")
        
        if 'heat_reduction' in bonuses:
            print(f"   {Colors.SUCCESS}❄️ Снижение Heat Level: -{bonuses['heat_reduction']}%{Colors.RESET}")
        
        if 'heat_level' in bonuses:
            print(f"   {Colors.ERROR}🔥 Стартовый Heat Level: +{bonuses['heat_level']}%{Colors.RESET}")
    
    def _step_3_starter_pack(self) -> None:
        """Этап 3: Выбор стартового пакета"""
        print(f"\n{Colors.WARNING}━━━━━━━━━━━━━━━━ ЭТАП 3: СТАРТОВЫЙ ПАКЕТ ━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        typing_effect(f"{Colors.INFO}Выберите стартовый набор, соответствующий вашему стилю игры.{Colors.RESET}")
        
        packs_list = list(self.starter_packs.items())
        
        for i, (pack_id, pack_data) in enumerate(packs_list, 1):
            print(f"\n{pack_data['name']}")
            print(f"   {Colors.INFO}{pack_data['desc']}{Colors.RESET}")
            
            # Показываем содержимое пакета
            bonuses = pack_data['bonuses']
            contents = []
            
            if 'skills' in bonuses:
                for skill, value in bonuses['skills'].items():
                    contents.append(f"{skill.replace('_', ' ').title()} +{value}")
            
            if 'btc_balance' in bonuses:
                contents.append(f"{bonuses['btc_balance']} BTC")
            
            if 'usd_balance' in bonuses:
                contents.append(f"${bonuses['usd_balance']} USD")
            
            if 'items' in bonuses:
                contents.append(f"{len(bonuses['items'])} специальных предметов")
            
            if 'contacts' in bonuses:
                contents.append(f"{len(bonuses['contacts'])} контактов")
            
            if 'heat_reduction' in bonuses:
                contents.append(f"-{bonuses['heat_reduction']}% Heat Level")
            
            if contents:
                print(f"   {Colors.SKILL}Содержимое: {', '.join(contents)}{Colors.RESET}")
        
        while True:
            choice = input(f"\n{Colors.PROMPT}Выберите пакет (1-{len(packs_list)}): {Colors.RESET}").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(packs_list):
                pack_id = packs_list[int(choice) - 1][0]
                pack_data = self.starter_packs[pack_id]
                
                print(f"\n{Colors.INFO}Выбран: {pack_data['name']}{Colors.RESET}")
                
                confirm = input(f"{Colors.PROMPT}Подтвердить? (y/n): {Colors.RESET}").lower()
                if confirm in ['y', 'yes']:
                    self.creation_data["starter_pack"] = pack_id
                    audio_system.play_sound("success")
                    print(f"{Colors.SUCCESS}✅ Стартовый пакет выбран!{Colors.RESET}")
                    break
            else:
                print(f"{Colors.ERROR}Неверный выбор{Colors.RESET}")
    
    def _step_4_terminal_theme(self) -> None:
        """Этап 4: Выбор темы терминала"""
        print(f"\n{Colors.WARNING}━━━━━━━━━━━━━━━━ ЭТАП 4: ТЕМА ТЕРМИНАЛА ━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        typing_effect(f"{Colors.INFO}Настройте внешний вид вашего терминала.{Colors.RESET}")
        typing_effect(f"{Colors.INFO}Это влияет только на эстетику, но стиль тоже важен!{Colors.RESET}")
        
        themes_list = list(self.terminal_themes.items())
        
        for i, (theme_id, theme_data) in enumerate(themes_list, 1):
            # Показываем превью темы
            primary_color = theme_data['colors']['primary']
            print(f"\n{i}. {theme_data['name']}")
            print(f"   {Colors.INFO}{theme_data['desc']}{Colors.RESET}")
            print(f"   {primary_color}Превью: {self.creation_data.get('nickname', 'user')}@xss.is:~$ help{Colors.RESET}")
        
        while True:
            choice = input(f"\n{Colors.PROMPT}Выберите тему (1-{len(themes_list)}): {Colors.RESET}").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(themes_list):
                theme_id = themes_list[int(choice) - 1][0]
                theme_data = self.terminal_themes[theme_id]
                
                # Показываем расширенное превью
                self._show_theme_preview(theme_id)
                
                confirm = input(f"\n{Colors.PROMPT}Использовать эту тему? (y/n): {Colors.RESET}").lower()
                if confirm in ['y', 'yes']:
                    self.creation_data["terminal_theme"] = theme_id
                    audio_system.play_sound("success")
                    print(f"{Colors.SUCCESS}✅ Тема '{theme_data['name']}' установлена!{Colors.RESET}")
                    break
            else:
                print(f"{Colors.ERROR}Неверный выбор{Colors.RESET}")
    
    def _show_theme_preview(self, theme_id: str) -> None:
        """Показывает превью темы"""
        theme_data = self.terminal_themes[theme_id]
        primary = theme_data['colors']['primary']
        secondary = theme_data['colors']['secondary']
        nickname = self.creation_data.get('nickname', 'user')
        
        print(f"\n{Colors.INFO}🎨 Превью темы '{theme_data['name']}':{Colors.RESET}")
        print()
        print(f"    {secondary}✦ XSS Game Terminal - {theme_data['name']} ✦{Colors.RESET}")
        print()
        print(f"    {primary}{nickname}@xss.is:~$ {secondary}status{Colors.RESET}")
        print(f"    {Colors.SUCCESS}✓{Colors.RESET} {secondary}Command executed successfully{Colors.RESET}")
        print(f"    {Colors.INFO}ℹ{Colors.RESET} {secondary}System ready for operations{Colors.RESET}")
        print(f"    {primary}{nickname}@xss.is:~$ {secondary}█{Colors.RESET}")
        print()
    
    def _step_5_finalization(self) -> None:
        """Этап 5: Финализация создания персонажа"""
        print(f"\n{Colors.WARNING}━━━━━━━━━━━━━━━━ ЭТАП 5: ФИНАЛИЗАЦИЯ ━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        # Показываем итоговый профиль
        self._show_final_profile()
        
        print(f"\n{Colors.INFO}Проверьте ваш профиль перед началом игры.{Colors.RESET}")
        
        while True:
            choice = input(f"\n{Colors.PROMPT}Начать игру с этим персонажем? (yes/no/edit): {Colors.RESET}").lower()
            
            if choice in ['yes', 'y', 'да']:
                # Применяем все настройки
                self._apply_character_settings()
                
                # Финальная анимация
                self._show_creation_complete()
                break
            
            elif choice in ['no', 'n', 'нет']:
                print(f"{Colors.WARNING}Создание персонажа отменено{Colors.RESET}")
                return self.start_creation()  # Начинаем заново
            
            elif choice == 'edit':
                self._edit_character()
            
            else:
                print(f"{Colors.ERROR}Введите yes, no или edit{Colors.RESET}")
    
    def _show_final_profile(self) -> None:
        """Показывает финальный профиль персонажа"""
        nickname = self.creation_data.get('nickname', 'Unknown')
        background_id = self.creation_data.get('background', 'script_kiddie')
        pack_id = self.creation_data.get('starter_pack', 'hacker')
        theme_id = self.creation_data.get('terminal_theme', 'classic_green')
        
        background_name = self.backgrounds[background_id]['name']
        pack_name = self.starter_packs[pack_id]['name']
        theme_name = self.terminal_themes[theme_id]['name']
        
        print(f"\n{Colors.HEADER}╔══════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.HEADER}║                  ПРОФИЛЬ ПЕРСОНАЖА                   ║{Colors.RESET}")
        print(f"{Colors.HEADER}╚══════════════════════════════════════════════════════╝{Colors.RESET}")
        
        print(f"\n{Colors.SUCCESS}👤 Никнейм: {nickname}{Colors.RESET}")
        print(f"{Colors.INFO}📖 Предыстория: {background_name}{Colors.RESET}")
        print(f"{Colors.WARNING}🎁 Стартовый пакет: {pack_name}{Colors.RESET}")
        print(f"{Colors.SKILL}🎨 Тема терминала: {theme_name}{Colors.RESET}")
        
        # Суммарные бонусы
        total_bonuses = self._calculate_total_bonuses()
        
        print(f"\n{Colors.MONEY}💰 СТАРТОВЫЕ РЕСУРСЫ:{Colors.RESET}")
        if total_bonuses.get('btc_balance', 0) > 0:
            print(f"   🟠 Bitcoin: {total_bonuses['btc_balance']} BTC")
        if total_bonuses.get('usd_balance', 0) > 0:
            print(f"   💵 USD: ${total_bonuses['usd_balance']}")
        if total_bonuses.get('reputation', 0) > 0:
            print(f"   ⭐ Репутация: +{total_bonuses['reputation']}")
        
        if total_bonuses.get('skills'):
            print(f"\n{Colors.SKILL}📈 СТАРТОВЫЕ НАВЫКИ:{Colors.RESET}")
            for skill, value in total_bonuses['skills'].items():
                skill_name = skill.replace('_', ' ').title()
                base_value = 1  # Базовое значение
                total_value = base_value + value
                print(f"   • {skill_name}: {total_value} ({base_value}+{value})")
        
        total_items = total_bonuses.get('items', [])
        if total_items:
            print(f"\n{Colors.INFO}📦 СТАРТОВЫЕ ПРЕДМЕТЫ: {len(total_items)} шт.{Colors.RESET}")
        
        total_contacts = total_bonuses.get('contacts', [])
        if total_contacts:
            print(f"\n{Colors.WARNING}📱 СТАРТОВЫЕ КОНТАКТЫ: {len(total_contacts)} шт.{Colors.RESET}")
    
    def _calculate_total_bonuses(self) -> Dict:
        """Вычисляет общие бонусы от предыстории и стартового пакета"""
        total = {
            'skills': {},
            'btc_balance': 50,  # Базовое значение
            'usd_balance': 1000,  # Базовое значение
            'reputation': 15,  # Базовое значение
            'items': [],
            'contacts': [],
            'heat_reduction': 0,
            'heat_level': 0
        }
        
        # Бонусы от предыстории
        background_id = self.creation_data.get('background', 'script_kiddie')
        bg_bonuses = self.backgrounds[background_id]['bonuses']
        
        for key, value in bg_bonuses.items():
            if key == 'skills':
                for skill, points in value.items():
                    total['skills'][skill] = total['skills'].get(skill, 0) + points
            elif key in total:
                if isinstance(total[key], list):
                    total[key].extend(value)
                else:
                    total[key] += value
        
        # Бонусы от стартового пакета
        pack_id = self.creation_data.get('starter_pack', 'hacker')
        pack_bonuses = self.starter_packs[pack_id]['bonuses']
        
        for key, value in pack_bonuses.items():
            if key == 'skills':
                for skill, points in value.items():
                    total['skills'][skill] = total['skills'].get(skill, 0) + points
            elif key in total:
                if isinstance(total[key], list):
                    total[key].extend(value)
                else:
                    total[key] += value
        
        return total
    
    def _edit_character(self) -> None:
        """Позволяет отредактировать персонажа"""
        print(f"\n{Colors.INFO}Что вы хотите изменить?{Colors.RESET}")
        print(f"1. Никнейм")
        print(f"2. Предыстория")
        print(f"3. Стартовый пакет")
        print(f"4. Тема терминала")
        print(f"5. Отмена")
        
        choice = input(f"\n{Colors.PROMPT}Выбор: {Colors.RESET}").strip()
        
        if choice == '1':
            self._step_1_nickname()
        elif choice == '2':
            self._step_2_background()
        elif choice == '3':
            self._step_3_starter_pack()
        elif choice == '4':
            self._step_4_terminal_theme()
        elif choice == '5':
            return
        else:
            print(f"{Colors.ERROR}Неверный выбор{Colors.RESET}")
    
    def _apply_character_settings(self) -> None:
        """Применяет настройки персонажа к игровому состоянию"""
        # Устанавливаем никнейм
        game_state.set_stat('username', self.creation_data['nickname'])
        
        # Применяем бонусы
        total_bonuses = self._calculate_total_bonuses()
        
        # Навыки
        for skill, bonus in total_bonuses.get('skills', {}).items():
            current = game_state.get_skill(skill)
            game_state.set_skill(skill, current + bonus)
        
        # Валюты
        if 'btc_balance' in total_bonuses:
            game_state.set_stat('btc_balance', total_bonuses['btc_balance'])
        if 'usd_balance' in total_bonuses:
            game_state.set_stat('usd_balance', total_bonuses['usd_balance'])
        
        # Репутация
        if 'reputation' in total_bonuses:
            game_state.set_stat('reputation', total_bonuses['reputation'])
        
        # Предметы
        for item in total_bonuses.get('items', []):
            game_state.add_to_inventory(item)
        
        # Контакты
        for contact in total_bonuses.get('contacts', []):
            game_state.add_contact(contact)
        
        # Heat level
        if 'heat_level' in total_bonuses and total_bonuses['heat_level'] > 0:
            game_state.set_stat('heat_level', total_bonuses['heat_level'])
        
        # Сохраняем тему терминала
        game_state.set_stat('terminal_theme', self.creation_data.get('terminal_theme', 'classic_green'))
        
        # Помечаем, что персонаж создан
        game_state.set_stat('character_created', True)
        game_state.set_stat('background', self.creation_data.get('background'))
        game_state.set_stat('starter_pack', self.creation_data.get('starter_pack'))
    
    def _show_creation_complete(self) -> None:
        """Показывает завершение создания персонажа"""
        print(f"\n{Colors.SUCCESS}{'═' * 60}{Colors.RESET}")
        
        # Анимация создания
        steps = [
            "Инициализация профиля...",
            "Настройка навыков...",
            "Загрузка стартового инвентаря...",
            "Установка темы терминала...",
            "Подключение к сети xss.is...",
            "Регистрация в системе..."
        ]
        
        for step in steps:
            print(f"\r{Colors.INFO}⏳ {step}{Colors.RESET}", end='', flush=True)
            time.sleep(0.8)
            print(f"\r{Colors.SUCCESS}✅ {step}{Colors.RESET}")
        
        audio_system.play_sound("achievement")
        show_ascii_art("level_up")
        
        boxed_text(
            f"ДОБРО ПОЖАЛОВАТЬ В XSS GAME!\n\n"
            f"Персонаж {self.creation_data['nickname']} успешно создан.\n"
            f"Ваш путь в мире хакинга начинается прямо сейчас!\n\n"
            f"Помните: в даркнете доверяют только коду и репутации.",
            color=Colors.SUCCESS
        )
        
        print(f"\n{Colors.INFO}💡 Используйте команду 'help' для просмотра доступных команд{Colors.RESET}")
        print(f"{Colors.INFO}💡 Начните с команды 'status' для просмотра профиля{Colors.RESET}")
        print(f"{Colors.INFO}💡 Изучите 'forum' для поиска первых заданий{Colors.RESET}")


# Глобальный экземпляр создателя персонажей
character_creator = CharacterCreator()