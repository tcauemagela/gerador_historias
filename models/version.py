"""
Modelo de dados para controle de versões de histórias.
Gerencia histórico de edições durante a sessão.
Segue Single Responsibility Principle.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import json


@dataclass
class StoryVersion:
    """
    Representa uma versão específica de uma história.

    Attributes:
        version_number: Número sequencial da versão (1, 2, 3...)
        timestamp: Data/hora de criação da versão
        content: Conteúdo completo da história nesta versão
        changes_summary: Resumo automático das mudanças realizadas
        user_note: Nota opcional adicionada pelo usuário
    """

    version_number: int
    timestamp: datetime
    content: Dict[str, Any]
    changes_summary: str
    user_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte versão para dicionário.

        Returns:
            Dict com dados da versão
        """
        return {
            "version_number": self.version_number,
            "timestamp": self.timestamp.isoformat(),
            "content": self.content,
            "changes_summary": self.changes_summary,
            "user_note": self.user_note
        }

    def to_json(self) -> str:
        """
        Converte versão para JSON.

        Returns:
            String JSON com dados da versão
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StoryVersion':
        """
        Cria StoryVersion a partir de dicionário.

        Args:
            data: Dicionário com dados da versão

        Returns:
            Instância de StoryVersion
        """
        return cls(
            version_number=data["version_number"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            content=data["content"],
            changes_summary=data["changes_summary"],
            user_note=data.get("user_note")
        )

    def get_formatted_timestamp(self) -> str:
        """
        Retorna timestamp formatado para exibição.

        Returns:
            String formatada (ex: "24/11/2024 15:30")
        """
        return self.timestamp.strftime("%d/%m/%Y %H:%M")

    def get_content_as_markdown(self) -> str:
        """
        Converte conteúdo da versão para Markdown.

        Returns:
            História em formato Markdown
        """
        return self.content.get('historia_gerada', '')
