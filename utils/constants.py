"""
Constantes utilizadas em todo o sistema.
Centraliza valores fixos para facilitar manutenção.
"""

# Validação de formulário
MAX_TITULO_LENGTH = 100
MIN_COMPLEXIDADE = 1
MAX_COMPLEXIDADE = 21

# Escala Fibonacci recomendada para complexidade
FIBONACCI_SCALE = [1, 2, 3, 5, 8, 13, 21]

# Caracteres proibidos no título
CARACTERES_PROIBIDOS_TITULO = r'[!@#$%^&*()]'

# Configurações de UI
APP_TITLE = "Gerador de Histórias de Usuário com IA"
APP_ICON = "📝"
APP_LAYOUT = "wide"

# Mensagens padrão
MSG_CAMPO_OBRIGATORIO = "Este campo é obrigatório"
MSG_TITULO_VAZIO = "Título não pode estar vazio"
MSG_LISTA_VAZIA = "Adicione pelo menos um item"

# Formato de arquivos
MIME_TYPES = {
    "txt": "text/plain",
    "md": "text/markdown",
    "json": "application/json"
}

# Configurações de exportação
MAX_FILENAME_LENGTH = 50
