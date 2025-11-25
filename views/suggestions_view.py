"""
View responsável pela exibição de sugestões de melhoria com IA.
Analisa história e exibe sugestões acionáveis.
Segue Single Responsibility Principle.
"""

import streamlit as st
from typing import List
from models.invest_validator import Suggestion
from controllers.editor_controller import EditorController


def render_suggestions(editor_controller: EditorController):
    """
    Renderiza interface de sugestões de melhoria.

    Args:
        editor_controller: Controller para análise
    """
    st.header("Sugestoes de Melhoria")

    if 'current_story' not in st.session_state or not st.session_state.current_story:
        st.warning("Nenhuma historia para analisar. Crie uma historia primeiro.")
        return

    st.info("Use IA para analisar a historia e receber sugestoes acionaveis de melhoria")

    # Botão para gerar sugestões
    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("Analisar com IA", type="primary", use_container_width=True):
            _run_analysis(editor_controller)

    with col2:
        # Mostrar info sobre o tipo de análise
        st.caption("A IA analisara estrutura, clareza, completude e criterios INVEST")

    st.markdown("---")

    # Exibir sugestões se disponíveis
    if 'suggestions' in st.session_state and st.session_state.suggestions:
        _display_suggestions(st.session_state.suggestions, editor_controller)
    else:
        st.info("Clique em 'Analisar com IA' para gerar sugestoes")


def _run_analysis(editor_controller: EditorController):
    """
    Executa análise com IA para gerar sugestões.

    Args:
        editor_controller: Controller
    """
    with st.spinner("Analisando historia com IA... (pode levar ate 20 segundos)"):
        suggestions, error = editor_controller.analyze_and_suggest(
            st.session_state.current_story
        )

        if error:
            st.error(f"Erro ao analisar: {error}")
            return

        if suggestions:
            st.session_state.suggestions = suggestions
            st.success(f"Analise concluida! {len(suggestions)} sugestoes geradas.")
            st.rerun()
        else:
            st.warning("Nenhuma sugestao gerada pela IA")


def _display_suggestions(suggestions: List[Suggestion], editor_controller: EditorController):
    """
    Exibe lista de sugestões com formatação adequada.

    Args:
        suggestions: Lista de Suggestion objects
        editor_controller: Controller para aplicar sugestões
    """
    st.subheader(f"Sugestoes Encontradas ({len(suggestions)})")

    # Filtros
    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        severity_filter = st.selectbox(
            "Filtrar por Severidade:",
            options=["Todas", "critica", "alta", "media", "baixa"],
            index=0
        )

    with col_filter2:
        type_filter = st.selectbox(
            "Filtrar por Tipo:",
            options=["Todos", "estrutura", "clareza", "completude", "invest"],
            index=0
        )

    st.markdown("---")

    # Filtrar sugestões
    filtered_suggestions = _filter_suggestions(
        suggestions,
        severity_filter,
        type_filter
    )

    if not filtered_suggestions:
        st.info("Nenhuma sugestao corresponde aos filtros selecionados")
        return

    # Ordenar por severidade (crítica -> baixa)
    severity_order = {"critica": 0, "alta": 1, "media": 2, "baixa": 3}
    sorted_suggestions = sorted(
        filtered_suggestions,
        key=lambda s: severity_order.get(s.severity, 4)
    )

    # Exibir cada sugestão
    for idx, suggestion in enumerate(sorted_suggestions, 1):
        _render_suggestion_card(idx, suggestion, editor_controller)


def _filter_suggestions(
    suggestions: List[Suggestion],
    severity_filter: str,
    type_filter: str
) -> List[Suggestion]:
    """
    Filtra sugestões por severidade e tipo.

    Args:
        suggestions: Lista original
        severity_filter: Filtro de severidade
        type_filter: Filtro de tipo

    Returns:
        Lista filtrada
    """
    filtered = suggestions

    if severity_filter != "Todas":
        filtered = [s for s in filtered if s.severity == severity_filter]

    if type_filter != "Todos":
        filtered = [s for s in filtered if s.type == type_filter]

    return filtered


