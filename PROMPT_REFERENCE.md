# 📚 PROMPT DE REFERÊNCIA - Geração de Histórias de Usuário

Este documento contém o prompt base usado pelo sistema para gerar histórias de usuário profissionais.

## 🎯 Regras Fundamentais

### ⚠️ REGRAS OBRIGATÓRIAS (NUNCA VIOLAR):

1. **NUNCA ADICIONAR EMOJIS NAS HISTÓRIAS GERADAS**
   - Histórias devem ser puramente profissionais
   - Sem emojis decorativos em títulos ou seções
   - Formato corporativo/técnico apenas

2. **NUNCA INVENTAR INFORMAÇÕES**
   - Usar APENAS dados fornecidos pelo usuário
   - Não criar APIs, endpoints ou tecnologias não mencionadas
   - Não adicionar regras de negócio não fornecidas
   - Se algo não foi informado, não especular

3. **NÃO SER MUITO CRIATIVA**
   - Ser objetiva e direta
   - Evitar floreios ou descrições excessivamente elaboradas
   - Foco em clareza e precisão técnica
   - Manter tom profissional e direto ao ponto

---

## 📋 Estrutura Obrigatória das Histórias

Toda história DEVE conter estas seções:

### 1. Título
Claro, descritivo e técnico

### 2. Formato Inicial
**Opção A - Clássico:**
```
Como [papel técnico]
Quero [funcionalidade]
Para [benefício técnico/negócio]
```

**Opção B - Direto:**
Sem formato "como/quero/para", direto para Contexto/Problema

### 3. Contexto/Problema
- Situação atual que motiva a história
- Problemas identificados
- Diagnóstico técnico (se aplicável)

### 4. Objetivo
- O que se pretende alcançar tecnicamente
- Métricas esperadas (se fornecidas)
- Resultado final esperado

### 5. Regras de Negócio
- TODAS as regras fornecidas pelo usuário
- Formato bullet points claro
- Sem adicionar regras não informadas

### 6. APIs/Serviços
Para cada API mencionada:
- Nome do serviço/API
- Endpoint (se fornecido)
- Método HTTP (se fornecido)
- Descrição técnica de uso

### 7. Objetivos Técnicos
- Lista de objetivos fornecidos
- Resultados esperados
- KPIs (se fornecidos)

### 8. Critérios de Aceitação
**Mínimo 3 critérios**, incluindo:
- Casos de sucesso (happy path)
- Casos de erro/exceção
- Validações técnicas

**Formatos aceitos:**

**Gherkin:**
```
Dado que [condição inicial]
Quando [ação executada]
Então [resultado esperado]
```

**Bullet points técnicos:**
```
- Validação X deve retornar Y
- Sistema deve processar em < Z segundos
- Formato de saída deve ser W
```

### 9. Cenários de Teste
Mínimo 3 cenários:
1. Cenário de sucesso
2. Cenário de erro/exceção
3. Cenário edge case

### 10. Complexidade
```
Pontos: [valor fornecido pelo usuário]
Justificativa: [explicação baseada nos dados fornecidos]
```

---

## ✅ Checklist de Qualidade

Antes de entregar, verificar:

**Completude:**
- [ ] Todas as seções obrigatórias presentes
- [ ] Todas as regras de negócio incluídas
- [ ] Todos os objetivos incluídos
- [ ] Todas as APIs mencionadas detalhadas
- [ ] Critérios de aceite completos (mínimo 3)

**Precisão:**
- [ ] Nenhuma informação inventada
- [ ] Apenas dados fornecidos pelo usuário
- [ ] Sem emojis no conteúdo da história
- [ ] Linguagem técnica e objetiva

**Formato:**
- [ ] Markdown bem estruturado
- [ ] Seções claramente separadas
- [ ] Critérios testáveis e verificáveis

---

## 🚫 Anti-Patterns (EVITAR)

