"""
Статические данные игры XSS Game 0.3.0 "DARK WEB EVOLUTION"
Расширенные данные с новыми системами фракций, событий и достижений
"""

# --- Фракции (расширенные данные) ---
FACTIONS = {
    "whitehats": {
        "name": "WhiteHats United",
        "desc": "Этичные хакеры, защищающие цифровой мир от киберугроз",
        "philosophy": "Использовать навыки хакинга для защиты и улучшения кибербезопасности",
        "bonuses": {
            "reputation_multiplier": 2.0,  # Удвоенная репутация за этичные миссии
            "heat_reduction": 25,           # Снижение Heat Level на 25%
            "skill_boost": 1,               # +1 ко всем навыкам
            "special_market": True          # Доступ к этичному рынку
        },
        "exclusive_missions": [
            "bug_bounty_hunt", "corporate_security_audit", "government_consultation",
            "security_conference", "ethical_penetration_test", "vulnerability_research",
            "cyber_defense_drill", "incident_response_training"
        ],
        "special_features": [
            "Доступ к корпоративным контрактам",
            "Легальная защита при операциях",
            "Сотрудничество с правоохранительными органами",
            "Эксклюзивные инструменты безопасности",
            "Возможность проведения официальных пентестов"
        ],
        "enemies": ["BlackHats Collective"],
        "allies": ["Корпорации", "Правительственные агентства"],
        "headquarters": "Кибер-Центр Безопасности, Силиконовая Долина"
    },
    
    "blackhats": {
        "name": "BlackHats Collective", 
        "desc": "Криминальное подполье даркнета, живущее вне закона",
        "philosophy": "Власть через код, деньги через взлом, свобода через анонимность",
        "bonuses": {
            "btc_multiplier": 2.5,         # В 2.5 раза больше BTC за миссии
            "risk_reduction": -10,          # Меньше шанс провала опасных миссий
            "heat_immunity": 15,            # Частичная защита от Heat Level
            "dark_market_access": True      # Доступ к черному рынку
        },
        "exclusive_missions": [
            "crypto_exchange_hack", "ransomware_deployment", "corporate_espionage",
            "government_data_theft", "financial_fraud", "dark_web_empire",
            "botnet_creation", "zero_day_trading", "cryptocurrency_laundering"
        ],
        "special_features": [
            "Доступ к криминальным сетям",
            "Торговля на черном рынке",
            "Защита от правоохранительных органов",
            "Эксклюзивные малварь и эксплойты",
            "Возможность создания собственной криминальной организации"
        ],
        "enemies": ["WhiteHats United"],
        "allies": ["Криминальные синдикаты", "Коррумпированные чиновники"],
        "headquarters": "Скрытые серверы в даркнете"
    },
    
    "grayhats": {
        "name": "GrayHats Syndicate",
        "desc": "Свободные агенты, играющие по своим правилам между светом и тьмой",
        "philosophy": "Мораль относительна, важна только эффективность и результат",
        "bonuses": {
            "mission_variety": True,        # Доступ к миссиям всех фракций
            "skill_boost": 2,               # +2 ко всем навыкам
            "faction_immunity": True,       # Защита от фракционных войн
            "freelancer_bonus": 1.5         # Бонус к наградам за гибкость
        },
        "exclusive_missions": [
            "double_agent_operation", "information_brokerage", "neutral_arbitration",
            "corporate_war_mediation", "freelance_investigation", "independent_research",
            "moral_hacking_dilemma", "ethics_vs_profit", "gray_zone_operations"
        ],
        "special_features": [
            "Работа на любую сторону конфликта",
            "Доступ к информации всех фракций",
            "Нейтральный статус в войнах фракций",
            "Уникальные дипломатические миссии",
            "Возможность переговоров между враждующими сторонами"
        ],
        "enemies": [],
        "allies": ["Независимые хакеры", "Журналисты-расследователи"],
        "headquarters": "Мобильные зашифрованные серверы"
    }
}

# --- Расширенные достижения ---
ACHIEVEMENTS = {
    # Сюжетные достижения
    "first_hack": {
        "name": "Первый взлом",
        "desc": "Выполните первую миссию",
        "reward_rep": 5,
        "reward_btc": 10,
        "icon": "🎯",
        "rarity": "common",
        "hidden": False
    },
    "story_complete": {
        "name": "Легенда даркнета",
        "desc": "Завершите основную сюжетную линию",
        "reward_rep": 100,
        "reward_btc": 1000,
        "icon": "👑",
        "rarity": "legendary",
        "hidden": False
    },
    
    # Экономические достижения
    "crypto_millionaire": {
        "name": "Крипто-миллионер",
        "desc": "Накопите 10,000 BTC",
        "reward_rep": 50,
        "reward_items": ["golden_wallet"],
        "icon": "💰",
        "rarity": "epic",
        "hidden": False
    },
    "market_manipulator": {
        "name": "Манипулятор рынка",
        "desc": "Заработайте 1000 BTC на торговле криптовалютами",
        "reward_rep": 25,
        "reward_skills": {"all": 1},
        "icon": "📈",
        "rarity": "rare",
        "hidden": False
    },
    "penny_pincher": {
        "name": "Скряга",
        "desc": "Накопите 100,000 USD не тратя их",
        "reward_rep": 15,
        "icon": "🏦",
        "rarity": "uncommon",
        "hidden": True
    },
    
    # Технические достижения
    "ghost_protocol": {
        "name": "Протокол Призрак",
        "desc": "Завершите 10 миссий без единого предупреждения",
        "reward_rep": 30,
        "reward_items": ["ghost_cloak"],
        "icon": "👻",
        "rarity": "epic",
        "hidden": False
    },
    "zero_day_hunter": {
        "name": "Охотник за Zero-Day",
        "desc": "Найдите 5 неизвестных уязвимостей",
        "reward_rep": 40,
        "reward_skills": {"cracking": 3},
        "icon": "🕳️",
        "rarity": "epic",
        "hidden": False
    },
    "network_ghost": {
        "name": "Сетевой призрак",
        "desc": "Поддерживайте Heat Level ниже 5% в течение 50 ходов",
        "reward_rep": 35,
        "reward_items": ["stealth_suite"],
        "icon": "🌫️",
        "rarity": "rare",
        "hidden": True
    },
    
    # Социальные достижения
    "forum_legend": {
        "name": "Легенда форума",
        "desc": "Достигните 500 репутации",
        "reward_rep": 100,
        "reward_contacts": ["forum_admin"],
        "icon": "🏆",
        "rarity": "legendary",
        "hidden": False
    },
    "connection_master": {
        "name": "Мастер связей",
        "desc": "Получите 15+ контактов",
        "reward_rep": 20,
        "reward_items": ["contact_enhancer"],
        "icon": "🕸️",
        "rarity": "rare",
        "hidden": False
    },
    "social_engineer": {
        "name": "Инженер душ",
        "desc": "Достигните 10 уровня социальной инженерии",
        "reward_rep": 25,
        "reward_skills": {"social_eng": 2},
        "icon": "🎭",
        "rarity": "rare",
        "hidden": False
    },
    
    # Фракционные достижения
    "white_knight": {
        "name": "Белый рыцарь",
        "desc": "Достигните 100 репутации в фракции WhiteHats",
        "reward_rep": 50,
        "reward_items": ["ethical_badge"],
        "icon": "🛡️",
        "rarity": "epic",
        "hidden": False,
        "req_faction": "whitehats"
    },
    "dark_lord": {
        "name": "Повелитель тьмы", 
        "desc": "Достигните 100 репутации в фракции BlackHats",
        "reward_rep": 50,
        "reward_items": ["dark_crown"],
        "icon": "☠️",
        "rarity": "epic", 
        "hidden": False,
        "req_faction": "blackhats"
    },
    "gray_eminence": {
        "name": "Серая минеция",
        "desc": "Достигните 100 репутации в фракции GrayHats",
        "reward_rep": 50,
        "reward_items": ["balance_pendant"],
        "icon": "⚖️",
        "rarity": "epic",
        "hidden": False,
        "req_faction": "grayhats"
    },
    "faction_traitor": {
        "name": "Предатель",
        "desc": "Смените фракцию 3 раза",
        "reward_rep": -25,
        "icon": "🔄",
        "rarity": "rare",
        "hidden": True
    },
    
    # Скрытые/Секретные достижения
    "easter_egg_hunter": {
        "name": "Охотник за пасхалками",
        "desc": "Найдите 10 скрытых отсылок в игре",
        "reward_rep": 15,
        "reward_items": ["easter_egg_collection"],
        "icon": "🥚",
        "rarity": "rare",
        "hidden": True
    },
    "konami_code": {
        "name": "Код Konami",
        "desc": "Введите секретную последовательность команд",
        "reward_rep": 10,
        "reward_btc": 100,
        "icon": "🎮",
        "rarity": "uncommon",
        "hidden": True
    },
    "time_traveler": {
        "name": "Путешественник во времени",
        "desc": "Играйте в течение 6 часов подряд",
        "reward_rep": 20,
        "icon": "⏰",
        "rarity": "rare",
        "hidden": True
    }
}

