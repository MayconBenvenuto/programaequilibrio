#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste simples para verificar a codificação/decodificação de CNPJs
"""

import requests
from urllib.parse import quote, unquote

# Configurações
BASE_URL = "http://localhost:5000"

def testar_codificacao_cnpj():
    """Testa diferentes formas de codificar/decodificar CNPJs"""
    
    # CNPJs de teste com diferentes formatos
    cnpjs_teste = [
        "32.997.318/0001-85",
        "11.222.333/0001-44", 
        "45.678.901/0001-23"
    ]
    
    print("🔍 TESTE DE CODIFICAÇÃO DE CNPJs")
    print("=" * 50)
    
    for cnpj in cnpjs_teste:
        print(f"\n📋 CNPJ Original: {cnpj}")
        
        # Testar codificação
        cnpj_encoded = quote(cnpj)
        print(f"🔐 CNPJ Codificado: {cnpj_encoded}")
        
        # Testar decodificação
        cnpj_decoded = unquote(cnpj_encoded)
        print(f"🔓 CNPJ Decodificado: {cnpj_decoded}")
        
        # Verificar se são iguais
        if cnpj == cnpj_decoded:
            print("✅ Codificação/Decodificação OK")
        else:
            print("❌ Erro na codificação/decodificação!")
        
        # Mostrar como ficaria na URL
        url_detalhes = f"{BASE_URL}/admin/empresa_detalhes/{cnpj_encoded}"
        url_pdf = f"{BASE_URL}/admin/exportar_empresa_pdf/{cnpj_encoded}"
        
        print(f"🌐 URL Detalhes: {url_detalhes}")
        print(f"📄 URL PDF: {url_pdf}")

def testar_requisicao_simples():
    """Faz um teste simples de requisição para verificar se o servidor está rodando"""
    
    print(f"\n🚀 TESTANDO CONEXÃO COM SERVIDOR")
    print("=" * 40)
    
    try:
        # Teste simples na página principal
        response = requests.get(BASE_URL, timeout=5)
        
        if response.status_code == 200:
            print("✅ Servidor rodando e acessível")
            return True
        else:
            print(f"⚠️ Servidor respondeu com status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao servidor")
        print("💡 Certifique-se de que o servidor Flask está rodando em http://localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Timeout ao conectar ao servidor")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    print("🧪 TESTE RÁPIDO - FUNCIONALIDADES DE EMPRESAS")
    print("=" * 55)
    
    # Teste 1: Codificação de CNPJs
    testar_codificacao_cnpj()
    
    # Teste 2: Conexão com servidor
    if testar_requisicao_simples():
        print("\n💡 PRÓXIMOS PASSOS:")
        print("1. Execute 'python testar_empresas_funcionalidades.py' para teste completo")
        print("2. Ou acesse http://localhost:5000/admin/empresas manualmente")
        print("3. Teste clicar em 'Ver Detalhes' e 'Exportar PDF'")
    else:
        print("\n🛠️ PARA CORRIGIR:")
        print("1. Execute 'python main.py' em outro terminal")
        print("2. Aguarde o servidor inicializar")
        print("3. Execute este teste novamente")
    
    print(f"\n{'=' * 55}")
    print("🏁 TESTE CONCLUÍDO")

if __name__ == "__main__":
    main()
