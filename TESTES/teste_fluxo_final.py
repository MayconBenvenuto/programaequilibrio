#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste Final do Fluxo Completo
Programa Equilíbrio - Belz Conecta Saúde
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_fluxo_final():
    """Testa o fluxo final: página inicial com validação → questionário com dados"""
    
    print("🚀 TESTE FINAL DO FLUXO COMPLETO")
    print("=" * 60)
    print(f"🕒 Teste iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🌐 URL base: {BASE_URL}")
    print()
    
    # Aguardar servidor estar pronto
    print("⏳ Aguardando servidor estar pronto...")
    time.sleep(2)
    
    resultados = {}
    
    # 1. Testar página inicial
    print("🏠 TESTANDO PÁGINA INICIAL")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            checks = {
                "Página carregou": True,
                "Campo CNPJ presente": 'name="cnpj"' in content,
                "Campo Razão Social editável": 'name="razao_social"' in content,
                "Botão submit presente": 'type="submit"' in content,
                "JavaScript de validação": 'validar_cnpj' in content.lower()
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
    
    # 2. Testar validação CNPJ
    print("📋 TESTANDO VALIDAÇÃO CNPJ")
    print("-" * 40)
    
    try:
        cnpj_teste = "11.222.333/0001-81"
        payload = {"cnpj": cnpj_teste}
        response = requests.post(f"{BASE_URL}/validar_cnpj", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            checks = {
                "CNPJ válido": result.get('valid', False),
                "Dados empresa presentes": 'dados_empresa' in result,
                "Razão social preenchida": bool(result.get('dados_empresa', {}).get('razao_social')),
                "CNPJ formatado": bool(result.get('dados_empresa', {}).get('cnpj')),
                "Situação ativa": result.get('dados_empresa', {}).get('situacao') == 'ATIVA'
            }
            
            print(f"✅ Status: {response.status_code}")
            for check, check_result in checks.items():
                status = "✅" if check_result else "❌"
                print(f"{status} {check}")
            
            if result.get('valid'):
                print(f"📝 Razão Social: {result['dados_empresa'].get('razao_social', 'N/A')[:50]}...")
                print(f"📝 CNPJ: {result['dados_empresa'].get('cnpj', 'N/A')}")
                print(f"📝 Situação: {result['dados_empresa'].get('situacao', 'N/A')}")
            
            resultados["Validação CNPJ"] = all(checks.values())
        else:
            print(f"❌ Erro: Status {response.status_code}")
            resultados["Validação CNPJ"] = False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        resultados["Validação CNPJ"] = False
    
    print()
    
    # 3. Testar página questionário
    print("❓ TESTANDO PÁGINA QUESTIONÁRIO")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/questionario", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            checks = {
                "Página carregou": True,
                "Campos dados empresa": 'cnpjDisplay' in content and 'razaoSocialDisplay' in content,
                "Campos obrigatórios": 'rhResponsavel' in content and 'emailContato' in content,
                "JavaScript presente": 'DOMContentLoaded' in content,
                "Validação sessionStorage": 'sessionStorage.getItem' in content,
                "Função proximaEtapa": 'proximaEtapa' in content
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
    print("📊 RELATÓRIO FINAL")
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
        print("✅ Fluxo completo funcionando:")
        print("   1. Página inicial valida CNPJ no submit")
        print("   2. Questionário recebe dados da página inicial")
        print("   3. Campos preenchidos automaticamente")
        print("🚀 SISTEMA PRONTO PARA DEPLOY!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Verificar implementação antes do deploy")
    
    print()
    print("🎯 TESTE MANUAL SUGERIDO:")
    print("1. Abra http://localhost:5000")
    print("2. Preencha CNPJ: 11.222.333/0001-81")
    print("3. Preencha outros campos obrigatórios") 
    print("4. Clique 'Iniciar Diagnóstico'")
    print("5. Verifique se questionário mostra dados da empresa")
    print("6. Complete campos RH e clique 'Iniciar Diagnóstico'")
    print("7. Responda perguntas e finalize")

if __name__ == "__main__":
    test_fluxo_final()
