#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from validate_docbr import CNPJ

def testar_receita_ws(cnpj):
    """Testa a API da ReceitaWS com um CNPJ específico"""
    cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj_limpo}'
    
    print(f'🔍 Testando CNPJ: {cnpj}')
    print(f'📋 CNPJ limpo: {cnpj_limpo}')
    print(f'🌐 URL: {url}')
    print('-' * 60)
    
    # Primeiro, validar se o CNPJ é válido
    cnpj_validator = CNPJ()
    if not cnpj_validator.validate(cnpj_limpo):
        print(f'❌ CNPJ INVÁLIDO: {cnpj}')
        return False
    else:
        print(f'✅ CNPJ VÁLIDO: {cnpj}')
    
    try:
        print('📡 Fazendo requisição...')
        response = requests.get(url, timeout=15)
        
        print(f'🌐 Status Code: {response.status_code}')
        print(f'📊 Headers: {dict(response.headers)}')
        
        if response.status_code == 200:
            print('✅ Resposta recebida com sucesso!')
            data = response.json()
            
            print('\n📄 Resposta JSON:')
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get('status') == 'ERROR':
                print(f'\n❌ ERRO NA API: {data.get("message", "Erro desconhecido")}')
                return False
            else:
                print('\n✅ Dados da empresa recebidos com sucesso!')
                print(f'📊 Razão Social: {data.get("nome", "N/A")}')
                print(f'🏢 Nome Fantasia: {data.get("fantasia", "N/A")}')
                print(f'📍 Situação: {data.get("situacao", "N/A")}')
                return True
        elif response.status_code == 429:
            print('❌ Limite de requisições excedido (429 - Too Many Requests)')
            print('⏰ Aguarde alguns minutos antes de tentar novamente')
            return False
        else:
            print(f'❌ Erro HTTP: {response.status_code}')
            print(f'📄 Resposta: {response.text}')
            return False
            
    except requests.exceptions.Timeout:
        print('❌ Timeout na requisição (15 segundos)')
        return False
    except requests.exceptions.ConnectionError:
        print('❌ Erro de conexão com a API')
        return False
    except Exception as e:
        print(f'❌ Erro na requisição: {str(e)}')
        return False

def testar_cnpjs_exemplos():
    """Testa alguns CNPJs de exemplo"""
    cnpjs_teste = [
        '11.222.333/0001-81',  # CNPJ válido de exemplo
        '11444777000161',      # Natura (sem formatação)
        '33.000.167/0001-01',  # CNPJ válido
        '00.000.000/0001-91',  # CNPJ válido mas empresa não existe
    ]
    
    print('🧪 === TESTE DE VALIDAÇÃO DE CNPJs ===\n')
    
    for cnpj in cnpjs_teste:
        resultado = testar_receita_ws(cnpj)
        print(f'\n🎯 Resultado para {cnpj}: {"✅ SUCESSO" if resultado else "❌ FALHOU"}')
        print('=' * 80)
        print()

if __name__ == '__main__':
    testar_cnpjs_exemplos()
