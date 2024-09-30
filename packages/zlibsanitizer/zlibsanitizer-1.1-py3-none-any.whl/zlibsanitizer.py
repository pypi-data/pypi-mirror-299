import re

# Константы для удаления меток
REMOVABLE_LABELS = [
    r' ?\(Z-Library\)',  # Удаляет (Z-Library)
    r'_Z_Library',  # Удаляет _Z_Library
    r' ?\[Z-Library\]',  # Удаляет [Z-Library]
    r' Z-Library',
]


def sanitize(text: str) -> str:
    # Удаляем заданные метки
    for label in REMOVABLE_LABELS:
        text = re.sub(label, '', text)

    # Убираем лишние пробелы, подчеркивания и тире в конце строки
    text = text.strip()  # Убираем пробелы в начале и конце
    text = re.sub(r'[_-]+$', '', text)  # Удаляем лишние подчеркивания и тире в конце

    return text