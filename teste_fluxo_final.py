#!/usr/bin/env python3
"""
Teste completo do fluxo de validação de CNPJ
"""

import sys
import os
import requests
import json
import time

# Adiciona o diretório principal ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import consultar_cnpj_com_fallback, validar_cnpj

def testar_validacao_completa():
    """Testa o fluxo completo de validação"""
    
    cnpjs_teste = [
        {
            'cnpj': '33000167000101',
            'nome': 'Petrobras (sem formatação)',
            'esperado': True
        },
        {
            'cnpj': '33.000.167/0001-01', 
            'nome': 'Petrobras (com formatação)',
            'esperado': True
        },
        {
            'cnpj': '11222333000181',
            'nome': 'CNPJ válido alternativo',
            'esperado': True
        },
        {
            'cnpj': '12345678000100',
            'nome': 'CNPJ inválido',
            'esperado': False
        }
    ]
    
    print("🧪 TESTE COMPLETO DE VALIDAÇÃO DE CNPJ")
    print("=" * 50)
    
    sucessos = 0
    total = len(cnpjs_teste)
    
    for i, teste in enumerate(cnpjs_teste, 1):
        cnpj = teste['cnpj']
        nome = teste['nome']
        esperado = teste['esperado']
        
        print(f"\n📋 Teste {i}/{total}: {nome}")
        print(f"CNPJ: {cnpj}")
        
        # Primeiro: validar formato
        print("🔍 Etapa 1: Validando formato...")
        formato_valido = validar_cnpj(cnpj)
        print(f"Formato válido: {'✅' if formato_valido else '❌'}")
        
        if formato_valido and esperado:
            # Segundo: consultar dados
            print("🔍 Etapa 2: Consultando dados...")
            dados = consultar_cnpj_com_fallback(cnpj)
            
            if dados and dados.get('razao_social'):
                print(f"✅ Dados encontrados!")
                print(f"   Razão Social: {dados.get('razao_social')}")
                print(f"   Situação: {dados.get('situacao')}")
                print(f"   Município: {dados.get('endereco', {}).get('municipio')}")
                sucessos += 1
            else:
                print(f"❌ Dados não encontrados ou incompletos")
        elif not formato_valido and not esperado:
            print("✅ CNPJ inválido detectado corretamente")
            sucessos += 1
        else:
            print(f"❌ Resultado inesperado")
        
        # Aguarda um pouco entre requisições
        if i < total:
            print("⏳ Aguardando para evitar rate limiting...")
            time.sleep(2)
    
    print(f"\n{'=' * 50}")
    print(f"📊 RESULTADOS FINAIS")
    print(f"Sucessos: {sucessos}/{total}")
    print(f"Taxa de sucesso: {(sucessos/total)*100:.1f}%")
    
    if sucessos == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        return True
    else:
        print("⚠️ Alguns testes falharam")
        return False

def testar_endpoint_api():
    """Testa o endpoint da API diretamente"""
    print(f"\n🌐 TESTANDO ENDPOINT /validar_cnpj")
    print("=" * 40)
    
    # Assumindo que a aplicação está rodando localmente
    base_url = "http://localhost:5000"
    
    try:
        # Testa com CNPJ válido
        cnpj_teste = "33000167000101"
        url = f"{base_url}/validar_cnpj"
        data = {"cnpj": cnpj_teste}
        
        print(f"📡 Fazendo requisição POST para {url}")
        print(f"Dados: {data}")
        
        response = requests.post(url, json=data, timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta recebida:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Erro HTTP: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Aplicação não está rodando localmente")
        print("Para testar o endpoint, execute: python main.py")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🚀 INICIANDO TESTES COMPLETOS")
    print("Testando as melhorias na validação de CNPJ")
    
    # Teste 1: Funções de validação
    teste1_ok = testar_validacao_completa()
    
    # Teste 2: Endpoint da API
    teste2_ok = testar_endpoint_api()
    
    print(f"\n{'=' * 60}")
    print("📋 RESUMO DOS TESTES")
    print(f"Validação de funções: {'✅' if teste1_ok else '❌'}")
    print(f"Endpoint da API: {'✅' if teste2_ok else '⚠️'}")
    
    if teste1_ok:
        print("\n🎉 As melhorias foram implementadas com sucesso!")
        print("💡 Principais melhorias:")
        print("   • Múltiplas APIs (BrasilAPI + ReceitaWS)")
        print("   • Sistema de fallback automático")
        print("   • Melhor tratamento de erros")
        print("   • Logs mais detalhados")
        print("\n🔧 Para aplicar em produção:")
        print("   1. Faça deploy do código atualizado")
        print("   2. Monitore os logs para confirmar funcionamento")
        print("   3. O sistema agora é mais robusto contra falhas de API")
    else:
        print("\n⚠️ Alguns problemas foram encontrados")
        print("Verifique os logs acima para mais detalhes")

if __name__ == "__main__":
    main()
