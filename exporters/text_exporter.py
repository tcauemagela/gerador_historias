"""
Exportador para formato TXT (texto simples).
"""

import re
from typing import List, Dict
from .base_exporter import BaseExporter


class TextExporter(BaseExporter):
    """Exporta histórias em texto simples"""

    def export(self, stories: List[Dict]) -> bytes:
        content = []

        for story in stories:
            # Remover markdown e formatar
            text = self._clean_markdown(story['historia_gerada'])
            content.append(text)
            content.append("\n\n" + "="*80 + "\n\n")

        return "".join(content).encode('utf-8')

    def _clean_markdown(self, text: str) -> str:
        """Remove formatação markdown"""
        # Remover ## ### etc
        text = re.sub(r'#{1,6}\s+', '', text)
        # Remover ** (negrito)
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        # Remover __ (itálico)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        # Remover ``` (código)
        text = re.sub(r'```[^\n]*\n', '', text)
        text = re.sub(r'```', '', text)
        return text

    def get_filename(self, base_name: str, timestamp: str) -> str:
        return f"{base_name}-{timestamp}.txt"

    def get_mime_type(self) -> str:
        return "text/plain"