# --- Случайные события ---
RANDOM_EVENTS = {
    # Экономические события
    "crypto_crash": {
        "name": "Крах криптовалют",
        "desc": "Рынок криптовалют обвалился на 30-50%",
        "type": "economic",
        "probability": 0.05,
        "effects": {
            "crypto_prices": {"multiplier": 0.5, "variance": 0.2},
            "player_impact": {"btc_value_loss": True}
        },
        "duration": 10,  # ходов
        "news_headline": "🔴 КРИПТО-АПОКАЛИПСИС: Рынок рушится!"
    },
    "crypto_boom": {
        "name": "Криптовалютный бум",
        "desc": "Внезапный рост цен на все криптовалюты",
        "type": "economic",
        "probability": 0.03,
        "effects": {
            "crypto_prices": {"multiplier": 1.8, "variance": 0.3},
            "player_impact": {"btc_value_gain": True}
        },
        "duration": 15,
        "news_headline": "🚀 КРИПТО-БУМ: Биткойн в небеса!"
    },
    "market_volatility": {
        "name": "Рыночная волатильность",
        "desc": "Экстремальные колебания цен на рынке",
        "type": "economic", 
        "probability": 0.08,
        "effects": {
            "crypto_prices": {"volatility_increase": 3.0},
            "player_impact": {"trading_opportunities": True}
        },
        "duration": 5,
        "news_headline": "⚡ ШТОРМ НА РЫНКЕ: Цены скачут как бешеные!"
    },
    
    # Политические/Правовые события
    "government_crackdown": {
        "name": "Правительственные облавы",
        "desc": "Усиление борьбы с киберпреступностью",
        "type": "political",
        "probability": 0.06,
        "effects": {
            "global_heat_increase": 20,
            "mission_risks": {"multiplier": 1.5},
            "faction_effects": {
                "whitehats": {"bonus": 10},
                "blackhats": {"penalty": 15}
            }
        },
        "duration": 20,
        "news_headline": "🚨 ОПЕРАЦИЯ 'ЧИСТАЯ СЕТЬ': Правительство идет в атаку!"
    },
    "cyber_war": {
        "name": "Кибервойна",
        "desc": "Эскалация международных кибератак",
        "type": "political",
        "probability": 0.04,
        "effects": {
            "faction_wars": True,
            "mission_rewards": {"multiplier": 2.0},
            "rare_missions": True
        },
        "duration": 30,
        "news_headline": "⚔️ ТРЕТЬЯ МИРОВАЯ В КИБЕРПРОСТРАНСТВЕ!"
    },
    "new_legislation": {
        "name": "Новое киберзаконодательство",
        "desc": "Принятие новых законов о кибербезопасности",
        "type": "political",
        "probability": 0.07,
        "effects": {
            "legal_penalties": {"increase": 25},
            "whitehats_bonus": 15,
            "corporate_missions": {"increase": True}
        },
        "duration": 50,
        "news_headline": "📜 НОВЫЕ ЗАКОНЫ: Киберпространство под контролем"
    },
    
    # Технологические события
    "major_breach": {
        "name": "Масштабная утечка данных",
        "desc": "Взлом крупной корпорации или государственного агентства",
        "type": "technological",
        "probability": 0.05,
        "effects": {
            "data_market_surge": True,
            "security_awareness": {"increase": 20},
            "investigation_missions": True,
            "media_attention": {"heat_multiplier": 1.3}
        },
        "duration": 15,
        "news_headline": "💥 МЕГАУТЕЧКА: 100 миллионов аккаунтов скомпрометировано!"
    },
    "new_vulnerability": {
        "name": "Критическая уязвимость",
        "desc": "Обнаружена новая серьезная уязвимость в популярном ПО",
        "type": "technological",
        "probability": 0.08,
        "effects": {
            "exploit_availability": True,
            "patch_race": True,
            "scanning_bonus": 25,
            "zero_day_missions": True
        },
        "duration": 7,
        "news_headline": "🕳️ КРИТИЧЕСКАЯ ДЫРА: Новая уязвимость потрясает интернет!"
    },
    "ai_breakthrough": {
        "name": "Прорыв в ИИ",
        "desc": "Новые технологии ИИ меняют ландшафт кибербезопасности",
        "type": "technological",
        "probability": 0.03,
        "effects": {
            "ai_tools_available": True,
            "automation_bonus": 30,
            "new_attack_vectors": True,
            "ai_defense_systems": True
        },
        "duration": 25,
        "news_headline": "🤖 ИИ-РЕВОЛЮЦИЯ: Машины берут контроль над кибервойной!"
    },
    
    # Социальные события
    "hacker_convention": {
        "name": "Хакерская конференция",
        "desc": "Крупное собрание хакерского сообщества",
        "type": "social",
        "probability": 0.06,
        "effects": {
            "knowledge_sharing": True,
            "new_contacts": {"bonus": 2},
            "skill_workshops": True,
            "networking_opportunities": True
        },
        "duration": 3,
        "news_headline": "🎪 DEFCON 2025: Хакеры со всего мира собираются!"
    },
    "whistleblower_leak": {
        "name": "Разоблачение от инсайдера",
        "desc": "Утечка секретной информации от инсайдера",
        "type": "social",
        "probability": 0.04,
        "effects": {
            "classified_info": True,
            "investigation_heat": 15,
            "media_frenzy": True,
            "government_secrets": True
        },
        "duration": 12,
        "news_headline": "📰 БОМБА: Инсайдер сливает государственные тайны!"
    },
    
    # Специальные события
    "solar_storm": {
        "name": "Солнечная буря",
        "desc": "Геомагнитная буря нарушает работу интернета",
        "type": "natural",
        "probability": 0.02,
        "effects": {
            "internet_disruption": True,
            "satellite_chaos": True,
            "communication_breakdown": True,
            "opportunity_window": True
        },
        "duration": 2,
        "news_headline": "☀️ СОЛНЕЧНЫЙ УДАР: Интернет планеты под угрозой!"
    },
    "quantum_breakthrough": {
        "name": "Квантовый прорыв",
        "desc": "Достижение в квантовых вычислениях угрожает современной криптографии",
        "type": "technological",
        "probability": 0.01,
        "effects": {
            "cryptography_obsolete": True,
            "quantum_tools": True,
            "security_revolution": True,
            "mass_panic": True
        },
        "duration": 100,
        "news_headline": "⚛️ КВАНТОВЫЙ АПОКАЛИПСИС: Вся криптография сломана!"
    }
}

