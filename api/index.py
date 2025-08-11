import sys
import os

# Adicionar o diretório raiz ao path para importar main.py
root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

# Criar aplicação Flask híbrida
from flask import Flask

# Tentar importar a aplicação completa, mas manter um fallback
try:
    from main import app as main_app
    print("✅ Aplicação principal importada com sucesso")
    
    # Usar a aplicação principal
    app = main_app
    app.config['DEBUG'] = False
    
except Exception as e:
    print(f"⚠️ Erro ao importar aplicação principal: {e}")
    print("🔄 Usando aplicação de fallback")
    
    # Criar aplicação de fallback
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return '''
        <html>
            <head><title>Programa Equilíbrio - Carregando</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>🔄 Programa Equilíbrio - Sistema em Carregamento</h1>
                <p>A aplicação está sendo inicializada. Por favor, aguarde alguns segundos e recarregue a página.</p>
                <p><strong>Se esta mensagem persistir, há um problema de configuração.</strong></p>
                <div style="margin-top: 30px; padding: 20px; background: #f0f0f0; border-radius: 5px;">
                    <h3>🧪 Status do Sistema:</h3>
                    <p>✅ Vercel funcionando</p>
                    <p>✅ Python executando</p>
                    <p>⚠️ Aplicação principal com problemas</p>
                </div>
            </body>
        </html>
        '''
