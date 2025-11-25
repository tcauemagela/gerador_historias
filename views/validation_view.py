"""
View responsável pela visualização de validação INVEST.
Exibe scores, justificativas e status visual.
Segue Single Responsibility Principle.
"""

import streamlit as st
from models.invest_validator import InvestScore
from controllers.editor_controller import EditorController


def render_invest_validation(editor_controller: EditorController):
    """
    Renderiza interface de validação INVEST.

    Args:
        editor_controller: Controller para validação
    """
    st.header("Validacao INVEST")

    if 'current_story' not in st.session_state or not st.session_state.current_story:
        st.warning("Nenhuma historia para validar. Crie uma historia primeiro.")
        return

    st.markdown("""
    **INVEST** é um acrônimo para os 6 critérios de qualidade de histórias de usuário:
    - **I**ndependent (Independente)
    - **N**egotiable (Negociável)
    - **V**aluable (Valiosa)
    - **E**stimable (Estimável)
    - **S**mall (Pequena)
    - **T**estable (Testável)
    """)

    st.markdown("---")

    # Opções de validação
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Validacao Rapida (Local)", use_container_width=True, type="secondary"):
            _run_local_validation(editor_controller)

    with col2:
        if st.button("Validacao Profunda (com IA)", use_container_width=True, type="primary"):
            _run_ai_validation(editor_controller)

    # Exibir resultados se disponível
    if 'invest_score' in st.session_state and st.session_state.invest_score:
        _display_invest_results(st.session_state.invest_score)


def _run_local_validation(editor_controller: EditorController):
    """
    Executa validação local (rápida).

    Args:
        editor_controller: Controller
    """
    with st.spinner("Validando historia..."):
        invest_score = editor_controller.validate_invest_local(
            st.session_state.current_story
        )

        st.session_state.invest_score = invest_score
        st.success("Validacao local concluida!")
        st.rerun()


def _run_ai_validation(editor_controller: EditorController):
    """
    Executa validação com IA (profunda).

    Args:
        editor_controller: Controller
    """
    with st.spinner("Analisando historia com IA... (pode levar ate 15 segundos)"):
        invest_score, error = editor_controller.validate_invest_with_ai(
            st.session_state.current_story
        )

        if error:
            st.warning(f"Usando validacao local devido a erro: {error}")

        if invest_score:
            st.session_state.invest_score = invest_score
            st.success("Validacao com IA concluida!")
            st.rerun()
        else:
            st.error("Erro ao validar com IA")