# --- Сюжетные этапы ---
STORY_STAGES = {
    0: {
        "title": "Новичок на форуме",
        "desc": "Вы только что зарегистрировались на xss.is. Изучите форум и начните с простых заданий.",
        "unlock_missions": ["port_scan", "info_gather"],
        "story_event": None
    },
    1: {
        "title": "Первые шаги",
        "desc": "Вы набираете репутацию. Админы начинают замечать вас.",
        "unlock_missions": ["web_vuln", "phishing_simple"],
        "story_event": "first_contact"
    },
    2: {
        "title": "Доверенный участник",
        "desc": "Вы получили доступ к приватным разделам. Серьезные заказчики обращают внимание.",
        "unlock_missions": ["database_breach", "crypto_theft"],
        "story_event": "faction_choice"
    },
    3: {
        "title": "Элитный хакер",
        "desc": "Вы стали легендой форума. Самые опасные миссии теперь доступны.",
        "unlock_missions": ["gov_hack", "zero_day"],
        "story_event": "final_decision"
    },
    4: {
        "title": "Легенда подполья",
        "desc": "Ваше имя знает каждый в даркнете. Выбор за вами - какое наследие оставить.",
        "unlock_missions": ["ultimate_heist", "expose_conspiracy"],
        "story_event": "ending_choice"
    }
}

# --- Базовые миссии ---
MISSIONS = {
    # Начальные миссии
    "port_scan": {
        "name": "Сканирование корпоративной сети",
        "desc": "Найти открытые порты в сети IT-компании",
        "req_rep": 10,
        "req_skills": {"scanning": 1},
        "reward_btc": 30,
        "reward_rep": 3,
        "reward_skills": {"scanning": 1},
        "duration": 2,
        "risk": 10,
        "heat_gain": 5,
        "story_stage": 0
    },
    "info_gather": {
        "name": "Сбор информации о цели",
        "desc": "Собрать данные через социальные сети и открытые источники",
        "req_rep": 15,
        "req_skills": {"social_eng": 1},
        "reward_btc": 40,
        "reward_rep": 4,
        "reward_skills": {"social_eng": 1},
        "duration": 3,
        "risk": 5,
        "heat_gain": 2,
        "story_stage": 0
    },

    # Миссии среднего уровня
    "web_vuln": {
        "name": "Поиск уязвимостей веб-приложения",
        "desc": "Найти SQL-инъекцию в интернет-магазине",
        "req_rep": 25,
        "req_skills": {"cracking": 2, "scanning": 2},
        "reward_btc": 80,
        "reward_rep": 8,
        "reward_skills": {"cracking": 1, "scanning": 1},
        "duration": 4,
        "risk": 20,
        "heat_gain": 10,
        "story_stage": 1
    },
    "phishing_simple": {
        "name": "Фишинговая атака на сотрудников",
        "desc": "Создать поддельную страницу авторизации",
        "req_rep": 30,
        "req_skills": {"social_eng": 2},
        "reward_btc": 60,
        "reward_rep": 6,
        "reward_skills": {"social_eng": 1},
        "duration": 3,
        "risk": 25,
        "heat_gain": 8,
        "story_stage": 1
    },

    # Продвинутые миссии
    "database_breach": {
        "name": "Взлом базы данных банка",
        "desc": "Получить доступ к базе клиентов крупного банка",
        "req_rep": 50,
        "req_skills": {"cracking": 3, "stealth": 2},
        "reward_btc": 200,
        "reward_rep": 20,
        "reward_skills": {"cracking": 1, "stealth": 1},
        "duration": 6,
        "risk": 40,
        "heat_gain": 20,
        "story_stage": 2
    },
    "crypto_theft": {
        "name": "Кража криптовалюты с биржи",
        "desc": "Опустошить горячий кошелек криптобиржи",
        "req_rep": 60,
        "req_skills": {"cracking": 4, "stealth": 3},
        "reward_btc": 350,
        "reward_rep": 20,
        "reward_skills": {"cracking": 1, "stealth": 1},
        "duration": 8,
        "risk": 50,
        "heat_gain": 25,
        "story_stage": 2
    },

    # Элитные миссии
    "gov_hack": {
        "name": "Взлом правительственной системы",
        "desc": "Проникнуть в сеть министерства обороны",
        "req_rep": 80,
        "req_skills": {"cracking": 5, "stealth": 4, "scanning": 3},
        "reward_btc": 700,
        "reward_rep": 40,
        "reward_skills": {"cracking": 2, "stealth": 2, "scanning": 1},
        "duration": 12,
        "risk": 80,
        "heat_gain": 40,
        "story_stage": 3
    },
    "zero_day": {
        "name": "Разработка 0-day эксплойта",
        "desc": "Найти и эксплуатировать неизвестную уязвимость в популярной ОС",
        "req_rep": 100,
        "req_skills": {"cracking": 6, "scanning": 5},
        "reward_btc": 1300,
        "reward_rep": 40,
        "reward_skills": {"cracking": 3, "scanning": 2},
        "duration": 15,
        "risk": 90,
        "heat_gain": 50,
        "story_stage": 3
    },

    # Фракционные миссии
    "bug_bounty": {
        "name": "Программа Bug Bounty",
        "desc": "Найти уязвимости для крупной корпорации легально",
        "req_rep": 40,
        "req_skills": {"scanning": 3, "cracking": 2},
        "req_faction": "whitehats",
        "reward_btc": 120,
        "reward_rep": 10,
        "reward_skills": {"scanning": 1},
        "duration": 5,
        "risk": 0,
        "heat_gain": -10,
        "story_stage": 2
    },
    "ransomware_attack": {
        "name": "Атака вымогателем",
        "desc": "Зашифровать данные больницы и требовать выкуп",
        "req_rep": 60,
        "req_skills": {"cracking": 4, "stealth": 3},
        "req_faction": "blackhats",
        "reward_btc": 450,
        "reward_rep": 25,
        "reward_skills": {"cracking": 2},
        "duration": 7,
        "risk": 70,
        "heat_gain": 35,
        "story_stage": 2
    },
    "double_agent": {
        "name": "Двойной агент",
        "desc": "Работать одновременно на правительство и криминал",
        "req_rep": 70,
        "req_skills": {"social_eng": 4, "stealth": 4},
        "req_faction": "grayhats",
        "reward_btc": 300,
        "reward_rep": 20,
        "reward_skills": {"social_eng": 1, "stealth": 1},
        "duration": 10,
        "risk": 60,
        "heat_gain": 15,
        "story_stage": 3
    },

    # Финальные миссии
    "ultimate_heist": {
        "name": "Величайшее ограбление века",
        "desc": "Украсть 1 миллиард долларов из центрального банка",
        "req_rep": 150,
        "req_skills": {"cracking": 8, "stealth": 7, "scanning": 6, "social_eng": 5},
        "reward_btc": 4000,
        "reward_rep": 60,
        "reward_skills": {"all": 2},
        "duration": 20,
        "risk": 95,
        "heat_gain": 100,
        "story_stage": 4
    },
    "expose_conspiracy": {
        "name": "Разоблачить мировой заговор",
        "desc": "Обнародовать секретные документы о глобальной слежке",
        "req_rep": 150,
        "req_skills": {"scanning": 7, "stealth": 8, "social_eng": 6},
        "reward_btc": 2000,
        "reward_rep": 80,
        "reward_skills": {"all": 3},
        "duration": 18,
        "risk": 85,
        "heat_gain": 80,
        "story_stage": 4
    }


}

