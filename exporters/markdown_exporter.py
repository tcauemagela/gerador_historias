"""
Exportador para formato Markdown com metadados.
"""

from typing import List, Dict
from .base_exporter import BaseExporter


class MarkdownExporter(BaseExporter):
    """Exporta histórias em Markdown com metadados"""

    def export(self, stories: List[Dict]) -> bytes:
        content = []

        for story in stories:
            # Adicionar metadados
            metadata = f"""---
id: {story['id']}
titulo: {story['titulo']}
created_at: {story['created_at']}
complexidade: {story['complexidade']}
---

"""
            content.append(metadata)
            content.append(story['historia_gerada'])
            content.append("\n\n---\n\n")

        return "".join(content).encode('utf-8')

    def get_filename(self, base_name: str, timestamp: str) -> str:
        return f"{base_name}-{timestamp}.md"

    def get_mime_type(self) -> str:
        return "text/markdown"
