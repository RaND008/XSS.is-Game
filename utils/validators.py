"""Утилиты для валидации пользовательского ввода"""

import re
from typing import Dict, Any


def validate_amount(value: str, min_val: float = 0, max_val: float = 1000000) -> Dict[str, Any]:
    """Валидация денежной суммы"""
    try:
        amount = float(value)
        if amount < min_val:
            return {"valid": False, "error": f"Сумма должна быть больше {min_val}"}
        if amount > max_val:
            return {"valid": False, "error": f"Сумма не может превышать {max_val}"}
        return {"valid": True, "value": amount}
    except (ValueError, OverflowError):
        return {"valid": False, "error": "Неверный формат числа"}


def validate_id(value: str, max_length: int = 50) -> Dict[str, Any]:
    """Валидация ID (миссий, предметов и т.д.)"""
    if not value or not isinstance(value, str):
        return {"valid": False, "error": "ID не может быть пустым"}

    value = value.strip()
    if len(value) > max_length:
        return {"valid": False, "error": f"ID слишком длинный (максимум {max_length} символов)"}

    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        return {"valid": False, "error": "ID может содержать только буквы, цифры, _ и -"}

    return {"valid": True, "value": value}