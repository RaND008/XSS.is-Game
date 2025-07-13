"""
Система форума и контактов для XSS Game
"""

import random
import time
import textwrap
from typing import List, Dict, Optional

from ui.colors import XSSColors as Colors
from ui.effects import typing_effect
from core.game_state import game_state
from systems.audio import audio_system
from config.game_data import FORUM_POSTS, CONTACTS


class ForumSystem:
    """Система управления форумом и контактами"""
    
    def __init__(self):
        self.forum_posts = FORUM_POSTS
        self.contacts_data = CONTACTS
    
    def browse_forum(self, args: List[str] = None) -> None:
        """Просмотр форума"""
        if not args:
            self._show_forum_main()
        elif len(args) == 2:
            section = args[0].lower()
            try:
                post_id = int(args[1])
                self._show_post(section, post_id)
            except ValueError:
                print(f"{Colors.ERROR}❌ ID должен быть числом{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}❌ Неверное использование команды{Colors.RESET}")
            self._show_forum_usage()
    
    def _show_forum_main(self) -> None:
        """Показывает главную страницу форума"""
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━━ ФОРУМ XSS.IS ━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        # Статистика форума
        online_users = random.randint(1337, 13337)
        print(f"\n{Colors.SUCCESS}🟢 Онлайн: {online_users:,} пользователей{Colors.RESET}")
        print(f"{Colors.INFO}📊 Всего тем: 133,337{Colors.RESET}")
        
        # Публичный раздел
        print(f"\n{Colors.WARNING}════ 📂 ПУБЛИЧНЫЙ РАЗДЕЛ ════{Colors.RESET}")
        self._show_posts_list("public", self.forum_posts["public"][:8])
        
        # Приватный раздел
        print(f"\n{Colors.DANGER}════ 🔒 ПРИВАТНЫЙ РАЗДЕЛ ════{Colors.RESET}")
        self._show_posts_list("private", self.forum_posts["private"])
        
        # Подсказка
        print(f"\n{Colors.INFO}💡 Подсказка: Используйте 'forum [public/private] [ID]' для чтения постов{Colors.RESET}")
        print(f"{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    
    def _show_posts_list(self, section: str, posts: List[Dict]) -> None:
        """Показывает список постов"""
        for post in posts:
            post_id = post.get("id", 0)
            title = post.get("title", "Без названия")
            author = post.get("author", "Аноним")
            
            # Определяем иконку для поста
            icon = self._get_post_icon(post, section)
            
            # Проверяем доступность для приватных постов
            if section == "private":
                requirements = post.get("requirements", {})
                if self._check_post_requirements(requirements):
                    # Доступный пост
                    print(f"\n   {icon} [{Colors.SUCCESS}{post_id:>3}{Colors.RESET}] {Colors.SUCCESS}{title}{Colors.RESET}")
                    print(f"        Автор: {Colors.PROMPT}{author}{Colors.RESET}")
                else:
                    # Заблокированный пост
                    print(f"\n   🔒 [{Colors.ERROR}{post_id:>3}{Colors.RESET}] {Colors.ERROR}[ЗАБЛОКИРОВАНО]{Colors.RESET}")
                    req_list = self._format_requirements(requirements)
                    print(f"        Требования: {Colors.WARNING}{', '.join(req_list)}{Colors.RESET}")
            else:
                # Публичный пост
                print(f"\n   {icon} [{Colors.INFO}{post_id:>3}{Colors.RESET}] {Colors.WARNING}{title}{Colors.RESET}")
                print(f"        Автор: {Colors.PROMPT}{author}{Colors.RESET}")
    
    def _get_post_icon(self, post: Dict, section: str) -> str:
        """Определяет иконку для поста"""
        title = post.get("title", "").lower()
        post_id = post.get("id", 0)
        
        if post.get("pinned", False) or post_id <= 2:
            return "📌"  # Закрепленные
        elif "срочно" in title or "🔥" in title or "эксклюзив" in title:
            return "🔥"  # Горячие
        elif "внимание" in title or "⚠️" in title or "предупреждение" in title:
            return "⚠️"  # Важные
        elif section == "private":
            return "🔓"  # Приватные доступные
        else:
            return "💬"  # Обычные
    
    def _check_post_requirements(self, requirements: Dict) -> bool:
        """Проверяет требования для доступа к посту"""
        if not requirements:
            return True
        
        # Проверяем репутацию
        req_rep = requirements.get("reputation", 0)
        if game_state.get_stat("reputation", 0) < req_rep:
            return False
        
        # Проверяем навыки
        req_skills = requirements.get("skills", {})
        for skill, level in req_skills.items():
            if game_state.get_skill(skill) < level:
                return False
        
        return True
    
    def _format_requirements(self, requirements: Dict) -> List[str]:
        """Форматирует требования в читаемый вид"""
        req_list = []
        
        req_rep = requirements.get("reputation", 0)
        if req_rep > 0:
            req_list.append(f"Репутация: {req_rep}")
        
        req_skills = requirements.get("skills", {})
        for skill, level in req_skills.items():
            skill_name = skill.replace('_', ' ').title()
            req_list.append(f"{skill_name}: {level}")
        
        return req_list
    
    def _show_post(self, section: str, post_id: int) -> None:
        """Показывает конкретный пост"""
        if section not in ["public", "private"]:
            print(f"{Colors.ERROR}❌ Неизвестный раздел. Используйте 'public' или 'private'{Colors.RESET}")
            return
        
        posts = self.forum_posts.get(section, [])
        post = next((p for p in posts if p.get("id") == post_id), None)
        
        if not post:
            print(f"{Colors.ERROR}❌ Пост #{post_id} не найден в разделе {section}{Colors.RESET}")
            return
        
        # Проверка доступа для приватных постов
        if section == "private":
            requirements = post.get("requirements", {})
            if not self._check_post_requirements(requirements):
                self._show_access_denied(requirements)
                return
        
        # Показываем пост
        self._display_post(post, section)
    
    def _show_access_denied(self, requirements: Dict) -> None:
        """Показывает сообщение об отказе в доступе"""
        print(f"\n{Colors.DANGER}━━━━━━━━━━ 🔒 ДОСТУП ЗАПРЕЩЕН 🔒 ━━━━━━━━━━{Colors.RESET}")
        
        req_list = self._format_requirements(requirements)
        print(f"\n{Colors.ERROR}Для доступа необходимо:{Colors.RESET}")
        for req in req_list:
            print(f"   • {Colors.WARNING}{req}{Colors.RESET}")
        
        print(f"\n{Colors.DANGER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    
    def _display_post(self, post: Dict, section: str) -> None:
        """Отображает пост"""
        title = post.get('title', 'Без заголовка')
        author = post.get('author', 'Неизвестен')
        content = post.get('content', 'Нет содержимого')
        
        # Определяем цвет заголовка
        header_color = Colors.WARNING if section == "public" else Colors.DANGER
        
        print(f"\n{header_color}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        # Иконка для типа поста
        icon = self._get_post_icon(post, section)
        
        print(f"\n{icon} {header_color}{title}{Colors.RESET}")
        print(f"\n{Colors.INFO}👤 Автор:{Colors.RESET} {Colors.PROMPT}{author}{Colors.RESET}")
        print(f"{Colors.INFO}📅 ID:{Colors.RESET} #{post.get('id', 0)}")
        
        print(f"\n{Colors.INFO}━━━ СОДЕРЖАНИЕ ━━━{Colors.RESET}\n")
        
        # Разбиваем контент на абзацы для лучшей читаемости
        paragraphs = content.split('. ')
        for paragraph in paragraphs:
            if paragraph.strip():
                # Добавляем точку обратно, если она была
                if not paragraph.endswith('.'):
                    paragraph += '.'
                
                # Оборачиваем длинные строки
                wrapped_lines = textwrap.wrap(paragraph, width=70)
                for line in wrapped_lines:
                    print(f"   {line}")
                print()  # Пустая строка между абзацами
        
        # Дополнительная информация для приватных постов
        if section == "private":
            print(f"\n{Colors.SUCCESS}✅ У вас есть доступ к этому приватному контенту{Colors.RESET}")
        
        print(f"\n{header_color}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    
    def _show_forum_usage(self) -> None:
        """Показывает справку по использованию команды forum"""
        print(f"{Colors.INFO}Используйте:{Colors.RESET}")
        print(f"   • forum - показать список тем")
        print(f"   • forum public [ID] - читать публичный пост")
        print(f"   • forum private [ID] - читать приватный пост")
    
    def show_contacts(self) -> None:
        """Показывает контакты игрока"""
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━ КОНТАКТЫ ━━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        player_contacts = game_state.get_stat("contacts", [])
        
        if not player_contacts:
            print(f"\n{Colors.WARNING}📭 У вас пока нет контактов{Colors.RESET}")
            print(f"\n{Colors.INFO}💡 Совет: Повышайте репутацию и выполняйте миссии,{Colors.RESET}")
            print(f"{Colors.INFO}   чтобы привлечь внимание важных персон форума{Colors.RESET}")
        else:
            print(f"\n{Colors.SUCCESS}📬 Ваши контакты ({len(player_contacts)}):{Colors.RESET}\n")
            
            for i, contact_id in enumerate(player_contacts, 1):
                if contact_id in self.contacts_data:
                    contact = self.contacts_data[contact_id]
                    self._display_contact_summary(i, contact_id, contact)
        
        print(f"\n{Colors.INFO}💬 Используйте 'pm [имя]' для отправки сообщения{Colors.RESET}")
        print(f"{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    
    def _display_contact_summary(self, index: int, contact_id: str, contact: Dict) -> None:
        """Отображает краткую информацию о контакте"""
        # Определяем статус контакта
        status_icon, status_color = self._get_contact_status(contact_id)
        
        print(f"   {status_icon} {index}. {status_color}{contact['name']}{Colors.RESET}")
        print(f"       {Colors.INFO}{contact['desc']}{Colors.RESET}")
        
        # Показываем последнее сообщение
        messages = contact.get("messages", [])
        if messages:
            last_msg = messages[0][:50] + "..." if len(messages[0]) > 50 else messages[0]
            print(f"       {Colors.WARNING}Последнее: \"{last_msg}\"{Colors.RESET}")
        
        print()  # Пустая строка между контактами
    
    def _get_contact_status(self, contact_id: str) -> tuple:
        """Получает статус и цвет контакта"""
        if contact_id == "shadow":
            return "🌑", Colors.ENCRYPTED
        elif contact_id == "nexus":
            return "💎", Colors.INFO
        elif contact_id == "ghost":
            return "👻", Colors.WARNING
        else:
            return "👤", Colors.INFO
    
    def private_message(self, contact_name: str) -> None:
        """Система личных сообщений"""
        player_contacts = game_state.get_stat("contacts", [])
        
        if contact_name not in player_contacts:
            print(f"\n{Colors.ERROR}❌ У вас нет контакта с именем '{contact_name}'{Colors.RESET}")
            available = ', '.join(player_contacts) if player_contacts else 'нет'
            print(f"{Colors.INFO}Доступные контакты: {available}{Colors.RESET}")
            return
        
        if contact_name not in self.contacts_data:
            print(f"\n{Colors.ERROR}❌ Контакт не найден в базе{Colors.RESET}")
            return
        
        contact = self.contacts_data[contact_name]
        
        # Анимация подключения
        self._show_connection_animation()
        
        # Определяем настроение контакта
        mood = self._determine_contact_mood()
        
        print(f"\n{Colors.INFO}[Настроение собеседника: {mood['icon']} {mood['name']}]{Colors.RESET}")
        
        # Выбираем сообщение
        message = self._get_contact_message(contact, mood)
        
        # Печатаем сообщение с эффектом
        print()
        typing_effect(f"{Colors.WARNING}[{contact['name']}]: {message}{Colors.RESET}", delay=0.02)
        
        # Проверяем специальные разблокировки
        self._check_contact_unlocks(contact_name, contact)
        
        # Возможность задать вопрос
        self._handle_conversation(contact_name, contact)
    
    def _show_connection_animation(self) -> None:
        """Анимация установки соединения"""
        print(f"\n{Colors.ENCRYPTED}[УСТАНОВКА ЗАЩИЩЕННОГО СОЕДИНЕНИЯ]{Colors.RESET}")
        for i in range(3):
            print(f"\r{Colors.WARNING}Шифрование канала{'.' * (i + 1)}{Colors.RESET}", end='', flush=True)
            time.sleep(0.5)
        print(f"\r{Colors.SUCCESS}✅ Защищенный канал установлен{Colors.RESET}")
        
        audio_system.play_sound("message")
    
    def _determine_contact_mood(self) -> Dict[str, str]:
        """Определяет настроение контакта"""
        moods = [
            {"name": "дружелюбное", "icon": "😊"},
            {"name": "нейтральное", "icon": "😐"},
            {"name": "загадочное", "icon": "🤔"},
            {"name": "спешащее", "icon": "⏰"},
            {"name": "осторожное", "icon": "🕵️"},
            {"name": "веселое", "icon": "😄"}
        ]
        return random.choice(moods)
    
    def _get_contact_message(self, contact: Dict, mood: Dict) -> str:
        """Получает сообщение от контакта"""
        base_messages = contact.get("messages", ["Привет!"])
        
        # Добавляем контекстные сообщения в зависимости от прогресса
        additional_messages = self._get_contextual_messages()
        
        all_messages = base_messages + additional_messages
        return random.choice(all_messages)
    
    def _get_contextual_messages(self) -> List[str]:
        """Получает контекстные сообщения в зависимости от состояния игрока"""
        messages = []
        
        reputation = game_state.get_stat("reputation", 0)
        heat_level = game_state.get_stat("heat_level", 0)
        warnings = game_state.get_stat("warnings", 0)
        
        if reputation > 100:
            messages.extend([
                "Ты далеко зашел. Будь осторожен, на тебя уже обратили внимание.",
                "С большой силой приходит большая ответственность... и большие враги."
            ])
        
        if heat_level > 70:
            messages.extend([
                "Ты слишком засветился. Советую залечь на дно.",
                "Слышал, за тобой уже охотятся. Будь начеку.",
                "Твой heat level зашкаливает. Время исчезнуть на время."
            ])
        
        if warnings > 0:
            messages.extend([
                "Будь осторожнее. Еще пара ошибок и тебя накроют.",
                "Админы начинают подозревать. Действуй аккуратнее."
            ])
        
        return messages
    
    def _check_contact_unlocks(self, contact_id: str, contact: Dict) -> None:
        """Проверяет разблокировки от контакта"""
        unlocks = contact.get("unlocks", [])
        if not unlocks:
            return
        
        # Шанс получить подсказку о новом предмете
        if random.random() < 0.3:  # 30% шанс
            print(f"\n{Colors.SUCCESS}[{contact['name']}]: Кстати, у меня есть кое-что интересное...{Colors.RESET}")
            time.sleep(1)
            
            unlock_item = random.choice(unlocks)
            print(f"{Colors.SUCCESS}[+] Информация о '{unlock_item}' может быть полезна в магазине!{Colors.RESET}")
    
    def _handle_conversation(self, contact_name: str, contact: Dict) -> None:
        """Обрабатывает диалог с контактом"""
        print(f"\n{Colors.INFO}[Введите 'q' чтобы выйти или любой текст для продолжения диалога]{Colors.RESET}")
        user_input = audio_system.get_input_with_sound(f"{Colors.PROMPT}Вы: {Colors.RESET}")
        
        if user_input.lower() != 'q':
            response = self._generate_response(contact_name, user_input.lower())
            typing_effect(f"{Colors.WARNING}[{contact['name']}]: {response}{Colors.RESET}", delay=0.02)
        
        print(f"\n{Colors.ENCRYPTED}[СОЕДИНЕНИЕ РАЗОРВАНО]{Colors.RESET}")
    
    def _generate_response(self, contact_name: str, user_input: str) -> str:
        """Генерирует ответ контакта на основе ввода пользователя"""
        # Базовые ответы по ключевым словам
        keyword_responses = {
            "миссия": [
                "Миссии - это путь к славе. Но выбирай с умом.",
                "Не все задания стоят риска. Думай головой.",
                "Лучшие миссии приходят к тем, кто доказал свою надежность."
            ],
            "помощь": [
                "Я помогаю только тем, кто помогает себе сам.",
                "Помощь в нашем мире стоит дорого.",
                "Сначала докажи, что заслуживаешь моей помощи."
            ],
            "совет": [
                "Мой совет - не доверяй никому. Даже мне.",
                "В этом мире выживают только параноики.",
                "Лучший совет - всегда иметь план отступления."
            ],
            "деньги": [
                "Деньги - это инструмент. Важно, как ты их используешь.",
                "В крипте сила, но не забывай про ликвидность.",
                "Богатство без анонимности - это мишень на спине."
            ],
            "взлом": [
                "Взлом - это искусство. Требует терпения и практики.",
                "Лучшие хакеры думают как художники, но действуют как инженеры.",
                "Каждая система имеет слабое звено. Найди его."
            ],
            "репутация": [
                "Репутация в нашем мире - это все.",
                "Заработать репутацию тяжело, потерять - легко.",
                "Твоя репутация открывает двери... или закрывает их навсегда."
            ],
            "безопасность": [
                "Безопасность - это не паранойя, это профессионализм.",
                "Один неосторожный шаг может стоить всего.",
                "OPSEC не обсуждается, OPSEC соблюдается."
            ]
        }
        
        # Специфичные ответы для разных контактов
        contact_specific = {
            "shadow": [
                "Тени помнят все...",
                "Информация - моя валюта.",
                "Некоторые секреты лучше оставить в темноте."
            ],
            "nexus": [
                "У меня есть связи везде.",
                "Информация течет через меня как вода.",
                "Правильный вопрос стоит больше правильного ответа."
            ],
            "ghost": [
                "Невидимость - мое преимущество.",
                "Оставаться неуловимым - это искусство.",
                "Призраки не оставляют следов."
            ]
        }
        
        # Проверяем ключевые слова
        for keyword, responses in keyword_responses.items():
            if keyword in user_input:
                return random.choice(responses)
        
        # Проверяем специфичные ответы контакта
        if contact_name in contact_specific:
            if random.random() < 0.3:  # 30% шанс специфичного ответа
                return random.choice(contact_specific[contact_name])
        
        # Общие ответы
        generic_responses = [
            "Интересная мысль...",
            "Я подумаю об этом.",
            "Время покажет.",
            "Возможно, ты прав.",
            "Это требует размышлений.",
            "Не все так просто, как кажется.",
            "У каждого свой путь.",
            "Мудрость приходит с опытом.",
            "Некоторые вещи лучше узнать самому.",
            "Терпение - добродетель хакера."
        ]
        
        return random.choice(generic_responses)
    
    def add_contact(self, contact_id: str) -> bool:
        """Добавляет новый контакт"""
        if contact_id not in self.contacts_data:
            print(f"{Colors.ERROR}Неизвестный контакт: {contact_id}{Colors.RESET}")
            return False
        
        if game_state.add_contact(contact_id):
            contact = self.contacts_data[contact_id]
            print(f"\n{Colors.SUCCESS}📬 НОВЫЙ КОНТАКТ!{Colors.RESET}")
            print(f"{Colors.SUCCESS}Добавлен контакт: {contact['name']}{Colors.RESET}")
            print(f"{Colors.INFO}{contact['desc']}{Colors.RESET}")
            
            audio_system.play_sound("notification")
            return True
        
        return False
    
    def get_contact_info(self, contact_id: str) -> Optional[Dict]:
        """Получает информацию о контакте"""
        return self.contacts_data.get(contact_id)
    
    def get_available_contacts(self) -> List[str]:
        """Получает список доступных контактов игрока"""
        return game_state.get_stat("contacts", [])
    
    def has_contact(self, contact_id: str) -> bool:
        """Проверяет наличие контакта у игрока"""
        return game_state.has_contact(contact_id)
    
    def generate_forum_activity(self) -> None:
        """Генерирует активность на форуме (новые посты)"""
        if random.random() < 0.1:  # 10% шанс нового поста
            new_post = self._generate_random_post()
            if new_post:
                print(f"\n{Colors.INFO}📝 Новый пост на форуме: \"{new_post['title']}\"{Colors.RESET}")
    
    def _generate_random_post(self) -> Optional[Dict]:
        """Генерирует случайный пост"""
        post_templates = [
            {
                "title": "Новая уязвимость в {software}",
                "author": "SecurityResearcher",
                "content": "Обнаружена критическая уязвимость в популярном ПО. Подробности в приватном разделе."
            },
            {
                "title": "Слив базы данных {company}",
                "author": "DataLeaker",
                "content": "Получил доступ к базе данных крупной компании. Продаю за разумную цену."
            },
            {
                "title": "Новые методы обхода {security_system}",
                "author": "BypassMaster", 
                "content": "Разработал новую технику обхода современных систем защиты."
            }
        ]
        
        template = random.choice(post_templates)
        
        # Заполняем переменные
        companies = ["TechCorp", "MegaSoft", "CyberInc", "DataSystems", "SecureBank"]
        software = ["Windows", "Chrome", "Firefox", "Office", "Adobe"]
        security_systems = ["антивируса", "файрвола", "2FA", "биометрии"]
        
        post = template.copy()
        post["title"] = post["title"].format(
            software=random.choice(software),
            company=random.choice(companies),
            security_system=random.choice(security_systems)
        )
        
        # Добавляем к существующим постам (в реальной игре)
        # В данной демонстрации просто возвращаем
        return post
    
    def show_forum_stats(self) -> None:
        """Показывает статистику активности на форуме"""
        player_contacts = len(game_state.get_stat("contacts", []))
        total_contacts = len(self.contacts_data)
        reputation = game_state.get_stat("reputation", 0)
        
        # Подсчитываем доступные приватные посты
        accessible_private = 0
        for post in self.forum_posts["private"]:
            requirements = post.get("requirements", {})
            if self._check_post_requirements(requirements):
                accessible_private += 1
        
        total_private = len(self.forum_posts["private"])
        
        print(f"\n{Colors.INFO}📊 СТАТИСТИКА ФОРУМА:{Colors.RESET}")
        print(f"   Ваши контакты: {player_contacts}/{total_contacts}")
        print(f"   Репутация: {reputation}")
        print(f"   Доступные приватные посты: {accessible_private}/{total_private}")
        
        # Рекомендации
        if player_contacts == 0:
            print(f"\n{Colors.WARNING}💡 Повышайте репутацию для получения контактов{Colors.RESET}")
        
        if accessible_private < total_private // 2:
            print(f"\n{Colors.WARNING}💡 Прокачивайте навыки для доступа к элитному контенту{Colors.RESET}")


# Глобальный экземпляр системы форума
forum_system = ForumSystem()