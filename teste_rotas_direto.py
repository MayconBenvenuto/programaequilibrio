#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste específico para verificar se as rotas estão funcionando
"""

import requests
from urllib.parse import quote

# Configurações
BASE_URL = "http://localhost:5000"

def testar_rotas_especificas():
    """Testa rotas específicas com dados conhecidos"""
    
    # CNPJs que sabemos que existem no banco
    cnpjs_conhecidos = [
        "32.997.318/0001-85",
        "11.222.333/0001-81"
    ]
    
    session = requests.Session()
    
    print("🧪 TESTE ESPECÍFICO DAS ROTAS")
    print("=" * 35)
    
    for cnpj in cnpjs_conhecidos:
        print(f"\n📋 Testando CNPJ: {cnpj}")
        
        # Codificar CNPJ
        cnpj_encoded = quote(cnpj)
        print(f"🔐 CNPJ codificado: {cnpj_encoded}")
        
        # Testar rota de detalhes (sem autenticação por enquanto)
        detalhes_url = f"{BASE_URL}/admin/empresa_detalhes/{cnpj_encoded}"
        print(f"🌐 URL Detalhes: {detalhes_url}")
        
        # Testar rota de teste (sem autenticação)
        test_url = f"{BASE_URL}/test/exportar_empresa_pdf/{cnpj_encoded}"
        print(f"🧪 URL Teste: {test_url}")
        
        try:
            print("\n--- Testando rota de detalhes ---")
            response = session.get(detalhes_url)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ Dados recebidos com sucesso!")
                    print(f"   - Razão Social: {data.get('razao_social', 'N/A')}")
                    print(f"   - CNPJ: {data.get('cnpj', 'N/A')}")
                except:
                    print("⚠️ Resposta não é JSON válido")
                    print(f"   Conteúdo: {response.text[:200]}...")
            elif response.status_code == 302:
                print("🔄 Redirecionado (provavelmente precisa de login)")
                print(f"   Location: {response.headers.get('Location', 'N/A')}")
            elif response.status_code == 401 or response.status_code == 403:
                print("🔒 Acesso negado (precisa de autenticação)")
            else:
                print(f"❌ Erro: {response.text[:200]}...")
            
            print("\n--- Testando rota de teste ---")
            test_response = session.get(test_url)
            print(f"📊 Status Teste: {test_response.status_code}")
            
            if test_response.status_code == 200:
                try:
                    test_data = test_response.json()
                    print("✅ Rota de teste funcionou!")
                    print(f"   Success: {test_data.get('success', 'N/A')}")
                    if test_data.get('empresa'):
                        empresa = test_data['empresa']
                        print(f"   - Razão Social: {empresa.get('razao_social', 'N/A')}")
                        print(f"   - CNPJ: {empresa.get('cnpj', 'N/A')}")
                except:
                    print("⚠️ Resposta não é JSON válido")
                    print(f"   Conteúdo: {test_response.text[:200]}...")
            else:
                print(f"❌ Erro na rota de teste: {test_response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    testar_rotas_especificas()
