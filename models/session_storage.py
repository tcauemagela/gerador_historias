"""
Modelo de armazenamento em sessão.
Encapsula acesso ao session_state do Streamlit.
Implementa padrão Repository para histórias em memória.
"""

import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime


class SessionStorage:
    """Encapsula acesso ao session_state para histórias"""

    @staticmethod
    def get_all_stories() -> List[Dict]:
        """
        Retorna todas as histórias da sessão.

        Returns:
            Lista de dicionários com histórias
        """
        if 'stories' not in st.session_state:
            st.session_state.stories = []
        return st.session_state.stories

    @staticmethod
    def add_story(story: Dict) -> None:
        """
        Adiciona nova história à sessão.

        Args:
            story: Dicionário com dados da história
        """
        stories = SessionStorage.get_all_stories()
        stories.append(story)

    @staticmethod
    def get_story_by_id(story_id: str) -> Optional[Dict]:
        """
        Busca história por ID.

        Args:
            story_id: ID único da história

        Returns:
            Dicionário da história ou None se não encontrada
        """
        stories = SessionStorage.get_all_stories()
        for story in stories:
            if story['id'] == story_id:
                return story
        return None

    @staticmethod
    def update_story(story_id: str, updated_story: Dict) -> bool:
        """
        Atualiza história existente.

        Args:
            story_id: ID da história
            updated_story: Dados atualizados

        Returns:
            True se atualizou, False se não encontrou
        """
        stories = SessionStorage.get_all_stories()
        for i, story in enumerate(stories):
            if story['id'] == story_id:
                updated_story['updated_at'] = datetime.now().isoformat()
                stories[i] = updated_story
                return True
        return False

    @staticmethod
    def delete_story(story_id: str) -> bool:
        """
        Remove história da sessão.

        Args:
            story_id: ID da história

        Returns:
            True se removeu, False se não encontrou
        """
        stories = SessionStorage.get_all_stories()
        initial_len = len(stories)
        st.session_state.stories = [s for s in stories if s['id'] != story_id]
        return len(st.session_state.stories) < initial_len

    @staticmethod
    def clear_all() -> int:
        """
        Remove todas as histórias da sessão.

        Returns:
            Quantidade de histórias removidas
        """
        count = len(st.session_state.get('stories', []))
        st.session_state.stories = []
        return count

    @staticmethod
    def count_stories() -> int:
        """
        Conta histórias na sessão.

        Returns:
            Número total de histórias
        """
        return len(SessionStorage.get_all_stories())

    @staticmethod
    def get_stories_created_today() -> int:
        """
        Conta histórias criadas hoje.

        Returns:
            Número de histórias criadas hoje
        """
        stories = SessionStorage.get_all_stories()
        today = datetime.now().date()

        count = 0
        for story in stories:
            created_at = story.get('created_at')
            if created_at:
                if isinstance(created_at, str):
                    created_date = datetime.fromisoformat(created_at).date()
                else:
                    created_date = created_at.date()

                if created_date == today:
                    count += 1

        return count

    @staticmethod
    def get_average_complexity() -> float:
        """
        Calcula complexidade média das histórias.

        Returns:
            Complexidade média ou 0 se não houver histórias
        """
        stories = SessionStorage.get_all_stories()
        if not stories:
            return 0.0

        total = sum(s.get('complexidade', 0) for s in stories)
        return total / len(stories)

    @staticmethod
    def count_stories_with_versions() -> int:
        """
        Conta histórias que possuem versões.

        Returns:
            Número de histórias com versões
        """
        stories = SessionStorage.get_all_stories()
        return sum(1 for s in stories if s.get('versions'))