def _display_invest_results(invest_score: InvestScore):
    """
    Exibe resultados da validação INVEST.

    Args:
        invest_score: Scores INVEST
    """
    st.markdown("---")
    st.subheader("Resultados da Validacao")

    # Score geral
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.metric("Score Geral INVEST", f"{invest_score.overall}%")

    with col2:
        # Indicador de cor
        color = invest_score.get_status_color()
        label = invest_score.get_status_label()

        if color == "green":
            st.success(f"Status: {label}")
        elif color == "orange":
            st.warning(f"Status: {label}")
        else:
            st.error(f"Status: {label}")

    with col3:
        # Barra de progresso visual
        st.progress(invest_score.overall / 100)

    st.markdown("---")

    # Scores individuais por critério
    st.subheader("Scores por Criterio")

    criteria = [
        ('independent', 'Independent (Independente)', 'História pode ser desenvolvida sozinha'),
        ('negotiable', 'Negotiable (Negociavel)', 'Tem flexibilidade de implementação'),
        ('valuable', 'Valuable (Valiosa)', 'Entrega valor claro'),
        ('estimable', 'Estimable (Estimavel)', 'Pode ser estimada com precisão'),
        ('small', 'Small (Pequena)', 'Tamanho adequado para uma sprint'),
        ('testable', 'Testable (Testavel)', 'Possui critérios testáveis')
    ]

    for attr, label, description in criteria:
        score = getattr(invest_score, attr)
        justification = invest_score.justifications.get(attr, "Sem justificativa")

        col_a, col_b = st.columns([1, 2])

        with col_a:
            st.markdown(f"**{label}**")
            st.caption(description)

        with col_b:
            # Barra de progresso com cor
            if score >= 80:
                st.progress(score / 100)
                st.markdown(f"✅ **{score}%** - Bom")
            elif score >= 50:
                st.progress(score / 100)
                st.markdown(f"⚠️ **{score}%** - Regular")
            else:
                st.progress(score / 100)
                st.markdown(f"❌ **{score}%** - Fraco")

            # Justificativa em expander
            with st.expander("Ver justificativa"):
                st.write(justification)

        st.markdown("---")

    # Pontos fortes e fracos
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Pontos Fortes")

        if invest_score.strengths:
            for strength in invest_score.strengths:
                st.success(f"✓ {strength}")
        else:
            st.info("Nenhum ponto forte identificado")

    with col_right:
        st.subheader("Pontos Fracos")

        if invest_score.weaknesses:
            for weakness in invest_score.weaknesses:
                st.warning(f"⚠ {weakness}")
        else:
            st.info("Nenhum ponto fraco identificado")

    # Sugestões de melhoria
    if invest_score.suggestions:
        st.markdown("---")
        st.subheader("Sugestoes de Melhoria")

        for i, suggestion in enumerate(invest_score.suggestions, 1):
            st.info(f"**{i}.** {suggestion}")

    # Exportar resultados
    st.markdown("---")

    col_export1, col_export2 = st.columns(2)

    with col_export1:
        # Exportar como JSON
        json_data = invest_score.to_json()
        st.download_button(
            label="Baixar Relatorio (JSON)",
            data=json_data,
            file_name="invest_validation.json",
            mime="application/json",
            use_container_width=True
        )

    with col_export2:
        # Gerar relatório texto
        report_text = _generate_text_report(invest_score)
        st.download_button(
            label="Baixar Relatorio (TXT)",
            data=report_text,
            file_name="invest_validation.txt",
            mime="text/plain",
            use_container_width=True
        )


def _generate_text_report(invest_score: InvestScore) -> str:
    """
    Gera relatório em texto da validação.

    Args:
        invest_score: Scores INVEST

    Returns:
        Relatório em texto
    """
    lines = []

    lines.append("=" * 60)
    lines.append("RELATORIO DE VALIDACAO INVEST")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"Score Geral: {invest_score.overall}%")
    lines.append(f"Status: {invest_score.get_status_label()}")
    lines.append("")

    lines.append("-" * 60)
    lines.append("SCORES POR CRITERIO")
    lines.append("-" * 60)
    lines.append("")

    criteria = [
        ('independent', 'Independent'),
        ('negotiable', 'Negotiable'),
        ('valuable', 'Valuable'),
        ('estimable', 'Estimable'),
        ('small', 'Small'),
        ('testable', 'Testable')
    ]

    for attr, label in criteria:
        score = getattr(invest_score, attr)
        justification = invest_score.justifications.get(attr, "")

        lines.append(f"{label}: {score}%")
        lines.append(f"  Justificativa: {justification}")
        lines.append("")

    if invest_score.strengths:
        lines.append("-" * 60)
        lines.append("PONTOS FORTES")
        lines.append("-" * 60)
        for strength in invest_score.strengths:
            lines.append(f"  - {strength}")
        lines.append("")

    if invest_score.weaknesses:
        lines.append("-" * 60)
        lines.append("PONTOS FRACOS")
        lines.append("-" * 60)
        for weakness in invest_score.weaknesses:
            lines.append(f"  - {weakness}")
        lines.append("")

    if invest_score.suggestions:
        lines.append("-" * 60)
        lines.append("SUGESTOES DE MELHORIA")
        lines.append("-" * 60)
        for i, suggestion in enumerate(invest_score.suggestions, 1):
            lines.append(f"  {i}. {suggestion}")
        lines.append("")

    lines.append("=" * 60)

    return "\n".join(lines)
