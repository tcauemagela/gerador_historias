"""
Service de integração com Claude API (Anthropic).
Responsável por comunicação com IA e geração de histórias.
Segue Single Responsibility Principle e Dependency Inversion Principle.
"""

from typing import List, Dict, Any
from anthropic import Anthropic, APITimeoutError, APIConnectionError, RateLimitError
import config


class AIService:
    """
    Service responsável pela comunicação com Claude API.
    Gera histórias de usuário técnicas usando IA.
    """

    def __init__(self, api_key: str):
        """
        Inicializa o service com configurações da API.

        Args:
            api_key: Chave de API da Anthropic
        """
        self.client = Anthropic(api_key=api_key)
        self.model = config.CLAUDE_MODEL
        self.max_tokens = config.CLAUDE_MAX_TOKENS
        self.timeout = config.CLAUDE_TIMEOUT

    def generate_story(
        self,
        titulo: str,
        regras_negocio: List[str],
        apis_servicos: List[str],
        objetivos: Dict[str, Any],
        complexidade: int,
        criterios_aceitacao: List[str]
    ) -> str:
        """
        Gera história técnica usando Claude API.

        Args:
            titulo: Título da história
            regras_negocio: Lista de regras de negócio
            apis_servicos: Lista de APIs/serviços necessários
            objetivos: Dicionário de objetivos com subseções
            complexidade: Pontos de complexidade (1-21)
            criterios_aceitacao: Lista de critérios de aceitação

        Returns:
            História gerada em formato Markdown

        Raises:
            APITimeoutError: Se a API demorar mais que o timeout
            RateLimitError: Se atingir limite de requisições
            APIConnectionError: Se houver erro de conexão
            Exception: Para outros erros da API
        """
        prompt = self._build_prompt(
            titulo=titulo,
            regras_negocio=regras_negocio,
            apis_servicos=apis_servicos,
            objetivos=objetivos,
            complexidade=complexidade,
            criterios_aceitacao=criterios_aceitacao
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                timeout=self.timeout,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extrai texto da resposta
            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise Exception("Resposta vazia da API")

        except APITimeoutError:
            raise APITimeoutError(
                "Tempo esgotado ao aguardar resposta da IA. Tente novamente."
            )
        except RateLimitError:
            raise RateLimitError(
                "Limite de requisições atingido. Aguarde alguns minutos."
            )
        except APIConnectionError:
            raise APIConnectionError(
                "Erro de conexão com a API. Verifique sua internet."
            )
        except Exception as e:
            raise Exception(f"Erro ao gerar história: {str(e)}")

    def _build_prompt(
        self,
        titulo: str,
        regras_negocio: List[str],
        apis_servicos: List[str],
        objetivos: Dict[str, Any],
        complexidade: int,
        criterios_aceitacao: List[str]
    ) -> str:
        """
        Constrói prompt estruturado profissional para Claude API.
        Baseado em padrões de Product Owner sênior.

        Args:
            titulo: Título da história
            regras_negocio: Lista de regras
            apis_servicos: Lista de APIs
            objetivos: Dicionário de objetivos com subseções
            complexidade: Pontos de complexidade
            criterios_aceitacao: Lista de critérios

        Returns:
            Prompt formatado em XML
        """
        # Formata listas em items
        regras_formatadas = "\n".join(f"- {regra}" for regra in regras_negocio)
        apis_formatadas = "\n".join(f"- {api}" for api in apis_servicos)

        # Converte dicionário de objetivos em lista formatada
        objetivos_lista = []

        # Garantir que objetivos seja um dicionário
        if not isinstance(objetivos, dict):
            objetivos = {}

        labels = {
            "como": "Como",
            "quero": "Quero",
            "para_que": "Para que",
            "listagem_medicos": "Listagem de Médicos",
            "filtros_busca": "Filtros de Busca",
            "exibicao_horarios": "Exibição de Horários",
            "agendamento": "Agendamento"
        }

        for key, value in objetivos.items():
            if value and isinstance(value, str) and value.strip():
                label = labels.get(key, key.replace("_", " ").title())
                objetivos_lista.append(f"{label}: {value.strip()}")

        objetivos_formatados = "\n".join(f"- {obj}" for obj in objetivos_lista) if objetivos_lista else "- Não especificado"
        criterios_formatados = "\n".join(f"- {crit}" for crit in criterios_aceitacao)

        prompt = f"""
<task>
Você é um Product Owner sênior especializado em metodologias ágeis e documentação técnica de alta qualidade.
Sua missão é gerar uma história de usuário COMPLETA, TÉCNICA e PROFISSIONAL seguindo rigorosamente
os padrões estabelecidos.
</task>

<critical_rules>
REGRAS ABSOLUTAS (NUNCA VIOLAR):

1. NUNCA ADICIONAR EMOJIS NO CONTEÚDO DA HISTÓRIA
   - Títulos e seções devem ser puramente textuais
   - Sem emojis decorativos em nenhuma parte
   - Formato corporativo/técnico profissional

2. NUNCA INVENTAR INFORMAÇÕES
   - Use APENAS dados fornecidos pelo usuário
   - Não criar APIs, endpoints ou tecnologias não mencionadas
   - Não adicionar regras de negócio não fornecidas
   - Se algo não foi informado, não especular
   - Mantenha-se fiel aos inputs fornecidos

3. SER OBJETIVA E DIRETA
   - Evitar floreios ou descrições elaboradas
   - Foco em clareza e precisão técnica
   - Tom profissional e direto ao ponto
   - Sem criatividade excessiva

4. FORMATO TÉCNICO
   - Esta é uma especificação para desenvolvedores
   - Linguagem técnica precisa
   - Sem formato "Como usuário, eu quero..."
   - Formato direto: "Implementar X", "Integrar Y"
</critical_rules>

<input_data>
<titulo>{titulo}</titulo>

<regras_negocio>
{regras_formatadas}
</regras_negocio>

<apis_servicos>
{apis_formatadas}
</apis_servicos>

<objetivos>
{objetivos_formatados}
</objetivos>

<complexidade>{complexidade}</complexidade>

<criterios_aceitacao>
{criterios_formatados}
</criterios_aceitacao>
</input_data>

<mandatory_structure>
SUA HISTÓRIA DEVE CONTER EXATAMENTE ESTAS SEÇÕES (SEM EMOJIS):

1. TÍTULO (nível ##)
   Formato: ## [Título da Tarefa]

2. CONTEXTO/PROBLEMA (nível ###)
   Formato: ### Contexto
   Conteúdo: Situação atual baseada APENAS nos dados fornecidos

3. OBJETIVO (nível ###)
   Formato: ### Objetivo
   Conteúdo: O que se pretende alcançar (baseado nos objetivos fornecidos)

4. REGRAS DE NEGÓCIO (nível ###)
   Formato: ### Regras de Negocio
   Conteúdo: TODAS as regras fornecidas (bullet points)
   IMPORTANTE: Incluir TODAS sem omitir nenhuma

5. APIS/SERVIÇOS (nível ###)
   Formato: ### APIs e Servicos Necessarios
   Conteúdo: Listar TODAS as APIs fornecidas
   Descrição: Uso técnico baseado no contexto

6. OBJETIVOS TÉCNICOS (nível ###)
   Formato: ### Objetivos Tecnicos
   Conteúdo: TODOS os objetivos fornecidos (bullet points)

7. CRITÉRIOS DE ACEITAÇÃO (nível ###)
   Formato: ### Criterios de Aceitacao
   Conteúdo: Mínimo 3 critérios

   Use formato Gherkin quando apropriado:
   ```
   CA1 - [Nome do critério]
   Dado que [condição]
   Quando [ação]
   Então [resultado esperado]
   ```

   OU bullet points técnicos:
   ```
   - Sistema deve validar X
   - Formato de saída deve ser Y
   - Performance deve ser < Z
   ```

   SEMPRE incluir:
   - Caso de sucesso
   - Caso de erro
   - Validação técnica

8. CENÁRIOS DE TESTE (nível ###)
   Formato: ### Cenarios de Teste Sugeridos
   Conteúdo: OBRIGATÓRIO mínimo 3 cenários

   1. Cenario de sucesso: [descrição objetiva]
   2. Cenario de erro/excecao: [descrição objetiva]
   3. Cenario edge case: [descrição objetiva]

9. COMPLEXIDADE (nível ###)
   Formato: ### Complexidade
   Conteúdo:
   Pontos: {complexidade}
</mandatory_structure>

<formatting_rules>
FORMATAÇÃO:

1. Use Markdown estruturado
   - ## para título principal
   - ### para seções
   - Listas com - ou números
   - Blocos de código com ```

2. NUNCA use emojis em:
   - Títulos (## ou ###)
   - Conteúdo das seções
   - Listas
   - Critérios
   - Nenhuma parte da história

3. Linguagem:
   - Técnica e profissional
   - Objetiva e direta
   - Sem adjetivos desnecessários
   - Foco em precisão

4. Estrutura:
   - Linha em branco entre seções
   - Bullet points alinhados
   - Numeração sequencial para cenários
</formatting_rules>

<quality_checklist>
ANTES DE ENTREGAR, VERIFICAR:

[ ] Nenhum emoji presente na história
[ ] Todas as 9 seções obrigatórias presentes
[ ] TODAS as regras de negócio incluídas
[ ] TODAS as APIs mencionadas detalhadas
[ ] TODOS os objetivos incluídos
[ ] TODOS os critérios fornecidos incluídos
[ ] Mínimo 3 cenários de teste
[ ] Nenhuma informação inventada
[ ] Linguagem objetiva e técnica
[ ] Formato Markdown correto
</quality_checklist>

<generation_instructions>
INSTRUÇÕES DE GERAÇÃO:

1. ANÁLISE:
   - Leia TODOS os inputs fornecidos
   - Identifique o tipo de implementação

2. CONTEXTO:
   - Infira situação atual BASEADO nos dados fornecidos
   - Não invente problemas não relacionados

3. DESCRIÇÃO:
   - Seja objetiva e direta
   - Use APENAS informações fornecidas
   - Não adicione tecnologias não mencionadas

4. CRITÉRIOS:
   - Derive dos critérios fornecidos
   - Adicione casos de erro/sucesso relacionados
   - Mantenha testável e verificável

5. FORMATAÇÃO:
   - Aplique Markdown estruturado
   - SEM emojis em nenhuma parte
   - Seções claramente separadas

6. VALIDAÇÃO FINAL:
   - Execute checklist de qualidade
   - Confirme ausência de emojis
   - Verifique que nada foi inventado
</generation_instructions>

<output_example>
EXEMPLO DE FORMATO ESPERADO (SEM EMOJIS):

## Implementar autenticacao OAuth com Google

### Contexto

Atualmente o sistema utiliza autenticacao basica com usuario e senha.
Necessidade de adicionar opcao de login social conforme especificado.

### Objetivo

Implementar fluxo de autenticacao OAuth 2.0 utilizando Google Identity Platform.

### Regras de Negocio

- Usuario deve poder iniciar login com botao dedicado
- Sistema deve redirecionar para tela de consentimento do Google
- Email do Google deve ser usado como identificador unico
- Sessao deve expirar apos periodo definido

### APIs e Servicos Necessarios

- Google OAuth 2.0 API: Autenticacao e autorizacao de usuarios
- Google Identity Platform: Gerenciamento de identidades

### Objetivos Tecnicos

- Permitir autenticacao via conta Google
- Reduzir tempo de cadastro
- Melhorar experiencia do usuario

### Criterios de Aceitacao

CA1 - Iniciar fluxo OAuth
Dado que usuario acessa tela de login
Quando clica em botao de login com Google
Então deve ser redirecionado para tela de consentimento

CA2 - Processar autorizacao
Dado que usuario autoriza acesso
Quando Google redireciona de volta
Então sistema deve processar tokens
E criar ou atualizar cadastro do usuario

CA3 - Tratar erro
Dado que usuario nega permissao
Quando retorna para aplicacao
Então sistema deve exibir mensagem de erro apropriada

### Cenarios de Teste Sugeridos

1. Cenario de sucesso: Usuario completa fluxo OAuth e e autenticado com sucesso
2. Cenario de erro: Usuario nega permissao e recebe mensagem apropriada
3. Cenario edge case: Token expira durante sessao e sistema renova automaticamente

### Complexidade

Pontos: {complexidade}
</output_example>

<final_reminder>
CRÍTICO - LEMBRE-SE:

1. SEM EMOJIS EM NENHUMA PARTE DA HISTÓRIA
2. USAR APENAS INFORMAÇÕES FORNECIDAS
3. NÃO INVENTAR NADA
4. SER OBJETIVA E DIRETA
5. INCLUIR TODAS AS SEÇÕES OBRIGATÓRIAS
6. INCLUIR TODAS AS REGRAS/APIs/OBJETIVOS/CRITÉRIOS FORNECIDOS

Retorne APENAS o Markdown da história, sem texto adicional antes ou depois.
</final_reminder>
"""

        return prompt.strip()

    # ============================================================
    # NOVOS MÉTODOS DA ETAPA 2
    # ============================================================

    def regenerate_section(
        self,
        section_name: str,
        original_story: Dict,
        form_data: Dict
    ) -> str:
        """
        Regenera apenas uma seção específica da história.
        ETAPA 2: Permite regeneração parcial mantendo contexto.

        Args:
            section_name: Nome da seção ("criterios", "testes", "arquitetura", "beneficios")
            original_story: História completa original
            form_data: Dados do formulário original

        Returns:
            Seção regenerada em Markdown

        Raises:
            Exception: Em caso de erro na API
        """
        prompt = self._build_regeneration_prompt(section_name, original_story, form_data)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                timeout=self.timeout,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise Exception("Resposta vazia da API")

        except APITimeoutError:
            raise APITimeoutError("Tempo esgotado ao regenerar seção. Tente novamente.")
        except RateLimitError:
            raise RateLimitError("Limite de requisições atingido. Aguarde alguns minutos.")
        except APIConnectionError:
            raise APIConnectionError("Erro de conexão com a API. Verifique sua internet.")
        except Exception as e:
            raise Exception(f"Erro ao regenerar seção: {str(e)}")

    def _build_regeneration_prompt(
        self,
        section_name: str,
        original_story: Dict,
        form_data: Dict
    ) -> str:
        """
        Constrói prompt para regeneração parcial.

        Args:
            section_name: Seção a regenerar
            original_story: História original
            form_data: Dados do formulário

        Returns:
            Prompt formatado
        """
        historia_completa = original_story.get('historia_gerada', '')

        section_mapping = {
            'criterios': 'Criterios de Aceitacao',
            'testes': 'Cenarios de Teste Sugeridos',
            'arquitetura': 'Estrutura Tecnica/Arquitetura',
            'beneficios': 'Beneficios'
        }

        section_label = section_mapping.get(section_name, section_name)

        prompt = f"""
<task>
Regenere APENAS a seção "{section_label}" desta história.
Mantenha todo o contexto e informações da história original.
</task>

<critical_rules>
1. NUNCA ADICIONAR EMOJIS
2. USAR APENAS INFORMAÇÕES FORNECIDAS
3. SER OBJETIVA E DIRETA
4. NÃO INVENTAR NADA
</critical_rules>

<original_story>
{historia_completa}
</original_story>

<form_data>
Título: {form_data.get('titulo', '')}
Regras de Negócio:
{chr(10).join(f"- {r}" for r in form_data.get('regras_negocio', []))}

APIs/Serviços:
{chr(10).join(f"- {a}" for a in form_data.get('apis_servicos', []))}

Objetivos:
{chr(10).join(f"- {o}" for o in form_data.get('objetivos', []))}

Complexidade: {form_data.get('complexidade', 5)}

Critérios de Aceitação:
{chr(10).join(f"- {c}" for c in form_data.get('criterios_aceitacao', []))}
</form_data>

<section_to_regenerate>
{section_label}
</section_to_regenerate>

<instructions>
1. Analise o contexto da história completa
2. Regenere APENAS a seção "{section_label}"
3. Mantenha consistência com o resto da história
4. Use mesmo nível de detalhe técnico
5. Retorne APENAS a seção em Markdown, começando com ### {section_label}
</instructions>

<output_format>
### {section_label}

[Conteúdo regenerado da seção...]
</output_format>

Retorne APENAS a seção solicitada em Markdown, sem texto adicional.
"""

        return prompt.strip()

    def validate_invest_with_ai(self, story: Dict) -> str:
        """
        Valida história com IA segundo critérios INVEST.
        ETAPA 2: Análise profunda de qualidade da história.

        Args:
            story: História completa

        Returns:
            Resposta JSON da IA com scores e justificativas

        Raises:
            Exception: Em caso de erro na API
        """
        from services.invest_service import InvestService

        invest_service = InvestService()
        prompt = invest_service.prepare_for_ai_validation(story)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                timeout=self.timeout,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise Exception("Resposta vazia da API")

        except APITimeoutError:
            raise APITimeoutError("Tempo esgotado ao validar. Tente novamente.")
        except RateLimitError:
            raise RateLimitError("Limite de requisições atingido. Aguarde alguns minutos.")
        except APIConnectionError:
            raise APIConnectionError("Erro de conexão com a API. Verifique sua internet.")
        except Exception as e:
            raise Exception(f"Erro ao validar história: {str(e)}")

    def analyze_and_suggest(self, story: Dict) -> str:
        """
        Analisa história e sugere melhorias.
        ETAPA 2: Identifica problemas e propõe soluções.

        Args:
            story: História completa

        Returns:
            Resposta JSON da IA com sugestões

        Raises:
            Exception: Em caso de erro na API
        """
        prompt = self._build_suggestion_prompt(story)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                timeout=self.timeout,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise Exception("Resposta vazia da API")

        except APITimeoutError:
            raise APITimeoutError("Tempo esgotado ao analisar. Tente novamente.")
        except RateLimitError:
            raise RateLimitError("Limite de requisições atingido. Aguarde alguns minutos.")
        except APIConnectionError:
            raise APIConnectionError("Erro de conexão com a API. Verifique sua internet.")
        except Exception as e:
            raise Exception(f"Erro ao analisar história: {str(e)}")

    def _build_suggestion_prompt(self, story: Dict) -> str:
        """
        Constrói prompt para análise e sugestões.

        Args:
            story: História completa

        Returns:
            Prompt formatado
        """
        historia_texto = story.get('historia_gerada', '')

        prompt = f"""
<task>
Analise esta história técnica e sugira melhorias específicas.
Seja OBJETIVO e PRÁTICO nas sugestões.
NÃO INVENTE - use apenas o que está na história.
</task>

<story>
{historia_texto}
</story>

<analysis_points>
Analise os seguintes aspectos:

1. AMBIGUIDADES:
   - Termos vagos ou imprecisos
   - Falta de especificidade técnica
   - Requisitos não claros

2. TAMANHO:
   - História muito grande (complexidade > 13)?
   - Pode ser quebrada em partes menores?
   - Sugestões de divisão lógica

3. CRITÉRIOS FALTANTES:
   - Cenários não cobertos
   - Casos de erro não tratados
   - Validações ausentes

4. CLAREZA:
   - Seções que precisam mais detalhes
   - Falta de exemplos concretos
   - Informações técnicas incompletas
</analysis_points>

<output_format>
Retorne APENAS JSON array neste formato:
[
  {{
    "type": "ambiguidade|tamanho|criterio|clareza",
    "severity": "baixa|media|alta",
    "problem": "descrição específica do problema encontrado",
    "suggestion": "sugestão específica e acionável de melhoria",
    "applicable": true|false
  }}
]
</output_format>

<important>
- Seja específico: "A seção X está vaga" não "História pode melhorar"
- Sugestões acionáveis: "Adicione critério para caso Y" não "Melhore critérios"
- Use dados da história, não invente
- Máximo 5 sugestões mais importantes
- Retorne APENAS o JSON, sem texto antes ou depois
</important>
"""

        return prompt.strip()
