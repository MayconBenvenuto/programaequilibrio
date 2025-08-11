#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Validação de CNPJ - Programa Equilíbrio
Testa a validação de CNPJ e integração com API ReceitaWS
"""

import requests
import json
import sys
from validate_docbr import CNPJ

# URL base da aplicação
BASE_URL = "http://localhost:5000"

# CNPJs para teste
CNPJS_TESTE = {
    "validos": [
        "11.222.333/0001-81",  # Magazine Luiza
        "07.526.557/0001-00",  # Natura
        "33.000.167/0001-01",  # Itaú
        "11111111000111",      # Formato sem pontuação
    ],
    "invalidos": [
        "12.345.678/0001-00",  # Formato correto mas inválido
        "00.000.000/0000-00",  # CNPJ zerado
        "123.456.789-10",      # Formato incorreto
        "invalid_cnpj",        # Texto inválido
        "",                    # Vazio
    ]
}

def test_cnpj_format_validation():
    """Testa a validação de formato de CNPJ usando validate-docbr"""
    print("🧪 Testando validação de formato de CNPJ...")
    
    cnpj_validator = CNPJ()
    results = {"passed": 0, "failed": 0}
    
    # Teste CNPJs válidos
    print("\n✅ Testando CNPJs com formato válido:")
    for cnpj in CNPJS_TESTE["validos"]:
        is_valid = cnpj_validator.validate(cnpj)
        print(f"   📋 {cnpj} - {'✅ Válido' if is_valid else '❌ Inválido'}")
        if is_valid:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Teste CNPJs inválidos
    print("\n❌ Testando CNPJs com formato inválido:")
    for cnpj in CNPJS_TESTE["invalidos"]:
        is_valid = cnpj_validator.validate(cnpj)
        expected_invalid = not is_valid
        print(f"   📋 {cnpj} - {'✅ Rejeitado corretamente' if expected_invalid else '❌ Aceito incorretamente'}")
        if expected_invalid:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    return results

def test_cnpj_api_validation():
    """Testa a validação de CNPJ via API da aplicação"""
    print("\n🧪 Testando validação via API da aplicação...")
    
    results = {"passed": 0, "failed": 0}
    
    for cnpj in CNPJS_TESTE["validos"][:2]:  # Testa apenas os 2 primeiros para não sobrecarregar
        try:
            print(f"🔍 Testando CNPJ: {cnpj}")
            
            # Faz requisição para a API de validação
            response = requests.post(
                f"{BASE_URL}/validar-cnpj",
                json={"cnpj": cnpj},
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("sucesso"):
                    print(f"   ✅ Validação bem-sucedida")
                    print(f"   📋 Empresa: {data.get('empresa', {}).get('nome', 'N/A')}")
                    print(f"   🏢 Situação: {data.get('empresa', {}).get('situacao', 'N/A')}")
                    results["passed"] += 1
                else:
                    print(f"   ❌ Validação falhou: {data.get('erro', 'Erro desconhecido')}")
                    results["failed"] += 1
            else:
                print(f"   ❌ Status HTTP: {response.status_code}")
                results["failed"] += 1
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Timeout na validação de {cnpj}")
            results["failed"] += 1
        except Exception as e:
            print(f"   ❌ Erro na validação de {cnpj}: {e}")
            results["failed"] += 1
    
    return results

def test_receita_ws_direct():
    """Testa a API da ReceitaWS diretamente"""
    print("\n🧪 Testando API ReceitaWS diretamente...")
    
    cnpj_teste = "11222333000181"  # Magazine Luiza (sem pontuação)
    
    try:
        print(f"🔍 Consultando CNPJ: {cnpj_teste}")
        
        response = requests.get(
            f"https://www.receitaws.com.br/v1/cnpj/{cnpj_teste}",
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                print("✅ API ReceitaWS funcionando!")
                print(f"   📋 Nome: {data.get('nome', 'N/A')}")
                print(f"   🏢 Situação: {data.get('situacao', 'N/A')}")
                print(f"   📅 Abertura: {data.get('abertura', 'N/A')}")
                return True
            else:
                print(f"❌ ReceitaWS retornou erro: {data.get('message', 'Erro desconhecido')}")
                return False
        else:
            print(f"❌ Status HTTP da ReceitaWS: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️ Timeout na consulta à ReceitaWS")
        return False
    except Exception as e:
        print(f"❌ Erro na consulta à ReceitaWS: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 TESTE DE VALIDAÇÃO DE CNPJ")
    print("=" * 60)
    
    all_results = []
    
    # Teste 1: Validação de formato
    format_results = test_cnpj_format_validation()
    all_results.append(("Validação de Formato", format_results))
    
    # Teste 2: API da aplicação
    api_results = test_cnpj_api_validation()
    all_results.append(("API da Aplicação", api_results))
    
    # Teste 3: ReceitaWS direto
    receita_success = test_receita_ws_direct()
    receita_results = {"passed": 1 if receita_success else 0, "failed": 0 if receita_success else 1}
    all_results.append(("API ReceitaWS", receita_results))
    
    # Resumo geral
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES DE CNPJ")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    for test_name, results in all_results:
        passed = results["passed"]
        failed = results["failed"]
        total_passed += passed
        total_failed += failed
        
        status = "✅ PASSOU" if failed == 0 else "❌ FALHOU"
        print(f"🔍 {test_name}: {passed} passou, {failed} falhou - {status}")
    
    print(f"\n🎯 TOTAL GERAL: {total_passed} passou, {total_failed} falhou")
    
    if total_failed == 0:
        print("\n🎉 TODOS OS TESTES DE CNPJ PASSARAM!")
        print("💡 A validação de CNPJ está funcionando perfeitamente.")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("💡 Verifique a configuração da API ReceitaWS e conexão de internet.")

if __name__ == "__main__":
    main()
