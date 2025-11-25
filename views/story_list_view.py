"""
View para listagem de histórias da sessão.
"""

import streamlit as st
from models.session_storage import SessionStorage
from utils.helpers import format_datetime_display


def render_story_list():
    """Renderiza lista de histórias da sessão"""
    st.header("📚 Minhas Historias")

    stories = SessionStorage.get_all_stories()

    if not stories:
        st.info("Nenhuma historia criada ainda. Crie sua primeira historia na aba 'Criar Historia'!")
        return

    st.write(f"**{len(stories)} historia(s) encontrada(s)**")
    st.markdown("---")

    # Listar histórias
    for i, story in enumerate(stories, 1):
        with st.expander(f"📋 {story['titulo']}", expanded=False):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.caption(f"Criado em: {format_datetime_display(story['created_at'])}")
                st.write(f"**Complexidade:** {story['complexidade']} pontos")

            with col2:
                if st.button("🗑️ Deletar", key=f"del_{story['id']}", use_container_width=True):
                    if SessionStorage.delete_story(story['id']):
                        st.success("Historia deletada!")
                        st.rerun()

            # Preview
            st.markdown("**Preview:**")
            preview = story['historia_gerada'][:300] + "..."
            st.text(preview)

            st.markdown("---")
            st.write(f"**Regras:** {len(story.get('regras_negocio', []))}")
            st.write(f"**APIs:** {len(story.get('apis_servicos', []))}")
            st.write(f"**Criterios:** {len(story.get('criterios_aceitacao', []))}")