# --- Расширенные миссии ---
MISSIONS.update({
    # Фракционные миссии WhiteHats
    "bug_bounty_hunt": {
        "name": "Охота за багами",
        "desc": "Найдите уязвимости в системах крупной корпорации легально",
        "req_rep": 30,
        "req_skills": {"scanning": 3, "cracking": 2},
        "req_faction": "whitehats",
        "reward_btc": 120,
        "reward_rep": 12,
        "reward_skills": {"scanning": 1},
        "duration": 4,
        "risk": 5,
        "heat_gain": -5,  # Снижает heat level
        "story_stage": 1,
        "special_rewards": ["corporate_recognition"]
    },
    "corporate_security_audit": {
        "name": "Аудит корпоративной безопасности",
        "desc": "Проведите полный аудит безопасности для Fortune 500 компании",
        "req_rep": 80,
        "req_skills": {"scanning": 5, "cracking": 4, "stealth": 3},
        "req_faction": "whitehats",
        "reward_btc": 350,
        "reward_rep": 25,
        "reward_skills": {"all": 1},
        "duration": 8,
        "risk": 10,
        "heat_gain": -10,
        "story_stage": 3,
        "special_rewards": ["corporate_partnership", "security_clearance"]
    },
    
    # Фракционные миссии BlackHats
    "crypto_exchange_hack": {
        "name": "Взлом криптобиржи",
        "desc": "Опустошите горячие кошельки крупной криптовалютной биржи",
        "req_rep": 70,
        "req_skills": {"cracking": 5, "stealth": 4},
        "req_faction": "blackhats",
        "reward_btc": 800,
        "reward_rep": 40,
        "reward_skills": {"cracking": 2},
        "duration": 10,
        "risk": 80,
        "heat_gain": 40,
        "story_stage": 2,
        "special_rewards": ["crypto_fortune", "dark_reputation"]
    },
    "ransomware_deployment": {
        "name": "Развертывание вымогателя",
        "desc": "Заразите корпоративную сеть вирусом-вымогателем",
        "req_rep": 50,
        "req_skills": {"cracking": 4, "stealth": 3, "social_eng": 2},
        "req_faction": "blackhats",
        "reward_btc": 500,
        "reward_rep": 20,
        "reward_skills": {"cracking": 1, "stealth": 1},
        "duration": 7,
        "risk": 70,
        "heat_gain": 35,
        "story_stage": 2,
        "special_rewards": ["ransomware_expertise", "fear_reputation"]
    },
    
    # Фракционные миссии GrayHats
    "double_agent_operation": {
        "name": "Операция двойного агента",
        "desc": "Работайте одновременно на корпорацию и криминальную группировку",
        "req_rep": 60,
        "req_skills": {"social_eng": 4, "stealth": 4, "scanning": 3},
        "req_faction": "grayhats",
        "reward_btc": 400,
        "reward_rep": 18,
        "reward_skills": {"social_eng": 2, "stealth": 1},
        "duration": 12,
        "risk": 60,
        "heat_gain": 20,
        "story_stage": 3,
        "special_rewards": ["double_contacts", "information_network"]
    },
    "information_brokerage": {
        "name": "Торговля информацией",
        "desc": "Собирайте и продавайте ценную информацию различным клиентам",
        "req_rep": 40,
        "req_skills": {"scanning": 3, "social_eng": 3},
        "req_faction": "grayhats",
        "reward_btc": 250,
        "reward_rep": 12,
        "reward_skills": {"scanning": 1, "social_eng": 1},
        "duration": 6,
        "risk": 30,
        "heat_gain": 10,
        "story_stage": 2,
        "special_rewards": ["information_contacts", "data_cache"]
    },
    
    # Специальные миссии событий
    "emergency_patch": {
        "name": "Экстренное исправление",
        "desc": "Помогите закрыть критическую уязвимость до выхода патча",
        "req_rep": 25,
        "req_skills": {"scanning": 2, "cracking": 3},
        "reward_btc": 160,
        "reward_rep": 15,
        "duration": 2,
        "risk": 20,
        "heat_gain": -5,
        "event_triggered": True,
        "special_rewards": ["vendor_gratitude"]
    },
    "data_recovery": {
        "name": "Восстановление данных",
        "desc": "Восстановите данные жертв вымогателей",
        "req_rep": 35,
        "req_skills": {"cracking": 4, "stealth": 2},
        "reward_btc": 200,
        "reward_rep": 20,
        "duration": 5,
        "risk": 25,
        "heat_gain": -10,
        "event_triggered": True,
        "special_rewards": ["victim_gratitude", "decryption_tools"]
    },
"operation_darkfall": {
    "name": "Операция 'Сумерки'",
    "desc": "Многоэтапная операция по внедрению в корпоративную сеть",
    "type": "multi_stage",
    "req_rep": 80,
    "req_skills": {"cracking": 4, "stealth": 5, "social_eng": 3},
    "stages": [
        {
            "name": "Разведка цели",
            "desc": "Соберите информацию о корпорации TechCorp",
            "duration": 3,
            "risk": 20,
            "requirements": {"scanning": 4},
            "rewards": {"intel_points": 10}
        },
        {
            "name": "Социальная инженерия",
            "desc": "Получите учетные данные сотрудника",
            "duration": 4,
            "risk": 40,
            "requirements": {"social_eng": 4},
            "rewards": {"credentials": "employee_access"}
        },
        {
            "name": "Проникновение в сеть",
            "desc": "Используйте полученные данные для взлома",
            "duration": 5,
            "risk": 70,
            "requirements": {"cracking": 5, "stealth": 4},
            "rewards": {"btc": 800, "rep": 40}
        }
    ],
    "final_rewards": {"btc": 1500, "rep": 80, "items": ["corp_backdoor"]},
    "time_limit": 72,  # часов
    "story_stage": 3
},

"heist_crypto_exchange": {
    "name": "Ограбление криптобиржи",
    "desc": "Командная операция по краже из крупной биржи",
    "type": "team_mission",
    "req_rep": 120,
    "req_skills": {"cracking": 6, "stealth": 5},
    "team_size": 3,
    "team_roles": ["hacker", "social_engineer", "lookout"],
    "stages": [
        {
            "name": "Подготовка команды",
            "desc": "Найдите и наймите союзников",
            "duration": 2,
            "risk": 10,
            "team_action": "recruit"
        },
        {
            "name": "Планирование",
            "desc": "Разработайте план атаки",
            "duration": 3,
            "risk": 5,
            "team_action": "planning"
        },
        {
            "name": "Выполнение",
            "desc": "Координированная атака на биржу",
            "duration": 6,
            "risk": 90,
            "team_action": "execute",
            "moral_choice": {
                "question": "Биржа хранит средства благотворительности. Украсть всё?",
                "choices": {
                    "steal_all": {"rep_change": -20, "btc_bonus": 2000, "faction_impact": {"blackhats": 20}},
                    "leave_charity": {"rep_change": 10, "btc_bonus": 0, "faction_impact": {"whitehats": 15}},
                    "donate_anonymous": {"rep_change": 30, "btc_penalty": 500, "special_reward": "hero_status"}
                }
            }
        }
    ],
    "success_rates": {"low": 0.3, "medium": 0.6, "high": 0.9},
    "final_rewards": {"btc": 5000, "rep": 100},
    "time_limit": 48,
    "story_stage": 4
},

"whistleblower_dilemma": {
    "name": "Дилемма информатора",
    "desc": "Получена информация о коррупции. Что делать?",
    "type": "moral_choice",
    "req_rep": 60,
    "req_skills": {"scanning": 3, "social_eng": 4},
    "stages": [
        {
            "name": "Получение данных",
            "desc": "Загрузите компрометирующие документы",
            "duration": 2,
            "risk": 30
        },
        {
            "name": "Моральный выбор",
            "desc": "Решите судьбу полученной информации",
            "moral_choice": {
                "question": "У вас есть доказательства коррупции высокопоставленных чиновников. Ваши действия?",
                "choices": {
                    "sell_to_media": {
                        "desc": "Продать журналистам за хорошие деньги",
                        "rep_change": 5,
                        "btc_bonus": 2000,
                        "faction_impact": {"grayhats": 10}
                    },
                    "blackmail_officials": {
                        "desc": "Шантажировать чиновников",
                        "rep_change": -15,
                        "btc_bonus": 5000,
                        "heat_gain": 40,
                        "faction_impact": {"blackhats": 25}
                    },
                    "anonymous_leak": {
                        "desc": "Анонимно слить в интернет",
                        "rep_change": 25,
                        "btc_bonus": 0,
                        "faction_impact": {"whitehats": 20},
                        "special_reward": "whistleblower_protection"
                    },
                    "destroy_evidence": {
                        "desc": "Уничтожить компромат",
                        "rep_change": -5,
                        "btc_bonus": 0,
                        "heat_gain": -10,
                        "special_consequence": "missed_opportunity"
                    }
                }
            }
        }
    ],
    "time_limit": 24,
    "random_events": [
        {
            "trigger": "stage_1_complete",
            "chance": 0.3,
            "event": "government_trace",
            "desc": "Спецслужбы засекли ваши действия!",
            "effects": {"heat_gain": 25, "time_pressure": True}
        }
    ],
    "story_stage": 2
},

# Миссии с временными ограничениями
"zero_day_auction": {
    "name": "Аукцион Zero-Day",
    "desc": "У вас есть 6 часов чтобы найти и продать 0-day эксплойт",
    "type": "time_critical",
    "req_rep": 100,
    "req_skills": {"cracking": 7, "scanning": 6},
    "time_limit": 6,  # часов
    "stages": [
        {
            "name": "Поиск уязвимости",
            "desc": "Найдите неизвестную уязвимость",
            "duration": 3,
            "risk": 60,
            "time_pressure_multiplier": 1.5
        },
        {
            "name": "Создание эксплойта",
            "desc": "Разработайте рабочий exploit",
            "duration": 2,
            "risk": 40
        },
        {
            "name": "Продажа на аукционе",
            "desc": "Продайте эксплойт на черном рынке",
            "duration": 1,
            "risk": 80,
            "bidding_war": True
        }
    ],
    "time_bonus": {"6h": 3000, "4h": 2000, "2h": 1000},
    "time_penalty": {"overtime": -50},  # % от награды
    "random_events": [
        {
            "trigger": "time_half",
            "chance": 0.4,
            "event": "competitor_found",
            "desc": "Другой хакер тоже ищет эту уязвимость!",
            "effects": {"competition": True, "risk_increase": 20}
        }
    ],
    "story_stage": 3
}
})

