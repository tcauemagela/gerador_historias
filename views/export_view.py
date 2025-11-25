"""
View para exportação de histórias.
"""

import streamlit as st
from datetime import datetime
from models.session_storage import SessionStorage
from exporters import TextExporter, MarkdownExporter, JSONExporter, ExcelExporter, ZipExporter
from utils.helpers import sanitize_filename


def render_export_options():
    """Renderiza opções de exportação"""
    st.header("💾 Exportar Historias")

    stories = SessionStorage.get_all_stories()

    if not stories:
        st.info("Nenhuma historia para exportar. Crie historias primeiro!")
        return

    st.write(f"**{len(stories)} historia(s) disponivel(is) para exportacao**")
    st.markdown("---")

    # Exportação individual ou em lote
    tab1, tab2 = st.tabs(["Exportacao Individual", "Exportacao em Lote"])

    with tab1:
        render_single_export(stories)

    with tab2:
        render_batch_export(stories)


def render_single_export(stories):
    """Exportação individual"""
    st.subheader("Exportar Historia Individual")

    # Seletor de história
    story_options = {f"{s['titulo']} (ID: {s['id'][:8]})": s for s in stories}
    selected_title = st.selectbox("Selecione a historia:", list(story_options.keys()))

    if selected_title:
        story = story_options[selected_title]
        st.markdown("---")

        # Preparar nome base
        base_name = sanitize_filename(story['titulo'])
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        col1, col2, col3 = st.columns(3)

        with col1:
            txt_exporter = TextExporter()
            file_bytes = txt_exporter.export([story])
            filename = txt_exporter.get_filename(base_name, timestamp)

            st.download_button(
                label="📄 TXT",
                data=file_bytes,
                file_name=filename,
                mime=txt_exporter.get_mime_type(),
                key=f"txt_{story['id']}",
                use_container_width=True
            )
            st.caption(f"{len(file_bytes)} bytes")

        with col2:
            md_exporter = MarkdownExporter()
            file_bytes = md_exporter.export([story])
            filename = md_exporter.get_filename(base_name, timestamp)

            st.download_button(
                label="📝 MD",
                data=file_bytes,
                file_name=filename,
                mime=md_exporter.get_mime_type(),
                key=f"md_{story['id']}",
                use_container_width=True
            )
            st.caption(f"{len(file_bytes)} bytes")

        with col3:
            json_exporter = JSONExporter()
            file_bytes = json_exporter.export([story])
            filename = json_exporter.get_filename(base_name, timestamp)

            st.download_button(
                label="📋 JSON",
                data=file_bytes,
                file_name=filename,
                mime=json_exporter.get_mime_type(),
                key=f"json_{story['id']}",
                use_container_width=True
            )
            st.caption(f"{len(file_bytes)} bytes")


def render_batch_export(stories):
    """Exportação em lote"""
    st.subheader("Exportar Multiplas Historias")

    # Seleção múltipla
    if 'selected_stories' not in st.session_state:
        st.session_state.selected_stories = []

    st.write("Selecione as historias para exportar:")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Selecionar Todas", use_container_width=True):
            st.session_state.selected_stories = [s['id'] for s in stories]
            st.rerun()
    with col_btn2:
        if st.button("Limpar Selecao", use_container_width=True):
            st.session_state.selected_stories = []
            st.rerun()

    # Checkboxes
    for story in stories:
        is_selected = story['id'] in st.session_state.selected_stories

        if st.checkbox(
            f"{story['titulo']} (Complexidade: {story['complexidade']})",
            value=is_selected,
            key=f"select_{story['id']}"
        ):
            if story['id'] not in st.session_state.selected_stories:
                st.session_state.selected_stories.append(story['id'])
        else:
            if story['id'] in st.session_state.selected_stories:
                st.session_state.selected_stories.remove(story['id'])

    selected_count = len(st.session_state.selected_stories)

    if selected_count == 0:
        st.warning("Nenhuma historia selecionada")
        return

    st.success(f"{selected_count} historia(s) selecionada(s)")
    st.markdown("---")

    # Filtrar histórias selecionadas
    selected_stories = [s for s in stories if s['id'] in st.session_state.selected_stories]

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    col1, col2, col3 = st.columns(3)

    with col1:
        try:
            zip_exporter = ZipExporter()
            file_bytes = zip_exporter.export(selected_stories)
            filename = zip_exporter.get_filename("historias", timestamp)

            st.download_button(
                label="📦 ZIP",
                data=file_bytes,
                file_name=filename,
                mime=zip_exporter.get_mime_type(),
                use_container_width=True
            )
            st.caption(f"{len(file_bytes) / 1024:.1f} KB")
        except Exception as e:
            st.error(f"Erro ZIP: {str(e)}")

    with col2:
        try:
            with st.spinner("Gerando Excel..."):
                excel_exporter = ExcelExporter()
                file_bytes = excel_exporter.export(selected_stories)
                filename = excel_exporter.get_filename("historias", timestamp)

            st.download_button(
                label="📊 Excel",
                data=file_bytes,
                file_name=filename,
                mime=excel_exporter.get_mime_type(),
                use_container_width=True
            )
            st.caption(f"{len(file_bytes) / 1024:.1f} KB")
        except Exception as e:
            st.error(f"Erro Excel: {str(e)}")

    with col3:
        json_exporter = JSONExporter()
        file_bytes = json_exporter.export(selected_stories)
        filename = json_exporter.get_filename("historias", timestamp)

        st.download_button(
            label="📋 JSON Array",
            data=file_bytes,
            file_name=filename,
            mime=json_exporter.get_mime_type(),
            use_container_width=True
        )
        st.caption(f"{len(file_bytes) / 1024:.1f} KB")
