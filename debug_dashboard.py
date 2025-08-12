#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para debug do dashboard em produção
Simula exatamente o que o dashboard faz
"""

import requests
import json

def testar_dashboard_com_login():
    """Testa o dashboard fazendo login primeiro"""
    print("🔐 TESTANDO DASHBOARD COM LOGIN COMPLETO")
    print("=" * 50)
    
    base_url = "https://programaequilibrio.vercel.app"
    
    # Criar sessão para manter cookies
    session = requests.Session()
    
    # 1. Pegar página de login
    try:
        login_page = session.get(f"{base_url}/admin/login", timeout=10)
        print(f"📋 Página de login: {login_page.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar login: {e}")
        return
    
    # 2. Fazer login
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        login_response = session.post(f"{base_url}/admin/login", data=login_data, timeout=10, allow_redirects=False)
        print(f"🔑 Login response: {login_response.status_code}")
        
        if login_response.status_code in [302, 301]:
            print("✅ Login bem-sucedido (redirecionamento)")
        else:
            print(f"❌ Login falhou: {login_response.text[:200]}")
            return
            
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return
    
    # 3. Acessar dashboard após login
    try:
        dashboard_response = session.get(f"{base_url}/admin/dashboard", timeout=10)
        print(f"📊 Dashboard: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            # Procurar pelos dados no HTML
            html_content = dashboard_response.text
            
            # Procurar pelos números nos cards
            if "0" in html_content and "Empresas Atendidas" in html_content:
                print("⚠️ Dashboard ainda mostra 0 empresas")
                
                # Verificar se há dados de JavaScript
                if "var riskData" in html_content:
                    print("✅ Dados de JavaScript encontrados")
                    
                    # Extrair os dados dos gráficos
                    import re
                    risk_match = re.search(r'"alto":\s*(\d+).*"moderado":\s*(\d+).*"baixo":\s*(\d+)', html_content)
                    if risk_match:
                        alto, moderado, baixo = risk_match.groups()
                        print(f"📊 Dados do gráfico de risco: Alto={alto}, Moderado={moderado}, Baixo={baixo}")
                    else:
                        print("❌ Não foi possível extrair dados do gráfico")
                else:
                    print("❌ Dados de JavaScript não encontrados")
            else:
                print("✅ Dashboard pode estar mostrando dados (não encontrou '0')")
                
        else:
            print(f"❌ Erro ao acessar dashboard: {dashboard_response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao acessar dashboard: {e}")

def verificar_deploy():
    """Verifica se o deploy mais recente está ativo"""
    print(f"\n🚀 VERIFICANDO DEPLOY")
    print("=" * 50)
    
    # Testar uma rota simples para ver se há diferenças
    try:
        response = requests.get("https://programaequilibrio.vercel.app/", timeout=10)
        
        # Procurar por indicadores de quando foi feito o último deploy
        if "Dashboard Executivo" in response.text:
            print("✅ Deploy mais recente parece estar ativo")
        else:
            print("⚠️ Pode estar rodando versão antiga")
            
        # Verificar se há erros JavaScript no console (olhando código fonte)
        if "console.error" in response.text:
            print("⚠️ Possíveis erros JavaScript encontrados")
        else:
            print("✅ Sem erros óbvios no JavaScript")
            
    except Exception as e:
        print(f"❌ Erro ao verificar deploy: {e}")

def main():
    print("🧪 DEBUG COMPLETO DO DASHBOARD EM PRODUÇÃO")
    print("=" * 60)
    
    verificar_deploy()
    testar_dashboard_com_login()
    
    print(f"\n🔍 POSSÍVEIS CAUSAS:")
    print(f"1. 🕐 Cache do Vercel ainda não atualizou")
    print(f"2. 🔄 Deploy não aplicou as mudanças")
    print(f"3. 🗃️ Problema de conexão com Supabase em produção")
    print(f"4. 🐛 Erro silencioso no código")
    
    print(f"\n💡 SOLUÇÕES:")
    print(f"1. Aguardar alguns minutos para cache atualizar")
    print(f"2. Fazer novo deploy: vercel --prod")
    print(f"3. Verificar variáveis de ambiente no Vercel")
    print(f"4. Conferir logs do Vercel")

if __name__ == "__main__":
    main()