❌ **Inventar tecnologias não mencionadas:**
```
Errado: "Usar Redis para cache e MongoDB para dados"
(se usuário não mencionou Redis/MongoDB)

Certo: "Usar [tecnologia informada pelo usuário]"
```

❌ **Adicionar regras não fornecidas:**
```
Errado: Adicionar "Sistema deve validar CPF" se não foi informado

Certo: Incluir APENAS regras fornecidas pelo usuário
```

❌ **Usar emojis:**
```
Errado: "## 🎯 Objetivo"
Errado: "✅ Validação concluída"

Certo: "## Objetivo"
Certo: "Validação concluída"
```

❌ **Ser muito criativo/elaborado:**
```
Errado: "Esta maravilhosa solução revolucionária transformará..."

Certo: "Esta implementação permitirá..."
```

---

## 📝 Exemplo de História Correta

```markdown
# Implementar autenticação OAuth com Google

## Formato

Como desenvolvedor backend
Quero integrar autenticação OAuth 2.0 do Google
Para permitir login seguro de usuários no sistema

## Contexto

Atualmente o sistema utiliza autenticação básica com usuário e senha.
Necessidade de adicionar opção de login social para melhorar experiência
do usuário e reduzir atrito no cadastro.

## Objetivo

Implementar fluxo completo de autenticação OAuth 2.0 utilizando
Google Identity Platform, permitindo que usuários façam login
com suas contas Google existentes.

## Regras de Negócio

- Usuário deve poder iniciar login clicando em botão "Login com Google"
- Sistema deve redirecionar para tela de consentimento do Google
- Após autorização, sistema deve criar ou atualizar cadastro do usuário
- Email do Google deve ser usado como identificador único
- Sessão deve expirar após 24 horas de inatividade

## APIs/Serviços

### Google OAuth 2.0 API
- Endpoint de autorização: https://accounts.google.com/o/oauth2/v2/auth
- Endpoint de token: https://oauth2.googleapis.com/token
- Escopos necessários: openid, email, profile
- Método: POST para obtenção de tokens

## Objetivos

- Permitir autenticação via conta Google
- Reduzir tempo de cadastro de novos usuários
- Aumentar taxa de conversão no signup

## Critérios de Aceitação

### CA1 - Iniciar fluxo OAuth
Dado que usuário acessa tela de login
Quando clica em "Login com Google"
Então deve ser redirecionado para tela de consentimento do Google

### CA2 - Processar callback
Dado que usuário autorizou acesso
Quando Google redireciona de volta com código
Então sistema deve trocar código por tokens
E criar/atualizar usuário no banco de dados

### CA3 - Tratar erro de autorização
Dado que usuário nega permissão no Google
Quando retorna para aplicação
Então sistema deve exibir mensagem de erro
E permitir tentar novamente

### CA4 - Validar token
Dado que usuário possui token válido
Quando acessa área autenticada
Então sistema deve validar token com Google
E permitir acesso aos recursos

## Cenários de Teste

1. **Sucesso**: Usuário completa fluxo OAuth e é autenticado
2. **Erro**: Usuário nega permissão e recebe mensagem apropriada
3. **Edge case**: Token expira durante sessão e renova automaticamente

## Complexidade

Pontos: 5

Justificativa:
- Integração com API externa (Google)
- Implementação de fluxo OAuth completo
- Tratamento de callbacks e tokens
- Sincronização de dados de usuário
```

---

## 🎯 Resumo das Diretrizes

1. **Use APENAS informações fornecidas**
2. **Seja objetiva e direta**
3. **Sem emojis no conteúdo da história**
4. **Todas as seções obrigatórias presentes**
5. **Critérios testáveis e verificáveis**
6. **Linguagem técnica profissional**
7. **Formato Markdown estruturado**

---

*Este documento deve ser consultado sempre que houver dúvidas sobre o formato
ou conteúdo esperado nas histórias geradas.*
