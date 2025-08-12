#!/usr/bin/env python3
"""
Teste das rotas com path:cnpj para CNPJs com barras
"""

import requests
import time

def test_routes_with_cnpj():
    """Testa as rotas com CNPJ contendo barras"""
    base_url = "http://127.0.0.1:5000"
    
    # CNPJ de teste que sabemos que existe
    cnpj_teste = "32.997.318/0001-85"
    
    print(f"🧪 TESTANDO ROTAS COM CNPJ: {cnpj_teste}")
    print("=" * 60)
    
    # Teste 1: Rota de detalhes JSON (sem autenticação necessária para o teste)
    print("\n1️⃣ Testando rota de detalhes:")
    try:
        # Usando o CNPJ diretamente (sem encoding)
        url_detalhes = f"{base_url}/admin/empresa_detalhes/{cnpj_teste}"
        print(f"   URL: {url_detalhes}")
        
        response = requests.get(url_detalhes, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Sucesso! Empresa encontrada: {data.get('razao_social', 'N/A')}")
        elif response.status_code == 401:
            print(f"   ⚠️  Erro 401: Acesso negado (precisa de autenticação)")
        elif response.status_code == 404:
            print(f"   ❌ Erro 404: Rota/empresa não encontrada")
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")
    
    # Teste 2: Rota de PDF
    print("\n2️⃣ Testando rota de PDF:")
    try:
        url_pdf = f"{base_url}/admin/exportar_empresa_pdf/{cnpj_teste}"
        print(f"   URL: {url_pdf}")
        
        response = requests.get(url_pdf, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Sucesso! PDF gerado (tamanho: {len(response.content)} bytes)")
        elif response.status_code == 401:
            print(f"   ⚠️  Erro 401: Acesso negado (precisa de autenticação)")
        elif response.status_code == 404:
            print(f"   ❌ Erro 404: Rota/empresa não encontrada")
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")
    
    # Teste 3: Rota de teste (se ainda existir)
    print("\n3️⃣ Testando rota de teste:")
    try:
        url_teste = f"{base_url}/test/exportar_empresa_pdf/{cnpj_teste}"
        print(f"   URL: {url_teste}")
        
        response = requests.get(url_teste, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Sucesso! Teste funcionando")
        elif response.status_code == 404:
            print(f"   ℹ️  Rota de teste não existe (normal)")
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando teste das rotas com path:cnpj...")
    time.sleep(2)  # Aguardar servidor estar pronto
    test_routes_with_cnpj()
    print("\n" + "=" * 60)
    print("✅ Teste concluído!")