# Добавляем новые типы событий для миссий
MISSION_EVENTS = {
    "government_trace": {
        "name": "Правительственное расследование",
        "desc": "Спецслужбы начали отслеживать ваши действия",
        "effects": {
            "heat_gain": 25,
            "stealth_requirement": +2,
            "time_pressure": True
        },
        "mitigation": {
            "vpn_active": {"heat_reduction": 10},
            "high_stealth": {"risk_reduction": 20}
        }
    },
    "competitor_interference": {
        "name": "Вмешательство конкурентов",
        "desc": "Другие хакеры пытаются помешать вашей операции",
        "effects": {
            "difficulty_increase": 1,
            "team_conflict": True
        }
    },
    "insider_help": {
        "name": "Помощь инсайдера",
        "desc": "Кто-то изнутри решил помочь",
        "effects": {
            "risk_reduction": 30,
            "bonus_intel": True,
            "time_bonus": 1  # час
        }
    },
    "security_upgrade": {
        "name": "Обновление безопасности",
        "desc": "Цель усилила защиту во время операции",
        "effects": {
            "risk_increase": 40,
            "skill_requirement": +1
        }
    }
}

# Расширяем моральные выборы
MORAL_CHOICES = {
    "collateral_damage": {
        "question": "Ваши действия могут навредить невинным людям. Продолжить?",
        "choices": {
            "proceed": {"desc": "Продолжить операцию", "rep_change": -10, "success_bonus": 0.2},
            "minimize_damage": {"desc": "Минимизировать ущерб", "rep_change": 5, "difficulty_increase": 1},
            "abort": {"desc": "Прервать миссию", "rep_change": 10, "mission_failure": True}
        }
    },
    "whistleblower_protection": {
        "question": "Информант просит защиты в обмен на данные. Согласиться?",
        "choices": {
            "protect": {"desc": "Обеспечить защиту", "rep_change": 15, "resource_cost": 500},
            "use_and_abandon": {"desc": "Использовать и бросить", "rep_change": -20, "intel_bonus": True},
            "refuse": {"desc": "Отказаться от сделки", "rep_change": 0, "alternative_path": True}
        }
    }
}

