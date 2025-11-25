"""
View responsável pela interface de edição de histórias.
Permite editar seções com preview em tempo real.
Segue Single Responsibility Principle.
"""

import streamlit as st
from typing import Dict, Any, Optional
from controllers.editor_controller import EditorController
import re


def render_editor(editor_controller: EditorController):
    """
    Renderiza interface de edição de histórias.

    Args:
        editor_controller: Controller para processar edições
    """
    st.header("Editar Historia")

    # Verificar se há história para editar
    if 'current_story' not in st.session_state or not st.session_state.current_story:
        st.warning("Nenhuma historia para editar. Crie uma historia primeiro na aba 'Criar Historia'.")
        return

    current_story = st.session_state.current_story
    historia_markdown = current_story.get('historia_gerada', '')

    # Extrair seções do Markdown
    sections = _extract_sections(historia_markdown)

    st.info("Edite as secoes abaixo. As alteracoes serao salvas como nova versao.")

    # Layout em 2 colunas: Edição | Preview
    col_edit, col_preview = st.columns([1, 1])

    # Inicializar campos editáveis no session_state se não existirem
    if 'editing_fields' not in st.session_state:
        st.session_state.editing_fields = sections.copy()

    with col_edit:
        st.subheader("Edicao")

        # Título (extrair do ##)
        titulo_atual = _extract_title(historia_markdown)
        edited_titulo = st.text_input(
            "Titulo",
            value=titulo_atual,
            key="edit_titulo_input",
            help="Titulo principal da historia"
        )
        st.session_state.editing_fields['titulo'] = edited_titulo

        st.markdown("---")

        # Seções editáveis
        section_order = [
            'Contexto',
            'Objetivo',
            'Regras de Negocio',
            'APIs e Servicos Necessarios',
            'Objetivos Tecnicos',
            'Criterios de Aceitacao',
            'Cenarios de Teste Sugeridos',
            'Complexidade'
        ]

        for section_name in section_order:
            if section_name in sections:
                with st.expander(f"Editar: {section_name}", expanded=False):
                    edited_content = st.text_area(
                        section_name,
                        value=sections[section_name],
                        height=200,
                        key=f"edit_{section_name}",
                        label_visibility="collapsed"
                    )
                    st.session_state.editing_fields[section_name] = edited_content

    with col_preview:
        st.subheader("Preview")

        # Gerar preview em tempo real
        preview_markdown = _generate_preview(st.session_state.editing_fields)

        # Renderizar preview
        st.markdown(preview_markdown)

    # Botões de ação
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Salvar Alteracoes", type="primary", use_container_width=True):
            _save_edits(editor_controller)

    with col2:
        if st.button("Cancelar", use_container_width=True):
            st.session_state.editing_fields = sections.copy()
            st.info("Alteracoes descartadas")
            st.rerun()

    with col3:
        # Botão para adicionar nota
        with st.popover("Adicionar Nota"):
            note = st.text_area("Nota sobre esta edicao:", key="edit_note")
            if st.button("Salvar com Nota"):
                _save_edits(editor_controller, user_note=note)

    with col4:
        # Mostrar contador de versões
        version_count = editor_controller.get_version_count()
        st.metric("Versoes", f"{version_count}/10")


def _extract_sections(markdown_text: str) -> Dict[str, str]:
    """
    Extrai seções de um Markdown.

    Args:
        markdown_text: Texto em Markdown

    Returns:
        Dict com seções extraídas
    """
    sections = {}

    # Padrão para encontrar seções ### Nome
    pattern = r'###\s+([^\n]+)\n\n?((?:(?!###).)+)'

    matches = re.finditer(pattern, markdown_text, re.DOTALL)

    for match in matches:
        section_name = match.group(1).strip()
        section_content = match.group(2).strip()
        sections[section_name] = section_content

    return sections


