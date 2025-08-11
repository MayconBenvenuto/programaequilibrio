#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste do Novo Fluxo de Validação CNPJ
Programa Equilíbrio - Belz Conecta Saúde
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"
CNPJ_TESTE = "11.222.333/0001-81"

def test_fluxo_completo():
    """Testa o fluxo completo: página inicial → validação CNPJ → questionário"""
    
    print("🚀 TESTANDO NOVO FLUXO DE VALIDAÇÃO CNPJ")
    print("=" * 60)
    print(f"🕒 Teste iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🌐 URL base: {BASE_URL}")
    print(f"📋 CNPJ de teste: {CNPJ_TESTE}")
    print()
    
    # Aguardar servidor estar pronto
    print("⏳ Aguardando servidor estar pronto...")
    time.sleep(3)
    
    resultados = {}
    
    # 1. Testar página inicial
    print("🏠 TESTANDO PÁGINA INICIAL")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            checks = {
                "Carregamento da página": True,
                "Campo CNPJ presente": 'id="cnpjInput"' in content,
                "Botão validar CNPJ": 'id="validarCnpjBtn"' in content,
                "Campos readonly inicialmente": 'readonly' in content,
                "Script de validação": 'validarCnpjBtn' in content
            }
            
            print(f"✅ Status: {response.status_code}")
            for check, result in checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check}")
            
            resultados["Página Inicial"] = all(checks.values())
        else:
            print(f"❌ Erro: Status {response.status_code}")
            resultados["Página Inicial"] = False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        resultados["Página Inicial"] = False
    
    print()
    
    # 2. Testar validação CNPJ via API
    print("📋 TESTANDO VALIDAÇÃO DE CNPJ")
    print("-" * 40)
    
    try:
        payload = {"cnpj": CNPJ_TESTE}
        response = requests.post(f"{BASE_URL}/validar_cnpj", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            checks = {
                "Resposta válida": result.get('valid', False),
                "Dados empresa presentes": 'dados_empresa' in result,
                "Razão social preenchida": bool(result.get('dados_empresa', {}).get('razao_social')),
                "CNPJ formatado": bool(result.get('dados_empresa', {}).get('cnpj'))
            }
            
            print(f"✅ Status: {response.status_code}")
            for check, result_check in checks.items():
                status = "✅" if result_check else "❌"
                print(f"{status} {check}")
            
            if result.get('valid'):
                print(f"📝 Razão Social: {result['dados_empresa'].get('razao_social', 'N/A')}")
                print(f"📝 CNPJ: {result['dados_empresa'].get('cnpj', 'N/A')}")
                print(f"📝 Situação: {result['dados_empresa'].get('situacao', 'N/A')}")
            
            resultados["Validação CNPJ"] = all(checks.values())
        else:
            print(f"❌ Erro: Status {response.status_code}")
            print(f"📄 Resposta: {response.text[:200]}")
            resultados["Validação CNPJ"] = False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        resultados["Validação CNPJ"] = False
    
    print()
    
    # 3. Testar página de questionário (deve funcionar sem validação dupla)
    print("❓ TESTANDO PÁGINA QUESTIONÁRIO")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/questionario", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            checks = {
                "Página carregou": True,
                "Estrutura de etapas": 'pergunta-container' in content,
                "Perguntas presentes": 'data-pergunta=' in content,
                "JavaScript presente": 'DOMContentLoaded' in content,
                "Seção dados empresa": 'id="dadosEmpresa"' in content
            }
            
            print(f"✅ Status: {response.status_code}")
            for check, result in checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check}")
            
            resultados["Página Questionário"] = all(checks.values())
        else:
            print(f"❌ Erro: Status {response.status_code}")
            resultados["Página Questionário"] = False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        resultados["Página Questionário"] = False
    
    print()
    
    # Relatório Final
    print("=" * 60)
    print("📊 RELATÓRIO FINAL DO NOVO FLUXO")
    print("=" * 60)
    print(f"🕒 Teste concluído em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    print("📋 RESULTADOS:")
    for teste, passou in resultados.items():
        status = "✅ PASSOU" if passou else "❌ FALHOU"
        print(f"   {teste}: {status}")
    
    print()
    
    total_testes = len(resultados)
    testes_aprovados = sum(resultados.values())
    taxa_sucesso = (testes_aprovados / total_testes) * 100
    
    print("📊 RESUMO:")
    print(f"   Total de testes: {total_testes}")
    print(f"   Testes aprovados: {testes_aprovados}")
    print(f"   Testes reprovados: {total_testes - testes_aprovados}")
    print(f"   Taxa de sucesso: {taxa_sucesso:.1f}%")
    print()
    
    if taxa_sucesso == 100:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Novo fluxo funcionando corretamente")
        print("🚀 Pronto para deploy!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Verificar problemas antes do deploy")
    
    return taxa_sucesso == 100

if __name__ == "__main__":
    test_fluxo_completo()
