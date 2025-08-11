#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE COMPLETO DA APLICAÇÃO EM PRODUÇÃO
Verifica se a aplicação está funcionando corretamente na Vercel
"""

import requests
import json
from datetime import datetime

# URLs para teste
BASE_URL = "https://programaequilibrio-chc4xxsjp-mayconbenvenutos-projects.vercel.app"

def test_basic_connection():
    """Testa conexão básica com a aplicação"""
    print("="*80)
    print("🧪 TESTE DE CONEXÃO BÁSICA")
    print("="*80)
    
    try:
        print(f"🔍 Testando URL: {BASE_URL}")
        
        # Configurar headers mais completos
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = requests.get(BASE_URL, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ Conexão básica: SUCESSO")
            
            # Verificar se é HTML válido
            if 'html' in response.headers.get('content-type', '').lower():
                content = response.text
                if '<title>' in content and 'Programa Equilíbrio' in content:
                    print("✅ Conteúdo HTML válido encontrado")
                    return True
                else:
                    print("⚠️ HTML carregado mas conteúdo não identificado")
            else:
                print("⚠️ Resposta não é HTML")
            
        elif response.status_code == 401:
            print("❌ Erro 401: Não autorizado")
            print("💡 Possível problema de configuração de segurança")
            
        elif response.status_code == 500:
            print("❌ Erro 500: Erro interno do servidor")
            print("💡 Ainda há problemas na aplicação")
            
        else:
            print(f"❌ Erro {response.status_code}: {response.reason}")
        
        return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão: URL inacessível")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout: Aplicação demorou mais que 30s para responder")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_api_endpoints():
    """Testa endpoints específicos da API"""
    print("\n" + "="*80)
    print("🧪 TESTE DE ENDPOINTS DA API")
    print("="*80)
    
    endpoints = [
        ("/", "Página inicial"),
        ("/questionario", "Página do questionário"),
        ("/admin/login", "Login administrativo"),
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        try:
            url = BASE_URL + endpoint
            print(f"\n🔍 Testando: {description} ({endpoint})")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ {description}: OK")
                results[endpoint] = "OK"
            elif response.status_code == 404:
                print(f"⚠️ {description}: Não encontrado")
                results[endpoint] = "NOT_FOUND"
            else:
                print(f"❌ {description}: Erro {response.status_code}")
                results[endpoint] = f"ERROR_{response.status_code}"
                
        except Exception as e:
            print(f"❌ {description}: Erro na conexão - {e}")
            results[endpoint] = "CONNECTION_ERROR"
    
    return results

def test_cnpj_validation():
    """Testa validação de CNPJ"""
    print("\n" + "="*80)
    print("🧪 TESTE DE VALIDAÇÃO DE CNPJ")
    print("="*80)
    
    try:
        url = BASE_URL + "/validar_cnpj"
        
        # CNPJ de teste (formato válido)
        test_data = {
            "cnpj": "11.222.333/0001-81"
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"🔍 Testando endpoint: {url}")
        print(f"📊 Dados enviados: {test_data}")
        
        response = requests.post(url, json=test_data, headers=headers, timeout=15)
        
        print(f"📈 Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ Resposta JSON válida: {result}")
                return True
            except:
                print("⚠️ Resposta não é JSON válido")
                return False
        else:
            print(f"❌ Erro na validação CNPJ: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste CNPJ: {e}")
        return False

def generate_test_report(basic_ok, endpoints_results, cnpj_ok):
    """Gera relatório de teste"""
    print("\n" + "="*80)
    print("📊 RELATÓRIO FINAL DOS TESTES")
    print("="*80)
    
    print(f"🕒 Teste realizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🌐 URL testada: {BASE_URL}")
    print("")
    
    # Status geral
    total_tests = 1 + len(endpoints_results) + 1  # básico + endpoints + cnpj
    passed_tests = 0
    
    print("📋 RESULTADOS DETALHADOS:")
    
    # Teste básico
    if basic_ok:
        print("✅ Conexão básica: PASSOU")
        passed_tests += 1
    else:
        print("❌ Conexão básica: FALHOU")
    
    # Endpoints
    for endpoint, result in endpoints_results.items():
        if result == "OK":
            print(f"✅ Endpoint {endpoint}: PASSOU")
            passed_tests += 1
        else:
            print(f"❌ Endpoint {endpoint}: {result}")
    
    # CNPJ
    if cnpj_ok:
        print("✅ Validação CNPJ: PASSOU")
        passed_tests += 1
    else:
        print("❌ Validação CNPJ: FALHOU")
    
    print("")
    print("📊 RESUMO:")
    print(f"   Total de testes: {total_tests}")
    print(f"   Testes passaram: {passed_tests}")
    print(f"   Testes falharam: {total_tests - passed_tests}")
    print(f"   Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("")
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Aplicação funcionando corretamente em produção")
        return True
    else:
        print("")
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Revisar configuração da aplicação")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DA APLICAÇÃO EM PRODUÇÃO")
    print(f"🎯 Alvo: {BASE_URL}")
    print("")
    
    # Executar testes
    basic_ok = test_basic_connection()
    endpoints_results = test_api_endpoints()
    cnpj_ok = test_cnpj_validation()
    
    # Gerar relatório
    all_passed = generate_test_report(basic_ok, endpoints_results, cnpj_ok)
    
    return all_passed

if __name__ == "__main__":
    main()
