import sys
import os
import traceback

# Adicionar o diretório raiz ao path para importar main.py
root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

print("🚀 [VERCEL] Iniciando aplicação...")
print(f"📁 [VERCEL] Diretório raiz: {root_dir}")
print(f"🌍 [VERCEL] Variáveis de ambiente relevantes:")
print(f"   VERCEL: {os.environ.get('VERCEL')}")
print(f"   FLASK_ENV: {os.environ.get('FLASK_ENV')}")
print(f"   DEBUG: {os.environ.get('DEBUG')}")

# Verificar se podemos importar sem problemas de Supabase em produção
try:
    # Importar a aplicação completa do main.py
    print("📦 [VERCEL] Tentando importar main.py...")
    from main import app
    print("✅ [VERCEL] Aplicação importada com sucesso do main.py")
    
    # Configurar caminhos para arquivos estáticos na Vercel
    app.static_folder = os.path.join(root_dir, 'static')
    app.template_folder = os.path.join(root_dir, 'templates')
    
    print(f"📁 [VERCEL] Static folder: {app.static_folder}")
    print(f"📁 [VERCEL] Template folder: {app.template_folder}")
    
    # Verificar se as pastas existem
    if os.path.exists(app.static_folder):
        print("✅ [VERCEL] Pasta static encontrada")
        static_files = []
        for root, dirs, files in os.walk(app.static_folder):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), app.static_folder)
                static_files.append(rel_path)
        print(f"📋 [VERCEL] Arquivos estáticos encontrados: {static_files[:10]}{'...' if len(static_files) > 10 else ''}")
    else:
        print(f"⚠️ [VERCEL] Pasta static não encontrada em: {app.static_folder}")
    
    if os.path.exists(app.template_folder):
        print("✅ [VERCEL] Pasta templates encontrada")
    else:
        print(f"⚠️ [VERCEL] Pasta templates não encontrada em: {app.template_folder}")
    
    # Testar configurações básicas
    print(f"🔧 [VERCEL] Secret key configurado: {bool(app.secret_key)}")
    print(f"🔧 [VERCEL] Debug mode: {app.config.get('DEBUG')}")
    
except Exception as e:
    print(f"⚠️ [VERCEL] Erro ao importar main.py: {e}")
    print(f"📋 [VERCEL] Traceback completo:")
    traceback.print_exc()
    
    # Fallback: importar versão simplificada se houver problema
    try:
        print("🔄 [VERCEL] Tentando fallback para app_test.py...")
        from app_test import app
        print("✅ [VERCEL] Usando app_test.py como fallback")
    except Exception as e2:
        print(f"❌ [VERCEL] Erro crítico: {e2}")
        print(f"📋 [VERCEL] Traceback do fallback:")
        traceback.print_exc()
        
        # Criar app básico de emergência
        from flask import Flask, jsonify
        app = Flask(__name__)
        app.secret_key = 'emergency-key-for-vercel'
        
        @app.route('/')
        def emergency():
            return jsonify({
                'status': 'error', 
                'message': 'Erro de configuração do servidor',
                'error_main': str(e),
                'error_fallback': str(e2)
            })
            
        @app.route('/health')
        def health():
            return jsonify({
                'status': 'emergency_mode',
                'main_error': str(e),
                'fallback_error': str(e2)
            })
            
        print("🚨 [VERCEL] Aplicação de emergência criada")

# Configurar para produção
try:
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    print("🔧 [VERCEL] Configurações de produção aplicadas")
except Exception as e:
    print(f"⚠️ [VERCEL] Erro ao configurar produção: {e}")

# Log de inicialização
print("🚀 [VERCEL] Aplicação iniciada para produção")
try:
    print(f"📋 [VERCEL] Debug: {app.config.get('DEBUG')}")
    print(f"📋 [VERCEL] App name: {app.name}")
    print(f"📋 [VERCEL] Routes disponíveis:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.endpoint}: {rule.rule}")
except Exception as e:
    print(f"⚠️ [VERCEL] Erro ao listar informações do app: {e}")

# Adicionar route de diagnóstico
try:
    @app.route('/api/diagnostico')
    def diagnostico():
        from flask import jsonify
        import sys
        import os
        
        return jsonify({
            'status': 'ok',
            'python_version': sys.version,
            'current_dir': os.getcwd(),
            'environment': {
                'VERCEL': os.environ.get('VERCEL'),
                'FLASK_ENV': os.environ.get('FLASK_ENV'),
                'DEBUG': os.environ.get('DEBUG')
            },
            'app_config': {
                'debug': app.config.get('DEBUG'),
                'testing': app.config.get('TESTING')
            }
        })
    print("✅ [VERCEL] Route de diagnóstico adicionada")
except Exception as e:
    print(f"⚠️ [VERCEL] Erro ao adicionar route de diagnóstico: {e}")

# Exportar app para o Vercel
# O Vercel procura por uma variável chamada 'app'
print("🎯 [VERCEL] App pronto para requisições")

if __name__ == "__main__":
    # Não executar em produção, apenas para testes locais
    print("🧪 [VERCEL] Modo de teste local")
    app.run(debug=False)
