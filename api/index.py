import sys
import os

# Adicionar o diretório raiz ao path para importar main.py
root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

# Verificar se podemos importar sem problemas de Supabase em produção
try:
    # Importar a aplicação completa do main.py
    from main import app
    print("✅ [VERCEL] Aplicação importada com sucesso do main.py")
except Exception as e:
    print(f"⚠️ [VERCEL] Erro ao importar main.py: {e}")
    
    # Fallback: importar versão simplificada se houver problema
    try:
        from app_test import app
        print("✅ [VERCEL] Usando app_test.py como fallback")
    except Exception as e2:
        print(f"❌ [VERCEL] Erro crítico: {e2}")
        # Criar app básico de emergência
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/')
        def emergency():
            return jsonify({'status': 'error', 'message': 'Erro de configuração do servidor'})

# Configurar para produção
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Log de inicialização
print("🚀 [VERCEL] Aplicação iniciada para produção")
print(f"📋 [VERCEL] Debug: {app.config.get('DEBUG')}")
print(f"📋 [VERCEL] Routes disponíveis:")
for rule in app.url_map.iter_rules():
    print(f"   {rule.endpoint}: {rule.rule}")

# Exportar app para o Vercel
# O Vercel procura por uma variável chamada 'app'
if __name__ == "__main__":
    # Não executar em produção, apenas para testes locais
    app.run(debug=False)
