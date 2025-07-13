"""
Система криптовалютной биржи для XSS Game
"""

import random
import time
from typing import Dict, Optional

from ui.colors import XSSColors as Colors
from ui.effects import format_currency
from core.game_state import game_state
from systems.audio import audio_system
from config.game_data import CRYPTO_DATA
from systems.event_system import event_system, CryptoMarketChangeEvent


class CryptoSystem:
    """Система управления криптовалютной биржей"""
    
    def __init__(self):
        self.crypto_data = CRYPTO_DATA.copy()
        self.price_history = {symbol: [] for symbol in self.crypto_data.keys()}
        self.market_volatility = 0.05  # 5% базовая волатильность
    
    def update_crypto_prices(self) -> None:
        """Обновляет цены криптовалют"""
        for symbol in self.crypto_data:
            # Сохраняем историю
            current_price = self.crypto_data[symbol]["price"]
            self.price_history[symbol].append(current_price)
            
            # Ограничиваем историю последними 50 значениями
            if len(self.price_history[symbol]) > 50:
                self.price_history[symbol] = self.price_history[symbol][-50:]
            
            # Рассчитываем новую цену
            change_percent = random.uniform(-self.market_volatility, self.market_volatility)
            
            # Добавляем тренды для разных валют
            if symbol == "BTC":
                # BTC более стабилен
                change_percent *= 0.7
            elif symbol == "DOGE":
                # DOGE более волатилен
                change_percent *= 2.0
            
            new_price = current_price * (1 + change_percent)
            
            # Ограничиваем минимальную цену
            min_price = 0.01 if symbol in ["DOGE", "XRP"] else 1.0
            self.crypto_data[symbol]["price"] = max(min_price, new_price)
    
    def get_24h_change(self, symbol: str) -> float:
        """Получает изменение цены за 24 часа (симуляция)"""
        if symbol not in self.price_history or len(self.price_history[symbol]) < 2:
            return random.uniform(-15, 15)
        
        # Берем "старую" цену из истории
        history = self.price_history[symbol]
        if len(history) >= 10:
            old_price = history[-10]
        else:
            old_price = history[0]
        
        current_price = self.crypto_data[symbol]["price"]
        change = ((current_price - old_price) / old_price) * 100
        
        return change
    
    def show_crypto_market(self) -> None:
        """Показывает криптовалютную биржу"""
        while True:
            self.update_crypto_prices()
            
            print(f"\n{Colors.HEADER}━━━━━━━━━━━━━━━━ КРИПТО БИРЖА ━━━━━━━━━━━━━━━━{Colors.RESET}")
            
            # Статистика портфеля
            self._show_portfolio_stats()
            
            # Текущие курсы
            self._show_crypto_rates()
            
            # Меню операций
            self._show_operations_menu()
            
            action = audio_system.get_input_with_sound(f"\n{Colors.PROMPT}Выберите действие: {Colors.RESET}").lower()
            
            if action == 'b':
                self._buy_crypto_menu()
            elif action == 's':
                self._sell_crypto_menu()
            elif action == 'c':
                self._convert_menu()
            elif action == 'r':
                print(f"\n{Colors.INFO}🔄 Обновление курсов...{Colors.RESET}")
                time.sleep(0.5)
                continue
            elif action == 'h':
                self._show_price_history()
            elif action == 't':
                self._show_trading_tips()
            elif action == 'p':
                self._show_portfolio_analysis()
            elif action == 'q':
                break
            else:
                print(f"{Colors.ERROR}❌ Неверный выбор{Colors.RESET}")
                time.sleep(1)
    
    def _show_portfolio_stats(self) -> None:
        """Показывает статистику портфеля"""
        usd_balance = game_state.get_stat("usd_balance", 0)
        btc_balance = game_state.get_stat("btc_balance", 0)
        
        # Рассчитываем общую стоимость криптовалют
        total_crypto_value = 0
        for symbol in ["ETH", "LTC", "XRP", "DOGE"]:
            amount = game_state.get_stat(symbol, 0)
            if amount > 0:
                total_crypto_value += amount * self.crypto_data[symbol]["price"]
        
        # Добавляем BTC
        btc_value = btc_balance * self.crypto_data["BTC"]["price"]
        total_portfolio = usd_balance + btc_value + total_crypto_value
        
        print(f"\n{Colors.MONEY}💼 ВАШ ПОРТФЕЛЬ:{Colors.RESET}")
        print(f"   💵 USD: {format_currency(usd_balance, 'USD')}")
        print(f"   🟠 BTC: {format_currency(btc_balance, 'BTC')} ({format_currency(btc_value, 'USD')})")
        
        if total_crypto_value > 0:
            print(f"   📊 Альткоины: {format_currency(total_crypto_value, 'USD')}")
        
        print(f"   {Colors.SUCCESS}💰 Общая стоимость: {format_currency(total_portfolio, 'USD')}{Colors.RESET}")
    
    def _show_crypto_rates(self) -> None:
        """Показывает текущие курсы"""
        print(f"\n{Colors.INFO}📈 ТЕКУЩИЕ КУРСЫ:{Colors.RESET}")
        print(f"\n   {'Валюта':<8} {'Название':<12} {'Цена USD':<12} {'24ч':<10} {'Ваш баланс':<15}")
        print(f"   {'-' * 65}")
        
        for symbol, data in self.crypto_data.items():
            change_24h = self.get_24h_change(symbol)
            
            # Цвет изменения
            if change_24h > 0:
                change_color = Colors.SUCCESS
                change_icon = "📈"
            else:
                change_color = Colors.ERROR
                change_icon = "📉"
            
            # Баланс игрока
            if symbol == "BTC":
                player_balance = game_state.get_stat("btc_balance", 0)
            else:
                player_balance = game_state.get_stat(symbol, 0)
            
            balance_usd = player_balance * data["price"] if player_balance > 0 else 0
            
            print(f"   {Colors.WARNING}{symbol:<8}{Colors.RESET} {data['name']:<12} "
                  f"${data['price']:<11.2f} {change_icon} {change_color}{change_24h:+.1f}%{Colors.RESET}  ", end="")
            
            if player_balance > 0:
                print(f"{Colors.MONEY}{player_balance:.4f} (${balance_usd:.2f}){Colors.RESET}")
            else:
                print(f"{Colors.INFO}0{Colors.RESET}")
    
    def _show_operations_menu(self) -> None:
        """Показывает меню операций"""
        print(f"\n{Colors.INFO}💱 ДОСТУПНЫЕ ОПЕРАЦИИ:{Colors.RESET}")
        print(f"   [B] Купить криптовалюту")
        print(f"   [S] Продать криптовалюту")
        print(f"   [C] Конвертировать BTC ↔ USD")
        print(f"   [R] Обновить курсы")
        print(f"   [H] История цен")
        print(f"   [T] Торговые советы")
        print(f"   [P] Анализ портфеля")
        print(f"   [Q] Выйти")
    
    def _buy_crypto_menu(self) -> None:
        """Меню покупки криптовалюты"""
        print(f"\n{Colors.SUCCESS}=== ПОКУПКА КРИПТОВАЛЮТЫ ==={Colors.RESET}")
        
        # Показываем доступные валюты
        print(f"\n{Colors.INFO}Доступные валюты:{Colors.RESET}")
        symbols = list(self.crypto_data.keys())
        for i, symbol in enumerate(symbols, 1):
            price = self.crypto_data[symbol]["price"]
            change = self.get_24h_change(symbol)
            change_color = Colors.SUCCESS if change > 0 else Colors.ERROR
            print(f"   {i}. {symbol} - {self.crypto_data[symbol]['name']} "
                  f"(${price:.2f}, {change_color}{change:+.1f}%{Colors.RESET})")
        
        choice = input(f"\n{Colors.PROMPT}Выберите валюту (1-{len(symbols)}) или символ: {Colors.RESET}").upper()
        
        # Преобразуем числовой выбор в символ
        if choice.isdigit() and 1 <= int(choice) <= len(symbols):
            symbol = symbols[int(choice) - 1]
        elif choice in self.crypto_data:
            symbol = choice
        else:
            print(f"{Colors.ERROR}❌ Неверный выбор{Colors.RESET}")
            return
        
        self._buy_crypto(symbol)
    
    def _buy_crypto(self, symbol: str) -> None:
        """Покупает криптовалюту"""
        price = self.crypto_data[symbol]["price"]
        usd_balance = game_state.get_stat("usd_balance", 0)
        
        print(f"\n{Colors.INFO}Покупка {symbol} по курсу ${price:.2f}{Colors.RESET}")
        print(f"{Colors.INFO}Доступно: {format_currency(usd_balance, 'USD')}{Colors.RESET}")
        
        amount_input = input(f"{Colors.PROMPT}Сумма в USD (или 'max' для всей суммы): {Colors.RESET}")
        
        try:
            if amount_input.lower() == 'max':
                amount_usd = usd_balance
            else:
                amount_usd = float(amount_input)
        except ValueError:
            print(f"{Colors.ERROR}❌ Неверная сумма{Colors.RESET}")
            return

        if amount_usd < 10:  # Было без ограничения
            print(f"{Colors.ERROR}Минимальная сумма операции: 10 USD{Colors.RESET}")
            return
        
        # Комиссия 1%
        fee = amount_usd * 0.02
        total_cost = amount_usd + fee
        
        if total_cost > usd_balance:
            print(f"{Colors.ERROR}❌ Недостаточно USD с учетом комиссии{Colors.RESET}")
            return
        
        crypto_amount = amount_usd / price
        
        # Подтверждение
        print(f"\n{Colors.WARNING}Подтверждение операции:{Colors.RESET}")
        print(f"   Покупка: {crypto_amount:.4f} {symbol}")
        print(f"   Стоимость: {format_currency(amount_usd, 'USD')}")
        print(f"   Комиссия: {format_currency(fee, 'USD')} (1%)")
        print(f"   Итого: {format_currency(total_cost, 'USD')}")
        
        confirm = input(f"\n{Colors.PROMPT}Подтвердить? (y/n): {Colors.RESET}").lower()
        
        if confirm == 'y':
            game_state.modify_stat("usd_balance", -total_cost)
            
            if symbol == "BTC":
                game_state.modify_stat("btc_balance", crypto_amount)
            else:
                current = game_state.get_stat(symbol, 0)
                game_state.set_stat(symbol, current + crypto_amount)
            
            audio_system.play_sound("coin")
            print(f"\n{Colors.SUCCESS}✅ Успешно куплено {crypto_amount:.4f} {symbol}!{Colors.RESET}")
            print(f"{Colors.INFO}Комиссия: {format_currency(fee, 'USD')}{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}Операция отменена{Colors.RESET}")
    
    def _sell_crypto_menu(self) -> None:
        """Меню продажи криптовалюты"""
        print(f"\n{Colors.ERROR}=== ПРОДАЖА КРИПТОВАЛЮТЫ ==={Colors.RESET}")
        
        # Показываем валюты с балансом
        available_cryptos = []
        print(f"\n{Colors.INFO}Ваши криптовалюты:{Colors.RESET}")
        
        for symbol in self.crypto_data:
            if symbol == "BTC":
                balance = game_state.get_stat("btc_balance", 0)
            else:
                balance = game_state.get_stat(symbol, 0)
            
            if balance > 0:
                available_cryptos.append(symbol)
                value_usd = balance * self.crypto_data[symbol]["price"]
                change = self.get_24h_change(symbol)
                change_color = Colors.SUCCESS if change > 0 else Colors.ERROR
                print(f"   {len(available_cryptos)}. {symbol}: {balance:.4f} "
                      f"({format_currency(value_usd, 'USD')}, {change_color}{change:+.1f}%{Colors.RESET})")
        
        if not available_cryptos:
            print(f"{Colors.WARNING}У вас нет криптовалют для продажи{Colors.RESET}")
            return
        
        choice = input(f"\n{Colors.PROMPT}Выберите валюту (1-{len(available_cryptos)}) или символ: {Colors.RESET}").upper()
        
        # Преобразуем выбор
        if choice.isdigit() and 1 <= int(choice) <= len(available_cryptos):
            symbol = available_cryptos[int(choice) - 1]
        elif choice in available_cryptos:
            symbol = choice
        else:
            print(f"{Colors.ERROR}❌ Неверный выбор{Colors.RESET}")
            return
        
        self._sell_crypto(symbol)
    
    def _sell_crypto(self, symbol: str) -> None:
        """Продает криптовалюту"""
        if symbol == "BTC":
            balance = game_state.get_stat("btc_balance", 0)
        else:
            balance = game_state.get_stat(symbol, 0)
        
        price = self.crypto_data[symbol]["price"]
        
        print(f"\n{Colors.INFO}Продажа {symbol} по курсу ${price:.2f}{Colors.RESET}")
        print(f"{Colors.INFO}Доступно: {balance:.4f} {symbol}{Colors.RESET}")
        
        amount_input = input(f"{Colors.PROMPT}Количество {symbol} (или 'max' для всего): {Colors.RESET}")
        
        try:
            if amount_input.lower() == 'max':
                amount = balance
            else:
                amount = float(amount_input)
        except ValueError:
            print(f"{Colors.ERROR}❌ Неверное количество{Colors.RESET}")
            return

        if amount < 0.001:  # Для BTC операций
            print(f"{Colors.ERROR}Минимальная сумма: 0.001 BTC{Colors.RESET}")
            return
        
        if amount > balance:
            print(f"{Colors.ERROR}❌ Недостаточно {symbol}{Colors.RESET}")
            return
        
        usd_amount = amount * price
        fee = usd_amount * 0.01  # Комиссия 1%
        final_amount = usd_amount - fee
        
        # Подтверждение
        print(f"\n{Colors.WARNING}Подтверждение операции:{Colors.RESET}")
        print(f"   Продажа: {amount:.4f} {symbol}")
        print(f"   Выручка: {format_currency(usd_amount, 'USD')}")
        print(f"   Комиссия: {format_currency(fee, 'USD')} (1%)")
        print(f"   К получению: {format_currency(final_amount, 'USD')}")
        
        confirm = input(f"\n{Colors.PROMPT}Подтвердить? (y/n): {Colors.RESET}").lower()
        
        if confirm == 'y':
            if symbol == "BTC":
                game_state.modify_stat("btc_balance", -amount)
            else:
                current = game_state.get_stat(symbol, 0)
                game_state.set_stat(symbol, current - amount)
            
            game_state.modify_stat("usd_balance", final_amount)
            
            audio_system.play_sound("sell")
            print(f"\n{Colors.SUCCESS}✅ Успешно продано {amount:.4f} {symbol}!{Colors.RESET}")
            print(f"{Colors.INFO}Получено: {format_currency(final_amount, 'USD')}{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}Операция отменена{Colors.RESET}")
    
    def _convert_menu(self) -> None:
        """Меню конвертации BTC/USD"""
        print(f"\n{Colors.WARNING}=== КОНВЕРТАЦИЯ BTC ↔ USD ==={Colors.RESET}")
        
        btc_price = self.crypto_data["BTC"]["price"]
        btc_balance = game_state.get_stat("btc_balance", 0)
        usd_balance = game_state.get_stat("usd_balance", 0)
        
        print(f"\n{Colors.INFO}Текущий курс: 1 BTC = ${btc_price:.2f}{Colors.RESET}")
        print(f"Ваши балансы:")
        print(f"   BTC: {btc_balance:.4f}")
        print(f"   USD: ${usd_balance:.2f}")
        
        print(f"\n   1. BTC → USD")
        print(f"   2. USD → BTC")
        
        choice = input(f"\n{Colors.PROMPT}Выберите направление: {Colors.RESET}")
        
        if choice == '1':
            amount = input(f"{Colors.PROMPT}Количество BTC: {Colors.RESET}")
            try:
                self.convert_btc_to_usd(float(amount))
            except ValueError:
                print(f"{Colors.ERROR}❌ Неверное количество{Colors.RESET}")
        elif choice == '2':
            amount = input(f"{Colors.PROMPT}Сумма USD: {Colors.RESET}")
            try:
                self.convert_usd_to_btc(float(amount))
            except ValueError:
                print(f"{Colors.ERROR}❌ Неверная сумма{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}❌ Неверный выбор{Colors.RESET}")
    
    def convert_btc_to_usd(self, amount: float) -> bool:
        """Конвертирует BTC в USD"""
        if amount <= 0:
            print(f"{Colors.ERROR}❌ Количество должно быть положительным{Colors.RESET}")
            return False
        
        btc_balance = game_state.get_stat("btc_balance", 0)
        if amount > btc_balance:
            print(f"{Colors.ERROR}❌ Недостаточно BTC{Colors.RESET}")
            return False
        
        btc_price = self.crypto_data["BTC"]["price"]
        usd_amount = amount * btc_price
        
        game_state.modify_stat("btc_balance", -amount)
        game_state.modify_stat("usd_balance", usd_amount)
        
        audio_system.play_sound("coin")
        print(f"{Colors.SUCCESS}✅ Обменяно {amount:.4f} BTC на ${usd_amount:.2f}{Colors.RESET}")
        return True
    
    def convert_usd_to_btc(self, amount: float) -> bool:
        """Конвертирует USD в BTC"""
        if amount <= 0:
            print(f"{Colors.ERROR}❌ Сумма должна быть положительной{Colors.RESET}")
            return False
        
        usd_balance = game_state.get_stat("usd_balance", 0)
        if amount > usd_balance:
            print(f"{Colors.ERROR}❌ Недостаточно USD{Colors.RESET}")
            return False
        
        btc_price = self.crypto_data["BTC"]["price"]
        btc_amount = amount / btc_price
        
        game_state.modify_stat("usd_balance", -amount)
        game_state.modify_stat("btc_balance", btc_amount)
        
        audio_system.play_sound("coin")
        print(f"{Colors.SUCCESS}✅ Обменяно ${amount:.2f} на {btc_amount:.4f} BTC{Colors.RESET}")
        return True
    
    def _show_price_history(self) -> None:
        """Показывает историю цен"""
        print(f"\n{Colors.INFO}📊 ИСТОРИЯ ЦЕН (последние изменения):{Colors.RESET}")
        
        for symbol, history in self.price_history.items():
            if len(history) < 2:
                continue
            
            print(f"\n{Colors.WARNING}{symbol} ({self.crypto_data[symbol]['name']}):{Colors.RESET}")
            
            # Показываем последние 5 цен
            recent_prices = history[-5:]
            trend_indicators = []
            
            for i in range(1, len(recent_prices)):
                if recent_prices[i] > recent_prices[i-1]:
                    trend_indicators.append("↗")
                elif recent_prices[i] < recent_prices[i-1]:
                    trend_indicators.append("↘")
                else:
                    trend_indicators.append("→")
            
            price_str = f"   ${recent_prices[0]:.2f}"
            for i, price in enumerate(recent_prices[1:], 0):
                color = Colors.SUCCESS if trend_indicators[i] == "↗" else Colors.ERROR if trend_indicators[i] == "↘" else Colors.INFO
                price_str += f" {color}{trend_indicators[i]} ${price:.2f}{Colors.RESET}"
            
            print(price_str)
        
        input(f"\n{Colors.INFO}Нажмите ENTER для продолжения...{Colors.RESET}")
    
    def _show_trading_tips(self) -> None:
        """Показывает торговые советы"""
        tips = [
            "💡 Покупайте на падении, продавайте на росте",
            "⚠️ Не вкладывайте все деньги в одну валюту",
            "📈 Следите за трендами - они могут дать подсказку",
            "🕒 Лучшее время для торговли - когда рынок волатилен",
            "💰 Помните про комиссии - они снижают прибыль",
            "🎯 Устанавливайте цели для покупки и продажи",
            "📊 Изучайте историю цен перед принятием решений",
            "🚫 Не торгуйте на эмоциях"
        ]
        
        print(f"\n{Colors.INFO}💡 ТОРГОВЫЕ СОВЕТЫ:{Colors.RESET}")
        for tip in random.sample(tips, 4):  # Показываем 4 случайных совета
            print(f"   {tip}")
        
        # Анализ текущего рынка
        print(f"\n{Colors.WARNING}📊 АНАЛИЗ РЫНКА:{Colors.RESET}")
        
        growing_coins = []
        falling_coins = []
        
        for symbol in self.crypto_data:
            change = self.get_24h_change(symbol)
            if change > 5:
                growing_coins.append((symbol, change))
            elif change < -5:
                falling_coins.append((symbol, change))
        
        if growing_coins:
            print(f"   {Colors.SUCCESS}📈 Растущие валюты:{Colors.RESET}")
            for symbol, change in sorted(growing_coins, key=lambda x: x[1], reverse=True):
                print(f"      {symbol}: +{change:.1f}%")
        
        if falling_coins:
            print(f"   {Colors.ERROR}📉 Падающие валюты:{Colors.RESET}")
            for symbol, change in sorted(falling_coins, key=lambda x: x[1]):
                print(f"      {symbol}: {change:.1f}%")
        
        if not growing_coins and not falling_coins:
            print(f"   {Colors.INFO}Рынок относительно стабилен{Colors.RESET}")
        
        input(f"\n{Colors.INFO}Нажмите ENTER для продолжения...{Colors.RESET}")
    
    def _show_portfolio_analysis(self) -> None:
        """Показывает анализ портфеля"""
        print(f"\n{Colors.INFO}📊 АНАЛИЗ ПОРТФЕЛЯ:{Colors.RESET}")
        
        # Подсчитываем распределение активов
        usd_balance = game_state.get_stat("usd_balance", 0)
        btc_balance = game_state.get_stat("btc_balance", 0)
        btc_value = btc_balance * self.crypto_data["BTC"]["price"]
        
        total_crypto_value = btc_value
        crypto_breakdown = {"BTC": btc_value}
        
        for symbol in ["ETH", "LTC", "XRP", "DOGE"]:
            amount = game_state.get_stat(symbol, 0)
            if amount > 0:
                value = amount * self.crypto_data[symbol]["price"]
                total_crypto_value += value
                crypto_breakdown[symbol] = value
        
        total_portfolio = usd_balance + total_crypto_value
        
        if total_portfolio == 0:
            print(f"   {Colors.WARNING}Портфель пуст{Colors.RESET}")
            return
        
        # Показываем распределение
        print(f"\n   {Colors.SUCCESS}Общая стоимость: ${total_portfolio:.2f}{Colors.RESET}")
        print(f"\n   Распределение активов:")
        
        if usd_balance > 0:
            usd_percent = (usd_balance / total_portfolio) * 100
            print(f"      💵 USD: {usd_percent:.1f}% (${usd_balance:.2f})")
        
        for symbol, value in crypto_breakdown.items():
            if value > 0:
                percent = (value / total_portfolio) * 100
                print(f"      🟠 {symbol}: {percent:.1f}% (${value:.2f})")
        
        # Рекомендации
        print(f"\n   {Colors.WARNING}Рекомендации:{Colors.RESET}")
        
        cash_percent = (usd_balance / total_portfolio) * 100 if total_portfolio > 0 else 0
        
        if cash_percent > 70:
            print(f"      • Слишком много наличных - рассмотрите инвестиции в крипту")
        elif cash_percent < 10:
            print(f"      • Мало ликвидности - оставьте часть в USD для маневров")
        
        if len(crypto_breakdown) == 1:
            print(f"      • Диверсифицируйте портфель - купите разные валюты")
        
        btc_percent = (btc_value / total_portfolio) * 100 if total_portfolio > 0 else 0
        if btc_percent > 80:
            print(f"      • Слишком большая доля BTC - рассмотрите альткоины")
        
        input(f"\n{Colors.INFO}Нажмите ENTER для продолжения...{Colors.RESET}")
    
    def get_crypto_price(self, symbol: str) -> float:
        """Получает текущую цену криптовалюты"""
        return self.crypto_data.get(symbol, {}).get("price", 0.0)
    
    def get_portfolio_value(self) -> float:
        """Получает общую стоимость портфеля"""
        total = game_state.get_stat("usd_balance", 0)
        
        for symbol in self.crypto_data:
            if symbol == "BTC":
                amount = game_state.get_stat("btc_balance", 0)
            else:
                amount = game_state.get_stat(symbol, 0)
            
            total += amount * self.crypto_data[symbol]["price"]
        
        return total

    def simulate_market_event(self, event_type: str) -> None:
        """Симулирует рыночное событие С ОТПРАВКОЙ СОБЫТИЙ"""
        if event_type == "bull_run":
            # Бычий рынок - все растет
            for symbol in self.crypto_data:
                old_price = self.crypto_data[symbol]["price"]
                multiplier = random.uniform(1.1, 1.3)
                new_price = old_price * multiplier
                self.crypto_data[symbol]["price"] = new_price

                # ОТПРАВЛЯЕМ СОБЫТИЕ
                change_percent = ((new_price - old_price) / old_price) * 100
                market_event = CryptoMarketChangeEvent(symbol, old_price, new_price, change_percent)
                event_system.dispatch(market_event)

            print(f"{Colors.SUCCESS}📈 Бычий рынок! Все криптовалюты растут!{Colors.RESET}")

        elif event_type == "bear_market":
            # Медвежий рынок - все падает
            for symbol in self.crypto_data:
                old_price = self.crypto_data[symbol]["price"]
                multiplier = random.uniform(0.7, 0.9)
                new_price = old_price * multiplier
                self.crypto_data[symbol]["price"] = new_price

                # ОТПРАВЛЯЕМ СОБЫТИЕ
                change_percent = ((new_price - old_price) / old_price) * 100
                market_event = CryptoMarketChangeEvent(symbol, old_price, new_price, change_percent)
                event_system.dispatch(market_event)

            print(f"{Colors.ERROR}📉 Медвежий рынок! Криптовалюты падают!{Colors.RESET}")

        elif event_type == "volatility":
            # Повышенная волатильность
            self.market_volatility = 0.15  # 15%
            print(f"{Colors.WARNING}⚡ Повышенная волатильность на рынке!{Colors.RESET}")

        elif event_type == "stability":
            # Стабильный рынок
            self.market_volatility = 0.02  # 2%
            print(f"{Colors.INFO}📊 Рынок стабилизировался{Colors.RESET}")


# Глобальный экземпляр системы криптовалют
crypto_system = CryptoSystem()