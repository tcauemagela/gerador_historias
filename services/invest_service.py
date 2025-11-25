"""
Service responsável pela validação INVEST de histórias.
INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable
Combina validação local (regras) + validação com IA (Claude).
Segue Single Responsibility Principle.
"""

from typing import Dict, Any, List
from models.invest_validator import InvestScore, Suggestion
import json
import re


class InvestService:
    """
    Service que valida histórias segundo critérios INVEST.
    Implementa validação em dois níveis: local e com IA.
    """

    def validate_invest_local(self, story: Dict[str, Any]) -> InvestScore:
        """
        Validação INVEST básica sem usar IA (regras fixas).

        Args:
            story: História completa

        Returns:
            InvestScore com scores básicos
        """
        score = InvestScore()

        # Independent: Verifica se não menciona dependências
        score.independent = self._check_independent(story)
        score.justifications['independent'] = self._justify_independent(score.independent)

        # Negotiable: Score padrão (precisa IA para avaliar)
        score.negotiable = 70
        score.justifications['negotiable'] = "Avaliação completa requer análise com IA"

        # Valuable: Verifica se tem objetivos definidos
        score.valuable = self._check_valuable(story)
        score.justifications['valuable'] = self._justify_valuable(score.valuable)

        # Estimable: Verifica se tem complexidade definida
        score.estimable = self._check_estimable(story)
        score.justifications['estimable'] = self._justify_estimable(score.estimable)

        # Small: Verifica se complexidade <= 13
        score.small = self._check_small(story)
        score.justifications['small'] = self._justify_small(score.small, story.get('complexidade', 0))

        # Testable: Verifica se tem critérios de aceitação
        score.testable = self._check_testable(story)
        score.justifications['testable'] = self._justify_testable(score.testable)

        # Calcular score geral
        score.calculate_overall()

        # Gerar pontos fortes e fracos
        score.strengths, score.weaknesses = self._generate_strengths_weaknesses(score)

        # Gerar sugestões básicas
        score.suggestions = self._generate_basic_suggestions(story, score)

        return score

    def _check_independent(self, story: Dict) -> int:
        """Verifica se história é independente (0-100)."""
        historia_texto = story.get('historia_gerada', '').lower()

        # Palavras que indicam dependência
        dependency_keywords = [
            'depende de',
            'após',
            'depois de',
            'requer que',
            'necessita da',
            'bloqueada por',
            'aguardar'
        ]

        # Contar menções a dependências
        dependency_count = sum(
            historia_texto.count(keyword) for keyword in dependency_keywords
        )

        if dependency_count == 0:
            return 100
        elif dependency_count == 1:
            return 70
        else:
            return 40

    def _justify_independent(self, score: int) -> str:
        """Justifica score de Independent."""
        if score >= 80:
            return "História não menciona dependências explícitas de outras histórias"
        elif score >= 50:
            return "História menciona algumas dependências, mas pode ser desenvolvida independentemente"
        else:
            return "História possui múltiplas dependências que podem bloquear desenvolvimento"

    def _check_valuable(self, story: Dict) -> int:
        """Verifica se história tem valor claro (0-100)."""
        objetivos = story.get('objetivos', [])

        if not objetivos:
            return 30

        if len(objetivos) >= 2:
            return 90
        else:
            return 70

    def _justify_valuable(self, score: int) -> str:
        """Justifica score de Valuable."""
        if score >= 80:
            return "Objetivos técnicos e de negócio estão claramente definidos"
        elif score >= 50:
            return "Valor está presente mas poderia ser mais explícito"
        else:
            return "Valor de negócio/técnico não está claro"

    def _check_estimable(self, story: Dict) -> int:
        """Verifica se história pode ser estimada (0-100)."""
        complexidade = story.get('complexidade', 0)

        if complexidade > 0:
            return 100
        else:
            return 20

    def _justify_estimable(self, score: int) -> str:
        """Justifica score de Estimable."""
        if score >= 80:
            return "Complexidade foi estimada, tornando história estimável"
        else:
            return "Falta estimativa de complexidade"

    def _check_small(self, story: Dict) -> int:
        """Verifica se história tem tamanho adequado (0-100)."""
        complexidade = story.get('complexidade', 0)

        if complexidade == 0:
            return 50  # Não definido

        if complexidade <= 5:
            return 100  # Pequena
        elif complexidade <= 8:
            return 90   # Adequada
        elif complexidade <= 13:
            return 70   # No limite
        else:
            return 30   # Grande demais

    def _justify_small(self, score: int, complexidade: int) -> str:
        """Justifica score de Small."""
        if score >= 90:
            return f"Complexidade de {complexidade} pontos é adequada para uma sprint"
        elif score >= 70:
            return f"Complexidade de {complexidade} pontos está no limite, considere quebrar"
        else:
            return f"Complexidade de {complexidade} pontos é muito alta, história deve ser quebrada"

    def _check_testable(self, story: Dict) -> int:
        """Verifica se história tem critérios testáveis (0-100)."""
        criterios = story.get('criterios_aceitacao', [])

        if not criterios:
            return 10

        num_criterios = len(criterios)

        if num_criterios >= 3:
            return 100
        elif num_criterios == 2:
            return 70
        else:
            return 50

    def _justify_testable(self, score: int) -> str:
        """Justifica score de Testable."""
        if score >= 80:
            return "Critérios de aceitação estão bem definidos e são testáveis"
        elif score >= 50:
            return "Possui alguns critérios, mas poderia ter mais para cobrir edge cases"
        else:
            return "Faltam critérios de aceitação claros e testáveis"

    def _generate_strengths_weaknesses(
        self,
        score: InvestScore
    ) -> tuple[List[str], List[str]]:
        """Gera lista de pontos fortes e fracos."""
        strengths = []
        weaknesses = []

        criteria = [
            ('independent', 'Independência'),
            ('negotiable', 'Negociabilidade'),
            ('valuable', 'Valor'),
            ('estimable', 'Estimabilidade'),
            ('small', 'Tamanho'),
            ('testable', 'Testabilidade')
        ]

        for attr, label in criteria:
            value = getattr(score, attr)

            if value >= 80:
                strengths.append(f"{label}: {value}%")
            elif value < 50:
                weaknesses.append(f"{label}: {value}%")

        return strengths, weaknesses

    def _generate_basic_suggestions(
        self,
        story: Dict,
        score: InvestScore
    ) -> List[str]:
        """Gera sugestões básicas de melhoria."""
        suggestions = []

        # Sugestão baseada em complexidade
        if score.small < 70:
            complexidade = story.get('complexidade', 0)
            suggestions.append(
                f"Considere quebrar esta história em partes menores. "
                f"Complexidade de {complexidade} pontos é muito alta para uma sprint."
            )

        # Sugestão baseada em critérios
        if score.testable < 80:
            num_criterios = len(story.get('criterios_aceitacao', []))
            suggestions.append(
                f"Adicione mais critérios de aceitação. "
                f"Atualmente tem {num_criterios}, recomendado mínimo 3."
            )

        # Sugestão baseada em objetivos
        if score.valuable < 80:
            suggestions.append(
                "Torne os objetivos de negócio/técnicos mais explícitos e mensuráveis."
            )

        # Sugestão baseada em independência
        if score.independent < 80:
            suggestions.append(
                "Reduza dependências de outras histórias para facilitar desenvolvimento paralelo."
            )

        return suggestions

    def prepare_for_ai_validation(self, story: Dict[str, Any]) -> str:
        """
        Prepara prompt para validação INVEST com IA.

        Args:
            story: História completa

        Returns:
            Prompt formatado para Claude API
        """
        historia_texto = story.get('historia_gerada', '')

        prompt = f"""
<task>
Avalie esta história de usuário segundo critérios INVEST.
Seja OBJETIVO e TÉCNICO na avaliação.
NÃO INVENTE INFORMAÇÕES - use apenas o que está na história.
</task>

<story>
{historia_texto}
</story>

<criteria>
Avalie cada critério de 0 a 100:

- Independent: A história pode ser desenvolvida independentemente de outras?
- Negotiable: Tem flexibilidade de implementação ou é muito rígida?
- Valuable: Entrega valor claro ao negócio ou técnico?
- Estimable: É possível estimar o esforço com precisão?
- Small: Tamanho adequado para completar em uma sprint (1-2 semanas)?
- Testable: Possui critérios de aceitação claros e testáveis?
</criteria>

<output_format>
Retorne APENAS JSON válido neste formato exato:
{{
  "independent": {{"score": 0-100, "justification": "explicação objetiva"}},
  "negotiable": {{"score": 0-100, "justification": "explicação objetiva"}},
  "valuable": {{"score": 0-100, "justification": "explicação objetiva"}},
  "estimable": {{"score": 0-100, "justification": "explicação objetiva"}},
  "small": {{"score": 0-100, "justification": "explicação objetiva"}},
  "testable": {{"score": 0-100, "justification": "explicação objetiva"}},
  "strengths": ["ponto forte 1", "ponto forte 2"],
  "weaknesses": ["ponto fraco 1", "ponto fraco 2"],
  "suggestions": ["sugestão específica 1", "sugestão específica 2"]
}}
</output_format>

<important>
- Seja específico nas justificativas
- Sugestões devem ser acionáveis
- Use dados da história, não invente
- Retorne APENAS o JSON, sem texto antes ou depois
</important>
"""

        return prompt.strip()

    def parse_ai_validation_response(self, ai_response: str) -> InvestScore:
        """
        Parseia resposta da IA para criar InvestScore.

        Args:
            ai_response: Resposta JSON da IA

        Returns:
            InvestScore preenchido
        """
        try:
            data = json.loads(ai_response)

            score = InvestScore(
                independent=data['independent']['score'],
                negotiable=data['negotiable']['score'],
                valuable=data['valuable']['score'],
                estimable=data['estimable']['score'],
                small=data['small']['score'],
                testable=data['testable']['score'],
                strengths=data.get('strengths', []),
                weaknesses=data.get('weaknesses', []),
                suggestions=data.get('suggestions', [])
            )

            # Adicionar justificativas
            for criterion in ['independent', 'negotiable', 'valuable', 'estimable', 'small', 'testable']:
                if criterion in data:
                    score.justifications[criterion] = data[criterion].get('justification', '')

            # Calcular score geral
            score.calculate_overall()

            return score

        except (json.JSONDecodeError, KeyError) as e:
            # Retornar score vazio em caso de erro
            return InvestScore()
