from flask import Flask, render_template, request, jsonify
import json
import os
import re
from datetime import datetime
import requests
from decouple import config
from validate_docbr import CNPJ
import hashlib
import secrets

app = Flask(__name__)

# Configurações da aplicação usando variáveis de ambiente
app.secret_key = config('FLASK_SECRET_KEY', default='dev-key-change-in-production')
app.config['DEBUG'] = config('DEBUG', default=True, cast=bool)

app.static_folder = 'static'
app.template_folder = 'templates'

# Validador de CNPJ
cnpj_validator = CNPJ()

# APIs externas
RECEITAWS_API_URL = config('RECEITAWS_API_URL', default='https://www.receitaws.com.br/v1/cnpj/')
RECEITAWS_TIMEOUT = config('RECEITAWS_TIMEOUT', default=15, cast=int)

def validar_cnpj(cnpj):
    """Validar se o CNPJ possui formato válido usando validate_docbr"""
    if not cnpj:
        return False
    
    # Remove formatação
    cnpj_limpo = re.sub(r'[^\d]', '', cnpj)
    
    return cnpj_validator.validate(cnpj_limpo)

def consultar_cnpj_receita_ws(cnpj):
    """Consulta dados da empresa na ReceitaWS"""
    try:
        # Remove formatação do CNPJ
        cnpj_limpo = re.sub(r'[^\d]', '', cnpj)
        print(f"🔍 [ReceitaWS] Consultando CNPJ: {cnpj_limpo}")
        
        # Faz a requisição para a API usando timeout configurado
        response = requests.get(f"{RECEITAWS_API_URL}{cnpj_limpo}", timeout=RECEITAWS_TIMEOUT)
        print(f"📡 [ReceitaWS] Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📋 [ReceitaWS] Dados brutos recebidos:")
            print(f"   Status API: {data.get('status', 'N/A')}")
            print(f"   Nome: {data.get('nome', 'N/A')}")
            print(f"   Fantasia: {data.get('fantasia', 'N/A')}")
            print(f"   Situação: {data.get('situacao', 'N/A')}")
            print(f"   Município: {data.get('municipio', 'N/A')}")
            print(f"   UF: {data.get('uf', 'N/A')}")
            
            # Verifica se houve erro na consulta
            if data.get('status') == 'ERROR':
                print(f"❌ [ReceitaWS] API retornou erro: {data.get('message', 'Erro não especificado')}")
                return None
            
            resultado = {
                'razao_social': data.get('nome', ''),
                'nome_fantasia': data.get('fantasia', ''),
                'cnpj': cnpj_limpo,
                'situacao': data.get('situacao', ''),
                'atividade_principal': data.get('atividade_principal', [{}])[0].get('text', '') if data.get('atividade_principal') else '',
                'endereco': {
                    'logradouro': data.get('logradouro', ''),
                    'numero': data.get('numero', ''),
                    'complemento': data.get('complemento', ''),
                    'bairro': data.get('bairro', ''),
                    'municipio': data.get('municipio', ''),
                    'uf': data.get('uf', ''),
                    'cep': data.get('cep', '')
                },
                'telefone': data.get('telefone', ''),
                'email': data.get('email', ''),
                'data_abertura': data.get('abertura', '')
            }
            
            print(f"✅ [ReceitaWS] Dados processados:")
            print(f"   Razão Social: '{resultado.get('razao_social')}'")
            print(f"   Situação: '{resultado.get('situacao')}'")
            print(f"   Tem razão social: {bool(resultado.get('razao_social'))}")
            
            return resultado
        else:
            print(f"❌ [ReceitaWS] Erro HTTP {response.status_code}: {response.text[:200]}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ [ReceitaWS] Erro de requisição: {e}")
        return None
    except Exception as e:
        print(f"❌ [ReceitaWS] Erro geral: {e}")
        return None

def consultar_brasilapi(cnpj):
    """Consulta CNPJ na BrasilAPI com tratamento adequado"""
    try:
        # Remove caracteres especiais do CNPJ
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verifica se tem dados essenciais
            if not data.get('legal_name'):
                return None
            
            # Converte para formato compatível com ReceitaWS
            return {
                'razao_social': data.get('legal_name', ''),
                'nome_fantasia': data.get('trade_name', ''),
                'cnpj': cnpj_limpo,
                'situacao': data.get('registration_status', ''),
                'atividade_principal': '',  # BrasilAPI tem estrutura diferente
                'endereco': {
                    'logradouro': data.get('address', {}).get('street', ''),
                    'numero': data.get('address', {}).get('number', ''),
                    'complemento': data.get('address', {}).get('details', ''),
                    'bairro': data.get('address', {}).get('district', ''),
                    'municipio': data.get('address', {}).get('city', ''),
                    'uf': data.get('address', {}).get('state', ''),
                    'cep': data.get('address', {}).get('zip_code', '')
                },
                'telefone': data.get('phone', ''),
                'email': data.get('email', ''),
                'data_abertura': data.get('founded', '')
            }
            
        return None
            
    except Exception as e:
        print(f"Erro na BrasilAPI: {e}")
        return None

