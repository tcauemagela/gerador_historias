"""
Service responsável pelo controle de versões de histórias.
Gerencia histórico de até 10 versões durante a sessão.
Segue Single Responsibility Principle.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from models.version import StoryVersion
import difflib
import streamlit as st


class VersionService:
    """
    Service que gerencia versionamento de histórias.
    Mantém histórico de até 10 versões por história.
    """

    MAX_VERSIONS = 10

    def create_version(
        self,
        story_content: Dict[str, Any],
        changes_summary: str = "",
        user_note: str = ""
    ) -> StoryVersion:
        """
        Cria nova versão da história.

        Args:
            story_content: Conteúdo completo da história
            changes_summary: Resumo automático das mudanças
            user_note: Nota opcional do usuário

        Returns:
            Nova StoryVersion criada
        """
        # Inicializar lista de versões se não existir
        if 'story_versions' not in st.session_state:
            st.session_state.story_versions = []

        # Calcular número da versão
        version_number = len(st.session_state.story_versions) + 1

        # Criar nova versão
        new_version = StoryVersion(
            version_number=version_number,
            timestamp=datetime.now(),
            content=story_content,
            changes_summary=changes_summary or "Versão inicial",
            user_note=user_note
        )

        # Adicionar à lista
        st.session_state.story_versions.append(new_version)

        # Manter apenas as últimas MAX_VERSIONS versões
        if len(st.session_state.story_versions) > self.MAX_VERSIONS:
            st.session_state.story_versions.pop(0)
            # Renumerar versões
            self._renumber_versions()

        # Atualizar versão atual
        st.session_state.current_version = new_version.version_number

        return new_version

    def _renumber_versions(self):
        """Renumera versões após remoção da mais antiga."""
        for i, version in enumerate(st.session_state.story_versions, 1):
            version.version_number = i

    def get_versions(self) -> List[StoryVersion]:
        """
        Retorna lista de todas as versões.

        Returns:
            Lista de StoryVersion ordenada (mais recente primeiro)
        """
        if 'story_versions' not in st.session_state:
            return []

        # Retornar em ordem reversa (mais recente primeiro)
        return list(reversed(st.session_state.story_versions))

    def get_version(self, version_number: int) -> Optional[StoryVersion]:
        """
        Retorna versão específica.

        Args:
            version_number: Número da versão

        Returns:
            StoryVersion ou None se não encontrada
        """
        if 'story_versions' not in st.session_state:
            return None

        for version in st.session_state.story_versions:
            if version.version_number == version_number:
                return version

        return None

    def get_current_version(self) -> Optional[StoryVersion]:
        """
        Retorna versão atual.

        Returns:
            StoryVersion atual ou None
        """
        if 'story_versions' not in st.session_state or not st.session_state.story_versions:
            return None

        return st.session_state.story_versions[-1]

    def restore_version(self, version_number: int, user_note: str = "") -> Optional[StoryVersion]:
        """
        Restaura versão anterior criando nova versão.

        Args:
            version_number: Número da versão a restaurar
            user_note: Nota explicativa da restauração

        Returns:
            Nova versão criada ou None se versão não encontrada
        """
        version_to_restore = self.get_version(version_number)

        if not version_to_restore:
            return None

        # Criar nova versão com conteúdo restaurado
        changes_summary = f"Restaurado da versão {version_number}"
        note = user_note or f"Restauração da versão {version_number}"

        new_version = self.create_version(
            story_content=version_to_restore.content,
            changes_summary=changes_summary,
            user_note=note
        )

        return new_version

    def compare_versions(
        self,
        version_a_number: int,
        version_b_number: int
    ) -> Optional[Tuple[str, str, str]]:
        """
        Compara duas versões e retorna diff HTML.

        Args:
            version_a_number: Número da primeira versão
            version_b_number: Número da segunda versão

        Returns:
            Tupla (version_a_content, version_b_content, diff_html) ou None
        """
        version_a = self.get_version(version_a_number)
        version_b = self.get_version(version_b_number)

        if not version_a or not version_b:
            return None

        # Obter conteúdo em Markdown
        content_a = version_a.get_content_as_markdown()
        content_b = version_b.get_content_as_markdown()

        # Gerar diff HTML
        diff_html = self._generate_diff_html(content_a, content_b)

        return content_a, content_b, diff_html

    def _generate_diff_html(self, text_a: str, text_b: str) -> str:
        """
        Gera HTML com diff entre dois textos.

        Args:
            text_a: Texto da versão A
            text_b: Texto da versão B

        Returns:
            HTML com diferenças destacadas
        """
        differ = difflib.HtmlDiff(wrapcolumn=80)

        html_diff = differ.make_table(
            text_a.splitlines(),
            text_b.splitlines(),
            fromdesc='Versão Anterior',
            todesc='Versão Atual',
            context=True,
            numlines=3
        )

        return html_diff

    def get_simple_diff(self, text_a: str, text_b: str) -> List[str]:
        """
        Gera diff simplificado (texto apenas).

        Args:
            text_a: Texto anterior
            text_b: Texto novo

        Returns:
            Lista de linhas com diff
        """
        diff = difflib.unified_diff(
            text_a.splitlines(),
            text_b.splitlines(),
            lineterm='',
            n=1
        )

        return list(diff)

    def add_note_to_version(self, version_number: int, note: str) -> bool:
        """
        Adiciona nota a uma versão existente.

        Args:
            version_number: Número da versão
            note: Nota a adicionar

        Returns:
            True se sucesso, False se versão não encontrada
        """
        version = self.get_version(version_number)

        if not version:
            return False

        version.user_note = note
        return True

    def get_version_count(self) -> int:
        """
        Retorna número total de versões.

        Returns:
            Quantidade de versões armazenadas
        """
        if 'story_versions' not in st.session_state:
            return 0

        return len(st.session_state.story_versions)

    def is_limit_reached(self) -> bool:
        """
        Verifica se limite de versões foi atingido.

        Returns:
            True se atingiu limite de 10 versões
        """
        return self.get_version_count() >= self.MAX_VERSIONS

    def clear_versions(self):
        """
        Remove todas as versões.
        Útil ao criar nova história.
        """
        st.session_state.story_versions = []
        st.session_state.current_version = 0

    def export_version_history(self) -> List[Dict]:
        """
        Exporta histórico de versões para formato serializável.

        Returns:
            Lista de dicts com dados de cada versão
        """
        versions = self.get_versions()
        return [version.to_dict() for version in versions]
