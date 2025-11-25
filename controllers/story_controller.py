"""
Controller responsável por orquestrar a criação de histórias.
Segue padrão MVC e Single Responsibility Principle.
"""

from typing import Dict, Any
from models.story import Story
from models.session_storage import SessionStorage
from services.ai_service import AIService
from anthropic import APITimeoutError, APIConnectionError, RateLimitError


class StoryController:
    """
    Controller que orquestra o fluxo de criação de histórias.
    Responsável por coordenar Models, Services e Views.
    """

    def __init__(self, ai_service: AIService):
        """
        Inicializa o controller com o service de IA.

        Args:
            ai_service: Instância do AIService configurado
        """
        self.ai_service = ai_service

    def create_story(self, form_data: Dict[str, Any]) -> tuple[Story | None, str | None]:
        """
        Cria uma história a partir dos dados do formulário.

        Args:
            form_data: Dicionário com dados do formulário contendo:
                - titulo: str
                - regras_negocio: List[str]
                - apis_servicos: List[str]
                - objetivos: List[str]
                - complexidade: int
                - criterios_aceitacao: List[str]

        Returns:
            Tupla (Story, error_type) onde:
            - Story: Objeto Story se sucesso, None se erro
            - error_type: None se sucesso, string com tipo de erro se falha
                         (timeout, rate_limit, connection, api_key, generic)
        """
        try:
            # Extrair dados do formulário
            titulo = form_data["titulo"]
            regras_negocio = form_data["regras_negocio"]
            apis_servicos = form_data["apis_servicos"]
            objetivos = form_data["objetivos"]
            complexidade = form_data["complexidade"]
            criterios_aceitacao = form_data["criterios_aceitacao"]
            api_specs = form_data.get("api_specs", None)

            # Chamar AI Service para gerar história
            historia_gerada = self.ai_service.generate_story(
                titulo=titulo,
                regras_negocio=regras_negocio,
                apis_servicos=apis_servicos,
                objetivos=objetivos,
                complexidade=complexidade,
                criterios_aceitacao=criterios_aceitacao,
                api_specs=api_specs
            )

            # Criar objeto Story
            story = Story(
                titulo=titulo,
                regras_negocio=regras_negocio,
                apis_servicos=apis_servicos,
                objetivos=objetivos,
                complexidade=complexidade,
                criterios_aceitacao=criterios_aceitacao,
                historia_gerada=historia_gerada
            )

            # Salvar história no SessionStorage (ETAPA 3)
            SessionStorage.add_story(story.to_dict())

            return story, None

        except APITimeoutError as e:
            return None, "timeout"

        except RateLimitError as e:
            return None, "rate_limit"

        except APIConnectionError as e:
            return None, "connection"

        except Exception as e:
            # Importar traceback para debug detalhado
            import traceback

            # Verifica se é erro de API key
            error_str = str(e).lower()
            if "api key" in error_str or "authentication" in error_str or "unauthorized" in error_str:
                return None, "api_key"

            # Erro genérico - retorna detalhes completos para debug
            error_details = f"{type(e).__name__}: {str(e)}\n\nStack Trace:\n{traceback.format_exc()}"
            return None, f"generic:{error_details}"

    def validate_story_data(self, form_data: Dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Valida os dados do formulário antes de criar a história.

        Args:
            form_data: Dados do formulário

        Returns:
            Tupla (is_valid, errors) onde:
            - is_valid: True se válido, False caso contrário
            - errors: Lista de mensagens de erro
        """
        from models.validation import validate_form

        return validate_form(
            titulo=form_data.get("titulo", ""),
            regras_negocio=form_data.get("regras_negocio", []),
            apis_servicos=form_data.get("apis_servicos", []),
            objetivos=form_data.get("objetivos", {}),
            complexidade=form_data.get("complexidade", 0),
            criterios_aceitacao=form_data.get("criterios_aceitacao", [])
        )