# --- Товары магазина (базовые) ---
MARKET_ITEMS = {
    # ===== НАЧАЛЬНЫЙ УРОВЕНЬ (0-25 репутации) =====
    "basic_port_scanner": {
        "name": "Базовый сканер портов",
        "price": 100,  # Было 50
        "type": "software",
        "desc": "Простой инструмент для сканирования открытых портов",
        "bonus": {"scanning": 1},
        "unlock_condition": {}
    },

    "simple_proxy": {
        "name": "Простой прокси",
        "price": 150,
        "type": "network",
        "desc": "Базовая защита IP-адреса",
        "bonus": {"stealth": 1},
        "unlock_condition": {}
    },

    "password_list": {
        "name": "Список паролей",
        "price": 80,
        "type": "documents",
        "desc": "Топ-1000 самых популярных паролей",
        "bonus": {"cracking": 1},
        "unlock_condition": {}
    },

    "fake_id_generator": {
        "name": "Генератор фейковых ID",
        "price": 120,
        "type": "software",
        "desc": "Создает поддельные личности для социальной инженерии",
        "bonus": {"social_eng": 1},
        "unlock_condition": {}
    },

    # ===== СРЕДНИЙ УРОВЕНЬ (25-50 репутации) =====
    "proxy_network": {
        "name": "Сеть прокси-серверов",
        "price": 400,  # Было 150
        "type": "network",
        "desc": "Распределенная сеть для повышенной анонимности",
        "bonus": {"stealth": 2, "heat_reduction": -5},
        "unlock_condition": {"reputation": 25}
    },

    "advanced_scanner": {
        "name": "Продвинутый сканер",
        "price": 500,  # Было 300
        "type": "software",
        "desc": "Профессиональный инструмент с OS fingerprinting",
        "bonus": {"scanning": 2},
        "unlock_condition": {"reputation": 25, "skills": {"scanning": 2}}
    },

    "phishing_kit": {
        "name": "Фишинговый набор",
        "price": 350,
        "type": "software",
        "desc": "Готовые шаблоны для фишинговых атак",
        "bonus": {"social_eng": 2},
        "unlock_condition": {"reputation": 30}
    },

    "vulnerability_database": {
        "name": "База уязвимостей",
        "price": 600,
        "type": "documents",
        "desc": "Актуальная база CVE с эксплойтами",
        "bonus": {"cracking": 2, "scanning": 1},
        "unlock_condition": {"reputation": 35}
    },

    # ===== ПРОДВИНУТЫЙ УРОВЕНЬ (50-100 репутации) =====
    "elite_proxy": {
        "name": "Элитная прокси-цепочка",
        "price": 1200,  # Было 500
        "type": "network",
        "desc": "Военного уровня анонимность через 7 стран",
        "bonus": {"stealth": 3, "heat_reduction": -10},
        "unlock_condition": {"reputation": 50, "skills": {"stealth": 3}}
    },

    "zero_day_exploit": {
        "name": "0-day эксплойт",
        "price": 2000,
        "type": "software",
        "desc": "Неизвестная уязвимость в популярном ПО",
        "bonus": {"cracking": 3},
        "unlock_condition": {"reputation": 60, "skills": {"cracking": 4}}
    },

    "ai_password_cracker": {
        "name": "ИИ взломщик паролей",
        "price": 1500,
        "type": "software",
        "desc": "Использует машинное обучение для подбора паролей",
        "bonus": {"cracking": 2, "all_skills": 1},
        "unlock_condition": {"reputation": 55}
    },

    "corporate_insider_data": {
        "name": "Инсайдерские данные",
        "price": 1000,
        "type": "documents",
        "desc": "Внутренняя информация крупных корпораций",
        "bonus": {"social_eng": 2, "reputation": 10},
        "unlock_condition": {"reputation": 65}
    },

    # ===== ЭКСПЕРТНЫЙ УРОВЕНЬ (100-200 репутации) =====
    "quantum_decryptor": {
        "name": "Квантовый дешифратор",
        "price": 3500,
        "type": "hardware",
        "desc": "Экспериментальное устройство для взлома шифрования",
        "bonus": {"cracking": 4},
        "unlock_condition": {"reputation": 100, "skills": {"cracking": 6}}
    },

    "botnet_access": {
        "name": "Доступ к ботнету",
        "price": 2900,
        "type": "network",
        "desc": "Управление сетью из 10,000 зараженных компьютеров",
        "bonus": {"all_skills": 2},
        "unlock_condition": {"reputation": 120}
    },

    "government_backdoor": {
        "name": "Правительственный бэкдор",
        "price": 4200,
        "type": "software",
        "desc": "Секретный доступ к государственным системам",
        "bonus": {"cracking": 3, "stealth": 2},
        "unlock_condition": {"reputation": 150, "faction": "blackhats"}
    },

    "nsa_toolkit": {
        "name": "Набор инструментов NSA",
        "price": 5000,
        "type": "software",
        "desc": "Утекшие инструменты спецслужб",
        "bonus": {"all_skills": 3},
        "unlock_condition": {"reputation": 180, "completed_missions": ["gov_hack"]}
    },

    # ===== ЛЕГЕНДАРНЫЙ УРОВЕНЬ (200+ репутации) =====
    "darknet_master_key": {
        "name": "Мастер-ключ даркнета",
        "price": 8000,
        "type": "documents",
        "desc": "Полный доступ ко всем скрытым ресурсам",
        "bonus": {"all_skills": 4, "reputation": 50},
        "unlock_condition": {"reputation": 200, "story_stage": 3}
    },

    "ai_singularity_core": {
        "name": "Ядро ИИ сингулярности",
        "price": 12000,
        "type": "hardware",
        "desc": "Самообучающийся ИИ для автоматизации взлома",
        "bonus": {"all_skills": 5},
        "unlock_condition": {"reputation": 300, "story_stage": 4}
    },

    # ===== СПЕЦИАЛЬНЫЕ ПРЕДМЕТЫ =====
    "vpn_subscription": {
        "name": "VPN подписка",
        "price": 200,
        "type": "network",
        "desc": "Месячная подписка на премиум VPN",
        "bonus": {"stealth": 1, "heat_reduction": -3},
        "unlock_condition": {}
    },

    "fake_documents": {
        "name": "Поддельные документы",
        "price": 400,
        "type": "documents",
        "desc": "Набор поддельных удостоверений личности",
        "bonus": {"social_eng": 1, "heat_reduction": -5},
        "unlock_condition": {"reputation": 40}
    },

    "encrypted_phone": {
        "name": "Зашифрованный телефон",
        "price": 800,
        "type": "hardware",
        "desc": "Военного уровня шифрование коммуникаций",
        "bonus": {"stealth": 2},
        "unlock_condition": {"reputation": 70}
    },

    "bitcoin_mixer": {
        "name": "Bitcoin миксер",
        "price": 500,
        "type": "software",
        "desc": "Отмывает криптовалюту через множество адресов",
        "bonus": {"heat_reduction": -15},
        "unlock_condition": {"reputation": 45}
    },

    # ===== ФРАКЦИОННЫЕ ПРЕДМЕТЫ =====
    "whitehat_certification": {
        "name": "Сертификат этичного хакера",
        "price": 1000,
        "type": "documents",
        "desc": "Официальный сертификат для легальной работы",
        "bonus": {"reputation": 20, "heat_reduction": -20},
        "unlock_condition": {"faction": "whitehats", "reputation": 50}
    },

    "blackhat_rootkit": {
        "name": "Продвинутый руткит",
        "price": 1500,
        "type": "software",
        "desc": "Невидимый для антивирусов вредоносный код",
        "bonus": {"stealth": 3, "cracking": 2},
        "unlock_condition": {"faction": "blackhats", "reputation": 75}
    },

    "grayhat_toolkit": {
        "name": "Универсальный набор",
        "price": 1200,
        "type": "software",
        "desc": "Инструменты для любых задач",
        "bonus": {"all_skills": 2},
        "unlock_condition": {"faction": "grayhats", "reputation": 60}
    },

    # ===== РАСХОДУЕМЫЕ ПРЕДМЕТЫ (можно добавить в будущем) =====
    "coffee_pack": {
        "name": "Упаковка кофе",
        "price": 20,
        "type": "consumable",
        "desc": "Повышает концентрацию на следующие 5 ходов",
        "bonus": {"temporary_skill_boost": 1},
        "unlock_condition": {}
    },

    "energy_drink": {
        "name": "Энергетик",
        "price": 40,
        "type": "consumable",
        "desc": "Дополнительный ход без усталости",
        "bonus": {"extra_turn": 1},
        "unlock_condition": {}
    },

    # ===== КОЛЛЕКЦИОННЫЕ ПРЕДМЕТЫ =====
    "original_phreaking_manual": {
        "name": "Оригинальное руководство по фрикингу",
        "price": 3000,
        "type": "documents",
        "desc": "Историческая реликвия хакерского движения 70-х",
        "bonus": {"reputation": 30, "all_skills": 1},
        "unlock_condition": {"reputation": 150}
    },

    "satoshi_wallet": {
        "name": "Кошелек Сатоши",
        "price": 15000,
        "type": "documents",
        "desc": "Легендарный биткоин-кошелек с историческим значением",
        "bonus": {"reputation": 100},
        "unlock_condition": {"reputation": 250, "achievements": ["crypto_master"]}
    }
}

# --- Контакты (базовые) ---
CONTACTS = {
    "shadow": {
        "name": "Shadow",
        "desc": "Таинственный ментор с большими связями",
        "messages": [
            "Помни - в нашем мире доверие стоит дороже биткоинов.",
            "Следи за heat level. Слишком много шума - и тебя найдут.",
            "У меня есть особое задание. Справишься - получишь доступ к элитным инструментам."
        ],
        "unlocks": ["advanced_scanner", "elite_proxy"]
    },
    "nexus": {
        "name": "Nexus",
        "desc": "Информационный брокер",
        "messages": [
            "Информация - это власть. У меня есть то, что тебе нужно... за правильную цену.",
            "Слышал, правительство готовит новую систему слежки. Интересно?",
            "Могу достать инсайдерскую информацию о следующем обновлении безопасности крупных корпораций."
        ],
        "unlocks": ["insider_info", "corporate_secrets"]
    },
    "ghost": {
        "name": "Ghost",
        "desc": "Мастер анонимности и OPSEC",
        "messages": [
            "Твои следы в сети слишком заметны. Нужно поработать над анонимностью.",
            "Используй мои инструменты - они помогут остаться невидимым.",
            "Помни: параноя - это просто повышенная осознанность в нашем деле."
        ],
        "unlocks": ["quantum_vpn", "trace_eraser"]
    }
}

