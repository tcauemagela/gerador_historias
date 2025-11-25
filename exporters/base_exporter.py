"""
Interface base para exportadores (Strategy Pattern).
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseExporter(ABC):
    """Interface base para exportadores de histórias"""

    @abstractmethod
    def export(self, stories: List[Dict]) -> bytes:
        """
        Exporta histórias para bytes.

        Args:
            stories: Lista de histórias (pode ser 1 ou múltiplas)

        Returns:
            Conteúdo do arquivo em bytes
        """
        pass

    @abstractmethod
    def get_filename(self, base_name: str, timestamp: str) -> str:
        """
        Retorna nome do arquivo com extensão.

        Args:
            base_name: Nome base (ex: titulo da história)
            timestamp: Timestamp formatado

        Returns:
            Nome completo do arquivo
        """
        pass

    @abstractmethod
    def get_mime_type(self) -> str:
        """
        Retorna MIME type para download.

        Returns:
            String com MIME type
        """
        pass
