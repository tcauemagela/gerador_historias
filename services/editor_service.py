"""
Service responsável pela lógica de edição de histórias.
Valida e processa alterações feitas pelo usuário.
Segue Single Responsibility Principle.
"""

from typing import Dict, Any, Tuple, List
import re


class EditorService:
    """
    Service que gerencia edição de histórias.
    Responsável por validar e processar alterações.
    """

    def validate_edit(self, edited_content: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida conteúdo editado antes de salvar.

        Args:
            edited_content: Dicionário com campos editados

        Returns:
            Tupla (is_valid, errors)
        """
        errors = []

        # Validar campos obrigatórios
        required_fields = [
            'titulo',
            'contexto',
            'objetivo',
            'regras_negocio',
            'apis_servicos',
            'objetivos_tecnicos',
            'criterios_aceitacao'
        ]

        for field in required_fields:
            if field not in edited_content or not edited_content[field]:
                errors.append(f"Campo '{field}' não pode estar vazio")

        # Validar que listas não estão vazias
        list_fields = [
            'regras_negocio',
            'apis_servicos',
            'objetivos_tecnicos',
            'criterios_aceitacao'
        ]

        for field in list_fields:
            if field in edited_content:
                if isinstance(edited_content[field], list):
                    if len(edited_content[field]) == 0:
                        errors.append(f"'{field}' deve ter pelo menos um item")
                elif isinstance(edited_content[field], str):
                    # Se for string, deve ter conteúdo
                    if not edited_content[field].strip():
                        errors.append(f"'{field}' não pode estar vazio")

        # Validar formato básico de Markdown (se fornecido)
        if 'historia_completa' in edited_content:
            if not self._validate_markdown_structure(edited_content['historia_completa']):
                errors.append("Estrutura Markdown inválida")

        return len(errors) == 0, errors

    def _validate_markdown_structure(self, markdown_text: str) -> bool:
        """
        Valida estrutura básica de Markdown.

        Args:
            markdown_text: Texto em Markdown

        Returns:
            True se estrutura válida
        """
        if not markdown_text or not markdown_text.strip():
            return False

        # Verificar se tem pelo menos um header ##
        if not re.search(r'^##\s+.+', markdown_text, re.MULTILINE):
            return False

        return True

    def parse_sections_from_markdown(self, markdown_text: str) -> Dict[str, str]:
        """
        Extrai seções de um texto Markdown.

        Args:
            markdown_text: História completa em Markdown

        Returns:
            Dict com seções extraídas
        """
        sections = {}

        # Padrão para encontrar seções ### Nome da Seção
        pattern = r'###\s+([^\n]+)\n\n?((?:(?!###).)+)'

        matches = re.finditer(pattern, markdown_text, re.DOTALL)

        for match in matches:
            section_name = match.group(1).strip()
            section_content = match.group(2).strip()
            sections[section_name] = section_content

        return sections

    def merge_sections(self, original_story: Dict, edited_sections: Dict[str, str]) -> str:
        """
        Mescla seções editadas com história original.

        Args:
            original_story: História original completa
            edited_sections: Seções que foram editadas

        Returns:
            História completa mesclada em Markdown
        """
        # Reconstruir Markdown com seções editadas
        markdown_parts = []

        # Adicionar título (## nível)
        if 'titulo' in edited_sections:
            markdown_parts.append(f"## {edited_sections['titulo']}\n")

        # Adicionar seções (### nível)
        section_order = [
            'Contexto',
            'Objetivo',
            'Regras de Negocio',
            'APIs e Servicos Necessarios',
            'Objetivos Tecnicos',
            'Criterios de Aceitacao',
            'Cenarios de Teste Sugeridos',
            'Complexidade'
        ]

        for section_name in section_order:
            if section_name in edited_sections:
                markdown_parts.append(f"### {section_name}\n\n{edited_sections[section_name]}\n")

        return "\n".join(markdown_parts)

    def extract_changes_summary(self, old_content: Dict, new_content: Dict) -> str:
        """
        Gera resumo automático das mudanças realizadas.

        Args:
            old_content: Conteúdo anterior
            new_content: Novo conteúdo

        Returns:
            Resumo das mudanças
        """
        changes = []

        # Campos a verificar
        fields_to_check = [
            ('titulo', 'Título'),
            ('contexto', 'Contexto'),
            ('objetivo', 'Objetivo'),
            ('regras_negocio', 'Regras de Negócio'),
            ('apis_servicos', 'APIs/Serviços'),
            ('criterios_aceitacao', 'Critérios de Aceitação')
        ]

        for field_key, field_label in fields_to_check:
            old_value = old_content.get(field_key, '')
            new_value = new_content.get(field_key, '')

            if old_value != new_value:
                changes.append(f"Modificou {field_label}")

        if not changes:
            return "Sem alterações significativas"

        return ", ".join(changes)

    def sanitize_markdown(self, markdown_text: str) -> str:
        """
        Remove ou corrige problemas comuns em Markdown.

        Args:
            markdown_text: Texto Markdown

        Returns:
            Markdown sanitizado
        """
        # Remove múltiplas linhas vazias consecutivas
        markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)

        # Remove espaços em branco no final das linhas
        markdown_text = re.sub(r' +\n', '\n', markdown_text)

        # Remove espaços no início e fim
        markdown_text = markdown_text.strip()

        return markdown_text

    def prepare_for_regeneration(
        self,
        original_story: Dict,
        section_name: str
    ) -> Dict[str, Any]:
        """
        Prepara dados para regeneração parcial de seção.

        Args:
            original_story: História original completa
            section_name: Nome da seção a regenerar

        Returns:
            Dict com dados preparados para prompt
        """
        return {
            'section_to_regenerate': section_name,
            'original_context': original_story.get('contexto', ''),
            'original_objetivo': original_story.get('objetivo', ''),
            'form_data': {
                'titulo': original_story.get('titulo', ''),
                'regras_negocio': original_story.get('regras_negocio', []),
                'apis_servicos': original_story.get('apis_servicos', []),
                'objetivos': original_story.get('objetivos_tecnicos', []),
                'complexidade': original_story.get('complexidade', 5),
                'criterios_aceitacao': original_story.get('criterios_aceitacao', [])
            }
        }
