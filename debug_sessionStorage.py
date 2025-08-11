#!/usr/bin/env python3
"""
Debug do problema no sessionStorage - Programa Equilíbrio
Testa o fluxo completo para identificar o problema
"""

import requests
import json

def testar_fluxo_completo():
    print("🔍 DEBUG DO SESSIONSTORAGE - PROGRAMA EQUILÍBRIO")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 1. Testar página inicial
    print("\n📋 1. TESTANDO PÁGINA INICIAL")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Status: {response.status_code}")
        
        if "CNPJ" in response.text:
            print("✅ Campo CNPJ encontrado")
        else:
            print("❌ Campo CNPJ NÃO encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao acessar página inicial: {e}")
        return
    
    # 2. Testar validação de CNPJ
    print("\n📋 2. TESTANDO VALIDAÇÃO DE CNPJ")
    print("-" * 40)
    
    cnpj_teste = "11.222.333/0001-81"
    dados_form = {
        'cnpj': cnpj_teste,
        'razao_social': 'CAIXA ESCOLAR TESTE',
        'nome_fantasia': 'ESCOLA TESTE',
        'rh_responsavel': 'João Silva',
        'cargo': 'Gerente RH',
        'email': 'joao@teste.com.br',
        'whatsapp': '11999999999',
        'num_colaboradores': '51-100',
        'setor': 'Educação'
    }
    
    try:
        # Simular validação CNPJ (endpoint usado no JavaScript)
        response = requests.post(f"{base_url}/validar_cnpj", 
                               json={'cnpj': cnpj_teste})
        
        print(f"✅ Status validação: {response.status_code}")
        
        if response.status_code == 200:
            dados = response.json()
            print(f"✅ Resposta: {json.dumps(dados, indent=2, ensure_ascii=False)}")
            
            # Verificar estrutura esperada pelo questionário
            print("\n🔍 VERIFICANDO ESTRUTURA DOS DADOS:")
            print(f"  - cnpj_validado: {'✅' if 'cnpj_validado' in dados else '❌'}")
            print(f"  - dados_receita: {'✅' if 'dados_receita' in dados else '❌'}")
            
            if 'dados_receita' in dados:
                receita = dados['dados_receita']
                print(f"  - dados_receita.cnpj: {'✅' if 'cnpj' in receita else '❌'}")
                print(f"  - dados_receita.razao_social: {'✅' if 'razao_social' in receita else '❌'}")
            
        else:
            print(f"❌ Erro na validação: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao validar CNPJ: {e}")
        return
    
    # 3. Simular o que seria salvo no sessionStorage
    print("\n📋 3. SIMULANDO DADOS DO SESSIONSTORAGE")
    print("-" * 40)
    
    # Como seria o objeto salvo no navegador
    dados_sessionstorage = {
        **dados_form,  # Todos os dados do formulário
        **dados,       # Dados da validação
    }
    
    print("📝 Dados que seriam salvos no sessionStorage:")
    print(json.dumps(dados_sessionstorage, indent=2, ensure_ascii=False))
    
    # 4. Testar acesso ao questionário
    print("\n📋 4. TESTANDO PÁGINA DO QUESTIONÁRIO")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/questionario")
        print(f"✅ Status questionário: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página carregou com sucesso")
            
            # Verificar se tem o JavaScript de validação
            if "dadosCarregados.cnpj_validado" in response.text:
                print("✅ JavaScript de validação encontrado")
            else:
                print("❌ JavaScript de validação NÃO encontrado")
                
        else:
            print(f"❌ Erro ao acessar questionário: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao acessar questionário: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 CONCLUSÕES:")
    print("1. Verifique se os dados estão sendo salvos corretamente no sessionStorage")
    print("2. A estrutura deve ter 'cnpj_validado' e 'dados_receita'")
    print("3. Abra o DevTools (F12) e veja o console para erros JavaScript")
    print("4. Verifique a aba Application > Session Storage no DevTools")

if __name__ == "__main__":
    testar_fluxo_completo()