def _render_suggestion_card(
    index: int,
    suggestion: Suggestion,
    editor_controller: EditorController
):
    """
    Renderiza card individual de sugestão.

    Args:
        index: Número da sugestão
        suggestion: Objeto Suggestion
        editor_controller: Controller
    """
    # Container para a sugestão
    with st.container():
        # Cabeçalho com severidade e tipo
        col_header1, col_header2, col_header3 = st.columns([2, 1, 1])

        with col_header1:
            st.markdown(f"### Sugestao {index}")

        with col_header2:
            # Badge de severidade com cor
            severity_colors = {
                "critica": "🔴",
                "alta": "🟠",
                "media": "🟡",
                "baixa": "🟢"
            }
            severity_icon = severity_colors.get(suggestion.severity, "⚪")
            st.markdown(f"{severity_icon} **{suggestion.severity.upper()}**")

        with col_header3:
            # Badge de tipo
            type_icons = {
                "estrutura": "📐",
                "clareza": "💡",
                "completude": "📋",
                "invest": "✅"
            }
            type_icon = type_icons.get(suggestion.type, "📌")
            st.caption(f"{type_icon} {suggestion.type}")

        # Problema identificado
        st.markdown("**Problema:**")
        st.warning(suggestion.problem)

        # Sugestão de melhoria
        st.markdown("**Sugestao:**")
        st.success(suggestion.suggestion)

        # Ações
        col_action1, col_action2 = st.columns([1, 3])

        with col_action1:
            if suggestion.applicable:
                if st.button("Aplicar", key=f"apply_{index}", use_container_width=True):
                    _apply_suggestion(suggestion, editor_controller, index)
            else:
                st.caption("Aplicacao manual necessaria")

        with col_action2:
            # Nota de contexto
            if suggestion.applicable:
                st.caption("Esta sugestao pode ser aplicada automaticamente")
            else:
                st.caption("Revise e aplique esta sugestao manualmente na edicao")

        st.markdown("---")


def _apply_suggestion(
    suggestion: Suggestion,
    editor_controller: EditorController,
    index: int
):
    """
    Aplica sugestão automaticamente (se aplicável).

    Args:
        suggestion: Sugestão a aplicar
        editor_controller: Controller
        index: Índice da sugestão
    """
    # Implementação simplificada
    # Em produção, você implementaria lógica específica por tipo de sugestão
    st.info(f"Aplicando sugestao {index}...")

    # Aqui você implementaria a lógica de aplicação automática
    # Por exemplo:
    # - Se tipo == "estrutura", reorganizar seções
    # - Se tipo == "completude", adicionar campos faltantes
    # - Etc.

    # Por enquanto, apenas marcar como aplicada
    st.success("Sugestao aplicada! Revise as alteracoes na aba 'Editar'")


def render_suggestion_summary(editor_controller: EditorController):
    """
    Renderiza resumo de sugestões em sidebar ou card.

    Args:
        editor_controller: Controller
    """
    if 'suggestions' not in st.session_state or not st.session_state.suggestions:
        return

    suggestions = st.session_state.suggestions

    # Contar por severidade
    severity_counts = {
        "critica": 0,
        "alta": 0,
        "media": 0,
        "baixa": 0
    }

    for suggestion in suggestions:
        severity_counts[suggestion.severity] = severity_counts.get(suggestion.severity, 0) + 1

    # Exibir resumo
    st.markdown("#### Resumo de Sugestoes")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total", len(suggestions))

    with col2:
        critical_count = severity_counts.get("critica", 0)
        if critical_count > 0:
            st.metric("Criticas", critical_count, delta=None, delta_color="inverse")

    # Mostrar distribuição
    if severity_counts.get("critica", 0) > 0:
        st.error(f"🔴 {severity_counts['critica']} Critica(s)")

    if severity_counts.get("alta", 0) > 0:
        st.warning(f"🟠 {severity_counts['alta']} Alta(s)")

    if severity_counts.get("media", 0) > 0:
        st.info(f"🟡 {severity_counts['media']} Media(s)")

    if severity_counts.get("baixa", 0) > 0:
        st.success(f"🟢 {severity_counts['baixa']} Baixa(s)")
