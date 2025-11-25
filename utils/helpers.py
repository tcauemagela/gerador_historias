"""
Funções auxiliares gerais do sistema.
Utilidades que não se encaixam em outras categorias.
"""

import re
from datetime import datetime


def simplify_string(text: str) -> str:
    """
    Simplifica string removendo caracteres especiais e acentos.

    Args:
        text: Texto a simplificar

    Returns:
        Texto simplificado
    """
    # Remove acentos
    import unicodedata
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('ASCII')

    # Remove caracteres especiais
    text = re.sub(r'[^\w\s-]', '', text)

    # Substitui espaços por underscores
    text = re.sub(r'\s+', '_', text)

    return text.lower()


def generate_filename(titulo: str, extensao: str) -> str:
    """
    Gera nome de arquivo baseado no título e timestamp.

    Args:
        titulo: Título da história
        extensao: Extensão do arquivo (sem ponto)

    Returns:
        Nome de arquivo formatado
    """
    from utils.constants import MAX_FILENAME_LENGTH

    titulo_limpo = simplify_string(titulo)
    titulo_limpo = titulo_limpo[:MAX_FILENAME_LENGTH]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"{titulo_limpo}_{timestamp}.{extensao}"


def format_list_items(items: list[str], prefix: str = "-") -> str:
    """
    Formata lista de items com prefixo.

    Args:
        items: Lista de strings
        prefix: Prefixo para cada item (padrão: "-")

    Returns:
        String formatada com items
    """
    return "\n".join(f"{prefix} {item}" for item in items)


def remove_emojis(text: str) -> str:
    """
    Remove emojis de um texto.

    Args:
        text: Texto com emojis

    Returns:
        Texto sem emojis
    """
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
        u"\U0001F680-\U0001F6FF"  # transporte & mapas
        u"\U0001F1E0-\U0001F1FF"  # bandeiras
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


def sanitize_filename(filename: str, max_length: int = 50) -> str:
    """
    Remove caracteres inválidos e limita tamanho do nome de arquivo.
    Usado pelos exportadores.

    Args:
        filename: Nome original
        max_length: Comprimento máximo

    Returns:
        Nome sanitizado
    """
    import unicodedata

    # Remover acentos
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.encode('ASCII', 'ignore').decode('ASCII')

    # Remover caracteres especiais
    filename = re.sub(r'[^\w\s-]', '', filename)

    # Substituir espaços por hífen
    filename = re.sub(r'[\s]+', '-', filename)

    # Múltiplos hífens para um só
    filename = re.sub(r'-+', '-', filename)

    # Remover hífens nas pontas
    filename = filename.strip('-')

    # Limitar tamanho
    filename = filename[:max_length]

    # Lowercase
    filename = filename.lower()

    return filename or "historia"


def format_datetime_display(dt_str: str) -> str:
    """
    Formata string datetime ISO para exibição amigável.

    Args:
        dt_str: String datetime em formato ISO

    Returns:
        String formatada (DD/MM/YYYY HH:MM)
    """
    if isinstance(dt_str, str):
        dt = datetime.fromisoformat(dt_str)
    else:
        dt = dt_str

    return dt.strftime("%d/%m/%Y %H:%M")
