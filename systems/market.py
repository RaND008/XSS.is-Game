"""
Система магазина для XSS Game
"""

import random
from typing import Dict, List, Optional

from ui.colors import XSSColors as Colors
from ui.effects import typing_effect
from core.game_state import game_state
from systems.audio import audio_system
from config.settings import ITEM_CATEGORIES
from config.game_data import MARKET_ITEMS


class MarketSystem:
    """Система управления магазином"""
    
    def __init__(self):
        self.base_items = MARKET_ITEMS
        self.special_offers = []
        self.item_categories = ITEM_CATEGORIES
    
    def get_available_items(self) -> List[dict]:
        """Получает список доступных товаров"""
        available_items = []
        
        # Проверяем базовые товары
        for item_id, item_data in self.base_items.items():
            if self._check_unlock_condition(item_data):
                item_copy = item_data.copy()
                item_copy["id"] = item_id
                available_items.append(item_copy)
        
        # Добавляем специальные предложения
        available_items.extend(self.special_offers)
        
        return available_items
    
    def _check_unlock_condition(self, item_data: dict) -> bool:
        """Проверяет условия разблокировки товара"""
        unlock_condition = item_data.get("unlock_condition", {})
        
        # Проверяем репутацию
        req_rep = unlock_condition.get("reputation", 0)
        if game_state.get_stat("reputation", 0) < req_rep:
            return False
        
        # Проверяем навыки
        req_skills = unlock_condition.get("skills", {})
        for skill, level in req_skills.items():
            if game_state.get_skill(skill) < level:
                return False
        
        # Проверяем фракцию
        req_faction = unlock_condition.get("faction")
        if req_faction and game_state.get_stat("faction") != req_faction:
            return False
        
        # Проверяем выполненные миссии
        req_missions = unlock_condition.get("completed_missions", [])
        for mission in req_missions:
            if not game_state.is_mission_completed(mission):
                return False
        
        # Проверяем контакты
        req_contacts = unlock_condition.get("contacts", [])
        for contact in req_contacts:
            if not game_state.has_contact(contact):
                return False
        
        return True
    
    def show_market(self) -> None:
        """Показывает магазин"""
        available_items = self.get_available_items()
        
        print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━━ ТЕНЕВОЙ РЫНОК ━━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        # Статистика
        total_items = len(available_items)
        owned_items = len(game_state.get_stat("inventory", []))
        new_items = sum(1 for item in available_items if item.get("special", False))
        
        print(f"\n{Colors.INFO}📊 Статистика:{Colors.RESET}")
        print(f"   Доступно товаров: {Colors.WARNING}{total_items}{Colors.RESET}")
        print(f"   Куплено: {Colors.SUCCESS}{owned_items}{Colors.RESET}")
        if new_items > 0:
            print(f"   {Colors.SUCCESS}✨ Специальные предложения: {new_items}{Colors.RESET}")
        
        print(f"\n{Colors.MONEY}💰 Ваш баланс: {game_state.get_stat('btc_balance', 0):.2f} BTC{Colors.RESET}")
        
        # Группируем товары по категориям
        categories = {}
        for item in available_items:
            cat = item.get("type", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        # Показываем товары по категориям
        for cat_id, items in categories.items():
            cat_info = self.item_categories.get(cat_id, {"name": "Прочее", "icon": "📦"})
            
            print(f"\n{Colors.INFO}━━━ {cat_info['icon']} {cat_info['name'].upper()} ━━━{Colors.RESET}")
            
            for item in sorted(items, key=lambda x: x.get("price", 0)):
                self._print_item(item)
        
        print(f"\n{Colors.INFO}💡 Команды:{Colors.RESET}")
        print(f"   buy [ID] - купить товар")
        print(f"   info [ID] - подробная информация")
        
        print(f"\n{Colors.WARNING}🔓 Новые товары появляются при повышении репутации и навыков{Colors.RESET}")
        print(f"{Colors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    
    def _print_item(self, item: dict) -> None:
        """Выводит информацию о товаре"""
        item_id = item.get("id", "unknown")
        price = item.get("price", 0)
        name = item.get("name", "Неизвестный товар")
        desc = item.get("desc", "Нет описания")
        
        # Проверяем статус товара
        if game_state.has_item(item_id):
            status = f"{Colors.SUCCESS}✓ Куплено{Colors.RESET}"
            price_display = f"{Colors.SUCCESS}{price} BTC{Colors.RESET}"
        elif game_state.can_afford(price, "btc_balance"):
            status = f"{Colors.WARNING}Доступно{Colors.RESET}"
            price_display = f"{Colors.MONEY}{price} BTC{Colors.RESET}"
        else:
            status = f"{Colors.ERROR}Дорого{Colors.RESET}"
            price_display = f"{Colors.ERROR}{price} BTC{Colors.RESET}"
        
        # Специальное предложение
        special_mark = ""
        if item.get("special", False):
            duration = item.get("duration", 0)
            special_mark = f"{Colors.SUCCESS} ⚡ СПЕЦПРЕДЛОЖЕНИЕ ({duration} ходов){Colors.RESET}"
        
        print(f"\n   {Colors.INFO}ID: {Colors.WARNING}{item_id}{Colors.RESET}{special_mark}")
        print(f"   {name} - {price_display}")
        print(f"   {Colors.INFO}{desc}{Colors.RESET}")
        
        # Показываем бонусы
        bonus = item.get("bonus", {})
        if bonus:
            bonus_str = []
            for bonus_type, value in bonus.items():
                if bonus_type == "all_skills":
                    bonus_str.append(f"Все навыки +{value}")
                elif bonus_type == "heat_reduction":
                    bonus_str.append(f"Heat level {value:+}%")
                elif bonus_type in ["scanning", "cracking", "stealth", "social_eng"]:
                    bonus_str.append(f"{bonus_type.title()} +{value}")
                elif bonus_type == "reputation":
                    bonus_str.append(f"Репутация +{value}")
            
            if bonus_str:
                print(f"   {Colors.SKILL}Бонусы: {', '.join(bonus_str)}{Colors.RESET}")
        
        print(f"   Статус: {status}")

    def buy_item(self, item_id: str) -> bool:
        """Покупает товар с учетом Heat Level"""
        # Получаем список доступных товаров
        available_items = self.get_available_items()

        # Ищем товар по ID
        item = next((i for i in available_items if i.get("id") == item_id), None)

        if not item:
            print(f"{Colors.ERROR}❌ Предмет '{item_id}' не найден или недоступен{Colors.RESET}")
            return False

        if game_state.has_item(item_id):
            print(f"{Colors.WARNING}[!] У вас уже есть '{item['name']}'{Colors.RESET}")
            return False

        # Получаем базовую цену
        base_price = item.get("price", 0)

        # Применяем динамическое ценообразование на основе Heat Level
        heat_level = game_state.get_stat("heat_level", 0)
        price = base_price  # Инициализируем переменную price

        if heat_level > 80:
            price = int(base_price * 1.5)  # +50% при критическом heat
            print(f"{Colors.DANGER}⚠️ КРИТИЧЕСКИЙ HEAT LEVEL! Цены увеличены на 50%!{Colors.RESET}")
        elif heat_level > 50:
            price = int(base_price * 1.2)  # +20% при высоком heat
            print(f"{Colors.WARNING}⚠️ Повышенная цена из-за вашего Heat Level (+20%)!{Colors.RESET}")

        # Проверяем, может ли игрок позволить себе покупку
        if not game_state.can_afford(price, "btc_balance"):
            needed = price - game_state.get_stat("btc_balance", 0)
            print(f"{Colors.ERROR}❌ Недостаточно BTC. Нужно еще: {needed:.2f} BTC{Colors.RESET}")
            return False

        # Подтверждение покупки
        print(f"\n{Colors.WARNING}Подтверждение покупки:{Colors.RESET}")
        print(f"   Товар: {item['name']}")
        if price != base_price:
            print(f"   Базовая цена: {Colors.MONEY}{base_price} BTC{Colors.RESET}")
            print(f"   Итоговая цена: {Colors.DANGER}{price} BTC{Colors.RESET}")
        else:
            print(f"   Цена: {Colors.MONEY}{price} BTC{Colors.RESET}")
        print(f"   Ваш баланс: {Colors.MONEY}{game_state.get_stat('btc_balance'):.2f} BTC{Colors.RESET}")
        print(f"   Останется: {Colors.MONEY}{game_state.get_stat('btc_balance') - price:.2f} BTC{Colors.RESET}")

        # Показываем описание предмета
        if item.get('desc'):
            print(f"\n   {Colors.INFO}Описание: {item['desc']}{Colors.RESET}")

        # Показываем бонусы
        bonus = item.get("bonus", {})
        if bonus:
            print(f"\n   {Colors.SKILL}Бонусы:{Colors.RESET}")
            for bonus_type, value in bonus.items():
                if bonus_type == "all_skills":
                    print(f"      • Все навыки +{value}")
                elif bonus_type == "heat_reduction":
                    if value < 0:
                        print(f"      • Heat Level {value}%")
                    else:
                        print(f"      • Heat Level +{value}%")
                elif bonus_type in ["scanning", "cracking", "stealth", "social_eng"]:
                    print(f"      • {bonus_type.replace('_', ' ').title()} +{value}")
                elif bonus_type == "reputation":
                    print(f"      • Репутация +{value}")

        confirm = input(f"\n{Colors.PROMPT}Подтвердить покупку? (y/n): {Colors.RESET}").lower()

        if confirm != 'y':
            print(f"{Colors.WARNING}Покупка отменена{Colors.RESET}")
            return False

        # Покупаем
        game_state.spend_currency(price, "btc_balance")
        game_state.add_to_inventory(item_id)

        print(f"\n{Colors.SUCCESS}✅ Успешная покупка!{Colors.RESET}")
        print(f"{Colors.SUCCESS}Вы приобрели: {item['name']}{Colors.RESET}")

        # Применяем бонусы
        self._apply_item_bonuses(item)

        # Звук покупки
        audio_system.play_sound("purchase")

        # Проверяем разблокировку новых товаров
        self._check_market_unlocks()

        # Специальное сообщение для некоторых предметов
        special_messages = {
            "elite_proxy": "Теперь ваши операции станут намного безопаснее!",
            "zero_day_exploit": "Мощное оружие в руках опытного хакера...",
            "quantum_decryptor": "Технология будущего теперь в ваших руках!",
            "darknet_master_key": "Вы получили доступ к самым темным уголкам сети...",
            "ai_singularity_core": "Искусственный интеллект подчиняется вашей воле!"
        }

        if item_id in special_messages:
            print(f"\n{Colors.STORY}💭 {special_messages[item_id]}{Colors.RESET}")

        return True
    
    def _apply_item_bonuses(self, item: dict) -> None:
        """Применяет бонусы от предмета"""
        bonus = item.get("bonus", {})
        if not bonus:
            return
        
        print(f"\n{Colors.SKILL}Получены бонусы:{Colors.RESET}")
        
        for bonus_type, value in bonus.items():
            if bonus_type in ["scanning", "cracking", "stealth", "social_eng"]:
                old_value = game_state.get_skill(bonus_type)
                new_value = game_state.modify_skill(bonus_type, value)
                print(f"   {Colors.SKILL}✨ {bonus_type.title()}: {old_value} → {new_value}{Colors.RESET}")
            
            elif bonus_type == "all_skills":
                for skill in ["scanning", "cracking", "stealth", "social_eng"]:
                    game_state.modify_skill(skill, value)
                print(f"   {Colors.SKILL}✨ Все навыки +{value}{Colors.RESET}")
            
            elif bonus_type == "heat_reduction":
                old_heat = game_state.get_stat("heat_level", 0)
                new_heat = max(0, old_heat + value)  # value может быть отрицательным
                game_state.set_stat("heat_level", new_heat)
                if value < 0:
                    print(f"   {Colors.SUCCESS}❄️ Heat level: {old_heat}% → {new_heat}%{Colors.RESET}")
                else:
                    print(f"   {Colors.WARNING}🔥 Heat level: {old_heat}% → {new_heat}%{Colors.RESET}")
            
            elif bonus_type == "reputation":
                old_rep = game_state.get_stat("reputation", 0)
                new_rep = game_state.modify_stat("reputation", value)
                print(f"   {Colors.REP}📈 Репутация: {old_rep} → {new_rep}{Colors.RESET}")
    
    def _check_market_unlocks(self) -> None:
        """Проверяет разблокировку новых товаров"""
        # Простая проверка - можно расширить
        current_items = self.get_available_items()
        
        # Логика для определения новых разблокировок
        # Здесь можно добавить сложную логику проверки условий
        
        # Пример: проверяем есть ли новые товары после покупки
        new_items_count = len([item for item in current_items 
                              if not game_state.has_item(item.get("id", ""))])
        
        if new_items_count > 0:
            print(f"\n{Colors.SUCCESS}🔓 Доступны новые товары в магазине!{Colors.RESET}")
    
    def show_item_info(self, item_id: str) -> None:
        """Показывает подробную информацию о товаре"""
        available_items = self.get_available_items()
        item = next((i for i in available_items if i.get("id") == item_id), None)
        
        if not item:
            print(f"{Colors.ERROR}❌ Предмет '{item_id}' не найден{Colors.RESET}")
            return
        
        item_type = item.get("type", "unknown")
        cat_info = self.item_categories.get(item_type, {"name": "Неизвестно", "icon": "❓"})
        
        print(f"\n{Colors.HEADER}━━━━━━━━━━ ИНФОРМАЦИЯ О ТОВАРЕ ━━━━━━━━━━{Colors.RESET}")
        print(f"\n{cat_info['icon']} {Colors.WARNING}{item['name']}{Colors.RESET}")
        print(f"\nКатегория: {cat_info['name']}")
        print(f"ID: {item.get('id', 'unknown')}")
        print(f"Цена: {Colors.MONEY}{item.get('price', 0)} BTC{Colors.RESET}")
        print(f"\n{Colors.INFO}Описание:{Colors.RESET}")
        print(f"{item.get('desc', 'Нет описания')}")
        
        # Показываем эффекты
        bonus = item.get("bonus", {})
        if bonus:
            print(f"\n{Colors.SKILL}Эффекты:{Colors.RESET}")
            for bonus_type, value in bonus.items():
                if bonus_type == "all_skills":
                    print(f"   • Повышает все навыки на {value}")
                elif bonus_type == "heat_reduction":
                    if value < 0:
                        print(f"   • Снижает уровень розыска на {abs(value)}%")
                    else:
                        print(f"   • Повышает уровень розыска на {value}%")
                elif bonus_type in ["scanning", "cracking", "stealth", "social_eng"]:
                    current = game_state.get_skill(bonus_type)
                    print(f"   • Повышает {bonus_type.replace('_', ' ').title()} на {value} (текущий: {current}/10)")
                elif bonus_type == "reputation":
                    print(f"   • Повышает репутацию на {value}")
        
        # Статус покупки
        if game_state.has_item(item.get("id", "")):
            print(f"\n{Colors.SUCCESS}✓ У вас уже есть этот предмет{Colors.RESET}")
        elif game_state.can_afford(item.get("price", 0), "btc_balance"):
            print(f"\n{Colors.SUCCESS}✓ Вы можете купить этот предмет{Colors.RESET}")
        else:
            needed = item.get("price", 0) - game_state.get_stat("btc_balance", 0)
            print(f"\n{Colors.ERROR}✗ Недостаточно средств (нужно еще {needed:.2f} BTC){Colors.RESET}")
        
        # Специальное предложение
        if item.get("special", False):
            duration = item.get("duration", 0)
            print(f"\n{Colors.SUCCESS}⚡ Специальное предложение! Осталось {duration} ходов{Colors.RESET}")
    
    def add_special_offer(self, item: dict, duration_turns: int = 10) -> None:
        """Добавляет специальное предложение"""
        special_item = item.copy()
        special_item["special"] = True
        special_item["duration"] = duration_turns
        
        self.special_offers.append(special_item)
        
        print(f"\n{Colors.SUCCESS}🎁 СПЕЦИАЛЬНОЕ ПРЕДЛОЖЕНИЕ!{Colors.RESET}")
        print(f"{Colors.WARNING}Новый товар доступен: {item['name']}{Colors.RESET}")
        print(f"{Colors.INFO}Предложение действует {duration_turns} ходов{Colors.RESET}")
        
        audio_system.play_sound("notification")
    
    def update_special_offers(self) -> None:
        """Обновляет специальные предложения"""
        to_remove = []
        
        for offer in self.special_offers:
            offer["duration"] -= 1
            if offer["duration"] <= 0:
                to_remove.append(offer)
        
        for offer in to_remove:
            self.special_offers.remove(offer)
            print(f"{Colors.WARNING}[!] Специальное предложение '{offer['name']}' больше недоступно{Colors.RESET}")
    
    def generate_random_offer(self) -> None:
        """Генерирует случайное специальное предложение"""
        if random.random() < 0.1:  # 10% шанс
            special_items = [
                {
                    "id": "mystery_box",
                    "name": "Таинственный ящик",
                    "price": 100,
                    "type": "documents",
                    "desc": "Никто не знает, что внутри...",
                    "bonus": {"all_skills": random.randint(1, 3)}
                },
                {
                    "id": "stolen_data",
                    "name": "Украденные данные",
                    "price": 150,
                    "type": "documents",
                    "desc": "Свежая утечка с крупной корпорации",
                    "bonus": {"reputation": 20}
                },
                {
                    "id": "prototype_tool",
                    "name": "Прототип инструмента",
                    "price": 200,
                    "type": "software",
                    "desc": "Экспериментальная разработка",
                    "bonus": {random.choice(["scanning", "cracking", "stealth", "social_eng"]): 3}
                }
            ]
            
            item = random.choice(special_items).copy()
            item["price"] = int(item["price"] * random.uniform(0.5, 1.5))  # Случайная цена
            
            self.add_special_offer(item, duration_turns=random.randint(5, 15))
    
    def get_item_by_id(self, item_id: str) -> Optional[dict]:
        """Получает товар по ID"""
        available_items = self.get_available_items()
        return next((item for item in available_items if item.get("id") == item_id), None)
    
    def get_items_by_category(self, category: str) -> List[dict]:
        """Получает товары по категории"""
        available_items = self.get_available_items()
        return [item for item in available_items if item.get("type") == category]
    
    def get_affordable_items(self) -> List[dict]:
        """Получает товары, которые игрок может купить"""
        available_items = self.get_available_items()
        balance = game_state.get_stat("btc_balance", 0)
        
        return [item for item in available_items 
                if item.get("price", 0) <= balance and not game_state.has_item(item.get("id", ""))]
    
    def get_owned_items(self) -> List[dict]:
        """Получает список купленных товаров"""
        inventory = game_state.get_stat("inventory", [])
        owned_items = []
        
        for item_id in inventory:
            # Ищем в базовых товарах
            if item_id in self.base_items:
                item = self.base_items[item_id].copy()
                item["id"] = item_id
                owned_items.append(item)
            # Ищем в специальных предложениях
            else:
                for offer in self.special_offers:
                    if offer.get("id") == item_id:
                        owned_items.append(offer)
                        break
        
        return owned_items
    
    def calculate_total_bonuses(self) -> Dict[str, int]:
        """Рассчитывает общие бонусы от всех предметов"""
        owned_items = self.get_owned_items()
        total_bonuses = {
            "scanning": 0,
            "cracking": 0,
            "stealth": 0,
            "social_eng": 0,
            "heat_reduction": 0,
            "reputation": 0
        }
        
        for item in owned_items:
            bonus = item.get("bonus", {})
            for bonus_type, value in bonus.items():
                if bonus_type in total_bonuses:
                    total_bonuses[bonus_type] += value
                elif bonus_type == "all_skills":
                    for skill in ["scanning", "cracking", "stealth", "social_eng"]:
                        total_bonuses[skill] += value
        
        return total_bonuses


# Глобальный экземпляр системы магазина
market_system = MarketSystem()