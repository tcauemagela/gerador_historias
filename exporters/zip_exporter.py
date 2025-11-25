"""
Exportador para formato ZIP (múltiplos arquivos).
"""

import zipfile
from io import BytesIO
from typing import List, Dict
from .base_exporter import BaseExporter
from .markdown_exporter import MarkdownExporter


class ZipExporter(BaseExporter):
    """Exporta múltiplas histórias em ZIP"""

    def export(self, stories: List[Dict]) -> bytes:
        buffer = BytesIO()

        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            md_exporter = MarkdownExporter()

            for i, story in enumerate(stories, 1):
                # Nome do arquivo individual
                from utils.helpers import sanitize_filename
                safe_title = sanitize_filename(story['titulo'])
                filename = f"historia-{i}-{safe_title}.md"

                # Conteúdo em markdown
                content = md_exporter.export([story])

                # Adicionar ao ZIP
                zip_file.writestr(f"historias/{filename}", content)

        return buffer.getvalue()

    def get_filename(self, base_name: str, timestamp: str) -> str:
        return f"historias-{timestamp}.zip"

    def get_mime_type(self) -> str:
        return "application/zip"
