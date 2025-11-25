"""
Modelo de dados para validação INVEST de histórias de usuário.
INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable
Segue Single Responsibility Principle.
"""

from dataclasses import dataclass, field
from typing import List, Dict
import json


@dataclass
class InvestScore:
    """
    Representa o resultado da validação INVEST de uma história.

    Cada critério recebe score de 0-100.
    Score geral é a média dos 6 critérios.

    Attributes:
        independent: Score para Independent (0-100)
        negotiable: Score para Negotiable (0-100)
        valuable: Score para Valuable (0-100)
        estimable: Score para Estimable (0-100)
        small: Score para Small (0-100)
        testable: Score para Testable (0-100)
        overall: Score geral (média dos 6 critérios)
        strengths: Lista de pontos fortes identificados
        weaknesses: Lista de pontos fracos identificados
        suggestions: Lista de sugestões de melhoria
        justifications: Justificativas para cada score
    """

    independent: int = 0  # 0-100
    negotiable: int = 0
    valuable: int = 0
    estimable: int = 0
    small: int = 0
    testable: int = 0

    overall: int = 0  # média dos 6 critérios

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    justifications: Dict[str, str] = field(default_factory=dict)

    def calculate_overall(self) -> int:
        """
        Calcula score geral como média dos 6 critérios.

        Returns:
            Score geral (0-100)
        """
        scores = [
            self.independent,
            self.negotiable,
            self.valuable,
            self.estimable,
            self.small,
            self.testable
        ]
        self.overall = sum(scores) // len(scores)
        return self.overall

    def get_status_color(self) -> str:
        """
        Retorna cor baseada no score geral.

        Returns:
            "green", "orange" ou "red"
        """
        if self.overall >= 80:
            return "green"
        elif self.overall >= 50:
            return "orange"
        else:
            return "red"

    def get_status_label(self) -> str:
        """
        Retorna label baseado no score geral.

        Returns:
            "Excelente", "Regular" ou "Necessita Melhorias"
        """
        color = self.get_status_color()
        if color == "green":
            return "Excelente"
        elif color == "orange":
            return "Regular"
        else:
            return "Necessita Melhorias"

    def get_criterion_status(self, criterion_score: int) -> str:
        """
        Retorna status de um critério específico.

        Args:
            criterion_score: Score do critério (0-100)

        Returns:
            "Bom", "Regular" ou "Fraco"
        """
        if criterion_score >= 80:
            return "Bom"
        elif criterion_score >= 50:
            return "Regular"
        else:
            return "Fraco"

    def to_dict(self) -> Dict:
        """
        Converte para dicionário.

        Returns:
            Dict com todos os dados do score
        """
        return {
            "scores": {
                "independent": self.independent,
                "negotiable": self.negotiable,
                "valuable": self.valuable,
                "estimable": self.estimable,
                "small": self.small,
                "testable": self.testable,
                "overall": self.overall
            },
            "status": {
                "color": self.get_status_color(),
                "label": self.get_status_label()
            },
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "suggestions": self.suggestions,
            "justifications": self.justifications
        }

    def to_json(self) -> str:
        """
        Converte para JSON.

        Returns:
            String JSON formatada
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class Suggestion:
    """
    Representa uma sugestão de melhoria para a história.

    Attributes:
        type: Tipo da sugestão (ambiguidade, tamanho, criterio, clareza)
        severity: Severidade (baixa, media, alta)
        problem: Descrição do problema identificado
        suggestion: Sugestão de melhoria
        applicable: Se pode ser aplicada automaticamente
    """

    type: str  # "ambiguidade", "tamanho", "criterio", "clareza"
    severity: str  # "baixa", "media", "alta"
    problem: str
    suggestion: str
    applicable: bool = False

    def get_severity_color(self) -> str:
        """
        Retorna cor baseada na severidade.

        Returns:
            "red", "orange" ou "blue"
        """
        if self.severity == "alta":
            return "red"
        elif self.severity == "media":
            return "orange"
        else:
            return "blue"

    def get_severity_icon(self) -> str:
        """
        Retorna ícone baseado na severidade.

        Returns:
            Emoji representando a severidade
        """
        if self.severity == "alta":
            return "🔴"
        elif self.severity == "media":
            return "🟠"
        else:
            return "🔵"

    def get_type_icon(self) -> str:
        """
        Retorna ícone baseado no tipo.

        Returns:
            Emoji representando o tipo
        """
        icons = {
            "ambiguidade": "❓",
            "tamanho": "📏",
            "criterio": "✅",
            "clareza": "💡"
        }
        return icons.get(self.type, "📝")

    def to_dict(self) -> Dict:
        """
        Converte para dicionário.

        Returns:
            Dict com dados da sugestão
        """
        return {
            "type": self.type,
            "severity": self.severity,
            "problem": self.problem,
            "suggestion": self.suggestion,
            "applicable": self.applicable
        }
