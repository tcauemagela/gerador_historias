"""
View responsável pela visualização de versões e histórico.
Exibe timeline, comparação visual (diff), e permite restauração.
Segue Single Responsibility Principle.
"""

import streamlit as st
from typing import List, Optional, Tuple
from models.version import StoryVersion
from controllers.editor_controller import EditorController
from datetime import datetime


def render_version_history(editor_controller: EditorController):
    """
    Renderiza interface de histórico de versões.

    Args:
        editor_controller: Controller para gerenciar versões
    """
    st.header("Historico de Versoes")

    # Obter versões
    versions = editor_controller.get_version_history()

    if not versions:
        st.info("Nenhuma versao salva ainda. Crie ou edite uma historia para gerar versoes.")
        return

    # Informações gerais
    col_info1, col_info2, col_info3 = st.columns(3)

    with col_info1:
        st.metric("Versoes Salvas", f"{len(versions)}/10")

    with col_info2:
        current_version = editor_controller.get_current_version()
        if current_version:
            st.metric("Versao Atual", f"v{current_version.version_number}")

    with col_info3:
        # Última modificação
        if versions:
            last_modified = versions[0].timestamp
            st.metric("Ultima Alteracao", last_modified.strftime("%d/%m %H:%M"))

    st.markdown("---")

    # Layout: Timeline | Detalhes
    col_timeline, col_details = st.columns([1, 2])

    with col_timeline:
        st.subheader("Timeline")
        selected_version = _render_version_timeline(versions)

    with col_details:
        st.subheader("Detalhes")
        if selected_version:
            _render_version_details(selected_version, editor_controller)

    st.markdown("---")

    # Comparação de versões
    _render_version_comparison(versions, editor_controller)


def _render_version_timeline(versions: List[StoryVersion]) -> Optional[StoryVersion]:
    """
    Renderiza timeline de versões como lista clicável.

    Args:
        versions: Lista de StoryVersion

    Returns:
        Versão selecionada ou None
    """
    # Inicializar seleção
    if 'selected_version_number' not in st.session_state:
        st.session_state.selected_version_number = versions[0].version_number if versions else None

    selected_version = None

    for version in versions:
        # Card de versão na timeline
        is_selected = st.session_state.selected_version_number == version.version_number

        # Container com borda se selecionado
        container_key = f"version_{version.version_number}"

        with st.container():
            # Cabeçalho
            col_v1, col_v2 = st.columns([3, 1])

            with col_v1:
                label = f"**v{version.version_number}**"
                if is_selected:
                    st.markdown(f"🔵 {label}")
                else:
                    st.markdown(label)

            with col_v2:
                st.caption(version.timestamp.strftime("%d/%m"))

            # Resumo de mudanças
            st.caption(version.changes_summary[:60] + "..." if len(version.changes_summary) > 60 else version.changes_summary)

            # Nota do usuário se houver
            if version.user_note:
                st.caption(f"📝 {version.user_note[:40]}...")

            # Botão para selecionar
            if st.button("Ver Detalhes", key=f"select_{version.version_number}", use_container_width=True):
                st.session_state.selected_version_number = version.version_number
                st.rerun()

            st.markdown("---")

        if is_selected:
            selected_version = version

    return selected_version


def _render_version_details(version: StoryVersion, editor_controller: EditorController):
    """
    Renderiza detalhes completos de uma versão.

    Args:
        version: Versão selecionada
        editor_controller: Controller
    """
    # Informações da versão
    st.markdown(f"### Versao {version.version_number}")

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        st.markdown(f"**Data:** {version.timestamp.strftime('%d/%m/%Y %H:%M:%S')}")

    with col_d2:
        st.markdown(f"**Modificacao:** {version.changes_summary}")

    if version.user_note:
        st.markdown("**Nota do Usuario:**")
        st.info(version.user_note)

    st.markdown("---")

    # Preview do conteúdo
    st.markdown("**Preview da Historia:**")

    with st.expander("Ver conteudo completo", expanded=False):
        historia_texto = version.content.get('historia_gerada', 'Conteudo nao disponivel')
        st.markdown(historia_texto)

    # Campos estruturados
    with st.expander("Ver dados estruturados", expanded=False):
        col_data1, col_data2 = st.columns(2)

        with col_data1:
            st.markdown(f"**Titulo:** {version.content.get('titulo', 'N/A')}")
            st.markdown(f"**Complexidade:** {version.content.get('complexidade', 'N/A')}")

        with col_data2:
            criterios = version.content.get('criterios_aceitacao', [])
            st.markdown(f"**Criterios:** {len(criterios)}")

            objetivos = version.content.get('objetivos', [])
            st.markdown(f"**Objetivos:** {len(objetivos)}")

    st.markdown("---")

    # Ações
    col_action1, col_action2, col_action3 = st.columns(3)

    with col_action1:
        # Restaurar versão
        current_version = editor_controller.get_current_version()
        if current_version and current_version.version_number != version.version_number:
            if st.button("Restaurar Esta Versao", type="primary", use_container_width=True):
                _restore_version(version.version_number, editor_controller)
        else:
            st.info("Versao atual")

    with col_action2:
        # Adicionar nota
        with st.popover("Adicionar Nota"):
            note = st.text_area("Nota:", key=f"note_{version.version_number}")
            if st.button("Salvar Nota", key=f"save_note_{version.version_number}"):
                _add_note_to_version(version.version_number, note, editor_controller)

    with col_action3:
        # Exportar versão
        historia_texto = version.content.get('historia_gerada', '')
        st.download_button(
            label="Exportar (MD)",
            data=historia_texto,
            file_name=f"historia_v{version.version_number}.md",
            mime="text/markdown",
            use_container_width=True
        )


