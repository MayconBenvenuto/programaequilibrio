#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar dashboard com logs detalhados
"""

import requests
import time

def testar_dashboard_completo():
    """Teste completo do dashboard com análise de logs"""
    print("🧪 TESTE COMPLETO DO DASHBOARD COM LOGS")
    print("=" * 60)
    
    base_url = "https://programaequilibrio.vercel.app"
    
    # 1. Testar rota de teste para confirmar deploy
    print("\n1️⃣ TESTANDO DEPLOY...")
    try:
        response = requests.get(f"{base_url}/test/fix")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Deploy confirmado: {data.get('version')} - {data.get('timestamp')}")
        else:
            print(f"❌ Erro no teste de deploy: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar deploy: {e}")
    
    # 2. Login e acesso ao dashboard
    print("\n2️⃣ FAZENDO LOGIN E ACESSANDO DASHBOARD...")
    
    session = requests.Session()
    
    # Login
    try:
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        login_response = session.post(f"{base_url}/admin/login", data=login_data, allow_redirects=False)
        
        if login_response.status_code in [302, 301]:
            print("✅ Login realizado com sucesso")
            
            # Acesso ao dashboard
            dashboard_response = session.get(f"{base_url}/admin/dashboard")
            
            if dashboard_response.status_code == 200:
                print("✅ Dashboard acessado com sucesso")
                
                # Analisar conteúdo do dashboard
                content = dashboard_response.text
                
                print("\n3️⃣ ANÁLISE DO CONTEÚDO:")
                
                # Procurar por indicadores de dados
                if 'total_empresas' in content:
                    print("✅ Variável total_empresas encontrada no HTML")
                else:
                    print("❌ Variável total_empresas NÃO encontrada no HTML")
                
                # Procurar por valores específicos
                if '"total_empresas": 12' in content or '"total_empresas":12' in content:
                    print("✅ Valor 12 empresas encontrado no HTML")
                elif '"total_empresas": 0' in content or '"total_empresas":0' in content:
                    print("⚠️ Valor 0 empresas encontrado no HTML - PROBLEMA!")
                else:
                    print("❓ Valor de empresas não identificado claramente")
                
                # Procurar por erros
                if '"error"' in content:
                    print("⚠️ Possível erro encontrado no HTML")
                    # Extrair o erro
                    import re
                    error_match = re.search(r'"error":\s*"([^"]*)"', content)
                    if error_match:
                        print(f"🚨 ERRO: {error_match.group(1)}")
                
                # Procurar por debug info
                if 'DEBUG - Dados recebidos' in content:
                    print("✅ Debug info encontrada no HTML")
                else:
                    print("❌ Debug info NÃO encontrada no HTML")
                
                # Salvar HTML para análise
                with open('dashboard_debug.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("💾 HTML salvo em 'dashboard_debug.html' para análise")
                
                return True
                
            else:
                print(f"❌ Erro ao acessar dashboard: {dashboard_response.status_code}")
                return False
        
        else:
            print(f"❌ Erro no login: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False

def main():
    print("🔍 ANÁLISE COMPLETA DO PROBLEMA DO DASHBOARD")
    print("=" * 60)
    
    sucesso = testar_dashboard_completo()
    
    if sucesso:
        print(f"\n📋 PRÓXIMOS PASSOS:")
        print(f"1. Abra o navegador em: https://programaequilibrio.vercel.app/admin/login")
        print(f"2. Faça login com admin/admin123")
        print(f"3. Abra o Console do Desenvolvedor (F12)")
        print(f"4. Veja os logs que começam com '🐛 [DEBUG]'")
        print(f"5. Procure por erros que começam com '🚨 [ERROR]'")
        print(f"6. Analise o arquivo 'dashboard_debug.html' criado")
    else:
        print(f"\n❌ Falha no teste. Verifique conexão e credenciais.")

if __name__ == "__main__":
    main()
