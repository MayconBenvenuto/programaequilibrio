#!/usr/bin/env python3
"""
Teste manual para verificar se as rotas com path:cnpj funcionam
"""

import requests
import json

def teste_rota_cnpj():
    """Teste simples da rota"""
    print("🧪 Testando rota com CNPJ contendo barras...")
    
    # CNPJ conhecido
    cnpj = "32.997.318/0001-85"
    
    # URL da rota (sem encoding - porque usamos <path:cnpj>)
    url = f"http://127.0.0.1:5000/admin/empresa_detalhes/{cnpj}"
    
    print(f"📍 URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"📊 Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCESSO! A rota está funcionando!")
            data = response.json()
            print(f"📄 Empresa: {data.get('razao_social', 'N/A')}")
            
        elif response.status_code == 401:
            print("🔐 Status 401 - Precisa de autenticação (normal)")
            print("✅ SUCESSO! A rota existe e está protegida corretamente!")
            
        elif response.status_code == 404:
            print("❌ Status 404 - Rota não encontrada")
            print("❌ FALHA! A correção não funcionou")
            
        else:
            print(f"⚠️  Status {response.status_code} - Resposta inesperada")
            print(f"📝 Resposta: {response.text[:200]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        
    print("\n" + "="*50)

if __name__ == "__main__":
    teste_rota_cnpj()
    input("Pressione Enter para fechar...")
