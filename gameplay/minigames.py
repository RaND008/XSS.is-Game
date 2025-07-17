"""
Мини-игры для XSS Game
"""

import random
import time
from typing import Tuple

from ui.colors import XSSColors
from systems.audio import audio_system
from core.game_state import game_state


class Minigame:
    """Базовый класс для мини-игр"""

    def __init__(self, name: str, description: str, skill: str):
        self.name = name
        self.description = description
        self.skill = skill

    def play(self) -> bool:
        """Запускает мини-игру. Возвращает True при успехе"""
        raise NotImplementedError

    def get_difficulty(self) -> int:
        """Возвращает сложность в зависимости от навыка игрока"""
        skill_level = game_state.get_skill(self.skill)
        return min(4 + skill_level // 2, 8)

    def get_reputation_reward(self) -> int:
        """Рассчитывает награду репутации для этой мини-игры"""
        skill_level = game_state.get_skill(self.skill)
        difficulty = self.get_difficulty()

        base_rep = 2
        difficulty_bonus = difficulty // 2
        skill_bonus = 1 if skill_level >= 7 else 0

        return base_rep + difficulty_bonus + skill_bonus

    def show_potential_rewards(self) -> None:
        """Показывает потенциальные награды перед началом игры"""
        skill_level = game_state.get_skill(self.skill)
        rep_reward = self.get_reputation_reward()

        print(f"\n{XSSColors.INFO}🏆 ПОТЕНЦИАЛЬНЫЕ НАГРАДЫ:{XSSColors.RESET}")
        print(f"   💰 BTC: 5-20")
        print(f"   ⭐ Репутация: {rep_reward}")
        print(f"   📊 Сложность: {self.get_difficulty()}/8")


class PasswordCrackGame(Minigame):
    """Мини-игра взлома пароля"""

    def __init__(self):
        super().__init__(
            "Взлом пароля",
            "Угадайте 4-значный код за 5 попыток",
            "cracking"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ ВЗЛОМ ПАРОЛЯ ━━━━━━━━━━{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Угадайте 4-значный код за 5 попыток{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}✓{XSSColors.RESET} - цифра на правильном месте")
        print(f"{XSSColors.WARNING}?{XSSColors.RESET} - цифра есть, но не на том месте")
        print(f"{XSSColors.ERROR}✗{XSSColors.RESET} - цифры нет в пароле\n")

        # Генерируем случайный пароль
        password = [str(random.randint(0, 9)) for _ in range(4)]
        attempts = 5

        while attempts > 0:
            guess = input(f"{XSSColors.PROMPT}Попытка {6 - attempts}/5: {XSSColors.RESET}")

            if len(guess) != 4 or not guess.isdigit():
                print(f"{XSSColors.ERROR}Введите 4 цифры!{XSSColors.RESET}")
                continue

            if list(guess) == password:
                audio_system.play_sound("minigame_win")
                print(f"\n{XSSColors.SUCCESS}🎉 ВЗЛОМАНО! Пароль: {''.join(password)}{XSSColors.RESET}")
                return True

            # Проверяем цифры
            result = []
            for i, digit in enumerate(guess):
                if digit == password[i]:
                    result.append(f"{XSSColors.SUCCESS}✓{XSSColors.RESET}")
                elif digit in password:
                    result.append(f"{XSSColors.WARNING}?{XSSColors.RESET}")
                else:
                    result.append(f"{XSSColors.ERROR}✗{XSSColors.RESET}")

            print(f"Результат: {' '.join(result)}")
            attempts -= 1

        audio_system.play_sound("minigame_lose")
        print(f"\n{XSSColors.ERROR}❌ Провал! Пароль был: {''.join(password)}{XSSColors.RESET}")
        return False


class FirewallBypassGame(Minigame):
    """Улучшенная мини-игра обхода файрвола с реалистичными техниками"""

    def __init__(self):
        super().__init__(
            "Обход файрвола",
            "Используйте различные техники для обхода сетевой защиты",
            "stealth"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        self._show_firewall_interface()

        skill_level = game_state.get_skill(self.skill)
        firewall_config = self._get_firewall_config(skill_level)

        # Генерируем конфигурацию файрвола
        firewall_rules = self._generate_firewall_rules(firewall_config)

        # Показываем информацию о цели
        target_info = self._generate_target_info(firewall_config)
        self._show_target_analysis(target_info, firewall_rules)

        # Основной игровой процесс
        return self._run_bypass_attempt(firewall_rules, target_info, firewall_config)

    def _show_firewall_interface(self):
        """Показывает интерфейс анализатора файрвола"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║              🛡️  FIREWALL PENETRATION TOOLKIT v3.7           ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                    АНАЛИЗ СЕТЕВОЙ ЗАЩИТЫ                     ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🎯 ЗАДАЧА: Обойти файрвол и достичь целевого сервиса{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🔍 Анализируйте правила, выберите технику обхода{XSSColors.RESET}")

    def _get_firewall_config(self, skill_level):
        """Конфигурация файрвола в зависимости от сложности"""
        configs = {
            'basic': {
                'rules_count': 3,
                'complexity': 'simple',
                'deep_inspection': False,
                'techniques_available': ['port_knocking', 'tunnel_http', 'fragment'],
                'time_limit': None,
                'hints_available': 2
            },
            'intermediate': {
                'rules_count': 5,
                'complexity': 'moderate',
                'deep_inspection': True,
                'techniques_available': ['port_knocking', 'tunnel_http', 'fragment', 'dns_tunnel', 'steganography'],
                'time_limit': 180,
                'hints_available': 1
            },
            'advanced': {
                'rules_count': 7,
                'complexity': 'complex',
                'deep_inspection': True,
                'techniques_available': ['port_knocking', 'tunnel_http', 'fragment', 'dns_tunnel', 'steganography',
                                         'timing_attack'],
                'time_limit': 120,
                'hints_available': 1
            },
            'expert': {
                'rules_count': 10,
                'complexity': 'sophisticated',
                'deep_inspection': True,
                'techniques_available': ['port_knocking', 'tunnel_http', 'fragment', 'dns_tunnel', 'steganography',
                                         'timing_attack', 'covert_channel'],
                'time_limit': 90,
                'hints_available': 0
            }
        }

        if skill_level <= 2:
            return configs['basic']
        elif skill_level <= 5:
            return configs['intermediate']
        elif skill_level <= 7:
            return configs['advanced']
        else:
            return configs['expert']

    def _generate_firewall_rules(self, config):
        """Генерирует правила файрвола"""
        rules = []
        rule_types = [
            {'type': 'port_block', 'ports': [22, 23, 80, 443, 3389], 'description': 'Блокировка стандартных портов'},
            {'type': 'ip_whitelist', 'ips': ['192.168.1.0/24', '10.0.0.0/8'], 'description': 'Разрешенные IP сети'},
            {'type': 'protocol_filter', 'protocols': ['TCP', 'UDP', 'ICMP'], 'description': 'Фильтрация протоколов'},
            {'type': 'content_filter', 'keywords': ['hack', 'exploit', 'payload'],
             'description': 'Фильтрация содержимого'},
            {'type': 'rate_limit', 'limit': '100 req/min', 'description': 'Ограничение скорости'},
            {'type': 'geo_block', 'countries': ['CN', 'RU', 'KP'], 'description': 'Географическая блокировка'},
            {'type': 'time_restriction', 'hours': '09:00-17:00', 'description': 'Временные ограничения'},
            {'type': 'signature_detection', 'signatures': ['Nmap', 'Metasploit'],
             'description': 'Обнаружение сигнатур'},
            {'type': 'ssl_inspection', 'enabled': True, 'description': 'Инспекция SSL трафика'},
            {'type': 'anomaly_detection', 'threshold': 'medium', 'description': 'Обнаружение аномалий'}
        ]

        # Выбираем случайные правила
        selected_rules = random.sample(rule_types, min(len(rule_types), config['rules_count']))

        for i, rule in enumerate(selected_rules, 1):
            rules.append({
                'id': i,
                'type': rule['type'],
                'details': rule,
                'bypass_difficulty': random.randint(1, 5),
                'effective_techniques': self._get_effective_techniques(rule['type'])
            })

        return rules

    def _get_effective_techniques(self, rule_type):
        """Возвращает эффективные техники для обхода конкретного правила"""
        technique_map = {
            'port_block': ['port_knocking', 'tunnel_http', 'dns_tunnel'],
            'ip_whitelist': ['tunnel_http', 'dns_tunnel', 'covert_channel'],
            'protocol_filter': ['fragment', 'steganography', 'covert_channel'],
            'content_filter': ['steganography', 'fragment', 'tunnel_http'],
            'rate_limit': ['timing_attack', 'fragment', 'covert_channel'],
            'geo_block': ['tunnel_http', 'dns_tunnel', 'covert_channel'],
            'time_restriction': ['timing_attack', 'covert_channel'],
            'signature_detection': ['steganography', 'fragment', 'covert_channel'],
            'ssl_inspection': ['dns_tunnel', 'covert_channel', 'steganography'],
            'anomaly_detection': ['timing_attack', 'steganography', 'covert_channel']
        }
        return technique_map.get(rule_type, ['tunnel_http'])

    def _generate_target_info(self, config):
        """Генерирует информацию о цели"""
        targets = [
            {
                'name': 'Web Server',
                'ip': '10.0.1.100',
                'port': 80,
                'service': 'Apache/2.4.41',
                'vulnerability': 'Outdated version'
            },
            {
                'name': 'Database Server',
                'ip': '10.0.1.200',
                'port': 3306,
                'service': 'MySQL 5.7',
                'vulnerability': 'Weak authentication'
            },
            {
                'name': 'SSH Server',
                'ip': '10.0.1.50',
                'port': 22,
                'service': 'OpenSSH 7.4',
                'vulnerability': 'Default credentials'
            },
            {
                'name': 'FTP Server',
                'ip': '10.0.1.150',
                'port': 21,
                'service': 'vsftpd 3.0.3',
                'vulnerability': 'Anonymous access'
            }
        ]

        return random.choice(targets)

    def _show_target_analysis(self, target_info, firewall_rules):
        """Показывает анализ цели и правил файрвола"""
        print(f"\n{XSSColors.WARNING}🎯 ЦЕЛЬ АТАКИ:{XSSColors.RESET}")
        print(f"   Сервис: {XSSColors.BRIGHT_GREEN}{target_info['name']}{XSSColors.RESET}")
        print(f"   IP: {target_info['ip']}")
        print(f"   Порт: {target_info['port']}")
        print(f"   Версия: {target_info['service']}")
        print(f"   Уязвимость: {XSSColors.ERROR}{target_info['vulnerability']}{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}🛡️ ОБНАРУЖЕННЫЕ ПРАВИЛА ФАЙРВОЛА:{XSSColors.RESET}")
        for rule in firewall_rules:
            difficulty_color = self._get_difficulty_color(rule['bypass_difficulty'])
            print(f"   {rule['id']}. {rule['details']['description']}")
            print(f"      Тип: {rule['type']}")
            print(f"      Сложность обхода: {difficulty_color}{rule['bypass_difficulty']}/5{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🔧 ДОСТУПНЫЕ ТЕХНИКИ ОБХОДА:{XSSColors.RESET}")

    def _run_bypass_attempt(self, firewall_rules, target_info, config):
        """Основной процесс обхода файрвола"""
        techniques_used = []
        rules_bypassed = []
        hints_used = 0
        start_time = time.time()

        # Показываем доступные техники
        available_techniques = config['techniques_available']
        for i, technique in enumerate(available_techniques, 1):
            technique_name = self._get_technique_display_name(technique)
            print(f"   {XSSColors.BRIGHT_GREEN}{i}.{XSSColors.RESET} {technique_name}")

        print(f"\n{XSSColors.INFO}📋 КОМАНДЫ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}use <technique_id> <rule_id>{XSSColors.RESET} - Применить технику к правилу")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze <rule_id>{XSSColors.RESET} - Анализировать правило")
        print(f"   {XSSColors.BRIGHT_GREEN}status{XSSColors.RESET} - Показать статус обхода")
        print(f"   {XSSColors.BRIGHT_GREEN}hint{XSSColors.RESET} - Получить подсказку")
        print(f"   {XSSColors.BRIGHT_GREEN}attack{XSSColors.RESET} - Попытаться атаковать цель")
        print(f"   {XSSColors.BRIGHT_GREEN}help{XSSColors.RESET} - Показать справку с примерами")

        print(f"\n{XSSColors.WARNING}💡 ПРИМЕР ИСПОЛЬЗОВАНИЯ:{XSSColors.RESET}")
        print(f"   {XSSColors.LIGHT_GRAY}use 1 2{XSSColors.RESET} - Применить технику #1 к правилу #2")
        print(f"   {XSSColors.LIGHT_GRAY}analyze 3{XSSColors.RESET} - Анализировать правило #3")

        while len(rules_bypassed) < len(firewall_rules):
            # Проверяем временное ограничение
            if config['time_limit']:
                elapsed = time.time() - start_time
                remaining = config['time_limit'] - elapsed
                if remaining <= 0:
                    print(f"\n{XSSColors.ERROR}⏰ ВРЕМЯ ВЫШЛО! Файрвол обнаружил вторжение!{XSSColors.RESET}")
                    return False
                elif remaining <= 30:
                    print(f"{XSSColors.WARNING}⚠️ Осталось {remaining:.0f} секунд!{XSSColors.RESET}")

            # Показываем статус
            self._show_bypass_status(rules_bypassed, len(firewall_rules), techniques_used)

            # Получаем команду
            command = audio_system.get_input_with_sound(
                f"{XSSColors.PROMPT}[Bypass]> {XSSColors.RESET}").strip().lower()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0]

            if cmd == "use" and len(parts) >= 3:
                try:
                    technique_id = int(parts[1])
                    rule_id = int(parts[2])

                    # Проверяем валидность ID техники
                    if not (1 <= technique_id <= len(available_techniques)):
                        print(
                            f"{XSSColors.ERROR}Неверный ID техники. Доступно: 1-{len(available_techniques)}{XSSColors.RESET}")
                        continue

                    # Получаем технику по ID
                    technique = available_techniques[technique_id - 1]

                    result = self._attempt_bypass(technique, rule_id, firewall_rules, available_techniques)
                    if result['success']:
                        if rule_id not in rules_bypassed:
                            rules_bypassed.append(rule_id)
                        if technique not in techniques_used:
                            techniques_used.append(technique)
                        print(f"{XSSColors.SUCCESS}✅ {result['message']}{XSSColors.RESET}")
                    else:
                        print(f"{XSSColors.ERROR}❌ {result['message']}{XSSColors.RESET}")
                        if result.get('detected', False):
                            print(
                                f"{XSSColors.DANGER}🚨 ОБНАРУЖЕНИЕ! Файрвол зафиксировал подозрительную активность!{XSSColors.RESET}")
                            return False
                except ValueError:
                    print(
                        f"{XSSColors.ERROR}Неверный формат. Используйте: use <technique_id> <rule_id>{XSSColors.RESET}")
                    print(f"{XSSColors.INFO}Пример: use 1 2 (применить технику #1 к правилу #2){XSSColors.RESET}")

            elif cmd == "analyze" and len(parts) > 1:
                try:
                    rule_id = int(parts[1])
                    self._analyze_rule(rule_id, firewall_rules)
                except ValueError:
                    print(f"{XSSColors.ERROR}Неверный ID правила{XSSColors.RESET}")

            elif cmd == "status":
                self._show_detailed_status(firewall_rules, rules_bypassed, techniques_used)

            elif cmd == "hint":
                if hints_used < config['hints_available']:
                    self._give_bypass_hint(firewall_rules, rules_bypassed, hints_used)
                    hints_used += 1
                else:
                    print(f"{XSSColors.WARNING}Подсказки исчерпаны{XSSColors.RESET}")

            elif cmd == "attack":
                if len(rules_bypassed) == len(firewall_rules):
                    return self._attempt_final_attack(target_info, time.time() - start_time, techniques_used)
                else:
                    remaining_rules = len(firewall_rules) - len(rules_bypassed)
                    print(
                        f"{XSSColors.WARNING}Файрвол все еще активен! Осталось обойти правил: {remaining_rules}{XSSColors.RESET}")

            elif cmd == "help":
                self._show_bypass_help()

            else:
                print(f"{XSSColors.ERROR}Неизвестная команда. Используйте 'help' для справки{XSSColors.RESET}")

        # Если все правила обойдены
        print(f"\n{XSSColors.SUCCESS}🎉 ВСЕ ПРАВИЛА ФАЙРВОЛА ОБОЙДЕНЫ!{XSSColors.RESET}")
        return self._attempt_final_attack(target_info, time.time() - start_time, techniques_used)

    def _attempt_bypass(self, technique, rule_id, firewall_rules, available_techniques):
        """Попытка обхода конкретного правила"""
        if technique not in available_techniques:
            return {'success': False, 'message': 'Техника недоступна'}

        # Находим правило
        rule = next((r for r in firewall_rules if r['id'] == rule_id), None)
        if not rule:
            return {'success': False, 'message': 'Правило не найдено'}

        # Проверяем эффективность техники
        effective_techniques = rule['effective_techniques']
        is_effective = technique in effective_techniques

        # Рассчитываем шанс успеха
        base_chance = 0.8 if is_effective else 0.3
        difficulty_penalty = rule['bypass_difficulty'] * 0.1
        skill_bonus = game_state.get_skill(self.skill) * 0.05

        success_chance = base_chance - difficulty_penalty + skill_bonus
        success_chance = max(0.1, min(0.95, success_chance))

        # Шанс обнаружения
        detection_chance = (1 - success_chance) * 0.5 if not is_effective else 0.1

        if random.random() < success_chance:
            technique_name = self._get_technique_display_name(technique)
            return {
                'success': True,
                'message': f'Правило #{rule_id} обойдено с помощью {technique_name}'
            }
        elif random.random() < detection_chance:
            return {
                'success': False,
                'message': 'Попытка обхода обнаружена файрволом',
                'detected': True
            }
        else:
            return {
                'success': False,
                'message': 'Техника оказалась неэффективной против этого правила'
            }

    def _analyze_rule(self, rule_id, firewall_rules):
        """Анализирует конкретное правило файрвола"""
        rule = next((r for r in firewall_rules if r['id'] == rule_id), None)
        if not rule:
            print(f"{XSSColors.ERROR}Правило {rule_id} не найдено{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.INFO}🔍 АНАЛИЗ ПРАВИЛА #{rule_id}:{XSSColors.RESET}")
        print(f"   Тип: {rule['type']}")
        print(f"   Описание: {rule['details']['description']}")
        print(
            f"   Сложность: {self._get_difficulty_color(rule['bypass_difficulty'])}{rule['bypass_difficulty']}/5{XSSColors.RESET}")

        # Показываем детали правила
        details = rule['details']
        if 'ports' in details:
            print(f"   Заблокированные порты: {', '.join(map(str, details['ports']))}")
        if 'ips' in details:
            print(f"   Разрешенные IP: {', '.join(details['ips'])}")
        if 'protocols' in details:
            print(f"   Фильтруемые протоколы: {', '.join(details['protocols'])}")
        if 'keywords' in details:
            print(f"   Запрещенные слова: {', '.join(details['keywords'])}")

        # Рекомендуемые техники
        effective_techniques = rule['effective_techniques']
        technique_names = [self._get_technique_display_name(t) for t in effective_techniques]
        print(f"   {XSSColors.SUCCESS}Эффективные техники: {', '.join(technique_names)}{XSSColors.RESET}")

    def _show_bypass_status(self, rules_bypassed, total_rules, techniques_used):
        """Показывает статус обхода"""
        progress = f"{len(rules_bypassed)}/{total_rules}"
        progress_color = XSSColors.SUCCESS if len(rules_bypassed) == total_rules else XSSColors.WARNING

        print(f"\n{XSSColors.INFO}📊 Прогресс: {progress_color}{progress}{XSSColors.RESET} правил обойдено")
        if techniques_used:
            print(
                f"   Использованные техники: {', '.join([self._get_technique_display_name(t) for t in techniques_used])}")

    def _show_detailed_status(self, firewall_rules, rules_bypassed, techniques_used):
        """Показывает детальный статус обхода"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ СТАТУС ОБХОДА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        for rule in firewall_rules:
            status = "✅ ОБОЙДЕНО" if rule['id'] in rules_bypassed else "🛡️ АКТИВНО"
            status_color = XSSColors.SUCCESS if rule['id'] in rules_bypassed else XSSColors.ERROR
            print(
                f"   Правило {rule['id']}: {status_color}{status}{XSSColors.RESET} - {rule['details']['description']}")

        if techniques_used:
            print(f"\n{XSSColors.INFO}🔧 Использованные техники:{XSSColors.RESET}")
            for technique in techniques_used:
                print(f"   • {self._get_technique_display_name(technique)}")

    def _give_bypass_hint(self, firewall_rules, rules_bypassed, hint_number):
        """Дает подсказку для обхода"""
        remaining_rules = [r for r in firewall_rules if r['id'] not in rules_bypassed]

        if not remaining_rules:
            print(f"{XSSColors.INFO}💡 Все правила обойдены! Используйте 'attack' для атаки на цель{XSSColors.RESET}")
            return

        if hint_number == 0:
            # Первая подсказка - о самом слабом правиле
            easiest_rule = min(remaining_rules, key=lambda r: r['bypass_difficulty'])
            print(
                f"\n{XSSColors.INFO}💡 ПОДСКАЗКА: Самое слабое правило - #{easiest_rule['id']} ({easiest_rule['details']['description']}){XSSColors.RESET}")
        else:
            # Вторая подсказка - о рекомендуемой технике
            random_rule = random.choice(remaining_rules)
            recommended_technique = random.choice(random_rule['effective_techniques'])
            technique_name = self._get_technique_display_name(recommended_technique)
            print(
                f"\n{XSSColors.INFO}💡 ПОДСКАЗКА: Попробуйте {technique_name} против правила #{random_rule['id']}{XSSColors.RESET}")

    def _attempt_final_attack(self, target_info, time_taken, techniques_used):
        """Попытка финальной атаки на цель"""
        print(f"\n{XSSColors.SUCCESS}🚀 ЗАПУСК АТАКИ НА ЦЕЛЬ...{XSSColors.RESET}")
        time.sleep(2)

        # Рассчитываем шанс успеха атаки
        base_success = 0.7
        technique_bonus = len(techniques_used) * 0.05
        time_bonus = max(0, (180 - time_taken) / 180 * 0.2)
        skill_bonus = game_state.get_skill(self.skill) * 0.03

        attack_success = base_success + technique_bonus + time_bonus + skill_bonus
        attack_success = min(0.95, attack_success)

        if random.random() < attack_success:
            self._show_attack_success(target_info, time_taken, techniques_used)
            return True
        else:
            self._show_attack_failure(target_info, time_taken)
            return False

    def _show_attack_success(self, target_info, time_taken, techniques_used):
        """Показывает экран успешной атаки"""
        audio_system.play_sound("minigame_win")

        print(f"\n{XSSColors.SUCCESS}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}                🎉 ФАЙРВОЛ УСПЕШНО ОБОЙДЕН! 🎉                {XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🎯 Цель достигнута: {target_info['name']}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}📡 Подключение установлено к {target_info['ip']}:{target_info['port']}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время обхода: {time_taken:.1f} секунд{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🔧 ИСПОЛЬЗОВАННЫЕ ТЕХНИКИ:{XSSColors.RESET}")
        for technique in techniques_used:
            print(f"   ✓ {self._get_technique_display_name(technique)}")

        # Показываем найденную уязвимость
        print(f"\n{XSSColors.ERROR}🔓 ОБНАРУЖЕНА УЯЗВИМОСТЬ:{XSSColors.RESET}")
        print(f"   {target_info['vulnerability']}")

        # Оценка производительности
        if time_taken < 60:
            rating = f"{XSSColors.SUCCESS}🌟 МОЛНИЕНОСНО!{XSSColors.RESET}"
        elif time_taken < 120:
            rating = f"{XSSColors.WARNING}💪 ОТЛИЧНО!{XSSColors.RESET}"
        else:
            rating = f"{XSSColors.INFO}👍 ХОРОШО!{XSSColors.RESET}"

        print(f"\n🏆 Оценка: {rating}")
        print(f"\n{XSSColors.SUCCESS}✅ Файрвол обойден! Доступ к внутренней сети получен.{XSSColors.RESET}")

    def _show_attack_failure(self, target_info, time_taken):
        """Показывает экран неудачной атаки"""
        audio_system.play_sound("minigame_lose")

        print(f"\n{XSSColors.ERROR}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}                    ❌ АТАКА НЕУДАЧНА ❌                     {XSSColors.RESET}")
        print(f"{XSSColors.ERROR}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}🛡️ Последний рубеж защиты устоял{XSSColors.RESET}")
        print(f"{XSSColors.WARNING}📡 Соединение с {target_info['ip']} заблокировано{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время попытки: {time_taken:.1f} секунд{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}💡 ВОЗМОЖНЫЕ ПРИЧИНЫ НЕУДАЧИ:{XSSColors.RESET}")
        print(f"   • Дополнительные меры защиты на целевом сервере")
        print(f"   • Система обнаружения вторжений (IDS)")
        print(f"   • Неожиданные изменения в конфигурации")
        print(f"   • Требуются дополнительные техники обхода")

        print(f"\n{XSSColors.INFO}🎯 Попробуйте использовать другие техники в следующий раз{XSSColors.RESET}")

    def _show_bypass_help(self):
        """Показывает справку по обходу файрвола"""
        print(f"\n{XSSColors.INFO}📖 СПРАВКА ПО ОБХОДУ ФАЙРВОЛА:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}use <technique_id> <rule_id>{XSSColors.RESET} - Применить технику к правилу")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze <rule_id>{XSSColors.RESET} - Детальный анализ правила")
        print(f"   {XSSColors.BRIGHT_GREEN}status{XSSColors.RESET} - Показать прогресс обхода")
        print(f"   {XSSColors.BRIGHT_GREEN}attack{XSSColors.RESET} - Атаковать цель (после обхода всех правил)")
        print(f"   {XSSColors.BRIGHT_GREEN}hint{XSSColors.RESET} - Получить подсказку")

        print(f"\n{XSSColors.WARNING}💡 ПРИМЕРЫ КОМАНД:{XSSColors.RESET}")
        print(f"   {XSSColors.LIGHT_GRAY}use 1 2{XSSColors.RESET} - Применить технику #1 к правилу #2")
        print(f"   {XSSColors.LIGHT_GRAY}use 3 1{XSSColors.RESET} - Применить технику #3 к правилу #1")
        print(f"   {XSSColors.LIGHT_GRAY}analyze 1{XSSColors.RESET} - Анализировать правило #1")
        print(f"   {XSSColors.LIGHT_GRAY}status{XSSColors.RESET} - Посмотреть прогресс")

        print(f"\n{XSSColors.WARNING}🔧 ТЕХНИКИ ОБХОДА:{XSSColors.RESET}")
        techniques = {
            '1. 🚪 Port Knocking': 'Секретная последовательность для открытия портов',
            '2. 🌐 HTTP Tunneling': 'Туннелирование через HTTP/HTTPS трафик',
            '3. 🧩 Packet Fragmentation': 'Фрагментация пакетов для обхода фильтров',
            '4. 📡 DNS Tunneling': 'Туннелирование через DNS запросы',
            '5. 🎭 Steganography': 'Сокрытие данных в легитимном трафике',
            '6. ⏰ Timing Attack': 'Атака на основе временных интервалов',
            '7. 🕵️ Covert Channel': 'Использование скрытых каналов связи'
        }

        for tech, desc in techniques.items():
            print(f"   • {tech}: {desc}")

        print(f"\n{XSSColors.SUCCESS}🎯 СТРАТЕГИЯ:{XSSColors.RESET}")
        print(f"   1. Используйте {XSSColors.BRIGHT_GREEN}analyze{XSSColors.RESET} для изучения правил")
        print(f"   2. Выберите эффективные техники из рекомендаций")
        print(f"   3. Применяйте техники командой {XSSColors.BRIGHT_GREEN}use{XSSColors.RESET}")
        print(f"   4. После обхода всех правил используйте {XSSColors.BRIGHT_GREEN}attack{XSSColors.RESET}")

    # Вспомогательные методы

    def _get_technique_display_name(self, technique):
        """Возвращает отображаемое имя техники"""
        names = {
            'port_knocking': '🚪 Port Knocking',
            'tunnel_http': '🌐 HTTP Tunneling',
            'fragment': '🧩 Packet Fragmentation',
            'dns_tunnel': '📡 DNS Tunneling',
            'steganography': '🎭 Steganography',
            'timing_attack': '⏰ Timing Attack',
            'covert_channel': '🕵️ Covert Channel'
        }
        return names.get(technique, technique.title())

    def _get_difficulty_color(self, difficulty):
        """Возвращает цвет для уровня сложности"""
        if difficulty <= 2:
            return XSSColors.SUCCESS
        elif difficulty <= 3:
            return XSSColors.WARNING
        else:
            return XSSColors.ERROR

    def get_difficulty(self) -> int:
        """Возвращает сложность в зависимости от навыка игрока"""
        skill_level = game_state.get_skill(self.skill)
        return min(4 + skill_level // 2, 8)

    def get_reputation_reward(self) -> int:
        """Рассчитывает награду репутации для этой мини-игры"""
        skill_level = game_state.get_skill(self.skill)
        difficulty = self.get_difficulty()

        base_rep = 3  # Увеличена базовая репутация для более сложной игры
        difficulty_bonus = difficulty // 2
        skill_bonus = 2 if skill_level >= 7 else 0

        return base_rep + difficulty_bonus + skill_bonus

    def show_potential_rewards(self) -> None:
        """Показывает потенциальные награды перед началом игры"""
        skill_level = game_state.get_skill(self.skill)
        rep_reward = self.get_reputation_reward()

        print(f"\n{XSSColors.INFO}🏆 ПОТЕНЦИАЛЬНЫЕ НАГРАДЫ:{XSSColors.RESET}")
        print(f"   💰 BTC: 8-25")
        print(f"   ⭐ Репутация: {rep_reward}")
        print(f"   📊 Сложность: {self.get_difficulty()}/8")
        print(f"   🎯 Тип навыка: Stealth (Скрытность)")

        if skill_level >= 8:
            print(f"   ✨ Экспертный бонус: Дополнительные техники обхода")


class MemorySequenceGame(Minigame):
    """Мини-игра запоминания последовательности"""

    def __init__(self):
        super().__init__(
            "Взлом памяти",
            "Запомните и повторите последовательность",
            "scanning"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ ВЗЛОМ ПАМЯТИ ━━━━━━━━━━{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Запомните и повторите последовательность!{XSSColors.RESET}\n")

        # Сложность зависит от навыков
        difficulty = self.get_difficulty() # чем выше сложность, тем длиннее последовательность
        sequence_length = min(difficulty + 2, 10) # от 6 до 10 символов

        # Символы для последовательности
        symbols = ['@', '#', '$', '%', '&', '*', '!', '?']
        sequence = [random.choice(symbols) for _ in range(sequence_length)]

        # Показываем последовательность
        print(f"{XSSColors.WARNING}Запоминайте:{XSSColors.RESET}")
        time.sleep(1)

        for i, symbol in enumerate(sequence):
            print(f"\r{' ' * 20}\r{XSSColors.SUCCESS}[{i + 1}/{sequence_length}] → {symbol}{XSSColors.RESET}", end='', flush=True)
            time.sleep(2.5) # Чуть быстрее для более высокой сложности

        print(f"\r{' ' * 30}\r", end='')  # Очищаем строку

        # Просим ввести
        print(f"\n{XSSColors.INFO}Введите последовательность (без пробелов):{XSSColors.RESET}")
        user_input = audio_system.get_input_with_sound(f"{XSSColors.PROMPT}>>> {XSSColors.RESET}")

        # Проверяем
        if list(user_input) == sequence:
            audio_system.play_sound("minigame_win")
            print(f"\n{XSSColors.SUCCESS}✅ ПРАВИЛЬНО! Память системы взломана!{XSSColors.RESET}")
            return True
        else:
            audio_system.play_sound("minigame_lose")
            print(f"\n{XSSColors.ERROR}❌ НЕВЕРНО!{XSSColors.RESET}")
            print(f"Правильная последовательность: {''.join(sequence)}")
            return False


class NetworkTraceGame(Minigame):
    """Мини-игра трассировки сети"""

    def __init__(self):
        super().__init__(
            "Трассировка сети",
            "Найдите правильный путь через узлы сети",
            "scanning"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ ТРАССИРОВКА СЕТИ ━━━━━━━━━━{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Найдите правильный путь через узлы сети{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}O{XSSColors.RESET} - безопасный узел")
        print(f"{XSSColors.ERROR}X{XSSColors.RESET} - файрвол")
        print(f"{XSSColors.WARNING}?{XSSColors.RESET} - неизвестный узел\n")

        # Создаем сетку
        size = min(5 + game_state.get_skill(self.skill) // 2, 8) # Размер сетки зависит от навыка
        grid = []

        # Генерируем путь
        path = [(0, 0)]
        x, y = 0, 0

        while (x, y) != (size - 1, size - 1):
            possible_moves = []
            if x < size - 1:
                possible_moves.append((x + 1, y))
            if y < size - 1:
                possible_moves.append((x, y + 1))

            if not possible_moves: # Если достигли конца или застряли
                break

            next_x, next_y = random.choice(possible_moves)
            x, y = next_x, next_y
            path.append((x, y))

        # Заполняем сетку
        for i in range(size):
            row = []
            for j in range(size):
                if (i, j) in path:
                    row.append('O')
                elif random.random() < 0.2 + (10 - game_state.get_skill(self.skill)) * 0.03: # Больше X на низкой сложности
                    row.append('X')
                else:
                    row.append('?')
            grid.append(row)

        # Начальная и конечная точки
        grid[0][0] = 'S'
        grid[size - 1][size - 1] = 'E'

        # Показываем сетку
        print("   ", end="")
        for i in range(size):
            print(f"{i: <3}", end="")
        print()

        for i in range(size):
            print(f"{i: <3}", end="")
            for j in range(size):
                cell = grid[i][j]
                if cell == 'S':
                    print(f"{XSSColors.SUCCESS}S  {XSSColors.RESET}", end="")
                elif cell == 'E':
                    print(f"{XSSColors.SUCCESS}E  {XSSColors.RESET}", end="")
                elif cell == 'O':
                    print(f"{XSSColors.SUCCESS}O  {XSSColors.RESET}", end="")
                elif cell == 'X':
                    print(f"{XSSColors.ERROR}X  {XSSColors.RESET}", end="")
                else:
                    print(f"{XSSColors.WARNING}?  {XSSColors.RESET}", end="")
            print()

        # Игрок вводит путь
        print(f"\n{XSSColors.INFO}Введите путь (например: 0,0 0,1 1,1 ...){XSSColors.RESET}")
        print(f"{XSSColors.INFO}От S(0,0) до E({size - 1},{size - 1}){XSSColors.RESET}")

        user_path = audio_system.get_input_with_sound(f"{XSSColors.PROMPT}Путь: {XSSColors.RESET}")

        try:
            # Парсим ввод пользователя
            coords = []
            for coord_str in user_path.split():
                x, y = map(int, coord_str.split(','))
                if not (0 <= x < size and 0 <= y < size):
                    raise ValueError("Координаты вне сетки")
                coords.append((x, y))

            # Проверяем путь
            if not coords:
                raise ValueError("Путь не может быть пустым")
            if coords[0] != (0, 0) or coords[-1] != (size - 1, size - 1):
                raise ValueError(f"Путь должен начинаться с S(0,0) и заканчиваться на E({size - 1},{size - 1})")

            # Проверяем каждый шаг
            for i in range(len(coords)):
                x, y = coords[i]
                if grid[x][y] == 'X':
                    audio_system.play_sound("minigame_lose")
                    print(f"\n{XSSColors.ERROR}❌ Вы попали в файрвол на позиции ({x},{y})!{XSSColors.RESET}")
                    return False

                # Проверяем, что шаги соседние
                if i > 0:
                    prev_x, prev_y = coords[i - 1]
                    # Разрешены только горизонтальные и вертикальные шаги (не по диагонали)
                    if not ((abs(x - prev_x) == 1 and y == prev_y) or (abs(y - prev_y) == 1 and x == prev_x)):
                        audio_system.play_sound("minigame_lose")
                        print(
                            f"\n{XSSColors.ERROR}❌ Неверный путь! Можно двигаться только на соседние клетки (не по диагонали){XSSColors.RESET}")
                        return False

            audio_system.play_sound("minigame_win")
            print(f"\n{XSSColors.SUCCESS}✅ УСПЕХ! Сеть протрассирована!{XSSColors.RESET}")
            return True

        except ValueError as ve:
            audio_system.play_sound("minigame_lose")
            print(f"\n{XSSColors.ERROR}❌ Ошибка в формате или содержании пути: {ve}{XSSColors.RESET}")
            return False
        except Exception as e:
            audio_system.play_sound("minigame_lose")
            print(f"\n{XSSColors.ERROR}❌ Произошла неизвестная ошибка при проверке пути: {e}{XSSColors.RESET}")
            return False


class SQLInjectionGame(Minigame):
    """Мини-игра SQL инъекции"""

    def __init__(self):
        super().__init__(
            "SQL инъекция",
            "Найдите правильную инъекцию для обхода авторизации",
            "cracking"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ SQL ИНЪЕКЦИЯ ━━━━━━━━━━{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Найдите правильную инъекцию для обхода авторизации{XSSColors.RESET}\n")

        # Варианты инъекций
        correct_injections = [
            "' OR '1'='1",
            "admin'--",
            "' OR 1=1--",
            "' OR 'a'='a",
            "' or 1=1 #", # Добавляем новые
            "\" or \"\"=\"",
            "\" or 1=1 --",
            "') OR ('1'='1"
        ]

        # Показываем "форму входа"
        print(f"{XSSColors.INFO}┌─────────────────────────────────┐{XSSColors.RESET}")
        print(f"{XSSColors.INFO}│      ADMIN PANEL LOGIN          │{XSSColors.RESET}")
        print(f"{XSSColors.INFO}├─────────────────────────────────┤{XSSColors.RESET}")
        print(f"{XSSColors.INFO}│ Username: [admin_____________]  │{XSSColors.RESET}")
        print(f"{XSSColors.INFO}│ Password: [******************]  │{XSSColors.RESET}")
        print(f"{XSSColors.INFO}│         [  LOGIN  ]             │{XSSColors.RESET}")
        print(f"{XSSColors.INFO}└─────────────────────────────────┘{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}Подсказка: попробуйте классические SQL инъекции{XSSColors.RESET}")
        print(f"{XSSColors.INFO}У вас есть 3 попытки{XSSColors.RESET}\n")

        attempts = 3
        while attempts > 0:
            injection = audio_system.get_input_with_sound(f"{XSSColors.PROMPT}SQL инъекция: {XSSColors.RESET}")

            if injection.strip() in correct_injections: # strip() для удаления лишних пробелов
                audio_system.play_sound("minigame_win")
                print(f"\n{XSSColors.SUCCESS}✅ УСПЕХ! Авторизация обойдена!{XSSColors.RESET}")
                print(
                    f"{XSSColors.INFO}Итоговый запрос: SELECT * FROM users WHERE username='admin' AND password='{injection}'{XSSColors.RESET}")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"{XSSColors.ERROR}Неверная инъекция! Осталось попыток: {attempts}{XSSColors.RESET}")
                else:
                    audio_system.play_sound("minigame_lose")
                    print(f"\n{XSSColors.ERROR}❌ Провал! Система заблокировала попытки входа{XSSColors.RESET}")
                    # Можно не показывать правильные, чтобы было сложнее
                    # print(f"{XSSColors.INFO}Правильные инъекции: {', '.join(correct_injections)}{XSSColors.RESET}")
                    return False

        return False

# --- НОВЫЕ МИНИ-ИГРЫ НАЧИНАЮТСЯ ЗДЕСЬ ---

class BruteForceGame(Minigame):
    """Улучшенная мини-игра "Атака перебором" - найди правильный порядок символов."""

    def __init__(self):
        super().__init__(
            "Атака перебором",
            "Найдите правильный порядок известных символов для взлома кода",
            "cracking"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")

        # Показываем крутой заголовок
        self._show_header()

        skill_level = game_state.get_skill(self.skill)

        # Улучшенная система сложности
        difficulty = self._calculate_difficulty(skill_level)
        code_length = difficulty['code_length']
        max_attempts = difficulty['max_attempts']
        time_pressure = difficulty['time_pressure']
        allow_repeats = difficulty['allow_repeats']

        # Генерируем целевой код
        target_code = self._generate_target_code(code_length, allow_repeats)

        # Получаем символы для показа (в перемешанном виде)
        available_symbols = self._get_shuffled_symbols(target_code, allow_repeats)

        # Показываем информацию о системе
        self._show_system_info(code_length, max_attempts, available_symbols, skill_level, time_pressure)

        attempts_made = 0
        start_time = time.time()
        best_match = 0  # Лучший результат (количество символов на правильных местах)

        while attempts_made < max_attempts:
            # Проверяем временное ограничение
            if time_pressure and (time.time() - start_time) > time_pressure:
                print(f"\n{XSSColors.DANGER}⏰ ВРЕМЯ ВЫШЛО! Система активировала блокировку!{XSSColors.RESET}")
                audio_system.play_sound("minigame_lose")
                return False

            # Показываем статус попытки
            remaining_time = ""
            if time_pressure:
                elapsed = time.time() - start_time
                remaining = time_pressure - elapsed
                if remaining > 0:
                    time_color = XSSColors.SUCCESS if remaining > time_pressure * 0.5 else XSSColors.WARNING if remaining > time_pressure * 0.2 else XSSColors.ERROR
                    remaining_time = f" | {time_color}⏱️  {remaining:.1f}s{XSSColors.RESET}"

            # Напоминаем доступные символы
            symbols_hint = f"Символы: {XSSColors.WARNING}{''.join(available_symbols)}{XSSColors.RESET}"
            prompt = f"{XSSColors.PROMPT}[{attempts_made + 1}/{max_attempts}]{remaining_time}\n{symbols_hint}\nВведите код: {XSSColors.RESET}"

            guess = audio_system.get_input_with_sound(prompt).lower().strip()

            # Валидация ввода
            if not self._validate_input(guess, code_length, available_symbols, allow_repeats):
                continue

            attempts_made += 1

            # Проверяем успех
            if guess == target_code:
                success_time = time.time() - start_time
                self._show_success(target_code, attempts_made, max_attempts, success_time)
                return True

            # Анализируем попытку и даем обратную связь
            feedback_result = self._analyze_guess(guess, target_code)
            self._show_feedback(guess, target_code, feedback_result, attempts_made, max_attempts)

            # Обновляем лучший результат
            if feedback_result['exact_matches'] > best_match:
                best_match = feedback_result['exact_matches']
                if best_match > 0:
                    print(
                        f"{XSSColors.SUCCESS}🎯 Новый рекорд! {best_match} символов на правильных местах!{XSSColors.RESET}")

        # Поражение
        self._show_failure(target_code, attempts_made, best_match)
        return False

    def _show_header(self):
        """Показывает крутой заголовок игры"""
        print(f"\n{XSSColors.WARNING}╔══════════════════════════════════════════╗{XSSColors.RESET}")
        print(
            f"{XSSColors.WARNING}║     {XSSColors.DANGER}🔐 ДЕШИФРОВКА ПОСЛЕДОВАТЕЛЬНОСТИ 🔐{XSSColors.WARNING}  ║{XSSColors.RESET}")
        print(f"{XSSColors.WARNING}║            АТАКА ПЕРЕБОРОМ v2.0          ║{XSSColors.RESET}")
        print(f"{XSSColors.WARNING}╚══════════════════════════════════════════╝{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🎯 Задача: Расставить известные символы в правильном порядке{XSSColors.RESET}")

    def _calculate_difficulty(self, skill_level):
        """Рассчитывает сложность игры в зависимости от навыка"""
        difficulties = {
            # Новичок (0-2)
            'beginner': {
                'code_length': 3,
                'max_attempts': 8,
                'time_pressure': None,
                'allow_repeats': False  # Все символы уникальные
            },
            # Любитель (3-4)
            'amateur': {
                'code_length': 4,
                'max_attempts': 10,
                'time_pressure': None,
                'allow_repeats': False
            },
            # Продвинутый (5-6)
            'advanced': {
                'code_length': 4,
                'max_attempts': 8,
                'time_pressure': 45,  # 45 секунд
                'allow_repeats': True  # Могут повторяться символы
            },
            # Эксперт (7-8)
            'expert': {
                'code_length': 5,
                'max_attempts': 10,
                'time_pressure': 40,
                'allow_repeats': True
            },
            # Мастер (9-10)
            'master': {
                'code_length': 6,
                'max_attempts': 12,
                'time_pressure': 35,
                'allow_repeats': True
            }
        }

        if skill_level <= 2:
            return difficulties['beginner']
        elif skill_level <= 4:
            return difficulties['amateur']
        elif skill_level <= 6:
            return difficulties['advanced']
        elif skill_level <= 8:
            return difficulties['expert']
        else:
            return difficulties['master']

    def _generate_target_code(self, code_length, allow_repeats):
        """Генерирует целевой код"""
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"

        if allow_repeats:
            # Могут повторяться символы
            return ''.join(random.choice(chars) for _ in range(code_length))
        else:
            # Все символы уникальные
            selected_chars = random.sample(chars, code_length)
            return ''.join(selected_chars)

    def _get_shuffled_symbols(self, target_code, allow_repeats):
        """Возвращает символы кода в перемешанном виде"""
        if allow_repeats:
            # Если повторы разрешены, показываем только уникальные символы
            unique_symbols = list(set(target_code))
            random.shuffle(unique_symbols)
            return unique_symbols
        else:
            # Если повторов нет, просто перемешиваем все символы
            symbols = list(target_code)
            random.shuffle(symbols)
            return symbols

    def _show_system_info(self, code_length, max_attempts, available_symbols, skill_level, time_pressure):
        """Показывает информацию о системе"""
        # Определяем тип системы
        system_types = {
            3: "🏠 Домашний Wi-Fi роутер",
            4: "🏢 Корпоративная база данных",
            5: "🏛️ Банковская система",
            6: "🔐 Засекреченный сервер"
        }

        system_type = system_types.get(code_length, "🔒 Неизвестная система")

        print(f"\n{XSSColors.INFO}🎯 ЦЕЛЬ: {system_type}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}📏 Длина пароля: {XSSColors.WARNING}{code_length} символов{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🎲 Попыток: {XSSColors.WARNING}{max_attempts}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}💪 Ваш навык взлома: {XSSColors.SUCCESS}{skill_level}/10{XSSColors.RESET}")

        if time_pressure:
            print(f"{XSSColors.WARNING}⏰ Ограничение времени: {time_pressure} секунд{XSSColors.RESET}")

        # Показываем перехваченные символы
        symbols_display = ''.join(available_symbols)
        print(f"\n{XSSColors.SUCCESS}🔍 ПЕРЕХВАЧЕННЫЕ СИМВОЛЫ: {XSSColors.WARNING}{symbols_display}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}💡 Задача: Найти правильный порядок этих символов{XSSColors.RESET}")

        # Показываем легенду цветов
        print(f"\n{XSSColors.INFO}🎨 ОБРАТНАЯ СВЯЗЬ:{XSSColors.RESET}")
        print(f"   {XSSColors.SUCCESS}●{XSSColors.RESET} Символ на правильном месте")
        print(f"   {XSSColors.WARNING}●{XSSColors.RESET} Символ есть, но не на том месте")
        print(f"   {XSSColors.ERROR}●{XSSColors.RESET} Символа нет в этой позиции")
        print(f"\n{XSSColors.WARNING}🚨 Начинаем дешифровку...{XSSColors.RESET}\n")

    def _validate_input(self, guess, code_length, available_symbols, allow_repeats):
        """Проверяет корректность ввода"""
        if len(guess) != code_length:
            print(f"{XSSColors.ERROR}❌ Неверная длина! Требуется {code_length} символов{XSSColors.RESET}")
            return False

        # Проверяем, что используются только доступные символы
        for char in guess:
            if char not in available_symbols:
                print(f"{XSSColors.ERROR}❌ Символ '{char}' не найден в перехваченных данных!{XSSColors.RESET}")
                print(f"{XSSColors.INFO}Доступные символы: {''.join(available_symbols)}{XSSColors.RESET}")
                return False

        # Если повторы не разрешены, проверяем уникальность
        if not allow_repeats and len(set(guess)) != len(guess):
            print(f"{XSSColors.ERROR}❌ Все символы должны быть уникальными!{XSSColors.RESET}")
            return False

        return True

    def _analyze_guess(self, guess, target_code):
        """Анализирует попытку и возвращает детальную обратную связь"""
        feedback = []
        exact_matches = 0
        wrong_position = 0

        # Создаем копии для анализа
        target_chars = list(target_code)
        guess_chars = list(guess)

        # Сначала находим точные совпадения
        for i in range(len(guess)):
            if guess_chars[i] == target_chars[i]:
                feedback.append('exact')
                exact_matches += 1
            else:
                feedback.append('pending')

        # Затем ищем символы не на своих местах
        for i in range(len(guess)):
            if feedback[i] == 'pending':
                char = guess_chars[i]
                # Ищем этот символ в других позициях target_code
                found_elsewhere = False
                for j in range(len(target_chars)):
                    if j != i and target_chars[j] == char and feedback[j] != 'exact':
                        # Проверяем, что на позиции j в guess нет правильного символа
                        if j < len(guess_chars) and guess_chars[j] != target_chars[j]:
                            feedback[i] = 'wrong_position'
                            wrong_position += 1
                            found_elsewhere = True
                            break

                if not found_elsewhere:
                    feedback[i] = 'not_here'

        return {
            'feedback': feedback,
            'exact_matches': exact_matches,
            'wrong_position': wrong_position
        }

    def _show_feedback(self, guess, target_code, result, attempts_made, max_attempts):
        """Показывает обратную связь по попытке"""
        # Показываем попытку и целевые позиции
        print(f"Попытка:  {guess.upper()}")
        print("Позиции:  " + "".join([str(i + 1) for i in range(len(guess))]))

        # Формируем визуальную обратную связь
        feedback_display = ""
        position_hints = ""

        for i, (char, status) in enumerate(zip(guess, result['feedback'])):
            if status == 'exact':
                feedback_display += f"{XSSColors.SUCCESS}●{XSSColors.RESET}"
                position_hints += f"{XSSColors.SUCCESS}{i + 1}{XSSColors.RESET}"
            elif status == 'wrong_position':
                feedback_display += f"{XSSColors.WARNING}●{XSSColors.RESET}"
                position_hints += f"{XSSColors.WARNING}{i + 1}{XSSColors.RESET}"
            else:
                feedback_display += f"{XSSColors.ERROR}●{XSSColors.RESET}"
                position_hints += f"{XSSColors.ERROR}{i + 1}{XSSColors.RESET}"

        print(f"Результат: {feedback_display}")
        print(f"Подсказка: {position_hints}")

        # Показываем статистику
        exact = result['exact_matches']
        wrong_pos = result['wrong_position']

        stats_parts = []
        if exact > 0:
            stats_parts.append(f"{XSSColors.SUCCESS}{exact} на месте{XSSColors.RESET}")
        if wrong_pos > 0:
            stats_parts.append(f"{XSSColors.WARNING}{wrong_pos} не на месте{XSSColors.RESET}")

        if stats_parts:
            print(f"📊 {' | '.join(stats_parts)}")

        # Прогресс-бар
        remaining = max_attempts - attempts_made
        if remaining > 0:
            progress = "▓" * attempts_made + "░" * remaining
            color = XSSColors.SUCCESS if remaining > max_attempts * 0.5 else XSSColors.WARNING if remaining > max_attempts * 0.2 else XSSColors.ERROR
            print(f"Прогресс: {color}{progress}{XSSColors.RESET} ({remaining} попыток осталось)")

        # Стратегическая подсказка
        if exact > 0:
            print(f"{XSSColors.INFO}💡 Зафиксируйте позиции с зелеными символами!{XSSColors.RESET}")
        elif wrong_pos > 0:
            print(f"{XSSColors.INFO}💡 Переставьте желтые символы в другие позиции{XSSColors.RESET}")

        print()  # Пустая строка для читаемости

    def _show_success(self, target_code, attempts_made, max_attempts, time_taken):
        """Показывает экран успеха"""
        audio_system.play_sound("minigame_win")

        print(f"\n{XSSColors.SUCCESS}╔══════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}║            🎉 КОД ДЕШИФРОВАН! 🎉         ║{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}╚══════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🔓 Правильная последовательность: {target_code.upper()}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}📊 Попыток использовано: {attempts_made}/{max_attempts}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️  Время дешифровки: {time_taken:.1f} секунд{XSSColors.RESET}")

        # Оценка производительности
        efficiency = (max_attempts - attempts_made + 1) / max_attempts
        if efficiency > 0.8:
            rating = f"{XSSColors.SUCCESS}🌟 МАСТЕР КРИПТОАНАЛИЗА!{XSSColors.RESET}"
        elif efficiency > 0.6:
            rating = f"{XSSColors.WARNING}💪 ОТЛИЧНАЯ ЛОГИКА!{XSSColors.RESET}"
        elif efficiency > 0.3:
            rating = f"{XSSColors.INFO}👍 ХОРОШАЯ РАБОТА!{XSSColors.RESET}"
        else:
            rating = f"{XSSColors.WARNING}😅 МЕТОДОМ ПРОБ И ОШИБОК{XSSColors.RESET}"

        print(f"🏆 Оценка: {rating}")
        print(f"\n{XSSColors.SUCCESS}✅ Система взломана! Пароль успешно дешифрован.{XSSColors.RESET}")

    def _show_failure(self, target_code, attempts_made, best_match):
        """Показывает экран поражения"""
        audio_system.play_sound("minigame_lose")

        print(f"\n{XSSColors.ERROR}╔══════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}║         🚨 ДЕШИФРОВКА НЕУДАЧНА! 🚨        ║{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}╚══════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}❌ Система заблокировала дальнейшие попытки{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🔐 Правильная последовательность: {target_code.upper()}{XSSColors.RESET}")

        if best_match > 0:
            print(
                f"{XSSColors.WARNING}🎯 Ваш лучший результат: {best_match} символов на правильных местах{XSSColors.RESET}")

        print(f"{XSSColors.WARNING}💡 Совет: Анализируйте позиции зеленых символов более внимательно{XSSColors.RESET}")
        print(f"\n{XSSColors.INFO}🎯 Тренируйтесь больше для развития логического мышления!{XSSColors.RESET}")


class CipherDecryptionGame(Minigame):
    """Продвинутая мини-игра "Расшифровка шифра" с различными криптографическими алгоритмами"""

    def __init__(self):
        super().__init__(
            "Расшифровка шифра",
            "Взломайте зашифрованное сообщение используя криптоанализ",
            "cracking"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        self._show_crypto_lab_interface()

        skill_level = game_state.get_skill(self.skill)
        crypto_config = self._get_crypto_config(skill_level)

        # Генерируем криптографическую задачу
        cipher_challenge = self._generate_cipher_challenge(crypto_config)

        # Показываем задачу
        self._show_cipher_challenge(cipher_challenge)

        # Запускаем процесс взлома
        return self._run_cryptanalysis(cipher_challenge, crypto_config)

    def _show_crypto_lab_interface(self):
        """Показывает интерфейс криптографической лаборатории"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║              🔐 CRYPTANALYSIS LAB v4.1.2                     ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                  ВЗЛОМ ШИФРОВ И КОДОВ                        ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.INFO}🔬 Добро пожаловать в лабораторию криптоанализа!{XSSColors.RESET}")
        print(f"{XSSColors.WARNING}⚡ Цель: Расшифровать перехваченное сообщение{XSSColors.RESET}")

    def _get_crypto_config(self, skill_level):
        """Конфигурация сложности криптозадач"""
        configs = {
            'beginner': {
                'cipher_types': ['caesar', 'atbash', 'rot13'],
                'max_key_length': 5,
                'provide_hints': True,
                'time_limit': None,
                'frequency_analysis': True,
                'tools_available': ['frequency', 'brute_force', 'pattern'],
                'message_length': 'short'
            },
            'intermediate': {
                'cipher_types': ['caesar', 'vigenere', 'substitution', 'affine'],
                'max_key_length': 10,
                'provide_hints': True,
                'time_limit': 420,  # 7 минут
                'frequency_analysis': True,
                'tools_available': ['frequency', 'brute_force', 'pattern', 'kasiski'],
                'message_length': 'medium'
            },
            'advanced': {
                'cipher_types': ['vigenere', 'substitution', 'playfair', 'hill', 'rail_fence'],
                'max_key_length': 15,
                'provide_hints': False,
                'time_limit': 360,  # 6 минут
                'frequency_analysis': True,
                'tools_available': ['frequency', 'brute_force', 'pattern', 'kasiski', 'index_coincidence'],
                'message_length': 'long'
            },
            'expert': {
                'cipher_types': ['enigma_simple', 'one_time_pad_weak', 'book_cipher', 'four_square'],
                'max_key_length': 20,
                'provide_hints': False,
                'time_limit': 300,  # 5 минут
                'frequency_analysis': True,
                'tools_available': ['frequency', 'brute_force', 'pattern', 'kasiski', 'index_coincidence',
                                    'differential'],
                'message_length': 'very_long'
            }
        }

        if skill_level <= 2:
            return configs['beginner']
        elif skill_level <= 5:
            return configs['intermediate']
        elif skill_level <= 7:
            return configs['advanced']
        else:
            return configs['expert']

    def _generate_cipher_challenge(self, config):
        """Генерирует криптографическую задачу"""
        cipher_type = random.choice(config['cipher_types'])

        # Генерируем исходное сообщение
        plaintext = self._generate_message(config['message_length'])

        # Генерируем ключ и шифруем
        key, ciphertext = self._encrypt_message(plaintext, cipher_type, config['max_key_length'])

        challenge = {
            'cipher_type': cipher_type,
            'ciphertext': ciphertext,
            'plaintext': plaintext,  # Для проверки
            'key': key,
            'hint_cipher_type': config['provide_hints'],
            'message_length': len(plaintext),
            'context': self._generate_context(cipher_type)
        }

        return challenge

    def _generate_message(self, length_category):
        """Генерирует сообщение для шифрования"""
        messages = {
            'short': [
                "ATTACK AT DAWN",
                "MISSION ACCOMPLISHED",
                "RENDEZVOUS AT BRIDGE",
                "CODE RED ACTIVATED",
                "TARGET ACQUIRED"
            ],
            'medium': [
                "THE PACKAGE WILL BE DELIVERED TO THE SAFE HOUSE AT MIDNIGHT",
                "OPERATION BLACKBIRD IS COMPROMISED ABORT IMMEDIATELY",
                "MEET AT THE OLD WAREHOUSE ON FIFTH STREET TOMORROW",
                "ENEMY AGENTS HAVE INFILTRATED OUR COMMUNICATIONS",
                "SECRET DOCUMENTS HIDDEN IN LOCKER SEVEN TWO FOUR"
            ],
            'long': [
                "INTELLIGENCE REPORTS INDICATE THAT THE ENEMY HAS DEVELOPED A NEW ENCRYPTION SYSTEM THAT MAY COMPROMISE ALL OF OUR CURRENT OPERATIONS PROCEED WITH EXTREME CAUTION",
                "THE COORDINATES FOR THE DROP ZONE ARE THIRTY SEVEN DEGREES NORTH SEVENTY FOUR DEGREES WEST EXTRACTION WILL OCCUR AT ZERO TWO HUNDRED HOURS",
                "CLASSIFIED INFORMATION SUGGESTS THAT OUR SECURE COMMUNICATION CHANNELS HAVE BEEN INTERCEPTED BY HOSTILE FORCES RECOMMEND IMMEDIATE PROTOCOL CHANGE"
            ],
            'very_long': [
                "URGENT CIPHER TELEGRAM STOP ENEMY FORCES HAVE SURROUNDED THE CAPITAL STOP REINFORCEMENTS REQUESTED IMMEDIATELY STOP AMMUNITION RUNNING LOW STOP MORALE HOLDING STEADY STOP AWAIT FURTHER INSTRUCTIONS STOP LONG LIVE THE RESISTANCE STOP",
                "CONFIDENTIAL REPORT INDICATES THAT THE DOUBLE AGENT CODENAMED NIGHTHAWK HAS SUCCESSFULLY INFILTRATED THE ENEMY HEADQUARTERS AND OBTAINED CRITICAL INTELLIGENCE REGARDING THEIR FUTURE OPERATIONS INCLUDING TROOP MOVEMENTS AND SUPPLY ROUTES"
            ]
        }

        return random.choice(messages[length_category]).replace(" ", "").upper()

    def _encrypt_message(self, plaintext, cipher_type, max_key_length):
        """Шифрует сообщение выбранным алгоритмом"""
        if cipher_type == 'caesar':
            shift = random.randint(1, 25)
            ciphertext = self._caesar_encrypt(plaintext, shift)
            return str(shift), ciphertext

        elif cipher_type == 'atbash':
            ciphertext = self._atbash_encrypt(plaintext)
            return "ATBASH", ciphertext

        elif cipher_type == 'rot13':
            ciphertext = self._caesar_encrypt(plaintext, 13)
            return "13", ciphertext

        elif cipher_type == 'vigenere':
            key = self._generate_vigenere_key(min(max_key_length, 8))
            ciphertext = self._vigenere_encrypt(plaintext, key)
            return key, ciphertext

        elif cipher_type == 'substitution':
            key = self._generate_substitution_key()
            ciphertext = self._substitution_encrypt(plaintext, key)
            return key, ciphertext

        elif cipher_type == 'affine':
            a, b = self._generate_affine_key()
            ciphertext = self._affine_encrypt(plaintext, a, b)
            return f"{a},{b}", ciphertext

        elif cipher_type == 'playfair':
            key = self._generate_playfair_key()
            ciphertext = self._playfair_encrypt(plaintext, key)
            return key, ciphertext

        elif cipher_type == 'rail_fence':
            rails = random.randint(3, 6)
            ciphertext = self._rail_fence_encrypt(plaintext, rails)
            return str(rails), ciphertext

        elif cipher_type == 'enigma_simple':
            rotor_pos = random.randint(1, 26)
            ciphertext = self._simple_enigma_encrypt(plaintext, rotor_pos)
            return str(rotor_pos), ciphertext

        else:
            # Fallback to Caesar
            shift = random.randint(1, 25)
            ciphertext = self._caesar_encrypt(plaintext, shift)
            return str(shift), ciphertext

    def _show_cipher_challenge(self, challenge):
        """Показывает криптографическую задачу"""
        print(f"\n{XSSColors.WARNING}📡 ПЕРЕХВАЧЕННОЕ СООБЩЕНИЕ{XSSColors.RESET}")
        print(f"{XSSColors.LIGHT_GRAY}{challenge['context']}{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}🔒 ЗАШИФРОВАННЫЙ ТЕКСТ:{XSSColors.RESET}")
        # Показываем шифртекст группами по 5 символов для удобства
        ciphertext = challenge['ciphertext']
        formatted_cipher = ' '.join([ciphertext[i:i + 5] for i in range(0, len(ciphertext), 5)])
        print(f"{XSSColors.BG_DARK}{formatted_cipher}{XSSColors.RESET}")

        print(f"\n{XSSColors.INFO}📊 ХАРАКТЕРИСТИКИ:{XSSColors.RESET}")
        print(f"   Длина сообщения: {len(ciphertext)} символов")

        if challenge['hint_cipher_type']:
            print(
                f"   {XSSColors.SUCCESS}💡 Подсказка: Тип шифра - {self._get_cipher_display_name(challenge['cipher_type'])}{XSSColors.RESET}")
        else:
            print(f"   Тип шифра: {XSSColors.WARNING}НЕИЗВЕСТЕН{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🛠️ ДОСТУПНЫЕ ИНСТРУМЕНТЫ КРИПТОАНАЛИЗА:{XSSColors.RESET}")

    def _run_cryptanalysis(self, challenge, config):
        """Основной процесс криптоанализа"""
        analysis_data = {
            'tools_used': [],
            'attempts': [],
            'current_hypothesis': None,
            'confidence': 0,
            'frequency_data': None,
            'pattern_data': None
        }

        start_time = time.time()
        hints_used = 0
        max_attempts = 5

        # Показываем доступные инструменты
        for i, tool in enumerate(config['tools_available'], 1):
            tool_name = self._get_tool_display_name(tool)
            print(f"   {i}. {tool_name}")

        print(f"\n{XSSColors.INFO}📋 КОМАНДЫ КРИПТОАНАЛИЗА:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}use <tool>{XSSColors.RESET} - Использовать инструмент анализа")
        print(f"   {XSSColors.BRIGHT_GREEN}decrypt <key>{XSSColors.RESET} - Попытка расшифровки с ключом")
        print(f"   {XSSColors.BRIGHT_GREEN}brute <cipher_type>{XSSColors.RESET} - Атака грубой силы")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze{XSSColors.RESET} - Показать результаты анализа")
        print(f"   {XSSColors.BRIGHT_GREEN}hint{XSSColors.RESET} - Получить подсказку")
        print(f"   {XSSColors.BRIGHT_GREEN}submit <plaintext>{XSSColors.RESET} - Отправить расшифрованный текст")

        while len(analysis_data['attempts']) < max_attempts:
            # Проверяем временное ограничение
            elapsed = time.time() - start_time
            remaining = None

            if config['time_limit']:
                remaining = config['time_limit'] - elapsed
                if remaining <= 0:
                    print(f"\n{XSSColors.ERROR}⏰ ВРЕМЯ ВЗЛОМА ИСТЕКЛО!{XSSColors.RESET}")
                    return self._evaluate_cryptanalysis(analysis_data, challenge, elapsed, False)
                elif remaining <= 60:
                    print(f"{XSSColors.WARNING}⚠️ Осталось {remaining:.0f} секунд!{XSSColors.RESET}")

            # Показываем статус
            self._show_crypto_status(analysis_data, max_attempts, elapsed, remaining)

            # Получаем команду
            command = audio_system.get_input_with_sound(f"{XSSColors.PROMPT}[CryptoLab]> {XSSColors.RESET}").strip()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()

            if cmd == "use" and len(parts) > 1:
                tool = parts[1].lower()
                if tool in config['tools_available'] or tool.isdigit():
                    if tool.isdigit():
                        tool_index = int(tool) - 1
                        if 0 <= tool_index < len(config['tools_available']):
                            tool = config['tools_available'][tool_index]
                        else:
                            print(f"{XSSColors.ERROR}Неверный номер инструмента{XSSColors.RESET}")
                            continue
                    self._use_crypto_tool(tool, challenge, analysis_data)
                else:
                    print(f"{XSSColors.ERROR}Инструмент недоступен{XSSColors.RESET}")

            elif cmd == "decrypt" and len(parts) > 1:
                key = ' '.join(parts[1:]).upper()
                self._attempt_decryption(key, challenge, analysis_data)

            elif cmd == "brute" and len(parts) > 1:
                cipher_type = parts[1].lower()
                self._brute_force_attack(cipher_type, challenge, analysis_data)

            elif cmd == "analyze":
                self._show_analysis_results(analysis_data, challenge)

            elif cmd == "hint":
                if config['provide_hints'] and hints_used < 2:
                    self._give_crypto_hint(challenge, analysis_data, hints_used)
                    hints_used += 1
                else:
                    print(f"{XSSColors.WARNING}Подсказки недоступны или исчерпаны{XSSColors.RESET}")

            elif cmd == "submit" and len(parts) > 1:
                submitted_text = ' '.join(parts[1:]).upper().replace(" ", "")
                if submitted_text == challenge['plaintext']:
                    final_elapsed = time.time() - start_time
                    print(f"\n{XSSColors.SUCCESS}🎉 ШИФР ВЗЛОМАН!{XSSColors.RESET}")
                    return self._evaluate_cryptanalysis(analysis_data, challenge, final_elapsed, True)
                else:
                    analysis_data['attempts'].append(submitted_text)
                    print(
                        f"{XSSColors.ERROR}❌ Неверный текст! Попыток осталось: {max_attempts - len(analysis_data['attempts'])}{XSSColors.RESET}")

            elif cmd == "help":
                self._show_crypto_help()

            else:
                print(f"{XSSColors.ERROR}Неизвестная команда. Используйте 'help' для справки{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}❌ Исчерпаны все попытки расшифровки!{XSSColors.RESET}")
        final_elapsed = time.time() - start_time
        return self._evaluate_cryptanalysis(analysis_data, challenge, final_elapsed, False)

    def _use_crypto_tool(self, tool, challenge, analysis_data):
        """Использует инструмент криптоанализа"""
        if tool in analysis_data['tools_used']:
            print(f"{XSSColors.WARNING}Инструмент уже использован{XSSColors.RESET}")
            return

        analysis_data['tools_used'].append(tool)

        print(f"\n{XSSColors.INFO}🔧 Запуск {self._get_tool_display_name(tool)}...{XSSColors.RESET}")
        time.sleep(random.uniform(1, 2))

        if tool == 'frequency':
            self._frequency_analysis(challenge, analysis_data)
        elif tool == 'brute_force':
            self._show_brute_force_options(challenge, analysis_data)
        elif tool == 'pattern':
            self._pattern_analysis(challenge, analysis_data)
        elif tool == 'kasiski':
            self._kasiski_examination(challenge, analysis_data)
        elif tool == 'index_coincidence':
            self._index_of_coincidence(challenge, analysis_data)
        elif tool == 'differential':
            self._differential_analysis(challenge, analysis_data)

    def _frequency_analysis(self, challenge, analysis_data):
        """Частотный анализ шифртекста"""
        ciphertext = challenge['ciphertext']
        freq_data = {}

        for char in ciphertext:
            if char.isalpha():
                freq_data[char] = freq_data.get(char, 0) + 1

        # Сортируем по частоте
        sorted_freq = sorted(freq_data.items(), key=lambda x: x[1], reverse=True)

        print(f"{XSSColors.SUCCESS}✅ Частотный анализ завершен{XSSColors.RESET}")
        print(f"\n{XSSColors.WARNING}📊 ЧАСТОТА СИМВОЛОВ (топ-10):{XSSColors.RESET}")

        for i, (char, count) in enumerate(sorted_freq[:10]):
            percentage = (count / len(ciphertext)) * 100
            bar = "█" * int(percentage)
            print(f"   {char}: {count:2d} ({percentage:4.1f}%) {bar}")

        # Показываем стандартные частоты английского языка
        print(
            f"\n{XSSColors.INFO}💡 Стандартные частоты английского: E(12.7%), T(9.1%), A(8.2%), O(7.5%), I(7.0%), N(6.7%){XSSColors.RESET}")

        analysis_data['frequency_data'] = sorted_freq
        analysis_data['confidence'] += 25

    def _pattern_analysis(self, challenge, analysis_data):
        """Анализ паттернов в шифртексте"""
        ciphertext = challenge['ciphertext']

        # Ищем повторяющиеся подстроки
        patterns = {}
        for length in range(2, 6):  # Паттерны длиной 2-5 символов
            for i in range(len(ciphertext) - length + 1):
                pattern = ciphertext[i:i + length]
                if pattern in patterns:
                    patterns[pattern].append(i)
                else:
                    patterns[pattern] = [i]

        # Находим повторяющиеся паттерны
        repeated = {k: v for k, v in patterns.items() if len(v) > 1}

        print(f"{XSSColors.SUCCESS}✅ Анализ паттернов завершен{XSSColors.RESET}")

        if repeated:
            print(f"\n{XSSColors.WARNING}🔍 НАЙДЕННЫЕ ПОВТОРЫ:{XSSColors.RESET}")
            for pattern, positions in list(repeated.items())[:5]:
                distances = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
                print(f"   '{pattern}' на позициях {positions} (расстояния: {distances})")
        else:
            print(f"{XSSColors.INFO}Повторяющиеся паттерны не найдены{XSSColors.RESET}")

        analysis_data['pattern_data'] = repeated
        analysis_data['confidence'] += 20

    def _kasiski_examination(self, challenge, analysis_data):
        """Тест Касиски для определения длины ключа Виженера"""
        ciphertext = challenge['ciphertext']

        # Находим повторяющиеся триграммы
        trigrams = {}
        for i in range(len(ciphertext) - 2):
            trigram = ciphertext[i:i + 3]
            if trigram in trigrams:
                trigrams[trigram].append(i)
            else:
                trigrams[trigram] = [i]

        repeated_trigrams = {k: v for k, v in trigrams.items() if len(v) > 1}

        print(f"{XSSColors.SUCCESS}✅ Тест Касиски завершен{XSSColors.RESET}")

        if repeated_trigrams:
            # Вычисляем расстояния
            all_distances = []
            for trigram, positions in repeated_trigrams.items():
                distances = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
                all_distances.extend(distances)
                print(f"   Триграмма '{trigram}': расстояния {distances}")

            # Находим НОД расстояний
            if all_distances:
                from math import gcd
                from functools import reduce
                key_length = reduce(gcd, all_distances)
                print(f"\n{XSSColors.WARNING}💡 Предполагаемая длина ключа: {key_length}{XSSColors.RESET}")
                analysis_data['confidence'] += 35
        else:
            print(f"{XSSColors.INFO}Недостаточно повторяющихся триграмм для анализа{XSSColors.RESET}")

    def _index_of_coincidence(self, challenge, analysis_data):
        """Вычисление индекса совпадений"""
        ciphertext = challenge['ciphertext']

        # Подсчитываем частоты
        freq = {}
        for char in ciphertext:
            if char.isalpha():
                freq[char] = freq.get(char, 0) + 1

        n = len([c for c in ciphertext if c.isalpha()])

        # Вычисляем индекс совпадений
        ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1)) if n > 1 else 0

        print(f"{XSSColors.SUCCESS}✅ Индекс совпадений вычислен{XSSColors.RESET}")
        print(f"\n{XSSColors.WARNING}📊 Индекс совпадений: {ic:.4f}{XSSColors.RESET}")

        # Интерпретация
        if ic > 0.06:
            print(f"{XSSColors.INFO}💡 Возможно моноалфавитный шифр (Caesar, Substitution){XSSColors.RESET}")
        elif ic > 0.04:
            print(f"{XSSColors.INFO}💡 Возможно полиалфавитный шифр с коротким ключом{XSSColors.RESET}")
        else:
            print(f"{XSSColors.INFO}💡 Возможно полиалфавитный шифр с длинным ключом{XSSColors.RESET}")

        analysis_data['confidence'] += 30

    def _differential_analysis(self, challenge, analysis_data):
        """Дифференциальный анализ"""
        ciphertext = challenge['ciphertext']

        print(f"{XSSColors.SUCCESS}✅ Дифференциальный анализ завершен{XSSColors.RESET}")

        # Анализ биграмм
        bigrams = {}
        for i in range(len(ciphertext) - 1):
            bigram = ciphertext[i:i + 2]
            bigrams[bigram] = bigrams.get(bigram, 0) + 1

        most_common = sorted(bigrams.items(), key=lambda x: x[1], reverse=True)[:5]

        print(f"\n{XSSColors.WARNING}🔍 ЧАСТЫЕ БИГРАММЫ:{XSSColors.RESET}")
        for bigram, count in most_common:
            print(f"   '{bigram}': {count} раз")

        print(f"\n{XSSColors.INFO}💡 В английском частые биграммы: TH, HE, IN, ER, AN{XSSColors.RESET}")
        analysis_data['confidence'] += 25

    def _attempt_decryption(self, key, challenge, analysis_data):
        """Попытка расшифровки с заданным ключом"""
        cipher_type = challenge['cipher_type']
        ciphertext = challenge['ciphertext']

        try:
            if cipher_type == 'caesar' and key.isdigit():
                shift = int(key)
                result = self._caesar_decrypt(ciphertext, shift)
            elif cipher_type == 'vigenere':
                result = self._vigenere_decrypt(ciphertext, key)
            elif cipher_type == 'affine' and ',' in key:
                a, b = map(int, key.split(','))
                result = self._affine_decrypt(ciphertext, a, b)
            else:
                print(f"{XSSColors.ERROR}Неподходящий ключ для данного типа шифра{XSSColors.RESET}")
                return

            print(f"\n{XSSColors.INFO}🔓 РЕЗУЛЬТАТ РАСШИФРОВКИ:{XSSColors.RESET}")
            formatted_result = ' '.join([result[i:i + 5] for i in range(0, len(result), 5)])
            print(f"{XSSColors.BRIGHT_GREEN}{formatted_result}{XSSColors.RESET}")

            # Проверяем правильность
            if result == challenge['plaintext']:
                print(f"{XSSColors.SUCCESS}✅ ПРАВИЛЬНО! Это и есть исходное сообщение!{XSSColors.RESET}")
                analysis_data['confidence'] = 100
            else:
                print(f"{XSSColors.WARNING}Возможно неполная расшифровка. Попробуйте другой ключ.{XSSColors.RESET}")

        except Exception as e:
            print(f"{XSSColors.ERROR}Ошибка при расшифровке: {e}{XSSColors.RESET}")

    def _brute_force_attack(self, cipher_type, challenge, analysis_data):
        """Атака грубой силы"""
        if cipher_type == 'caesar' or challenge['cipher_type'] == 'caesar':
            print(f"\n{XSSColors.INFO}🔨 Запуск атаки грубой силы для шифра Цезаря...{XSSColors.RESET}")

            for shift in range(1, 26):
                result = self._caesar_decrypt(challenge['ciphertext'], shift)
                print(f"   Сдвиг {shift:2d}: {result[:50]}...")

                if result == challenge['plaintext']:
                    print(f"{XSSColors.SUCCESS}✅ НАЙДЕН КЛЮЧ: {shift}!{XSSColors.RESET}")
                    break
        else:
            print(f"{XSSColors.WARNING}Атака грубой силы недоступна для данного типа шифра{XSSColors.RESET}")

    def _show_brute_force_options(self, challenge, analysis_data):
        """Показывает опции для атаки грубой силы"""
        print(f"{XSSColors.SUCCESS}✅ Модуль атаки грубой силы готов{XSSColors.RESET}")
        print(f"\n{XSSColors.WARNING}⚡ ДОСТУПНЫЕ АТАКИ:{XSSColors.RESET}")
        print(f"   • {XSSColors.BRIGHT_GREEN}brute caesar{XSSColors.RESET} - Перебор всех сдвигов Цезаря")
        print(f"   • {XSSColors.BRIGHT_GREEN}brute affine{XSSColors.RESET} - Перебор ключей аффинного шифра")
        print(f"   • {XSSColors.BRIGHT_GREEN}brute vigenere{XSSColors.RESET} - Перебор коротких ключей Виженера")

    def _give_crypto_hint(self, challenge, analysis_data, hint_number):
        """Дает подсказку для криптоанализа"""
        hints = [
            f"💡 Длина ключа: {len(str(challenge['key']))} символов",
            f"💡 Обратите внимание на частоту символов",
            f"💡 Ключ: {challenge['key'][:2]}..."  # Первые 2 символа ключа
        ]

        if hint_number < len(hints):
            print(f"\n{XSSColors.INFO}{hints[hint_number]}{XSSColors.RESET}")

    def _show_crypto_status(self, analysis_data, max_attempts, elapsed, remaining):
        """Показывает статус криптоанализа"""
        tools_used = len(analysis_data['tools_used'])
        attempts_left = max_attempts - len(analysis_data['attempts'])
        confidence = analysis_data['confidence']

        confidence_color = XSSColors.SUCCESS if confidence >= 80 else XSSColors.WARNING if confidence >= 50 else XSSColors.ERROR

        status = f"\n{XSSColors.INFO}📊 Статус: {tools_used} инструментов | "
        status += f"Попыток: {attempts_left} | "
        status += f"Уверенность: {confidence_color}{confidence}%{XSSColors.RESET}"

        if remaining:
            time_color = XSSColors.SUCCESS if remaining > 180 else XSSColors.WARNING if remaining > 60 else XSSColors.ERROR
            status += f" | ⏰ {time_color}{remaining:.0f}s{XSSColors.RESET}"
        else:
            status += f" | ⏱️ {elapsed:.0f}s"

        print(status)

    def _show_analysis_results(self, analysis_data, challenge):
        """Показывает результаты анализа"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ РЕЗУЛЬТАТЫ АНАЛИЗА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🔍 ИСПОЛЬЗОВАННЫЕ ИНСТРУМЕНТЫ:{XSSColors.RESET}")
        for tool in analysis_data['tools_used']:
            print(f"   ✓ {self._get_tool_display_name(tool)}")

        if analysis_data['frequency_data']:
            top_chars = analysis_data['frequency_data'][:3]
            print(
                f"\n{XSSColors.INFO}📊 Самые частые символы: {', '.join([f'{char}({count})' for char, count in top_chars])}{XSSColors.RESET}")

        if analysis_data['pattern_data']:
            patterns = list(analysis_data['pattern_data'].keys())[:3]
            print(f"🔍 Найденные паттерны: {', '.join(patterns)}")

        confidence = analysis_data['confidence']
        confidence_color = XSSColors.SUCCESS if confidence >= 80 else XSSColors.WARNING if confidence >= 50 else XSSColors.ERROR
        print(f"\n{XSSColors.INFO}📈 Общая уверенность: {confidence_color}{confidence}%{XSSColors.RESET}")

    def _evaluate_cryptanalysis(self, analysis_data, challenge, time_taken, success):
        """Оценивает результаты криптоанализа"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ РЕЗУЛЬТАТЫ ВЗЛОМА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Подсчет баллов
        tool_score = len(analysis_data['tools_used']) * 20
        success_score = 200 if success else 0
        confidence_score = analysis_data['confidence']
        time_bonus = max(0, 150 - int(time_taken / 2)) if success else 0
        attempts_penalty = len(analysis_data['attempts']) * 10

        total_score = tool_score + success_score + confidence_score + time_bonus - attempts_penalty

        print(f"\n{XSSColors.INFO}📊 ПОДСЧЕТ БАЛЛОВ:{XSSColors.RESET}")
        print(f"   Использование инструментов: +{tool_score}")
        if success_score > 0:
            print(f"   Успешная расшифровка: +{success_score}")
        print(f"   Уверенность анализа: +{confidence_score}")
        if time_bonus > 0:
            print(f"   Бонус за скорость: +{time_bonus}")
        if attempts_penalty > 0:
            print(f"   Штраф за неудачные попытки: -{attempts_penalty}")

        print(f"\n{XSSColors.BRIGHT_GREEN}🏆 ИТОГО: {total_score} баллов{XSSColors.RESET}")

        if success:
            self._show_crypto_success(challenge, analysis_data, total_score, time_taken)
        else:
            self._show_crypto_failure(challenge, analysis_data, total_score)

        return success

    def _show_crypto_success(self, challenge, analysis_data, score, time_taken):
        """Показывает экран успешного взлома"""
        audio_system.play_sound("minigame_win")

        print(f"\n{XSSColors.SUCCESS}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}║                🎉 ШИФР УСПЕШНО ВЗЛОМАН! 🎉                  ║{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🔓 Расшифрованное сообщение:{XSSColors.RESET}")
        formatted_plaintext = ' '.join(
            [challenge['plaintext'][i:i + 5] for i in range(0, len(challenge['plaintext']), 5)])
        print(f"{XSSColors.BRIGHT_GREEN}{formatted_plaintext}{XSSColors.RESET}")

        print(f"\n{XSSColors.INFO}🔑 Использованный ключ: {challenge['key']}{XSSColors.RESET}")
        print(
            f"{XSSColors.INFO}🏷️ Тип шифра: {self._get_cipher_display_name(challenge['cipher_type'])}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время взлома: {time_taken:.1f} секунд{XSSColors.RESET}")
        print(f"{XSSColors.BRIGHT_GREEN}🏆 Итоговый счет: {score} баллов{XSSColors.RESET}")

        # Определяем ранг криптоаналитика
        if score >= 500 and time_taken < 120:
            rank = f"{XSSColors.DANGER}🌟 ГРАНД-МАСТЕР КРИПТОГРАФИИ{XSSColors.RESET}"
        elif score >= 450:
            rank = f"{XSSColors.SUCCESS}💎 ЭКСПЕРТ ПО КРИПТОАНАЛИЗУ{XSSColors.RESET}"
        elif score >= 400:
            rank = f"{XSSColors.WARNING}🔧 SENIOR CRYPTANALYST{XSSColors.RESET}"
        elif score >= 350:
            rank = f"{XSSColors.INFO}🎯 CIPHER BREAKER{XSSColors.RESET}"
        else:
            rank = f"{XSSColors.LIGHT_GRAY}📚 JUNIOR ANALYST{XSSColors.RESET}"

        print(f"\n🏅 Ваш ранг: {rank}")

        # Показываем исторический контекст
        print(f"\n{XSSColors.STORY}📖 ИСТОРИЧЕСКАЯ СПРАВКА:{XSSColors.RESET}")
        historical_info = self._get_historical_info(challenge['cipher_type'])
        print(f"{XSSColors.LIGHT_GRAY}{historical_info}{XSSColors.RESET}")

        # Показываем развитые навыки
        print(f"\n{XSSColors.INFO}📈 РАЗВИТЫЕ НАВЫКИ:{XSSColors.RESET}")
        skills = [
            "Частотный анализ текстов",
            "Распознавание криптографических паттернов",
            "Методы атак грубой силы",
            "Статистический криптоанализ",
            "Исторические шифровальные системы"
        ]
        for skill in skills:
            print(f"   • {skill}")

    def _show_crypto_failure(self, challenge, analysis_data, score):
        """Показывает экран неудачного взлома"""
        audio_system.play_sound("minigame_lose")

        print(f"\n{XSSColors.ERROR}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}║                   ❌ ШИФР НЕ ВЗЛОМАН ❌                      ║{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🔒 Сообщение остается зашифрованным{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}📉 Итоговый счет: {score} баллов{XSSColors.RESET}")

        # Показываем правильное решение
        print(f"\n{XSSColors.INFO}💡 ПРАВИЛЬНОЕ РЕШЕНИЕ:{XSSColors.RESET}")
        print(
            f"   Тип шифра: {XSSColors.SUCCESS}{self._get_cipher_display_name(challenge['cipher_type'])}{XSSColors.RESET}")
        print(f"   Ключ: {challenge['key']}")

        formatted_plaintext = ' '.join(
            [challenge['plaintext'][i:i + 5] for i in range(0, len(challenge['plaintext']), 5)])
        print(f"   Исходное сообщение: {XSSColors.BRIGHT_GREEN}{formatted_plaintext}{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🎯 РЕКОМЕНДАЦИИ ДЛЯ УЛУЧШЕНИЯ:{XSSColors.RESET}")
        recommendations = [
            "Изучите частотный анализ букв",
            "Обращайте внимание на повторяющиеся паттерны",
            "Используйте тест Касиски для полиалфавитных шифров",
            "Попробуйте атаки грубой силы для простых шифров",
            "Анализируйте индекс совпадений"
        ]
        for rec in recommendations:
            print(f"   • {rec}")

    def _show_crypto_help(self):
        """Показывает справку по криптоанализу"""
        print(f"\n{XSSColors.INFO}📖 СПРАВКА ПО КРИПТОАНАЛИЗУ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}use <tool>{XSSColors.RESET} - Использовать инструмент анализа")
        print(f"   {XSSColors.BRIGHT_GREEN}decrypt <key>{XSSColors.RESET} - Попытка расшифровки с ключом")
        print(f"   {XSSColors.BRIGHT_GREEN}brute <cipher_type>{XSSColors.RESET} - Атака грубой силы")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze{XSSColors.RESET} - Показать результаты анализа")
        print(f"   {XSSColors.BRIGHT_GREEN}submit <plaintext>{XSSColors.RESET} - Отправить расшифрованный текст")
        print(f"   {XSSColors.BRIGHT_GREEN}hint{XSSColors.RESET} - Получить подсказку")

    # Методы шифрования и расшифровки

    def _caesar_encrypt(self, plaintext, shift):
        """Шифр Цезаря - шифрование"""
        result = ""
        for char in plaintext:
            if char.isalpha():
                shifted = ((ord(char) - ord('A') + shift) % 26) + ord('A')
                result += chr(shifted)
            else:
                result += char
        return result

    def _caesar_decrypt(self, ciphertext, shift):
        """Шифр Цезаря - расшифровка"""
        return self._caesar_encrypt(ciphertext, -shift)

    def _atbash_encrypt(self, plaintext):
        """Шифр Атбаш"""
        result = ""
        for char in plaintext:
            if char.isalpha():
                result += chr(ord('Z') - (ord(char) - ord('A')))
            else:
                result += char
        return result

    def _vigenere_encrypt(self, plaintext, key):
        """Шифр Виженера - шифрование"""
        result = ""
        key_index = 0
        for char in plaintext:
            if char.isalpha():
                key_char = key[key_index % len(key)]
                shift = ord(key_char) - ord('A')
                encrypted = ((ord(char) - ord('A') + shift) % 26) + ord('A')
                result += chr(encrypted)
                key_index += 1
            else:
                result += char
        return result

    def _vigenere_decrypt(self, ciphertext, key):
        """Шифр Виженера - расшифровка"""
        result = ""
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                key_char = key[key_index % len(key)]
                shift = ord(key_char) - ord('A')
                decrypted = ((ord(char) - ord('A') - shift) % 26) + ord('A')
                result += chr(decrypted)
                key_index += 1
            else:
                result += char
        return result

    def _substitution_encrypt(self, plaintext, key):
        """Простой подстановочный шифр"""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""
        for char in plaintext:
            if char in alphabet:
                index = alphabet.index(char)
                result += key[index]
            else:
                result += char
        return result

    def _affine_encrypt(self, plaintext, a, b):
        """Аффинный шифр - шифрование"""
        result = ""
        for char in plaintext:
            if char.isalpha():
                x = ord(char) - ord('A')
                encrypted = (a * x + b) % 26
                result += chr(encrypted + ord('A'))
            else:
                result += char
        return result

    def _affine_decrypt(self, ciphertext, a, b):
        """Аффинный шифр - расшифровка"""
        # Находим модульное обращение a
        a_inv = self._mod_inverse(a, 26)
        if a_inv is None:
            raise ValueError("Ключ 'a' не взаимно прост с 26")

        result = ""
        for char in ciphertext:
            if char.isalpha():
                y = ord(char) - ord('A')
                decrypted = (a_inv * (y - b)) % 26
                result += chr(decrypted + ord('A'))
            else:
                result += char
        return result

    def _playfair_encrypt(self, plaintext, key):
        """Упрощенная версия шифра Плейфера"""
        # Создаем матрицу 5x5
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J исключена
        key_clean = "".join(dict.fromkeys(key + alphabet))[:25]

        matrix = [list(key_clean[i:i + 5]) for i in range(0, 25, 5)]

        # Упрощенная реализация (только для демонстрации)
        result = ""
        for i in range(0, len(plaintext), 2):
            if i + 1 < len(plaintext):
                result += plaintext[i:i + 2]
            else:
                result += plaintext[i] + 'X'
        return result

    def _rail_fence_encrypt(self, plaintext, rails):
        """Шифр железнодорожной ограды"""
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1

        for char in plaintext:
            fence[rail].append(char)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction

        return ''.join([''.join(rail_chars) for rail_chars in fence])

    def _simple_enigma_encrypt(self, plaintext, rotor_pos):
        """Упрощенная имитация Энигмы"""
        rotor = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
        result = ""

        for i, char in enumerate(plaintext):
            if char.isalpha():
                pos = (ord(char) - ord('A') + rotor_pos + i) % 26
                result += rotor[pos]
            else:
                result += char
        return result

    # Вспомогательные методы

    def _generate_context(self, cipher_type):
        """Генерирует контекст для шифра"""
        contexts = {
            'caesar': "Обнаружена радиопередача времен Второй мировой войны:",
            'vigenere': "Перехвачена зашифрованная дипломатическая депеша:",
            'substitution': "Найден зашифрованный дневник агента:",
            'enigma_simple': "Декодирован фрагмент сообщения Энигмы:",
            'playfair': "Расшифрован военный приказ времен Первой мировой:",
            'atbash': "Обнаружен древний шифрованный текст:",
            'affine': "Перехвачено сообщение преступной группировки:",
            'rail_fence': "Найдена зашифрованная записка в тайнике:"
        }
        return contexts.get(cipher_type, "Обнаружено зашифрованное сообщение:")

    def _generate_vigenere_key(self, max_length):
        """Генерирует ключ для шифра Виженера"""
        length = random.randint(3, max_length)
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))

    def _generate_substitution_key(self):
        """Генерирует ключ для подстановочного шифра"""
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        key = alphabet.copy()
        random.shuffle(key)
        return ''.join(key)

    def _generate_affine_key(self):
        """Генерирует ключ для аффинного шифра"""
        # a должно быть взаимно простым с 26
        valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        a = random.choice(valid_a)
        b = random.randint(0, 25)
        return a, b

    def _generate_playfair_key(self):
        """Генерирует ключ для шифра Плейфера"""
        words = ["MONARCHY", "PLAYFAIR", "EXAMPLE", "SECRET"]
        return random.choice(words)

    def _mod_inverse(self, a, m):
        """Находит модульное обращение"""
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        return None

    def _get_cipher_display_name(self, cipher_type):
        """Возвращает отображаемое имя шифра"""
        names = {
            'caesar': 'Шифр Цезаря',
            'atbash': 'Шифр Атбаш',
            'rot13': 'ROT13',
            'vigenere': 'Шифр Виженера',
            'substitution': 'Подстановочный шифр',
            'affine': 'Аффинный шифр',
            'playfair': 'Шифр Плейфера',
            'hill': 'Шифр Хилла',
            'rail_fence': 'Железнодорожная ограда',
            'enigma_simple': 'Упрощенная Энигма',
            'one_time_pad_weak': 'Ослабленный одноразовый блокнот',
            'book_cipher': 'Книжный шифр',
            'four_square': 'Четырехквадратный шифр'
        }
        return names.get(cipher_type, cipher_type.title())

    def _get_tool_display_name(self, tool):
        """Возвращает отображаемое имя инструмента"""
        names = {
            'frequency': '📊 Частотный анализ',
            'brute_force': '🔨 Атака грубой силы',
            'pattern': '🔍 Анализ паттернов',
            'kasiski': '🔬 Тест Касиски',
            'index_coincidence': '📈 Индекс совпадений',
            'differential': '⚡ Дифференциальный анализ'
        }
        return names.get(tool, tool.title())

    def _get_historical_info(self, cipher_type):
        """Возвращает историческую информацию о шифре"""
        info = {
            'caesar': "Шифр Цезаря использовался Юлием Цезарем для защиты военной корреспонденции. Один из древнейших известных шифров.",
            'vigenere': "Шифр Виженера, изобретенный в XVI веке, считался 'неразгаданным шифром' до взлома Касиски в 1863 году.",
            'enigma_simple': "Энигма использовалась немецкими войсками во время Второй мировой войны. Ее взлом в Блетчли-Парк изменил ход войны.",
            'substitution': "Простые подстановочные шифры использовались еще в древности и легко взламываются частотным анализом.",
            'playfair': "Шифр Плейфера использовался британскими войсками в Первой мировой войне и считался практически неразгаданным."
        }
        return info.get(cipher_type, "Один из классических криптографических алгоритмов.")

class ReverseEngineeringGame(Minigame):
    """Мини-игра "Обратная разработка"."""
    def __init__(self):
        super().__init__(
            "Обратная разработка",
            "Определите последовательность операций для получения числа",
            "cracking"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ ОБРАТНАЯ РАЗРАБОТКА ━━━━━━━━━━{XSSColors.RESET}")
        skill_level = game_state.get_skill(self.skill)
        num_operations = min(3 + skill_level // 3, 6) # Количество операций

        start_value = random.randint(5, 20)
        target_value = start_value
        operations_sequence = []
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            #'/': lambda x, y: x // y if y != 0 else x # Деление может быть сложным для инвертирования
        }
        op_symbols = list(operations.keys())

        # Генерируем целевое значение и последовательность операций
        for _ in range(num_operations):
            op_symbol = random.choice(op_symbols)
            operand = random.randint(1, 5)
            operations_sequence.append((op_symbol, operand))
            target_value = operations[op_symbol](target_value, operand)

        print(f"{XSSColors.INFO}Начальное значение: {start_value}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Целевое значение: {target_value}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Доступные операции: {', '.join(op_symbols)}. Введите их в правильном порядке.{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Пример ввода: + 5 - 2 * 3 (пробел между оператором и операндом){XSSColors.RESET}\n")

        attempts = 2
        while attempts > 0:
            user_input = audio_system.get_input_with_sound(f"{XSSColors.PROMPT}Ваша последовательность ({num_operations} операций): {XSSColors.RESET}")
            parts = user_input.split()

            if len(parts) != num_operations * 2:
                print(f"{XSSColors.ERROR}Неверное количество аргументов. Ожидается {num_operations} операций и {num_operations} операндов.{XSSColors.RESET}")
                attempts -= 1
                continue

            current_value = start_value
            is_valid_input = True
            for i in range(0, len(parts), 2):
                op_symbol = parts[i]
                try:
                    operand = int(parts[i+1])
                except (ValueError, IndexError):
                    print(f"{XSSColors.ERROR}Неверный формат операнда '{parts[i+1]}'. Ожидается число.{XSSColors.RESET}")
                    is_valid_input = False
                    break

                if op_symbol not in operations:
                    print(f"{XSSColors.ERROR}Неизвестная операция '{op_symbol}'. Используйте {', '.join(op_symbols)}.{XSSColors.RESET}")
                    is_valid_input = False
                    break
                current_value = operations[op_symbol](current_value, operand)

            if not is_valid_input:
                attempts -= 1
                continue

            if current_value == target_value:
                audio_system.play_sound("minigame_win")
                print(f"\n{XSSColors.SUCCESS}🎉 УСПЕХ! Вы нашли правильную последовательность!{XSSColors.RESET}")
                return True
            else:
                attempts -= 1
                print(f"{XSSColors.WARNING}Неверная последовательность. Получено {current_value}, ожидалось {target_value}. Попыток осталось: {attempts}{XSSColors.RESET}")

        audio_system.play_sound("minigame_lose")
        print(f"\n{XSSColors.ERROR}❌ Провал! Правильная последовательность была: {' '.join([f'{op}{val}' for op, val in operations_sequence])} (без скобок){XSSColors.RESET}")
        return False


class PacketSniffingGame(Minigame):
    """Улучшенная мини-игра "Перехват пакетов" с реалистичным сетевым трафиком"""

    def __init__(self):
        super().__init__(
            "Перехват пакетов",
            "Анализируйте сетевой трафик и найдите подозрительные пакеты",
            "cracking"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        self._show_game_header()

        skill_level = game_state.get_skill(self.skill)
        difficulty_config = self._get_difficulty_config(skill_level)

        # Генерируем сетевую среду
        network_scenario = self._generate_network_scenario(difficulty_config)
        packets = self._generate_packet_stream(network_scenario, difficulty_config)

        # Показываем интерфейс анализатора
        self._show_packet_analyzer_interface(network_scenario)

        # Основной игровой процесс
        return self._run_packet_analysis(packets, network_scenario, difficulty_config)

    def _show_game_header(self):
        """Показывает заголовок игры в стиле сетевого анализатора"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║              🔍 WIRESHARK PACKET ANALYZER v2.5               ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                  СЕТЕВОЙ АНАЛИЗ ТРАФИКА                      ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

    def _get_difficulty_config(self, skill_level):
        """Настройки сложности в зависимости от навыка"""
        configs = {
            # Новичок (0-2)
            'beginner': {
                'total_packets': 12,
                'suspicious_count': 2,
                'time_limit': None,
                'show_hints': True,
                'network_complexity': 'simple',
                'packet_types': ['HTTP', 'DNS', 'SSH'],
                'analysis_depth': 'basic'
            },
            # Средний (3-5)
            'intermediate': {
                'total_packets': 18,
                'suspicious_count': 3,
                'time_limit': 300,
                'show_hints': True,
                'network_complexity': 'medium',
                'packet_types': ['HTTP', 'DNS', 'SSH', 'FTP', 'SMTP'],
                'analysis_depth': 'intermediate'
            },
            # Продвинутый (6-7)
            'advanced': {
                'total_packets': 25,
                'suspicious_count': 4,
                'time_limit': 240,
                'show_hints': False,
                'network_complexity': 'complex',
                'packet_types': ['HTTP', 'DNS', 'SSH', 'FTP', 'SMTP', 'HTTPS', 'IRC'],
                'analysis_depth': 'detailed'
            },
            # Эксперт (8-10)
            'expert': {
                'total_packets': 35,
                'suspicious_count': 6,
                'time_limit': 180,
                'show_hints': False,
                'network_complexity': 'enterprise',
                'packet_types': ['HTTP', 'DNS', 'SSH', 'FTP', 'SMTP', 'HTTPS', 'IRC', 'VPN', 'TOR'],
                'analysis_depth': 'forensic'
            }
        }

        if skill_level <= 2:
            return configs['beginner']
        elif skill_level <= 5:
            return configs['intermediate']
        elif skill_level <= 7:
            return configs['advanced']
        else:
            return configs['expert']

    def _generate_network_scenario(self, config):
        """Генерирует сценарий сетевой среды"""
        scenarios = {
            'simple': {
                'name': '🏠 Домашняя сеть',
                'description': 'Небольшая домашняя сеть с базовым трафиком',
                'target_keywords': ['password', 'login', 'admin'],
                'attack_types': ['password_theft', 'session_hijack']
            },
            'medium': {
                'name': '🏢 Корпоративная сеть',
                'description': 'Офисная сеть с различными сервисами',
                'target_keywords': ['confidential', 'transfer', 'database', 'credentials'],
                'attack_types': ['data_exfiltration', 'lateral_movement', 'privilege_escalation']
            },
            'complex': {
                'name': '🏛️ Банковская сеть',
                'description': 'Высокозащищенная финансовая инфраструктура',
                'target_keywords': ['transaction', 'account', 'swift', 'vault'],
                'attack_types': ['apt_attack', 'zero_day', 'insider_threat']
            },
            'enterprise': {
                'name': '🔐 Государственная сеть',
                'description': 'Критически важная правительственная инфраструктура',
                'target_keywords': ['classified', 'operation', 'intelligence', 'secure'],
                'attack_types': ['nation_state', 'advanced_persistent', 'cyber_warfare']
            }
        }

        return scenarios[config['network_complexity']]

    def _generate_packet_stream(self, scenario, config):
        """Генерирует поток сетевых пакетов"""
        packets = []
        suspicious_packets = []

        # IP адреса для сети
        internal_ips = [f"192.168.1.{i}" for i in range(10, 50)]
        external_ips = [
            f"{random.randint(1, 223)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}" for _
            in range(10)]

        # Генерируем подозрительные пакеты
        for i in range(config['suspicious_count']):
            suspicious_packet = self._create_suspicious_packet(scenario, config, internal_ips, external_ips, i)
            suspicious_packets.append(suspicious_packet)
            packets.append(suspicious_packet)

        # Генерируем обычные пакеты
        normal_count = config['total_packets'] - config['suspicious_count']
        for i in range(normal_count):
            normal_packet = self._create_normal_packet(config, internal_ips, external_ips, i)
            packets.append(normal_packet)

        # Перемешиваем пакеты
        random.shuffle(packets)

        # Добавляем номера пакетов
        for i, packet in enumerate(packets, 1):
            packet['packet_id'] = i

        return packets, suspicious_packets

    def _create_suspicious_packet(self, scenario, config, internal_ips, external_ips, index):
        """Создает подозрительный пакет"""
        attack_types = scenario['attack_types']
        attack_type = random.choice(attack_types)

        suspicious_patterns = {
            'password_theft': {
                'protocol': 'HTTP',
                'payload': f"POST /login.php user=admin&password={random.choice(['123456', 'password', 'admin123'])}",
                'flags': ['Unencrypted', 'Credentials'],
                'threat_level': 'Medium'
            },
            'session_hijack': {
                'protocol': 'HTTP',
                'payload': f"GET /admin/panel Cookie: SESSID={self._generate_session_id()}",
                'flags': ['Session Token', 'Privilege'],
                'threat_level': 'High'
            },
            'data_exfiltration': {
                'protocol': 'HTTPS',
                'payload': f"POST /upload.php Content-Length: 1048576 [ENCRYPTED: {random.choice(scenario['target_keywords'])}]",
                'flags': ['Large Upload', 'Encrypted'],
                'threat_level': 'Critical'
            },
            'lateral_movement': {
                'protocol': 'SSH',
                'payload': f"ssh root@{random.choice(internal_ips)} -i ~/.ssh/stolen_key",
                'flags': ['Internal Access', 'Key Auth'],
                'threat_level': 'High'
            },
            'privilege_escalation': {
                'protocol': 'TCP',
                'payload': f"exploit/linux/local/cve-2023-{random.randint(1000, 9999)}",
                'flags': ['Exploit', 'Root Access'],
                'threat_level': 'Critical'
            },
            'apt_attack': {
                'protocol': 'DNS',
                'payload': f"Query: {random.choice(['c2server', 'malware', 'backdoor'])}.{self._generate_domain()}",
                'flags': ['C2 Communication', 'APT'],
                'threat_level': 'Critical'
            },
            'zero_day': {
                'protocol': 'HTTP',
                'payload': f"GET /api/v1/exploit?payload=0x{self._generate_hex_payload()}",
                'flags': ['Unknown Exploit', '0-day'],
                'threat_level': 'Critical'
            },
            'insider_threat': {
                'protocol': 'FTP',
                'payload': f"RETR /confidential/{random.choice(scenario['target_keywords'])}_docs.zip",
                'flags': ['Internal User', 'Sensitive Data'],
                'threat_level': 'High'
            },
            'nation_state': {
                'protocol': 'TOR',
                'payload': f"CONNECT {self._generate_onion_address()} via relay_chain",
                'flags': ['Anonymous', 'State Actor'],
                'threat_level': 'Critical'
            },
            'advanced_persistent': {
                'protocol': 'HTTPS',
                'payload': f"Beacon: {self._generate_beacon_data()}",
                'flags': ['Persistent', 'Command Control'],
                'threat_level': 'Critical'
            },
            'cyber_warfare': {
                'protocol': 'SCADA',
                'payload': f"WRITE_COIL device_id=PLC_{random.randint(100, 999)} value=OVERRIDE",
                'flags': ['Industrial Control', 'Sabotage'],
                'threat_level': 'Critical'
            }
        }

        pattern = suspicious_patterns.get(attack_type, suspicious_patterns['password_theft'])

        return {
            'protocol': pattern['protocol'],
            'src_ip': random.choice(external_ips if attack_type in ['apt_attack', 'nation_state'] else internal_ips),
            'dst_ip': random.choice(internal_ips),
            'src_port': random.randint(1024, 65535),
            'dst_port': self._get_protocol_port(pattern['protocol']),
            'payload': pattern['payload'],
            'timestamp': self._generate_timestamp(),
            'size': random.randint(512, 8192),
            'flags': pattern['flags'],
            'threat_level': pattern['threat_level'],
            'is_suspicious': True,
            'attack_type': attack_type
        }

    def _create_normal_packet(self, config, internal_ips, external_ips, index):
        """Создает обычный пакет"""
        protocol = random.choice(config['packet_types'])

        normal_payloads = {
            'HTTP': [
                "GET /index.html HTTP/1.1 Host: example.com",
                "POST /contact.php form_data=user_message",
                "GET /images/logo.png HTTP/1.1",
                "GET /css/style.css HTTP/1.1"
            ],
            'DNS': [
                "Query: www.google.com A record",
                "Query: api.github.com AAAA record",
                "Query: cdn.jsdelivr.net CNAME record",
                "Query: mx.example.com MX record"
            ],
            'SSH': [
                "SSH-2.0-OpenSSH_8.0 Protocol negotiation",
                "Key exchange: diffie-hellman-group14-sha256",
                "User authentication: publickey",
                "Channel open: session"
            ],
            'FTP': [
                "USER anonymous",
                "RETR /pub/software/package.tar.gz",
                "LIST /home/user/documents",
                "STOR backup_file.zip"
            ],
            'SMTP': [
                "MAIL FROM: user@example.com",
                "RCPT TO: admin@company.com",
                "DATA: Subject: Monthly report",
                "QUIT"
            ],
            'HTTPS': [
                "TLS 1.3 Handshake: ClientHello",
                "Application Data [encrypted]",
                "TLS Alert: close_notify",
                "Certificate Verify"
            ]
        }

        payload = random.choice(normal_payloads.get(protocol, normal_payloads['HTTP']))

        return {
            'protocol': protocol,
            'src_ip': random.choice(internal_ips + external_ips),
            'dst_ip': random.choice(internal_ips + external_ips),
            'src_port': random.randint(1024, 65535),
            'dst_port': self._get_protocol_port(protocol),
            'payload': payload,
            'timestamp': self._generate_timestamp(),
            'size': random.randint(64, 1500),
            'flags': ['Normal'],
            'threat_level': 'None',
            'is_suspicious': False,
            'attack_type': None
        }

    def _show_packet_analyzer_interface(self, scenario):
        """Показывает интерфейс анализатора пакетов"""
        print(f"\n{XSSColors.INFO}🌐 Анализируемая сеть: {scenario['name']}{XSSColors.RESET}")
        print(f"{XSSColors.LIGHT_GRAY}{scenario['description']}{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🎯 ЗАДАЧА АНАЛИЗА:{XSSColors.RESET}")
        print(f"   • Найти все подозрительные пакеты в трафике")
        print(f"   • Определить тип атаки или угрозы")
        print(f"   • Проанализировать источник и назначение")

        print(f"\n{XSSColors.SUCCESS}🔍 ИНДИКАТОРЫ ПОДОЗРИТЕЛЬНОСТИ:{XSSColors.RESET}")
        print(f"   {XSSColors.ERROR}• Высокий:{XSSColors.RESET} Незашифрованные пароли, эксплойты")
        print(f"   {XSSColors.WARNING}• Средний:{XSSColors.RESET} Необычные порты, большой трафик")
        print(f"   {XSSColors.INFO}• Низкий:{XSSColors.RESET} Подозрительные домены, редкие протоколы")

        print(f"\n{XSSColors.INFO}📋 КОМАНДЫ АНАЛИЗА:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze <packet_id>{XSSColors.RESET} - Детальный анализ пакета")
        print(f"   {XSSColors.BRIGHT_GREEN}filter <protocol>{XSSColors.RESET} - Фильтр по протоколу")
        print(f"   {XSSColors.BRIGHT_GREEN}suspicious <ids>{XSSColors.RESET} - Отметить подозрительные (через пробел)")
        print(f"   {XSSColors.BRIGHT_GREEN}hint{XSSColors.RESET} - Получить подсказку (если доступно)")
        print(f"   {XSSColors.BRIGHT_GREEN}submit{XSSColors.RESET} - Завершить анализ")

    def _run_packet_analysis(self, packets_data, scenario, config):
        """Основной процесс анализа пакетов"""
        packets, suspicious_packets = packets_data
        found_suspicious = []
        analysis_history = []
        hints_used = 0
        max_hints = 2 if config['show_hints'] else 0

        start_time = time.time()
        time_limit = config['time_limit']

        # Показываем начальный список пакетов
        self._display_packet_list(packets, show_details=False)

        while True:
            # Инициализируем переменные времени
            elapsed = time.time() - start_time
            remaining = None

            # Проверяем временное ограничение
            if time_limit:
                remaining = time_limit - elapsed
                if remaining <= 0:
                    print(f"\n{XSSColors.ERROR}⏰ ВРЕМЯ ВЫШЛО! Анализ прерван системой безопасности.{XSSColors.RESET}")
                    return False
                elif remaining <= 10:
                    print(f"{XSSColors.ERROR}⚠️ Осталось {remaining:.0f} секунд!{XSSColors.RESET}")

            # Показываем статус
            self._show_analysis_status(found_suspicious, len(suspicious_packets), elapsed, remaining)

            # Получаем команду от пользователя
            command = audio_system.get_input_with_sound(
                f"{XSSColors.PROMPT}[Packet Analyzer]> {XSSColors.RESET}").strip().lower()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0]

            if cmd == "analyze" and len(parts) > 1:
                try:
                    packet_id = int(parts[1])
                    if 1 <= packet_id <= len(packets):
                        packet = packets[packet_id - 1]
                        self._show_detailed_analysis(packet, analysis_history)
                        analysis_history.append(packet_id)
                    else:
                        print(f"{XSSColors.ERROR}Неверный ID пакета{XSSColors.RESET}")
                except ValueError:
                    print(f"{XSSColors.ERROR}ID должен быть числом{XSSColors.RESET}")

            elif cmd == "filter" and len(parts) > 1:
                protocol = parts[1].upper()
                self._show_filtered_packets(packets, protocol)

            elif cmd == "suspicious" and len(parts) > 1:
                try:
                    new_suspicious = [int(x) for x in parts[1:]]
                    if all(1 <= x <= len(packets) for x in new_suspicious):
                        found_suspicious = new_suspicious
                        print(
                            f"{XSSColors.SUCCESS}Отмечено {len(found_suspicious)} подозрительных пакетов{XSSColors.RESET}")
                    else:
                        print(f"{XSSColors.ERROR}Некоторые ID пакетов неверны{XSSColors.RESET}")
                except ValueError:
                    print(f"{XSSColors.ERROR}Все ID должны быть числами{XSSColors.RESET}")

            elif cmd == "hint":
                if hints_used < max_hints:
                    self._give_hint(packets, suspicious_packets, hints_used)
                    hints_used += 1
                else:
                    print(f"{XSSColors.WARNING}Подсказки исчерпаны или недоступны на этом уровне{XSSColors.RESET}")

            elif cmd == "submit":
                final_elapsed = time.time() - start_time
                return self._evaluate_analysis(found_suspicious, suspicious_packets, analysis_history, final_elapsed)

            elif cmd == "list":
                self._display_packet_list(packets, show_details=False)

            elif cmd == "help":
                self._show_analysis_help()

            else:
                print(f"{XSSColors.ERROR}Неизвестная команда. Используйте 'help' для справки{XSSColors.RESET}")

    def _display_packet_list(self, packets, show_details=False):
        """Отображает список пакетов"""
        print(f"\n{XSSColors.INFO}📦 ЗАХВАЧЕННЫЕ ПАКЕТЫ ({len(packets)} total):{XSSColors.RESET}")
        print(
            f"{XSSColors.DARK_GRAY}{'ID':<3} {'Protocol':<8} {'Source':<15} {'Destination':<15} {'Size':<6} {'Time':<8}{XSSColors.RESET}")
        print(f"{XSSColors.DARK_GRAY}{'-' * 70}{XSSColors.RESET}")

        for packet in packets:
            protocol_color = self._get_protocol_color(packet['protocol'])
            size_color = XSSColors.WARNING if packet['size'] > 2000 else XSSColors.RESET

            print(f"{packet['packet_id']:<3} {protocol_color}{packet['protocol']:<8}{XSSColors.RESET} "
                  f"{packet['src_ip']:<15} {packet['dst_ip']:<15} "
                  f"{size_color}{packet['size']:<6}{XSSColors.RESET} {packet['timestamp']}")

    def _show_detailed_analysis(self, packet, history):
        """Показывает детальный анализ пакета"""
        print(
            f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ АНАЛИЗ ПАКЕТА #{packet['packet_id']} ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Базовая информация
        protocol_color = self._get_protocol_color(packet['protocol'])
        print(f"\n{XSSColors.INFO}📋 ОСНОВНАЯ ИНФОРМАЦИЯ:{XSSColors.RESET}")
        print(f"   Протокол: {protocol_color}{packet['protocol']}{XSSColors.RESET}")
        print(f"   Источник: {packet['src_ip']}:{packet['src_port']}")
        print(f"   Назначение: {packet['dst_ip']}:{packet['dst_port']}")
        print(f"   Размер: {packet['size']} байт")
        print(f"   Время: {packet['timestamp']}")

        # Анализ полезной нагрузки
        print(f"\n{XSSColors.WARNING}📄 ПОЛЕЗНАЯ НАГРУЗКА:{XSSColors.RESET}")
        print(f"   {XSSColors.LIGHT_GRAY}{packet['payload']}{XSSColors.RESET}")

        # Флаги безопасности
        print(f"\n{XSSColors.INFO}🚩 ФЛАГИ АНАЛИЗА:{XSSColors.RESET}")
        for flag in packet['flags']:
            flag_color = self._get_flag_color(flag)
            print(f"   {flag_color}• {flag}{XSSColors.RESET}")

        # Уровень угрозы
        threat_color = self._get_threat_color(packet['threat_level'])
        print(f"\n{XSSColors.INFO}⚠️ УРОВЕНЬ УГРОЗЫ: {threat_color}{packet['threat_level']}{XSSColors.RESET}")

        # Дополнительный анализ для подозрительных пакетов
        if packet.get('is_suspicious'):
            print(f"\n{XSSColors.ERROR}🔍 ОБНАРУЖЕННЫЕ ИНДИКАТОРЫ КОМПРОМЕТАЦИИ:{XSSColors.RESET}")
            self._show_ioc_analysis(packet)

        # Рекомендации
        print(f"\n{XSSColors.SUCCESS}💡 РЕКОМЕНДАЦИИ АНАЛИТИКА:{XSSColors.RESET}")
        self._show_packet_recommendations(packet)

    def _show_ioc_analysis(self, packet):
        """Показывает анализ индикаторов компрометации"""
        ioc_patterns = {
            'password_theft': [
                "Незашифрованная передача учетных данных",
                "Использование слабых паролей",
                "Отсутствие HTTPS для аутентификации"
            ],
            'session_hijack': [
                "Подозрительное использование сессионных токенов",
                "Доступ к привилегированным разделам",
                "Аномальная активность сессии"
            ],
            'data_exfiltration': [
                "Большой объем исходящих данных",
                "Шифрование при передаче конфиденциальных данных",
                "Подключение к внешним серверам"
            ],
            'apt_attack': [
                "Соединение с известными C&C серверами",
                "Использование продвинутых техник сокрытия",
                "Долгосрочное присутствие в сети"
            ]
        }

        attack_type = packet.get('attack_type', 'unknown')
        indicators = ioc_patterns.get(attack_type, ["Неизвестные индикаторы компрометации"])

        for indicator in indicators:
            print(f"   {XSSColors.ERROR}⚡ {indicator}{XSSColors.RESET}")

    def _show_packet_recommendations(self, packet):
        """Показывает рекомендации по пакету"""
        if packet.get('is_suspicious'):
            recommendations = [
                "Заблокировать IP-адрес источника",
                "Проверить системы на наличие компрометации",
                "Усилить мониторинг сетевого трафика",
                "Обновить правила IDS/IPS"
            ]
        else:
            recommendations = [
                "Пакет соответствует нормальной активности",
                "Дополнительных действий не требуется",
                "Продолжить мониторинг"
            ]

        for rec in recommendations:
            print(f"   {XSSColors.SUCCESS}✓ {rec}{XSSColors.RESET}")

    def _show_filtered_packets(self, packets, protocol):
        """Показывает отфильтрованные пакеты"""
        filtered = [p for p in packets if p['protocol'] == protocol]

        if not filtered:
            print(f"{XSSColors.WARNING}Пакеты с протоколом {protocol} не найдены{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.INFO}🔍 ФИЛЬТР: {protocol} ({len(filtered)} пакетов){XSSColors.RESET}")
        for packet in filtered:
            status = "🚨" if packet.get('is_suspicious') else "✅"
            print(
                f"   {status} #{packet['packet_id']}: {packet['src_ip']} → {packet['dst_ip']} ({packet['size']} bytes)")

    def _give_hint(self, packets, suspicious_packets, hint_number):
        """Дает подсказку игроку"""
        if hint_number == 0:
            # Первая подсказка - о количестве
            print(
                f"\n{XSSColors.INFO}💡 ПОДСКАЗКА 1: В трафике содержится {len(suspicious_packets)} подозрительных пакетов{XSSColors.RESET}")
        elif hint_number == 1:
            # Вторая подсказка - о протоколах
            suspicious_protocols = set(p['protocol'] for p in suspicious_packets)
            print(
                f"\n{XSSColors.INFO}💡 ПОДСКАЗКА 2: Подозрительные протоколы: {', '.join(suspicious_protocols)}{XSSColors.RESET}")

    def _show_analysis_status(self, found, total_suspicious, elapsed, remaining):
        """Показывает статус анализа"""
        progress = f"{len(found)}/{total_suspicious}"
        progress_color = XSSColors.SUCCESS if len(found) == total_suspicious else XSSColors.WARNING

        status_line = f"\n{XSSColors.INFO}📊 Прогресс: {progress_color}{progress}{XSSColors.RESET} подозрительных пакетов найдено"

        if remaining:
            time_color = XSSColors.SUCCESS if remaining > 20 else XSSColors.WARNING if remaining > 10 else XSSColors.ERROR
            status_line += f" | ⏰ {time_color}{remaining:.0f}s{XSSColors.RESET} осталось"
        elif elapsed:
            status_line += f" | ⏱️ {elapsed:.0f}s прошло"

        print(status_line)

    def _evaluate_analysis(self, found_suspicious, actual_suspicious, analysis_history, time_taken):
        """Оценивает результаты анализа"""
        actual_ids = [p['packet_id'] for p in actual_suspicious]

        # Находим правильные и неправильные результаты
        correct_found = set(found_suspicious) & set(actual_ids)
        false_positives = set(found_suspicious) - set(actual_ids)
        missed = set(actual_ids) - set(found_suspicious)

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ РЕЗУЛЬТАТЫ АНАЛИЗА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Подсчет очков
        correct_score = len(correct_found) * 100
        false_positive_penalty = len(false_positives) * 30
        missed_penalty = len(missed) * 50
        time_bonus = max(0, 50 - int(time_taken))

        total_score = correct_score - false_positive_penalty - missed_penalty + time_bonus

        # Показываем результаты
        print(f"\n{XSSColors.SUCCESS}✅ ПРАВИЛЬНО НАЙДЕНО: {len(correct_found)}/{len(actual_ids)}{XSSColors.RESET}")
        for packet_id in correct_found:
            packet = next(p for p in actual_suspicious if p['packet_id'] == packet_id)
            print(f"   #{packet_id}: {packet['attack_type']} ({packet['threat_level']})")

        if false_positives:
            print(f"\n{XSSColors.WARNING}⚠️ ЛОЖНЫЕ СРАБАТЫВАНИЯ: {len(false_positives)}{XSSColors.RESET}")
            for packet_id in false_positives:
                print(f"   #{packet_id}: Обычный трафик")

        if missed:
            print(f"\n{XSSColors.ERROR}❌ ПРОПУЩЕНО: {len(missed)}{XSSColors.RESET}")
            for packet_id in missed:
                packet = next(p for p in actual_suspicious if p['packet_id'] == packet_id)
                print(f"   #{packet_id}: {packet['attack_type']} ({packet['threat_level']})")

        # Подсчет итогового балла
        print(f"\n{XSSColors.INFO}📊 ПОДСЧЕТ ОЧКОВ:{XSSColors.RESET}")
        print(f"   Правильные находки: +{correct_score}")
        if false_positive_penalty > 0:
            print(f"   Ложные срабатывания: -{false_positive_penalty}")
        if missed_penalty > 0:
            print(f"   Пропущенные угрозы: -{missed_penalty}")
        if time_bonus > 0:
            print(f"   Бонус за скорость: +{time_bonus}")

        print(f"   {XSSColors.BRIGHT_GREEN}ИТОГО: {total_score} очков{XSSColors.RESET}")

        # Определяем успех
        success_threshold = 70  # Минимум 70% для успеха
        accuracy = (len(correct_found) / len(actual_ids)) * 100 if actual_ids else 0

        if accuracy >= success_threshold and len(false_positives) <= 1:
            self._show_success_analysis(accuracy, time_taken, total_score)
            return True
        else:
            self._show_failure_analysis(accuracy, time_taken, total_score, missed, false_positives)
            return False

    def _show_success_analysis(self, accuracy, time_taken, score):
        """Показывает экран успешного анализа"""
        audio_system.play_sound("minigame_win")

        print(f"\n{XSSColors.SUCCESS}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}║                  🎉 АНАЛИЗ ЗАВЕРШЕН УСПЕШНО! 🎉              ║{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🔍 Точность анализа: {accuracy:.1f}%{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время анализа: {time_taken:.1f} секунд{XSSColors.RESET}")
        print(f"{XSSColors.BRIGHT_GREEN}🏆 Итоговый счет: {score} очков{XSSColors.RESET}")

        # Определяем ранг аналитика
        if accuracy >= 95 and time_taken < 20:
            rank = f"{XSSColors.DANGER}🌟 КИБЕР-ДЕТЕКТИВ{XSSColors.RESET}"
        elif accuracy >= 85:
            rank = f"{XSSColors.SUCCESS}💎 ЭКСПЕРТ ПО БЕЗОПАСНОСТИ{XSSColors.RESET}"
        elif accuracy >= 75:
            rank = f"{XSSColors.WARNING}🔧 СЕТЕВОЙ АНАЛИТИК{XSSColors.RESET}"
        else:
            rank = f"{XSSColors.INFO}🎯 СПЕЦИАЛИСТ SOC{XSSColors.RESET}"

        print(f"\n🏅 Ваш ранг: {rank}")

        # Показываем полученные навыки
        print(f"\n{XSSColors.INFO}📈 РАЗВИТЫЕ НАВЫКИ:{XSSColors.RESET}")
        print(f"   • Анализ сетевого трафика")
        print(f"   • Обнаружение индикаторов компрометации")
        print(f"   • Классификация угроз безопасности")
        print(f"   • Форензика сетевых атак")

    def _show_failure_analysis(self, accuracy, time_taken, score, missed, false_positives):
        """Показывает экран неудачного анализа"""
        audio_system.play_sound("minigame_lose")

        print(f"\n{XSSColors.ERROR}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}║                    ❌ АНАЛИЗ НЕПОЛНЫЙ ❌                     ║{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🔍 Точность анализа: {accuracy:.1f}%{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время анализа: {time_taken:.1f} секунд{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}📉 Итоговый счет: {score} очков{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}📋 АНАЛИЗ ОШИБОК:{XSSColors.RESET}")
        if missed:
            print(f"   • Пропущено критических угроз: {len(missed)}")
        if false_positives:
            print(f"   • Ложных срабатываний: {len(false_positives)}")

        print(f"\n{XSSColors.INFO}💡 РЕКОМЕНДАЦИИ ДЛЯ УЛУЧШЕНИЯ:{XSSColors.RESET}")
        print(f"   • Изучите паттерны сетевых атак")
        print(f"   • Обращайте внимание на размеры пакетов")
        print(f"   • Анализируйте полезную нагрузку более детально")
        print(f"   • Используйте команду 'analyze' для подробного изучения")

    def _show_analysis_help(self):
        """Показывает справку по командам анализа"""
        print(f"\n{XSSColors.INFO}📖 СПРАВКА ПО КОМАНДАМ АНАЛИЗА:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze <id>{XSSColors.RESET} - Детальный анализ пакета")
        print(
            f"   {XSSColors.BRIGHT_GREEN}filter <protocol>{XSSColors.RESET} - Показать пакеты определенного протокола")
        print(
            f"   {XSSColors.BRIGHT_GREEN}suspicious <id1> <id2> ...{XSSColors.RESET} - Отметить подозрительные пакеты")
        print(f"   {XSSColors.BRIGHT_GREEN}list{XSSColors.RESET} - Показать весь список пакетов")
        print(f"   {XSSColors.BRIGHT_GREEN}hint{XSSColors.RESET} - Получить подсказку")
        print(f"   {XSSColors.BRIGHT_GREEN}submit{XSSColors.RESET} - Завершить анализ и получить результаты")
        print(f"   {XSSColors.BRIGHT_GREEN}help{XSSColors.RESET} - Показать эту справку")

    # Вспомогательные методы

    def _get_protocol_color(self, protocol):
        """Возвращает цвет для протокола"""
        colors = {
            'HTTP': XSSColors.WARNING,
            'HTTPS': XSSColors.SUCCESS,
            'SSH': XSSColors.INFO,
            'FTP': XSSColors.WARNING,
            'DNS': XSSColors.INFO,
            'SMTP': XSSColors.INFO,
            'TCP': XSSColors.LIGHT_GRAY,
            'TOR': XSSColors.DANGER,
            'VPN': XSSColors.SUCCESS,
            'SCADA': XSSColors.ERROR
        }
        return colors.get(protocol, XSSColors.RESET)

    def _get_protocol_port(self, protocol):
        """Возвращает стандартный порт для протокола"""
        ports = {
            'HTTP': 80,
            'HTTPS': 443,
            'SSH': 22,
            'FTP': 21,
            'DNS': 53,
            'SMTP': 25,
            'IRC': 6667,
            'VPN': 1194,
            'TOR': 9050,
            'SCADA': 502
        }
        return ports.get(protocol, random.randint(1024, 65535))

    def _get_flag_color(self, flag):
        """Возвращает цвет для флага"""
        dangerous_flags = ['Credentials', 'Exploit', 'C2 Communication', 'APT', 'Sabotage']
        warning_flags = ['Large Upload', 'Session Token', 'Anonymous', 'Encrypted']

        if any(danger in flag for danger in dangerous_flags):
            return XSSColors.ERROR
        elif any(warning in flag for warning in warning_flags):
            return XSSColors.WARNING
        else:
            return XSSColors.INFO

    def _get_threat_color(self, threat_level):
        """Возвращает цвет для уровня угрозы"""
        colors = {
            'None': XSSColors.SUCCESS,
            'Low': XSSColors.INFO,
            'Medium': XSSColors.WARNING,
            'High': XSSColors.ERROR,
            'Critical': XSSColors.DANGER
        }
        return colors.get(threat_level, XSSColors.RESET)

    def _generate_timestamp(self):
        """Генерирует временную метку"""
        now = time.time()
        offset = random.uniform(-300, 0)  # Последние 5 минут
        timestamp = now + offset
        return time.strftime("%H:%M:%S", time.localtime(timestamp))

    def _generate_session_id(self):
        """Генерирует случайный ID сессии"""
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def _generate_domain(self):
        """Генерирует случайный домен"""
        domains = ['evil-corp.com', 'malware-c2.net', 'suspicious-site.org', 'bad-actor.biz']
        return random.choice(domains)

    def _generate_hex_payload(self):
        """Генерирует hex payload"""
        return ''.join(random.choices('0123456789ABCDEF', k=16))

    def _generate_onion_address(self):
        """Генерирует адрес .onion"""
        chars = 'abcdefghijklmnopqrstuvwxyz234567'
        return ''.join(random.choices(chars, k=16)) + '.onion'

    def _generate_beacon_data(self):
        """Генерирует данные маяка"""
        beacon_types = ['heartbeat', 'command_request', 'data_exfil', 'lateral_move']
        return f"{random.choice(beacon_types)}_{random.randint(1000, 9999)}"


class MalwareAnalysisGame(Minigame):
    """Продвинутая мини-игра "Анализ вредоносного ПО" с реалистичными техниками исследования"""

    def __init__(self):
        super().__init__(
            "Анализ вредоносного ПО",
            "Исследуйте подозрительный файл используя различные техники анализа",
            "cracking"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        self._show_lab_interface()

        skill_level = game_state.get_skill(self.skill)
        analysis_config = self._get_analysis_config(skill_level)

        # Генерируем образец малвари
        malware_sample = self._generate_malware_sample(analysis_config)

        # Показываем начальную информацию
        self._show_sample_info(malware_sample)

        # Запускаем процесс анализа
        return self._run_malware_analysis(malware_sample, analysis_config)

    def _show_lab_interface(self):
        """Показывает интерфейс лаборатории анализа малвари"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║              🦠 MALWARE ANALYSIS LAB v3.2.1                  ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                ИЗОЛИРОВАННАЯ ПЕСОЧНИЦА                       ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}⚠️  ВНИМАНИЕ: Анализ проводится в изолированной среде{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🔬 Доступные инструменты: Песочница, Дизассемблер, Гексредактор{XSSColors.RESET}")

    def _get_analysis_config(self, skill_level):
        """Конфигурация сложности анализа"""
        configs = {
            'novice': {
                'complexity': 'simple',
                'obfuscation_level': 1,
                'analysis_tools': ['basic_scan', 'strings', 'sandbox'],
                'hints_available': 3,
                'time_limit': None,
                'sample_types': ['trojan', 'adware']
            },
            'intermediate': {
                'complexity': 'moderate',
                'obfuscation_level': 2,
                'analysis_tools': ['basic_scan', 'strings', 'sandbox', 'disassembler'],
                'hints_available': 2,
                'time_limit': 300,  # 5 минут
                'sample_types': ['trojan', 'adware', 'spyware', 'ransomware']
            },
            'advanced': {
                'complexity': 'complex',
                'obfuscation_level': 3,
                'analysis_tools': ['basic_scan', 'strings', 'sandbox', 'disassembler', 'hex_editor'],
                'hints_available': 1,
                'time_limit': 240,  # 4 минуты
                'sample_types': ['trojan', 'rootkit', 'ransomware', 'apt_malware']
            },
            'expert': {
                'complexity': 'sophisticated',
                'obfuscation_level': 4,
                'analysis_tools': ['basic_scan', 'strings', 'sandbox', 'disassembler', 'hex_editor',
                                   'behavioral_analysis'],
                'hints_available': 0,
                'time_limit': 180,  # 3 минуты
                'sample_types': ['rootkit', 'apt_malware', 'polymorphic', 'nation_state']
            }
        }

        if skill_level <= 2:
            return configs['novice']
        elif skill_level <= 5:
            return configs['intermediate']
        elif skill_level <= 7:
            return configs['advanced']
        else:
            return configs['expert']

    def _generate_malware_sample(self, config):
        """Генерирует образец вредоносного ПО"""
        sample_type = random.choice(config['sample_types'])
        obfuscation = config['obfuscation_level']

        # Базовые характеристики образца
        sample = {
            'filename': self._generate_filename(sample_type),
            'size': random.randint(1024, 1024 * 1024),  # От 1KB до 1MB
            'md5': self._generate_hash('md5'),
            'sha256': self._generate_hash('sha256'),
            'type': sample_type,
            'obfuscation_level': obfuscation,
            'packed': obfuscation >= 2,
            'encrypted': obfuscation >= 3,
            'polymorphic': obfuscation >= 4,
        }

        # Генерируем характеристики для каждого типа
        sample.update(self._get_malware_characteristics(sample_type, obfuscation))

        return sample

    def _generate_filename(self, malware_type):
        """Генерирует имя файла в зависимости от типа малвари"""
        filename_patterns = {
            'trojan': ['system_update.exe', 'security_patch.exe', 'important_document.pdf.exe', 'game_crack.exe'],
            'adware': ['free_software.exe', 'download_manager.exe', 'media_player.exe', 'toolbar_installer.exe'],
            'spyware': ['keylogger.exe', 'monitoring_tool.exe', 'parental_control.exe', 'system_monitor.exe'],
            'ransomware': ['decrypt_files.exe', 'payment_info.exe', 'unlock_tool.exe', 'file_recovery.exe'],
            'rootkit': ['system32.dll', 'kernel_driver.sys', 'windows_service.exe', 'boot_manager.exe'],
            'apt_malware': ['office_plugin.dll', 'network_scanner.exe', 'remote_admin.exe', 'lateral_tool.exe'],
            'polymorphic': ['morphing_sample.exe', 'variant_' + str(random.randint(1000, 9999)) + '.exe'],
            'nation_state': ['infrastructure_tool.exe', 'cyber_weapon.dll', 'state_actor.exe']
        }

        return random.choice(filename_patterns.get(malware_type, ['suspicious_file.exe']))

    def _get_malware_characteristics(self, malware_type, obfuscation):
        """Получает характеристики для каждого типа малвари"""
        characteristics = {
            'trojan': {
                'family': random.choice(['Zeus', 'Emotet', 'Trickbot', 'BankBot']),
                'purpose': 'Backdoor access and data theft',
                'network_activity': True,
                'persistence_method': 'Registry autostart',
                'target_data': ['banking_credentials', 'personal_files', 'system_info'],
                'c2_servers': [self._generate_c2_server() for _ in range(random.randint(1, 3))],
                'encryption_key': self._generate_key() if obfuscation >= 2 else None,
                'evasion_techniques': ['process_injection', 'api_hooking'] if obfuscation >= 3 else []
            },
            'adware': {
                'family': random.choice(['AdLoad', 'Superfish', 'Genieo', 'SearchMine']),
                'purpose': 'Display unwanted advertisements',
                'network_activity': True,
                'persistence_method': 'Browser extension',
                'target_data': ['browsing_history', 'search_queries'],
                'ad_servers': [f'ads{i}.malvertising.com' for i in range(1, 4)],
                'tracking_cookies': True,
                'browser_modification': True
            },
            'spyware': {
                'family': random.choice(['FinSpy', 'DarkComet', 'SpyEye', 'Pegasus']),
                'purpose': 'Covert surveillance and data collection',
                'network_activity': True,
                'persistence_method': 'System service',
                'target_data': ['keystrokes', 'screenshots', 'microphone', 'camera'],
                'stealth_level': 'high',
                'data_exfil_method': 'encrypted_channel',
                'monitoring_features': ['keylogger', 'screen_capture', 'file_monitor']
            },
            'ransomware': {
                'family': random.choice(['WannaCry', 'Ryuk', 'Maze', 'REvil']),
                'purpose': 'File encryption for ransom',
                'network_activity': False,
                'persistence_method': 'Immediate execution',
                'target_data': ['documents', 'images', 'databases'],
                'encryption_algorithm': 'AES-256' if obfuscation >= 2 else 'XOR',
                'ransom_note': f'YOUR_FILES_ARE_ENCRYPTED_{random.randint(1000, 9999)}.txt',
                'payment_method': 'Bitcoin',
                'timer_mechanism': True
            },
            'rootkit': {
                'family': random.choice(['Stuxnet', 'Flame', 'Carbanak', 'Turla']),
                'purpose': 'Deep system compromise and persistence',
                'network_activity': True,
                'persistence_method': 'Kernel-level hooks',
                'target_data': ['system_processes', 'network_traffic', 'file_system'],
                'stealth_techniques': ['file_hiding', 'process_hiding', 'network_hiding'],
                'privilege_level': 'kernel',
                'detection_evasion': 'advanced'
            },
            'apt_malware': {
                'family': random.choice(['APT1', 'Lazarus', 'Cozy Bear', 'Fancy Bear']),
                'purpose': 'Advanced persistent threat operations',
                'network_activity': True,
                'persistence_method': 'Multiple vectors',
                'target_data': ['classified_docs', 'intellectual_property', 'credentials'],
                'attribution': random.choice(['Nation State', 'Organized Crime', 'Hacktivist']),
                'campaign_name': f'Operation {random.choice(["Moonlight", "Shadowstorm", "Whisper", "Phantom"])}',
                'lateral_movement': True,
                'zero_days': obfuscation >= 3
            },
            'polymorphic': {
                'family': 'Polymorphic Engine',
                'purpose': 'Self-modifying malware',
                'network_activity': True,
                'persistence_method': 'Variable',
                'target_data': ['various'],
                'mutation_rate': f'{random.randint(60, 95)}%',
                'generation': random.randint(1, 100),
                'base_type': random.choice(['trojan', 'virus', 'worm']),
                'detection_rate': f'{random.randint(5, 30)}%'
            },
            'nation_state': {
                'family': random.choice(['Olympic Destroyer', 'NotPetya', 'Triton', 'VPNFilter']),
                'purpose': 'Cyber warfare and espionage',
                'network_activity': True,
                'persistence_method': 'Infrastructure compromise',
                'target_data': ['critical_infrastructure', 'government_secrets', 'military_data'],
                'sophistication': 'nation-state-level',
                'targets': ['power_grid', 'financial_system', 'government', 'military'],
                'attribution_confidence': 'moderate',
                'geopolitical_impact': 'high'
            }
        }

        return characteristics.get(malware_type, characteristics['trojan'])

    def _show_sample_info(self, sample):
        """Показывает базовую информацию об образце"""
        print(f"\n{XSSColors.WARNING}🦠 НОВЫЙ ОБРАЗЕЦ ДЛЯ АНАЛИЗА{XSSColors.RESET}")
        print(f"   Файл: {XSSColors.ERROR}{sample['filename']}{XSSColors.RESET}")
        print(f"   Размер: {sample['size']} байт")
        print(f"   MD5: {sample['md5']}")
        print(f"   SHA256: {sample['sha256'][:32]}...")

        # Показываем уровень обфускации
        obfuscation_status = ""
        if sample['packed']:
            obfuscation_status += f"{XSSColors.WARNING}📦 Упакован{XSSColors.RESET} "
        if sample['encrypted']:
            obfuscation_status += f"{XSSColors.ERROR}🔒 Зашифрован{XSSColors.RESET} "
        if sample['polymorphic']:
            obfuscation_status += f"{XSSColors.DANGER}🧬 Полиморфный{XSSColors.RESET} "

        if obfuscation_status:
            print(f"   Статус: {obfuscation_status}")

        print(f"\n{XSSColors.INFO}🔬 Начинаем анализ в изолированной среде...{XSSColors.RESET}")

    def _run_malware_analysis(self, sample, config):
        """Основной процесс анализа малвари"""
        analysis_data = {
            'tools_used': [],
            'findings': [],
            'identified_type': None,
            'confidence_level': 0,
            'analysis_score': 0
        }

        hints_used = 0
        start_time = time.time()

        print(f"\n{XSSColors.SUCCESS}🛠️  ДОСТУПНЫЕ ИНСТРУМЕНТЫ АНАЛИЗА:{XSSColors.RESET}")
        for i, tool in enumerate(config['analysis_tools'], 1):
            tool_name = self._get_tool_display_name(tool)
            print(f"   {i}. {tool_name}")

        print(f"\n{XSSColors.INFO}📋 КОМАНДЫ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}use <tool_name>{XSSColors.RESET} - Использовать инструмент")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze{XSSColors.RESET} - Финальный анализ")
        print(f"   {XSSColors.BRIGHT_GREEN}findings{XSSColors.RESET} - Показать найденные артефакты")
        print(f"   {XSSColors.BRIGHT_GREEN}identify <type>{XSSColors.RESET} - Идентифицировать тип малвари")
        print(f"   {XSSColors.BRIGHT_GREEN}hint{XSSColors.RESET} - Получить подсказку")
        print(f"   {XSSColors.BRIGHT_GREEN}submit{XSSColors.RESET} - Завершить анализ")

        while True:
            # Проверяем временное ограничение
            elapsed = time.time() - start_time
            remaining = None
            if config['time_limit']:
                remaining = config['time_limit'] - elapsed
                if remaining <= 0:
                    print(f"\n{XSSColors.ERROR}⏰ ВРЕМЯ АНАЛИЗА ИСТЕКЛО!{XSSColors.RESET}")
                    return self._evaluate_analysis(analysis_data, sample, elapsed, False)
                elif remaining <= 60:
                    print(f"{XSSColors.WARNING}⚠️ Осталось {remaining:.0f} секунд!{XSSColors.RESET}")

            # Показываем статус
            self._show_analysis_status(analysis_data, elapsed, remaining if config['time_limit'] else None)

            # Получаем команду
            command = audio_system.get_input_with_sound(
                f"{XSSColors.PROMPT}[Malware Lab]> {XSSColors.RESET}").strip().lower()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0]

            if cmd == "use" and len(parts) > 1:
                tool_input = parts[1].lower()

                # Создаем словарь соответствий для удобства пользователя
                tool_mappings = {
                    '1': 'basic_scan',
                    'basic_scan': 'basic_scan',
                    'антивирусное': 'basic_scan',
                    'сканирование': 'basic_scan',

                    '2': 'strings',
                    'strings': 'strings',
                    'строки': 'strings',
                    'анализ': 'strings',

                    '3': 'sandbox',
                    'sandbox': 'sandbox',
                    'песочница': 'sandbox',

                    '4': 'disassembler',
                    'disassembler': 'disassembler',
                    'дизассемблер': 'disassembler',

                    '5': 'hex_editor',
                    'hex_editor': 'hex_editor',
                    'hex': 'hex_editor',

                    '6': 'behavioral_analysis',
                    'behavioral_analysis': 'behavioral_analysis',
                    'поведенческий': 'behavioral_analysis'
                }

                tool = tool_mappings.get(tool_input)
                if tool and tool in config['analysis_tools']:
                    self._use_analysis_tool(tool, sample, analysis_data)
                else:
                    print(f"{XSSColors.ERROR}Инструмент недоступен или неверное название{XSSColors.RESET}")
                    print(
                        f"{XSSColors.INFO}Доступные: {', '.join(config['analysis_tools'])} или номера 1-6{XSSColors.RESET}")

            elif cmd == "findings":
                self._show_findings(analysis_data)

            elif cmd == "identify" and len(parts) > 1:
                identified_type = parts[1]
                self._identify_malware_type(identified_type, sample, analysis_data)

            elif cmd == "hint":
                if hints_used < config['hints_available']:
                    self._give_analysis_hint(sample, analysis_data, hints_used)
                    hints_used += 1
                else:
                    print(f"{XSSColors.WARNING}Подсказки исчерпаны{XSSColors.RESET}")

            elif cmd == "analyze":
                self._show_comprehensive_analysis(sample, analysis_data)

            elif cmd == "submit":
                final_elapsed = time.time() - start_time
                return self._evaluate_analysis(analysis_data, sample, final_elapsed, True)

            elif cmd == "help":
                self._show_analysis_help()

            else:
                print(f"{XSSColors.ERROR}Неизвестная команда. Используйте 'help' для справки{XSSColors.RESET}")

    def _use_analysis_tool(self, tool, sample, analysis_data):
        """Использует инструмент анализа"""
        if tool in analysis_data['tools_used']:
            print(f"{XSSColors.WARNING}Инструмент уже использован{XSSColors.RESET}")
            return

        analysis_data['tools_used'].append(tool)

        print(f"\n{XSSColors.INFO}🔧 Запуск {self._get_tool_display_name(tool)}...{XSSColors.RESET}")
        time.sleep(random.uniform(1, 2))  # Имитация анализа

        if tool == "basic_scan":
            self._basic_scan_analysis(sample, analysis_data)
        elif tool == "strings":
            self._strings_analysis(sample, analysis_data)
        elif tool == "sandbox":
            self._sandbox_analysis(sample, analysis_data)
        elif tool == "disassembler":
            self._disassembler_analysis(sample, analysis_data)
        elif tool == "hex_editor":
            self._hex_editor_analysis(sample, analysis_data)
        elif tool == "behavioral_analysis":
            self._behavioral_analysis(sample, analysis_data)

    def _basic_scan_analysis(self, sample, analysis_data):
        """Базовое сканирование антивирусом"""
        print(f"{XSSColors.SUCCESS}✅ Сканирование завершено{XSSColors.RESET}")

        # Симулируем обнаружение
        detection_engines = random.randint(15, 45)
        total_engines = 70

        findings = [
            f"Обнаружено {detection_engines}/{total_engines} антивирусными движками",
            f"Семейство: {sample.get('family', 'Unknown')}",
            f"Первое обнаружение: {random.randint(1, 30)} дней назад"
        ]

        if sample['type'] == 'polymorphic':
            findings.append("⚠️ Обнаружены признаки полиморфизма")

        analysis_data['findings'].extend(findings)
        analysis_data['confidence_level'] += 20

    def _strings_analysis(self, sample, analysis_data):
        """Анализ строк в файле"""
        print(f"{XSSColors.SUCCESS}✅ Извлечение строк завершено{XSSColors.RESET}")

        # Генерируем интересные строки в зависимости от типа
        malware_strings = self._generate_malware_strings(sample)

        print(f"\n{XSSColors.WARNING}📄 НАЙДЕННЫЕ СТРОКИ:{XSSColors.RESET}")
        for string in malware_strings[:5]:  # Показываем первые 5
            print(f"   {XSSColors.LIGHT_GRAY}'{string}'{XSSColors.RESET}")

        findings = [
            f"Извлечено {random.randint(50, 200)} читаемых строк",
            f"Обнаружены подозрительные API вызовы",
        ]

        if 'c2_servers' in sample:
            findings.append(f"Найдены C&C серверы: {sample['c2_servers'][0]}")

        analysis_data['findings'].extend(findings)
        analysis_data['confidence_level'] += 25

    def _sandbox_analysis(self, sample, analysis_data):
        """Анализ в песочнице"""
        print(f"{XSSColors.SUCCESS}✅ Выполнение в песочнице завершено{XSSColors.RESET}")

        # Симулируем поведенческий анализ
        behaviors = self._generate_sandbox_behaviors(sample)

        print(f"\n{XSSColors.WARNING}🏃‍♂️ ОБНАРУЖЕННОЕ ПОВЕДЕНИЕ:{XSSColors.RESET}")
        for behavior in behaviors:
            print(f"   {XSSColors.ERROR}• {behavior}{XSSColors.RESET}")

        findings = [
            f"Зарегистрировано {len(behaviors)} подозрительных действий",
            f"Попытки сетевого соединения: {'Да' if sample.get('network_activity') else 'Нет'}",
            f"Модификация реестра: {'Да' if 'Registry' in sample.get('persistence_method', '') else 'Нет'}"
        ]

        analysis_data['findings'].extend(findings)
        analysis_data['confidence_level'] += 30

    def _disassembler_analysis(self, sample, analysis_data):
        """Дизассемблирование кода"""
        print(f"{XSSColors.SUCCESS}✅ Дизассемблирование завершено{XSSColors.RESET}")

        # Генерируем псевдокод
        assembly_snippets = self._generate_assembly_code(sample)

        print(f"\n{XSSColors.WARNING}⚙️ КЛЮЧЕВЫЕ ФРАГМЕНТЫ КОДА:{XSSColors.RESET}")
        for snippet in assembly_snippets:
            print(f"   {XSSColors.LIGHT_GRAY}{snippet}{XSSColors.RESET}")

        findings = [
            "Обнаружены обфусцированные функции",
            f"Точки входа: {random.randint(1, 5)}",
            "Использование криптографических API"
        ]

        if sample.get('packed'):
            findings.append("⚠️ Обнаружен упаковщик/протектор")

        analysis_data['findings'].extend(findings)
        analysis_data['confidence_level'] += 35

    def _hex_editor_analysis(self, sample, analysis_data):
        """Анализ в hex-редакторе"""
        print(f"{XSSColors.SUCCESS}✅ Hex-анализ завершен{XSSColors.RESET}")

        # Генерируем hex-паттерны
        hex_patterns = self._generate_hex_patterns(sample)

        print(f"\n{XSSColors.WARNING}🔍 НАЙДЕННЫЕ ПАТТЕРНЫ:{XSSColors.RESET}")
        for pattern in hex_patterns:
            print(f"   {XSSColors.LIGHT_GRAY}{pattern}{XSSColors.RESET}")

        findings = [
            "Обнаружены встроенные исполняемые файлы",
            "Найдены зашифрованные секции",
            f"Энтропия файла: {random.uniform(6.5, 7.9):.2f} (подозрительно высокая)"
        ]

        analysis_data['findings'].extend(findings)
        analysis_data['confidence_level'] += 25

    def _behavioral_analysis(self, sample, analysis_data):
        """Продвинутый поведенческий анализ"""
        print(f"{XSSColors.SUCCESS}✅ Поведенческий анализ завершен{XSSColors.RESET}")

        # Продвинутые техники анализа
        advanced_behaviors = [
            f"Техника уклонения: {random.choice(['VM detection', 'Sandbox evasion', 'Debugger detection'])}",
            f"Методы персистенции: {sample.get('persistence_method', 'Unknown')}",
            f"Сетевая активность: {len(sample.get('c2_servers', []))} C&C серверов"
        ]

        print(f"\n{XSSColors.ERROR}🧠 ПРОДВИНУТЫЙ АНАЛИЗ ПОВЕДЕНИЯ:{XSSColors.RESET}")
        for behavior in advanced_behaviors:
            print(f"   • {behavior}")

        findings = [
            "Обнаружены anti-analysis техники",
            "Использование living-off-the-land binaries",
            f"Уровень сложности: {sample.get('obfuscation_level', 1)}/5"
        ]

        analysis_data['findings'].extend(findings)
        analysis_data['confidence_level'] += 40

    def _identify_malware_type(self, identified_type, sample, analysis_data):
        """Попытка идентификации типа малвари"""
        actual_type = sample['type']

        if identified_type == actual_type:
            print(f"{XSSColors.SUCCESS}✅ Правильная идентификация: {identified_type.upper()}{XSSColors.RESET}")
            analysis_data['identified_type'] = identified_type
            analysis_data['confidence_level'] += 50
        else:
            print(f"{XSSColors.ERROR}❌ Неверная идентификация. Попробуйте еще раз.{XSSColors.RESET}")
            analysis_data['confidence_level'] -= 10

    def _give_analysis_hint(self, sample, analysis_data, hint_number):
        """Дает подсказку для анализа"""
        hints = [
            f"💡 Подозрительное поведение связано с {sample.get('purpose', 'неизвестной целью')}",
            f"💡 Обратите внимание на {sample.get('persistence_method', 'методы персистенции')}",
            f"💡 Тип семейства: {sample.get('family', 'неизвестно')}"
        ]

        if hint_number < len(hints):
            print(f"\n{XSSColors.INFO}{hints[hint_number]}{XSSColors.RESET}")

    def _show_analysis_status(self, analysis_data, elapsed, remaining):
        """Показывает статус анализа"""
        tools_used = len(analysis_data['tools_used'])
        confidence = analysis_data['confidence_level']

        confidence_color = XSSColors.SUCCESS if confidence >= 80 else XSSColors.WARNING if confidence >= 50 else XSSColors.ERROR

        status = f"\n{XSSColors.INFO}📊 Статус: {tools_used} инструментов использовано | "
        status += f"Уверенность: {confidence_color}{confidence}%{XSSColors.RESET}"

        if remaining:
            time_color = XSSColors.SUCCESS if remaining > 120 else XSSColors.WARNING if remaining > 60 else XSSColors.ERROR
            status += f" | ⏰ {time_color}{remaining:.0f}s{XSSColors.RESET}"
        else:
            status += f" | ⏱️ {elapsed:.0f}s"

        print(status)

    def _show_findings(self, analysis_data):
        """Показывает все найденные артефакты"""
        if not analysis_data['findings']:
            print(f"{XSSColors.WARNING}Артефакты не найдены. Используйте инструменты анализа.{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.INFO}🔍 НАЙДЕННЫЕ АРТЕФАКТЫ:{XSSColors.RESET}")
        for i, finding in enumerate(analysis_data['findings'], 1):
            print(f"   {i}. {finding}")

    def _show_comprehensive_analysis(self, sample, analysis_data):
        """Показывает комплексный анализ"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ КОМПЛЕКСНЫЙ АНАЛИЗ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🦠 ОБРАЗЕЦ: {sample['filename']}{XSSColors.RESET}")
        print(f"   Размер: {sample['size']} байт")
        print(f"   Тип: {sample['type'].upper()}")
        print(f"   Семейство: {sample.get('family', 'Неизвестно')}")

        if analysis_data['identified_type']:
            correct = analysis_data['identified_type'] == sample['type']
            color = XSSColors.SUCCESS if correct else XSSColors.ERROR
            print(f"   Ваша идентификация: {color}{analysis_data['identified_type'].upper()}{XSSColors.RESET}")

        print(f"\n{XSSColors.INFO}🎯 НАЗНАЧЕНИЕ: {sample.get('purpose', 'Неизвестно')}{XSSColors.RESET}")

        if 'target_data' in sample:
            print(f"   Целевые данные: {', '.join(sample['target_data'])}")

        if 'c2_servers' in sample:
            print(f"   C&C серверы: {', '.join(sample['c2_servers'])}")

        print(f"\n{XSSColors.WARNING}🔧 ИСПОЛЬЗОВАННЫЕ ИНСТРУМЕНТЫ: {len(analysis_data['tools_used'])}{XSSColors.RESET}")
        for tool in analysis_data['tools_used']:
            print(f"   ✓ {self._get_tool_display_name(tool)}")

        confidence = analysis_data['confidence_level']
        confidence_color = XSSColors.SUCCESS if confidence >= 80 else XSSColors.WARNING if confidence >= 50 else XSSColors.ERROR
        print(f"\n{XSSColors.INFO}📊 Уверенность в анализе: {confidence_color}{confidence}%{XSSColors.RESET}")

    def _evaluate_analysis(self, analysis_data, sample, time_taken, completed):
        """Оценивает результаты анализа малвари"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ РЕЗУЛЬТАТЫ АНАЛИЗА ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Подсчет баллов
        tool_score = len(analysis_data['tools_used']) * 15
        identification_score = 100 if analysis_data['identified_type'] == sample['type'] else 0
        confidence_score = analysis_data['confidence_level']
        time_bonus = max(0, 100 - int(time_taken / 3)) if completed else 0
        completion_bonus = 50 if completed else -25

        total_score = tool_score + identification_score + confidence_score + time_bonus + completion_bonus

        print(f"\n{XSSColors.INFO}📊 ПОДСЧЕТ БАЛЛОВ:{XSSColors.RESET}")
        print(f"   Использование инструментов: +{tool_score}")
        if identification_score > 0:
            print(f"   Правильная идентификация: +{identification_score}")
        else:
            print(f"   Идентификация: {XSSColors.ERROR}не выполнена{XSSColors.RESET}")
        print(f"   Уверенность анализа: +{confidence_score}")
        if time_bonus > 0:
            print(f"   Бонус за скорость: +{time_bonus}")
        if completion_bonus < 0:
            print(f"   Штраф за незавершенность: {completion_bonus}")
        else:
            print(f"   Бонус за завершение: +{completion_bonus}")

        print(f"\n{XSSColors.BRIGHT_GREEN}🏆 ИТОГО: {total_score} баллов{XSSColors.RESET}")

        # Определяем успех
        success_threshold = 200
        identification_required = analysis_data['identified_type'] == sample['type']
        min_tools_used = len(analysis_data['tools_used']) >= 3

        success = total_score >= success_threshold and identification_required and min_tools_used

        if success:
            self._show_analysis_success(sample, analysis_data, total_score, time_taken)
        else:
            self._show_analysis_failure(sample, analysis_data, total_score, identification_required, min_tools_used)

        return success

    def _show_analysis_success(self, sample, analysis_data, score, time_taken):
        """Показывает экран успешного анализа"""
        audio_system.play_sound("minigame_win")

        print(f"\n{XSSColors.SUCCESS}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}║               🎉 АНАЛИЗ ЗАВЕРШЕН УСПЕШНО! 🎉                 ║{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🔬 Образец успешно классифицирован как: {sample['type'].upper()}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🏷️  Семейство: {sample.get('family', 'Неизвестно')}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время анализа: {time_taken:.1f} секунд{XSSColors.RESET}")
        print(f"{XSSColors.BRIGHT_GREEN}🏆 Итоговый счет: {score} баллов{XSSColors.RESET}")

        # Определяем ранг аналитика
        if score >= 400 and time_taken < 120:
            rank = f"{XSSColors.DANGER}🌟 ГРАНД-МАСТЕР МАЛВАРИ{XSSColors.RESET}"
        elif score >= 350:
            rank = f"{XSSColors.SUCCESS}💎 ЭКСПЕРТ ПО REVERSE ENGINEERING{XSSColors.RESET}"
        elif score >= 300:
            rank = f"{XSSColors.WARNING}🔧 SENIOR MALWARE ANALYST{XSSColors.RESET}"
        elif score >= 250:
            rank = f"{XSSColors.INFO}🎯 MALWARE RESEARCHER{XSSColors.RESET}"
        else:
            rank = f"{XSSColors.LIGHT_GRAY}📚 JUNIOR ANALYST{XSSColors.RESET}"

        print(f"\n🏅 Ваш ранг: {rank}")

        # Показываем детали обнаруженной угрозы
        print(f"\n{XSSColors.ERROR}🚨 ОТЧЕТ ОБ УГРОЗЕ:{XSSColors.RESET}")
        print(f"   • Назначение: {sample.get('purpose', 'Неизвестно')}")
        print(f"   • Уровень опасности: {self._get_threat_level(sample['type'])}")
        print(f"   • Рекомендуемые действия: {self._get_recommendations(sample['type'])}")

        # Показываем полученные навыки
        print(f"\n{XSSColors.INFO}📈 РАЗВИТЫЕ НАВЫКИ:{XSSColors.RESET}")
        skills = [
            "Статический анализ исполняемых файлов",
            "Динамический анализ поведения",
            "Reverse engineering техники",
            "Классификация семейств малвари",
            "Обнаружение техник уклонения"
        ]
        for skill in skills:
            print(f"   • {skill}")

    def _show_analysis_failure(self, sample, analysis_data, score, identification_correct, min_tools_used):
        """Показывает экран неудачного анализа"""
        audio_system.play_sound("minigame_lose")

        print(f"\n{XSSColors.ERROR}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}║                   ❌ АНАЛИЗ НЕПОЛНЫЙ ❌                      ║{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🔬 Образец не был полностью проанализирован{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}📉 Итоговый счет: {score} баллов{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}📋 АНАЛИЗ НЕДОСТАТКОВ:{XSSColors.RESET}")

        if not identification_correct:
            actual_type = sample['type']
            identified = analysis_data.get('identified_type', 'не определен')
            print(f"   ❌ Неверная идентификация: {identified} (правильно: {actual_type})")

        if not min_tools_used:
            used_count = len(analysis_data['tools_used'])
            print(f"   ❌ Недостаточно инструментов: {used_count}/3 минимум")

        if analysis_data['confidence_level'] < 50:
            print(f"   ❌ Низкая уверенность: {analysis_data['confidence_level']}%")

        # Показываем правильную информацию
        print(f"\n{XSSColors.INFO}💡 ПРАВИЛЬНАЯ КЛАССИФИКАЦИЯ:{XSSColors.RESET}")
        print(f"   Тип: {XSSColors.SUCCESS}{sample['type'].upper()}{XSSColors.RESET}")
        print(f"   Семейство: {sample.get('family', 'Неизвестно')}")
        print(f"   Назначение: {sample.get('purpose', 'Неизвестно')}")

        print(f"\n{XSSColors.WARNING}🎯 РЕКОМЕНДАЦИИ ДЛЯ УЛУЧШЕНИЯ:{XSSColors.RESET}")
        recommendations = [
            "Используйте больше инструментов анализа",
            "Обращайте внимание на строки и API вызовы",
            "Анализируйте поведение в песочнице",
            "Изучайте ассемблерный код для понимания функций",
            "Сопоставляйте найденные артефакты с известными семействами"
        ]
        for rec in recommendations:
            print(f"   • {rec}")

    def _show_analysis_help(self):
        """Показывает справку по анализу"""
        print(f"\n{XSSColors.INFO}📖 СПРАВКА ПО АНАЛИЗУ МАЛВАРИ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}use <tool>{XSSColors.RESET} - Использовать инструмент анализа")
        print(f"   {XSSColors.BRIGHT_GREEN}findings{XSSColors.RESET} - Показать все найденные артефакты")
        print(f"   {XSSColors.BRIGHT_GREEN}identify <type>{XSSColors.RESET} - Идентифицировать тип малвари")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze{XSSColors.RESET} - Показать комплексный анализ")
        print(f"   {XSSColors.BRIGHT_GREEN}hint{XSSColors.RESET} - Получить подсказку")
        print(f"   {XSSColors.BRIGHT_GREEN}submit{XSSColors.RESET} - Завершить анализ")

        print(f"\n{XSSColors.WARNING}🛠️ ДОСТУПНЫЕ ИНСТРУМЕНТЫ:{XSSColors.RESET}")
        tools = {
            'basic_scan': 'Антивирусное сканирование',
            'strings': 'Извлечение строк',
            'sandbox': 'Динамический анализ',
            'disassembler': 'Дизассемблирование',
            'hex_editor': 'Hex-анализ',
            'behavioral_analysis': 'Поведенческий анализ'
        }
        for tool, desc in tools.items():
            print(f"   • {tool} - {desc}")

    # Вспомогательные методы для генерации данных

    def _get_tool_display_name(self, tool):
        """Возвращает отображаемое имя инструмента"""
        names = {
            'basic_scan': '🛡️ Антивирусное сканирование',
            'strings': '📝 Анализ строк',
            'sandbox': '🏃‍♂️ Песочница',
            'disassembler': '⚙️ Дизассемблер',
            'hex_editor': '🔍 Hex-редактор',
            'behavioral_analysis': '🧠 Поведенческий анализ'
        }
        return names.get(tool, tool)

    def _generate_hash(self, hash_type):
        """Генерирует случайный хеш"""
        import hashlib
        import secrets

        data = secrets.token_bytes(32)
        if hash_type == 'md5':
            return hashlib.md5(data).hexdigest()
        elif hash_type == 'sha256':
            return hashlib.sha256(data).hexdigest()
        return hashlib.sha1(data).hexdigest()

    def _generate_c2_server(self):
        """Генерирует адрес C&C сервера"""
        domains = [
            'evil-command.com', 'malware-c2.net', 'bot-control.org',
            'remote-admin.biz', 'cyber-command.info', 'dark-control.online'
        ]
        return random.choice(domains)

    def _generate_key(self):
        """Генерирует криптографический ключ"""
        return ''.join(random.choices('0123456789ABCDEF', k=32))

    def _generate_malware_strings(self, sample):
        """Генерирует характерные строки для типа малвари"""
        common_strings = [
            "CreateProcessA", "WriteProcessMemory", "VirtualAlloc",
            "GetProcAddress", "LoadLibraryA", "RegOpenKeyEx"
        ]

        type_specific = {
            'trojan': [
                "Banking credentials", "keylogger.dll", "steal_passwords",
                sample.get('c2_servers', ['unknown.com'])[0] if sample.get('c2_servers') else 'c2.evil.com'
            ],
            'ransomware': [
                "YOUR FILES ARE ENCRYPTED", "send bitcoins to",
                sample.get('ransom_note', 'ransom.txt'), "AES encrypt"
            ],
            'spyware': [
                "screenshot.jpg", "keystrokes.log", "microphone access",
                "webcam capture", "location data"
            ],
            'rootkit': [
                "hide process", "kernel driver", "SSDT hook",
                "file system filter", "network hide"
            ]
        }

        strings = common_strings + type_specific.get(sample['type'], [])
        return random.sample(strings, min(len(strings), 8))

    def _generate_sandbox_behaviors(self, sample):
        """Генерирует поведение в песочнице"""
        common_behaviors = [
            "Попытка записи в системные директории",
            "Создание новых процессов",
            "Модификация реестра Windows"
        ]

        type_behaviors = {
            'trojan': [
                "Соединение с внешними серверами",
                "Кража сохраненных паролей браузера",
                "Установка backdoor компонентов"
            ],
            'ransomware': [
                "Массовое шифрование файлов",
                "Удаление теневых копий",
                "Создание файлов с требованием выкупа"
            ],
            'spyware': [
                "Мониторинг ввода с клавиатуры",
                "Создание скриншотов экрана",
                "Отправка собранных данных"
            ],
            'rootkit': [
                "Загрузка драйверов уровня ядра",
                "Перехват системных вызовов",
                "Сокрытие файлов и процессов"
            ]
        }

        behaviors = common_behaviors + type_behaviors.get(sample['type'], [])
        return random.sample(behaviors, min(len(behaviors), 5))

    def _generate_assembly_code(self, sample):
        """Генерирует фрагменты ассемблерного кода"""
        common_snippets = [
            "CALL GetProcAddress",
            "PUSH offset aKernel32dll",
            "MOV EAX, DWORD PTR [EBP+8]"
        ]

        type_snippets = {
            'trojan': [
                "CALL InternetConnectA",
                "PUSH offset aHttpsSomeC2Co",
                "CALL CryptEncrypt"
            ],
            'ransomware': [
                "CALL CryptGenRandom",
                "PUSH 00000080h ; AES-128",
                "CALL DeleteFileA"
            ],
            'spyware': [
                "CALL GetAsyncKeyState",
                "PUSH offset aKeylogTxt",
                "CALL CreateFileA"
            ]
        }

        snippets = common_snippets + type_snippets.get(sample['type'], [])
        return random.sample(snippets, min(len(snippets), 4))

    def _generate_hex_patterns(self, sample):
        """Генерирует характерные hex-паттерны"""
        common_patterns = [
            "4D 5A 90 00 (PE header)",
            "FF 25 ?? ?? ?? ?? (API thunk)",
            "55 8B EC (function prologue)"
        ]

        type_patterns = {
            'trojan': [
                "68 74 74 70 73 3A 2F 2F (https://)",
                "50 61 73 73 77 6F 72 64 (Password)"
            ],
            'ransomware': [
                "41 45 53 2D 32 35 36 (AES-256)",
                "2E 65 6E 63 72 79 70 74 (.encrypt)"
            ]
        }

        patterns = common_patterns + type_patterns.get(sample['type'], [])
        return random.sample(patterns, min(len(patterns), 4))

    def _get_threat_level(self, malware_type):
        """Возвращает уровень угрозы"""
        threat_levels = {
            'adware': 'Низкий',
            'spyware': 'Средний',
            'trojan': 'Высокий',
            'ransomware': 'Критический',
            'rootkit': 'Критический',
            'apt_malware': 'Критический',
            'nation_state': 'Критический'
        }
        return threat_levels.get(malware_type, 'Средний')

    def _get_recommendations(self, malware_type):
        """Возвращает рекомендации по реагированию"""
        recommendations = {
            'trojan': 'Изолировать систему, сменить пароли',
            'ransomware': 'Отключить от сети, восстановить из бэкапов',
            'spyware': 'Проверить утечку данных, усилить мониторинг',
            'rootkit': 'Полная переустановка системы',
            'apt_malware': 'Комплексное расследование, уведомление ИБ'
        }
        return recommendations.get(malware_type, 'Удалить и усилить защиту')


class HoneypotAvoidanceGame(Minigame):
    """Улучшенная мини-игра избегания honeypot'ов с реалистичной сетевой разведкой"""

    def __init__(self):
        super().__init__(
            "Избегание медовых ловушек",
            "Проведите разведку сети и избежите honeypot'ов на пути к цели",
            "stealth"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        self._show_reconnaissance_interface()

        skill_level = game_state.get_skill(self.skill)
        network_config = self._get_network_config(skill_level)

        # Генерируем сетевую топологию
        network_map = self._generate_network_topology(network_config)

        # Показываем начальную разведку
        self._show_initial_scan(network_map, network_config)

        # Основной игровой процесс
        return self._run_network_infiltration(network_map, network_config)

    def _show_reconnaissance_interface(self):
        """Показывает интерфейс разведки сети"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║              🕵️  NETWORK RECONNAISSANCE SUITE v4.2           ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                    HONEYPOT DETECTION SYSTEM                 ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🎯 МИССИЯ: Проникнуть в целевую сеть, избегая honeypot'ов{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🔍 Используйте инструменты разведки для обнаружения ловушек{XSSColors.RESET}")

    def _get_network_config(self, skill_level):
        """Конфигурация сети в зависимости от сложности"""
        configs = {
            'beginner': {
                'network_size': (4, 4),  # 4x4 сетка
                'honeypot_count': 2,
                'decoy_services': 1,
                'scan_tools': ['ping', 'port_scan', 'banner_grab'],
                'time_limit': None,
                'detection_difficulty': 'easy',
                'false_positives': 0
            },
            'intermediate': {
                'network_size': (5, 5),  # 5x5 сетка
                'honeypot_count': 3,
                'decoy_services': 2,
                'scan_tools': ['ping', 'port_scan', 'banner_grab', 'os_detect'],
                'time_limit': 240,  # 4 минуты
                'detection_difficulty': 'medium',
                'false_positives': 1
            },
            'advanced': {
                'network_size': (6, 6),  # 6x6 сетка
                'honeypot_count': 5,
                'decoy_services': 3,
                'scan_tools': ['ping', 'port_scan', 'banner_grab', 'os_detect', 'vuln_scan'],
                'time_limit': 180,  # 3 минуты
                'detection_difficulty': 'hard',
                'false_positives': 2
            },
            'expert': {
                'network_size': (7, 7),  # 7x7 сетка
                'honeypot_count': 8,
                'decoy_services': 5,
                'scan_tools': ['ping', 'port_scan', 'banner_grab', 'os_detect', 'vuln_scan', 'traffic_analysis'],
                'time_limit': 120,  # 2 минуты
                'detection_difficulty': 'extreme',
                'false_positives': 3
            }
        }

        if skill_level <= 2:
            return configs['beginner']
        elif skill_level <= 5:
            return configs['intermediate']
        elif skill_level <= 7:
            return configs['advanced']
        else:
            return configs['expert']

    def _generate_network_topology(self, config):
        """Генерирует топологию сети с хостами и honeypot'ами"""
        rows, cols = config['network_size']
        network = {}

        # Создаем все узлы сети
        for row in range(rows):
            for col in range(cols):
                node_id = f"{row}-{col}"
                network[node_id] = {
                    'position': (row, col),
                    'ip': f"192.168.{row}.{col + 10}",
                    'type': 'unknown',
                    'scanned': False,
                    'services': [],
                    'os': None,
                    'vulnerabilities': [],
                    'honeypot_indicators': [],
                    'suspicion_level': 0
                }

        # Определяем точки входа и цель
        entry_point = "0-0"
        target = f"{rows - 1}-{cols - 1}"

        network[entry_point]['type'] = 'entry'
        network[target]['type'] = 'target'

        # Размещаем honeypot'ы
        possible_positions = [k for k in network.keys() if k not in [entry_point, target]]
        honeypot_positions = random.sample(possible_positions, config['honeypot_count'])

        for pos in honeypot_positions:
            network[pos]['type'] = 'honeypot'
            self._configure_honeypot(network[pos], config['detection_difficulty'])

        # Размещаем обычные хосты
        remaining_positions = [k for k in possible_positions if k not in honeypot_positions]
        for pos in remaining_positions:
            network[pos]['type'] = 'legitimate'
            self._configure_legitimate_host(network[pos])

        # Настраиваем цель
        self._configure_target(network[target])

        # Добавляем ложные срабатывания
        self._add_false_positives(network, config['false_positives'])

        return {
            'nodes': network,
            'entry': entry_point,
            'target': target,
            'rows': rows,
            'cols': cols
        }

    def _configure_honeypot(self, node, difficulty):
        """Настраивает honeypot с различными уровнями маскировки"""
        honeypot_types = {
            'easy': {
                'services': [22, 80, 443],  # Стандартные порты
                'os': 'Linux 2.6.32 (fake)',
                'vulnerabilities': ['CVE-2020-1234 (fake)', 'Weak SSH'],
                'indicators': ['Too many open ports', 'Suspicious banner', 'Perfect vulnerability']
            },
            'medium': {
                'services': [22, 80, 443, 3306, 21],
                'os': 'Linux 4.15.0-generic',
                'vulnerabilities': ['Outdated OpenSSL', 'MySQL default creds'],
                'indicators': ['Honeypot signature in banner', 'Unusual response time']
            },
            'hard': {
                'services': [22, 80, 443, 3306, 21, 25, 110],
                'os': 'Ubuntu 18.04.3 LTS',
                'vulnerabilities': ['Apache 2.4.29 RCE', 'SSH bruteforce vulnerable'],
                'indicators': ['Kippo SSH signature', 'Too eager responses']
            },
            'extreme': {
                'services': [22, 80, 443, 3306, 21, 25, 110, 143, 993],
                'os': 'Ubuntu 20.04.1 LTS',
                'vulnerabilities': ['Zero-day available', 'Multiple RCE vulns'],
                'indicators': ['Subtle timing anomalies', 'Honeypot filesystem artifacts']
            }
        }

        config = honeypot_types[difficulty]
        node['services'] = config['services']
        node['os'] = config['os']
        node['vulnerabilities'] = config['vulnerabilities']
        node['honeypot_indicators'] = config['indicators']

        # Уровень подозрительности зависит от сложности
        suspicion_map = {'easy': 8, 'medium': 6, 'hard': 4, 'extreme': 2}
        node['suspicion_level'] = suspicion_map[difficulty]

    def _configure_legitimate_host(self, node):
        """Настраивает легитимный хост"""
        legitimate_configs = [
            {
                'services': [22, 80],
                'os': 'Ubuntu 20.04.1 LTS',
                'vulnerabilities': ['Minor config issues'],
                'suspicion_level': 0
            },
            {
                'services': [80, 443],
                'os': 'CentOS 7.8',
                'vulnerabilities': [],
                'suspicion_level': 0
            },
            {
                'services': [22, 3306],
                'os': 'Debian 10.3',
                'vulnerabilities': ['Outdated packages'],
                'suspicion_level': 1
            },
            {
                'services': [21, 22, 80],
                'os': 'Windows Server 2019',
                'vulnerabilities': ['SMB misconfiguration'],
                'suspicion_level': 1
            }
        ]

        config = random.choice(legitimate_configs)
        node['services'] = config['services']
        node['os'] = config['os']
        node['vulnerabilities'] = config['vulnerabilities']
        node['suspicion_level'] = config['suspicion_level']
        node['honeypot_indicators'] = []

    def _configure_target(self, node):
        """Настраивает целевой хост"""
        node['services'] = [22, 80, 443, 8080]
        node['os'] = 'Ubuntu 18.04.5 LTS'
        node['vulnerabilities'] = ['Apache Struts RCE', 'Weak admin credentials']
        node['suspicion_level'] = 0
        node['honeypot_indicators'] = []

    def _add_false_positives(self, network, count):
        """Добавляет ложные индикаторы honeypot'ов к легитимным хостам"""
        legitimate_hosts = [k for k, v in network.items() if v['type'] == 'legitimate']

        if count > 0 and legitimate_hosts:
            false_positive_hosts = random.sample(legitimate_hosts, min(count, len(legitimate_hosts)))

            fake_indicators = [
                'Unusual banner text',
                'Slow response time',
                'Default service responses',
                'Suspicious port configuration'
            ]

            for host in false_positive_hosts:
                network[host]['honeypot_indicators'] = [random.choice(fake_indicators)]
                network[host]['suspicion_level'] = random.randint(2, 4)

    def _show_initial_scan(self, network_map, config):
        """Показывает результаты начального сканирования"""
        print(f"\n{XSSColors.WARNING}🌐 ОБНАРУЖЕННАЯ СЕТЕВАЯ ТОПОЛОГИЯ:{XSSColors.RESET}")

        self._display_network_grid(network_map, show_details=False)

        print(f"\n{XSSColors.INFO}📡 Точка входа: {network_map['entry']} (ваша позиция){XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}🎯 Цель: {network_map['target']} (целевой сервер){XSSColors.RESET}")
        print(f"{XSSColors.WARNING}❓ Неизвестные узлы: сканирование требуется{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🛠️ ДОСТУПНЫЕ ИНСТРУМЕНТЫ РАЗВЕДКИ:{XSSColors.RESET}")
        for i, tool in enumerate(config['scan_tools'], 1):
            tool_name = self._get_tool_display_name(tool)
            print(f"   {XSSColors.BRIGHT_GREEN}{i}.{XSSColors.RESET} {tool_name}")

    def _display_network_grid(self, network_map, show_details=True):
        """Отображает сетку сети"""
        rows, cols = network_map['rows'], network_map['cols']

        # Заголовок с номерами колонок
        print("     ", end="")
        for col in range(cols):
            print(f"{col:^4}", end="")
        print()

        # Отображаем каждую строку
        for row in range(rows):
            print(f"{row:^3} ", end="")

            for col in range(cols):
                node_id = f"{row}-{col}"
                node = network_map['nodes'][node_id]
                symbol = self._get_node_symbol(node, show_details)
                print(f" {symbol} ", end=" ")
            print()

        if show_details:
            print(f"\n{XSSColors.INFO}ЛЕГЕНДА:{XSSColors.RESET}")
            print(f"   🏠 Точка входа    🎯 Цель         ? Неизвестно")
            print(f"   ✅ Безопасно     ⚠️  Подозрительно  🍯 Honeypot")
            print(f"   🔍 Сканируется   ❌ Заблокировано")

    def _get_node_symbol(self, node, show_details):
        """Возвращает символ для отображения узла"""
        if node['type'] == 'entry':
            return f"{XSSColors.SUCCESS}🏠{XSSColors.RESET}"
        elif node['type'] == 'target':
            return f"{XSSColors.BRIGHT_GREEN}🎯{XSSColors.RESET}"
        elif not node['scanned']:
            return f"{XSSColors.LIGHT_GRAY}?{XSSColors.RESET}"
        elif show_details:
            if node['type'] == 'honeypot':
                return f"{XSSColors.DANGER}🍯{XSSColors.RESET}"
            elif node['suspicion_level'] >= 5:
                return f"{XSSColors.WARNING}⚠️{XSSColors.RESET}"
            else:
                return f"{XSSColors.SUCCESS}✅{XSSColors.RESET}"
        else:
            return f"{XSSColors.INFO}🔍{XSSColors.RESET}"

    def _run_network_infiltration(self, network_map, config):
        """Основной процесс проникновения в сеть"""
        current_position = network_map['entry']
        scanned_nodes = []
        identified_honeypots = []
        false_alarms = []
        start_time = time.time()

        print(f"\n{XSSColors.INFO}📋 КОМАНДЫ РАЗВЕДКИ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}scan <tool_id> <position>{XSSColors.RESET} - Сканировать узел")
        print(f"   {XSSColors.BRIGHT_GREEN}move <position>{XSSColors.RESET} - Переместиться к узлу")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze <position>{XSSColors.RESET} - Детальный анализ узла")
        print(f"   {XSSColors.BRIGHT_GREEN}map{XSSColors.RESET} - Показать карту сети")
        print(f"   {XSSColors.BRIGHT_GREEN}status{XSSColors.RESET} - Статус миссии")
        print(f"   {XSSColors.BRIGHT_GREEN}help{XSSColors.RESET} - Справка")

        print(
            f"\n{XSSColors.WARNING}💡 ПРИМЕР: scan 1 1-2 (сканировать узел позиции 1-2 инструментом #1){XSSColors.RESET}")

        while True:
            # Проверяем временное ограничение
            if config['time_limit']:
                elapsed = time.time() - start_time
                remaining = config['time_limit'] - elapsed
                if remaining <= 0:
                    print(f"\n{XSSColors.ERROR}⏰ ВРЕМЯ МИССИИ ИСТЕКЛО!{XSSColors.RESET}")
                    return False
                elif remaining <= 30:
                    print(f"{XSSColors.WARNING}⚠️ Осталось {remaining:.0f} секунд!{XSSColors.RESET}")

            # Показываем текущий статус
            self._show_infiltration_status(current_position, network_map, scanned_nodes)

            # Получаем команду
            command = audio_system.get_input_with_sound(
                f"{XSSColors.PROMPT}[{current_position}]> {XSSColors.RESET}").strip().lower()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0]

            if cmd == "scan" and len(parts) >= 3:
                try:
                    tool_id = int(parts[1])
                    target_pos = parts[2]

                    if not (1 <= tool_id <= len(config['scan_tools'])):
                        print(
                            f"{XSSColors.ERROR}Неверный ID инструмента. Доступно: 1-{len(config['scan_tools'])}{XSSColors.RESET}")
                        continue

                    tool = config['scan_tools'][tool_id - 1]
                    result = self._perform_scan(tool, target_pos, network_map, config)

                    if result['success']:
                        if target_pos not in scanned_nodes:
                            scanned_nodes.append(target_pos)
                        print(f"{XSSColors.SUCCESS}✅ {result['message']}{XSSColors.RESET}")

                        # Показываем результаты сканирования
                        self._show_scan_results(result['data'])

                    else:
                        print(f"{XSSColors.ERROR}❌ {result['message']}{XSSColors.RESET}")

                except ValueError:
                    print(f"{XSSColors.ERROR}Неверный формат. Используйте: scan <tool_id> <position>{XSSColors.RESET}")

            elif cmd == "move" and len(parts) > 1:
                target_pos = parts[1]
                result = self._attempt_move(current_position, target_pos, network_map)

                if result['success']:
                    current_position = target_pos
                    print(f"{XSSColors.SUCCESS}✅ {result['message']}{XSSColors.RESET}")

                    # Проверяем, достигли ли цели
                    if current_position == network_map['target']:
                        final_elapsed = time.time() - start_time
                        return self._evaluate_mission(identified_honeypots, false_alarms, final_elapsed, True)

                    # Проверяем, попали ли в honeypot
                    node = network_map['nodes'][current_position]
                    if node['type'] == 'honeypot':
                        print(f"\n{XSSColors.DANGER}🚨 ПОПАЛИ В HONEYPOT! МИССИЯ ПРОВАЛЕНА!{XSSColors.RESET}")
                        self._show_honeypot_detection(node)
                        return False

                else:
                    print(f"{XSSColors.ERROR}❌ {result['message']}{XSSColors.RESET}")

            elif cmd == "analyze" and len(parts) > 1:
                target_pos = parts[1]
                self._analyze_node(target_pos, network_map)

            elif cmd == "map":
                print(f"\n{XSSColors.INFO}🗺️ КАРТА СЕТИ:{XSSColors.RESET}")
                self._display_network_grid(network_map, show_details=True)

            elif cmd == "status":
                self._show_detailed_status(current_position, network_map, scanned_nodes, identified_honeypots)

            elif cmd == "help":
                self._show_infiltration_help(config)

            else:
                print(f"{XSSColors.ERROR}Неизвестная команда. Используйте 'help' для справки{XSSColors.RESET}")

    def _perform_scan(self, tool, target_pos, network_map, config):
        """Выполняет сканирование узла указанным инструментом"""
        if target_pos not in network_map['nodes']:
            return {'success': False, 'message': 'Узел не найден в сети'}

        node = network_map['nodes'][target_pos]
        node['scanned'] = True

        # Различные инструменты дают разную информацию
        scan_data = {}

        if tool == 'ping':
            scan_data = self._ping_scan(node)
        elif tool == 'port_scan':
            scan_data = self._port_scan(node)
        elif tool == 'banner_grab':
            scan_data = self._banner_grab(node)
        elif tool == 'os_detect':
            scan_data = self._os_detection(node)
        elif tool == 'vuln_scan':
            scan_data = self._vulnerability_scan(node)
        elif tool == 'traffic_analysis':
            scan_data = self._traffic_analysis(node)

        tool_name = self._get_tool_display_name(tool)
        return {
            'success': True,
            'message': f'Сканирование {target_pos} завершено ({tool_name})',
            'data': scan_data
        }

    def _ping_scan(self, node):
        """Выполняет ping сканирование"""
        return {
            'tool': 'ping',
            'ip': node['ip'],
            'alive': True,
            'response_time': f"{random.randint(1, 50)}ms",
            'ttl': random.randint(60, 255)
        }

    def _port_scan(self, node):
        """Выполняет сканирование портов"""
        return {
            'tool': 'port_scan',
            'ip': node['ip'],
            'open_ports': node['services'],
            'port_count': len(node['services']),
            'scan_time': f"{random.randint(5, 30)}s"
        }

    def _banner_grab(self, node):
        """Захватывает баннеры сервисов"""
        banners = {}
        for port in node['services']:
            if port == 22:
                banners[22] = "SSH-2.0-OpenSSH_7.4"
            elif port == 80:
                banners[80] = "Apache/2.4.29 (Ubuntu)"
            elif port == 443:
                banners[443] = "nginx/1.14.0"
            elif port == 3306:
                banners[3306] = "MySQL 5.7.29"

        # Добавляем индикаторы honeypot'а в баннеры
        if node['type'] == 'honeypot' and node['honeypot_indicators']:
            suspicious_banner = random.choice(node['honeypot_indicators'])
            random_port = random.choice(node['services'])
            banners[random_port] += f" ({suspicious_banner})"

        return {
            'tool': 'banner_grab',
            'ip': node['ip'],
            'banners': banners,
            'suspicious_patterns': len(node['honeypot_indicators'])
        }

    def _os_detection(self, node):
        """Определяет операционную систему"""
        return {
            'tool': 'os_detect',
            'ip': node['ip'],
            'os': node['os'],
            'confidence': random.randint(85, 99),
            'fingerprint': f"OS:{random.randint(1000, 9999)}"
        }

    def _vulnerability_scan(self, node):
        """Сканирует уязвимости"""
        return {
            'tool': 'vuln_scan',
            'ip': node['ip'],
            'vulnerabilities': node['vulnerabilities'],
            'risk_level': 'High' if len(node['vulnerabilities']) > 2 else 'Medium',
            'exploitable': len(node['vulnerabilities']) > 0
        }

    def _traffic_analysis(self, node):
        """Анализирует сетевой трафик"""
        traffic_patterns = []

        if node['type'] == 'honeypot':
            traffic_patterns = [
                "Unusual response timing patterns",
                "Artificial traffic generation",
                "Honeypot signature in packets"
            ]
        else:
            traffic_patterns = [
                "Normal user activity",
                "Standard service responses",
                "Legitimate network patterns"
            ]

        return {
            'tool': 'traffic_analysis',
            'ip': node['ip'],
            'traffic_patterns': traffic_patterns,
            'anomaly_score': node['suspicion_level'],
            'baseline_deviation': f"{random.randint(0, 10)}%"
        }

    def _show_scan_results(self, scan_data):
        """Отображает результаты сканирования"""
        tool = scan_data['tool']
        ip = scan_data['ip']

        print(f"\n{XSSColors.INFO}🔍 РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ ({ip}):{XSSColors.RESET}")

        if tool == 'ping':
            print(f"   Статус: {XSSColors.SUCCESS}АКТИВЕН{XSSColors.RESET}")
            print(f"   Время отклика: {scan_data['response_time']}")
            print(f"   TTL: {scan_data['ttl']}")

        elif tool == 'port_scan':
            print(f"   Открытых портов: {XSSColors.WARNING}{scan_data['port_count']}{XSSColors.RESET}")
            print(f"   Порты: {', '.join(map(str, scan_data['open_ports']))}")
            print(f"   Время сканирования: {scan_data['scan_time']}")

        elif tool == 'banner_grab':
            print(f"   Найдено баннеров: {len(scan_data['banners'])}")
            for port, banner in scan_data['banners'].items():
                suspicious = "⚠️" if "suspicious" in banner.lower() or "honeypot" in banner.lower() else ""
                print(f"     Порт {port}: {banner} {suspicious}")

            if scan_data['suspicious_patterns'] > 0:
                print(f"   {XSSColors.WARNING}⚠️ Обнаружены подозрительные паттерны!{XSSColors.RESET}")

        elif tool == 'os_detect':
            print(f"   ОС: {XSSColors.INFO}{scan_data['os']}{XSSColors.RESET}")
            print(f"   Точность: {scan_data['confidence']}%")
            print(f"   Отпечаток: {scan_data['fingerprint']}")

        elif tool == 'vuln_scan':
            print(f"   Уязвимости: {XSSColors.ERROR}{len(scan_data['vulnerabilities'])}{XSSColors.RESET}")
            print(f"   Уровень риска: {scan_data['risk_level']}")
            for vuln in scan_data['vulnerabilities']:
                print(f"     • {vuln}")

        elif tool == 'traffic_analysis':
            print(f"   Аномальность: {XSSColors.WARNING}{scan_data['anomaly_score']}/10{XSSColors.RESET}")
            print(f"   Отклонение от базы: {scan_data['baseline_deviation']}")
            for pattern in scan_data['traffic_patterns']:
                color = XSSColors.ERROR if "honeypot" in pattern.lower() or "artificial" in pattern.lower() else XSSColors.SUCCESS
                print(f"     • {color}{pattern}{XSSColors.RESET}")

    def _attempt_move(self, current_pos, target_pos, network_map):
        """Попытка перемещения к узлу"""
        if target_pos not in network_map['nodes']:
            return {'success': False, 'message': 'Целевой узел не существует'}

        # Проверяем, является ли перемещение допустимым (соседние узлы)
        current_row, current_col = map(int, current_pos.split('-'))
        target_row, target_col = map(int, target_pos.split('-'))

        # Разрешаем перемещение только к соседним узлам (включая диагонали)
        row_diff = abs(target_row - current_row)
        col_diff = abs(target_col - current_col)

        if row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff) > 0:
            return {
                'success': True,
                'message': f'Перемещение с {current_pos} на {target_pos}'
            }
        else:
            return {
                'success': False,
                'message': 'Можно перемещаться только к соседним узлам'
            }

    def _analyze_node(self, target_pos, network_map):
        """Детальный анализ узла"""
        if target_pos not in network_map['nodes']:
            print(f"{XSSColors.ERROR}Узел {target_pos} не найден{XSSColors.RESET}")
            return

        node = network_map['nodes'][target_pos]

        if not node['scanned']:
            print(
                f"{XSSColors.WARNING}Узел {target_pos} не сканирован. Выполните сканирование сначала.{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ АНАЛИЗ УЗЛА {target_pos} ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        print(f"\n{XSSColors.INFO}📋 ОСНОВНАЯ ИНФОРМАЦИЯ:{XSSColors.RESET}")
        print(f"   IP-адрес: {node['ip']}")
        print(f"   Тип: {self._get_node_type_display(node['type'])}")
        print(f"   ОС: {node['os'] if node['os'] else 'Неизвестна'}")

        if node['services']:
            print(f"\n{XSSColors.WARNING}🔌 АКТИВНЫЕ СЕРВИСЫ:{XSSColors.RESET}")
            for port in node['services']:
                service_name = self._get_service_name(port)
                print(f"   • Порт {port}: {service_name}")

        if node['vulnerabilities']:
            print(f"\n{XSSColors.ERROR}🔓 УЯЗВИМОСТИ:{XSSColors.RESET}")
            for vuln in node['vulnerabilities']:
                print(f"   • {vuln}")

        # Анализ подозрительности
        suspicion = node['suspicion_level']
        if suspicion > 0:
            print(f"\n{XSSColors.WARNING}⚠️ АНАЛИЗ ПОДОЗРИТЕЛЬНОСТИ:{XSSColors.RESET}")
            print(f"   Уровень подозрительности: {self._get_suspicion_color(suspicion)}{suspicion}/10{XSSColors.RESET}")

            if node['honeypot_indicators']:
                print(f"   {XSSColors.ERROR}🚨 ИНДИКАТОРЫ HONEYPOT'А:{XSSColors.RESET}")
                for indicator in node['honeypot_indicators']:
                    print(f"     • {indicator}")

        # Рекомендации
        print(f"\n{XSSColors.SUCCESS}💡 РЕКОМЕНДАЦИИ:{XSSColors.RESET}")
        if suspicion >= 7:
            print(f"   {XSSColors.ERROR}❌ КРАЙНЕ ОПАСНО - Вероятно honeypot!{XSSColors.RESET}")
        elif suspicion >= 4:
            print(f"   {XSSColors.WARNING}⚠️ ПОДОЗРИТЕЛЬНО - Требует осторожности{XSSColors.RESET}")
        elif suspicion >= 2:
            print(f"   {XSSColors.INFO}ℹ️ УМЕРЕННЫЙ РИСК - Дополнительная проверка{XSSColors.RESET}")
        else:
            print(f"   {XSSColors.SUCCESS}✅ ОТНОСИТЕЛЬНО БЕЗОПАСНО{XSSColors.RESET}")

    def _show_infiltration_status(self, current_pos, network_map, scanned_nodes):
        """Показывает статус проникновения"""
        total_nodes = len(network_map['nodes'])
        scanned_count = len(scanned_nodes)

        print(f"\n{XSSColors.INFO}📊 Позиция: {XSSColors.BRIGHT_GREEN}{current_pos}{XSSColors.RESET} | "
              f"Отсканировано: {XSSColors.WARNING}{scanned_count}/{total_nodes}{XSSColors.RESET} узлов")

    def _show_detailed_status(self, current_pos, network_map, scanned_nodes, identified_honeypots):
        """Показывает детальный статус миссии"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ СТАТУС МИССИИ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        print(f"\n{XSSColors.INFO}📍 ТЕКУЩАЯ ПОЗИЦИЯ: {current_pos}{XSSColors.RESET}")
        print(f"🎯 ЦЕЛЬ: {network_map['target']}")
        print(f"🔍 Отсканированных узлов: {len(scanned_nodes)}")
        print(f"🍯 Обнаруженных honeypot'ов: {len(identified_honeypots)}")

        # Показываем подозрительные узлы
        suspicious_nodes = []
        for node_id, node in network_map['nodes'].items():
            if node['scanned'] and node['suspicion_level'] >= 4:
                suspicious_nodes.append((node_id, node['suspicion_level']))

        if suspicious_nodes:
            print(f"\n{XSSColors.WARNING}⚠️ ПОДОЗРИТЕЛЬНЫЕ УЗЛЫ:{XSSColors.RESET}")
            for node_id, suspicion in sorted(suspicious_nodes, key=lambda x: x[1], reverse=True):
                color = self._get_suspicion_color(suspicion)
                print(f"   • {node_id}: {color}{suspicion}/10{XSSColors.RESET}")

    def _show_honeypot_detection(self, node):
        """Показывает информацию об обнаруженном honeypot'е"""
        print(f"\n{XSSColors.DANGER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.DANGER}║                    🍯 HONEYPOT DETECTED! 🍯                  ║{XSSColors.RESET}")
        print(f"{XSSColors.DANGER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}🚨 Вы попали в honeypot на узле {node['ip']}!{XSSColors.RESET}")
        print(f"📊 Уровень подозрительности был: {node['suspicion_level']}/10")

        if node['honeypot_indicators']:
            print(f"\n{XSSColors.WARNING}🔍 ИНДИКАТОРЫ, КОТОРЫЕ СЛЕДОВАЛО ЗАМЕТИТЬ:{XSSColors.RESET}")
            for indicator in node['honeypot_indicators']:
                print(f"   • {indicator}")

        print(
            f"\n{XSSColors.INFO}💡 Система безопасности зафиксировала вторжение и активировала защитные меры.{XSSColors.RESET}")

    def _evaluate_mission(self, identified_honeypots, false_alarms, time_taken, success):
        """Оценивает результаты миссии"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ РЕЗУЛЬТАТЫ МИССИИ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        if success:
            self._show_mission_success(identified_honeypots, false_alarms, time_taken)
            return True
        else:
            self._show_mission_failure(time_taken)
            return False

    def _show_mission_success(self, identified_honeypots, false_alarms, time_taken):
        """Показывает экран успешной миссии"""
        audio_system.play_sound("minigame_win")

        print(f"\n{XSSColors.SUCCESS}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}║                🎉 МИССИЯ ВЫПОЛНЕНА! 🎉                       ║{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.SUCCESS}🎯 Цель достигнута без обнаружения!{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время миссии: {time_taken:.1f} секунд{XSSColors.RESET}")

        # Подсчет очков
        base_score = 100
        time_bonus = max(0, 50 - int(time_taken / 10))
        stealth_bonus = 25 if len(identified_honeypots) == 0 else 10

        total_score = base_score + time_bonus + stealth_bonus

        print(f"\n{XSSColors.INFO}📊 ПОДСЧЕТ ОЧКОВ:{XSSColors.RESET}")
        print(f"   Базовые очки: +{base_score}")
        if time_bonus > 0:
            print(f"   Бонус за скорость: +{time_bonus}")
        print(f"   Бонус за скрытность: +{stealth_bonus}")
        print(f"   {XSSColors.BRIGHT_GREEN}Итого: {total_score} очков{XSSColors.RESET}")

        # Оценка производительности
        if total_score >= 160:
            rating = f"{XSSColors.SUCCESS}🌟 МАСТЕР РАЗВЕДКИ!{XSSColors.RESET}"
        elif total_score >= 140:
            rating = f"{XSSColors.WARNING}💪 ОПЫТНЫЙ АГЕНТ!{XSSColors.RESET}"
        elif total_score >= 120:
            rating = f"{XSSColors.INFO}👍 ХОРОШАЯ РАБОТА!{XSSColors.RESET}"
        else:
            rating = f"{XSSColors.WARNING}😅 ЦЕЛЬ ДОСТИГНУТА{XSSColors.RESET}"

        print(f"\n🏆 Оценка: {rating}")

        print(f"\n{XSSColors.SUCCESS}✅ Honeypot'ы успешно обойдены! Доступ к целевой системе получен.{XSSColors.RESET}")

    def _show_mission_failure(self, time_taken):
        """Показывает экран провала миссии"""
        audio_system.play_sound("minigame_lose")

        print(f"\n{XSSColors.ERROR}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}║                    ❌ МИССИЯ ПРОВАЛЕНА ❌                    ║{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}🚨 Обнаружение сорвало операцию{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время до обнаружения: {time_taken:.1f} секунд{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}💡 СОВЕТЫ ДЛЯ СЛЕДУЮЩЕЙ ПОПЫТКИ:{XSSColors.RESET}")
        print(f"   • Тщательно сканируйте узлы перед перемещением")
        print(f"   • Обращайте внимание на уровень подозрительности")
        print(f"   • Используйте все доступные инструменты разведки")
        print(f"   • Анализируйте результаты сканирования на предмет индикаторов honeypot'ов")

        print(f"\n{XSSColors.INFO}🎯 Honeypot'ы - это ловушки, замаскированные под легитимные системы{XSSColors.RESET}")

    def _show_infiltration_help(self, config):
        """Показывает справку по проникновению"""
        print(f"\n{XSSColors.INFO}📖 СПРАВКА ПО ПРОНИКНОВЕНИЮ В СЕТЬ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}scan <tool_id> <position>{XSSColors.RESET} - Сканировать узел инструментом")
        print(f"   {XSSColors.BRIGHT_GREEN}move <position>{XSSColors.RESET} - Переместиться к соседнему узлу")
        print(f"   {XSSColors.BRIGHT_GREEN}analyze <position>{XSSColors.RESET} - Детальный анализ узла")
        print(f"   {XSSColors.BRIGHT_GREEN}map{XSSColors.RESET} - Показать карту сети")
        print(f"   {XSSColors.BRIGHT_GREEN}status{XSSColors.RESET} - Статус миссии")

        print(f"\n{XSSColors.WARNING}💡 ПРИМЕРЫ КОМАНД:{XSSColors.RESET}")
        print(f"   {XSSColors.LIGHT_GRAY}scan 1 1-2{XSSColors.RESET} - Ping узла 1-2")
        print(f"   {XSSColors.LIGHT_GRAY}scan 3 1-2{XSSColors.RESET} - Захват баннеров узла 1-2")
        print(f"   {XSSColors.LIGHT_GRAY}move 1-1{XSSColors.RESET} - Переместиться к узлу 1-1")
        print(f"   {XSSColors.LIGHT_GRAY}analyze 1-2{XSSColors.RESET} - Анализ узла 1-2")

        print(f"\n{XSSColors.SUCCESS}🛠️ ИНСТРУМЕНТЫ РАЗВЕДКИ:{XSSColors.RESET}")
        tools = {
            '1. 📡 Ping': 'Проверка доступности узла',
            '2. 🔍 Port Scan': 'Сканирование открытых портов',
            '3. 📋 Banner Grab': 'Захват баннеров сервисов',
            '4. 💻 OS Detection': 'Определение операционной системы',
            '5. 🔓 Vuln Scan': 'Поиск уязвимостей',
            '6. 📊 Traffic Analysis': 'Анализ сетевого трафика'
        }

        available_tools = config['scan_tools']
        for i, tool in enumerate(available_tools, 1):
            tool_key = f"{i}. {self._get_tool_display_name(tool)}"
            description = tools.get(tool_key, 'Инструмент разведки')
            print(f"   • {tool_key}: {description}")

        print(f"\n{XSSColors.ERROR}🍯 ОБНАРУЖЕНИЕ HONEYPOT'ОВ:{XSSColors.RESET}")
        print(f"   • Высокий уровень подозрительности (7+/10)")
        print(f"   • Подозрительные баннеры и отклики")
        print(f"   • Слишком много открытых портов")
        print(f"   • Идеальные уязвимости (слишком удобные)")
        print(f"   • Аномальные паттерны трафика")

        print(f"\n{XSSColors.WARNING}🎯 СТРАТЕГИЯ:{XSSColors.RESET}")
        print(f"   1. Сканируйте узлы перед перемещением")
        print(f"   2. Анализируйте подозрительные узлы детально")
        print(f"   3. Избегайте узлов с высоким уровнем подозрительности")
        print(f"   4. Планируйте безопасный маршрут к цели")

    # Вспомогательные методы

    def _get_tool_display_name(self, tool):
        """Возвращает отображаемое имя инструмента"""
        names = {
            'ping': '📡 Ping',
            'port_scan': '🔍 Port Scan',
            'banner_grab': '📋 Banner Grab',
            'os_detect': '💻 OS Detection',
            'vuln_scan': '🔓 Vuln Scan',
            'traffic_analysis': '📊 Traffic Analysis'
        }
        return names.get(tool, tool.title())

    def _get_node_type_display(self, node_type):
        """Возвращает отображаемый тип узла"""
        types = {
            'entry': f"{XSSColors.SUCCESS}Точка входа{XSSColors.RESET}",
            'target': f"{XSSColors.BRIGHT_GREEN}Цель{XSSColors.RESET}",
            'honeypot': f"{XSSColors.DANGER}Honeypot{XSSColors.RESET}",
            'legitimate': f"{XSSColors.INFO}Легитимный хост{XSSColors.RESET}",
            'unknown': f"{XSSColors.LIGHT_GRAY}Неизвестно{XSSColors.RESET}"
        }
        return types.get(node_type, node_type)

    def _get_service_name(self, port):
        """Возвращает название сервиса по порту"""
        services = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            3306: 'MySQL',
            8080: 'HTTP-Alt'
        }
        return services.get(port, 'Unknown')

    def _get_suspicion_color(self, level):
        """Возвращает цвет для уровня подозрительности"""
        if level >= 7:
            return XSSColors.DANGER
        elif level >= 4:
            return XSSColors.ERROR
        elif level >= 2:
            return XSSColors.WARNING
        else:
            return XSSColors.SUCCESS

    def get_difficulty(self) -> int:
        """Возвращает сложность в зависимости от навыка игрока"""
        skill_level = game_state.get_skill(self.skill)
        return min(3 + skill_level // 2, 8)

    def get_reputation_reward(self) -> int:
        """Рассчитывает награду репутации для этой мини-игры"""
        skill_level = game_state.get_skill(self.skill)
        difficulty = self.get_difficulty()

        base_rep = 3
        difficulty_bonus = difficulty // 2
        skill_bonus = 2 if skill_level >= 7 else 0

        return base_rep + difficulty_bonus + skill_bonus

    def show_potential_rewards(self) -> None:
        """Показывает потенциальные награды перед началом игры"""
        skill_level = game_state.get_skill(self.skill)
        rep_reward = self.get_reputation_reward()

        print(f"\n{XSSColors.INFO}🏆 ПОТЕНЦИАЛЬНЫЕ НАГРАДЫ:{XSSColors.RESET}")
        print(f"   💰 BTC: 7-22")
        print(f"   ⭐ Репутация: {rep_reward}")
        print(f"   📊 Сложность: {self.get_difficulty()}/8")
        print(f"   🎯 Тип навыка: Stealth (Скрытность)")

        if skill_level >= 8:
            print(f"   ✨ Экспертный бонус: Продвинутые инструменты разведки")

class LogDeletionGame(Minigame):
    """Мини-игра "Удаление логов"."""
    def __init__(self):
        super().__init__(
            "Удаление логов",
            "Быстро удалите критические записи из списка логов",
            "stealth"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ УДАЛЕНИЕ ЛОГОВ ━━━━━━━━━━{XSSColors.RESET}")
        skill_level = game_state.get_skill(self.skill)
        num_logs = 10 + skill_level * 2
        critical_keywords = ["ERROR", "ATTACK", "INTRUSION", "FAILED LOGIN"]

        log_entries = []
        critical_indices = []

        for i in range(num_logs):
            is_critical = random.random() < 0.2 + skill_level * 0.02 # Шанс на критический лог
            if is_critical:
                keyword = random.choice(critical_keywords)
                log_entries.append(f"{time.strftime('%H:%M:%S')} [CRITICAL] {keyword} from {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
                critical_indices.append(i)
            else:
                log_entries.append(f"{time.strftime('%H:%M:%S')} [INFO] User {random.choice(['admin', 'guest', 'dev'])} logged in.")

        random.shuffle(log_entries) # Перемешиваем, чтобы не было легко

        # Пересчитываем индексы критических логов после перемешивания
        final_critical_indices = []
        for i, entry in enumerate(log_entries):
            for keyword in critical_keywords:
                if keyword in entry:
                    final_critical_indices.append(i + 1) # +1 для нумерации с 1
                    break

        if not final_critical_indices: # Если случайно не сгенерировалось ни одного критического лога
            # Добавим хотя бы один
            idx_to_make_critical = random.randint(0, num_logs - 1)
            keyword = random.choice(critical_keywords)
            log_entries[idx_to_make_critical] = f"{time.strftime('%H:%M:%S')} [CRITICAL] {keyword} from {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            final_critical_indices.append(idx_to_make_critical + 1)

        final_critical_indices = sorted(list(set(final_critical_indices))) # Убираем дубликаты и сортируем

        print(f"{XSSColors.INFO}Перед вами список логов. Ваша задача - быстро ввести номера логов, которые содержат критические ключевые слова (ERROR, ATTACK, INTRUSION, FAILED LOGIN).{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Введите номера через пробел (например: 3 5 7).{XSSColors.RESET}\n")

        for i, log in enumerate(log_entries):
            print(f"   {i+1}. {log}")

        print(f"\n{XSSColors.INFO}У вас есть {max(5, 15 - skill_level)} секунд на удаление.{XSSColors.RESET}")

        start_time = time.time()
        user_input_str = audio_system.get_input_with_sound(f"{XSSColors.PROMPT}Логи для удаления: {XSSColors.RESET}")
        end_time = time.time()

        time_taken = end_time - start_time
        time_limit = max(5, 15 - skill_level) # Время уменьшается с уровнем навыка

        if time_taken > time_limit:
            audio_system.play_sound("minigame_lose")
            print(f"\n{XSSColors.ERROR}❌ Время вышло! Вы слишком медленно удаляли логи ({time_taken:.2f} сек.){XSSColors.RESET}")
            print(f"Нужно было удалить: {', '.join(map(str, final_critical_indices))}{XSSColors.RESET}")
            return False

        try:
            user_deleted_indices = sorted(list(set([int(x) for x in user_input_str.split()])))

            if user_deleted_indices == final_critical_indices:
                audio_system.play_sound("minigame_win")
                print(f"\n{XSSColors.SUCCESS}🎉 УСПЕХ! Все критические логи успешно удалены!{XSSColors.RESET}")
                print(f"Время: {time_taken:.2f} сек.{XSSColors.RESET}")
                return True
            else:
                audio_system.play_sound("minigame_lose")
                print(f"\n{XSSColors.ERROR}❌ Провал! Вы удалили не те или не все логи.{XSSColors.RESET}")
                print(f"Нужно было удалить: {', '.join(map(str, final_critical_indices))}{XSSColors.RESET}")
                print(f"Вы удалили: {', '.join(map(str, user_deleted_indices))}{XSSColors.RESET}")
                return False

        except ValueError:
            audio_system.play_sound("minigame_lose")
            print(f"{XSSColors.ERROR}Неверный формат ввода. Введите числа, разделенные пробелами.{XSSColors.RESET}")
            return False

class TrafficObfuscationGame(Minigame):
    """Мини-игра "Маскировка трафика"."""
    def __init__(self):
        super().__init__(
            "Маскировка трафика",
            "Выберите лучший метод обфускации для скрытия своих действий",
            "stealth"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ МАСКИРОВКА ТРАФИКА ━━━━━━━━━━{XSSColors.RESET}")

        obfuscation_methods = {
            "VPN": "Перенаправляет трафик через зашифрованный туннель, меняя ваш IP.",
            "Tor": "Маршрутизирует трафик через распределенную сеть серверов, многократно шифруя.",
            "Прокси-сервер": "Выступает посредником между вами и целевым сервером, скрывая ваш IP.",
            "DNS Tunneling": "Скрывает данные в DNS-запросах и ответах.",
            "SSL/TLS Encapsulation": "Оборачивает вредоносный трафик в легитимный SSL/TLS."
        }

        scenarios = [
            {"goal": "Скрыть IP-адрес для обычного просмотра веб-страниц", "correct": "VPN"},
            {"goal": "Обеспечить максимальную анонимность и обход цензуры", "correct": "Tor"},
            {"goal": "Доступ к ресурсам, заблокированным по географическому признаку", "correct": "Прокси-сервер"},
            {"goal": "Скрытно передать небольшие объемы данных через файрвол, блокирующий обычный трафик", "correct": "DNS Tunneling"},
            {"goal": "Маскировать атакующий трафик под безопасное HTTPS-соединение", "correct": "SSL/TLS Encapsulation"}
        ]

        selected_scenario = random.choice(scenarios)
        correct_method = selected_scenario["correct"]

        print(f"{XSSColors.INFO}Прочитайте сценарий и выберите наиболее подходящий метод маскировки трафика.{XSSColors.RESET}\n")
        print(f"{XSSColors.WARNING}Сценарий: {selected_scenario['goal']}{XSSColors.RESET}\n")

        print(f"{XSSColors.INFO}Доступные методы:{XSSColors.RESET}")
        method_options = list(obfuscation_methods.keys())
        random.shuffle(method_options) # Перемешиваем порядок отображения

        for i, method in enumerate(method_options, 1):
            print(f"   {i}. {method} - {obfuscation_methods[method]}")

        attempts = 2
        while attempts > 0:
            try:
                user_choice_idx = int(audio_system.get_input_with_sound(f"{XSSColors.PROMPT}Ваш выбор (номер): {XSSColors.RESET}"))

                if not (1 <= user_choice_idx <= len(method_options)):
                    print(f"{XSSColors.ERROR}Неверный номер. Попробуйте еще раз.{XSSColors.RESET}")
                    continue

                user_guess_method = method_options[user_choice_idx - 1]

                if user_guess_method == correct_method:
                    audio_system.play_sound("minigame_win")
                    print(f"\n{XSSColors.SUCCESS}🎉 УСПЕХ! Вы выбрали оптимальный метод маскировки.{XSSColors.RESET}")
                    return True
                else:
                    attempts -= 1
                    print(f"{XSSColors.ERROR}Неверно! Это не самый эффективный метод для данного сценария. Попыток осталось: {attempts}.{XSSColors.RESET}")
            except ValueError:
                print(f"{XSSColors.ERROR}Введите число.{XSSColors.RESET}")

        audio_system.play_sound("minigame_lose")
        print(f"\n{XSSColors.ERROR}❌ Провал! Правильный метод был: {correct_method}.{XSSColors.RESET}")
        return False


class SocialEngineeringGame(Minigame):
    """Мини-игра "Социальная инженерия"."""

    def __init__(self):
        super().__init__(
            "Социальная инженерия",
            "Выберите правильный ответ в диалоге для получения информации",
            "stealth"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ СОЦИАЛЬНАЯ ИНЖЕНЕРИЯ ━━━━━━━━━━{XSSColors.RESET}")

        dialogues = [
            {
                "scenario": "Вы звоните в техподдержку. Цель: узнать имя руководителя.",
                "conversation": [
                    {"speaker": "Секретарь", "text": "Техническая поддержка, чем могу помочь?"},
                    {"speaker": "Вы", "options": [
                        "1. Здравствуйте, я из отдела аудита, мне нужен контакт вашего руководителя.",
                        "2. Привет, у меня проблема с доступом к системе. С кем я могу поговорить по этому поводу?",
                        "3. Здравствуйте, меня зовут [Ваше имя], я новый сотрудник, и мне нужно срочно связаться с руководителем вашего отдела по важному вопросу."
                    ], "correct_option": "3", "feedback": {
                        "1": "Секретарь: Извините, мы не можем предоставить эту информацию по телефону.",
                        "2": "Секретарь: Я могу помочь вам с доступом. Опишите проблему.",
                        "3": "Секретарь: О, новый сотрудник! Конечно, наш руководитель - Иван Петров, его прямой номер 123-45-67."
                    }},
                ]
            },
            {
                "scenario": "Вы общаетесь в чате с сотрудником компании. Цель: получить его логин.",
                "conversation": [
                    {"speaker": "Сотрудник", "text": "Привет, есть вопрос по проекту 'Альфа'."},
                    {"speaker": "Вы", "options": [
                        "1. Привет! А кто это, чтобы я мог правильно вас идентифицировать?",
                        "2. Привет. Какой именно вопрос? Мой логин 'хакер_про', чтобы ты мог меня найти.",
                        "3. Привет! Могу помочь. Подскажи, пожалуйста, свой логин, чтобы я мог посмотреть твой доступ к проекту?"
                    ], "correct_option": "3", "feedback": {
                        "1": "Сотрудник: Я - Олег из отдела 'Бета'.",
                        "2": "Сотрудник: Эм, не знаю такого логина. Может, ты ошибся?",
                        "3": "Сотрудник: Конечно, мой логин 'oleg_b'. Спасибо за помощь!"
                    }},
                ]
            }
        ]

        selected_dialogue = random.choice(dialogues)

        print(f"{XSSColors.INFO}Сценарий: {selected_dialogue['scenario']}{XSSColors.RESET}\n")

        for turn in selected_dialogue["conversation"]:
            # Исправлено: используем правильный ключ для текста
            speaker_text = turn.get('text', '')
            if speaker_text:
                print(f"{turn['speaker']}: {speaker_text}")

            if "options" in turn:
                for option in turn["options"]:
                    print(f"   {option}")

                attempts = 1  # Одна попытка на каждый выбор
                while attempts > 0:
                    user_choice = audio_system.get_input_with_sound(
                        f"{XSSColors.PROMPT}Ваш выбор (номер): {XSSColors.RESET}")

                    if user_choice == turn["correct_option"].replace(".", ""):  # Убираем точку, если она в опции
                        print(f"{XSSColors.SUCCESS}{turn['feedback'][user_choice]}{XSSColors.RESET}")
                        audio_system.play_sound("minigame_win")
                        return True
                    else:
                        if user_choice in turn["feedback"]:
                            print(f"{XSSColors.ERROR}{turn['feedback'][user_choice]}{XSSColors.RESET}")
                        else:
                            print(f"{XSSColors.ERROR}Неверный выбор. Попробуйте еще раз.{XSSColors.RESET}")
                        attempts -= 1

        audio_system.play_sound("minigame_lose")
        print(f"\n{XSSColors.ERROR}❌ Провал! Не удалось получить нужную информацию.{XSSColors.RESET}")
        return False


class CovertChannelGame(Minigame):
    """Продвинутая мини-игра "Скрытый канал" с реалистичными техниками сокрытия данных"""

    def __init__(self):
        super().__init__(
            "Скрытый канал",
            "Используйте различные техники стеганографии для скрытой передачи данных",
            "stealth"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        self._show_covert_lab_interface()

        skill_level = game_state.get_skill(self.skill)
        mission_config = self._get_mission_config(skill_level)

        # Генерируем миссию
        mission = self._generate_covert_mission(mission_config)

        # Показываем брифинг
        self._show_mission_briefing(mission)

        # Основной игровой процесс
        return self._run_covert_operation(mission, mission_config)

    def _show_covert_lab_interface(self):
        """Показывает интерфейс лаборатории скрытых каналов"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║              🕵️  COVERT CHANNEL LABORATORY v2.8              ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                  ЛАБОРАТОРИЯ СТЕГАНОГРАФИИ                   ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(
            f"\n{XSSColors.WARNING}🎯 МИССИЯ: Передать секретные данные незаметно для систем мониторинга{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🔬 Используйте продвинутые техники стеганографии и сокрытия{XSSColors.RESET}")

    def _get_mission_config(self, skill_level):
        """Конфигурация миссии в зависимости от сложности"""
        configs = {
            'novice': {
                'data_size': 'small',  # 2-4 байта
                'detection_level': 'basic',
                'available_methods': ['lsb_image', 'text_spacing', 'dns_timing'],
                'monitoring_systems': 1,
                'time_limit': 180,  # 3 минуты
                'hints_available': 3,
                'noise_level': 'low'
            },
            'intermediate': {
                'data_size': 'medium',  # 8-16 байт
                'detection_level': 'moderate',
                'available_methods': ['lsb_image', 'text_spacing', 'dns_timing', 'tcp_timestamp', 'icmp_echo'],
                'monitoring_systems': 2,
                'time_limit': 150,
                'hints_available': 2,
                'noise_level': 'medium'
            },
            'advanced': {
                'data_size': 'large',  # 32-64 байта
                'detection_level': 'high',
                'available_methods': ['lsb_image', 'text_spacing', 'dns_timing', 'tcp_timestamp', 'icmp_echo',
                                      'file_slack'],
                'monitoring_systems': 3,
                'time_limit': 120,
                'hints_available': 1,
                'noise_level': 'high'
            },
            'expert': {
                'data_size': 'enterprise',  # 128+ байт
                'detection_level': 'military',
                'available_methods': ['lsb_image', 'text_spacing', 'dns_timing', 'tcp_timestamp', 'icmp_echo',
                                      'file_slack', 'blockchain_meta', 'audio_spectral'],
                'monitoring_systems': 4,
                'time_limit': 90,
                'hints_available': 0,
                'noise_level': 'extreme'
            }
        }

        if skill_level <= 2:
            return configs['novice']
        elif skill_level <= 5:
            return configs['intermediate']
        elif skill_level <= 7:
            return configs['advanced']
        else:
            return configs['expert']

    def _generate_covert_mission(self, config):
        """Генерирует миссию для скрытой передачи"""
        # Определяем тип секретных данных
        data_types = {
            'small': {
                'data': self._generate_secret_code(8),  # 8-символьный код
                'description': 'Код активации агента',
                'priority': 'Высокий',
                'bytes': 8
            },
            'medium': {
                'data': self._generate_coordinates() + "|" + self._generate_time_code(),
                'description': 'Координаты встречи и время',
                'priority': 'Критический',
                'bytes': 24
            },
            'large': {
                'data': self._generate_operation_plan(),
                'description': 'План операции "Фантом"',
                'priority': 'Совершенно секретно',
                'bytes': 64
            },
            'enterprise': {
                'data': self._generate_intelligence_report(),
                'description': 'Разведывательный отчет',
                'priority': 'Только для руководства',
                'bytes': 128
            }
        }

        secret_data = data_types[config['data_size']]

        # Генерируем контекст миссии
        mission_contexts = [
            {
                'scenario': 'Промышленный шпионаж',
                'target': 'TechCorp Industries',
                'cover': 'IT-консультант',
                'risk_level': 'Средний'
            },
            {
                'scenario': 'Правительственная разведка',
                'target': 'Министерство обороны',
                'cover': 'Системный администратор',
                'risk_level': 'Высокий'
            },
            {
                'scenario': 'Кибер-операция',
                'target': 'Банковская система',
                'cover': 'Специалист по безопасности',
                'risk_level': 'Критический'
            },
            {
                'scenario': 'Контрразведка',
                'target': 'Иностранная резидентура',
                'cover': 'Журналист',
                'risk_level': 'Экстремальный'
            }
        ]

        context = random.choice(mission_contexts)

        return {
            'context': context,
            'secret_data': secret_data,
            'monitoring_systems': self._generate_monitoring_systems(config),
            'cover_traffic': self._generate_cover_traffic(config),
            'time_window': config['time_limit']
        }

    def _generate_monitoring_systems(self, config):
        """Генерирует системы мониторинга"""
        systems = []

        all_systems = [
            {
                'name': 'Firewall DPI',
                'type': 'deep_packet_inspection',
                'detection_methods': ['pattern_matching', 'statistical_analysis'],
                'effectiveness': 70,
                'description': 'Глубокая инспекция пакетов с анализом содержимого'
            },
            {
                'name': 'IDS Snort',
                'type': 'intrusion_detection',
                'detection_methods': ['signature_based', 'anomaly_detection'],
                'effectiveness': 65,
                'description': 'Система обнаружения вторжений с базой сигнатур'
            },
            {
                'name': 'Traffic Analyzer',
                'type': 'network_analysis',
                'detection_methods': ['flow_analysis', 'timing_analysis'],
                'effectiveness': 80,
                'description': 'Анализатор сетевого трафика с ML-алгоритмами'
            },
            {
                'name': 'Steganography Scanner',
                'type': 'stego_detection',
                'detection_methods': ['lsb_analysis', 'frequency_analysis'],
                'effectiveness': 85,
                'description': 'Специализированный сканер стеганографии'
            },
            {
                'name': 'Behavioral Monitor',
                'type': 'behavior_analysis',
                'detection_methods': ['user_profiling', 'access_patterns'],
                'effectiveness': 75,
                'description': 'Система анализа поведения пользователей'
            }
        ]

        # Выбираем системы в зависимости от количества
        selected_systems = random.sample(all_systems, config['monitoring_systems'])

        # Адаптируем эффективность к уровню сложности
        detection_multiplier = {
            'basic': 0.7,
            'moderate': 0.85,
            'high': 1.0,
            'military': 1.2
        }

        for system in selected_systems:
            system['effectiveness'] = min(95, int(
                system['effectiveness'] * detection_multiplier[config['detection_level']]))
            systems.append(system)

        return systems

    def _generate_cover_traffic(self, config):
        """Генерирует легитимный трафик для маскировки"""
        traffic_types = [
            {
                'type': 'web_browsing',
                'description': 'Обычный веб-трафик (HTTP/HTTPS)',
                'volume': 'high',
                'suspicion': 'very_low'
            },
            {
                'type': 'email_exchange',
                'description': 'Корпоративная почта (SMTP/IMAP)',
                'volume': 'medium',
                'suspicion': 'low'
            },
            {
                'type': 'file_transfers',
                'description': 'Передача файлов (FTP/SFTP)',
                'volume': 'medium',
                'suspicion': 'medium'
            },
            {
                'type': 'video_calls',
                'description': 'Видеоконференции (RTP/WebRTC)',
                'volume': 'high',
                'suspicion': 'low'
            },
            {
                'type': 'software_updates',
                'description': 'Обновления ПО',
                'volume': 'low',
                'suspicion': 'very_low'
            }
        ]

        # Выбираем подходящие типы трафика
        available_traffic = random.sample(traffic_types, random.randint(2, 4))
        return available_traffic

    def _show_mission_briefing(self, mission):
        """Показывает брифинг миссии"""
        print(f"\n{XSSColors.WARNING}📋 БРИФИНГ МИССИИ{XSSColors.RESET}")
        print(f"{XSSColors.LIGHT_GRAY}{'─' * 60}{XSSColors.RESET}")

        context = mission['context']
        secret_data = mission['secret_data']

        print(f"\n{XSSColors.INFO}🎭 ЛЕГЕНДА:{XSSColors.RESET}")
        print(f"   Сценарий: {context['scenario']}")
        print(f"   Цель: {context['target']}")
        print(f"   Прикрытие: {context['cover']}")
        print(
            f"   Уровень риска: {self._get_risk_color(context['risk_level'])}{context['risk_level']}{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}🔒 СЕКРЕТНЫЕ ДАННЫЕ:{XSSColors.RESET}")
        print(f"   Тип: {secret_data['description']}")
        print(f"   Приоритет: {secret_data['priority']}")
        print(f"   Размер: {secret_data['bytes']} байт")
        print(f"   Данные: {XSSColors.DANGER}[ЗАСЕКРЕЧЕНО]{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🔍 СИСТЕМЫ МОНИТОРИНГА:{XSSColors.RESET}")
        for i, system in enumerate(mission['monitoring_systems'], 1):
            effectiveness_color = self._get_effectiveness_color(system['effectiveness'])
            print(f"   {i}. {system['name']}")
            print(f"      Тип: {system['type']}")
            print(f"      Эффективность: {effectiveness_color}{system['effectiveness']}%{XSSColors.RESET}")
            print(f"      Описание: {system['description']}")

        print(f"\n{XSSColors.SUCCESS}📡 ДОСТУПНЫЙ ЛЕГИТИМНЫЙ ТРАФИК:{XSSColors.RESET}")
        for traffic in mission['cover_traffic']:
            suspicion_color = self._get_suspicion_color(traffic['suspicion'])
            print(
                f"   • {traffic['description']} - Подозрительность: {suspicion_color}{traffic['suspicion']}{XSSColors.RESET}")

        print(f"\n{XSSColors.INFO}⏰ Время на выполнение: {mission['time_window']} секунд{XSSColors.RESET}")

    def _run_covert_operation(self, mission, config):
        """Основной процесс скрытой передачи"""
        available_methods = config['available_methods']
        secret_data = mission['secret_data']['data']
        monitoring_systems = mission['monitoring_systems']

        print(f"\n{XSSColors.SUCCESS}🛠️  ДОСТУПНЫЕ МЕТОДЫ СОКРЫТИЯ:{XSSColors.RESET}")
        for i, method in enumerate(available_methods, 1):
            method_info = self._get_method_info(method)
            print(f"   {i}. {method_info['name']}")
            print(f"      Описание: {method_info['description']}")
            print(f"      Скрытность: {self._get_stealth_rating(method_info['stealth'])}")
            print(f"      Пропускная способность: {method_info['capacity']}")

        print(f"\n{XSSColors.INFO}📋 КОМАНДЫ ОПЕРАЦИИ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}use <method_id>{XSSColors.RESET} - Выбрать метод сокрытия")
        print(f"   {XSSColors.BRIGHT_GREEN}configure <parameters>{XSSColors.RESET} - Настроить параметры")
        print(f"   {XSSColors.BRIGHT_GREEN}test{XSSColors.RESET} - Тестовая передача")
        print(f"   {XSSColors.BRIGHT_GREEN}transmit{XSSColors.RESET} - Передать секретные данные")
        print(f"   {XSSColors.BRIGHT_GREEN}status{XSSColors.RESET} - Статус операции")
        print(f"   {XSSColors.BRIGHT_GREEN}abort{XSSColors.RESET} - Прервать операцию")

        # Состояние операции
        operation_state = {
            'selected_method': None,
            'configured': False,
            'test_passed': False,
            'detection_risk': 0,
            'time_elapsed': 0,
            'attempts': 0,
            'max_attempts': 3
        }

        start_time = time.time()

        while operation_state['attempts'] < operation_state['max_attempts']:
            # Проверяем время
            elapsed = time.time() - start_time
            remaining = mission['time_window'] - elapsed

            if remaining <= 0:
                print(f"\n{XSSColors.ERROR}⏰ ВРЕМЯ ОПЕРАЦИИ ИСТЕКЛО!{XSSColors.RESET}")
                return self._evaluate_operation(operation_state, mission, elapsed, False, "timeout")

            # Показываем статус
            self._show_operation_status(operation_state, remaining)

            # Получаем команду
            command = audio_system.get_input_with_sound(
                f"{XSSColors.PROMPT}[Операция]> {XSSColors.RESET}").strip().lower()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0]

            if cmd == "use" and len(parts) > 1:
                try:
                    method_id = int(parts[1])
                    if 1 <= method_id <= len(available_methods):
                        method = available_methods[method_id - 1]
                        operation_state['selected_method'] = method
                        operation_state['configured'] = False
                        operation_state['test_passed'] = False
                        print(
                            f"{XSSColors.SUCCESS}✅ Выбран метод: {self._get_method_info(method)['name']}{XSSColors.RESET}")
                    else:
                        print(f"{XSSColors.ERROR}Неверный ID метода{XSSColors.RESET}")
                except ValueError:
                    print(f"{XSSColors.ERROR}Неверный формат команды{XSSColors.RESET}")

            elif cmd == "configure":
                if operation_state['selected_method']:
                    result = self._configure_method(operation_state['selected_method'],
                                                    parts[1:] if len(parts) > 1 else [])
                    operation_state['configured'] = result['success']
                    operation_state['detection_risk'] = result.get('risk', 0)
                    if result['success']:
                        print(f"{XSSColors.SUCCESS}✅ Метод настроен{XSSColors.RESET}")
                    else:
                        print(f"{XSSColors.ERROR}❌ {result['message']}{XSSColors.RESET}")
                else:
                    print(f"{XSSColors.ERROR}Сначала выберите метод{XSSColors.RESET}")

            elif cmd == "test":
                if operation_state['configured']:
                    result = self._test_transmission(operation_state, monitoring_systems)
                    operation_state['test_passed'] = result['success']
                    operation_state['detection_risk'] += result.get('risk_increase', 0)

                    if result['success']:
                        print(f"{XSSColors.SUCCESS}✅ Тест прошел успешно{XSSColors.RESET}")
                    else:
                        print(f"{XSSColors.WARNING}⚠️ {result['message']}{XSSColors.RESET}")
                        if result.get('detected', False):
                            operation_state['attempts'] += 1
                            print(
                                f"{XSSColors.ERROR}🚨 Обнаружение! Попыток осталось: {operation_state['max_attempts'] - operation_state['attempts']}{XSSColors.RESET}")
                else:
                    print(f"{XSSColors.ERROR}Сначала настройте метод{XSSColors.RESET}")

            elif cmd == "transmit":
                if operation_state['test_passed']:
                    final_elapsed = time.time() - start_time
                    result = self._final_transmission(operation_state, monitoring_systems, secret_data)
                    return self._evaluate_operation(operation_state, mission, final_elapsed, result['success'],
                                                    result.get('failure_reason', 'unknown'))
                else:
                    print(f"{XSSColors.ERROR}Необходимо провести успешный тест{XSSColors.RESET}")

            elif cmd == "status":
                self._show_detailed_status(operation_state, mission)

            elif cmd == "abort":
                print(f"{XSSColors.WARNING}Операция прервана{XSSColors.RESET}")
                return False

            elif cmd == "help":
                self._show_operation_help()

            else:
                print(f"{XSSColors.ERROR}Неизвестная команда{XSSColors.RESET}")

        print(f"\n{XSSColors.ERROR}❌ Исчерпаны все попытки! Операция провалена.{XSSColors.RESET}")
        return False

    def _configure_method(self, method, parameters):
        """Настройка выбранного метода"""
        method_configs = {
            'lsb_image': {
                'required_params': ['bit_depth', 'image_type'],
                'valid_values': {
                    'bit_depth': ['1', '2', '3'],
                    'image_type': ['jpg', 'png', 'bmp']
                },
                'default_risk': 30
            },
            'text_spacing': {
                'required_params': ['spacing_type', 'document_format'],
                'valid_values': {
                    'spacing_type': ['character', 'word', 'line'],
                    'document_format': ['txt', 'doc', 'pdf']
                },
                'default_risk': 20
            },
            'dns_timing': {
                'required_params': ['delay_pattern', 'domain_count'],
                'valid_values': {
                    'delay_pattern': ['fixed', 'variable', 'fibonacci'],
                    'domain_count': ['3', '5', '10']
                },
                'default_risk': 40
            },
            'tcp_timestamp': {
                'required_params': ['timestamp_field', 'encoding_rate'],
                'valid_values': {
                    'timestamp_field': ['options', 'sequence', 'ack'],
                    'encoding_rate': ['1', '2', '4']
                },
                'default_risk': 50
            },
            'icmp_echo': {
                'required_params': ['payload_size', 'interval'],
                'valid_values': {
                    'payload_size': ['32', '64', '128'],
                    'interval': ['1', '2', '5']
                },
                'default_risk': 45
            },
            'file_slack': {
                'required_params': ['file_type', 'cluster_size'],
                'valid_values': {
                    'file_type': ['exe', 'dll', 'sys'],
                    'cluster_size': ['4096', '8192', '16384']
                },
                'default_risk': 25
            },
            'blockchain_meta': {
                'required_params': ['blockchain', 'transaction_type'],
                'valid_values': {
                    'blockchain': ['bitcoin', 'ethereum', 'monero'],
                    'transaction_type': ['standard', 'multisig', 'contract']
                },
                'default_risk': 15
            },
            'audio_spectral': {
                'required_params': ['frequency_range', 'encoding_method'],
                'valid_values': {
                    'frequency_range': ['low', 'mid', 'high'],
                    'encoding_method': ['lsb', 'phase', 'spread']
                },
                'default_risk': 35
            }
        }

        config = method_configs.get(method)
        if not config:
            return {'success': False, 'message': 'Неизвестный метод'}

        if not parameters:
            # Показываем справку по настройке выбранного метода
            method_help = {
                'lsb_image': {
                    'title': '🖼️ LSB STEGANOGRAPHY',
                    'params': [
                        ('bit_depth', ['1', '2', '3'], [
                            '1 = 1 бит (максимальная скрытность, медленно)',
                            '2 = 2 бита (баланс скрытности и скорости)',
                            '3 = 3 бита (быстро, но заметно)'
                        ]),
                        ('image_type', ['jpg', 'png', 'bmp'], [
                            'jpg = JPEG (сжатый, может исказить)',
                            'png = PNG (без потерь, РЕКОМЕНДУЕТСЯ)',
                            'bmp = BMP (большой, подозрительно)'
                        ])
                    ],
                    'examples': ['configure 1 png', 'configure 2 png', 'configure 3 jpg']
                },
                'text_spacing': {
                    'title': '📝 TEXT SPACING',
                    'params': [
                        ('spacing_type', ['character', 'word', 'line'], [
                            'character = между символами (заметно)',
                            'word = между словами (средне)',
                            'line = между строками (НЕЗАМЕТНО)'
                        ]),
                        ('document_format', ['txt', 'doc', 'pdf'], [
                            'txt = обычный текст (странно)',
                            'doc = Word документ (нормально)',
                            'pdf = PDF (профессионально)'
                        ])
                    ],
                    'examples': ['configure line pdf', 'configure word doc', 'configure character txt']
                },
                'dns_timing': {
                    'title': '🌐 DNS TIMING',
                    'params': [
                        ('delay_pattern', ['fixed', 'variable', 'fibonacci'], [
                            'fixed = одинаковые (ЛЕГКО ОБНАРУЖИТЬ)',
                            'variable = случайные (средняя защита)',
                            'fibonacci = Фибоначчи (ТРУДНО ОБНАРУЖИТЬ)'
                        ]),
                        ('domain_count', ['3', '5', '10'], [
                            '3 = быстро, паттерн заметен',
                            '5 = ОПТИМАЛЬНО',
                            '10 = скрытно, но медленно'
                        ])
                    ],
                    'examples': ['configure fibonacci 5', 'configure variable 3', 'configure variable 10']
                },
                'tcp_timestamp': {
                    'title': '📡 TCP TIMESTAMP',
                    'params': [
                        ('timestamp_field', ['options', 'sequence', 'ack'], [
                            'options = поле опций (БЕЗОПАСНЕЕ)',
                            'sequence = номер последовательности (рискованно)',
                            'ack = номер подтверждения (ОЧЕНЬ РИСКОВАННО)'
                        ]),
                        ('encoding_rate', ['1', '2', '4'], [
                            '1 = 1 бит/пакет (медленно, СКРЫТНО)',
                            '2 = 2 бита/пакет (баланс)',
                            '4 = 4 бита/пакет (быстро, ЗАМЕТНО)'
                        ])
                    ],
                    'examples': ['configure options 1', 'configure options 2', 'configure sequence 4']
                },
                'icmp_echo': {
                    'title': '📶 ICMP ECHO',
                    'params': [
                        ('payload_size', ['32', '64', '128'], [
                            '32 = стандартный ping (НЕЗАМЕТНО)',
                            '64 = немного больше обычного',
                            '128 = ПОДОЗРИТЕЛЬНО большой'
                        ]),
                        ('interval', ['1', '2', '5'], [
                            '1 = 1 сек (частые пинги, ПОДОЗРИТЕЛЬНО)',
                            '2 = 2 сек (НОРМАЛЬНАЯ частота)',
                            '5 = 5 сек (редко, незаметно, медленно)'
                        ])
                    ],
                    'examples': ['configure 32 2', 'configure 32 5', 'configure 64 2']
                },
                'file_slack': {
                    'title': '💾 FILE SLACK SPACE',
                    'params': [
                        ('file_type', ['exe', 'dll', 'sys'], [
                            'exe = исполняемые (проверка антивирусом)',
                            'dll = библиотеки (МЕНЕЕ ПОДОЗРИТЕЛЬНО)',
                            'sys = системные (скрытно, но рискованно)'
                        ]),
                        ('cluster_size', ['4096', '8192', '16384'], [
                            '4096 = 4KB (мало места, незаметно)',
                            '8192 = 8KB (ОПТИМАЛЬНО)',
                            '16384 = 16KB (много места, подозрительно)'
                        ])
                    ],
                    'examples': ['configure dll 8192', 'configure sys 4096', 'configure exe 16384']
                },
                'blockchain_meta': {
                    'title': '₿ BLOCKCHAIN METADATA',
                    'params': [
                        ('blockchain', ['bitcoin', 'ethereum', 'monero'], [
                            'bitcoin = популярный, много транзакций',
                            'ethereum = умные контракты (ГИБКОСТЬ)',
                            'monero = анонимный (МАКСИМАЛЬНАЯ СКРЫТНОСТЬ)'
                        ]),
                        ('transaction_type', ['standard', 'multisig', 'contract'], [
                            'standard = обычная (простая, дешевая)',
                            'multisig = мультиподпись (БОЛЬШЕ МЕСТА)',
                            'contract = смарт-контракт (максимум возможностей)'
                        ])
                    ],
                    'examples': ['configure monero multisig', 'configure bitcoin standard',
                                 'configure ethereum contract']
                },
                'audio_spectral': {
                    'title': '🎵 AUDIO SPECTRAL',
                    'params': [
                        ('frequency_range', ['low', 'mid', 'high'], [
                            'low = низкие частоты (МЕНЕЕ ЗАМЕТНО)',
                            'mid = средние частоты (баланс)',
                            'high = высокие частоты (заметно при анализе)'
                        ]),
                        ('encoding_method', ['lsb', 'phase', 'spread'], [
                            'lsb = младшие биты (простой, может быть обнаружен)',
                            'phase = фазовое кодирование (СЛОЖНЕЕ ОБНАРУЖИТЬ)',
                            'spread = спектральное распределение (МАКСИМАЛЬНАЯ СКРЫТНОСТЬ)'
                        ])
                    ],
                    'examples': ['configure low spread', 'configure mid phase', 'configure high lsb']
                }
            }

            help_info = method_help.get(method)
            if help_info:
                print(f"\n{XSSColors.INFO}⚙️ НАСТРОЙКА: {help_info['title']}{XSSColors.RESET}")
                print(
                    f"Команда: {XSSColors.BRIGHT_GREEN}configure <{help_info['params'][0][0]}> <{help_info['params'][1][0]}>{XSSColors.RESET}")

                for param_name, valid_values, descriptions in help_info['params']:
                    print(f"\n{XSSColors.WARNING}{param_name}:{XSSColors.RESET}")
                    for desc in descriptions:
                        print(f"  {desc}")

                print(f"\n{XSSColors.SUCCESS}Примеры команд:{XSSColors.RESET}")
                for example in help_info['examples']:
                    print(f"  {XSSColors.LIGHT_GRAY}{example}{XSSColors.RESET}")

                return {'success': False, 'message': 'Выберите параметры из списка выше'}
            else:
                print(f"\n{XSSColors.ERROR}Справка для метода {method} недоступна{XSSColors.RESET}")
                return {'success': False, 'message': 'Неизвестный метод'}

        # Проверяем параметры
        if len(parameters) < len(config['required_params']):
            return {'success': False, 'message': 'Недостаточно параметров'}

        for i, param_value in enumerate(parameters[:len(config['required_params'])]):
            param_name = config['required_params'][i]
            if param_value not in config['valid_values'][param_name]:
                return {'success': False, 'message': f'Неверное значение для {param_name}'}

        # Рассчитываем риск на основе выбранных параметров
        risk = config['default_risk']

        # Некоторые параметры увеличивают/уменьшают риск
        risk_modifiers = {
            'bit_depth': {'1': -10, '2': 0, '3': +10},
            'spacing_type': {'character': +5, 'word': 0, 'line': -5},
            'delay_pattern': {'fixed': +15, 'variable': 0, 'fibonacci': -10},
            'payload_size': {'32': -5, '64': 0, '128': +10}
        }

        for i, param_value in enumerate(parameters[:len(config['required_params'])]):
            param_name = config['required_params'][i]
            if param_name in risk_modifiers and param_value in risk_modifiers[param_name]:
                risk += risk_modifiers[param_name][param_value]

        risk = max(10, min(90, risk))  # Ограничиваем риск

        return {'success': True, 'risk': risk}

    def _test_transmission(self, operation_state, monitoring_systems):
        """Тестовая передача данных"""
        method = operation_state['selected_method']
        base_risk = operation_state['detection_risk']

        print(f"\n{XSSColors.INFO}🧪 Запуск тестовой передачи...{XSSColors.RESET}")
        time.sleep(random.uniform(1, 2))

        # Проверяем каждую систему мониторинга
        detected = False
        total_suspicion = 0

        for system in monitoring_systems:
            detection_chance = self._calculate_detection_chance(method, system, base_risk)

            if random.random() * 100 < detection_chance:
                print(f"{XSSColors.ERROR}🚨 {system['name']}: Обнаружена аномалия!{XSSColors.RESET}")
                detected = True
                break
            else:
                suspicion_increase = random.randint(1, 5)
                total_suspicion += suspicion_increase
                print(f"{XSSColors.SUCCESS}✅ {system['name']}: Трафик выглядит нормальным{XSSColors.RESET}")

        if detected:
            return {
                'success': False,
                'detected': True,
                'message': 'Тестовая передача обнаружена системами мониторинга',
                'risk_increase': 20
            }
        else:
            print(f"{XSSColors.SUCCESS}✅ Тест прошел успешно. Данные переданы незаметно.{XSSColors.RESET}")
            return {
                'success': True,
                'message': 'Тестовая передача успешна',
                'risk_increase': total_suspicion
            }

    def _final_transmission(self, operation_state, monitoring_systems, secret_data):
        """Финальная передача секретных данных"""
        method = operation_state['selected_method']
        base_risk = operation_state['detection_risk']

        print(f"\n{XSSColors.WARNING}🚀 НАЧАЛО ПЕРЕДАЧИ СЕКРЕТНЫХ ДАННЫХ{XSSColors.RESET}")
        print(f"Метод: {self._get_method_info(method)['name']}")
        print(f"Размер данных: {len(secret_data)} байт")

        time.sleep(2)

        # Имитация процесса передачи
        steps = [
            "Инициализация канала связи...",
            "Подготовка данных для сокрытия...",
            "Внедрение данных в носитель...",
            "Проверка целостности...",
            "Отправка данных..."
        ]

        for step in steps:
            print(f"{XSSColors.INFO}📡 {step}{XSSColors.RESET}")
            time.sleep(random.uniform(0.5, 1.5))

        # Финальная проверка обнаружения (более строгая)
        detected = False
        detection_details = []

        for system in monitoring_systems:
            # Увеличиваем шанс обнаружения для финальной передачи
            detection_chance = self._calculate_detection_chance(method, system, base_risk) * 1.3

            if random.random() * 100 < detection_chance:
                detected = True
                detection_details.append({
                    'system': system['name'],
                    'method': random.choice(system['detection_methods']),
                    'confidence': random.randint(75, 95)
                })
                break

        if detected:
            print(f"\n{XSSColors.DANGER}🚨 ОБНАРУЖЕНИЕ! ОПЕРАЦИЯ КОМПРОМЕТИРОВАНА!{XSSColors.RESET}")
            for detail in detection_details:
                print(f"   {detail['system']}: {detail['method']} (уверенность: {detail['confidence']}%)")

            return {
                'success': False,
                'failure_reason': 'detected',
                'detection_details': detection_details
            }
        else:
            print(f"\n{XSSColors.SUCCESS}🎉 ДАННЫЕ ПЕРЕДАНЫ УСПЕШНО!{XSSColors.RESET}")
            return {'success': True}

    def _calculate_detection_chance(self, method, system, base_risk):
        """Рассчитывает шанс обнаружения метода системой"""
        method_info = self._get_method_info(method)

        # Базовый шанс обнаружения системы
        base_detection = system['effectiveness']

        # Модификатор на основе скрытности метода
        stealth_modifier = {
            'very_low': 30,
            'low': 15,
            'medium': 0,
            'high': -20,
            'very_high': -35
        }

        # Совместимость метода с типом системы
        compatibility_bonus = 0
        if system['type'] == 'stego_detection' and method in ['lsb_image', 'audio_spectral']:
            compatibility_bonus = 25  # Стего-сканер лучше детектирует стеганографию
        elif system['type'] == 'network_analysis' and method in ['dns_timing', 'tcp_timestamp', 'icmp_echo']:
            compatibility_bonus = 20  # Сетевой анализ лучше детектирует сетевые каналы
        elif system['type'] == 'behavior_analysis' and method in ['file_slack', 'blockchain_meta']:
            compatibility_bonus = 15  # Поведенческий анализ детектирует необычную файловую активность

        stealth_penalty = stealth_modifier.get(method_info['stealth'], 0)

        final_chance = base_detection + stealth_penalty + compatibility_bonus + base_risk - 50
        return max(5, min(95, final_chance))

    def _show_operation_status(self, operation_state, remaining_time):
        """Показывает статус операции"""
        method_name = "Не выбран"
        if operation_state['selected_method']:
            method_name = self._get_method_info(operation_state['selected_method'])['name']

        status_icons = {
            'selected_method': "✅" if operation_state['selected_method'] else "❌",
            'configured': "✅" if operation_state['configured'] else "❌",
            'test_passed': "✅" if operation_state['test_passed'] else "❌"
        }

        risk_color = self._get_risk_color_by_level(operation_state['detection_risk'])

        print(f"\n{XSSColors.INFO}📊 СТАТУС ОПЕРАЦИИ:{XSSColors.RESET}")
        print(f"   Метод: {status_icons['selected_method']} {method_name}")
        print(f"   Настройка: {status_icons['configured']}")
        print(f"   Тест: {status_icons['test_passed']}")
        print(f"   Риск обнаружения: {risk_color}{operation_state['detection_risk']}%{XSSColors.RESET}")
        print(f"   Попыток осталось: {operation_state['max_attempts'] - operation_state['attempts']}")
        print(f"   ⏰ Время: {remaining_time:.0f}s")

    def _show_detailed_status(self, operation_state, mission):
        """Показывает детальный статус операции"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ ДЕТАЛЬНЫЙ СТАТУС ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Статус выбранного метода
        if operation_state['selected_method']:
            method_info = self._get_method_info(operation_state['selected_method'])
            print(f"\n{XSSColors.WARNING}🔧 ВЫБРАННЫЙ МЕТОД:{XSSColors.RESET}")
            print(f"   Название: {method_info['name']}")
            print(f"   Скрытность: {self._get_stealth_rating(method_info['stealth'])}")
            print(f"   Пропускная способность: {method_info['capacity']}")
            print(f"   Описание: {method_info['description']}")

        # Анализ угроз
        print(f"\n{XSSColors.ERROR}⚠️ АНАЛИЗ УГРОЗ:{XSSColors.RESET}")
        for system in mission['monitoring_systems']:
            if operation_state['selected_method']:
                threat_level = self._calculate_detection_chance(
                    operation_state['selected_method'],
                    system,
                    operation_state['detection_risk']
                )
                threat_color = self._get_risk_color_by_level(threat_level)
                print(f"   {system['name']}: {threat_color}{threat_level:.0f}% угроза{XSSColors.RESET}")
            else:
                print(f"   {system['name']}: Анализ недоступен")

        # Рекомендации
        print(f"\n{XSSColors.SUCCESS}💡 РЕКОМЕНДАЦИИ:{XSSColors.RESET}")
        if not operation_state['selected_method']:
            print(f"   • Выберите метод сокрытия данных")
        elif not operation_state['configured']:
            print(f"   • Настройте выбранный метод")
        elif not operation_state['test_passed']:
            print(f"   • Проведите тестовую передачу")
        else:
            print(f"   • Готово к передаче секретных данных")

        if operation_state['detection_risk'] > 60:
            print(f"   • Высокий риск обнаружения - рассмотрите другой метод")

    def _evaluate_operation(self, operation_state, mission, time_taken, success, failure_reason):
        """Оценивает результаты операции"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ РЕЗУЛЬТАТЫ ОПЕРАЦИИ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        # Подсчет очков
        base_score = 100 if success else 0
        time_bonus = max(0, 50 - int(time_taken / 6))  # Бонус за скорость
        stealth_bonus = max(0, 100 - operation_state['detection_risk'])  # Бонус за скрытность
        attempts_penalty = (operation_state['attempts']) * 15  # Штраф за попытки

        total_score = base_score + time_bonus + stealth_bonus - attempts_penalty

        print(f"\n{XSSColors.INFO}📊 ПОДСЧЕТ ОЧКОВ:{XSSColors.RESET}")
        if success:
            print(f"   Успешная передача: +{base_score}")
        if time_bonus > 0:
            print(f"   Бонус за скорость: +{time_bonus}")
        print(f"   Бонус за скрытность: +{stealth_bonus}")
        if attempts_penalty > 0:
            print(f"   Штраф за обнаружения: -{attempts_penalty}")

        print(f"\n{XSSColors.BRIGHT_GREEN}🏆 ИТОГО: {total_score} очков{XSSColors.RESET}")

        if success:
            self._show_operation_success(mission, operation_state, total_score, time_taken)
        else:
            self._show_operation_failure(mission, failure_reason, total_score)

        return success

    def _show_operation_success(self, mission, operation_state, score, time_taken):
        """Показывает экран успешной операции"""
        audio_system.play_sound("minigame_win")

        print(f"\n{XSSColors.SUCCESS}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}║                🎉 ОПЕРАЦИЯ ВЫПОЛНЕНА! 🎉                     ║{XSSColors.RESET}")
        print(f"{XSSColors.SUCCESS}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        secret_data = mission['secret_data']
        method_info = self._get_method_info(operation_state['selected_method'])

        print(f"\n{XSSColors.SUCCESS}📡 Секретные данные переданы успешно!{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🔒 Тип данных: {secret_data['description']}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}📦 Размер: {secret_data['bytes']} байт{XSSColors.RESET}")
        print(f"{XSSColors.INFO}🛠️ Метод: {method_info['name']}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}⏱️ Время операции: {time_taken:.1f} секунд{XSSColors.RESET}")
        print(f"{XSSColors.BRIGHT_GREEN}🏆 Итоговый счет: {score} очков{XSSColors.RESET}")

        # Определяем ранг оператора
        if score >= 180 and time_taken < 60:
            rank = f"{XSSColors.DANGER}🌟 МАСТЕР СТЕГАНОГРАФИИ{XSSColors.RESET}"
        elif score >= 150:
            rank = f"{XSSColors.SUCCESS}💎 ЭКСПЕРТ ПО СКРЫТЫМ КАНАЛАМ{XSSColors.RESET}"
        elif score >= 120:
            rank = f"{XSSColors.WARNING}🔧 СПЕЦИАЛИСТ ПО СОКРЫТИЮ{XSSColors.RESET}"
        elif score >= 90:
            rank = f"{XSSColors.INFO}🎯 АГЕНТ-НОВИЧОК{XSSColors.RESET}"
        else:
            rank = f"{XSSColors.LIGHT_GRAY}📚 СТАЖЕР{XSSColors.RESET}"

        print(f"\n🏅 Ваш ранг: {rank}")

        # Показываем какие системы были обмануты
        print(f"\n{XSSColors.SUCCESS}🕵️ ОБМАНУТЫЕ СИСТЕМЫ:{XSSColors.RESET}")
        for system in mission['monitoring_systems']:
            print(f"   ✅ {system['name']} - не обнаружил передачу")

        print(f"\n{XSSColors.INFO}📈 РАЗВИТЫЕ НАВЫКИ:{XSSColors.RESET}")
        skills = [
            "Техники стеганографии",
            "Обход систем мониторинга",
            "Скрытная передача данных",
            "Анализ сетевого трафика",
            "Противодействие детектированию"
        ]
        for skill in skills:
            print(f"   • {skill}")

    def _show_operation_failure(self, mission, failure_reason, score):
        """Показывает экран неудачной операции"""
        audio_system.play_sound("minigame_lose")

        print(f"\n{XSSColors.ERROR}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}║                    ❌ ОПЕРАЦИЯ ПРОВАЛЕНА ❌                  ║{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        failure_messages = {
            'detected': "🚨 Передача данных обнаружена системами мониторинга",
            'timeout': "⏰ Время операции истекло",
            'unknown': "❓ Неизвестная ошибка операции"
        }

        message = failure_messages.get(failure_reason, failure_messages['unknown'])
        print(f"\n{XSSColors.ERROR}{message}{XSSColors.RESET}")
        print(f"{XSSColors.ERROR}📉 Итоговый счет: {score} очков{XSSColors.RESET}")

        # Показываем последствия провала
        print(f"\n{XSSColors.WARNING}⚠️ ПОСЛЕДСТВИЯ ПРОВАЛА:{XSSColors.RESET}")
        consequences = [
            "Компрометация агентской сети",
            "Усиление систем безопасности",
            "Расследование службы безопасности",
            "Потеря доверия руководства"
        ]

        for consequence in random.sample(consequences, 2):
            print(f"   • {consequence}")

        print(f"\n{XSSColors.INFO}💡 РЕКОМЕНДАЦИИ ДЛЯ СЛЕДУЮЩЕЙ ОПЕРАЦИИ:{XSSColors.RESET}")
        recommendations = [
            "Изучите характеристики систем мониторинга",
            "Выбирайте методы с более высокой скрытностью",
            "Тщательно настраивайте параметры передачи",
            "Проводите больше тестов перед финальной передачей",
            "Учитывайте временные ограничения операции"
        ]

        for rec in recommendations[:3]:
            print(f"   • {rec}")

    def _show_operation_help(self):
        """Показывает детальную справку по операциям"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}                📖 РУКОВОДСТВО АГЕНТА ПО СКРЫТЫМ КАНАЛАМ      {XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.WARNING}🎯 ЦЕЛЬ МИССИИ:{XSSColors.RESET}")
        print(f"   Передать секретные данные через контролируемую сеть так, чтобы")
        print(f"   системы мониторинга не обнаружили факт передачи конфиденциальной")
        print(f"   информации. Используйте техники стеганографии и скрытых каналов.")

        print(f"\n{XSSColors.SUCCESS}📋 ОСНОВНЫЕ КОМАНДЫ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}use <method_id>{XSSColors.RESET}")
        print(f"      Выбрать метод сокрытия данных из доступного списка")
        print(f"      Пример: {XSSColors.LIGHT_GRAY}use 1{XSSColors.RESET} (выбрать LSB Steganography)")
        print(f"      Пример: {XSSColors.LIGHT_GRAY}use 3{XSSColors.RESET} (выбрать DNS Timing)")

        print(f"\n   {XSSColors.BRIGHT_GREEN}configure <параметр1> <параметр2> ...{XSSColors.RESET}")
        print(f"      Настроить параметры выбранного метода")
        print(f"      Каждый метод имеет свои уникальные настройки")
        print(f"      Пример: {XSSColors.LIGHT_GRAY}configure 2 png{XSSColors.RESET} (LSB: 2 бита, PNG)")
        print(
            f"      Пример: {XSSColors.LIGHT_GRAY}configure variable 5{XSSColors.RESET} (DNS: переменные задержки, 5 доменов)")

        print(f"\n   {XSSColors.BRIGHT_GREEN}test{XSSColors.RESET}")
        print(f"      Провести тестовую передачу перед основной операцией")
        print(f"      Позволяет оценить риск обнаружения без компрометации")
        print(f"      ⚠️ Обязательно перед финальной передачей!")

        print(f"\n   {XSSColors.BRIGHT_GREEN}transmit{XSSColors.RESET}")
        print(f"      Передать секретные данные (только после успешного теста)")
        print(f"      Финальная операция - нет возможности отменить")

        print(f"\n   {XSSColors.BRIGHT_GREEN}status{XSSColors.RESET}")
        print(f"      Показать детальный статус операции и анализ угроз")
        print(f"      Включает: выбранный метод, настройки, риски, рекомендации")

        print(f"\n   {XSSColors.BRIGHT_GREEN}abort{XSSColors.RESET}")
        print(f"      Прервать операцию (засчитывается как провал)")

        print(f"\n{XSSColors.WARNING}🔧 ПОШАГОВАЯ ПРОЦЕДУРА:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}1. АНАЛИЗ ОБСТАНОВКИ{XSSColors.RESET}")
        print(f"      • Изучите системы мониторинга в брифинге")
        print(f"      • Определите их типы и эффективность")
        print(f"      • Оцените доступный легитимный трафик")

        print(f"\n   {XSSColors.BRIGHT_GREEN}2. ВЫБОР МЕТОДА{XSSColors.RESET}")
        print(f"      • Выберите метод командой {XSSColors.BRIGHT_GREEN}use <id>{XSSColors.RESET}")
        print(f"      • Учитывайте совместимость с системами мониторинга")
        print(f"      • Балансируйте скрытность и пропускную способность")

        print(f"\n   {XSSColors.BRIGHT_GREEN}3. НАСТРОЙКА ПАРАМЕТРОВ{XSSColors.RESET}")
        print(f"      • Используйте {XSSColors.BRIGHT_GREEN}configure{XSSColors.RESET} без параметров для справки")
        print(f"      • Настройте метод для минимизации риска обнаружения")
        print(f"      • Более консервативные настройки = меньше риска")

        print(f"\n   {XSSColors.BRIGHT_GREEN}4. ТЕСТИРОВАНИЕ{XSSColors.RESET}")
        print(f"      • Обязательно выполните {XSSColors.BRIGHT_GREEN}test{XSSColors.RESET} перед передачей")
        print(f"      • При неудаче - измените метод или настройки")
        print(f"      • Каждая неудача увеличивает подозрительность")

        print(f"\n   {XSSColors.BRIGHT_GREEN}5. ФИНАЛЬНАЯ ПЕРЕДАЧА{XSSColors.RESET}")
        print(f"      • Выполните {XSSColors.BRIGHT_GREEN}transmit{XSSColors.RESET} только после успешного теста")
        print(f"      • Следите за оставшимся временем")
        print(f"      • При обнаружении - миссия провалена")

        print(f"\n{XSSColors.INFO}🛠️ ДЕТАЛЬНОЕ ОПИСАНИЕ ВСЕХ ПАРАМЕТРОВ:{XSSColors.RESET}")

        print(f"\n   {XSSColors.INFO}🖼️ LSB STEGANOGRAPHY{XSSColors.RESET}")
        print(f"      Команда: {XSSColors.BRIGHT_GREEN}configure <bit_depth> <image_type>{XSSColors.RESET}")
        print(f"      ")
        print(f"      {XSSColors.WARNING}bit_depth (глубина битов):{XSSColors.RESET}")
        print(f"        1 = 1 младший бит (МАКСИМАЛЬНАЯ СКРЫТНОСТЬ, медленно)")
        print(f"        2 = 2 младших бита (баланс скрытности и скорости)")
        print(f"        3 = 3 младших бита (быстро, но более заметно)")
        print(f"      ")
        print(f"      {XSSColors.WARNING}image_type (формат изображения):{XSSColors.RESET}")
        print(f"        jpg = JPEG (сжатый, может исказить данные)")
        print(f"        png = PNG (без потерь, РЕКОМЕНДУЕТСЯ)")
        print(f"        bmp = BMP (большой размер, подозрительно)")
        print(f"      ")
        print(f"      {XSSColors.SUCCESS}Примеры:{XSSColors.RESET}")
        print(f"        {XSSColors.LIGHT_GRAY}configure 1 png{XSSColors.RESET} - максимальная скрытность")
        print(f"        {XSSColors.LIGHT_GRAY}configure 2 png{XSSColors.RESET} - рекомендуемые настройки")
        print(f"        {XSSColors.LIGHT_GRAY}configure 3 jpg{XSSColors.RESET} - быстро, но рискованно")

        print(f"\n   {XSSColors.INFO}📝 TEXT SPACING{XSSColors.RESET}")
        print(f"      Команда: {XSSColors.BRIGHT_GREEN}configure <spacing_type> <document_format>{XSSColors.RESET}")
        print(f"      ")
        print(f"      {XSSColors.WARNING}spacing_type (тип интервалов):{XSSColors.RESET}")
        print(f"        character = между символами (заметно при чтении)")
        print(f"        word = между словами (средняя заметность)")
        print(f"        line = между строками (НЕЗАМЕТНО, рекомендуется)")
        print(f"      ")
        print(f"      {XSSColors.WARNING}document_format (формат документа):{XSSColors.RESET}")
        print(f"        txt = обычный текст (может выглядеть странно)")
        print(f"        doc = Word документ (нормально выглядит)")
        print(f"        pdf = PDF файл (профессионально)")
        print(f"      ")
        print(f"      {XSSColors.SUCCESS}Примеры:{XSSColors.RESET}")
        print(f"        {XSSColors.LIGHT_GRAY}configure line pdf{XSSColors.RESET} - самый незаметный")
        print(f"        {XSSColors.LIGHT_GRAY}configure word doc{XSSColors.RESET} - хороший баланс")

        print(f"\n   {XSSColors.INFO}🌐 DNS TIMING{XSSColors.RESET}")
        print(f"      Команда: {XSSColors.BRIGHT_GREEN}configure <delay_pattern> <domain_count>{XSSColors.RESET}")
        print(f"      ")
        print(f"      {XSSColors.WARNING}delay_pattern (паттерн задержек):{XSSColors.RESET}")
        print(f"        fixed = одинаковые интервалы (ЛЕГКО ОБНАРУЖИТЬ)")
        print(f"        variable = случайные интервалы (средняя защита)")
        print(f"        fibonacci = последовательность Фибоначчи (ТРУДНО ОБНАРУЖИТЬ)")
        print(f"      ")
        print(f"      {XSSColors.WARNING}domain_count (количество доменов):{XSSColors.RESET}")
        print(f"        3 = 3 домена (быстро, но паттерн заметен)")
        print(f"        5 = 5 доменов (ОПТИМАЛЬНО)")
        print(f"        10 = 10 доменов (очень скрытно, но медленно)")
        print(f"      ")
        print(f"      {XSSColors.SUCCESS}Примеры:{XSSColors.RESET}")
        print(f"        {XSSColors.LIGHT_GRAY}configure fibonacci 5{XSSColors.RESET} - лучший вариант")
        print(f"        {XSSColors.LIGHT_GRAY}configure variable 3{XSSColors.RESET} - быстрый вариант")

        print(f"\n   {XSSColors.INFO}📡 TCP TIMESTAMP{XSSColors.RESET}")
        print(f"      Команда: {XSSColors.BRIGHT_GREEN}configure <timestamp_field> <encoding_rate>{XSSColors.RESET}")
        print(f"      ")
        print(f"      {XSSColors.WARNING}timestamp_field (поле для сокрытия):{XSSColors.RESET}")
        print(f"        options = в поле опций TCP (БЕЗОПАСНЕЕ)")
        print(f"        sequence = в номере последовательности (рискованно)")
        print(f"        ack = в номере подтверждения (ОЧЕНЬ РИСКОВАННО)")
        print(f"      ")
        print(f"      {XSSColors.WARNING}encoding_rate (скорость кодирования):{XSSColors.RESET}")
        print(f"        1 = 1 бит на пакет (медленно, но СКРЫТНО)")
        print(f"        2 = 2 бита на пакет (баланс)")
        print(f"        4 = 4 бита на пакет (быстро, но ЗАМЕТНО)")
        print(f"      ")
        print(f"      {XSSColors.SUCCESS}Примеры:{XSSColors.RESET}")
        print(f"        {XSSColors.LIGHT_GRAY}configure options 1{XSSColors.RESET} - самый безопасный")
        print(f"        {XSSColors.LIGHT_GRAY}configure options 2{XSSColors.RESET} - рекомендуемый")

        print(f"\n   {XSSColors.INFO}📶 ICMP ECHO{XSSColors.RESET}")
        print(f"      Команда: {XSSColors.BRIGHT_GREEN}configure <payload_size> <interval>{XSSColors.RESET}")
        print(f"      ")
        print(f"      {XSSColors.WARNING}payload_size (размер данных в пакете):{XSSColors.RESET}")
        print(f"        32 = 32 байта (стандартный ping, НЕЗАМЕТНО)")
        print(f"        64 = 64 байта (немного больше обычного)")
        print(f"        128 = 128 байт (ПОДОЗРИТЕЛЬНО большой)")
        print(f"      ")
        print(f"      {XSSColors.WARNING}interval (интервал между пакетами в сек.):{XSSColors.RESET}")
        print(f"        1 = 1 секунда (частые пинги, ПОДОЗРИТЕЛЬНО)")
        print(f"        2 = 2 секунды (НОРМАЛЬНАЯ частота)")
        print(f"        5 = 5 секунд (редко, незаметно, но медленно)")
        print(f"      ")
        print(f"      {XSSColors.SUCCESS}Примеры:{XSSColors.RESET}")
        print(f"        {XSSColors.LIGHT_GRAY}configure 32 2{XSSColors.RESET} - стандартные настройки")
        print(f"        {XSSColors.LIGHT_GRAY}configure 32 5{XSSColors.RESET} - максимально незаметно")

        print(f"\n   {XSSColors.INFO}💾 FILE SLACK SPACE{XSSColors.RESET}")
        print(f"      Команда: {XSSColors.BRIGHT_GREEN}configure <file_type> <cluster_size>{XSSColors.RESET}")
        print(f"      ")
        print(f"      {XSSColors.WARNING}file_type (тип файла):{XSSColors.RESET}")
        print(f"        exe = исполняемые файлы (могут проверяться антивирусом)")
        print(f"        dll = библиотеки (МЕНЕЕ ПОДОЗРИТЕЛЬНО)")
        print(f"        sys = системные файлы (очень скрытно, но рискованно)")
        print(f"      ")
        print(f"      {XSSColors.WARNING}cluster_size (размер кластера диска):{XSSColors.RESET}")
        print(f"        4096 = 4KB кластеры (мало места, но незаметно)")
        print(f"        8192 = 8KB кластеры (ОПТИМАЛЬНО)")
        print(f"        16384 = 16KB кластеры (много места, но подозрительно)")
        print(f"      ")
        print(f"      {XSSColors.SUCCESS}Примеры:{XSSColors.RESET}")
        print(f"        {XSSColors.LIGHT_GRAY}configure dll 8192{XSSColors.RESET} - лучший выбор")
        print(f"        {XSSColors.LIGHT_GRAY}configure sys 4096{XSSColors.RESET} - максимальная скрытность")

        print(f"\n   {XSSColors.INFO}₿ BLOCKCHAIN METADATA{XSSColors.RESET}")
        print(f"      Команда: {XSSColors.BRIGHT_GREEN}configure <blockchain> <transaction_type>{XSSColors.RESET}")
        print(f"      ")
        print(f"      {XSSColors.WARNING}blockchain (тип блокчейна):{XSSColors.RESET}")
        print(f"        bitcoin = Bitcoin (популярный, много транзакций)")
        print(f"        ethereum = Ethereum (умные контракты, ГИБКОСТЬ)")
        print(f"        monero = Monero (анонимный, МАКСИМАЛЬНАЯ СКРЫТНОСТЬ)")
        print(f"      ")
        print(f"      {XSSColors.WARNING}transaction_type (тип транзакции):{XSSColors.RESET}")
        print(f"        standard = обычная транзакция (простая, дешевая)")
        print(f"        multisig = мультиподпись (БОЛЬШЕ МЕСТА для данных)")
        print(f"        contract = смарт-контракт (максимум возможностей)")
        print(f"      ")
        print(f"      {XSSColors.SUCCESS}Примеры:{XSSColors.RESET}")
        print(f"        {XSSColors.LIGHT_GRAY}configure monero multisig{XSSColors.RESET} - максимальная анонимность")
        print(f"        {XSSColors.LIGHT_GRAY}configure bitcoin standard{XSSColors.RESET} - простой и дешевый")

        print(f"\n   {XSSColors.INFO}🎵 AUDIO SPECTRAL{XSSColors.RESET}")
        print(f"      Команда: {XSSColors.BRIGHT_GREEN}configure <frequency_range> <encoding_method>{XSSColors.RESET}")
        print(f"      ")
        print(f"      {XSSColors.WARNING}frequency_range (частотный диапазон):{XSSColors.RESET}")
        print(f"        low = низкие частоты (МЕНЕЕ ЗАМЕТНО)")
        print(f"        mid = средние частоты (баланс)")
        print(f"        high = высокие частоты (заметно при анализе)")
        print(f"      ")
        print(f"      {XSSColors.WARNING}encoding_method (метод кодирования):{XSSColors.RESET}")
        print(f"        lsb = младшие биты (простой, может быть обнаружен)")
        print(f"        phase = фазовое кодирование (СЛОЖНЕЕ ОБНАРУЖИТЬ)")
        print(f"        spread = спектральное распределение (МАКСИМАЛЬНАЯ СКРЫТНОСТЬ)")
        print(f"      ")
        print(f"      {XSSColors.SUCCESS}Примеры:{XSSColors.RESET}")
        print(f"        {XSSColors.LIGHT_GRAY}configure low spread{XSSColors.RESET} - самый скрытный")
        print(f"        {XSSColors.LIGHT_GRAY}configure mid phase{XSSColors.RESET} - хороший баланс")

        print(f"\n{XSSColors.ERROR}⚠️ СИСТЕМА РИСКОВ:{XSSColors.RESET}")
        print(f"   {XSSColors.WARNING}Риск обнаружения рассчитывается по формуле:{XSSColors.RESET}")
        print(f"   • Базовая эффективность системы: 60-95%")
        print(f"   • Модификатор скрытности метода: -35% до +30%")
        print(f"   • Бонус совместимости системы: +0% до +25%")
        print(f"   • Влияние ваших настроек: ±15%")
        print(f"   • Накопленный риск от предыдущих действий")

        print(f"\n   {XSSColors.WARNING}Критические пороги:{XSSColors.RESET}")
        print(f"   • {XSSColors.SUCCESS}0-30%{XSSColors.RESET} - Низкий риск (безопасно)")
        print(f"   • {XSSColors.WARNING}31-50%{XSSColors.RESET} - Умеренный риск (осторожно)")
        print(f"   • {XSSColors.ERROR}51-70%{XSSColors.RESET} - Высокий риск (опасно)")
        print(f"   • {XSSColors.DANGER}71%+{XSSColors.RESET} - Критический риск (почти гарантированное обнаружение)")

        print(f"\n{XSSColors.SUCCESS}💡 СТРАТЕГИЧЕСКИЕ СОВЕТЫ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}📊 АНАЛИЗ СИСТЕМ МОНИТОРИНГА:{XSSColors.RESET}")
        print(f"   • Firewall DPI → избегайте сетевых методов (DNS, TCP, ICMP)")
        print(f"   • Steganography Scanner → избегайте LSB и Audio")
        print(f"   • Network Analyzer → избегайте всех сетевых каналов")
        print(f"   • Behavioral Monitor → избегайте необычных файловых операций")

        print(f"\n   {XSSColors.BRIGHT_GREEN}🎯 ВЫБОР МЕТОДА ПО СИТУАЦИИ:{XSSColors.RESET}")
        print(f"   • Много стего-сканеров → используйте File Slack или Blockchain")
        print(f"   • Сильный сетевой мониторинг → используйте Text Spacing")
        print(f"   • Ограниченное время → выбирайте LSB или Audio (быстрые)")
        print(f"   • Максимальная скрытность → только Blockchain или File Slack")

        print(f"\n   {XSSColors.BRIGHT_GREEN}⚙️ ОПТИМИЗАЦИЯ НАСТРОЕК:{XSSColors.RESET}")
        print(f"   • Меньше битов/частота = меньше риска")
        print(f"   • Переменные паттерны лучше фиксированных")
        print(f"   • Стандартные форматы менее подозрительны")
        print(f"   • Больше доменов/узлов = больше маскировка")

        print(f"\n   {XSSColors.BRIGHT_GREEN}⏰ УПРАВЛЕНИЕ ВРЕМЕНЕМ:{XSSColors.RESET}")
        print(f"   • Следите за таймером - операция ограничена по времени")
        print(f"   • Быстрая настройка дает бонус к очкам")
        print(f"   • При критическом времени используйте знакомые методы")

        print(f"\n{XSSColors.INFO}🏆 СИСТЕМА ОЦЕНКИ:{XSSColors.RESET}")
        print(f"   {XSSColors.BRIGHT_GREEN}Очки начисляются за:{XSSColors.RESET}")
        print(f"   • Успешную передачу: +100 очков")
        print(f"   • Скорость операции: до +50 очков")
        print(f"   • Низкий риск обнаружения: до +100 очков")
        print(f"   • Штраф за неудачи: -15 очков за попытку")

        print(f"\n   {XSSColors.BRIGHT_GREEN}Ранги агентов:{XSSColors.RESET}")
        print(f"   • 180+ очков: 🌟 Мастер стеганографии")
        print(f"   • 150+ очков: 💎 Эксперт по скрытым каналам")
        print(f"   • 120+ очков: 🔧 Специалист по сокрытию")
        print(f"   • 90+ очков: 🎯 Агент-новичок")
        print(f"   • <90 очков: 📚 Стажер")

        print(f"\n{XSSColors.WARNING}🚨 ЧАСТЫЕ ОШИБКИ НОВИЧКОВ:{XSSColors.RESET}")
        print(f"   ❌ Игнорирование типов систем мониторинга")
        print(f"   ❌ Попытка передачи без тестирования")
        print(f"   ❌ Использование максимальных настроек (высокий риск)")
        print(f"   ❌ Выбор неподходящего метода для ситуации")
        print(f"   ❌ Невнимание к накапливающемуся риску")

        print(f"\n{XSSColors.SUCCESS}✅ ПРИЗНАКИ МАСТЕРСТВА:{XSSColors.RESET}")
        print(f"   ✅ Анализ систем перед выбором метода")
        print(f"   ✅ Консервативные настройки для снижения риска")
        print(f"   ✅ Обязательное тестирование перед передачей")
        print(f"   ✅ Адаптация стратегии под каждую миссию")
        print(f"   ✅ Баланс между скоростью и безопасностью")

        print(f"\n{XSSColors.BRIGHT_GREEN}🎮 ПРИМЕР УСПЕШНОЙ ОПЕРАЦИИ:{XSSColors.RESET}")
        print(f"   {XSSColors.LIGHT_GRAY}# Ситуация: 2 стего-сканера, 1 сетевой анализатор{XSSColors.RESET}")
        print(
            f"   {XSSColors.LIGHT_GRAY}use 6{XSSColors.RESET}                     # File Slack (избегаем стего-сканеров)")
        print(f"   {XSSColors.LIGHT_GRAY}configure dll 8192{XSSColors.RESET}       # Консервативные настройки")
        print(f"   {XSSColors.LIGHT_GRAY}test{XSSColors.RESET}                      # Проверяем безопасность")
        print(f"   {XSSColors.LIGHT_GRAY}transmit{XSSColors.RESET}                  # Передаем данные")
        print(f"   {XSSColors.SUCCESS}# Результат: 165 очков, ранг 'Эксперт'{XSSColors.RESET}")

        input(f"\n{XSSColors.PROMPT}Нажмите Enter для возврата к операции...{XSSColors.RESET}")

    # Вспомогательные методы для генерации данных

    def _generate_secret_code(self, length):
        """Генерирует секретный код"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(random.choices(chars, k=length))

    def _generate_coordinates(self):
        """Генерирует координаты"""
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        return f"{lat:.4f},{lon:.4f}"

    def _generate_time_code(self):
        """Генерирует временной код"""
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"

    def _generate_operation_plan(self):
        """Генерирует план операции"""
        operations = ["INFILTRATE", "EXTRACT", "OBSERVE", "NEUTRALIZE"]
        targets = ["ALPHA", "BRAVO", "CHARLIE", "DELTA"]
        times = ["0300", "1500", "2100", "0600"]

        op = random.choice(operations)
        target = random.choice(targets)
        time_code = random.choice(times)

        return f"OP:{op}|TGT:{target}|TIME:{time_code}|AUTH:PHANTOM"

    def _generate_intelligence_report(self):
        """Генерирует разведывательный отчет"""
        agencies = ["CIA", "FSB", "MSS", "MOSSAD"]
        statuses = ["CONFIRMED", "PROBABLE", "POSSIBLE"]
        threats = ["HIGH", "MEDIUM", "LOW"]

        agency = random.choice(agencies)
        status = random.choice(statuses)
        threat = random.choice(threats)
        asset_id = self._generate_secret_code(6)

        return f"INTEL:{agency}|STATUS:{status}|THREAT:{threat}|ASSET:{asset_id}|CLASS:TS/SCI"

    def _get_method_info(self, method):
        """Возвращает информацию о методе сокрытия"""
        methods = {
            'lsb_image': {
                'name': '🖼️ LSB Steganography',
                'description': 'Сокрытие данных в младших битах изображений',
                'stealth': 'medium',
                'capacity': 'Высокая'
            },
            'text_spacing': {
                'name': '📝 Text Spacing',
                'description': 'Использование интервалов в тексте для кодирования',
                'stealth': 'high',
                'capacity': 'Низкая'
            },
            'dns_timing': {
                'name': '🌐 DNS Timing',
                'description': 'Кодирование в интервалах DNS-запросов',
                'stealth': 'medium',
                'capacity': 'Средняя'
            },
            'tcp_timestamp': {
                'name': '📡 TCP Timestamp',
                'description': 'Использование полей временных меток TCP',
                'stealth': 'low',
                'capacity': 'Средняя'
            },
            'icmp_echo': {
                'name': '📶 ICMP Echo',
                'description': 'Сокрытие в ICMP ping-пакетах',
                'stealth': 'low',
                'capacity': 'Низкая'
            },
            'file_slack': {
                'name': '💾 File Slack Space',
                'description': 'Использование неиспользуемого пространства файлов',
                'stealth': 'very_high',
                'capacity': 'Средняя'
            },
            'blockchain_meta': {
                'name': '₿ Blockchain Metadata',
                'description': 'Сокрытие в метаданных блокчейн-транзакций',
                'stealth': 'very_high',
                'capacity': 'Очень низкая'
            },
            'audio_spectral': {
                'name': '🎵 Audio Spectral',
                'description': 'Спектральное сокрытие в аудиофайлах',
                'stealth': 'high',
                'capacity': 'Высокая'
            }
        }
        return methods.get(method, {'name': 'Unknown', 'description': 'Unknown method', 'stealth': 'low',
                                    'capacity': 'Unknown'})

    def _get_stealth_rating(self, stealth_level):
        """Возвращает рейтинг скрытности с цветом"""
        ratings = {
            'very_low': f"{XSSColors.DANGER}★☆☆☆☆ Очень низкая{XSSColors.RESET}",
            'low': f"{XSSColors.ERROR}★★☆☆☆ Низкая{XSSColors.RESET}",
            'medium': f"{XSSColors.WARNING}★★★☆☆ Средняя{XSSColors.RESET}",
            'high': f"{XSSColors.SUCCESS}★★★★☆ Высокая{XSSColors.RESET}",
            'very_high': f"{XSSColors.BRIGHT_GREEN}★★★★★ Очень высокая{XSSColors.RESET}"
        }
        return ratings.get(stealth_level, "Unknown")

    def _get_risk_color(self, risk_level):
        """Возвращает цвет для уровня риска"""
        colors = {
            'Низкий': XSSColors.SUCCESS,
            'Средний': XSSColors.WARNING,
            'Высокий': XSSColors.ERROR,
            'Критический': XSSColors.DANGER,
            'Экстремальный': XSSColors.DANGER
        }
        return colors.get(risk_level, XSSColors.INFO)

    def _get_risk_color_by_level(self, risk_percentage):
        """Возвращает цвет для процентного риска"""
        if risk_percentage <= 20:
            return XSSColors.SUCCESS
        elif risk_percentage <= 40:
            return XSSColors.WARNING
        elif risk_percentage <= 70:
            return XSSColors.ERROR
        else:
            return XSSColors.DANGER

    def _get_effectiveness_color(self, effectiveness):
        """Возвращает цвет для эффективности системы"""
        if effectiveness >= 80:
            return XSSColors.DANGER
        elif effectiveness >= 60:
            return XSSColors.ERROR
        elif effectiveness >= 40:
            return XSSColors.WARNING
        else:
            return XSSColors.SUCCESS

    def _get_suspicion_color(self, suspicion_level):
        """Возвращает цвет для уровня подозрительности"""
        colors = {
            'very_low': XSSColors.SUCCESS,
            'low': XSSColors.INFO,
            'medium': XSSColors.WARNING,
            'high': XSSColors.ERROR,
            'very_high': XSSColors.DANGER
        }
        return colors.get(suspicion_level, XSSColors.INFO)

class PortScanningGame(Minigame):
    """Мини-игра "Сканирование портов"."""
    def __init__(self):
        super().__init__(
            "Сканирование портов",
            "Определите открытый порт на целевом сервере",
            "scanning"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ СКАНИРОВАНИЕ ПОРТОВ ━━━━━━━━━━{XSSColors.RESET}")
        skill_level = game_state.get_skill(self.skill)

        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 3389: "RDP"
        }

        # Выбираем несколько портов, один из которых будет открыт
        possible_ports = random.sample(list(common_ports.keys()), k=min(len(common_ports), 5 + skill_level // 2))
        open_port = random.choice(possible_ports)

        print(f"{XSSColors.INFO}Вы сканируете целевой сервер. Определите, какой из перечисленных портов открыт.{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Введите номер открытого порта.{XSSColors.RESET}\n")

        for i, port in enumerate(possible_ports):
            status = f"{XSSColors.ERROR}ЗАКРЫТ{XSSColors.RESET}"
            if port == open_port and random.random() < 0.2 + skill_level * 0.05: # Шанс, что сканер покажет правильно
                status = f"{XSSColors.SUCCESS}ОТКРЫТ{XSSColors.RESET}"
            elif port != open_port and random.random() < 0.05: # Маленький шанс на ложное срабатывание
                 status = f"{XSSColors.WARNING}ОТКРЫТ (ЛОЖНОЕ){XSSColors.RESET}"
            print(f"   Порт {port} ({common_ports.get(port, 'Неизвестно')}): {status}")

        print("\n")
        attempts = 2
        while attempts > 0:
            try:
                user_guess = int(audio_system.get_input_with_sound(f"{XSSColors.PROMPT}Какой порт открыт? {XSSColors.RESET}"))

                if user_guess == open_port:
                    audio_system.play_sound("minigame_win")
                    print(f"\n{XSSColors.SUCCESS}🎉 УСПЕХ! Порт {open_port} действительно открыт!{XSSColors.RESET}")
                    return True
                else:
                    attempts -= 1
                    print(f"{XSSColors.ERROR}Неверно. Этот порт закрыт или является ложным срабатыванием. Попыток осталось: {attempts}.{XSSColors.RESET}")
            except ValueError:
                print(f"{XSSColors.ERROR}Введите число.{XSSColors.RESET}")

        audio_system.play_sound("minigame_lose")
        print(f"\n{XSSColors.ERROR}❌ Провал! Открытым был порт {open_port}.{XSSColors.RESET}")
        return False

class VulnerabilityAssessmentGame(Minigame):
    """Мини-игра "Оценка уязвимостей"."""
    def __init__(self):
        super().__init__(
            "Оценка уязвимостей",
            "Определите наиболее критическую уязвимость",
            "scanning"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ ОЦЕНКА УЯЗВИМОСТЕЙ ━━━━━━━━━━{XSSColors.RESET}")

        vulnerabilities = [
            {"name": "XSS (Межсайтовый скриптинг)", "severity": 6, "desc": "Позволяет внедрять вредоносный код в веб-страницы."},
            {"name": "SQL Injection", "severity": 8, "desc": "Позволяет манипулировать базой данных через ввод пользователя."},
            {"name": "Buffer Overflow (Переполнение буфера)", "severity": 9, "desc": "Позволяет выполнять произвольный код путем перезаписи памяти."},
            {"name": "Broken Authentication (Ненадежная аутентификация)", "severity": 7, "desc": "Слабости в механизмах входа в систему."},
            {"name": "DDoS Vulnerability", "severity": 5, "desc": "Система уязвима к атакам отказа в обслуживании."}
        ]

        # Выбираем случайные уязвимости для отображения
        num_vulns = min(len(vulnerabilities), 3 + game_state.get_skill(self.skill) // 2)
        displayed_vulns = random.sample(vulnerabilities, num_vulns)

        # Определяем наиболее критическую среди отображаемых
        most_critical = max(displayed_vulns, key=lambda x: x['severity'])

        print(f"{XSSColors.INFO}Перед вами список обнаруженных уязвимостей. Определите, какая из них является наиболее критической.{XSSColors.RESET}\n")

        for i, vuln in enumerate(displayed_vulns, 1):
            print(f"   {i}. {vuln['name']}: {vuln['desc']}")

        attempts = 2
        while attempts > 0:
            try:
                user_choice_idx = int(audio_system.get_input_with_sound(f"{XSSColors.PROMPT}Введите номер наиболее критической уязвимости: {XSSColors.RESET}"))

                if not (1 <= user_choice_idx <= num_vulns):
                    print(f"{XSSColors.ERROR}Неверный номер. Попробуйте еще раз.{XSSColors.RESET}")
                    continue

                user_guess_vuln = displayed_vulns[user_choice_idx - 1]

                if user_guess_vuln == most_critical:
                    audio_system.play_sound("minigame_win")
                    print(f"\n{XSSColors.SUCCESS}🎉 УСПЕХ! Вы правильно определили наиболее критическую уязвимость: {most_critical['name']} (Серьезность: {most_critical['severity']})!{XSSColors.RESET}")
                    return True
                else:
                    attempts -= 1
                    print(f"{XSSColors.ERROR}Неверно. Эта уязвимость не самая критическая. Попыток осталось: {attempts}.{XSSColors.RESET}")
                    print(f"Ее серьезность: {user_guess_vuln['severity']}. Попробуйте найти выше.{XSSColors.RESET}")
            except ValueError:
                print(f"{XSSColors.ERROR}Введите число.{XSSColors.RESET}")

        audio_system.play_sound("minigame_lose")
        print(f"\n{XSSColors.ERROR}❌ Провал! Наиболее критической уязвимостью была: {most_critical['name']} (Серьезность: {most_critical['severity']}).{XSSColors.RESET}")
        return False

class DataMiningGame(Minigame):
    """Мини-игра "Анализ данных"."""
    def __init__(self):
        super().__init__(
            "Анализ данных",
            "Найдите скрытую информацию в большом объеме текста",
            "scanning"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ АНАЛИЗ ДАННЫХ ━━━━━━━━━━{XSSColors.RESET}")

        target_info = random.choice([
            "Пароль: supersecret123",
            "Код доступа: G1B3R4N3T",
            "Координаты базы: 40.7128,-74.0060",
            "Имя агента: АЛИСА",
            "Криптоключ: 0xDEADBEEF"
        ])

        # Генерируем "шумный" текст
        junk_words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua"]
        noise_text = " ".join(random.choices(junk_words, k=50))

        # Вставляем целевую информацию в случайное место
        insert_pos = random.randint(0, len(noise_text) // 2)
        full_text = noise_text[:insert_pos] + target_info + noise_text[insert_pos:]

        print(f"{XSSColors.INFO}Перед вами массив данных. Ваша задача - найти конкретную скрытую информацию.{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Вам нужно найти строку, которая начинается с 'Пароль:', 'Код доступа:', 'Координаты базы:', 'Имя агента:' или 'Криптоключ:'.{XSSColors.RESET}\n")
        print(f"{XSSColors.LIGHT_GRAY}{full_text}{XSSColors.RESET}\n")

        attempts = 2
        while attempts > 0:
            user_guess = audio_system.get_input_with_sound(f"{XSSColors.PROMPT}Введите найденную информацию: {XSSColors.RESET}").strip()

            if user_guess == target_info:
                audio_system.play_sound("minigame_win")
                print(f"\n{XSSColors.SUCCESS}🎉 УСПЕХ! Вы успешно извлекли скрытую информацию: '{target_info}'!{XSSColors.RESET}")
                return True
            else:
                attempts -= 1
                print(f"{XSSColors.ERROR}Неверно. Информация не найдена или введена неточно. Попыток осталось: {attempts}.{XSSColors.RESET}")

        audio_system.play_sound("minigame_lose")
        print(f"\n{XSSColors.ERROR}❌ Провал! Искомая информация была: '{target_info}'.{XSSColors.RESET}")
        return False


class ForensicAnalysisGame(Minigame):
    """Мини-игра "Судебный анализ"""

    def __init__(self):
        super().__init__(
            "Судебный анализ",
            "Найдите 'улику' среди множества нерелевантных данных, анализируя различные типы источников.",
            "scanning"
        )
        self.clue_types = {
            "log": {
                "relevant": [
                    "Log entry: {timestamp} - Unusual admin login from {ip_address}",
                    "Log entry: {timestamp} - Critical error in system_core, process ID {pid}",
                    "Log entry: {timestamp} - Unauthorized access attempt on database 'users'",
                    "Log entry: {timestamp} - File deletion detected: {filename} by user 'sysadmin'"
                ],
                "irrelevant": [
                    "Log entry: {timestamp} - User 'guest' logged out.",
                    "Log entry: {timestamp} - System uptime check passed.",
                    "Log entry: {timestamp} - Routine backup completed successfully.",
                    "Log entry: {timestamp} - Info: CPU temperature nominal."
                ]
            },
            "email": {
                "relevant": [
                    "Email: 'URGENT - Transfer funds to offshore account {account_id}' from {sender}",
                    "Email: 'Confidential project details' attached in email from {sender}",
                    "Email: 'RE: Phase 3 Operations - Target coordinates: {coords}'",
                    "Email: 'Payment confirmation for illegal software license {license_id}'"
                ],
                "irrelevant": [
                    "Email: 'Reminder: Friday team meeting at 2 PM'",
                    "Email: 'Newsletter subscription confirmation'",
                    "Email: 'Your order #{order_id} has been shipped'",
                    "Email: 'Holiday greetings from company X'"
                ]
            },
            "file": {
                "relevant": [
                    "Deleted file: '{filename_secret}.doc' (recovered from Recycle Bin)",
                    "File metadata: '{filename_exec}' last accessed by unauthorized process '{process_id}'",
                    "Hidden file: '{hidden_filename}' found in system directory",
                    "Corrupted file: '{corrupted_filename}' with unusual size and timestamp"
                ],
                "irrelevant": [
                    "File: 'my_cat_pics_{num}.jpg'",
                    "File: 'report_{month}.pdf' (standard company report)",
                    "File: 'config.ini' (system default configuration)",
                    "File: 'memo_{date}.txt' (daily internal memo)"
                ]
            },
            "registry": {
                "relevant": [
                    "Registry key: HKLM\\Software\\MalwareCo\\backdoor_active (value: 1)",
                    "Registry key: HKCU\\Run\\PersistenceService (value: '{path_to_malware}.exe')",
                    "Registry key: HKLM\\System\\ControlSet001\\Services\\{service_name}\\Parameters\\BypassAuth (value: true)",
                    "Registry key: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StartupApproved\\Run\\{program_id}: '{random_path}'"
                ],
                "irrelevant": [
                    "Registry key: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                    "Registry key: HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
                    "Registry key: HKCU\\Control Panel\\Desktop",
                    "Registry key: HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager"
                ]
            },
            "network": {
                "relevant": [
                    "Network traffic: Large data transfer ({size}GB) to unknown IP {ip_address}",
                    "Network traffic: Encrypted tunnel established to {country_code} IP {ip_address}",
                    "Network traffic: Port scan detected from {source_ip} targeting port {port_num}",
                    "Network traffic: DNS exfiltration attempt for domain '{domain}'"
                ],
                "irrelevant": [
                    "Network traffic: Standard DNS query for google.com",
                    "Network traffic: Routine NTP sync with time.windows.com",
                    "Network traffic: Small HTTP request to cdn.example.com",
                    "Network traffic: PING request to local gateway 192.168.1.1"
                ]
            }
        }

    def _generate_timestamp(self):
        # Генерируем случайную дату/время за последний месяц
        days_ago = random.randint(1, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        from datetime import datetime, timedelta
        dt = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def _generate_ip_address(self, is_internal=False):
        if is_internal:
            return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        return f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

    def _generate_random_string(self, length=8):
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _generate_data_entry(self, is_relevant: bool, clue_type: str) -> str:
        templates = self.clue_types[clue_type]["relevant" if is_relevant else "irrelevant"]
        template = random.choice(templates)

        # Заполнение плейсхолдеров
        replacements = {
            "{timestamp}": self._generate_timestamp(),
            "{ip_address}": self._generate_ip_address(is_internal=random.choice([True, False])),
            "{filename}": f"{self._generate_random_string(6)}.txt",
            "{sender}": f"{self._generate_random_string(5)}@{self._generate_random_string(4)}.com",
            "{account_id}": self._generate_random_string(6).upper(),
            "{pid}": str(random.randint(1000, 9999)),
            "{filename_secret}": f"secret_proj_{self._generate_random_string(4)}",
            "{filename_exec}": f"tool_{self._generate_random_string(3)}.exe",
            "{process_id}": self._generate_random_string(7),
            "{hidden_filename}": f".hidden_data_{self._generate_random_string(5)}.dat",
            "{corrupted_filename}": f"corrupt_file_{self._generate_random_string(4)}.bin",
            "{num}": str(random.randint(1, 100)),
            "{month}": random.choice(
                ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
            "{date}": f"{random.randint(1, 28)}_{random.randint(1, 12)}_{random.randint(2023, 2025)}",
            "{license_id}": f"{self._generate_random_string(4)}-{self._generate_random_string(4)}-{self._generate_random_string(4)}",
            "{coords}": f"{random.uniform(-90, 90):.4f}, {random.uniform(-180, 180):.4f}",
            "{size}": str(random.randint(10, 500)),
            "{country_code}": random.choice(["CN", "RU", "KP", "IR", "US"]),
            "{source_ip}": self._generate_ip_address(),
            "{port_num}": str(random.randint(1, 65535)),
            "{domain}": f"{self._generate_random_string(6)}.com",
            "{program_id}": self._generate_random_string(7),
            "{random_path}": f"C:\\Users\\Public\\{self._generate_random_string(5)}\\{self._generate_random_string(6)}.exe",
            "{service_name}": self._generate_random_string(8)
        }

        for placeholder, value in replacements.items():
            template = template.replace(placeholder, value)

        return template

    def _examine_entry(self, entry: str, is_target: bool):
        """Предоставляет детальный анализ выбранной записи."""
        print(f"\n{XSSColors.CYAN}--- Детальный Анализ Записи ---{XSSColors.RESET}")
        print(f"{XSSColors.WHITE}Запись:{XSSColors.RESET} {entry}")

        time.sleep(1)  # Имитация процесса анализа

        if is_target:
            print(
                f"{XSSColors.LIGHT_GREEN}Анализ завершен: Обнаружены аномалии! Эта запись содержит потенциально важные улики. Рекомендуется дальнейшее расследование.{XSSColors.RESET}")
        else:
            print(
                f"{XSSColors.LIGHT_GRAY}Анализ завершен: Запись кажется обычной. Нет явных признаков подозрительной активности.{XSSColors.RESET}")
        print(f"{XSSColors.CYAN}-------------------------------{XSSColors.RESET}\n")
        time.sleep(1)

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ СУДЕБНЫЙ АНАЛИЗ ━━━━━━━━━━{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Добро пожаловать в игру 'Судебный анализ'!{XSSColors.RESET}")
        print(
            f"{XSSColors.INFO}Ваша задача — найти единственную 'улику' среди множества данных, указывающую на подозрительную активность.{XSSColors.RESET}")
        print(
            f"{XSSColors.INFO}Вы можете {XSSColors.WHITE}'изучить'{XSSColors.INFO} любую запись, чтобы получить больше информации, прежде чем сделать свой выбор.{XSSColors.RESET}\n")

        skill_level = game_state.get_skill(self.skill)
        num_irrelevant_entries = 5 + skill_level * 2  # Больше шума на высоких уровнях

        all_clue_types = list(self.clue_types.keys())
        target_clue_type = random.choice(all_clue_types)

        target_clue_data = self._generate_data_entry(is_relevant=True, clue_type=target_clue_type)

        data_list_objects = []
        for _ in range(num_irrelevant_entries):
            random_clue_type = random.choice(all_clue_types)
            data_list_objects.append(
                {"content": self._generate_data_entry(is_relevant=False, clue_type=random_clue_type),
                 "is_target": False})

        data_list_objects.append({"content": target_clue_data, "is_target": True})
        random.shuffle(data_list_objects)

        attempts = 2  # Можно сделать зависимым от сложности/навыка

        while attempts > 0:
            print(f"{XSSColors.HEADER}--- ДОСТУПНЫЕ ДАННЫЕ ДЛЯ АНАЛИЗА ({attempts} попыток) ---{XSSColors.RESET}")
            for i, entry_obj in enumerate(data_list_objects, 1):
                print(f"    {XSSColors.PROMPT}{i}.{XSSColors.RESET} {entry_obj['content']}")
            print(f"{XSSColors.HEADER}--------------------------------------------------{XSSColors.RESET}\n")

            user_action = audio_system.get_input_with_sound(
                f"{XSSColors.PROMPT}Введите {XSSColors.WHITE}'номер'{XSSColors.PROMPT} записи для анализа или {XSSColors.WHITE}'g'{XSSColors.PROMPT} для догадки: {XSSColors.RESET}").lower()

            if user_action == 'g':
                # Фаза догадки
                try:
                    guess_idx = int(audio_system.get_input_with_sound(
                        f"{XSSColors.PROMPT}Введите номер записи, которая является уликой: {XSSColors.RESET}"))
                    if not (1 <= guess_idx <= len(data_list_objects)):
                        print(f"{XSSColors.ERROR}Неверный номер. Попробуйте еще раз.{XSSColors.RESET}")
                        continue

                    user_guess_obj = data_list_objects[guess_idx - 1]

                    if user_guess_obj["is_target"]:
                        audio_system.play_sound("minigame_win")
                        print(
                            f"\n{XSSColors.SUCCESS}🎉 УСПЕХ! Вы успешно нашли улику: '{user_guess_obj['content']}'!{XSSColors.RESET}")
                        return True
                    else:
                        attempts -= 1
                        print(
                            f"{XSSColors.ERROR}Неверно. Эта запись не является уликой. Попыток осталось: {attempts}.{XSSColors.RESET}")
                        if attempts == 0:
                            audio_system.play_sound("minigame_lose")
                            # Находим правильную улику, чтобы показать ее в случае провала
                            correct_clue_content = next(obj['content'] for obj in data_list_objects if obj['is_target'])
                            print(
                                f"\n{XSSColors.ERROR}❌ Провал! Уликой была запись: '{correct_clue_content}'.{XSSColors.RESET}")
                            return False
                except ValueError:
                    print(f"{XSSColors.ERROR}Введите число для догадки или 'g'.{XSSColors.RESET}")
            else:
                # Фаза анализа
                try:
                    analyze_idx = int(user_action)
                    if not (1 <= analyze_idx <= len(data_list_objects)):
                        print(f"{XSSColors.ERROR}Неверный номер. Попробуйте еще раз.{XSSColors.RESET}")
                        continue

                    selected_entry_obj = data_list_objects[analyze_idx - 1]
                    self._examine_entry(selected_entry_obj["content"], selected_entry_obj["is_target"])
                except ValueError:
                    print(f"{XSSColors.ERROR}Введите номер записи для анализа или 'g' для догадки.{XSSColors.RESET}")

        return False

class PatternRecognitionGame(Minigame):
    """Мини-игра "Распознавание паттернов"."""
    def __init__(self):
        super().__init__(
            "Распознавание паттернов",
            "Определите повторяющийся паттерн в последовательности символов",
            "scanning"
        )

    def play(self) -> bool:
        audio_system.play_sound("minigame_start")
        print(f"\n{XSSColors.WARNING}━━━━━━━━━━ РАСПОЗНАВАНИЕ ПАТТЕРНОВ ━━━━━━━━━━{XSSColors.RESET}")
        skill_level = game_state.get_skill(self.skill)

        possible_patterns = [
            "ABBC", "XYZA", "12123", "QWEQWE", "++--", "#@#@"
        ]

        chosen_pattern = random.choice(possible_patterns)
        sequence_length = 20 + skill_level * 2 # Длина последовательности

        # Генерируем последовательность с повторяющимся паттерном и шумом
        full_sequence = ""
        for _ in range(sequence_length // len(chosen_pattern) + 2): # чтобы точно вместить паттерн несколько раз
            full_sequence += chosen_pattern

        noise_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

        # Внедряем шум
        noisy_sequence = list(full_sequence[:sequence_length])
        num_noise = max(1, (sequence_length // 4) - skill_level) # Чем выше навык, тем меньше шума

        for _ in range(num_noise):
            idx = random.randint(0, len(noisy_sequence) - 1)
            noisy_sequence[idx] = random.choice(noise_chars)

        final_sequence = "".join(noisy_sequence)

        print(f"{XSSColors.INFO}Вам дана последовательность символов. Найдите повторяющийся паттерн в ней.{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Паттерн может быть длиной от 3 до 6 символов.{XSSColors.RESET}")
        print(f"{XSSColors.INFO}Последовательность: {final_sequence}{XSSColors.RESET}\n")

        attempts = 2
        while attempts > 0:
            user_guess = audio_system.get_input_with_sound(f"{XSSColors.PROMPT}Введите найденный паттерн: {XSSColors.RESET}").strip()

            if user_guess == chosen_pattern:
                audio_system.play_sound("minigame_win")
                print(f"\n{XSSColors.SUCCESS}🎉 УСПЕХ! Вы правильно распознали паттерн: '{chosen_pattern}'!{XSSColors.RESET}")
                return True
            else:
                attempts -= 1
                print(f"{XSSColors.ERROR}Неверный паттерн. Попыток осталось: {attempts}.{XSSColors.RESET}")
                print(f"Подсказка: Попробуйте найти короткие повторяющиеся блоки.{XSSColors.RESET}")

        audio_system.play_sound("minigame_lose")
        print(f"\n{XSSColors.ERROR}❌ Провал! Правильный паттерн был: '{chosen_pattern}'.{XSSColors.RESET}")
        return False

# Добавьте эти классы в MinigameHub
class MinigameHub:
    """Центр мини-игр"""

    def __init__(self):
        self.games = {
            "password_crack": PasswordCrackGame(),
            "firewall_bypass": FirewallBypassGame(),
            "memory_sequence": MemorySequenceGame(),
            "network_trace": NetworkTraceGame(),
            "sql_injection": SQLInjectionGame(),
            # НОВЫЕ ИГРЫ
            "brute_force": BruteForceGame(),
            "cipher_decryption": CipherDecryptionGame(),
            "reverse_engineering": ReverseEngineeringGame(),
            "packet_sniffing": PacketSniffingGame(),
            "malware_analysis": MalwareAnalysisGame(),
            "honeypot_avoidance": HoneypotAvoidanceGame(),
            "log_deletion": LogDeletionGame(),
            "traffic_obfuscation": TrafficObfuscationGame(),
            "social_engineering": SocialEngineeringGame(),
            "covert_channel": CovertChannelGame(),
            "port_scanning": PortScanningGame(),
            "vulnerability_assessment": VulnerabilityAssessmentGame(),
            "data_mining": DataMiningGame(),
            "forensic_analysis": ForensicAnalysisGame(),
            "pattern_recognition": PatternRecognitionGame(),
        }

    def show_hub(self) -> None:
        """Показывает центр мини-игр с полной информацией о наградах и статистике"""
        while True:
            # Очищаем экран для лучшего восприятия (опционально)
            print("\n" * 2)

            print(
                f"{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
            print(f"{XSSColors.HEADER}║               🎮 ТРЕНИРОВОЧНЫЙ ЦЕНТР XSS.IS 🎮               ║{XSSColors.RESET}")
            print(
                f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

            print(
                f"\n{XSSColors.INFO}🎯 Развивайте свои хакерские навыки через практические тренировки!{XSSColors.RESET}")

            # Показываем общую статистику игрока
            self._show_player_training_stats()

            # Система наград
            print(f"\n{XSSColors.SUCCESS}🎁 СИСТЕМА НАГРАД ЗА ТРЕНИРОВКИ:{XSSColors.RESET}")
            print(f"   {XSSColors.MONEY}💰 BTC:{XSSColors.RESET} 5-20 (уменьшается с ростом навыка)")
            print(f"   {XSSColors.REP}⭐ Репутация:{XSSColors.RESET} 2-8 (зависит от сложности и мастерства)")
            print(f"   {XSSColors.SKILL}📈 Рост навыка:{XSSColors.RESET} 30% шанс (уменьшается с опытом)")
            print(
                f"   {XSSColors.WARNING}✨ Экспертный бонус:{XSSColors.RESET} до +10 репутации для мастеров (8+ навык)")

            # Показываем категории тренировок
            print(f"\n{XSSColors.INFO}📚 ДОСТУПНЫЕ ТРЕНИРОВКИ ПО КАТЕГОРИЯМ:{XSSColors.RESET}")

            # Группируем игры по навыкам
            games_by_skill = self._group_games_by_skill()

            game_list = []
            counter = 1

            for skill_type, skill_games in games_by_skill.items():
                skill_color = self._get_skill_color(skill_type)
                skill_level = game_state.get_skill(skill_type)

                print(f"\n   {skill_color}🎯 {skill_type.upper()} (Уровень: {skill_level}/10){XSSColors.RESET}")
                print(f"   {XSSColors.DARK_GRAY}{'─' * 50}{XSSColors.RESET}")

                for game_id, game in skill_games:
                    difficulty = game.get_difficulty()
                    rep_reward = game.get_reputation_reward() if hasattr(game,
                                                                         'get_reputation_reward') else self._calculate_rep_reward(
                        game)

                    # Определяем награды BTC
                    btc_min, btc_max = self._calculate_btc_range(skill_level)

                    # Определяем статус сложности
                    difficulty_status = self._get_difficulty_status(difficulty)

                    # Определяем рекомендацию
                    recommendation = self._get_game_recommendation(skill_level, difficulty)

                    print(f"      {counter}. {XSSColors.BRIGHT_GREEN}{game.name}{XSSColors.RESET}")
                    print(f"         📋 Описание: {game.description}")
                    print(f"         🎯 Сложность: {difficulty_status}")
                    print(f"         💰 BTC: {btc_min}-{btc_max} | ⭐ Репутация: +{rep_reward}")
                    print(f"         {recommendation}")

                    game_list.append((game_id, game))
                    counter += 1
                    print()

            # Дополнительные опции
            print(f"{XSSColors.WARNING}📊 ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ:{XSSColors.RESET}")
            print(f"   s. Подробная статистика тренировок")
            print(f"   r. Рекомендации по развитию навыков")
            print(f"   h. Справка по мини-играм")
            print(f"   0. Выход из тренировочного центра")

            print(f"\n{XSSColors.PROMPT}{'═' * 60}{XSSColors.RESET}")
            choice = audio_system.get_input_with_sound(
                f"{XSSColors.PROMPT}Выберите тренировку или опцию: {XSSColors.RESET}")

            # Обработка выбора
            if choice == '0':
                print(f"{XSSColors.INFO}Выход из тренировочного центра...{XSSColors.RESET}")
                break
            elif choice.lower() == 's':
                self._show_detailed_training_stats()
            elif choice.lower() == 'r':
                self._show_skill_recommendations()
            elif choice.lower() == 'h':
                self._show_minigame_help()
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(game_list):
                        game_id, game = game_list[idx]
                        self._start_training_session(game_id, game)
                    else:
                        print(
                            f"{XSSColors.ERROR}❌ Неверный выбор. Введите число от 1 до {len(game_list)}{XSSColors.RESET}")
                        input(f"{XSSColors.PROMPT}Нажмите Enter для продолжения...{XSSColors.RESET}")
                except ValueError:
                    print(f"{XSSColors.ERROR}❌ Введите корректный номер или букву опции{XSSColors.RESET}")
                    input(f"{XSSColors.PROMPT}Нажмите Enter для продолжения...{XSSColors.RESET}")

    def _show_player_training_stats(self) -> None:
        """Показывает статистику тренировок игрока"""
        total_reputation = game_state.get_stat("reputation", 0)
        training_reputation = game_state.get_stat("training_reputation_earned", 0)
        training_sessions = game_state.get_stat("training_sessions_completed", 0)

        print(f"\n{XSSColors.INFO}👤 ВАША СТАТИСТИКА:{XSSColors.RESET}")
        print(f"   📊 Общая репутация: {XSSColors.REP}{total_reputation}{XSSColors.RESET}")
        if training_reputation > 0:
            print(f"   📚 Репутация от тренировок: {XSSColors.SUCCESS}{training_reputation}{XSSColors.RESET}")
        if training_sessions > 0:
            print(f"   🎮 Завершенных тренировок: {XSSColors.WARNING}{training_sessions}{XSSColors.RESET}")

        # Показываем текущие навыки
        skills = ["cracking", "stealth", "scanning"]
        print(f"   🛠️  Навыки: ", end="")
        skill_displays = []
        for skill in skills:
            level = game_state.get_skill(skill)
            color = XSSColors.SUCCESS if level >= 7 else XSSColors.WARNING if level >= 4 else XSSColors.ERROR
            skill_displays.append(f"{skill}: {color}{level}/10{XSSColors.RESET}")
        print(" | ".join(skill_displays))

    def _group_games_by_skill(self) -> dict:
        """Группирует игры по типам навыков"""
        games_by_skill = {}

        for game_id, game in self.games.items():
            skill = game.skill
            if skill not in games_by_skill:
                games_by_skill[skill] = []
            games_by_skill[skill].append((game_id, game))

        # Сортируем игры внутри каждой группы по сложности
        for skill in games_by_skill:
            games_by_skill[skill].sort(key=lambda x: x[1].get_difficulty())

        return games_by_skill

    def _get_skill_color(self, skill_type: str) -> str:
        """Возвращает цвет для типа навыка"""
        skill_colors = {
            "cracking": XSSColors.DANGER,
            "stealth": XSSColors.WARNING,
            "scanning": XSSColors.INFO
        }
        return skill_colors.get(skill_type, XSSColors.INFO)

    def _calculate_rep_reward(self, game: Minigame) -> int:
        """Рассчитывает награду репутации для игры (fallback)"""
        skill_level = game_state.get_skill(game.skill)
        difficulty = game.get_difficulty()

        base_rep = 2
        difficulty_bonus = difficulty // 2
        skill_bonus = 1 if skill_level >= 7 else 0

        return base_rep + difficulty_bonus + skill_bonus

    def _calculate_btc_range(self, skill_level: int) -> tuple:
        """Рассчитывает диапазон BTC наград"""
        btc_min, btc_max = 5, 20

        if skill_level >= 7:
            btc_min, btc_max = int(btc_min * 0.5), int(btc_max * 0.5)
        elif skill_level >= 5:
            btc_min, btc_max = int(btc_min * 0.7), int(btc_max * 0.7)

        return btc_min, btc_max

    def _get_difficulty_status(self, difficulty: int) -> str:
        """Возвращает статус сложности с цветом"""
        if difficulty <= 3:
            return f"{XSSColors.SUCCESS}Легко ({difficulty}/8){XSSColors.RESET}"
        elif difficulty <= 5:
            return f"{XSSColors.WARNING}Средне ({difficulty}/8){XSSColors.RESET}"
        elif difficulty <= 7:
            return f"{XSSColors.ERROR}Сложно ({difficulty}/8){XSSColors.RESET}"
        else:
            return f"{XSSColors.DANGER}Экстремально ({difficulty}/8){XSSColors.RESET}"

    def _get_game_recommendation(self, skill_level: int, difficulty: int) -> str:
        """Возвращает рекомендацию для игры"""
        if difficulty <= skill_level - 2:
            return f"         {XSSColors.SUCCESS}✅ Рекомендовано: Легко для вашего уровня{XSSColors.RESET}"
        elif difficulty <= skill_level + 1:
            return f"         {XSSColors.INFO}🎯 Рекомендовано: Подходящий вызов{XSSColors.RESET}"
        elif difficulty <= skill_level + 3:
            return f"         {XSSColors.WARNING}⚡ Сложно: Требует мастерства{XSSColors.RESET}"
        else:
            return f"         {XSSColors.ERROR}🔥 Очень сложно: Для экспертов{XSSColors.RESET}"

    def _start_training_session(self, game_id: str, game: Minigame) -> None:
        """Запускает тренировочную сессию с подробной информацией"""
        skill_level = game_state.get_skill(game.skill)
        difficulty = game.get_difficulty()

        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}                     🚀 НАЧАЛО ТРЕНИРОВКИ                      {XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.BRIGHT_GREEN}🎯 {game.name}{XSSColors.RESET}")
        print(f"{XSSColors.INFO}📋 {game.description}{XSSColors.RESET}")

        # Показываем детальный прогноз наград
        self._show_detailed_rewards_preview(game, skill_level, difficulty)

        # Подтверждение начала
        confirm = input(f"\n{XSSColors.PROMPT}🚀 Начать тренировку? (y/n): {XSSColors.RESET}").lower()

        if confirm in ['y', 'yes', 'да', '']:
            print(f"\n{XSSColors.SUCCESS}✅ Запуск тренировки...{XSSColors.RESET}")
            time.sleep(1)
            self.play_game(game_id, game)
        else:
            print(f"{XSSColors.INFO}❌ Тренировка отменена{XSSColors.RESET}")

    def _show_detailed_rewards_preview(self, game: Minigame, skill_level: int, difficulty: int) -> None:
        """Показывает детальный прогноз наград"""
        btc_min, btc_max = self._calculate_btc_range(skill_level)
        rep_reward = self._calculate_rep_reward(game)

        # Шанс роста навыка
        base_chance = 30
        skill_penalty = skill_level * 3
        upgrade_chance = max(5, base_chance - skill_penalty)

        print(f"\n{XSSColors.INFO}🏆 ДЕТАЛЬНЫЙ ПРОГНОЗ НАГРАД:{XSSColors.RESET}")
        print(f"   {XSSColors.MONEY}💰 BTC при успехе:{XSSColors.RESET} {btc_min}-{btc_max}")
        print(f"   {XSSColors.REP}⭐ Репутация при успехе:{XSSColors.RESET} +{rep_reward}")
        print(f"   {XSSColors.SKILL}📈 Шанс роста навыка '{game.skill}':{XSSColors.RESET} {upgrade_chance}%")

        if skill_level >= 8:
            print(f"   {XSSColors.SUCCESS}✨ Экспертный бонус:{XSSColors.RESET} 10% шанс на +5-10 репутации")

        print(f"   🎯 Сложность тренировки: {self._get_difficulty_status(difficulty)}")

        # Показываем риски неудачи
        if random.random() < 0.1:  # Показываем иногда
            print(f"   {XSSColors.WARNING}⚠️  При неудаче:{XSSColors.RESET} возможна потеря 1-2 репутации (10% шанс)")

    def _show_detailed_training_stats(self) -> None:
        """Показывает подробную статистику тренировок"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                   📊 СТАТИСТИКА ТРЕНИРОВОК                   ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        # Общая статистика
        total_sessions = game_state.get_stat("training_sessions_completed", 0)
        successful_sessions = game_state.get_stat("training_sessions_successful", 0)
        training_rep = game_state.get_stat("training_reputation_earned", 0)
        training_btc = game_state.get_stat("training_btc_earned", 0)

        success_rate = (successful_sessions / total_sessions * 100) if total_sessions > 0 else 0

        print(f"\n{XSSColors.INFO}📈 ОБЩАЯ СТАТИСТИКА:{XSSColors.RESET}")
        print(f"   🎮 Всего тренировок: {total_sessions}")
        print(f"   ✅ Успешных: {successful_sessions}")
        print(f"   📊 Процент успеха: {success_rate:.1f}%")

        if training_rep > 0:
            print(f"   ⭐ Заработано репутации: {XSSColors.REP}{training_rep}{XSSColors.RESET}")
        if training_btc > 0:
            print(f"   💰 Заработано BTC: {XSSColors.MONEY}{training_btc}{XSSColors.RESET}")

        # Статистика по навыкам
        print(f"\n{XSSColors.INFO}🛠️  ПРОГРЕСС ПО НАВЫКАМ:{XSSColors.RESET}")
        skills = ["cracking", "stealth", "scanning"]

        for skill in skills:
            level = game_state.get_skill(skill)
            sessions_skill = game_state.get_stat(f"training_{skill}_sessions", 0)

            level_color = XSSColors.SUCCESS if level >= 7 else XSSColors.WARNING if level >= 4 else XSSColors.ERROR
            progress_bar = "▓" * level + "░" * (10 - level)

            print(
                f"   {skill.upper()}: {level_color}{progress_bar}{XSSColors.RESET} {level}/10 ({sessions_skill} тренировок)")

        # Рекомендации
        print(f"\n{XSSColors.WARNING}💡 РЕКОМЕНДАЦИИ:{XSSColors.RESET}")

        weakest_skill = min(skills, key=lambda s: game_state.get_skill(s))
        strongest_skill = max(skills, key=lambda s: game_state.get_skill(s))

        print(f"   • Слабейший навык: {weakest_skill} - рекомендуется развивать")
        print(f"   • Сильнейший навык: {strongest_skill} - используйте для сложных миссий")

        if success_rate < 70:
            print(f"   • Низкий процент успеха - попробуйте более легкие тренировки")
        elif success_rate > 90:
            print(f"   • Высокий процент успеха - попробуйте более сложные тренировки")

        input(f"\n{XSSColors.PROMPT}Нажмите Enter для возврата в меню...{XSSColors.RESET}")

    def _show_skill_recommendations(self) -> None:
        """Показывает рекомендации по развитию навыков"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                  💡 РЕКОМЕНДАЦИИ ПО РАЗВИТИЮ                 ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        reputation = game_state.get_stat("reputation", 0)

        print(f"\n{XSSColors.INFO}🎯 АНАЛИЗ ВАШЕГО ПРОФИЛЯ:{XSSColors.RESET}")
        print(f"   Репутация: {reputation}")

        # Анализ навыков
        skills = {
            "cracking": game_state.get_skill("cracking"),
            "stealth": game_state.get_skill("stealth"),
            "scanning": game_state.get_skill("scanning")
        }

        avg_skill = sum(skills.values()) / len(skills)

        print(f"   Средний уровень навыков: {avg_skill:.1f}/10")

        # Персонализированные рекомендации
        print(f"\n{XSSColors.WARNING}📋 ПЕРСОНАЛЬНЫЕ РЕКОМЕНДАЦИИ:{XSSColors.RESET}")

        if avg_skill < 3:
            print(f"   🔰 НОВИЧОК - Фокусируйтесь на базовых тренировках:")
            print(f"      • Взлом пароля (cracking)")
            print(f"      • Сканирование портов (scanning)")
            print(f"      • Избегайте сложных игр пока")

        elif avg_skill < 6:
            print(f"   ⚡ РАЗВИВАЮЩИЙСЯ - Расширяйте кругозор:")
            print(f"      • Пробуйте разные типы тренировок")
            print(f"      • Развивайте слабые навыки")
            print(f"      • Начинайте пробовать командные миссии")

        elif avg_skill < 8:
            print(f"   🎯 ПРОДВИНУТЫЙ - Специализируйтесь:")
            print(f"      • Выберите основную специализацию")
            print(f"      • Тренируйтесь на максимальной сложности")
            print(f"      • Участвуйте в сложных миссиях")

        else:
            print(f"   👑 ЭКСПЕРТ - Совершенствуйтесь:")
            print(f"      • Поддерживайте навыки регулярными тренировками")
            print(f"      • Ищите экспертные бонусы")
            print(f"      • Помогайте другим или ведите команды")

        # Рекомендации по конкретным играм
        print(f"\n{XSSColors.SUCCESS}🎮 РЕКОМЕНДОВАННЫЕ ТРЕНИРОВКИ:{XSSColors.RESET}")

        weakest_skill = min(skills, key=skills.get)
        strongest_skill = max(skills, key=skills.get)

        recommended_games = []

        for game_id, game in self.games.items():
            if game.skill == weakest_skill:
                difficulty = game.get_difficulty()
                if difficulty <= skills[weakest_skill] + 2:  # Подходящая сложность
                    recommended_games.append(f"      • {game.name} (развитие {weakest_skill})")

        if recommended_games:
            print(f"   Для развития слабого навыка ({weakest_skill}):")
            for rec in recommended_games[:3]:  # Показываем первые 3
                print(rec)

        input(f"\n{XSSColors.PROMPT}Нажмите Enter для возврата в меню...{XSSColors.RESET}")

    def _show_minigame_help(self) -> None:
        """Показывает справку по мини-играм"""
        print(f"\n{XSSColors.HEADER}╔══════════════════════════════════════════════════════════════╗{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}║                     📖 СПРАВКА ПО ИГРАМ                      ║{XSSColors.RESET}")
        print(f"{XSSColors.HEADER}╚══════════════════════════════════════════════════════════════╝{XSSColors.RESET}")

        print(f"\n{XSSColors.INFO}🎯 ТИПЫ НАВЫКОВ:{XSSColors.RESET}1")
        print(f"   {XSSColors.DANGER}🔓 CRACKING{XSSColors.RESET} - Взлом паролей, шифров, систем безопасности")
        print(f"   {XSSColors.WARNING}👻 STEALTH{XSSColors.RESET} - Скрытность, обход защиты, социальная инженерия")
        print(f"   {XSSColors.INFO}🔍 SCANNING{XSSColors.RESET} - Разведка, анализ данных, поиск уязвимостей")

        print(f"\n{XSSColors.SUCCESS}🏆 СИСТЕМА НАГРАД:{XSSColors.RESET}")
        print(f"   • Награды зависят от сложности игры и вашего навыка")
        print(f"   • Чем выше навык, тем меньше BTC, но больше репутации")
        print(f"   • Экспертный бонус активируется при навыке 8+")
        print(f"   • Шанс роста навыка уменьшается с опытом")

        print(f"\n{XSSColors.WARNING}💡 СОВЕТЫ:{XSSColors.RESET}")
        print(f"   • Начинайте с легких игр для изучения механик")
        print(f"   • Развивайте все навыки равномерно")
        print(f"   • Сложные игры дают больше репутации")
        print(f"   • Регулярные тренировки поддерживают форму")
        print(f"   • Неудачи могут снижать репутацию")

        print(f"\n{XSSColors.INFO}🎮 ОСОБЕННОСТИ ИГР:{XSSColors.RESET}")
        print(f"   • Каждая игра уникальна и развивает определенные навыки")
        print(f"   • Сложность адаптируется под ваш уровень")
        print(f"   • Некоторые игры имеют особые механики")
        print(f"   • Прогресс сохраняется между сессиями")

        input(f"\n{XSSColors.PROMPT}Нажмите Enter для возврата в меню...{XSSColors.RESET}")

    def play_game(self, game_id: str, game: Minigame) -> None:
        """Запускает конкретную мини-игру с отслеживанием статистики"""
        print(f"\n{XSSColors.INFO}Запуск: {game.name}{XSSColors.RESET}")
        time.sleep(1)

        game_state.modify_stat("training_sessions_completed", 1)

        # Играем
        success = game.play()

        if success:
            # Уменьшаем шанс прокачки и добавляем прогрессивную сложность
            current_skill = game_state.get_skill(game.skill)

            # Шанс уменьшается с ростом навыка
            base_chance = 0.3
            skill_penalty = current_skill * 0.03
            upgrade_chance = max(0.05, base_chance - skill_penalty)

            if random.random() < upgrade_chance:
                if current_skill < 10:
                    game_state.modify_skill(game.skill, 1)
                    print(
                        f"\n{XSSColors.SKILL}[+] Навык '{game.skill}' повышен до {game_state.get_skill(game.skill)}/10!{XSSColors.RESET}")

            # Награды за успех с репутацией
            # Уменьшаем награду в BTC для высоких навыков
            btc_reward = random.randint(5, 20)
            if current_skill >= 7:
                btc_reward = int(btc_reward * 0.5)
            elif current_skill >= 5:
                btc_reward = int(btc_reward * 0.7)

            # ДОБАВЛЯЕМ РЕПУТАЦИЮ
            # Репутация зависит от сложности мини-игры и навыка
            base_reputation = 2  # Базовая репутация за любое прохождение
            difficulty_bonus = game.get_difficulty() // 2  # Бонус за сложность
            skill_bonus = 1 if current_skill >= 7 else 0  # Бонус для высокого навыка

            reputation_reward = base_reputation + difficulty_bonus + skill_bonus

            # Применяем награды
            game_state.earn_currency(btc_reward, 'btc_balance')
            game_state.modify_stat("reputation", reputation_reward)

            print(f"{XSSColors.MONEY}[+] Заработано {btc_reward} BTC за тренировку{XSSColors.RESET}")
            print(
                f"{XSSColors.REP}[+] Репутация +{reputation_reward} (сложность: {game.get_difficulty()}){XSSColors.RESET}")

            # Дополнительные бонусы для особо сложных игр
            if current_skill >= 8 and random.random() < 0.1:  # 10% шанс для экспертов
                bonus_rep = random.randint(5, 10)
                game_state.modify_stat("reputation", bonus_rep)
                print(f"{XSSColors.SUCCESS}[БОНУС] Экспертное выполнение! +{bonus_rep} репутации{XSSColors.RESET}")


            game_state.modify_stat("training_sessions_successful", 1)
            game_state.modify_stat("training_reputation_earned", reputation_reward)
            game_state.modify_stat("training_btc_earned", btc_reward)
            game_state.modify_stat(f"training_{game.skill}_sessions", 1)

        else:
            print(f"\n{XSSColors.INFO}Продолжайте тренироваться!{XSSColors.RESET}")
            # Можно добавить небольшую потерю репутации за неудачи
            if random.random() < 0.1:  # 10% шанс потери репутации
                rep_loss = random.randint(1, 2)
                game_state.modify_stat("reputation", -rep_loss)
                print(f"{XSSColors.WARNING}[-] Неудача повлияла на репутацию: -{rep_loss}{XSSColors.RESET}")

        # Спрашиваем, хочет ли играть еще
        again = input(f"\n{XSSColors.PROMPT}Сыграть еще? (y/n): {XSSColors.RESET}").lower()
        if again == 'y':
            self.play_game(game_id, game)

    def get_random_minigame(self) -> Tuple[str, Minigame]:
        """Возвращает случайную мини-игру"""
        game_id = random.choice(list(self.games.keys()))
        return game_id, self.games[game_id]


# Глобальный экземпляр центра мини-игр
minigame_hub = MinigameHub()