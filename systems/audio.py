"""
Аудио система для XSS Game
"""

import os
import threading
import time
from typing import Optional

from config.settings import AUDIO_SETTINGS, SOUND_EFFECTS
from ui.colors import XSSColors


class AudioSystem:
    """Класс для управления аудио системой"""
    
    def __init__(self):
        self.audio_available = False
        self.audio_backend = None
        self.music_enabled = AUDIO_SETTINGS['music_enabled']
        self.sound_enabled = AUDIO_SETTINGS['sound_enabled']
        self.music_volume = AUDIO_SETTINGS['music_volume']
        self.sound_volume = AUDIO_SETTINGS['sound_volume']
        self.background_music = AUDIO_SETTINGS['background_music']
        
        # Переменные для управления музыкой
        self.music_thread = None
        self.stop_music_flag = False
        
        self._initialize_audio()
    
    def _initialize_audio(self) -> None:
        """Инициализация аудио системы"""
        # Пробуем pygame первым
        try:
            import pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.audio_available = True
            self.audio_backend = "pygame"
            print(f"{XSSColors.SUCCESS}[♪] Аудио система: pygame (рекомендуется){XSSColors.RESET}")
            return
        except Exception as e:
            print(f"{XSSColors.WARNING}[!] pygame недоступен: {e}{XSSColors.RESET}")
        
        # Fallback на playsound
        try:
            self.audio_available = True
            self.audio_backend = "playsound"
            print(f"{XSSColors.INFO}[♪] Аудио система: playsound{XSSColors.RESET}")
        except Exception:
            self.audio_available = False
            print(f"{XSSColors.ERROR}[!] Аудио недоступно. Установите pygame или playsound{XSSColors.RESET}")
    
    def check_audio_files(self) -> bool:
        """Проверяет наличие аудио файлов"""
        os.makedirs("music", exist_ok=True)
        os.makedirs("sounds", exist_ok=True)
        
        missing = []
        
        # Проверяем фоновую музыку
        if not os.path.exists(self.background_music):
            missing.append(f"Фоновая музыка: {self.background_music}")
        
        # Проверяем звуковые эффекты
        for effect, path in SOUND_EFFECTS.items():
            if not os.path.exists(path):
                missing.append(f"Звук '{effect}': {path}")
        
        if missing:
            print(f"{XSSColors.WARNING}[!] Некоторые аудио файлы отсутствуют:{XSSColors.RESET}")
            # Показываем только первые 5
            for item in missing[:5]:
                print(f"    - {item}")
            if len(missing) > 5:
                print(f"    ... и еще {len(missing) - 5} файлов")
            print(f"{XSSColors.INFO}Игра будет работать без отсутствующих звуков{XSSColors.RESET}")
            return False
        
        print(f"{XSSColors.SUCCESS}[♪] Все аудио файлы найдены!{XSSColors.RESET}")
        return True

    def play_sound(self, effect_name: str, wait: bool = False) -> bool:
        """Воспроизводит звуковой эффект с проверкой файлов"""
        if not self.audio_available or not self.sound_enabled:
            return False

        if effect_name not in SOUND_EFFECTS:
            return False

        file_path = SOUND_EFFECTS[effect_name]

        # Проверяем существование файла
        if not os.path.exists(file_path):
            # Создаем недостающие директории
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # Логируем отсутствие файла, но не прерываем игру
            if hasattr(self, '_missing_sounds'):
                if effect_name not in self._missing_sounds:
                    self._missing_sounds.add(effect_name)
                    print(f"{XSSColors.WARNING}[Аудио] Файл не найден: {file_path}{XSSColors.RESET}")
            else:
                self._missing_sounds = {effect_name}
                print(f"{XSSColors.WARNING}[Аудио] Файл не найден: {file_path}{XSSColors.RESET}")
            return False

        try:
            if self.audio_backend == "pygame":
                import pygame
                sound = pygame.mixer.Sound(file_path)
                sound.set_volume(self.sound_volume)
                channel = sound.play()
                if wait and channel:
                    while channel.get_busy():
                        time.sleep(0.1)
                return True
            else:
                # playsound версия
                threading.Thread(
                    target=self._safe_playsound,
                    args=(os.path.abspath(file_path),),
                    daemon=True
                ).start()
                return True
        except Exception as e:
            print(f"{XSSColors.ERROR}[Аудио] Ошибка воспроизведения {effect_name}: {e}{XSSColors.RESET}")
            return False

    def start_background_music(self) -> bool:
        """Запускает фоновую музыку с проверкой файла"""
        if not self.audio_available or not self.music_enabled:
            return False

        # Проверяем существование файла
        if not os.path.exists(self.background_music):
            os.makedirs(os.path.dirname(self.background_music), exist_ok=True)
            print(f"{XSSColors.WARNING}[Музыка] Файл не найден: {self.background_music}{XSSColors.RESET}")
            return False

        try:
            if self.audio_backend == "pygame":
                import pygame
                pygame.mixer.music.load(self.background_music)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # -1 = бесконечный цикл
                return True
            else:
                # Старый код для playsound
                self.stop_music_flag = False
                self.music_thread = threading.Thread(target=self._music_loop, daemon=True)
                self.music_thread.start()
                return True
        except Exception as e:
            print(f"{XSSColors.ERROR}[Музыка] Ошибка: {e}{XSSColors.RESET}")
            return False
    
    def stop_background_music(self) -> None:
        """Останавливает фоновую музыку"""
        if self.audio_backend == "pygame":
            try:
                import pygame
                pygame.mixer.music.stop()
            except Exception:
                pass
        else:
            # Старый код для playsound
            self.stop_music_flag = True
            if self.music_thread and self.music_thread.is_alive():
                self.music_thread.join(timeout=0.5)
    
    def _music_loop(self) -> None:
        """Воспроизводит фоновую музыку в цикле (для playsound)"""
        while self.music_enabled and not self.stop_music_flag:
            try:
                if os.path.exists(self.background_music):
                    self._safe_playsound(self.background_music)
                    time.sleep(1)  # Пауза между повторами
                else:
                    break
            except Exception as e:
                if "Error 259" not in str(e) and "Error 263" not in str(e):
                    print(f"{XSSColors.ERROR}[Ошибка музыки] {e}{XSSColors.RESET}")
                break
    
    def is_music_playing(self) -> bool:
        """Проверяет, играет ли музыка"""
        if self.audio_backend == "pygame":
            try:
                import pygame
                return pygame.mixer.music.get_busy()
            except Exception:
                return False
        else:
            return self.music_thread and self.music_thread.is_alive() if self.music_thread else False
    
    def toggle_music(self) -> None:
        """Включает/выключает музыку"""
        self.music_enabled = not self.music_enabled
        
        if self.music_enabled:
            self.start_background_music()
            print(f"{XSSColors.SUCCESS}[♪] Музыка включена{XSSColors.RESET}")
        else:
            self.stop_background_music()
            print(f"{XSSColors.WARNING}[♪] Музыка выключена{XSSColors.RESET}")
    
    def toggle_sounds(self) -> None:
        """Включает/выключает звуки"""
        self.sound_enabled = not self.sound_enabled
        status = "включены" if self.sound_enabled else "выключены"
        print(f"{XSSColors.INFO}[🔊] Звуковые эффекты {status}{XSSColors.RESET}")
        
        if self.sound_enabled:
            self.play_sound("success")
    
    def set_music_volume(self, volume: float) -> bool:
        """Устанавливает громкость музыки"""
        if not 0 <= volume <= 1:
            return False
        
        self.music_volume = volume
        
        if self.audio_backend == "pygame":
            try:
                import pygame
                pygame.mixer.music.set_volume(volume)
                return True
            except Exception:
                return False
        
        return True
    
    def set_sound_volume(self, volume: float) -> bool:
        """Устанавливает громкость звуков"""
        if not 0 <= volume <= 1:
            return False
        
        self.sound_volume = volume
        return True
    
    def get_music_volume(self) -> float:
        """Получает текущую громкость музыки"""
        if self.audio_backend == "pygame":
            try:
                import pygame
                return pygame.mixer.music.get_volume()
            except Exception:
                return self.music_volume
        return self.music_volume
    
    def test_sounds(self) -> None:
        """Тестирует звуковые эффекты"""
        print(f"\n{XSSColors.INFO}Тестирование звуков...{XSSColors.RESET}")
        test_sounds = ["keypress", "success", "fail", "coin", "alert"]
        
        for sound in test_sounds:
            if sound in SOUND_EFFECTS and os.path.exists(SOUND_EFFECTS[sound]):
                print(f"   Проигрывается: {sound}")
                self.play_sound(sound)
                time.sleep(1)  # Пауза между звуками
    
    def audio_menu(self) -> None:
        """Меню настроек аудио"""
        while True:
            print(f"\n{XSSColors.HEADER}━━━━━━━━━━ НАСТРОЙКИ ЗВУКА ━━━━━━━━━━{XSSColors.RESET}")
            
            # Показываем какой бэкенд используется
            print(f"\n{XSSColors.INFO}Аудио система: {self.audio_backend}{XSSColors.RESET}")
            
            print(f"\n{XSSColors.INFO}Текущий статус:{XSSColors.RESET}")
            print(f"   Фоновая музыка: {XSSColors.SUCCESS if self.music_enabled else XSSColors.ERROR}"
                  f"{'Включена' if self.music_enabled else 'Выключена'}{XSSColors.RESET}")
            
            # Для pygame показываем реальный статус воспроизведения
            if self.audio_backend == "pygame" and self.music_enabled:
                playing = self.is_music_playing()
                print(f"   Статус воспроизведения: {XSSColors.SUCCESS if playing else XSSColors.WARNING}"
                      f"{'Играет' if playing else 'Остановлена'}{XSSColors.RESET}")
            
            print(f"   Звуковые эффекты: {XSSColors.SUCCESS if self.sound_enabled else XSSColors.ERROR}"
                  f"{'Включены' if self.sound_enabled else 'Выключены'}{XSSColors.RESET}")
            
            print(f"\n{XSSColors.INFO}Управление:{XSSColors.RESET}")
            print(f"   [M] Вкл/выкл музыку")
            print(f"   [S] Вкл/выкл звуки")
            print(f"   [R] Перезапустить музыку")
            print(f"   [V] Громкость музыки")
            print(f"   [N] Громкость звуков")
            print(f"   [T] Тест звуков")
            print(f"   [Q] Выход")
            
            choice = input(f"\n{XSSColors.PROMPT}Выбор: {XSSColors.RESET}").lower()
            
            if choice == 'm':
                self.toggle_music()
            elif choice == 's':
                self.toggle_sounds()
            elif choice == 'r':
                if self.music_enabled:
                    self.stop_background_music()
                    time.sleep(0.5)
                    self.start_background_music()
                    print(f"{XSSColors.SUCCESS}[♪] Музыка перезапущена{XSSColors.RESET}")
            elif choice == 'v':
                if self.audio_backend == "pygame":
                    current_vol = self.get_music_volume()
                    print(f"\n{XSSColors.INFO}Текущая громкость музыки: {current_vol:.1f}{XSSColors.RESET}")
                    try:
                        new_vol = float(input(f"{XSSColors.PROMPT}Новая громкость (0.0-1.0): {XSSColors.RESET}"))
                        if self.set_music_volume(new_vol):
                            print(f"{XSSColors.SUCCESS}Громкость установлена: {new_vol:.1f}{XSSColors.RESET}")
                        else:
                            print(f"{XSSColors.ERROR}Громкость должна быть от 0.0 до 1.0{XSSColors.RESET}")
                    except ValueError:
                        print(f"{XSSColors.ERROR}Неверное значение{XSSColors.RESET}")
                else:
                    print(f"{XSSColors.WARNING}Регулировка громкости доступна только для pygame{XSSColors.RESET}")
            elif choice == 'n':
                print(f"\n{XSSColors.INFO}Текущая громкость звуков: {self.sound_volume:.1f}{XSSColors.RESET}")
                try:
                    new_vol = float(input(f"{XSSColors.PROMPT}Новая громкость (0.0-1.0): {XSSColors.RESET}"))
                    if self.set_sound_volume(new_vol):
                        print(f"{XSSColors.SUCCESS}Громкость звуков установлена: {new_vol:.1f}{XSSColors.RESET}")
                        self.play_sound("success")  # Тест
                    else:
                        print(f"{XSSColors.ERROR}Громкость должна быть от 0.0 до 1.0{XSSColors.RESET}")
                except ValueError:
                    print(f"{XSSColors.ERROR}Неверное значение{XSSColors.RESET}")
            elif choice == 't':
                self.test_sounds()
            elif choice == 'q':
                break
            else:
                print(f"{XSSColors.ERROR}Неверный выбор{XSSColors.RESET}")
            
            if choice != 'q':
                input(f"\n{XSSColors.INFO}Нажмите ENTER для продолжения...{XSSColors.RESET}")
    
    def get_input_with_sound(self, prompt: str) -> str:
        """Input со звуком нажатия клавиши"""
        self.play_sound("keypress")
        return input(prompt)


# Глобальный экземпляр аудио системы
audio_system = AudioSystem()