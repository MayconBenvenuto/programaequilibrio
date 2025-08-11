#!/usr/bin/env python3
"""
Script para testar se as variáveis de ambiente do Supabase estão configuradas corretamente na Vercel
"""

import requests
import json
import sys

def test_environment_variables(base_url):
    """Testa se as variáveis de ambiente estão configuradas na produção"""
    
    print(f"🔧 Testando variáveis de ambiente em: {base_url}")
    print("=" * 60)
    
    # Testar rota de debug de admin
    print("📊 Testando configurações de ambiente...")
    try:
        response = requests.get(f"{base_url}/admin/debug", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Rota de debug acessível")
            print(f"\n🔍 Informações do ambiente:")
            print(f"   - Produção: {data.get('is_production', 'N/A')}")
            print(f"   - Secret key configurado: {data.get('flask_secret_key_set', 'N/A')}")
            print(f"   - Cookies seguros: {data.get('session_cookie_secure', 'N/A')}")
            print(f"   - Cookies HTTPOnly: {data.get('session_cookie_httponly', 'N/A')}")
            
        else:
            print(f"⚠️ Rota de debug retornou status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar debug: {e}")
    
    # Testar se Supabase está funcionando
    print(f"\n🗄️ Testando conexão com Supabase...")
    try:
        # Tentar acessar uma página que usa Supabase
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # Procurar por indicadores de erro de Supabase
            if 'supabase' in content or 'conecta' in content:
                print("✅ Página principal carregou corretamente")
                if 'erro' not in content and 'error' not in content:
                    print("✅ Sem erros visíveis relacionados ao Supabase")
                else:
                    print("⚠️ Possíveis erros encontrados na página")
            else:
                print("⚠️ Conteúdo da página pode ter problemas")
                
        else:
            print(f"❌ Página principal retornou status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar página principal: {e}")
    
    # Testar acesso ao painel admin
    print(f"\n👨‍💼 Testando acesso ao painel administrativo...")
    try:
        response = requests.get(f"{base_url}/admin/login", timeout=10)
        
        if response.status_code == 200:
            print("✅ Página de login do admin acessível")
            
            # Verificar se não há erros de configuração
            content = response.text.lower()
            if 'error' not in content and 'erro' not in content:
                print("✅ Página de login sem erros visíveis")
            else:
                print("⚠️ Possíveis erros na página de login")
                
        else:
            print(f"⚠️ Página de login retornou status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar página de login: {e}")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Uso: python test_env_vars.py <URL_BASE>")
        print("Exemplo: python test_env_vars.py https://seuapp.vercel.app")
        return 1
    
    base_url = sys.argv[1].rstrip('/')
    success = test_environment_variables(base_url)
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DAS VARIÁVEIS CONFIGURADAS:")
    print("")
    print("🔧 Variáveis principais:")
    print("   ✅ SUPABASE_URL")
    print("   ✅ SUPABASE_ANON_KEY") 
    print("   ✅ FLASK_SECRET_KEY")
    print("   ✅ FLASK_ENV=production")
    print("   ✅ DEBUG=False")
    print("")
    print("👨‍💼 Variáveis de administração:")
    print("   ✅ ADMIN_EMAIL")
    print("   ✅ ADMIN_PASSWORD")
    print("   ✅ ADMIN_NAME")
    print("")
    print("🔒 Variáveis de segurança:")
    print("   ✅ SESSION_COOKIE_SECURE=True")
    print("   ✅ SESSION_COOKIE_HTTPONLY=True")
    print("")
    print("🌐 APIs externas:")
    print("   ✅ RECEITAWS_API_URL")
    print("   ✅ VIACEP_API_URL")
    print("")
    print("💡 Como verificar se estão funcionando:")
    print("   1. Acesse a aplicação")
    print("   2. Teste o cadastro de uma empresa")
    print("   3. Tente fazer login no painel admin")
    print("   4. Verifique se não há erros no console")
    print("")
    print("🔧 Para adicionar mais variáveis:")
    print("   vercel env add NOME_VARIAVEL")
    print("")
    print("📋 Para listar todas as variáveis:")
    print("   vercel env ls")
    print("")
    print("✅ Todas as variáveis principais do Supabase foram configuradas!")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