# --- Посты форума ---
FORUM_POSTS = {
    "public": [
        {
            "id": 1,
            "title": "Приветствие от админа",
            "author": "Admin",
            "content": "Добро пожаловать на xss.is, братва! Надеюсь, найдете тут что-то полезное. Не нарушайте правила и не палитесь.",
            "pinned": True
        },
        {
            "id": 2,
            "title": "Как остаться анонимным в сети?",
            "author": "Ghost",
            "content": "VPN + TOR + VM. Никаких личных данных при регистрации, никаких совпадений с реалом. Всегда используйте одноразовые почты и крипту для оплаты."
        },
        {
            "id": 3,
            "title": "Поиск уязвимостей в WEB",
            "author": "WebSec",
            "content": "Начинайте с основ: OWASP Top 10. Изучите SQLi, XSS, CSRF, XXE, SSRF. Используйте Burp Suite или OWASP ZAP."
        },
        {
            "id": 4,
            "title": "Фишинг: социальная инженерия",
            "author": "SocialEng",
            "content": "Самый слабый элемент - человек. Учитесь манипулировать, создавать убедительные письма и сайты. Это искусство."
        },
        {
            "id": 5,
            "title": "Обсуждение последних новостей ИБ",
            "author": "NewsBot",
            "content": "Свежие сливы данных и новые эксплойты обсуждаем здесь. Держите руку на пульсе!"
        },
        {
            "id": 6,
            "title": "🔥 СРОЧНО: Новая уязвимость в популярной CMS",
            "author": "0dayHunter",
            "content": "Обнаружена критическая RCE в последней версии [РЕДАКТИРОВАНО]. Эксплойт уже в дикой природе. Детали в приватном разделе для проверенных участников."
        },
        {
            "id": 7,
            "title": "Истории из жизни: Как я чуть не спалился",
            "author": "LuckyOne",
            "content": "Расскажу поучительную историю. Делал пентест для одной конторы, забыл включить VPN... Хорошо, что у них логи не настроены были. Мораль: ВСЕГДА проверяйте OPSEC перед работой!"
        },
        {
            "id": 8,
            "title": "Криптовалютные миксеры: Обзор 2024",
            "author": "CryptoAnon",
            "content": "Сравнение актуальных сервисов для повышения приватности транзакций. TornadoCash уже не торт, есть альтернативы получше."
        }
    ],
    "private": [
        {
            "id": 1,
            "title": "🔴 ЭКСКЛЮЗИВ: База данных крупного банка",
            "author": "DataLeak",
            "content": "Свежий дамп: 2M+ записей с полными данными клиентов. Включает: ФИО, телефоны, балансы счетов. Цена договорная, только для репутации 50+",
            "requirements": {"reputation": 50}
        },
        {
            "id": 2,
            "title": "Zero-Day в Windows 11",
            "author": "KernelPanic",
            "content": "Privilege escalation через уязвимость в драйвере. Работает на всех версиях, включая последние патчи. PoC прилагается. Microsoft еще не в курсе ;)",
            "requirements": {"reputation": 40, "skills": {"cracking": 3}}
        },
        {
            "id": 3,
            "title": "Приватная сеть ботов - 100k+ машин",
            "author": "BotMaster",
            "content": "Сдаю в аренду ботнет. География: US/EU/ASIA. Отличный аптайм, чистые IP. DDoS, майнинг, рассылки - что угодно. Цены от 1000 BTC/день.",
            "requirements": {"reputation": 60, "skills": {"cracking": 4}}
        },
        {
            "id": 4,
            "title": "🎯 Целевой фишинг: Автоматизация",
            "author": "PhishKing",
            "content": "Мой фреймворк для автоматизированного spear-phishing. AI генерация писем, обход спам-фильтров, статистика в реальном времени.",
            "requirements": {"reputation": 35, "skills": {"social_eng": 3}}
        },
        {
            "id": 5,
            "title": "Взлом криптобирж: Методология",
            "author": "CryptoBreaker",
            "content": "Пошаговое руководство по поиску уязвимостей в криптобиржах. От API до смарт-контрактов. Уже заработал 1000+ BTC.",
            "requirements": {"reputation": 70, "skills": {"cracking": 5}}
        }
    ]
}

# --- Криптовалюты ---
CRYPTO_DATA = {
    "BTC": {"name": "Bitcoin", "price": 65000.0},
    "ETH": {"name": "Ethereum", "price": 3500.0},
    "LTC": {"name": "Litecoin", "price": 150.0},
    "XRP": {"name": "Ripple", "price": 0.75},
    "DOGE": {"name": "Dogecoin", "price": 0.15}
}

# --- Расширенные товары магазина ---
MARKET_ITEMS.update({
    # Фракционные предметы
    "ethical_hacker_toolkit": {
        "name": "Набор этичного хакера",
        "price": 200,
        "type": "software",
        "desc": "Профессиональные инструменты для легального тестирования",
        "bonus": {"scanning": 2, "reputation_bonus": 5},
        "unlock_condition": {"faction": "whitehats"},
        "faction_exclusive": True
    },
    "corporate_badge": {
        "name": "Корпоративный бейдж",
        "price": 150,
        "type": "documents",
        "desc": "Официальное удостоверение для работы с корпорациями",
        "bonus": {"heat_reduction": 20, "corporate_access": True},
        "unlock_condition": {"faction": "whitehats", "reputation": 50}
    },
    "dark_web_access": {
        "name": "Премиум доступ к даркнету",
        "price": 300,
        "type": "service",
        "desc": "Эксклюзивный доступ к закрытым разделам даркнета",
        "bonus": {"cracking": 2, "dark_market_access": True},
        "unlock_condition": {"faction": "blackhats"},
        "faction_exclusive": True
    },
    "criminal_connections": {
        "name": "Криминальные связи",
        "price": 250,
        "type": "documents",
        "desc": "Контакты в преступном мире для особых операций",
        "bonus": {"social_eng": 2, "criminal_missions": True},
        "unlock_condition": {"faction": "blackhats", "reputation": 40}
    },
    "neutral_network": {
        "name": "Нейтральная сеть",
        "price": 180,
        "type": "service",
        "desc": "Доступ к информационным сетям всех фракций",
        "bonus": {"scanning": 1, "social_eng": 1, "information_access": True},
        "unlock_condition": {"faction": "grayhats"},
        "faction_exclusive": True
    },
    "diplomat_credentials": {
        "name": "Дипломатические полномочия",
        "price": 220,
        "type": "documents",
        "desc": "Возможность ведения переговоров между фракциями",
        "bonus": {"social_eng": 3, "faction_immunity": True},
        "unlock_condition": {"faction": "grayhats", "reputation": 60}
    },
    
    # Предметы событий
    "emergency_kit": {
        "name": "Аварийный набор",
        "price": 100,
        "type": "software",
        "desc": "Инструменты для экстренного реагирования на кибератаки",
        "bonus": {"all_skills": 1, "emergency_bonus": True},
        "unlock_condition": {"event": "major_breach"},
        "event_exclusive": True,
        "duration": 20  # Доступен только 20 ходов
    },
    "quantum_shield": {
        "name": "Квантовая защита",
        "price": 1000,
        "type": "software",
        "desc": "Защита от квантовых атак (экспериментальная)",
        "bonus": {"stealth": 5, "quantum_immunity": True},
        "unlock_condition": {"event": "quantum_breakthrough"},
        "event_exclusive": True,
        "rarity": "legendary"
    },
    
    # Легендарные предметы
    "gods_eye": {
        "name": "Око Бога",
        "price": 5000,
        "type": "software",
        "desc": "Легендарная система наблюдения с глобальным доступом",
        "bonus": {"scanning": 10, "global_access": True},
        "unlock_condition": {"reputation": 200, "completed_missions": 50},
        "rarity": "legendary",
        "unique": True
    },
    "pandoras_box": {
        "name": "Ящик Пандоры",
        "price": 10000,
        "type": "malware",
        "desc": "Мифический вирус, способный парализовать интернет",
        "bonus": {"cracking": 15, "apocalypse_weapon": True},
        "unlock_condition": {"faction": "blackhats", "reputation": 150},
        "rarity": "legendary",
        "unique": True,
        "consequences": {"global_chaos": True}
    }
})

