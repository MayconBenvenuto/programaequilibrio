#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste do Botão Iniciar Diagnóstico
Programa Equilíbrio - Belz Conecta Saúde
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_fluxo_iniciar_diagnostico():
    """Testa se a validação CNPJ funciona ao clicar no botão Iniciar Diagnóstico"""
    
    print("🚀 TESTANDO FLUXO: INICIAR DIAGNÓSTICO")
    print("=" * 60)
    print(f"🕒 Teste iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🌐 URL base: {BASE_URL}")
    print()
    
    # Aguardar servidor estar pronto
    print("⏳ Aguardando servidor estar pronto...")
    time.sleep(2)
    
    # 1. Testar página inicial
    print("🏠 TESTANDO PÁGINA INICIAL")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # Verificar elementos específicos
            checks = {
                "Carregamento da página": True,
                "Campo CNPJ presente": 'name="cnpj"' in content and 'id="cnpjInput"' in content,
                "Campo Razão Social editável": 'name="razao_social"' in content and 'readonly' not in content.lower(),
                "Botão submit presente": 'type="submit"' in content,
                "Texto 'Iniciar Diagnóstico'": 'Iniciar Diagnóstico' in content,
                "JavaScript de validação": 'validar_cnpj' in content.lower()
            }
            
            print(f"✅ Status: {response.status_code}")
            for check, result in checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check}")
            
            page_ok = all(checks.values())
        else:
            print(f"❌ Erro: Status {response.status_code}")
            page_ok = False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        page_ok = False
    
    print()
    
    # 2. Testar casos de CNPJ
    test_cases = [
        {
            'nome': 'CNPJ Válido',
            'cnpj': '11.222.333/0001-81',
            'esperado': True
        },
        {
            'nome': 'CNPJ Inválido - formato',  
            'cnpj': '11.222.333/0001-99',
            'esperado': False
        },
        {
            'nome': 'CNPJ Incompleto',
            'cnpj': '11.222.333/0001',
            'esperado': False
        }
    ]
    
    api_results = []
    
    for test_case in test_cases:
        print(f"📋 TESTANDO: {test_case['nome']}")
        print("-" * 40)
        print(f"🔍 CNPJ: {test_case['cnpj']}")
        
        try:
            payload = {"cnpj": test_case['cnpj']}
            response = requests.post(f"{BASE_URL}/validar_cnpj", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                is_valid = result.get('valid', False)
                
                if is_valid == test_case['esperado']:
                    print(f"✅ Resultado esperado: {'Válido' if is_valid else 'Inválido'}")
                    if is_valid and 'dados_empresa' in result:
                        print(f"📝 Razão Social: {result['dados_empresa'].get('razao_social', 'N/A')[:50]}...")
                    api_results.append(True)
                else:
                    print(f"❌ Resultado inesperado: {'Válido' if is_valid else 'Inválido'} (esperado: {'Válido' if test_case['esperado'] else 'Inválido'})")
                    api_results.append(False)
                
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                api_results.append(False)
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            api_results.append(False)
        
        print()
    
    # Relatório Final
    print("=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    print(f"🕒 Teste concluído em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    resultados = {
        "Página Inicial": page_ok,
        "API Validação": all(api_results)
    }
    
    print("📋 RESULTADOS:")
    for teste, passou in resultados.items():
        status = "✅ PASSOU" if passou else "❌ FALHOU"
        print(f"   {teste}: {status}")
    
    print()
    
    if all(resultados.values()):
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Botão 'Iniciar Diagnóstico' funcionando corretamente")
        print("✅ Validação CNPJ integrada ao formulário")
        print("🚀 Pronto para teste manual!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Verificar implementação")
    
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print("1. Teste manual: Abra http://localhost:5000")
    print("2. Preencha CNPJ: 11.222.333/0001-81") 
    print("3. Preencha outros campos obrigatórios")
    print("4. Clique em 'Iniciar Diagnóstico'")
    print("5. Verificar se valida CNPJ e vai para questionário")

if __name__ == "__main__":
    test_fluxo_iniciar_diagnostico()