def _extract_title(markdown_text: str) -> str:
    """
    Extrai título ## do Markdown.

    Args:
        markdown_text: Texto em Markdown

    Returns:
        Título extraído
    """
    match = re.search(r'^##\s+(.+)$', markdown_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def _generate_preview(edited_fields: Dict[str, str]) -> str:
    """
    Gera preview Markdown com campos editados.

    Args:
        edited_fields: Campos editados

    Returns:
        Markdown completo
    """
    parts = []

    # Título
    if 'titulo' in edited_fields:
        parts.append(f"## {edited_fields['titulo']}\n")

    # Seções na ordem
    section_order = [
        'Contexto',
        'Objetivo',
        'Regras de Negocio',
        'APIs e Servicos Necessarios',
        'Objetivos Tecnicos',
        'Criterios de Aceitacao',
        'Cenarios de Teste Sugeridos',
        'Complexidade'
    ]

    for section_name in section_order:
        if section_name in edited_fields and edited_fields[section_name]:
            parts.append(f"### {section_name}\n\n{edited_fields[section_name]}\n")

    return "\n".join(parts)


def _save_edits(editor_controller: EditorController, user_note: str = ""):
    """
    Salva edições realizadas.

    Args:
        editor_controller: Controller para processar
        user_note: Nota opcional do usuário
    """
    # Reconstruir história completa
    edited_markdown = _generate_preview(st.session_state.editing_fields)

    # Atualizar current_story
    updated_story = st.session_state.current_story.copy()
    updated_story['historia_gerada'] = edited_markdown

    # Atualizar também campos individuais se possível
    updated_story['titulo'] = st.session_state.editing_fields.get('titulo', '')

    # Processar via controller
    success, errors, new_version = editor_controller.handle_edit(
        edited_content=updated_story,
        user_note=user_note
    )

    if success:
        st.success(f"Alteracoes salvas! Versao {new_version.version_number} criada.")
        # Limpar campos de edição
        if 'editing_fields' in st.session_state:
            del st.session_state.editing_fields
        st.rerun()
    else:
        st.error("Erro ao salvar:")
        for error in errors:
            st.error(f"- {error}")


def render_regeneration_panel(editor_controller: EditorController):
    """
    Renderiza painel de regeneração de seções.

    Args:
        editor_controller: Controller para processar
    """
    st.subheader("Regenerar Secoes")

    if 'current_story' not in st.session_state or not st.session_state.current_story:
        st.warning("Nenhuma historia carregada")
        return

    st.info("Regenere secoes especificas mantendo o resto da historia intacto")

    # Obter dados do formulário original (se disponível)
    form_data = st.session_state.get('form_data', {})

    if not form_data:
        st.warning("Dados do formulario original nao encontrados. Regeneracao pode nao funcionar corretamente.")

    # Opções de seções
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Regenerar Criterios de Aceitacao", use_container_width=True):
            _regenerate_section(editor_controller, 'criterios', form_data)

        if st.button("Regenerar Cenarios de Teste", use_container_width=True):
            _regenerate_section(editor_controller, 'testes', form_data)

    with col2:
        if st.button("Regenerar Arquitetura", use_container_width=True):
            _regenerate_section(editor_controller, 'arquitetura', form_data)

        if st.button("Regenerar Beneficios", use_container_width=True):
            _regenerate_section(editor_controller, 'beneficios', form_data)


def _regenerate_section(
    editor_controller: EditorController,
    section_name: str,
    form_data: Dict[str, Any]
):
    """
    Regenera seção específica.

    Args:
        editor_controller: Controller
        section_name: Nome da seção
        form_data: Dados do formulário
    """
    with st.spinner(f"Regenerando {section_name}..."):
        regenerated, error = editor_controller.handle_regeneration(
            section_name=section_name,
            original_story=st.session_state.current_story,
            form_data=form_data
        )

        if error:
            st.error(f"Erro ao regenerar: {error}")
            return

        # Mostrar comparação
        st.success("Secao regenerada!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Versao Anterior:**")
            # Extrair seção antiga
            sections = _extract_sections(
                st.session_state.current_story.get('historia_gerada', '')
            )
            section_mapping = {
                'criterios': 'Criterios de Aceitacao',
                'testes': 'Cenarios de Teste Sugeridos',
                'arquitetura': 'Estrutura Tecnica',
                'beneficios': 'Beneficios'
            }
            old_section = sections.get(section_mapping.get(section_name, ''), 'Nao encontrada')
            st.markdown(old_section)

        with col2:
            st.markdown("**Nova Versao:**")
            st.markdown(regenerated)

        # Botões de ação
        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("Aceitar Nova Versao", key=f"accept_{section_name}"):
                success, new_version = editor_controller.apply_regenerated_section(
                    section_name=section_name,
                    regenerated_content=regenerated,
                    user_note=f"Regeneracao de {section_name}"
                )

                if success:
                    st.success("Nova versao aplicada!")
                    st.rerun()
                else:
                    st.error("Erro ao aplicar")

        with col_b:
            if st.button("Manter Versao Anterior", key=f"reject_{section_name}"):
                st.info("Versao anterior mantida")
                st.rerun()