def _restore_version(version_number: int, editor_controller: EditorController):
    """
    Restaura versão específica.

    Args:
        version_number: Número da versão
        editor_controller: Controller
    """
    with st.spinner(f"Restaurando versao {version_number}..."):
        success, new_version, error = editor_controller.restore_version(
            version_number,
            user_note=f"Restaurada versao {version_number}"
        )

        if success:
            st.success(f"Versao {version_number} restaurada! Nova versao {new_version.version_number} criada.")
            st.rerun()
        else:
            st.error(f"Erro ao restaurar: {error}")


def _add_note_to_version(
    version_number: int,
    note: str,
    editor_controller: EditorController
):
    """
    Adiciona nota a uma versão.

    Args:
        version_number: Número da versão
        note: Nota a adicionar
        editor_controller: Controller
    """
    if not note.strip():
        st.warning("Nota vazia")
        return

    success = editor_controller.add_note_to_version(version_number, note)

    if success:
        st.success("Nota adicionada!")
        st.rerun()
    else:
        st.error("Erro ao adicionar nota")


def _render_version_comparison(versions: List[StoryVersion], editor_controller: EditorController):
    """
    Renderiza interface de comparação entre versões.

    Args:
        versions: Lista de versões
        editor_controller: Controller
    """
    st.subheader("Comparar Versoes")

    if len(versions) < 2:
        st.info("Precisa de pelo menos 2 versoes para comparar")
        return

    # Seletores de versão
    col_comp1, col_comp2, col_comp3 = st.columns([2, 2, 1])

    version_numbers = [v.version_number for v in versions]

    with col_comp1:
        version_a = st.selectbox(
            "Versao A:",
            options=version_numbers,
            index=0,
            key="compare_version_a"
        )

    with col_comp2:
        # Padrão: versão anterior à A
        default_b_index = 1 if len(version_numbers) > 1 else 0
        version_b = st.selectbox(
            "Versao B:",
            options=version_numbers,
            index=default_b_index,
            key="compare_version_b"
        )

    with col_comp3:
        compare_button = st.button("Comparar", type="secondary", use_container_width=True)

    if compare_button:
        if version_a == version_b:
            st.warning("Selecione versoes diferentes")
        else:
            _display_diff(version_a, version_b, editor_controller)


def _display_diff(
    version_a: int,
    version_b: int,
    editor_controller: EditorController
):
    """
    Exibe comparação visual (diff) entre duas versões.

    Args:
        version_a: Número da versão A
        version_b: Número da versão B
        editor_controller: Controller
    """
    st.markdown("---")
    st.markdown(f"### Comparacao: v{version_a} vs v{version_b}")

    with st.spinner("Gerando comparacao..."):
        result, error = editor_controller.compare_versions(version_a, version_b)

        if error:
            st.error(f"Erro ao comparar: {error}")
            return

        if not result:
            st.error("Versoes nao encontradas")
            return

        content_a, content_b, diff_html = result

    # Mostrar diff
    st.markdown("**Diferencas:**")

    # Renderizar HTML do diff
    if diff_html:
        st.markdown(diff_html, unsafe_allow_html=True)
    else:
        st.info("Nenhuma diferenca encontrada")

    st.markdown("---")

    # Mostrar conteúdos lado a lado
    st.markdown("**Comparacao Lado a Lado:**")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"**Versao {version_a}**")
        with st.expander("Ver conteudo completo"):
            st.text_area(
                f"v{version_a}",
                value=content_a,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

    with col_b:
        st.markdown(f"**Versao {version_b}**")
        with st.expander("Ver conteudo completo"):
            st.text_area(
                f"v{version_b}",
                value=content_b,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )


def render_version_stats(editor_controller: EditorController):
    """
    Renderiza estatísticas de versões (para sidebar ou card).

    Args:
        editor_controller: Controller
    """
    versions = editor_controller.get_version_history()

    if not versions:
        st.caption("Nenhuma versao salva")
        return

    st.markdown("#### Estatisticas de Versoes")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total", f"{len(versions)}/10")

    with col2:
        current = editor_controller.get_current_version()
        if current:
            st.metric("Atual", f"v{current.version_number}")

    # Última modificação
    if versions:
        last_modified = versions[0].timestamp
        hours_ago = (datetime.now() - last_modified).total_seconds() / 3600

        if hours_ago < 1:
            time_text = "Há poucos minutos"
        elif hours_ago < 24:
            time_text = f"Há {int(hours_ago)} hora(s)"
        else:
            time_text = f"Há {int(hours_ago/24)} dia(s)"

        st.caption(f"Ultima modificacao: {time_text}")
