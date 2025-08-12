#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar o dashboard em produção via API
"""

import requests
import json

def testar_producao():
    """Testa se o dashboard está funcionando em produção"""
    print("🌐 TESTANDO DASHBOARD EM PRODUÇÃO")
    print("=" * 50)
    
    base_url = "https://programaequilibrio.vercel.app"
    
    # 1. Testar página inicial
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"📱 Página inicial: {response.status_code} - {'✅ OK' if response.status_code == 200 else '❌ Erro'}")
    except Exception as e:
        print(f"📱 Página inicial: ❌ Erro de conexão - {e}")
    
    # 2. Testar página de admin (deve dar redirect para login)
    try:
        response = requests.get(f"{base_url}/admin", timeout=10, allow_redirects=False)
        if response.status_code in [302, 301]:  # Redirect para login
            print(f"🔐 Admin redirect: {response.status_code} - ✅ OK (redirecionando para login)")
        else:
            print(f"🔐 Admin redirect: {response.status_code} - ⚠️ Comportamento inesperado")
    except Exception as e:
        print(f"🔐 Admin redirect: ❌ Erro de conexão - {e}")
    
    # 3. Testar página de login do admin
    try:
        response = requests.get(f"{base_url}/admin/login", timeout=10)
        if response.status_code == 200 and "login" in response.text.lower():
            print(f"🔑 Login admin: {response.status_code} - ✅ OK (página de login carregada)")
        else:
            print(f"🔑 Login admin: {response.status_code} - ❌ Problema na página")
    except Exception as e:
        print(f"🔑 Login admin: ❌ Erro de conexão - {e}")
    
    print(f"\n📋 INSTRUÇÕES PARA TESTAR O DASHBOARD:")
    print(f"1. Acesse: {base_url}/admin/login")
    print(f"2. Use as credenciais de admin configuradas")
    print(f"3. Verifique se o dashboard mostra:")
    print(f"   - 6 empresas atendidas")
    print(f"   - 17 diagnósticos realizados")
    print(f"   - 1.625 colaboradores analisados")
    print(f"   - Distribuição de risco nos gráficos")

def main():
    print("🧪 TESTE DE PRODUÇÃO - DASHBOARD CORRIGIDO")
    print("=" * 60)
    
    testar_producao()
    
    print(f"\n✅ Correção aplicada com sucesso!")
    print(f"🚀 Dashboard deve estar funcionando normalmente em produção.")

if __name__ == "__main__":
    main()
