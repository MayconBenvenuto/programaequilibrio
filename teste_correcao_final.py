#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste rápido para verificar se o erro strftime foi corrigido
"""

import requests
import time

def teste_rapido():
    """Teste rápido do dashboard"""
    print("🧪 TESTE RÁPIDO - CORREÇÃO DO ERRO STRFTIME")
    print("=" * 50)
    
    # Aguardar deploy
    print("⏳ Aguardando 10 segundos para deploy propagar...")
    time.sleep(10)
    
    base_url = "https://programaequilibrio.vercel.app"
    session = requests.Session()
    
    # Login
    try:
        login_data = {'username': 'admin', 'password': 'admin123'}
        login_response = session.post(f"{base_url}/admin/login", data=login_data, allow_redirects=False)
        
        if login_response.status_code in [302, 301]:
            print("✅ Login OK")
            
            # Dashboard
            dashboard_response = session.get(f"{base_url}/admin/dashboard")
            
            if dashboard_response.status_code == 200:
                content = dashboard_response.text
                
                print("\n🔍 ANÁLISE DO CONTEÚDO:")
                
                # Verificar se ainda há erro
                if '"error"' in content and 'strftime' in content:
                    print("❌ Ainda há erro strftime")
                    return False
                elif '"error"' not in content:
                    print("✅ Não há mais erros no stats")
                else:
                    print("⚠️ Há erro, mas não é strftime")
                
                # Verificar dados
                if '"total_empresas": 12' in content or '"total_empresas":12' in content:
                    print("✅ SUCESSO! 12 empresas detectadas")
                    return True
                elif '"total_empresas": 0' in content or '"total_empresas":0' in content:
                    print("❌ Ainda mostra 0 empresas")
                    return False
                else:
                    print("❓ Valor de empresas não claro")
                    return False
            else:
                print(f"❌ Dashboard erro: {dashboard_response.status_code}")
                return False
        else:
            print(f"❌ Login erro: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🔧 VERIFICAÇÃO DA CORREÇÃO")
    print("=" * 30)
    
    sucesso = teste_rapido()
    
    if sucesso:
        print(f"\n🎉 CORREÇÃO APLICADA COM SUCESSO!")
        print(f"📊 Dashboard deve mostrar:")
        print(f"   - 12 empresas atendidas")
        print(f"   - 17 diagnósticos realizados")
        print(f"   - Gráficos funcionais")
    else:
        print(f"\n⚠️ Ainda há problemas. Verificar logs adicionais.")

if __name__ == "__main__":
    main()
