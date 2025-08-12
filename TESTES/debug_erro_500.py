#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Debug do erro 500 específico - Investigação detalhada
"""

import requests
import json
import time

def testar_com_dados_reais():
    """Testa com dados mais próximos do que o frontend real envia"""
    
    print("🔍 DEBUG ERRO 500 - DADOS REAIS")
    print("=" * 60)
    
    # Dados simulando exatamente o que o frontend envia
    dados_teste = {
        'dados_empresa': {
            'cnpj': '11.222.333/0001-81',  # CNPJ válido
            'razao_social': 'EMPRESA TESTE LTDA',
            'nome_fantasia': 'Empresa Teste',
            'rh_responsavel': 'Maria Silva',
            'cargo': 'Gerente de RH',
            'email': 'maria.silva@teste.com',
            'whatsapp': '11999999999',  # Sem formatação
            'num_colaboradores': 50,  # Como número
            'setor': 'Tecnologia',
            'telefone': '1133334444',
            'endereco': {
                'logradouro': 'Rua das Flores, 123',
                'complemento': 'Sala 45',
                'bairro': 'Centro',
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01234567'  # CEP sem formatação
            },
            'atividade_principal': 'Desenvolvimento de software'
        },
        'respostas': {
            '1': ['alta_carga', 'metas_excessivas'],  # Múltiplas respostas
            '2': ['frequencia_moderada'],
            '3': ['programa_basico'],
            '4': ['comunicacao_regular'],
            '5': ['nivel_medio'],
            '6': ['beneficios_tradicionais'],
            '7': ['sistema_basico'],
            '8': ['comunicacao_regular'],
            '9': ['equipamento_adequado'],
            '10': ['treinamento_regular'],
            '11': ['feedback_regular'],
            '12': ['politicas_completas']
        }
    }
    
    try:
        print("📤 Enviando dados de teste...")
        
        response = requests.post(
            "https://programaequilibrio.vercel.app/processar_questionario",
            json=dados_teste,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"⏱️ Tempo: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            resultado = response.json()
            print("✅ SUCESSO!")
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
            
        elif response.status_code == 500:
            print("❌ ERRO 500 - Detalhes:")
            print(f"Headers: {dict(response.headers)}")
            try:
                error_info = response.json()
                print("JSON Error:", json.dumps(error_info, indent=2, ensure_ascii=False))
            except:
                print("Texto do erro:", response.text[:2000])
        else:
            print(f"❌ ERRO {response.status_code}")
            print(response.text[:1000])
            
    except Exception as e:
        print(f"❌ EXCEÇÃO: {e}")

def testar_com_cnpj_invalido():
    """Testa com CNPJ inválido para ver se é isso"""
    
    print("\n" + "=" * 60)
    print("🔍 TESTE COM CNPJ INVÁLIDO")
    print("=" * 60)
    
    dados_teste = {
        'dados_empresa': {
            'cnpj': '11.111.111/0001-11',  # CNPJ inválido
            'razao_social': 'EMPRESA TESTE LTDA',
            'rh_responsavel': 'Maria Silva',
            'cargo': 'Gerente de RH',
            'email': 'maria@teste.com',
            'whatsapp': '11999999999',
            'num_colaboradores': 50,
            'setor': 'Tecnologia'
        },
        'respostas': {
            '1': ['alta_carga'],
            '2': ['frequencia_moderada'],
            '3': ['programa_inexistente'],
            '4': ['comunicacao_deficiente'],
            '5': ['nivel_baixo'],
            '6': ['beneficios_limitados'],
            '7': ['sistema_inexistente'],
            '8': ['comunicacao_limitada'],
            '9': ['equipamento_inadequado'],
            '10': ['treinamento_basico'],
            '11': ['feedback_limitado'],
            '12': ['politicas_basicas']
        }
    }
    
    try:
        response = requests.post(
            "https://programaequilibrio.vercel.app/processar_questionario",
            json=dados_teste,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Resposta: {response.text[:500]}")
        else:
            print("✅ Funcionou com CNPJ inválido!")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")

def testar_com_dados_minimos():
    """Testa com dados mínimos obrigatórios"""
    
    print("\n" + "=" * 60)
    print("🔍 TESTE COM DADOS MÍNIMOS")
    print("=" * 60)
    
    dados_teste = {
        'dados_empresa': {
            'cnpj': '11.222.333/0001-81',
            'rh_responsavel': 'Teste',
            'cargo': 'RH',
            'email': 'teste@teste.com',
            'whatsapp': '11999999999',
            'num_colaboradores': 10,
            'setor': 'Teste'
        },
        'respostas': {
            '1': ['alta_carga'],
            '2': ['frequencia_baixa']
        }
    }
    
    try:
        response = requests.post(
            "https://programaequilibrio.vercel.app/processar_questionario",
            json=dados_teste,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Resposta: {response.text[:500]}")
        else:
            print("✅ Funcionou com dados mínimos!")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")

def main():
    print("🔍 INVESTIGAÇÃO DETALHADA DO ERRO 500")
    print("Testando diferentes cenários para identificar a causa...")
    
    # Teste 1: Dados completos e realistas
    testar_com_dados_reais()
    
    # Teste 2: CNPJ inválido
    testar_com_cnpj_invalido()
    
    # Teste 3: Dados mínimos
    testar_com_dados_minimos()
    
    print("\n" + "=" * 60)
    print("📋 CONCLUSÕES")
    print("=" * 60)
    print("Se algum teste passou, o problema pode estar em:")
    print("- Formato específico dos dados do frontend")
    print("- Validação de campos específicos")
    print("- Timeout de processamento")
    print("- Caracteres especiais nos dados")

if __name__ == "__main__":
    main()
