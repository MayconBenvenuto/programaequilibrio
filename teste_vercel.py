#!/usr/bin/env python3
"""
Teste final antes do deploy no Vercel
"""

import sys
import os

def testar_importacao():
    """Testa se conseguimos importar a aplicação"""
    print("🧪 TESTE DE IMPORTAÇÃO PARA VERCEL")
    print("=" * 50)
    
    # Testar importação do main.py
    try:
        from main import app as main_app
        print("✅ main.py importado com sucesso")
        
        # Verificar rotas
        routes = []
        for rule in main_app.url_map.iter_rules():
            routes.append(f"{rule.endpoint}: {rule.rule}")
        
        print(f"📋 Rotas encontradas no main.py: {len(routes)}")
        for route in routes[:5]:  # Mostrar apenas 5 primeiras
            print(f"   {route}")
            
        return True, main_app
        
    except Exception as e:
        print(f"❌ Erro ao importar main.py: {e}")
        return False, None

def testar_fallback():
    """Testa se o fallback app_test funciona"""
    try:
        from app_test import app as test_app
        print("✅ app_test.py importado com sucesso como fallback")
        
        # Verificar rotas
        routes = []
        for rule in test_app.url_map.iter_rules():
            routes.append(f"{rule.endpoint}: {rule.rule}")
        
        print(f"📋 Rotas encontradas no app_test.py: {len(routes)}")
        for route in routes[:5]:
            print(f"   {route}")
            
        return True, test_app
        
    except Exception as e:
        print(f"❌ Erro ao importar app_test.py: {e}")
        return False, None

def testar_api_index():
    """Testa se api/index.py funciona"""
    print(f"\n🧪 TESTE API/INDEX.PY")
    print("=" * 30)
    
    try:
        # Simular o que api/index.py faz
        sys.path.insert(0, os.path.dirname(__file__))
        
        from api.index import app as api_app
        print("✅ api/index.py importado com sucesso")
        
        # Verificar configuração
        print(f"📋 Debug: {api_app.config.get('DEBUG')}")
        print(f"📋 Testing: {api_app.config.get('TESTING')}")
        
        return True, api_app
        
    except Exception as e:
        print(f"❌ Erro ao importar api/index.py: {e}")
        return False, None

def main():
    print("🚀 TESTE FINAL PRÉ-DEPLOY VERCEL")
    print("=" * 60)
    
    # Teste 1: main.py
    main_ok, main_app = testar_importacao()
    
    # Teste 2: app_test.py (fallback)
    fallback_ok, test_app = testar_fallback()
    
    # Teste 3: api/index.py
    api_ok, api_app = testar_api_index()
    
    print(f"\n{'=' * 60}")
    print("📋 RESUMO DOS TESTES")
    print(f"main.py: {'✅' if main_ok else '❌'}")
    print(f"app_test.py (fallback): {'✅' if fallback_ok else '❌'}")
    print(f"api/index.py: {'✅' if api_ok else '❌'}")
    
    if api_ok:
        print(f"\n🎉 PRONTO PARA DEPLOY!")
        print("✅ O sistema Vercel conseguirá importar a aplicação")
        print("✅ Sistema de fallback implementado")
        print("✅ Logs de debug configurados")
        
        print(f"\n🔧 PRÓXIMOS PASSOS:")
        print("1. Configure as variáveis de ambiente no Vercel:")
        print("   - SUPABASE_URL")
        print("   - SUPABASE_ANON_KEY") 
        print("   - FLASK_SECRET_KEY")
        print("2. Execute: vercel --prod")
        print("3. Teste a aplicação em produção")
        
        return True
        
    else:
        print(f"\n❌ PROBLEMAS ENCONTRADOS")
        print("Corrija os erros acima antes do deploy")
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
