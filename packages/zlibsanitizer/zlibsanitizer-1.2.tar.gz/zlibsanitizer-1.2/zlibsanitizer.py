import re

# Константы для удаления меток
REMOVABLE_LABELS = [
    "Z-Library",
    "Z-library",
    "z-library",
    "Z-Lib",
    "z-lib",
    "Z.Library",
    "Z.library",
    "z.library",
    "Z.Lib",
    "z.lib",
    "ZLib",
    "Zlib",
    "zlib",
    "Z_Library",
    "Z_library",
    "z_library",
    "Z_Lib",
    "z_lib",
    "ZLibrary",
    "Zlibrary",
    "zlibrary",
]

all_labels = '|'.join(re.escape(label) for label in REMOVABLE_LABELS)

full_pattern = fr'(\[|\()?({all_labels})(\]|\))?'


def sanitize(text: str) -> str:
    text = re.sub(full_pattern, '', text)

    for idx in range(5):
        text = re.sub(r'[_-]+$', '', text)
        text = text.strip()

    return text
