"""
View responsável por renderizar o formulário de entrada.
Implementa campos com múltiplas entradas dinâmicas.
Segue Single Responsibility Principle.
"""

import streamlit as st
from typing import Dict, Any
from models.validation import validate_form


def initialize_session_state():
    """
    Inicializa o session_state com valores padrão.
    Deve ser chamado antes de renderizar o formulário.
    """
    if 'titulo' not in st.session_state:
        st.session_state.titulo = ""

    if 'regras_negocio' not in st.session_state:
        st.session_state.regras_negocio = [""]

    if 'apis_servicos' not in st.session_state:
        st.session_state.apis_servicos = [""]

    if 'objetivos' not in st.session_state:
        st.session_state.objetivos = [""]

    if 'complexidade' not in st.session_state:
        st.session_state.complexidade = 5

    if 'criterios_aceitacao' not in st.session_state:
        st.session_state.criterios_aceitacao = [""]

    if 'validation_errors' not in st.session_state:
        st.session_state.validation_errors = []

    # Campos específicos para API
    if 'is_api' not in st.session_state:
        st.session_state.is_api = False

    if 'api_endpoint' not in st.session_state:
        st.session_state.api_endpoint = ""

    if 'api_parametros' not in st.session_state:
        st.session_state.api_parametros = ""

    if 'api_formato_resposta' not in st.session_state:
        st.session_state.api_formato_resposta = ""

    if 'api_tratamento_erros' not in st.session_state:
        st.session_state.api_tratamento_erros = ""

    if 'api_documentacao' not in st.session_state:
        st.session_state.api_documentacao = ""

    # Subseções de Objetivos
    if 'objetivo_como' not in st.session_state:
        st.session_state.objetivo_como = ""

    if 'objetivo_quero' not in st.session_state:
        st.session_state.objetivo_quero = ""

    if 'objetivo_para_que' not in st.session_state:
        st.session_state.objetivo_para_que = ""

    if 'objetivo_listagem_medicos' not in st.session_state:
        st.session_state.objetivo_listagem_medicos = ""

    if 'objetivo_filtros_busca' not in st.session_state:
        st.session_state.objetivo_filtros_busca = ""

    if 'objetivo_exibicao_horarios' not in st.session_state:
        st.session_state.objetivo_exibicao_horarios = ""

    if 'objetivo_agendamento' not in st.session_state:
        st.session_state.objetivo_agendamento = ""


