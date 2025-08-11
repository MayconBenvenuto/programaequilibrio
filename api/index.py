import sys
import os

# Adicionar o diretório raiz ao path para importar main.py
root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

# Importar a aplicação completa do main.py
from main import app

# Configurar para produção
app.config['DEBUG'] = False