def consultar_cnpj_com_fallback(cnpj):
    """
    Consulta CNPJ usando múltiplas APIs como fallback
    1. Tenta BrasilAPI primeiro (mais rápida e sem limite rigoroso)
    2. Se falhar, usa ReceitaWS
    """
    print(f"🔍 [FALLBACK] Consultando CNPJ: {cnpj}")
    
    # Primeira tentativa: BrasilAPI
    print("📡 [FALLBACK] Tentativa 1: BrasilAPI...")
    resultado = consultar_brasilapi(cnpj)
    
    if resultado and resultado.get('razao_social'):
        print(f"✅ [FALLBACK] Sucesso com BrasilAPI!")
        print(f"   Razão Social encontrada: '{resultado.get('razao_social')}'")
        return resultado
    else:
        print("⚠️ [FALLBACK] BrasilAPI não retornou dados completos")
        if resultado:
            print(f"   Dados BrasilAPI: razao_social='{resultado.get('razao_social')}', situacao='{resultado.get('situacao')}'")
    
    # Segunda tentativa: ReceitaWS
    print("📡 [FALLBACK] Tentativa 2: ReceitaWS...")
    resultado = consultar_cnpj_receita_ws(cnpj)
    
    if resultado and resultado.get('razao_social'):
        print(f"✅ [FALLBACK] Sucesso com ReceitaWS!")
        print(f"   Razão Social encontrada: '{resultado.get('razao_social')}'")
        return resultado
    else:
        print("⚠️ [FALLBACK] ReceitaWS não retornou dados completos")
        if resultado:
            print(f"   Dados ReceitaWS: razao_social='{resultado.get('razao_social')}', situacao='{resultado.get('situacao')}'")
    
    # Se ambas falharam
    print("❌ [FALLBACK] Nenhuma API retornou dados válidos")
    print(f"   BrasilAPI resultado: {type(resultado)}")
    print(f"   ReceitaWS resultado: {type(resultado)}")
    return None

@app.route('/validar_cnpj', methods=['POST'])
def validar_cnpj_route():
    """Endpoint para validar CNPJ e buscar dados da empresa"""
    data = request.get_json()
    cnpj = data.get('cnpj', '').strip()
    
    print(f"\n🔍 [ROUTE] /validar_cnpj chamada")
    print(f"   CNPJ recebido: '{cnpj}'")
    
    if not cnpj:
        print(f"❌ [ROUTE] CNPJ vazio")
        return jsonify({'valid': False, 'message': 'CNPJ é obrigatório'})
    
    # Validar formato do CNPJ
    formato_valido = validar_cnpj(cnpj)
    print(f"📋 [ROUTE] Formato válido: {formato_valido}")
    
    if not formato_valido:
        print(f"❌ [ROUTE] CNPJ com formato inválido")
        return jsonify({'valid': False, 'message': 'CNPJ inválido'})
    
    # Consultar dados usando múltiplas APIs
    print(f"🔍 [ROUTE] Iniciando consulta de dados...")
    dados_empresa = consultar_cnpj_com_fallback(cnpj)
    
    print(f"📊 [ROUTE] Resultado da consulta:")
    print(f"   Dados encontrados: {dados_empresa is not None}")
    
    if dados_empresa:
        print(f"   Razão Social: '{dados_empresa.get('razao_social')}'")
        print(f"   Situação: '{dados_empresa.get('situacao')}'")
        print(f"   CNPJ: '{dados_empresa.get('cnpj')}'")
        print(f"   Município: '{dados_empresa.get('endereco', {}).get('municipio')}'")
    
    if not dados_empresa:
        print(f"❌ [ROUTE] Nenhum dado encontrado")
        return jsonify({'valid': False, 'message': 'CNPJ não encontrado ou erro na consulta'})
    
    situacao = dados_empresa.get('situacao', '').upper()
    print(f"📋 [ROUTE] Verificando situação: '{situacao}'")
    
    if situacao != 'ATIVA':
        print(f"⚠️ [ROUTE] Empresa não ativa: {situacao}")
        return jsonify({
            'valid': False, 
            'message': f'Empresa com situação: {dados_empresa.get("situacao", "INATIVA")}. Apenas empresas ativas podem realizar o diagnóstico.'
        })
    
    resposta = {
        'valid': True,
        'dados_empresa': dados_empresa,
        'cnpj_validado': True,
        'message': 'CNPJ válido e empresa ativa'
    }
    
    print(f"✅ [ROUTE] Sucesso! Retornando dados:")
    print(f"   valid: {resposta['valid']}")
    print(f"   cnpj_validado: {resposta['cnpj_validado']}")
    print(f"   dados_empresa keys: {list(resposta['dados_empresa'].keys())}")
    
    return jsonify(resposta)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionario')
def questionario():
    return render_template('questionario.html')

if __name__ == '__main__':
    # Executar aplicação Flask
    print("🚀 INICIANDO APLICAÇÃO FLASK COM LOGS DETALHADOS")
    print("=" * 60)
    print("📋 Funcionalidades ativas:")
    print("   ✅ Múltiplas APIs (BrasilAPI + ReceitaWS)")
    print("   ✅ Logs detalhados de consulta CNPJ")
    print("   ✅ Sistema de fallback automático")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
