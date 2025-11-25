"""
Módulo de validação de formulários.
Responsável por validar entradas do usuário antes do processamento.
Segue Single Responsibility Principle.
"""

import re
from typing import List, Tuple, Dict, Any


def validate_titulo(titulo: str) -> Tuple[bool, str]:
    """
    Valida o título da história.

    Args:
        titulo: Título a ser validado

    Returns:
        Tupla (is_valid, error_message)
    """
    if not titulo or not titulo.strip():
        return False, "Título não pode estar vazio"

    if len(titulo) > 100:
        return False, "Título não pode ter mais de 100 caracteres"

    # Verifica caracteres especiais não permitidos
    caracteres_proibidos = r'[!@#$%^&*()]'
    if re.search(caracteres_proibidos, titulo):
        return False, "Título não pode conter caracteres especiais (!@#$%^&*())"

    return True, ""


def validate_lista_campos(
    lista: List[str],
    nome_campo: str,
    min_items: int = 1
) -> Tuple[bool, str]:
    """
    Valida campos que contêm listas de strings.

    Args:
        lista: Lista de strings a validar
        nome_campo: Nome do campo para mensagens de erro
        min_items: Número mínimo de itens não vazios

    Returns:
        Tupla (is_valid, error_message)
    """
    # Remove strings vazias ou apenas com espaços
    lista_limpa = [item.strip() for item in lista if item and item.strip()]

    if len(lista_limpa) < min_items:
        return False, f"{nome_campo} deve ter pelo menos {min_items} item(ns)"

    return True, ""


def validate_complexidade(complexidade: int) -> Tuple[bool, str]:
    """
    Valida pontos de complexidade.

    Args:
        complexidade: Valor de complexidade

    Returns:
        Tupla (is_valid, error_message)
    """
    if complexidade < 1:
        return False, "Complexidade deve ser no mínimo 1"

    if complexidade > 21:
        return False, "Complexidade não pode ser maior que 21"

    return True, ""


def validate_objetivos_dict(objetivos: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Valida dicionário de objetivos (nova estrutura).

    Args:
        objetivos: Dicionário com subseções de objetivos

    Returns:
        Tupla (is_valid, error_message)
    """
    if not isinstance(objetivos, dict):
        return False, "Objetivos deve ser um dicionário"

    # Verificar se pelo menos um campo foi preenchido
    valores_preenchidos = [v.strip() for v in objetivos.values() if v and isinstance(v, str) and v.strip()]

    if len(valores_preenchidos) == 0:
        return False, "Pelo menos um campo de Objetivos deve ser preenchido"

    return True, ""


def validate_form(
    titulo: str,
    regras_negocio: List[str],
    apis_servicos: List[str],
    objetivos: Dict[str, Any],  # Mudado de List[str] para Dict[str, Any]
    complexidade: int,
    criterios_aceitacao: List[str]
) -> Tuple[bool, List[str]]:
    """
    Valida todos os campos do formulário.

    Args:
        titulo: Título da história
        regras_negocio: Lista de regras de negócio
        apis_servicos: Lista de APIs/serviços
        objetivos: Dicionário de objetivos com subseções
        complexidade: Pontos de complexidade
        criterios_aceitacao: Lista de critérios de aceitação

    Returns:
        Tupla (is_valid, list_of_errors)
    """
    errors = []

    # Valida título
    valid, error = validate_titulo(titulo)
    if not valid:
        errors.append(f"❌ Título: {error}")

    # Valida regras de negócio
    valid, error = validate_lista_campos(
        regras_negocio,
        "Regras de Negócio",
        min_items=1
    )
    if not valid:
        errors.append(f"❌ Regras de Negócio: {error}")

    # Valida APIs/Serviços
    valid, error = validate_lista_campos(
        apis_servicos,
        "APIs/Serviços",
        min_items=1
    )
    if not valid:
        errors.append(f"❌ APIs/Serviços: {error}")

    # Valida objetivos (novo formato dict) - validação desabilitada, campos opcionais
    # valid, error = validate_objetivos_dict(objetivos)
    # if not valid:
    #     errors.append(f"❌ Objetivos: {error}")

    # Valida complexidade
    valid, error = validate_complexidade(complexidade)
    if not valid:
        errors.append(f"❌ Complexidade: {error}")
    elif error:  # Warning sobre Fibonacci
        errors.append(error)

    # Valida critérios de aceitação
    valid, error = validate_lista_campos(
        criterios_aceitacao,
        "Critérios de Aceitação",
        min_items=1
    )
    if not valid:
        errors.append(f"❌ Critérios de Aceitação: {error}")

    return len(errors) == 0, errors
