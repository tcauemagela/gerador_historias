"""
Controller responsável por orquestrar edição, validação e versionamento.
Coordena Services e gerencia fluxo de dados entre Models e Views.
Segue padrão MVC e Single Responsibility Principle.
"""

from typing import Dict, Any, Optional, Tuple, List
import streamlit as st
from models.story import Story
from models.version import StoryVersion
from models.invest_validator import InvestScore, Suggestion
from models.session_storage import SessionStorage
from services.editor_service import EditorService
from services.version_service import VersionService
from services.invest_service import InvestService
from services.ai_service import AIService
import json


class EditorController:
    """
    Controller que orquestra funcionalidades de edição da ETAPA 2.
    Coordena Editor, Version, INVEST e AI Services.
    """

    def __init__(self, ai_service: AIService):
        """
        Inicializa controller com services necessários.

        Args:
            ai_service: Instância configurada do AIService
        """
        self.ai_service = ai_service
        self.editor_service = EditorService()
        self.version_service = VersionService()
        self.invest_service = InvestService()

    def handle_edit(
        self,
        edited_content: Dict[str, Any],
        user_note: str = ""
    ) -> Tuple[bool, List[str], Optional[StoryVersion]]:
        """
        Processa edição de história.

        Args:
            edited_content: Conteúdo editado pelo usuário
            user_note: Nota opcional sobre a edição

        Returns:
            Tupla (success, errors, new_version)
        """
        # Validar edição
        is_valid, errors = self.editor_service.validate_edit(edited_content)

        if not is_valid:
            return False, errors, None

        # Obter história atual
        if 'current_story' not in st.session_state:
            return False, ["Nenhuma história para editar"], None

        old_story = st.session_state.current_story

        # Calcular resumo de mudanças
        changes_summary = self.editor_service.extract_changes_summary(
            old_story,
            edited_content
        )

        # Atualizar história no session state
        st.session_state.current_story.update(edited_content)

        # Atualizar história no SessionStorage (ETAPA 3)
        story_id = st.session_state.current_story.get('id')
        if story_id:
            SessionStorage.update_story(story_id, st.session_state.current_story)

        # Criar nova versão
        new_version = self.version_service.create_version(
            story_content=st.session_state.current_story,
            changes_summary=changes_summary,
            user_note=user_note
        )

        return True, [], new_version

    def handle_regeneration(
        self,
        section_name: str,
        original_story: Dict[str, Any],
        form_data: Dict[str, Any]
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Regenera seção específica da história.

        Args:
            section_name: Nome da seção ("criterios", "testes", etc)
            original_story: História original completa
            form_data: Dados do formulário original

        Returns:
            Tupla (regenerated_section, error_message)
        """
        try:
            # Chamar AI Service para regenerar
            regenerated_section = self.ai_service.regenerate_section(
                section_name=section_name,
                original_story=original_story,
                form_data=form_data
            )

            # Sanitizar Markdown
            regenerated_section = self.editor_service.sanitize_markdown(
                regenerated_section
            )

            return regenerated_section, None

        except Exception as e:
            return None, str(e)

    def apply_regenerated_section(
        self,
        section_name: str,
        regenerated_content: str,
        user_note: str = ""
    ) -> Tuple[bool, Optional[StoryVersion]]:
        """
        Aplica seção regenerada à história atual.

        Args:
            section_name: Nome da seção regenerada
            regenerated_content: Conteúdo regenerado
            user_note: Nota sobre a regeneração

        Returns:
            Tupla (success, new_version)
        """
        if 'current_story' not in st.session_state:
            return False, None

        # Atualizar seção na história
        # Aqui você pode implementar lógica para substituir seção específica
        # no Markdown completo da história

        current_story = st.session_state.current_story
        historia_atual = current_story.get('historia_gerada', '')

        # Substituir seção no Markdown
        # Esta é uma implementação simplificada
        # Em produção, você faria parsing mais robusto
        updated_historia = self._replace_section_in_markdown(
            historia_atual,
            section_name,
            regenerated_content
        )

        current_story['historia_gerada'] = updated_historia

        # Atualizar história no SessionStorage (ETAPA 3)
        story_id = current_story.get('id')
        if story_id:
            SessionStorage.update_story(story_id, current_story)

        # Criar nova versão
        changes_summary = f"Regenerada seção: {section_name}"
        new_version = self.version_service.create_version(
            story_content=current_story,
            changes_summary=changes_summary,
            user_note=user_note or f"Regeneração de {section_name}"
        )

        return True, new_version

    def _replace_section_in_markdown(
        self,
        markdown_text: str,
        section_name: str,
        new_content: str
    ) -> str:
        """
        Substitui seção específica no Markdown.

        Args:
            markdown_text: Markdown completo
            section_name: Nome da seção
            new_content: Novo conteúdo da seção

        Returns:
            Markdown atualizado
        """
        import re

        section_mapping = {
            'criterios': 'Criterios de Aceitacao',
            'testes': 'Cenarios de Teste Sugeridos',
            'arquitetura': 'Estrutura Tecnica',
            'beneficios': 'Beneficios'
        }

        section_label = section_mapping.get(section_name, section_name)

        # Padrão para encontrar a seção
        pattern = rf"(###\s+{section_label}.*?)(?=###|\Z)"

        # Substituir seção
        replacement = new_content if new_content.startswith('###') else f"### {section_label}\n\n{new_content}"

        updated_text = re.sub(
            pattern,
            replacement,
            markdown_text,
            flags=re.DOTALL
        )

        return updated_text

    def validate_invest_local(
        self,
        story: Dict[str, Any]
    ) -> InvestScore:
        """
        Valida história com regras locais (sem IA).

        Args:
            story: História completa

        Returns:
            InvestScore com scores básicos
        """
        return self.invest_service.validate_invest_local(story)

    def validate_invest_with_ai(
        self,
        story: Dict[str, Any]
    ) -> Tuple[Optional[InvestScore], Optional[str]]:
        """
        Valida história usando IA (análise profunda).

        Args:
            story: História completa

        Returns:
            Tupla (invest_score, error_message)
        """
        try:
            # Chamar AI Service
            ai_response = self.ai_service.validate_invest_with_ai(story)

            # Parsear resposta
            invest_score = self.invest_service.parse_ai_validation_response(ai_response)

            return invest_score, None

        except Exception as e:
            # Em caso de erro, retornar validação local
            local_score = self.invest_service.validate_invest_local(story)
            return local_score, f"Erro na validação com IA: {str(e)}"

    def analyze_and_suggest(
        self,
        story: Dict[str, Any]
    ) -> Tuple[Optional[List[Suggestion]], Optional[str]]:
        """
        Analisa história e retorna sugestões de melhoria.

        Args:
            story: História completa

        Returns:
            Tupla (suggestions, error_message)
        """
        try:
            # Chamar AI Service
            ai_response = self.ai_service.analyze_and_suggest(story)

            # Parsear resposta JSON
            suggestions_data = json.loads(ai_response)

            # Converter para objetos Suggestion
            suggestions = [
                Suggestion(
                    type=s['type'],
                    severity=s['severity'],
                    problem=s['problem'],
                    suggestion=s['suggestion'],
                    applicable=s.get('applicable', False)
                )
                for s in suggestions_data
            ]

            return suggestions, None

        except json.JSONDecodeError:
            return None, "Erro ao processar resposta da IA"
        except Exception as e:
            return None, str(e)

    def restore_version(
        self,
        version_number: int,
        user_note: str = ""
    ) -> Tuple[bool, Optional[StoryVersion], Optional[str]]:
        """
        Restaura versão anterior da história.

        Args:
            version_number: Número da versão a restaurar
            user_note: Nota sobre a restauração

        Returns:
            Tupla (success, new_version, error_message)
        """
        try:
            # Restaurar versão via service
            new_version = self.version_service.restore_version(
                version_number,
                user_note
            )

            if not new_version:
                return False, None, f"Versão {version_number} não encontrada"

            # Atualizar current_story no session state
            st.session_state.current_story = new_version.content

            return True, new_version, None

        except Exception as e:
            return False, None, str(e)

    def compare_versions(
        self,
        version_a: int,
        version_b: int
    ) -> Tuple[Optional[Tuple[str, str, str]], Optional[str]]:
        """
        Compara duas versões da história.

        Args:
            version_a: Número da primeira versão
            version_b: Número da segunda versão

        Returns:
            Tupla ((content_a, content_b, diff_html), error_message)
        """
        try:
            result = self.version_service.compare_versions(version_a, version_b)

            if not result:
                return None, f"Versões {version_a} ou {version_b} não encontradas"

            return result, None

        except Exception as e:
            return None, str(e)

    def get_version_history(self) -> List[StoryVersion]:
        """
        Retorna histórico de versões.

        Returns:
            Lista de StoryVersion (mais recente primeiro)
        """
        return self.version_service.get_versions()

    def get_current_version(self) -> Optional[StoryVersion]:
        """
        Retorna versão atual.

        Returns:
            StoryVersion atual ou None
        """
        return self.version_service.get_current_version()

    def add_note_to_version(
        self,
        version_number: int,
        note: str
    ) -> bool:
        """
        Adiciona nota a uma versão.

        Args:
            version_number: Número da versão
            note: Nota a adicionar

        Returns:
            True se sucesso, False se versão não encontrada
        """
        return self.version_service.add_note_to_version(version_number, note)

    def initialize_first_version(self, story: Dict[str, Any]):
        """
        Cria primeira versão ao gerar história nova.

        Args:
            story: História recém-gerada
        """
        # Limpar versões antigas
        self.version_service.clear_versions()

        # Criar primeira versão
        self.version_service.create_version(
            story_content=story,
            changes_summary="Versão inicial gerada pela IA",
            user_note=""
        )

    def can_add_version(self) -> bool:
        """
        Verifica se pode adicionar mais versões.

        Returns:
            True se não atingiu limite de 10 versões
        """
        return not self.version_service.is_limit_reached()

    def get_version_count(self) -> int:
        """
        Retorna número de versões armazenadas.

        Returns:
            Quantidade de versões
        """
        return self.version_service.get_version_count()
