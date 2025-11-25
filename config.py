"""
Módulo de configuração central do sistema.
Responsável por gerenciar API keys e configurações globais.
Segue Single Responsibility Principle (SOLID).
"""

import os
import streamlit as st
from dotenv import load_dotenv


def get_api_key() -> str:
    """
    Obtém API key da Anthropic com fallback automático.

    Prioridade de busca:
    1. Streamlit Secrets (produção/cloud)
    2. Arquivo .env (desenvolvimento local)
    3. Erro se nenhuma configuração encontrada

    Returns:
        str: API key da Anthropic

    Raises:
        SystemExit: Se API key não for encontrada em nenhuma fonte
    """
    # Tenta carregar de Streamlit Secrets (produção)
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        if api_key and api_key.strip():
            return api_key.strip()
    except (KeyError, FileNotFoundError):
        pass

    # Tenta carregar de .env (desenvolvimento local)
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if api_key and api_key.strip():
        return api_key.strip()

    # Nenhuma configuração encontrada - exibir erro e parar
    st.error("❌ API Key da Anthropic não encontrada!")
    st.info("""
    **Como configurar a API Key:**

    **Opção 1 - Desenvolvimento Local:**
    1. Crie um arquivo `.env` na raiz do projeto
    2. Adicione: `ANTHROPIC_API_KEY=sua-chave-aqui`
    3. Obtenha sua chave em: https://console.anthropic.com/

    **Opção 2 - Streamlit Cloud:**
    1. Vá em Settings > Secrets
    2. Adicione: `ANTHROPIC_API_KEY = "sua-chave-aqui"`
    """)
    st.stop()


# Configurações do modelo Claude
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 4000
CLAUDE_TIMEOUT = 30
CLAUDE_MAX_RETRIES = 2

# Configurações da aplicação
APP_TITLE = "Gerador de Histórias"
APP_ICON = "📝"
APP_LAYOUT = "wide"
APP_AUTHOR = "Cauê Magela [AI-SPEC/CS]"
