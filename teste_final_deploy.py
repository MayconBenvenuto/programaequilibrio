"""
Teste final da aplicação antes do deploy
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def teste_completo():
    """Realiza teste completo da aplicação"""
    
    print("🧪 INICIANDO TESTE FINAL ANTES DO DEPLOY")
    print("=" * 50)
    
    # Teste 1: Dependências básicas
    print("\n📦 TESTE 1: Dependências Básicas")
    dependencias_ok = True
    
    try:
        import flask
        print(f"✅ Flask: {flask.__version__ if hasattr(flask, '__version__') else 'OK'}")
    except ImportError:
        print("❌ Flask: ERRO - Dependência crítica!")
        dependencias_ok = False
    
    try:
        from decouple import config
        print("✅ Python-decouple: OK")
    except ImportError:
        print("❌ Python-decouple: ERRO - Dependência crítica!")
        dependencias_ok = False
        
    try:
        import requests
        print("✅ Requests: OK")
    except ImportError:
        print("❌ Requests: ERRO - Dependência crítica!")
        dependencias_ok = False
        
    try:
        from validate_docbr import CNPJ
        print("✅ Validate-docbr: OK")
    except ImportError:
        print("❌ Validate-docbr: ERRO - Dependência crítica!")
        dependencias_ok = False
    
    # Teste 2: Dependências opcionais
    print("\n📦 TESTE 2: Dependências Opcionais")
    
    try:
        import reportlab
        print("✅ ReportLab: Disponível")
    except ImportError:
        print("⚠️ ReportLab: Indisponível (opcional)")
        
    try:
        from supabase import create_client
        print("✅ Supabase: Disponível") 
    except ImportError:
        print("⚠️ Supabase: Indisponível (opcional)")
    
    # Teste 3: Importação da aplicação principal
    print("\n🚀 TESTE 3: Importação da Aplicação Principal")
    
    try:
        from main import app
        print("✅ main.py importado com sucesso!")
        
        # Verificar configurações básicas
        print(f"   - Nome: {app.name}")
        print(f"   - Debug: {app.config.get('DEBUG', 'Não definido')}")
        print(f"   - Secret Key: {'Configurado' if app.secret_key else 'NÃO CONFIGURADO'}")
        
        # Contar routes
        routes_count = len([r for r in app.url_map.iter_rules() if not r.endpoint.startswith('static')])
        print(f"   - Routes: {routes_count} disponíveis")
        
    except Exception as e:
        print(f"❌ ERRO ao importar main.py: {e}")
        dependencias_ok = False
        import traceback
        traceback.print_exc()
    
    # Teste 4: API de entrada do Vercel
    print("\n🌐 TESTE 4: API de Entrada do Vercel")
    
    try:
        sys.path.insert(0, 'api')
        import index as api_index
        print("✅ api/index.py importado com sucesso!")
        
        if hasattr(api_index, 'app'):
            print(f"   - App disponível: {api_index.app.name}")
        else:
            print("❌ Variável 'app' não encontrada no index!")
            dependencias_ok = False
            
    except Exception as e:
        print(f"❌ ERRO ao importar api/index.py: {e}")
        dependencias_ok = False
        import traceback
        traceback.print_exc()
    
    # Resultado final
    print("\n" + "=" * 50)
    if dependencias_ok:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Aplicação pronta para deploy no Vercel")
        return True
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("⚠️ Revisar problemas antes do deploy")
        return False

if __name__ == "__main__":
    sucesso = teste_completo()
    sys.exit(0 if sucesso else 1)
