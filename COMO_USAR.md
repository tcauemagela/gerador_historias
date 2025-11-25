# 🚀 COMO USAR - Guia Definitivo

## ✅ Status: Projeto 100% Pronto!

**Localização:** `C:\Users\Usuário\Desktop\projetos_ia\gerador_historia\`

**Dependências:** ✅ Todas instaladas!

---

## 📝 PRÓXIMOS PASSOS

### Passo 1: Configure sua API Key da Anthropic

**IMPORTANTE:** Você precisa de uma chave de API da Anthropic para usar o sistema.

#### Opção A - Criar arquivo .env (Desenvolvimento Local)

1. Vá para a pasta do projeto:
   ```bash
   cd "C:\Users\Usuário\Desktop\projetos_ia\gerador_historia"
   ```

2. Copie o arquivo de exemplo:
   ```bash
   copy .env.example .env
   ```

3. Edite o arquivo `.env` com qualquer editor de texto:
   ```
   ANTHROPIC_API_KEY=sua-chave-api-aqui
   ```

4. **Onde obter a chave:**
   - Acesse: https://console.anthropic.com/
   - Faça login ou crie uma conta
   - Vá em "API Keys"
   - Clique em "Create Key"
   - Copie a chave e cole no arquivo .env

#### Opção B - Usar Streamlit Secrets (Deploy)

Se for fazer deploy no Streamlit Cloud:
1. Vá em Settings > Secrets
2. Adicione:
   ```toml
   ANTHROPIC_API_KEY = "sua-chave-aqui"
   ```

---

### Passo 2: Execute o Projeto

```bash
cd "C:\Users\Usuário\Desktop\projetos_ia\gerador_historia"
streamlit run app.py
```

O aplicativo abrirá automaticamente no navegador em `http://localhost:8501`

---

## 🎯 EXEMPLO DE USO

### Teste Rápido (copie e cole):

1. **Título:**
   ```
   Implementar autenticação OAuth com Google
   ```

2. **Regra de Negócio:**
   ```
   Usuário deve poder fazer login com conta Google existente
   ```
   (Clique em "➕ Adicionar Regra" para mais regras)

3. **API/Serviço:**
   ```
   Google OAuth 2.0 API
   ```

4. **Objetivo:**
   ```
   Permitir autenticação social de forma segura e rápida
   ```

5. **Complexidade:**
   ```
   5
   ```

6. **Critério de Aceitação:**
   ```
   Dado que o usuário clica em "Login com Google", quando autentica com sucesso, então deve ser redirecionado para o dashboard
   ```

Clique em **"🤖 Gerar História"** e aguarde 10-30 segundos!

---

## 📥 EXPORTAR HISTÓRIA

Após gerar, você pode exportar em:

- **📄 TXT**: Texto simples (sem formatação)
- **📝 Markdown**: Com toda a formatação
- **📊 JSON**: Dados estruturados para integração
- **📋 Copiar**: Copiar para área de transferência

---

## 🏗️ ESTRUTURA DO PROJETO

```
gerador_historia/
├── app.py                    # ⭐ ARQUIVO PRINCIPAL - Execute este!
├── config.py                 # Configurações e API key
├── requirements.txt          # Dependências (já instaladas)
├── .env.example              # Template de configuração
├── .env                      # ⚠️ CRIE ESTE com sua API key!
├── README.md                 # Documentação completa
├── QUICK_START.md            # Guia rápido
├── COMO_USAR.md             # Este arquivo
│
├── controllers/              # Orquestração MVC
├── models/                   # Modelos de dados
├── views/                    # Interface do usuário
├── services/                 # Integração com Claude API
└── utils/                    # Funções auxiliares
```

---

## 🐛 PROBLEMAS COMUNS

### ❌ "API Key não encontrada"

**Solução:**
1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Abra o arquivo e confirme que está no formato:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-sua-chave-aqui
   ```
3. Reinicie a aplicação

### ❌ "ModuleNotFoundError"

**Solução:**
```bash
pip install -r requirements.txt
```

### ❌ História não gera (fica carregando)

**Possíveis causas:**
1. Internet lenta ou sem conexão
2. API key inválida
3. Limite de requisições atingido

**Solução:**
- Aguarde até 30 segundos
- Verifique sua conexão
- Teste a API key em https://console.anthropic.com/

### ❌ Botões +/- não funcionam

**Solução:**
```bash
streamlit cache clear
```
E reinicie a aplicação.

---

## 🎨 FORMATO DA HISTÓRIA GERADA

As histórias seguem este padrão técnico:

```markdown
## 📋 [Título da Tarefa]

### 🎯 Descrição
Descrição detalhada da implementação

### 📐 Regras de Negócio
- Regra 1
- Regra 2

### 🔌 APIs/Serviços Necessários
- API X (uso Y)
- Serviço Z (uso W)

### 🎯 Objetivos
- Objetivo mensurável 1
- Objetivo mensurável 2

### ✅ Critérios de Aceitação
- Critério 1
- Critério 2

### 🧪 Cenários de Teste Sugeridos
1. Cenário de sucesso
2. Cenário de erro
3. Cenário edge case

### 📊 Complexidade
Pontos: 5
Justificativa: [explicação]
```

---

## 💡 DICAS

1. **Seja específico**: Quanto mais detalhes você fornecer, melhor será a história
2. **Use múltiplas entradas**: Adicione várias regras, APIs e critérios
3. **Escala Fibonacci**: Use valores 1, 2, 3, 5, 8, 13, 21 para complexidade
4. **Formato técnico**: O sistema gera tarefas técnicas (não "Como usuário, eu quero...")
5. **Tempo de resposta**: A IA pode levar de 10 a 30 segundos

---

## 📚 DOCUMENTAÇÃO

- **README.md**: Documentação técnica completa
- **QUICK_START.md**: Instalação em 5 minutos
- **COMO_USAR.md**: Este guia (orientado ao uso)

---

## 🎉 PRONTO PARA COMEÇAR!

Execute agora:

```bash
cd "C:\Users\Usuário\Desktop\projetos_ia\gerador_historia"
streamlit run app.py
```

**Não esqueça de configurar o arquivo .env com sua API key primeiro!**

---

## 📞 PRECISA DE AJUDA?

1. Leia o README.md completo
2. Verifique a seção de Troubleshooting
3. Consulte a documentação da Anthropic: https://docs.anthropic.com/

---

**Desenvolvido com arquitetura SOLID/MVC**
**Powered by Claude AI e Streamlit**
