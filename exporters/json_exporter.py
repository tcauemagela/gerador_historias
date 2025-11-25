"""
Exportador para formato JSON.
"""

import json
from typing import List, Dict
from .base_exporter import BaseExporter


class JSONExporter(BaseExporter):
    """Exporta histórias em JSON"""

    def export(self, stories: List[Dict]) -> bytes:
        # Se for apenas 1 história, exportar objeto
        if len(stories) == 1:
            data = stories[0]
        else:
            # Se múltiplas, exportar array
            data = stories

        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return json_str.encode('utf-8')

    def get_filename(self, base_name: str, timestamp: str) -> str:
        return f"{base_name}-{timestamp}.json"

    def get_mime_type(self) -> str:
        return "application/json"
