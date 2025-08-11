import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Aplicação Flask mínima para testar
from flask import Flask

# Criar aplicação básica
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>🎉 TESTE BÁSICO FUNCIONANDO!</h1><p>Se você vê esta mensagem, a aplicação está rodando corretamente.</p>'

@app.route('/health')
def health():
    return {'status': 'OK', 'message': 'Aplicação funcionando'}

# Para Vercel
application = app

if __name__ == '__main__':
    app.run(debug=True)
