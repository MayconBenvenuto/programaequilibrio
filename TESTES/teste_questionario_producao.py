#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste específico para debug do erro 500 no endpoint /processar_questionario
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
import time

# URLs
BASE_URL_PROD = "https://programaequilibrio.vercel.app"
BASE_URL_LOCAL = "http://127.0.0.1:5000"

def testar_questionario_producao():
    """Testa o envio do questionário na produção"""
    
    print("=" * 60)
    print("🧪 TESTE QUESTIONÁRIO - PRODUÇÃO")
    print("=" * 60)
    
    # Dados de exemplo para o teste (estrutura correta)
    dados_teste = {
        'dados_empresa': {
            'cnpj': '11.222.333/0001-81',
            'rh_responsavel': 'Maria Silva',
            'cargo': 'Gerente de RH',
            'email': 'teste@empresa.com',
            'whatsapp': '(11) 99999-9999',
            'num_colaboradores': 50,
            'setor': 'Tecnologia',
            'razao_social': 'Empresa Teste Ltda',
            'nome_fantasia': 'Empresa Teste',
            'endereco': {
                'logradouro': 'Rua Teste, 123',
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01234-567'
            }
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
        print("📤 Enviando dados do questionário...")
        print(f"🔗 URL: {BASE_URL_PROD}/processar_questionario")
        
        # Headers apropriados
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"📋 Dados enviados: {json.dumps(dados_teste, indent=2, ensure_ascii=False)}")
        
        # Fazer a requisição
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL_PROD}/processar_questionario",
            json=dados_teste,
            headers=headers,
            timeout=30
        )
        end_time = time.time()
        
        print(f"⏱️ Tempo de resposta: {end_time - start_time:.2f}s")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Headers de resposta: {dict(response.headers)}")
        
        # Analisar resposta
        if response.status_code == 200:
            try:
                resultado = response.json()
                print("✅ SUCESSO!")
                print(f"📄 Resposta JSON: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
            except Exception as e:
                print("✅ Resposta recebida, mas não é JSON válido")
                print(f"📄 Conteúdo: {response.text[:1000]}...")
        
        elif response.status_code == 500:
            print("❌ ERRO 500 - Internal Server Error")
            print("📄 Conteúdo da resposta:")
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    error_data = response.json()
                    print(json.dumps(error_data, indent=2, ensure_ascii=False))
                else:
                    print(response.text[:2000])
            except:
                print(response.text[:2000])
        
        else:
            print(f"❌ ERRO {response.status_code}")
            print(f"📄 Resposta: {response.text[:1000]}...")
            
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT - Requisição demorou mais que 30 segundos")
    except requests.exceptions.ConnectionError:
        print("🔌 ERRO DE CONEXÃO - Não foi possível conectar ao servidor")
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {str(e)}")
        print(f"❌ Tipo: {type(e).__name__}")

def testar_questionario_local():
    """Testa o mesmo endpoint localmente para comparação"""
    
    print("\n" + "=" * 60)
    print("🏠 TESTE QUESTIONÁRIO - LOCAL")
    print("=" * 60)
    
    # Dados de exemplo para o teste (estrutura correta)
    dados_teste = {
        'dados_empresa': {
            'cnpj': '11.222.333/0001-81',
            'rh_responsavel': 'Maria Silva',
            'cargo': 'Gerente de RH',
            'email': 'teste@empresa.com',
            'whatsapp': '(11) 99999-9999',
            'num_colaboradores': 50,
            'setor': 'Tecnologia',
            'razao_social': 'Empresa Teste Ltda',
            'nome_fantasia': 'Empresa Teste',
            'endereco': {
                'logradouro': 'Rua Teste, 123',
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01234-567'
            }
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
        print("📤 Testando localmente...")
        print(f"🔗 URL: {BASE_URL_LOCAL}/processar_questionario")
        
        # Headers apropriados
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Fazer a requisição
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL_LOCAL}/processar_questionario",
            json=dados_teste,
            headers=headers,
            timeout=10
        )
        end_time = time.time()
        
        print(f"⏱️ Tempo de resposta: {end_time - start_time:.2f}s")
        print(f"📊 Status Code: {response.status_code}")
        
        # Analisar resposta
        if response.status_code == 200:
            try:
                resultado = response.json()
                print("✅ SUCESSO LOCAL!")
                print(f"📄 Resposta JSON: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
            except Exception as e:
                print("✅ Resposta recebida, mas não é JSON válido")
                print(f"📄 Conteúdo: {response.text[:500]}...")
        else:
            print(f"❌ ERRO LOCAL {response.status_code}")
            print(f"📄 Resposta: {response.text[:500]}...")
            
    except requests.exceptions.ConnectionError:
        print("🔌 Servidor local não está rodando")
    except Exception as e:
        print(f"❌ ERRO LOCAL: {str(e)}")

def main():
    print("🧪 DIAGNÓSTICO QUESTIONÁRIO - PRODUÇÃO vs LOCAL")
    print("Este script testa especificamente o endpoint /processar_questionario")
    
    # Testar produção
    testar_questionario_producao()
    
    # Testar local (se disponível)
    testar_questionario_local()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO")
    print("=" * 60)
    print("Se o erro 500 aparecer apenas na produção:")
    print("- Problema com variáveis de ambiente")
    print("- Problema com conexão Supabase")
    print("- Problema com estrutura de dados")
    print("- Problema com timeout")
    
    print("\nSe o erro aparecer também localmente:")
    print("- Problema no código da função")
    print("- Problema na validação dos dados")
    print("- Problema na estrutura do banco")

if __name__ == "__main__":
    main()
