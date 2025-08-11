#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das APIs Externas - Programa Equilíbrio
Testa integração com APIs externas (ReceitaWS, ViaCEP, etc.)
"""

import requests
import time
import json
import sys

def test_receita_ws():
    """Testa a API da ReceitaWS"""
    print("🧪 Testando API ReceitaWS...")
    
    cnpjs_teste = [
        "11222333000181",  # Magazine Luiza
        "07526557000100",  # Natura
    ]
    
    results = {"passed": 0, "failed": 0}
    
    for cnpj in cnpjs_teste:
        try:
            print(f"🔍 Consultando CNPJ: {cnpj}")
            
            response = requests.get(
                f"https://www.receitaws.com.br/v1/cnpj/{cnpj}",
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "OK":
                    print(f"   ✅ Consulta bem-sucedida")
                    print(f"   📋 Nome: {data.get('nome', 'N/A')}")
                    print(f"   🏢 Situação: {data.get('situacao', 'N/A')}")
                    print(f"   📍 Cidade: {data.get('municipio', 'N/A')}/{data.get('uf', 'N/A')}")
                    results["passed"] += 1
                else:
                    print(f"   ❌ ReceitaWS retornou erro: {data.get('message', 'Erro desconhecido')}")
                    results["failed"] += 1
            else:
                print(f"   ❌ Status HTTP: {response.status_code}")
                results["failed"] += 1
            
            # Aguarda um pouco entre consultas para evitar rate limit
            time.sleep(2)
            
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Timeout na consulta do CNPJ {cnpj}")
            results["failed"] += 1
        except requests.exceptions.ConnectionError:
            print(f"   🌐 Erro de conexão para CNPJ {cnpj}")
            results["failed"] += 1
        except Exception as e:
            print(f"   ❌ Erro inesperado para CNPJ {cnpj}: {e}")
            results["failed"] += 1
    
    return results

def test_via_cep():
    """Testa a API do ViaCEP"""
    print("\n🧪 Testando API ViaCEP...")
    
    ceps_teste = [
        "01310-100",  # Av. Paulista, São Paulo
        "20040020",   # Centro, Rio de Janeiro
        "30112000",   # Centro, Belo Horizonte
    ]
    
    results = {"passed": 0, "failed": 0}
    
    for cep in ceps_teste:
        try:
            # Remove pontuação do CEP
            cep_clean = cep.replace("-", "").replace(".", "")
            print(f"🔍 Consultando CEP: {cep}")
            
            response = requests.get(
                f"https://viacep.com.br/ws/{cep_clean}/json/",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get("erro"):
                    print(f"   ✅ Consulta bem-sucedida")
                    print(f"   📍 Endereço: {data.get('logradouro', 'N/A')}")
                    print(f"   🏘️ Bairro: {data.get('bairro', 'N/A')}")
                    print(f"   🏙️ Cidade: {data.get('localidade', 'N/A')}/{data.get('uf', 'N/A')}")
                    results["passed"] += 1
                else:
                    print(f"   ❌ CEP não encontrado: {cep}")
                    results["failed"] += 1
            else:
                print(f"   ❌ Status HTTP: {response.status_code}")
                results["failed"] += 1
            
            # Pequena pausa entre consultas
            time.sleep(1)
            
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Timeout na consulta do CEP {cep}")
            results["failed"] += 1
        except requests.exceptions.ConnectionError:
            print(f"   🌐 Erro de conexão para CEP {cep}")
            results["failed"] += 1
        except Exception as e:
            print(f"   ❌ Erro inesperado para CEP {cep}: {e}")
            results["failed"] += 1
    
    return results

def test_internet_connectivity():
    """Testa conectividade geral com a internet"""
    print("\n🧪 Testando conectividade com internet...")
    
    test_sites = [
        "https://www.google.com",
        "https://httpbin.org/status/200",
        "https://jsonplaceholder.typicode.com/posts/1"
    ]
    
    results = {"passed": 0, "failed": 0}
    
    for site in test_sites:
        try:
            print(f"🔍 Testando conectividade: {site}")
            
            response = requests.get(site, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Conectividade OK")
                results["passed"] += 1
            else:
                print(f"   ❌ Status HTTP: {response.status_code}")
                results["failed"] += 1
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Timeout")
            results["failed"] += 1
        except requests.exceptions.ConnectionError:
            print(f"   🌐 Erro de conexão")
            results["failed"] += 1
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            results["failed"] += 1
    
    return results

def test_api_response_time():
    """Testa tempo de resposta das APIs"""
    print("\n🧪 Testando tempo de resposta das APIs...")
    
    apis_teste = [
        ("ReceitaWS", "https://www.receitaws.com.br/v1/cnpj/11222333000181"),
        ("ViaCEP", "https://viacep.com.br/ws/01310100/json/"),
    ]
    
    results = []
    
    for api_name, url in apis_teste:
        try:
            print(f"⏱️ Testando velocidade da {api_name}...")
            
            start_time = time.time()
            response = requests.get(url, timeout=30)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200:
                print(f"   ✅ {api_name}: {response_time:.2f} segundos")
                
                if response_time < 5:
                    print(f"   🚀 Resposta rápida!")
                elif response_time < 10:
                    print(f"   ⚡ Resposta aceitável")
                else:
                    print(f"   🐌 Resposta lenta")
                
                results.append((api_name, True, response_time))
            else:
                print(f"   ❌ {api_name}: Status {response.status_code}")
                results.append((api_name, False, response_time))
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️ {api_name}: Timeout (>30s)")
            results.append((api_name, False, 30.0))
        except Exception as e:
            print(f"   ❌ {api_name}: Erro - {e}")
            results.append((api_name, False, 0.0))
        
        time.sleep(1)
    
    return results

def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 TESTE DE APIs EXTERNAS")
    print("=" * 60)
    
    all_results = []
    
    # Teste 1: Conectividade
    print("📡 Verificando conectividade básica...")
    connectivity = test_internet_connectivity()
    all_results.append(("Conectividade", connectivity))
    
    # Se não há conectividade, não adianta testar APIs específicas
    if connectivity["passed"] == 0:
        print("\n❌ SEM CONECTIVIDADE COM INTERNET!")
        print("💡 Verifique sua conexão e tente novamente.")
        return
    
    # Teste 2: ReceitaWS
    receita_results = test_receita_ws()
    all_results.append(("ReceitaWS", receita_results))
    
    # Teste 3: ViaCEP
    cep_results = test_via_cep()
    all_results.append(("ViaCEP", cep_results))
    
    # Teste 4: Tempo de resposta
    print("\n" + "=" * 40)
    response_times = test_api_response_time()
    
    # Resumo geral
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES DE API")
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
    
    # Resumo de tempo de resposta
    print(f"\n⏱️ TEMPO DE RESPOSTA:")
    for api_name, success, response_time in response_times:
        status = "✅" if success else "❌"
        print(f"   {status} {api_name}: {response_time:.2f}s")
    
    print(f"\n🎯 TOTAL GERAL: {total_passed} passou, {total_failed} falhou")
    
    if total_failed == 0:
        print("\n🎉 TODAS AS APIs ESTÃO FUNCIONANDO!")
        print("💡 O sistema pode fazer consultas externas normalmente.")
    else:
        print("\n⚠️ ALGUMAS APIs APRESENTARAM PROBLEMAS!")
        print("💡 Verifique a conectividade e tente novamente mais tarde.")
        
        # Dicas específicas
        if any("ReceitaWS" in name for name, results in all_results if results["failed"] > 0):
            print("🔍 ReceitaWS: Pode estar temporariamente indisponível ou com rate limit")
        
        if any("ViaCEP" in name for name, results in all_results if results["failed"] > 0):
            print("🔍 ViaCEP: Verifique se os CEPs de teste são válidos")

if __name__ == "__main__":
    main()
