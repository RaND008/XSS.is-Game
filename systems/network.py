"""
Система сетевых узлов для XSS Game 0.3.1
"""

import random
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from ui.colors import XSSColors
from ui.effects import typing_effect, progress_bar, boxed_text
from core.game_state import game_state
from systems.audio import audio_system


class NetworkNode:
    """Класс сетевого узла"""

    def __init__(self, address: str, name: str, node_type: str = "server"):
        self.address = address
        self.name = name
        self.type = node_type
        self.security_level = 1
        self.services = []
        self.vulnerabilities = []
        self.connected_nodes = []
        self.is_compromised = False
        self.owner = "system"
        self.heat_level = 0

        # НОВЫЕ свойства для расширенной сети
        self.firewall = None
        self.ids_system = None
        self.honeypots = []
        self.subnet = None
        self.geo_location = {"country": "Unknown", "city": "Unknown"}
        self.uptime = 100
        self.bandwidth = "1Gbps"
        self.os_type = "Linux"
        self.last_scan = None
        self.network_interfaces = []
        self.open_ports = []
        self.filtered_ports = []
        self.closed_ports = []
        self.response_time = 0

    def to_dict(self) -> dict:
        """Преобразует узел в словарь для сохранения"""
        return {
            # Существующие поля...
            "address": self.address,
            "name": self.name,
            "type": self.type,
            "security_level": self.security_level,
            "services": self.services,
            "vulnerabilities": self.vulnerabilities,
            "connected_nodes": self.connected_nodes,
            "is_compromised": self.is_compromised,
            "owner": self.owner,
            "heat_level": self.heat_level,

            # Сериализуем объекты в простые данные
            "firewall": self.firewall.to_dict() if self.firewall else None,
            "ids_system": self.ids_system.to_dict() if self.ids_system else None,
            "honeypots": [hp.to_dict() for hp in self.honeypots] if self.honeypots else [],
            "subnet": self.subnet,
            "geo_location": self.geo_location,
            "uptime": self.uptime,
            "bandwidth": self.bandwidth,
            "os_type": self.os_type,
            "network_interfaces": self.network_interfaces,
            "open_ports": self.open_ports,
            "filtered_ports": self.filtered_ports,
            "closed_ports": self.closed_ports,
            "response_time": self.response_time
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'NetworkNode':
        """Создает узел из словаря"""
        node = cls(data["address"], data["name"], data.get("type", "server"))
        node.security_level = data.get("security_level", 1)
        node.services = data.get("services", [])
        node.vulnerabilities = data.get("vulnerabilities", [])
        node.connected_nodes = data.get("connected_nodes", [])
        node.is_compromised = data.get("is_compromised", False)
        node.owner = data.get("owner", "system")
        node.heat_level = data.get("heat_level", 0)

        # ИСПРАВЛЕННАЯ десериализация объектов
        firewall_data = data.get("firewall")
        if firewall_data:
            node.firewall = Firewall.from_dict(firewall_data)

        ids_data = data.get("ids_system")
        if ids_data:
            node.ids_system = IDSSystem.from_dict(ids_data)

        honeypots_data = data.get("honeypots", [])
        node.honeypots = [Honeypot.from_dict(hp_data) for hp_data in honeypots_data]

        # Остальные поля
        node.subnet = data.get("subnet")
        node.geo_location = data.get("geo_location", {"country": "Unknown", "city": "Unknown"})
        node.uptime = data.get("uptime", 100)
        node.bandwidth = data.get("bandwidth", "1Gbps")
        node.os_type = data.get("os_type", "Linux")
        node.network_interfaces = data.get("network_interfaces", [])
        node.open_ports = data.get("open_ports", [])
        node.filtered_ports = data.get("filtered_ports", [])
        node.closed_ports = data.get("closed_ports", [])
        node.response_time = data.get("response_time", 0)

        return node


class Firewall:
    """Класс файрвола"""

    def __init__(self, firewall_type: str = "basic"):
        self.type = firewall_type  # basic, advanced, enterprise
        self.rules = []
        self.blocked_ips = []
        self.allowed_ports = [80, 443, 22]
        self.is_active = True
        self.detection_rate = 0.7

    def add_rule(self, rule: dict):
        """Добавить правило файрвола"""
        self.rules.append(rule)

    def check_connection(self, source_ip: str, dest_port: int) -> bool:
        """Проверить разрешено ли соединение"""
        if source_ip in self.blocked_ips:
            return False
        if dest_port not in self.allowed_ports:
            return False
        return True

    def to_dict(self) -> dict:
        """Сериализация в словарь"""
        return {
            "type": self.type,
            "rules": self.rules,
            "blocked_ips": self.blocked_ips,
            "allowed_ports": self.allowed_ports,
            "is_active": self.is_active,
            "detection_rate": self.detection_rate
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Firewall':
        """Десериализация из словаря"""
        firewall = cls(data.get("type", "basic"))
        firewall.rules = data.get("rules", [])
        firewall.blocked_ips = data.get("blocked_ips", [])
        firewall.allowed_ports = data.get("allowed_ports", [80, 443, 22])
        firewall.is_active = data.get("is_active", True)
        firewall.detection_rate = data.get("detection_rate", 0.7)
        return firewall


class IDSSystem:
    """Система обнаружения вторжений"""

    def __init__(self, ids_type: str = "signature"):
        self.type = ids_type  # signature, anomaly, hybrid
        self.signatures = []
        self.alert_threshold = 5
        self.detection_rate = 0.8
        self.false_positive_rate = 0.1
        self.is_active = True

    def detect_intrusion(self, activity: dict) -> bool:
        """Обнаружить попытку вторжения"""
        if not self.is_active:
            return False

        # Симуляция обнаружения
        if activity.get("suspicious", False):
            return random.random() < self.detection_rate
        return False

    def to_dict(self) -> dict:
        """Сериализация в словарь"""
        return {
            "type": self.type,
            "signatures": self.signatures,
            "alert_threshold": self.alert_threshold,
            "detection_rate": self.detection_rate,
            "false_positive_rate": self.false_positive_rate,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'IDSSystem':
        """Десериализация из словаря"""
        ids = cls(data.get("type", "signature"))
        ids.signatures = data.get("signatures", [])
        ids.alert_threshold = data.get("alert_threshold", 5)
        ids.detection_rate = data.get("detection_rate", 0.8)
        ids.false_positive_rate = data.get("false_positive_rate", 0.1)
        ids.is_active = data.get("is_active", True)
        return ids


class Honeypot:
    """Ловушка для хакеров"""

    def __init__(self, honeypot_type: str = "ssh"):
        self.type = honeypot_type  # ssh, web, ftp, email
        self.port = self._get_default_port()
        self.is_active = True
        self.interactions = []
        self.detection_value = 0.9

    def _get_default_port(self) -> int:
        """Получить порт по умолчанию для типа"""
        ports = {"ssh": 22, "web": 80, "ftp": 21, "email": 25}
        return ports.get(self.type, 8080)

    def log_interaction(self, attacker_ip: str, activity: str):
        """Логировать взаимодействие с ловушкой"""
        self.interactions.append({
            "timestamp": time.time(),
            "attacker_ip": attacker_ip,
            "activity": activity
        })

    def to_dict(self) -> dict:
        """Сериализация в словарь"""
        return {
            "type": self.type,
            "port": self.port,
            "is_active": self.is_active,
            "interactions": self.interactions,
            "detection_value": self.detection_value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Honeypot':
        """Десериализация из словаря"""
        honeypot = cls(data.get("type", "ssh"))
        honeypot.port = data.get("port", honeypot.port)
        honeypot.is_active = data.get("is_active", True)
        honeypot.interactions = data.get("interactions", [])
        honeypot.detection_value = data.get("detection_value", 0.9)
        return honeypot


class VPNConnection:
    """VPN соединение"""

    def __init__(self, country: str, provider: str):
        self.country = country
        self.provider = provider
        self.is_active = False
        self.anonymity_level = random.uniform(0.7, 0.95)
        self.speed_reduction = random.uniform(0.1, 0.4)
        self.cost_per_hour = random.uniform(0.01, 0.05)


class Botnet:
    """Ботнет"""

    def __init__(self, name: str):
        self.name = name
        self.bots = []
        self.controller_ip = None
        self.command_servers = []
        self.total_bandwidth = 0
        self.is_active = False

    def add_bot(self, bot_ip: str, bot_info: dict):
        """Добавить бот в сеть"""
        self.bots.append({"ip": bot_ip, "info": bot_info})
        self.total_bandwidth += bot_info.get("bandwidth", 10)


class NetworkTools:
    """Симулятор сетевых инструментов"""

    def __init__(self, network_system):
        self.network_system = network_system
        self.scan_history = []

    def nmap_scan(self, target: str, scan_type: str = "basic") -> dict:
        """Симуляция nmap сканирования"""
        if target not in self.network_system.nodes:
            return {"error": "Узел не найден"}

        node = self.network_system.nodes[target]

        print(f"\n{XSSColors.INFO}🔍 Запуск Nmap сканирования {target}...{XSSColors.RESET}")

        # Симуляция времени сканирования
        scan_time = random.uniform(2, 8)
        for i in range(int(scan_time)):
            print(f"\rСканирование... {i + 1}/{int(scan_time)}s", end="", flush=True)
            time.sleep(1)
        print()

        # Результаты сканирования
        result = {
            "target": target,
            "scan_type": scan_type,
            "timestamp": time.time(),
            "host_status": "up" if node.uptime > 0 else "down",
            "os_detection": node.os_type,
            "open_ports": [],
            "filtered_ports": [],
            "closed_ports": [],
            "services": {},
            "vulnerabilities": []
        }

        # Сканирование портов
        if scan_type == "basic":
            ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
        elif scan_type == "full":
            ports_to_scan = list(range(1, 1024))
        else:  # stealth
            ports_to_scan = [80, 443, 22]

        for port in ports_to_scan:
            if self._is_port_open(node, port):
                result["open_ports"].append(port)
                service = self._identify_service(port)
                result["services"][port] = service
            elif self._is_port_filtered(node, port):
                result["filtered_ports"].append(port)
            else:
                result["closed_ports"].append(port)

        # Обнаружение уязвимостей
        if scan_type in ["full", "vuln"]:
            result["vulnerabilities"] = node.vulnerabilities.copy()

        # Проверка обнаружения
        if self._check_detection(node, scan_type):
            heat_gain = random.randint(5, 15)
            game_state.modify_stat("heat_level", heat_gain)
            print(f"{XSSColors.DANGER}⚠ Сканирование обнаружено! Heat Level +{heat_gain}%{XSSColors.RESET}")

        self.scan_history.append(result)
        self._display_nmap_results(result)

        return result

    def _is_port_open(self, node: NetworkNode, port: int) -> bool:
        """Проверить открыт ли порт"""
        # Проверка файрвола
        if node.firewall and node.firewall.is_active:
            if not node.firewall.check_connection("attacker", port):
                return False

        # Стандартные открытые порты для сервисов
        service_ports = {
            "http": [80, 8080],
            "https": [443, 8443],
            "ssh": [22],
            "ftp": [21],
            "telnet": [23],
            "smtp": [25],
            "dns_service": [53],
            "pop3": [110],
            "imap": [143]
        }

        for service in node.services:
            if port in service_ports.get(service, []):
                return True

        return random.random() < 0.1  # 10% шанс случайного открытого порта

    def _is_port_filtered(self, node: NetworkNode, port: int) -> bool:
        """Проверить фильтруется ли порт"""
        if node.firewall and node.firewall.is_active:
            return random.random() < 0.3
        return False

    def _identify_service(self, port: int) -> str:
        """Определить сервис по порту"""
        services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
            53: "dns", 80: "http", 110: "pop3", 143: "imap",
            443: "https", 993: "imaps", 995: "pop3s"
        }
        return services.get(port, "unknown")

    def _check_detection(self, node: NetworkNode, scan_type: str) -> bool:
        """Проверить обнаружено ли сканирование"""
        detection_chance = 0.1  # Базовый шанс

        if node.ids_system and node.ids_system.is_active:
            detection_chance += node.ids_system.detection_rate

        if scan_type == "stealth":
            detection_chance *= 0.3
        elif scan_type == "full":
            detection_chance *= 2

        return random.random() < detection_chance

    def _display_nmap_results(self, result: dict):
        """Отобразить результаты nmap"""
        print(f"\n{XSSColors.SUCCESS}━━━ NMAP SCAN RESULTS ━━━{XSSColors.RESET}")
        print(f"Target: {result['target']}")
        print(f"Host Status: {result['host_status']}")
        print(f"OS: {result['os_detection']}")

        if result['open_ports']:
            print(f"\n{XSSColors.SUCCESS}Open Ports:{XSSColors.RESET}")
            for port in result['open_ports']:
                service = result['services'].get(port, 'unknown')
                print(f"  {port}/tcp  open   {service}")

        if result['filtered_ports']:
            print(f"\n{XSSColors.WARNING}Filtered Ports:{XSSColors.RESET}")
            for port in result['filtered_ports']:
                print(f"  {port}/tcp  filtered")

        if result['vulnerabilities']:
            print(f"\n{XSSColors.DANGER}Vulnerabilities:{XSSColors.RESET}")
            for vuln in result['vulnerabilities']:
                print(f"  - {vuln}")

    def wireshark_capture(self, interface: str = "eth0", duration: int = 10) -> dict:
        """Симуляция перехвата трафика Wireshark"""
        print(f"\n{XSSColors.INFO}📡 Запуск Wireshark на интерфейсе {interface}...{XSSColors.RESET}")

        packets = []
        protocols = ["TCP", "UDP", "HTTP", "HTTPS", "SSH", "FTP", "DNS"]

        for i in range(duration):
            print(f"\rПерехват пакетов... {i + 1}/{duration}s", end="", flush=True)
            time.sleep(1)

            # Генерируем случайные пакеты
            for _ in range(random.randint(5, 20)):
                packet = {
                    "timestamp": time.time(),
                    "protocol": random.choice(protocols),
                    "src_ip": f"192.168.1.{random.randint(1, 254)}",
                    "dst_ip": f"10.0.0.{random.randint(1, 254)}",
                    "src_port": random.randint(1024, 65535),
                    "dst_port": random.choice([80, 443, 22, 21, 25, 53]),
                    "size": random.randint(64, 1500)
                }
                packets.append(packet)

        print(f"\n\n{XSSColors.SUCCESS}Захвачено {len(packets)} пакетов{XSSColors.RESET}")

        # Анализ трафика
        self._analyze_traffic(packets)

        return {"packets": packets, "count": len(packets)}

    def _analyze_traffic(self, packets: list):
        """Анализ захваченного трафика"""
        protocols = {}
        suspicious_activity = []

        for packet in packets:
            protocol = packet["protocol"]
            protocols[protocol] = protocols.get(protocol, 0) + 1

            # Поиск подозрительной активности
            if packet["dst_port"] in [22, 23] and packet["protocol"] == "TCP":
                suspicious_activity.append(f"SSH/Telnet connection to {packet['dst_ip']}")

        print(f"\n{XSSColors.INFO}📊 Анализ трафика:{XSSColors.RESET}")
        for protocol, count in protocols.items():
            print(f"  {protocol}: {count} пакетов")

        if suspicious_activity:
            print(f"\n{XSSColors.WARNING}⚠ Подозрительная активность:{XSSColors.RESET}")
            for activity in suspicious_activity[:5]:
                print(f"  - {activity}")

    def metasploit_exploit(self, target: str, exploit: str) -> dict:
        """Симуляция Metasploit эксплойта"""
        if target not in self.network_system.nodes:
            return {"error": "Цель не найдена"}

        node = self.network_system.nodes[target]

        print(f"\n{XSSColors.DANGER}💀 Запуск Metasploit против {target}...{XSSColors.RESET}")
        print(f"Эксплойт: {exploit}")

        # Симуляция загрузки модуля
        loading_steps = [
            "Загрузка модуля эксплойта...",
            "Проверка совместимости цели...",
            "Настройка полезной нагрузки...",
            "Запуск атаки..."
        ]

        for step in loading_steps:
            print(f"\r{step}", end="", flush=True)
            time.sleep(1.5)
        print()

        # Проверка успешности атаки
        success_chance = 0.3  # Базовый шанс

        # Факторы влияющие на успех
        if exploit in node.vulnerabilities:
            success_chance += 0.4

        if node.firewall and node.firewall.is_active:
            success_chance -= 0.2

        if node.ids_system and node.ids_system.is_active:
            success_chance -= 0.1

        # Навыки игрока
        cracking_skill = game_state.get_skill("cracking")
        success_chance += cracking_skill * 0.05

        success = random.random() < success_chance

        result = {
            "target": target,
            "exploit": exploit,
            "success": success,
            "timestamp": time.time()
        }

        if success:
            print(f"\n{XSSColors.SUCCESS}✅ ЭКСПЛОЙТ УСПЕШЕН!{XSSColors.RESET}")
            print(f"Получен доступ к {node.name}")

            # Компрометируем узел
            self.network_system.compromise_node(target)

            # Награды
            btc_reward = node.security_level * 40
            rep_reward = node.security_level * 8

            game_state.earn_currency(btc_reward, "btc_balance")
            game_state.modify_stat("reputation", rep_reward)

            result["rewards"] = {"btc": btc_reward, "reputation": rep_reward}

        else:
            print(f"\n{XSSColors.ERROR}❌ Эксплойт провалился{XSSColors.RESET}")

            # Штрафы за провал
            heat_gain = random.randint(10, 25)
            game_state.modify_stat("heat_level", heat_gain)
            print(f"{XSSColors.DANGER}Heat Level +{heat_gain}%{XSSColors.RESET}")

        return result


class VPNManager:
    """Менеджер VPN соединений"""

    def __init__(self):
        self.available_vpns = self._generate_vpn_providers()
        self.active_vpn = None
        self.connection_history = []

    def _generate_vpn_providers(self) -> list:
        """Генерирует список VPN провайдеров"""
        providers = [
            {"name": "CyberGhost", "countries": ["US", "UK", "DE", "NL"], "cost": 0.02, "anonymity": 0.85},
            {"name": "NordVPN", "countries": ["US", "CA", "SE", "CH"], "cost": 0.03, "anonymity": 0.90},
            {"name": "ExpressVPN", "countries": ["US", "UK", "JP", "AU"], "cost": 0.05, "anonymity": 0.95},
            {"name": "DarkNet VPN", "countries": ["RU", "CN", "IR"], "cost": 0.08, "anonymity": 0.98},
            {"name": "TorVPN", "countries": ["TOR"], "cost": 0.01, "anonymity": 0.75}
        ]

        vpn_list = []
        for provider in providers:
            for country in provider["countries"]:
                vpn_list.append(VPNConnection(country, provider["name"]))
                vpn_list[-1].cost_per_hour = provider["cost"]
                vpn_list[-1].anonymity_level = provider["anonymity"]

        return vpn_list

    def show_vpn_list(self):
        """Показать список доступных VPN"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ VPN ПРОВАЙДЕРЫ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        if self.active_vpn:
            print(f"\n{XSSColors.SUCCESS}🔒 Активное соединение:{XSSColors.RESET}")
            print(f"   {self.active_vpn.provider} ({self.active_vpn.country})")
            print(f"   Анонимность: {self.active_vpn.anonymity_level:.1%}")
            print(f"   Стоимость: ${self.active_vpn.cost_per_hour:.3f}/час")

        print(f"\n{XSSColors.INFO}📋 Доступные VPN:{XSSColors.RESET}")

        for i, vpn in enumerate(self.available_vpns, 1):
            status = "🔒" if vpn == self.active_vpn else "🔓"
            print(f"   {i:2d}. {status} {vpn.provider:<12} ({vpn.country}) - "
                  f"Анонимность: {vpn.anonymity_level:.1%}, "
                  f"${vpn.cost_per_hour:.3f}/ч")

    def connect_vpn(self, vpn_index: int) -> bool:
        """Подключиться к VPN"""
        if not (1 <= vpn_index <= len(self.available_vpns)):
            print(f"{XSSColors.ERROR}Неверный номер VPN{XSSColors.RESET}")
            return False

        vpn = self.available_vpns[vpn_index - 1]

        # Проверяем средства
        btc_balance = game_state.get_stat("btc_balance", 0)
        if btc_balance < vpn.cost_per_hour:
            print(f"{XSSColors.ERROR}Недостаточно BTC для подключения{XSSColors.RESET}")
            return False

        # Отключаем текущий VPN
        if self.active_vpn:
            self.disconnect_vpn()

        # Подключаемся
        print(f"\n{XSSColors.INFO}🔒 Подключение к {vpn.provider} ({vpn.country})...{XSSColors.RESET}")
        time.sleep(2)

        vpn.is_active = True
        self.active_vpn = vpn

        # Списываем оплату
        game_state.spend_currency(vpn.cost_per_hour, "btc_balance")

        print(f"{XSSColors.SUCCESS}✅ VPN подключен!{XSSColors.RESET}")
        print(f"Ваш новый IP: {self._generate_fake_ip(vpn.country)}")
        print(f"Уровень анонимности: {vpn.anonymity_level:.1%}")

        # Снижаем heat level
        heat_reduction = int(vpn.anonymity_level * 20)
        game_state.modify_stat("heat_level", -heat_reduction)
        print(f"{XSSColors.SUCCESS}Heat Level -{heat_reduction}%{XSSColors.RESET}")

        return True

    def disconnect_vpn(self):
        """Отключить VPN"""
        if not self.active_vpn:
            print(f"{XSSColors.WARNING}VPN не подключен{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.INFO}Отключение от {self.active_vpn.provider}...{XSSColors.RESET}")

        self.active_vpn.is_active = False
        self.active_vpn = None

        print(f"{XSSColors.SUCCESS}✅ VPN отключен{XSSColors.RESET}")
        print(f"Ваш IP: {self._generate_fake_ip('LOCAL')}")

    def _generate_fake_ip(self, country: str) -> str:
        """Генерирует поддельный IP адрес"""
        country_ranges = {
            "US": "192.168",
            "UK": "172.16",
            "DE": "10.0",
            "RU": "203.0",
            "TOR": "127.0"
        }

        prefix = country_ranges.get(country, "192.168")
        return f"{prefix}.{random.randint(1, 255)}.{random.randint(1, 255)}"

    def get_anonymity_bonus(self) -> float:
        """Получить бонус анонимности от VPN"""
        if self.active_vpn:
            return self.active_vpn.anonymity_level
        return 0.0


class BotnetManager:
    """Менеджер ботнетов"""

    def __init__(self):
        self.owned_botnets = []
        self.available_botnets = self._generate_market_botnets()

    def _generate_market_botnets(self) -> list:
        """Генерирует ботнеты на продажу"""
        names = ["Zeus", "Conficker", "Mirai", "Sality", "Necurs", "Dridex"]
        botnets = []

        for name in names:
            botnet = Botnet(f"{name}-{random.randint(1000, 9999)}")
            bot_count = random.randint(100, 10000)

            for i in range(bot_count):
                bot_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
                bot_info = {
                    "country": random.choice(["US", "RU", "CN", "DE", "BR"]),
                    "bandwidth": random.randint(5, 100),
                    "os": random.choice(["Windows", "Linux", "Android"])
                }
                botnet.add_bot(bot_ip, bot_info)

            botnets.append(botnet)

        return botnets

    def show_botnet_market(self):
        """Показать рынок ботнетов"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ БОТНЕТ МАРКЕТ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        if self.owned_botnets:
            print(f"\n{XSSColors.SUCCESS}🤖 Ваши ботнеты:{XSSColors.RESET}")
            for i, botnet in enumerate(self.owned_botnets, 1):
                print(f"   {i}. {botnet.name} - {len(botnet.bots)} ботов, "
                      f"{botnet.total_bandwidth} Mbps")

        print(f"\n{XSSColors.INFO}💰 Доступные для покупки:{XSSColors.RESET}")
        for i, botnet in enumerate(self.available_botnets, 1):
            price = len(botnet.bots) * 0.05  # 0.05 BTC за бота
            print(f"   {i}. {botnet.name}")
            print(f"      Ботов: {len(botnet.bots)}")
            print(f"      Общая пропускная способность: {botnet.total_bandwidth} Mbps")
            print(f"      Цена: {price:.2f} BTC")
            print()

    def buy_botnet(self, botnet_index: int) -> bool:
        """Купить ботнет"""
        if not (1 <= botnet_index <= len(self.available_botnets)):
            print(f"{XSSColors.ERROR}Неверный номер ботнета{XSSColors.RESET}")
            return False

        botnet = self.available_botnets[botnet_index - 1]
        price = len(botnet.bots) * 0.01

        if not game_state.can_afford(price, "btc_balance"):
            print(f"{XSSColors.ERROR}Недостаточно BTC (нужно {price:.2f}){XSSColors.RESET}")
            return False

        # Покупаем
        game_state.spend_currency(price, "btc_balance")

        # Переносим в собственность
        self.owned_botnets.append(botnet)
        self.available_botnets.remove(botnet)

        print(f"\n{XSSColors.SUCCESS}✅ Ботнет {botnet.name} приобретен!{XSSColors.RESET}")
        print(f"Под вашим контролем {len(botnet.bots)} ботов")

        return True

    def launch_ddos(self, target: str, botnet_index: int = None) -> dict:
        """Запустить DDoS атаку"""
        if not self.owned_botnets:
            print(f"{XSSColors.ERROR}У вас нет ботнетов{XSSColors.RESET}")
            return {"success": False, "error": "No botnets"}

        # Выбираем ботнет
        if botnet_index is None:
            botnet = max(self.owned_botnets, key=lambda b: len(b.bots))
        else:
            if not (1 <= botnet_index <= len(self.owned_botnets)):
                print(f"{XSSColors.ERROR}Неверный номер ботнета{XSSColors.RESET}")
                return {"success": False, "error": "Invalid botnet"}
            botnet = self.owned_botnets[botnet_index - 1]

        if target not in network_system.nodes:
            print(f"{XSSColors.ERROR}Цель не найдена{XSSColors.RESET}")
            return {"success": False, "error": "Target not found"}

        target_node = network_system.nodes[target]

        print(f"\n{XSSColors.DANGER}💥 ЗАПУСК DDOS АТАКИ{XSSColors.RESET}")
        print(f"Цель: {target_node.name}")
        print(f"Ботнет: {botnet.name}")
        print(f"Количество ботов: {len(botnet.bots)}")
        print(f"Общая мощность: {botnet.total_bandwidth} Mbps")

        # Симуляция атаки
        attack_duration = random.randint(30, 120)  # секунды
        print(f"\n{XSSColors.WARNING}⚡ Атака началась! Длительность: {attack_duration}s{XSSColors.RESET}")

        # Факторы успеха
        attack_power = botnet.total_bandwidth
        target_defense = target_node.security_level * 100

        if target_node.firewall and target_node.firewall.is_active:
            target_defense *= 1.5

        success_chance = min(0.9, attack_power / (attack_power + target_defense))

        # Прогресс атаки
        for i in range(10):
            time.sleep(0.5)
            progress = (i + 1) * 10
            print(f"\rАтака: [{'█' * (i + 1)}{'░' * (9 - i)}] {progress}%", end="", flush=True)

        print(f"\n")

        success = random.random() < success_chance

        result = {
            "target": target,
            "botnet": botnet.name,
            "success": success,
            "duration": attack_duration,
            "timestamp": time.time()
        }

        if success:
            print(f"\n{XSSColors.SUCCESS}💥 АТАКА УСПЕШНА!{XSSColors.RESET}")
            print(f"{target_node.name} недоступен в течение {attack_duration} минут")

            # Награды
            btc_reward = len(botnet.bots) * 0.001
            rep_reward = target_node.security_level * 5

            game_state.earn_currency(btc_reward, "btc_balance")
            game_state.modify_stat("reputation", rep_reward)

            # Помечаем узел как недоступный
            target_node.uptime = 0

            result["rewards"] = {"btc": btc_reward, "reputation": rep_reward}

        else:
            print(f"\n{XSSColors.ERROR}❌ Атака отражена!{XSSColors.RESET}")
            print(f"Защитные системы {target_node.name} выдержали нагрузку")

            # Штрафы
            heat_gain = random.randint(20, 40)
            game_state.modify_stat("heat_level", heat_gain)
            print(f"{XSSColors.DANGER}Heat Level +{heat_gain}%{XSSColors.RESET}")

        # Небольшой шанс потерять ботов
        bots_lost = random.randint(0, len(botnet.bots) // 20)
        if bots_lost > 0:
            botnet.bots = botnet.bots[bots_lost:]
            botnet.total_bandwidth -= bots_lost * 10
            print(f"{XSSColors.WARNING}Потеряно {bots_lost} ботов в ходе атаки{XSSColors.RESET}")

        return result


class NetworkSystem:
    """Система управления сетью"""

    def __init__(self):
        self.nodes = {}
        self.discovered_nodes = set()
        self.current_path = []

        # НОВЫЕ компоненты
        self.network_tools = NetworkTools(self)
        self.vpn_manager = VPNManager()
        self.botnet_manager = BotnetManager()

        self._initialize_base_network()
        self._initialize_advanced_network()  # НОВЫЙ метод

    def _initialize_base_network(self) -> None:
        """Инициализирует базовую сеть"""
        # Localhost - стартовый узел
        localhost = NetworkNode("127.0.0.1", "localhost", "personal")
        localhost.security_level = 0
        localhost.is_compromised = True
        localhost.owner = "player"
        self.nodes["localhost"] = localhost
        self.discovered_nodes.add("localhost")

        # Базовые узлы интернета
        base_nodes = [
            ("8.8.8.8", "Google DNS", "dns", ["dns_service"], 3),
            ("1.1.1.1", "Cloudflare DNS", "dns", ["dns_service"], 3),
            ("forum.xss.is", "XSS Forum", "webserver", ["http", "https"], 2),
            ("market.darknet", "Dark Market", "webserver", ["http", "tor"], 4),
            ("bank.secure.net", "SecureBank", "webserver", ["https", "ssh"], 5),
            ("corp.megasoft.com", "MegaSoft Corp", "corporate", ["http", "https", "ftp"], 4),
            ("gov.agency.mil", "Government Server", "government", ["https", "ssh"], 8),
            ("news.hackerz.net", "Hacker News", "webserver", ["http"], 1),
            ("vpn.cyberghost.com", "CyberGhost VPN", "vpn_server", ["https", "openvpn"], 6),
            ("mail.tempmail.org", "TempMail Service", "webserver", ["http", "smtp"], 2),
            ("cloud.storage.net", "Cloud Storage", "webserver", ["https", "ftp"], 5),
            ("router.home.lan", "Home Router", "router", ["telnet", "http"], 1),
            ("camera.security.cam", "Security Camera", "iot", ["http"], 1),
            ("server.university.edu", "University Server", "educational", ["http", "ssh"], 3)
        ]

        for address, name, node_type, services, security in base_nodes:
            node = NetworkNode(address, name, node_type)
            node.services = services
            node.security_level = security

            # Добавляем случайные уязвимости в зависимости от уровня безопасности
            if security < 5:
                vulns = random.sample([
                    "outdated_ssl", "weak_password", "sql_injection",
                    "buffer_overflow", "default_config", "unpatched_service",
                    "directory_traversal", "cross_site_scripting", "csrf_vulnerability",
                    "information_disclosure", "privilege_escalation"
                ], random.randint(1, 3))
                node.vulnerabilities = vulns

            # Устанавливаем OS тип
            if node_type == "government":
                node.os_type = "Windows Server"
            elif node_type == "router":
                node.os_type = "Embedded Linux"
            elif node_type == "iot":
                node.os_type = "Embedded"
            else:
                node.os_type = random.choice(["Linux", "Windows", "FreeBSD"])

            self.nodes[address] = node

        # Создаем связи между узлами
        self._generate_network_topology()
    def _initialize_advanced_network(self) -> None:
        """Инициализирует продвинутую сеть с защитными системами"""
        # Добавляем файрволы к серверам
        for address, node in self.nodes.items():
            if node.type in ["corporate", "government", "webserver"]:
                if node.security_level >= 3:
                    firewall_type = "basic" if node.security_level < 6 else "advanced"
                    node.firewall = Firewall(firewall_type)

                if node.security_level >= 5:
                    ids_type = "signature" if node.security_level < 8 else "hybrid"
                    node.ids_system = IDSSystem(ids_type)

                # Добавляем honeypots к высокозащищенным узлам
                if node.security_level >= 7:
                    honeypot_types = ["ssh", "web", "ftp"]
                    for hp_type in random.sample(honeypot_types, random.randint(1, 2)):
                        node.honeypots.append(Honeypot(hp_type))

        # Создаем более реалистичные подсети
        self._create_subnets()

        # Добавляем географическую информацию
        self._assign_geo_locations()

    def _create_subnets(self) -> None:
        """Создает подсети для узлов"""
        subnets = {
            "corporate": "10.0.0.0/24",
            "government": "172.16.0.0/24",
            "webserver": "192.168.1.0/24",
            "dns": "8.8.8.0/24"
        }

        for address, node in self.nodes.items():
            if node.type in subnets:
                node.subnet = subnets[node.type]

    def _assign_geo_locations(self) -> None:
        """Назначает географические локации узлам"""
        locations = [
            {"country": "US", "city": "New York"},
            {"country": "UK", "city": "London"},
            {"country": "DE", "city": "Berlin"},
            {"country": "RU", "city": "Moscow"},
            {"country": "CN", "city": "Beijing"},
            {"country": "JP", "city": "Tokyo"}
        ]

        for address, node in self.nodes.items():
            node.geo_location = random.choice(locations)

    def _generate_network_topology(self) -> None:
        """Генерирует топологию сети"""
        # Localhost подключен к DNS серверам и домашнему роутеру
        self.nodes["localhost"].connected_nodes = ["8.8.8.8", "1.1.1.1", "router.home.lan"]

        # DNS серверы знают о многих узлах
        self.nodes["8.8.8.8"].connected_nodes = [
            "forum.xss.is", "news.hackerz.net", "corp.megasoft.com",
            "mail.tempmail.org", "server.university.edu"
        ]
        self.nodes["1.1.1.1"].connected_nodes = [
            "bank.secure.net", "market.darknet", "cloud.storage.net", "vpn.cyberghost.com"
        ]

        # Веб-серверы связаны между собой
        self.nodes["forum.xss.is"].connected_nodes = ["market.darknet", "news.hackerz.net"]
        self.nodes["news.hackerz.net"].connected_nodes = ["forum.xss.is", "server.university.edu"]
        self.nodes["mail.tempmail.org"].connected_nodes = ["forum.xss.is"]

        # Корпоративные серверы изолированы, но связаны с банками
        self.nodes["corp.megasoft.com"].connected_nodes = ["bank.secure.net", "cloud.storage.net"]
        self.nodes["bank.secure.net"].connected_nodes = ["corp.megasoft.com"]

        # Правительственные серверы максимально изолированы
        self.nodes["gov.agency.mil"].connected_nodes = ["bank.secure.net"]

        # Домашний роутер подключен к IoT устройствам
        self.nodes["router.home.lan"].connected_nodes = ["camera.security.cam", "localhost"]

        # Камера видеонаблюдения подключена только к роутеру
        self.nodes["camera.security.cam"].connected_nodes = ["router.home.lan"]

        # VPN сервер доступен из многих мест
        self.nodes["vpn.cyberghost.com"].connected_nodes = ["forum.xss.is", "market.darknet"]

        # Облачное хранилище доступно корпорациям
        self.nodes["cloud.storage.net"].connected_nodes = ["corp.megasoft.com", "server.university.edu"]

        # Университетский сервер связан с образовательными ресурсами
        self.nodes["server.university.edu"].connected_nodes = ["news.hackerz.net", "cloud.storage.net"]

    def get_current_node(self) -> Optional[NetworkNode]:
        """Получает текущий узел"""
        current_address = game_state.get_stat("current_node", "localhost")
        return self.nodes.get(current_address)

    def show_network_map(self) -> None:
        """Показывает карту сети"""
        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━ КАРТА СЕТИ ━━━━━━━━━━━━━━━━{XSSColors.RESET}")

        current_node = self.get_current_node()
        if current_node:
            print(
                f"\n{XSSColors.INFO}📍 Текущее местоположение: {XSSColors.BRIGHT_GREEN}{current_node.name}{XSSColors.RESET}")
            print(f"   Адрес: {current_node.address}")
            print(f"   Тип: {current_node.type}")

            if current_node.is_compromised:
                print(f"   Статус: {XSSColors.SUCCESS}✓ Скомпрометирован{XSSColors.RESET}")
            else:
                print(f"   Статус: {XSSColors.ERROR}✗ Защищен{XSSColors.RESET}")

        # Показываем обнаруженные узлы
        print(f"\n{XSSColors.WARNING}🌐 ОБНАРУЖЕННЫЕ УЗЛЫ:{XSSColors.RESET}")

        discovered_count = 0
        for address in sorted(self.discovered_nodes):
            if address in self.nodes:
                node = self.nodes[address]
                discovered_count += 1

                # Определяем цвет по типу и статусу
                if node.is_compromised:
                    color = XSSColors.SUCCESS
                    icon = "✓"
                elif node.security_level >= 7:
                    color = XSSColors.ERROR
                    icon = "⚠"
                elif node.security_level >= 4:
                    color = XSSColors.WARNING
                    icon = "!"
                else:
                    color = XSSColors.INFO
                    icon = "•"

                print(f"\n   {icon} [{color}{address}{XSSColors.RESET}] {node.name}")
                print(f"      Тип: {node.type} | Безопасность: {self._get_security_bar(node.security_level)}")

                if node.services:
                    print(f"      Сервисы: {', '.join(node.services)}")

                if node.is_compromised and node.vulnerabilities:
                    print(f"      {XSSColors.SUCCESS}Уязвимости: {', '.join(node.vulnerabilities)}{XSSColors.RESET}")

        undiscovered = len(self.nodes) - discovered_count
        print(f"\n{XSSColors.INFO}Обнаружено узлов: {discovered_count}/{len(self.nodes)}{XSSColors.RESET}")

        if current_node and current_node.connected_nodes:
            print(f"\n{XSSColors.INFO}🔗 Доступные соединения:{XSSColors.RESET}")
            for connected in current_node.connected_nodes:
                if connected in self.discovered_nodes:
                    connected_node = self.nodes.get(connected)
                    if connected_node:
                        print(f"   → {connected} ({connected_node.name})")
                else:
                    print(f"   → {connected} (неизвестный узел)")

        print(f"\n{XSSColors.HEADER}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{XSSColors.RESET}")

    def _get_security_bar(self, level: int) -> str:
        """Возвращает визуальное представление уровня безопасности"""
        max_level = 10
        filled = "█" * level
        empty = "░" * (max_level - level)

        if level >= 7:
            color = XSSColors.ERROR
        elif level >= 4:
            color = XSSColors.WARNING
        else:
            color = XSSColors.SUCCESS

        return f"{color}{filled}{empty}{XSSColors.RESET}"

    def connect_to_node(self, target_address: str) -> bool:
        """Подключается к узлу"""
        current_node = self.get_current_node()
        if not current_node:
            print(f"{XSSColors.ERROR}Ошибка: текущий узел не найден{XSSColors.RESET}")
            return False

        # Проверяем, можем ли подключиться
        if target_address not in current_node.connected_nodes:
            print(f"{XSSColors.ERROR}Нет прямого соединения с {target_address}{XSSColors.RESET}")
            print(f"{XSSColors.INFO}Используйте 'scan' для поиска доступных узлов{XSSColors.RESET}")
            return False

        if target_address not in self.nodes:
            print(f"{XSSColors.ERROR}Узел {target_address} не существует{XSSColors.RESET}")
            return False

        target_node = self.nodes[target_address]

        # Анимация подключения
        print(f"\n{XSSColors.INFO}Подключение к {target_node.name}...{XSSColors.RESET}")
        self._show_connection_animation()

        # Проверка безопасности
        if not target_node.is_compromised and target_node.security_level > 0:
            print(f"{XSSColors.WARNING}⚠ Обнаружена система защиты!{XSSColors.RESET}")
            print(f"Уровень безопасности: {self._get_security_bar(target_node.security_level)}")

            # Проверяем навыки для обхода
            skill_check = self._perform_security_check(target_node)
            if not skill_check:
                print(f"{XSSColors.ERROR}❌ Подключение отклонено системой безопасности{XSSColors.RESET}")

                # Повышаем heat
                heat_gain = target_node.security_level * 2
                game_state.modify_stat("heat_level", heat_gain)
                print(f"{XSSColors.DANGER}[!] Heat Level +{heat_gain}%{XSSColors.RESET}")

                return False

        # Успешное подключение
        self.current_path.append(current_node.address)
        game_state.set_stat("current_node", target_address)

        # Добавляем в обнаруженные
        self.discovered_nodes.add(target_address)

        audio_system.play_sound("connection")
        print(f"{XSSColors.SUCCESS}✅ Подключение установлено{XSSColors.RESET}")

        # Обнаруживаем новые узлы
        self._discover_connected_nodes(target_node)

        # Показываем информацию об узле
        self._show_node_info(target_node)

        return True

    def _show_connection_animation(self) -> None:
        """Анимация подключения"""
        steps = ["Резолвинг DNS...", "Установка TCP соединения...", "Обход файрвола...", "Аутентификация..."]

        for step in steps:
            print(f"\r   {XSSColors.INFO}{step}{XSSColors.RESET}", end='', flush=True)
            time.sleep(0.5)

        print()  # Новая строка

    def _perform_security_check(self, node: NetworkNode) -> bool:
        """Проверяет, может ли игрок обойти защиту"""
        # Получаем навыки игрока
        scanning = game_state.get_skill("scanning")
        cracking = game_state.get_skill("cracking")
        stealth = game_state.get_skill("stealth")

        # Считаем общую силу атаки
        attack_power = scanning + cracking + (stealth * 2)  # Stealth важнее

        # Сложность = уровень безопасности * 3
        difficulty = node.security_level * 3

        # Добавляем случайность
        roll = random.randint(1, 20)
        total = attack_power + roll

        print(f"\n{XSSColors.INFO}Попытка обхода защиты...{XSSColors.RESET}")
        print(f"Ваши навыки: {attack_power} + бросок: {roll} = {total}")
        print(f"Требуется: {difficulty}")

        return total >= difficulty

    def _discover_connected_nodes(self, node: NetworkNode) -> None:
        """Обнаруживает подключенные узлы"""
        new_discoveries = []

        for connected_address in node.connected_nodes:
            if connected_address not in self.discovered_nodes:
                self.discovered_nodes.add(connected_address)
                new_discoveries.append(connected_address)

        if new_discoveries:
            print(f"\n{XSSColors.SUCCESS}🔍 Обнаружены новые узлы:{XSSColors.RESET}")
            for addr in new_discoveries:
                if addr in self.nodes:
                    discovered_node = self.nodes[addr]
                    print(f"   + {addr} ({discovered_node.name})")
                else:
                    print(f"   + {addr} (неизвестный)")

    def _show_node_info(self, node: NetworkNode) -> None:
        """Показывает информацию об узле"""
        print(f"\n{XSSColors.INFO}━━━ ИНФОРМАЦИЯ ОБ УЗЛЕ ━━━{XSSColors.RESET}")
        print(f"Имя: {node.name}")
        print(f"Адрес: {node.address}")
        print(f"Тип: {node.type}")
        print(f"Владелец: {node.owner}")

        if node.services:
            print(f"\nАктивные сервисы:")
            for service in node.services:
                port = self._get_service_port(service)
                print(f"   • {service} (port {port})")

        if node.is_compromised and node.vulnerabilities:
            print(f"\n{XSSColors.WARNING}Обнаруженные уязвимости:{XSSColors.RESET}")
            for vuln in node.vulnerabilities:
                print(f"   ⚠ {vuln}")

    def _get_service_port(self, service: str) -> int:
        """Возвращает порт для сервиса"""
        ports = {
            "http": 80,
            "https": 443,
            "ssh": 22,
            "ftp": 21,
            "telnet": 23,
            "smtp": 25,
            "dns_service": 53,
            "tor": 9050
        }
        return ports.get(service, 0)

    def disconnect(self) -> bool:
        """Отключается от текущего узла"""
        current_node = self.get_current_node()
        if not current_node:
            print(f"{XSSColors.ERROR}Вы не подключены ни к какому узлу{XSSColors.RESET}")
            return False

        if current_node.address == "localhost":
            print(f"{XSSColors.WARNING}Вы уже на localhost{XSSColors.RESET}")
            return False

        # Возвращаемся к предыдущему узлу
        if self.current_path:
            previous = self.current_path.pop()
            game_state.set_stat("current_node", previous)

            print(f"{XSSColors.INFO}Отключение от {current_node.name}...{XSSColors.RESET}")
            time.sleep(1)
            print(f"{XSSColors.SUCCESS}✅ Возврат к {previous}{XSSColors.RESET}")
        else:
            # Возвращаемся на localhost
            game_state.set_stat("current_node", "localhost")
            print(f"{XSSColors.SUCCESS}✅ Возврат на localhost{XSSColors.RESET}")

        return True

    def scan_network(self) -> None:
        """Сканирует текущую сеть"""
        current_node = self.get_current_node()
        if not current_node:
            print(f"{XSSColors.ERROR}Ошибка: текущий узел не найден{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.INFO}🔍 Сканирование сети от {current_node.name}...{XSSColors.RESET}")

        # Анимация сканирования
        scan_duration = 3
        for i in range(scan_duration):
            progress = (i + 1) / scan_duration
            bar = progress_bar(i + 1, scan_duration, length=30)
            print(f"\r{bar} Сканирование...", end='', flush=True)
            time.sleep(1)

        print(f"\n\n{XSSColors.SUCCESS}✅ Сканирование завершено{XSSColors.RESET}")

        # Показываем результаты
        if current_node.connected_nodes:
            print(f"\n{XSSColors.INFO}Обнаруженные узлы:{XSSColors.RESET}")

            for addr in current_node.connected_nodes:
                if addr in self.nodes:
                    node = self.nodes[addr]

                    # Определяем статус
                    if node.is_compromised:
                        status = f"{XSSColors.SUCCESS}[ВЗЛОМАН]{XSSColors.RESET}"
                    elif addr in self.discovered_nodes:
                        status = f"{XSSColors.WARNING}[ИЗВЕСТЕН]{XSSColors.RESET}"
                    else:
                        status = f"{XSSColors.INFO}[НОВЫЙ]{XSSColors.RESET}"
                        # Добавляем в обнаруженные
                        self.discovered_nodes.add(addr)

                    print(f"\n   {status} {addr}")
                    print(f"   Имя: {node.name}")
                    print(f"   Тип: {node.type}")
                    print(f"   Безопасность: {self._get_security_bar(node.security_level)}")
        else:
            print(f"{XSSColors.WARNING}Не обнаружено подключенных узлов{XSSColors.RESET}")

        # Шанс обнаружить скрытые узлы при высоком навыке
        if game_state.get_skill("scanning") >= 5:
            if random.random() < 0.3:
                self._discover_hidden_node()

    def _discover_hidden_node(self) -> None:
        """Обнаруживает скрытый узел"""
        hidden_nodes = [
            ("10.0.0.1", "Hidden Server", "hidden", ["ssh"], 6),
            ("192.168.1.1", "Local Router", "router", ["telnet", "http"], 2),
            ("onion.site", "Dark Market VIP", "darknet", ["tor"], 7),
            ("zero.day", "0-Day Exchange", "underground", ["https"], 8)
        ]

        # Выбираем случайный скрытый узел
        address, name, node_type, services, security = random.choice(hidden_nodes)

        if address not in self.nodes:
            node = NetworkNode(address, name, node_type)
            node.services = services
            node.security_level = security
            self.nodes[address] = node

            # Добавляем связь с текущим узлом
            current_node = self.get_current_node()
            if current_node and address not in current_node.connected_nodes:
                current_node.connected_nodes.append(address)

            self.discovered_nodes.add(address)

            print(f"\n{XSSColors.SUCCESS}🎯 ОБНАРУЖЕН СКРЫТЫЙ УЗЕЛ!{XSSColors.RESET}")
            print(f"   Адрес: {address}")
            print(f"   Имя: {name}")
            audio_system.play_sound("discovery")

    def traceroute(self, target_address: str) -> None:
        """Трассировка маршрута до цели"""
        if target_address not in self.discovered_nodes:
            print(f"{XSSColors.ERROR}Неизвестный адрес: {target_address}{XSSColors.RESET}")
            return

        if target_address not in self.nodes:
            print(f"{XSSColors.ERROR}Узел не существует{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.INFO}🛤️ Трассировка маршрута до {target_address}...{XSSColors.RESET}")

        # Симулируем трассировку
        hops = self._calculate_route(target_address)

        if not hops:
            print(f"{XSSColors.ERROR}Маршрут не найден{XSSColors.RESET}")
            return

        print(f"\n{XSSColors.SUCCESS}Маршрут найден ({len(hops)} хопов):{XSSColors.RESET}")

        for i, hop in enumerate(hops):
            time.sleep(0.3)
            if hop in self.nodes:
                node = self.nodes[hop]
                latency = random.randint(10, 100) * (i + 1)
                print(f"   {i + 1}. {hop} ({node.name}) - {latency}ms")
            else:
                print(f"   {i + 1}. {hop} (unknown) - timeout")

    def _calculate_route(self, target: str) -> List[str]:
        """Вычисляет маршрут до цели (упрощенный BFS)"""
        current = game_state.get_stat("current_node", "localhost")

        if current == target:
            return [target]

        # Простой поиск пути
        visited = set()
        queue = [(current, [current])]

        while queue:
            node_addr, path = queue.pop(0)

            if node_addr == target:
                return path

            if node_addr in visited:
                continue

            visited.add(node_addr)

            if node_addr in self.nodes:
                node = self.nodes[node_addr]
                for connected in node.connected_nodes:
                    if connected not in visited:
                        queue.append((connected, path + [connected]))

        return []

    def compromise_node(self, address: str) -> bool:
        """Компрометирует узел (после успешного взлома)"""
        if address not in self.nodes:
            return False

        node = self.nodes[address]
        if node.is_compromised:
            return True

        node.is_compromised = True
        node.owner = "player"

        print(f"\n{XSSColors.SUCCESS}🎯 УЗЕЛ СКОМПРОМЕТИРОВАН!{XSSColors.RESET}")
        print(f"Вы получили контроль над {node.name}")

        # Награды за взлом
        btc_reward = node.security_level * 20
        rep_reward = node.security_level * 5

        game_state.earn_currency(btc_reward, "btc_balance")
        game_state.modify_stat("reputation", rep_reward)

        print(f"{XSSColors.MONEY}[+] {btc_reward} BTC{XSSColors.RESET}")
        print(f"{XSSColors.REP}[+] {rep_reward} репутации{XSSColors.RESET}")

        # Обнаруживаем уязвимости
        if not node.vulnerabilities:
            vulns = random.sample([
                "weak_admin_password", "unpatched_rce", "sql_injection",
                "exposed_api_keys", "misconfigured_firewall"
            ], random.randint(1, 3))
            node.vulnerabilities = vulns

        return True

    def update_network_state(self) -> None:
        """Обновляет состояние сети (вызывается каждые N ходов)"""
        # Случайные события в сети
        if random.random() < 0.1:  # 10% шанс
            self._network_event()

        # Обновляем heat level узлов
        for node in self.nodes.values():
            if node.heat_level > 0:
                node.heat_level = max(0, node.heat_level - 1)

    def _network_event(self) -> None:
        """Генерирует случайное сетевое событие"""
        events = [
            self._new_node_appears,
            self._node_security_update,
            self._network_maintenance,
            self._hacker_activity
        ]

        event = random.choice(events)
        event()

    def _new_node_appears(self) -> None:
        """Появляется новый узел"""
        new_nodes = [
            ("startup.tech", "TechStartup Server", "corporate", ["http", "api"], 3),
            ("blog.personal", "Personal Blog", "personal", ["http"], 1),
            ("store.online", "Online Store", "commerce", ["https", "api"], 4)
        ]

        address, name, node_type, services, security = random.choice(new_nodes)

        if address not in self.nodes:
            node = NetworkNode(address, name, node_type)
            node.services = services
            node.security_level = security
            self.nodes[address] = node

            # Добавляем связь с случайным существующим узлом
            existing = random.choice(list(self.nodes.keys()))
            if existing != address:
                self.nodes[existing].connected_nodes.append(address)

            print(f"\n{XSSColors.INFO}📡 Новый узел появился в сети: {name}{XSSColors.RESET}")

    def _node_security_update(self) -> None:
        """Обновление безопасности узла"""
        # Выбираем случайный не взломанный узел
        candidates = [n for n in self.nodes.values() if not n.is_compromised and n.type != "personal"]

        if candidates:
            node = random.choice(candidates)
            old_level = node.security_level
            node.security_level = min(10, node.security_level + 1)

            if node.address in self.discovered_nodes:
                print(f"\n{XSSColors.WARNING}⚠ {node.name} обновил систему безопасности!{XSSColors.RESET}")
                print(f"Уровень защиты: {old_level} → {node.security_level}")

    def _network_maintenance(self) -> None:
        """Техническое обслуживание сети"""
        # Случайный узел временно недоступен
        candidates = [n for n in self.nodes.values() if n.type != "personal" and n.address != "localhost"]

        if candidates:
            node = random.choice(candidates)
            if node.address in self.discovered_nodes:
                print(f"\n{XSSColors.INFO}🔧 {node.name} на техническом обслуживании{XSSColors.RESET}")

    def _hacker_activity(self) -> None:
        """Активность других хакеров"""
        messages = [
            "Замечена подозрительная активность в сети",
            "Кто-то сканирует корпоративные серверы",
            "Обнаружена попытка DDoS атаки",
            "Неизвестный хакер взломал правительственный сервер"
        ]

        print(f"\n{XSSColors.WARNING}👾 {random.choice(messages)}{XSSColors.RESET}")

    def get_network_stats(self) -> Dict:
        """Возвращает статистику сети"""
        total_nodes = len(self.nodes)
        discovered = len(self.discovered_nodes)
        compromised = sum(1 for n in self.nodes.values() if n.is_compromised)

        return {
            "total_nodes": total_nodes,
            "discovered": discovered,
            "compromised": compromised,
            "discovery_percent": (discovered / total_nodes * 100) if total_nodes > 0 else 0,
            "control_percent": (compromised / total_nodes * 100) if total_nodes > 0 else 0
        }

    def save_network_state(self) -> Dict:
        """Сохраняет состояние сети"""
        return {
            "nodes": {addr: node.to_dict() for addr, node in self.nodes.items()},
            "discovered_nodes": list(self.discovered_nodes),
            "current_path": self.current_path
        }

    def load_network_state(self, data: Dict) -> None:
        """Загружает состояние сети"""
        if "nodes" in data:
            self.nodes = {}
            for addr, node_data in data["nodes"].items():
                self.nodes[addr] = NetworkNode.from_dict(node_data)

        if "discovered_nodes" in data:
            self.discovered_nodes = set(data["discovered_nodes"])

        if "current_path" in data:
            self.current_path = data["current_path"]

# Глобальный экземпляр сетевой системы
network_system = NetworkSystem()