def render_multiple_text_areas(
    label: str,
    key_prefix: str,
    state_key: str,
    placeholder: str = ""
):
    """
    Renderiza múltiplas text_areas com botões de adicionar/remover.

    Args:
        label: Label do campo
        key_prefix: Prefixo para keys únicas
        state_key: Chave no session_state
        placeholder: Texto placeholder
    """
    # Label com caixa de destaque
    st.markdown(f"""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">{label}</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)

    items = st.session_state[state_key]

    for i, item in enumerate(items):
        col1, col2 = st.columns([6, 1])

        with col1:
            new_value = st.text_area(
                f"{label} {i + 1}",
                value=item,
                key=f"{key_prefix}_{i}",
                placeholder=placeholder,
                label_visibility="collapsed",
                height=100
            )
            st.session_state[state_key][i] = new_value

        with col2:
            # Botão remover (só aparece se houver mais de 1 item)
            if len(items) > 1:
                if st.button("➖", key=f"remove_{key_prefix}_{i}", help="Remover"):
                    st.session_state[state_key].pop(i)
                    st.rerun()

    # Botão adicionar
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        if st.button(f"➕ Adicionar {label}", key=f"add_{key_prefix}"):
            st.session_state[state_key].append("")
            st.rerun()

    st.markdown("---")


def render_form() -> Dict[str, Any]:
    """
    Renderiza o formulário completo de entrada.

    Returns:
        Dict com os dados do formulário ou None se não submetido
    """
    initialize_session_state()

    # Título principal com destaque (sem emoji)
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        ">
            <h2 style="color: white; margin: 0; font-weight: 700;">Criar Nova História</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Campo 1: Título (único, sem múltiplas entradas)
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Título da Tarefa</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.titulo = st.text_input(
        "Título",
        value=st.session_state.titulo,
        max_chars=100,
        placeholder="Ex: DU Benefícios - Desenvolver API Districts/Bairros",
        help="Título técnico da tarefa (máx. 100 caracteres, sem caracteres especiais !@#$%^&*())",
        label_visibility="collapsed"
    )
    st.markdown("---")

    # Campo 2: Regras de Negócio (múltiplas entradas)
    render_multiple_text_areas(
        label="Regras de Negócio",
        key_prefix="regra",
        state_key="regras_negocio",
        placeholder="Descreva uma regra de negócio..."
    )

    # Campo 3: APIs/Serviços (múltiplas entradas)
    render_multiple_text_areas(
        label="APIs/Serviços Necessários",
        key_prefix="api",
        state_key="apis_servicos",
        placeholder="Ex: API do Google OAuth 2.0, Firebase Authentication..."
    )

    # Campo 4: Subseções de objetivos (direto, sem header principal)

    # Subseção: Como
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Como:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_como = st.text_area(
        "Como",
        value=st.session_state.objetivo_como,
        placeholder="Descreva o contexto ou papel do usuário...",
        label_visibility="collapsed",
        height=80,
        key="obj_como"
    )

    # Subseção: Quero
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Quero:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_quero = st.text_area(
        "Quero",
        value=st.session_state.objetivo_quero,
        placeholder="Descreva o que o usuário deseja fazer...",
        label_visibility="collapsed",
        height=80,
        key="obj_quero"
    )

    # Subseção: Para que
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Para que:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_para_que = st.text_area(
        "Para que",
        value=st.session_state.objetivo_para_que,
        placeholder="Descreva o benefício ou objetivo final...",
        label_visibility="collapsed",
        height=80,
        key="obj_para_que"
    )

    # Subseção: Listagem de Médicos
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Listagem de Médicos:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_listagem_medicos = st.text_area(
        "Listagem de Médicos",
        value=st.session_state.objetivo_listagem_medicos,
        placeholder="Descreva requisitos para listagem de médicos...",
        label_visibility="collapsed",
        height=80,
        key="obj_listagem"
    )

    # Subseção: Filtros de Busca
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Filtros de Busca:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_filtros_busca = st.text_area(
        "Filtros de Busca",
        value=st.session_state.objetivo_filtros_busca,
        placeholder="Descreva filtros de busca necessários...",
        label_visibility="collapsed",
        height=80,
        key="obj_filtros"
    )

    # Subseção: Exibição de Horários
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Exibição de Horários:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_exibicao_horarios = st.text_area(
        "Exibição de Horários",
        value=st.session_state.objetivo_exibicao_horarios,
        placeholder="Descreva como os horários devem ser exibidos...",
        label_visibility="collapsed",
        height=80,
        key="obj_horarios"
    )

    # Subseção: Agendamento
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Agendamento:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_agendamento = st.text_area(
        "Agendamento",
        value=st.session_state.objetivo_agendamento,
        placeholder="Descreva requisitos para agendamento...",
        label_visibility="collapsed",
        height=80,
        key="obj_agendamento"
    )
    st.markdown("---")

    # Campo 5: Complexidade (único)
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Complexidade Estimada (pontos)</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.complexidade = st.number_input(
        "Complexidade",
        min_value=1,
        max_value=21,
        value=st.session_state.complexidade,
        step=1,
        help="Defina a complexidade da tarefa (1 a 21 pontos)",
        label_visibility="collapsed"
    )
    st.caption("Defina a complexidade da tarefa (1 a 21 pontos)")
    st.markdown("---")

    # Campo 6: Critérios de Aceitação (múltiplas entradas)
    render_multiple_text_areas(
        label="Critérios de Aceitação",
        key_prefix="criterio",
        state_key="criterios_aceitacao",
        placeholder="Descreva um critério de aceitação..."
    )

    # Pergunta sobre API (dentro dos critérios de aceitação)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Esta tarefa envolve desenvolvimento de API?</strong>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.is_api = st.checkbox(
        "Sim, esta tarefa envolve desenvolvimento de API",
        value=st.session_state.is_api,
        key="is_api_checkbox"
    )

    # Se for API, mostrar campos específicos
    if st.session_state.is_api:
        st.markdown("<br>", unsafe_allow_html=True)

        # Endpoint da API
        st.markdown("""
            <div style="
                background-color: rgba(139, 92, 246, 0.08);
                border-left: 3px solid #8B5CF6;
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                margin-bottom: 0.5rem;
            ">
                <strong style="color: #E0E0E0; font-size: 0.95rem;">Endpoint da API</strong>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.api_endpoint = st.text_input(
            "Endpoint",
            value=st.session_state.api_endpoint,
            placeholder="Ex: /api/v1/districts",
            label_visibility="collapsed",
            key="api_endpoint_input"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Parâmetros de Consulta
        st.markdown("""
            <div style="
                background-color: rgba(139, 92, 246, 0.08);
                border-left: 3px solid #8B5CF6;
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                margin-bottom: 0.5rem;
            ">
                <strong style="color: #E0E0E0; font-size: 0.95rem;">Parâmetros de Consulta</strong>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.api_parametros = st.text_area(
            "Parâmetros",
            value=st.session_state.api_parametros,
            placeholder="Ex: city_id (obrigatório), limit (opcional), offset (opcional)",
            label_visibility="collapsed",
            height=100,
            key="api_parametros_input"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Formato da Resposta
        st.markdown("""
            <div style="
                background-color: rgba(139, 92, 246, 0.08);
                border-left: 3px solid #8B5CF6;
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                margin-bottom: 0.5rem;
            ">
                <strong style="color: #E0E0E0; font-size: 0.95rem;">Formato da Resposta</strong>
            </div>
        """, unsafe_allow_html=True)
        st.caption("A resposta da API deve ser retornada no formato JSON, contendo:")
        st.session_state.api_formato_resposta = st.text_area(
            "Formato Resposta",
            value=st.session_state.api_formato_resposta,
            placeholder='Ex: {\n  "districts": [...],\n  "total": 10,\n  "page": 1\n}',
            label_visibility="collapsed",
            height=150,
            key="api_formato_input"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Tratamento de Erros
        st.markdown("""
            <div style="
                background-color: rgba(139, 92, 246, 0.08);
                border-left: 3px solid #8B5CF6;
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                margin-bottom: 0.5rem;
            ">
                <strong style="color: #E0E0E0; font-size: 0.95rem;">Tratamento de Erros</strong>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.api_tratamento_erros = st.text_area(
            "Tratamento Erros",
            value=st.session_state.api_tratamento_erros,
            placeholder="Ex: 400 - Parâmetros inválidos\n404 - Recurso não encontrado\n500 - Erro interno do servidor",
            label_visibility="collapsed",
            height=100,
            key="api_erros_input"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Documentação
        st.markdown("""
            <div style="
                background-color: rgba(139, 92, 246, 0.08);
                border-left: 3px solid #8B5CF6;
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                margin-bottom: 0.5rem;
            ">
                <strong style="color: #E0E0E0; font-size: 0.95rem;">Documentação</strong>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.api_documentacao = st.text_area(
            "Documentação",
            value=st.session_state.api_documentacao,
            placeholder="Descreva requisitos de documentação (Swagger, OpenAPI, etc.)",
            label_visibility="collapsed",
            height=100,
            key="api_doc_input"
        )

    st.markdown("---")

    # Exibir erros de validação (se houver)
    if st.session_state.validation_errors:
        st.error("**Erros de validação:**")
        for error in st.session_state.validation_errors:
            st.markdown(f"- {error}")
        st.markdown("---")

    # Botão de submissão
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        submit_button = st.button(
            "✨ Gerar História",
            type="primary",
            use_container_width=True
        )

    # Processar submissão
    if submit_button:
        # Validar formulário
        is_valid, errors = validate_form(
            titulo=st.session_state.titulo,
            regras_negocio=st.session_state.regras_negocio,
            apis_servicos=st.session_state.apis_servicos,
            objetivos=st.session_state.objetivos,
            complexidade=st.session_state.complexidade,
            criterios_aceitacao=st.session_state.criterios_aceitacao
        )

        if not is_valid:
            st.session_state.validation_errors = errors
            st.rerun()
        else:
            st.session_state.validation_errors = []

            # Retornar dados limpos
            objetivos_dict = {
                "como": st.session_state.objetivo_como.strip(),
                "quero": st.session_state.objetivo_quero.strip(),
                "para_que": st.session_state.objetivo_para_que.strip(),
                "listagem_medicos": st.session_state.objetivo_listagem_medicos.strip(),
                "filtros_busca": st.session_state.objetivo_filtros_busca.strip(),
                "exibicao_horarios": st.session_state.objetivo_exibicao_horarios.strip(),
                "agendamento": st.session_state.objetivo_agendamento.strip()
            }

            form_data = {
                "titulo": st.session_state.titulo.strip(),
                "regras_negocio": [r.strip() for r in st.session_state.regras_negocio if r.strip()],
                "apis_servicos": [a.strip() for a in st.session_state.apis_servicos if a.strip()],
                "objetivos": objetivos_dict,
                "complexidade": st.session_state.complexidade,
                "criterios_aceitacao": [c.strip() for c in st.session_state.criterios_aceitacao if c.strip()],
                "is_api": st.session_state.is_api
            }

            # Adicionar dados da API se aplicável
            if st.session_state.is_api:
                form_data["api_specs"] = {
                    "endpoint": st.session_state.api_endpoint.strip(),
                    "parametros": st.session_state.api_parametros.strip(),
                    "formato_resposta": st.session_state.api_formato_resposta.strip(),
                    "tratamento_erros": st.session_state.api_tratamento_erros.strip(),
                    "documentacao": st.session_state.api_documentacao.strip()
                }

            return form_data

    return None


def reset_form():
    """
    Reseta o formulário para os valores iniciais.
    Útil após gerar uma história com sucesso.
    """
    st.session_state.titulo = ""
    st.session_state.regras_negocio = [""]
    st.session_state.apis_servicos = [""]
    st.session_state.complexidade = 5
    st.session_state.criterios_aceitacao = [""]
    st.session_state.validation_errors = []

    # Resetar campos de Objetivos
    st.session_state.objetivo_como = ""
    st.session_state.objetivo_quero = ""
    st.session_state.objetivo_para_que = ""
    st.session_state.objetivo_listagem_medicos = ""
    st.session_state.objetivo_filtros_busca = ""
    st.session_state.objetivo_exibicao_horarios = ""
    st.session_state.objetivo_agendamento = ""

    # Resetar campos da API
    st.session_state.is_api = False
    st.session_state.api_endpoint = ""
    st.session_state.api_parametros = ""
    st.session_state.api_formato_resposta = ""
    st.session_state.api_tratamento_erros = ""
    st.session_state.api_documentacao = ""
