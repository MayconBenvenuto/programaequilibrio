import sys
import os

# Adicionar o diretório raiz ao path para importar main.py
root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

try:
    # Importar a aplicação Flask do main.py
    from main import app
    
    # Configurar para produção Vercel
    app.config['DEBUG'] = False
    
    # Definir variável app para Vercel
    application = app
    
except Exception as e:
    print(f"Erro ao importar aplicação: {e}")
    raise
