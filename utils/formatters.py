"""
Formatadores de dados para diferentes tipos de exportação.
Segue Single Responsibility Principle.
"""

import json
import re
from typing import Dict, Any
from datetime import datetime


def format_to_text(markdown_content: str) -> str:
    """
    Converte conteúdo Markdown para texto simples.

    Args:
        markdown_content: Conteúdo em Markdown

    Returns:
        Texto simples formatado
    """
    text = markdown_content

    # Remove emojis
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)

    # Remove formatação Markdown
    text = re.sub(r'#{1,6}\s', '', text)  # Headers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # Italic
    text = re.sub(r'`(.+?)`', r'\1', text)  # Code
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Links

    return text.strip()


def format_to_json(story_data: Dict[str, Any]) -> str:
    """
    Formata dados da história para JSON estruturado.

    Args:
        story_data: Dicionário com dados da história

    Returns:
        String JSON formatada
    """
    return json.dumps(story_data, ensure_ascii=False, indent=2)


def format_to_markdown(content: str) -> str:
    """
    Garante que o conteúdo Markdown está bem formatado.

    Args:
        content: Conteúdo Markdown

    Returns:
        Markdown formatado
    """
    # Remove múltiplas linhas vazias
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Garante espaço após headers
    content = re.sub(r'(#{1,6}\s.+)\n([^\n])', r'\1\n\n\2', content)

    return content.strip()


def format_error_message(error_type: str, technical_details: str = "") -> Dict[str, str]:
    """
    Formata mensagens de erro de forma amigável.

    Args:
        error_type: Tipo do erro (timeout, rate_limit, connection, api_key, generic)
        technical_details: Detalhes técnicos do erro (opcional)

    Returns:
        Dict com título e mensagem formatados
    """
    error_messages = {
        "timeout": {
            "title": "⏱️ Tempo Esgotado",
            "message": "A IA demorou muito para responder. Tente novamente ou reduza a complexidade.",
            "suggestion": "Tente simplificar as informações ou aguarde alguns minutos."
        },
        "rate_limit": {
            "title": "🚫 Limite Atingido",
            "message": "Muitas requisições em pouco tempo. Aguarde alguns minutos.",
            "suggestion": "Aguarde 1-2 minutos antes de tentar novamente."
        },
        "connection": {
            "title": "🌐 Erro de Conexão",
            "message": "Não foi possível conectar à API da Anthropic.",
            "suggestion": "Verifique sua conexão com a internet."
        },
        "api_key": {
            "title": "🔑 Problema com API Key",
            "message": "A chave de API está inválida ou expirada.",
            "suggestion": "Verifique a configuração no arquivo .env ou Streamlit Secrets."
        },
        "generic": {
            "title": "❌ Erro Inesperado",
            "message": f"Ocorreu um erro ao gerar a história: {technical_details}",
            "suggestion": "Tente novamente ou entre em contato com o suporte."
        }
    }

    return error_messages.get(error_type, error_messages["generic"])