# --- Новые контакты ---
CONTACTS.update({
    "forum_admin": {
        "name": "Administrator",
        "desc": "Загадочный администратор форума xss.is",
        "messages": [
            "Твоя репутация на форуме впечатляет. Возможно, пришло время для особых заданий.",
            "Следи за объявлениями. Скоро появятся возможности для элитных участников.",
            "Помни: с большой репутацией приходит большая ответственность."
        ],
        "unlocks": ["admin_missions", "elite_access"],
        "unlock_condition": {"reputation": 100}
    },
    "corporate_insider": {
        "name": "Corporate Mole",
        "desc": "Инсайдер из крупной технологической корпорации",
        "messages": [
            "У меня есть информация о внутренних системах безопасности.",
            "Корпорация планирует крупное обновление безопасности. Это наша возможность.",
            "Будь осторожен. Корпоративная безопасность не дремлет."
        ],
        "unlocks": ["corporate_intel", "insider_access"],
        "unlock_condition": {"faction": "any", "reputation": 60}
    },
    "government_agent": {
        "name": "Agent Smith",
        "desc": "Секретный агент спецслужб",
        "messages": [
            "Государство нуждается в таких, как ты. Готов послужить родине?",
            "Некоторые операции требуют... неофициального подхода.",
            "Твои навыки могут быть полезны для национальной безопасности."
        ],
        "unlocks": ["government_ops", "classified_missions"],
        "unlock_condition": {"faction": "whitehats", "reputation": 80}
    },
    "crime_boss": {
        "name": "The Kingpin",
        "desc": "Влиятельный лидер киберпреступного синдиката",
        "messages": [
            "В нашем деле нужны надежные люди. Покажи, чего ты стоишь.",
            "Большие деньги требуют больших рисков. Готов?",
            "Лояльность вознаграждается щедро. Предательство... не прощается."
        ],
        "unlocks": ["crime_syndicate", "high_stakes_missions"],
        "unlock_condition": {"faction": "blackhats", "reputation": 70}
    },
    "information_broker": {
        "name": "The Oracle",
        "desc": "Торговец информацией, знающий все обо всех",
        "messages": [
            "Информация - это власть. А власть имеет свою цену.",
            "У меня есть данные, которые могут изменить твою жизнь. Интересно?",
            "Вопрос не в том, что ты знаешь, а в том, что ты готов узнать."
        ],
        "unlocks": ["information_market", "intelligence_missions"],
        "unlock_condition": {"faction": "grayhats", "reputation": 50}
    }
})

# --- Концовки игры (базовые) ---
ENDINGS = {
    "hero": {
        "title": "Цифровой герой",
        "desc": "Вы использовали свои навыки для защиты невинных и разоблачения коррупции. Ваше имя войдет в историю как символ справедливости в цифровую эпоху.",
        "requirements": {"faction": "whitehats", "reputation": 150, "completed_missions": ["expose_conspiracy"]}
    },
    "kingpin": {
        "title": "Король даркнета",
        "desc": "Вы построили криминальную империю и стали самым влиятельным человеком в подполье. Власть и богатство в ваших руках, но какой ценой?",
        "requirements": {"faction": "blackhats", "btc_balance": 50000, "completed_missions": ["ultimate_heist"]}
    },
    "ghost": {
        "title": "Призрак в машине",
        "desc": "Вы исчезли без следа, став легендой. Никто не знает, кто вы на самом деле, но ваши деяния будут жить вечно в коде и памяти сети.",
        "requirements": {"faction": "grayhats", "heat_level": 0, "skills": {"stealth": 10}}
    },
    "burned": {
        "title": "Сгоревший агент",
        "desc": "Ваша деятельность привлекла слишком много внимания. Теперь вы в бегах, а за вашу голову назначена награда.",
        "requirements": {"heat_level": 100, "warnings": 3}
    },
    "reformed": {
        "title": "Исправившийся хакер",
        "desc": "Вы решили использовать свои навыки на благо общества, став консультантом по кибербезопасности.",
        "requirements": {"story_choices": {"reformed": True}, "reputation": 100}
    }
}

# --- Концовки игры (расширенные) ---
ENDINGS.update({
    "cyber_messiah": {
        "title": "Кибер-мессия",
        "desc": "Вы стали спасителем цифрового мира, ваши действия изменили интернет к лучшему",
        "requirements": {
            "faction": "whitehats", 
            "reputation": 200, 
            "completed_missions": ["save_the_internet"]
        },
        "rarity": "legendary"
    },
    "digital_emperor": {
        "title": "Цифровой император",
        "desc": "Вы построили криминальную империю и контролируете весь даркнет",
        "requirements": {
            "faction": "blackhats", 
            "btc_balance": 100000, 
            "completed_missions": ["conquer_darknet"]
        },
        "rarity": "legendary"
    },
    "shadow_puppeteer": {
        "title": "Кукловод теней",
        "desc": "Вы стали невидимым кукловодом, управляющим событиями из тени",
        "requirements": {
            "faction": "grayhats", 
            "heat_level": 0, 
            "skills": {"all": 10},
            "hidden_achievements": 10
        },
        "rarity": "legendary"
    },
    "digital_nomad": {
        "title": "Цифровой кочевник",
        "desc": "Вы живете вне системы, свободно перемещаясь в цифровом пространстве",
        "requirements": {
            "faction_changes": 3,
            "countries_visited": 10,
            "stealth_missions": 25
        },
        "rarity": "epic"
    },
    "quantum_hacker": {
        "title": "Квантовый хакер",
        "desc": "Вы освоили квантовые технологии и стали хакером будущего",
        "requirements": {
            "quantum_missions": 5,
            "future_tech": True,
            "reputation": 150
        },
        "rarity": "epic"
    }
})

# --- Игровая статистика и метрики ---
GAME_METRICS = {
    "difficulty_scaling": {
        "easy": {"mission_risk_modifier": 0.8, "reward_modifier": 0.9},
        "normal": {"mission_risk_modifier": 1.0, "reward_modifier": 1.0},
        "hard": {"mission_risk_modifier": 1.3, "reward_modifier": 1.2},
        "nightmare": {"mission_risk_modifier": 1.8, "reward_modifier": 1.5}
    },
    "progression_milestones": {
        25: {"unlock": "faction_choice", "bonus": "starter_bonus"},
        50: {"unlock": "advanced_missions", "bonus": "skill_boost"},
        100: {"unlock": "elite_content", "bonus": "reputation_multiplier"},
        150: {"unlock": "endgame_content", "bonus": "legendary_access"},
        200: {"unlock": "transcendence", "bonus": "god_mode"}
    },
    "balance_parameters": {
        "max_heat_per_turn": 15,
        "min_mission_cooldown": 1,
        "faction_reputation_cap": 100,
        "skill_training_cost_multiplier": 1.5,
        "crypto_volatility_base": 0.05
    }
}