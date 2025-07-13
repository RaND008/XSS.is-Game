"""
Цветовая схема для XSS Game - обновлено для версии 0.3.5
"""

import colorama
from colorama import Fore, Style, Back

# Инициализируем colorama
colorama.init(autoreset=True)


class Colors:
    """Основная цветовая схема игры"""
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    INFO = Fore.CYAN + Style.BRIGHT
    HEADER = Fore.MAGENTA + Style.BRIGHT
    MONEY = Fore.YELLOW + Style.BRIGHT
    REP = Fore.BLUE + Style.BRIGHT
    SKILL = Fore.GREEN
    DANGER = Fore.RED + Back.BLACK + Style.BRIGHT
    PROMPT = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL
    STORY = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
    SYSTEM = Fore.LIGHTBLUE_EX + Style.BRIGHT
    ENCRYPTED = Fore.LIGHTRED_EX + Style.DIM


class XSSColors:
    """Новая цветовая схема в стиле XSS.is для версии 0.3.5"""
    
    # Основные цвета из логотипа XSS.is
    # Темно-серый фон (#2a2e32) и ярко-зеленый (#7ed321)
    DARK_BG = "\033[48;2;42;46;50m"           # Темно-серый фон
    BRIGHT_GREEN = "\033[38;2;126;211;33m"    # Ярко-зеленый (основной цвет)
    WHITE = "\033[38;2;255;255;255m"          # Белый текст
    DARK_GRAY = "\033[38;2;128;128;128m"      # Темно-серый текст
    LIGHT_GRAY = "\033[38;2;192;192;192m"     # Светло-серый
    PROMPT = "\033[38;2;255;255;255m"         # Белый для подсказок ввода
    
    # Акцентные цвета
    HEADER = "\033[38;2;155;89;182m"  # Фиолетовый для заголовков
    REP = "\033[38;2;33;150;243m"  # Синий для репутации
    SKILL = "\033[38;2;76;175;80m"  # Зеленый для навыков
    STORY = "\033[38;2;186;104;200m"  # Светло-фиолетовый для сюжета
    SYSTEM = "\033[38;2;144;202;249m"  # Светло-голубой для системы
    ENCRYPTED = "\033[38;2;255;138;128m"  # Светло-красный для шифрования
    SUCCESS = "\033[38;2;126;211;33m"         # Зеленый для успеха (как в логотипе)
    ERROR = "\033[38;2;244;67;54m"            # Красный для ошибок
    WARNING = "\033[38;2;255;193;7m"          # Желтый для предупреждений
    INFO = "\033[38;2;100;181;246m"           # Голубой для информации
    MONEY = "\033[38;2;255;235;59m"           # Золотой для денег
    CRITICAL_ERROR = "\033[38;2;255;0;0m"     # Ярко-красный для критических ошибок
    DANGER = "\033[38;2;255;50;50m"           # Красный для предупреждений об опасности, возможно, чуть светлее CRITICAL_ERROR
    
    # Градиенты зеленого (для разных уровней)
    GREEN_DARK = "\033[38;2;76;175;80m"       # Темно-зеленый
    GREEN_LIGHT = "\033[38;2;139;195;74m"     # Светло-зеленый
    GREEN_BRIGHT = "\033[38;2;126;211;33m"    # Ярко-зеленый (основной)
    
    # Специальные эффекты
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKETHROUGH = "\033[9m"
    
    # Фоновые цвета
    BG_BLACK = "\033[40m"
    BG_GREEN = "\033[48;2;126;211;33m"
    BG_DARK = "\033[48;2;42;46;50m"
    BG_ERROR = "\033[48;2;244;67;54m"
    
    # Сброс
    RESET = "\033[0m"
    
    @classmethod
    def gradient_text(cls, text: str, start_color: tuple, end_color: tuple) -> str:
        """Создает градиентный текст"""
        length = len(text)
        if length == 0:
            return ""
        
        result = ""
        for i, char in enumerate(text):
            # Интерполируем цвет
            ratio = i / (length - 1) if length > 1 else 0
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            result += f"\033[38;2;{r};{g};{b}m{char}"
        
        return result + cls.RESET
    
    @classmethod
    def heat_color(cls, heat_level: int) -> str:
        """Возвращает цвет в зависимости от уровня heat"""
        if heat_level < 30:
            return cls.SUCCESS
        elif heat_level < 70:
            return cls.WARNING
        else:
            return cls.ERROR
    
    @classmethod
    def skill_color(cls, skill_level: int) -> str:
        """Возвращает цвет в зависимости от уровня навыка"""
        if skill_level < 3:
            return cls.DARK_GRAY
        elif skill_level < 7:
            return cls.WARNING
        else:
            return cls.SUCCESS


def print_separator(char="─", length=60, color=None):
    """Печать разделителя"""
    if color is None:
        color = XSSColors.DARK_GRAY
    print(f"{color}{char * length}{XSSColors.RESET}")


def colored_text(text, color=None):
    """Возвращает цветной текст"""
    if color is None:
        color = XSSColors.WHITE
    return f"{color}{text}{XSSColors.RESET}"


def print_logo():
    """Печатает логотип XSS.is"""
    logo = f"""
{XSSColors.BRIGHT_GREEN}~/{XSSColors.WHITE}{XSSColors.BOLD}XSS{XSSColors.RESET}{XSSColors.DARK_GRAY}.is{XSSColors.RESET}
    """
    print(logo)


def print_xss_banner():
    """Печатает баннер в стиле XSS.is"""
    banner = f"""
{XSSColors.DARK_BG}{' ' * 80}{XSSColors.RESET}
{XSSColors.DARK_BG} {XSSColors.BRIGHT_GREEN}~/{XSSColors.WHITE}{XSSColors.BOLD}XSS{XSSColors.RESET}{XSSColors.DARK_BG}{XSSColors.DARK_GRAY}.is   {XSSColors.WHITE}UNDERGROUND HACKING SIMULATOR v0.3.8{' ' * 32}{XSSColors.RESET}
{XSSColors.DARK_BG}{' ' * 80}{XSSColors.RESET}
    """
    print(banner)


def format_menu_item(number: int, icon: str, text: str, description: str = "") -> str:
    """Форматирует пункт меню в стиле XSS"""
    result = f"{XSSColors.DARK_GRAY}[{number:02d}]{XSSColors.RESET} {icon} {XSSColors.WHITE}{text}{XSSColors.RESET}"
    if description:
        result += f"\n     {XSSColors.DARK_GRAY}{description}{XSSColors.RESET}"
    return result


def print_box_header(title: str, width: int = 60):
    """Печатает заголовок бокса"""
    print(f"{XSSColors.DARK_GRAY}┌─{XSSColors.BRIGHT_GREEN}{title}{XSSColors.DARK_GRAY}{'─' * (width - len(title) - 3)}┐{XSSColors.RESET}")


def print_box_footer(width: int = 60):
    """Печатает нижнюю границу бокса"""
    print(f"{XSSColors.DARK_GRAY}└{'─' * (width - 2)}┘{XSSColors.RESET}")


def print_box_line(content: str, width: int = 60):
    """Печатает строку внутри бокса"""
    padding = width - len(content) - 2
    print(f"{XSSColors.DARK_GRAY}│{XSSColors.RESET} {content}{' ' * padding}{XSSColors.DARK_GRAY}│{XSSColors.RESET}")