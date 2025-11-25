"""
View responsável por exibir a história gerada e opções de exportação.
Segue Single Responsibility Principle.
"""

import streamlit as st
import json
from datetime import datetime
from models.story import Story


def render_story(story: Story):
    """
    Renderiza a história gerada com opções de visualização e exportação.

    Args:
        story: Objeto Story com a história gerada
    """
    st.success("✅ História gerada com sucesso!")
    st.markdown("---")

    # Cabeçalho
    st.header("História Gerada ✨")

    # Container para a história
    with st.container():
        # Renderiza o Markdown da história
        st.markdown(story.historia_gerada, unsafe_allow_html=True)

    st.markdown("---")

    # Seção de exportação
    st.subheader("📥 Exportar História")

    # Gerar nome de arquivo baseado no título e timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    titulo_simplificado = _simplify_filename(story.titulo)
    base_filename = f"{titulo_simplificado}_{timestamp}"

    # Layout de botões de exportação
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Exportar como TXT
        txt_content = story.to_text_export()
        st.download_button(
            label="📄 TXT",
            data=txt_content,
            file_name=f"{base_filename}.txt",
            mime="text/plain",
            use_container_width=True,
            help="Baixar como texto simples"
        )

    with col2:
        # Exportar como MD
        md_content = story.to_markdown_export()
        st.download_button(
            label="📝 Markdown",
            data=md_content,
            file_name=f"{base_filename}.md",
            mime="text/markdown",
            use_container_width=True,
            help="Baixar como Markdown"
        )

    with col3:
        # Exportar como JSON
        json_content = json.dumps(
            story.to_json_export(),
            ensure_ascii=False,
            indent=2
        )
        st.download_button(
            label="📊 JSON",
            data=json_content,
            file_name=f"{base_filename}.json",
            mime="application/json",
            use_container_width=True,
            help="Baixar como JSON estruturado"
        )

    with col4:
        # Botão para copiar
        if st.button("📋 Copiar", use_container_width=True, help="Copiar Markdown"):
            _show_copy_modal(story.historia_gerada)

    st.markdown("---")

    # Botão para criar nova história
    if st.button("➕ Criar Nova História", type="primary", use_container_width=False):
        # Limpar história atual do session state
        if 'current_story' in st.session_state:
            del st.session_state.current_story
        st.rerun()


def _simplify_filename(titulo: str) -> str:
    """
    Simplifica o título para usar como nome de arquivo.
    Remove caracteres especiais e substitui espaços por underscores.

    Args:
        titulo: Título original

    Returns:
        Título simplificado para filename
    """
    import re

    # Remove caracteres especiais, mantém apenas alfanuméricos e espaços
    titulo_limpo = re.sub(r'[^\w\s-]', '', titulo)

    # Substitui espaços por underscores
    titulo_limpo = re.sub(r'\s+', '_', titulo_limpo)

    # Converte para lowercase e limita tamanho
    titulo_limpo = titulo_limpo.lower()[:50]

    return titulo_limpo


def _show_copy_modal(content: str):
    """
    Exibe modal com conteúdo para copiar.

    Args:
        content: Conteúdo a ser copiado
    """
    st.info("📋 **Copie o conteúdo abaixo:**")

    # Usa st.code para melhor visualização e facilidade de cópia
    st.code(content, language="markdown")

    st.caption("💡 Dica: Clique no ícone de copiar no canto superior direito do código")


def show_loading(message: str = "🤖 Gerando história com IA..."):
    """
    Exibe spinner de loading durante a geração.

    Args:
        message: Mensagem a exibir durante loading
    """
    with st.spinner(message):
        st.info("⏳ Isso pode levar até 30 segundos...")


def show_error(error_message: str, error_type: str = "generic"):
    """
    Exibe mensagem de erro formatada com base no tipo.

    Args:
        error_message: Mensagem de erro técnica
        error_type: Tipo do erro (timeout, rate_limit, connection, generic)
    """
    st.error(f"❌ **Erro ao gerar história**")

    if error_type == "timeout":
        st.warning("⏱️ **Tempo esgotado:** A IA demorou muito para responder.")
        st.info("💡 **Sugestão:** Tente novamente ou reduza a complexidade.")

    elif error_type == "rate_limit":
        st.warning("🚫 **Limite atingido:** Muitas requisições em pouco tempo.")
        st.info("💡 **Sugestão:** Aguarde alguns minutos antes de tentar novamente.")

    elif error_type == "connection":
        st.warning("🌐 **Erro de conexão:** Não foi possível conectar à API.")
        st.info("💡 **Sugestão:** Verifique sua conexão com a internet.")

    elif error_type == "api_key":
        st.warning("🔑 **API Key inválida:** A chave de API está incorreta ou expirada.")
        st.info("💡 **Sugestão:** Verifique a configuração da API key no arquivo .env ou Streamlit Secrets.")

    else:
        # Se for erro genérico com detalhes (formato "generic:detalhes")
        if error_type.startswith("generic:"):
            error_details = error_type.replace("generic:", "")
            st.error("**Erro Desconhecido:** Ocorreu um erro inesperado ao gerar a história.")

            # Mostrar detalhes em um expander para não poluir a tela
            with st.expander("🔍 Detalhes Técnicos (Debug)", expanded=True):
                st.code(error_details, language="python")

            st.info("💡 **Ação sugerida:** Copie os detalhes acima e compartilhe com o desenvolvedor para análise.")
        else:
            st.warning(f"**Detalhes técnicos:** {error_message}")

    # Sempre oferecer botão de retry
    if st.button("🔄 Tentar Novamente", type="secondary"):
        st.rerun()
