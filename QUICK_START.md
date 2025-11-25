# 🚀 Guia Rápido de Instalação

## ⚡ Setup em 5 Minutos

### 1. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 2. Configure a API Key

Crie um arquivo `.env` na raiz do projeto:

```bash
ANTHROPIC_API_KEY=sua-chave-api-aqui
```

**Onde obter a chave:** https://console.anthropic.com/

### 3. Execute o Projeto

```bash
streamlit run app.py
```

Pronto! O aplicativo abrirá em `http://localhost:8501`

## 📝 Teste Rápido

1. **Título**: "Implementar autenticação OAuth com Google"
2. **Regra de Negócio**: "Usuário deve poder fazer login com conta Google"
3. **API/Serviço**: "Google OAuth 2.0 API"
4. **Objetivo**: "Permitir autenticação social segura"
5. **Complexidade**: 5
6. **Critério**: "Dado que usuário clica em 'Login com Google', quando autentica, então é redirecionado para dashboard"

Clique em "Gerar História" e veja a mágica acontecer!

## 🐛 Problemas Comuns

**API Key não encontrada:**
```bash
# Verifique se o arquivo .env existe
ls -la .env

# Verifique o conteúdo
cat .env
```

**Erro ao importar módulos:**
```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt
```

**Streamlit não encontrado:**
```bash
pip install streamlit
```

## 📚 Documentação Completa

Veja o arquivo [README.md](README.md) para documentação completa.
