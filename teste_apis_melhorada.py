import requests
import json
import time

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
            
            # Padronizar formato de retorno
            resultado = {
                'status': 'OK',
                'nome': data.get('legal_name', ''),
                'fantasia': data.get('trade_name', ''),
                'situacao': data.get('registration_status', ''),
                'cnpj': data.get('tax_id', ''),
                'abertura': data.get('founded', ''),
                'tipo': data.get('company_size', ''),
                'natureza_juridica': data.get('legal_nature', ''),
                'porte': data.get('company_size', ''),
                'logradouro': data.get('address', {}).get('street', ''),
                'numero': data.get('address', {}).get('number', ''),
                'complemento': data.get('address', {}).get('details', ''),
                'bairro': data.get('address', {}).get('district', ''),
                'municipio': data.get('address', {}).get('city', ''),
                'uf': data.get('address', {}).get('state', ''),
                'cep': data.get('address', {}).get('zip_code', ''),
                'telefone': data.get('phone', ''),
                'email': data.get('email', ''),
                'atividade_principal': [],
                'atividades_secundarias': []
            }
            
            # Processar atividades
            if 'primary_activity' in data:
                for atividade in data['primary_activity']:
                    resultado['atividade_principal'].append({
                        'code': atividade.get('id', ''),
                        'text': atividade.get('description', '')
                    })
            
            if 'secondary_activity' in data:
                for atividade in data['secondary_activity']:
                    resultado['atividades_secundarias'].append({
                        'code': atividade.get('id', ''),
                        'text': atividade.get('description', '')
                    })
            
            return resultado
            
        elif response.status_code == 429:
            return {'status': 'ERROR', 'message': 'Muitas requisições. Tente novamente em alguns segundos.'}
        else:
            return {'status': 'ERROR', 'message': f'Erro HTTP {response.status_code}'}
            
    except Exception as e:
        return {'status': 'ERROR', 'message': f'Erro na consulta: {str(e)}'}

def consultar_receitaws(cnpj):
    """Consulta CNPJ na ReceitaWS (mantém implementação atual)"""
    try:
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_limpo}"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'ERROR', 'message': f'Erro HTTP {response.status_code}'}
            
    except Exception as e:
        return {'status': 'ERROR', 'message': f'Erro na consulta: {str(e)}'}

def consultar_cnpj_com_fallback(cnpj):
    """
    Consulta CNPJ usando múltiplas APIs como fallback
    1. Tenta BrasilAPI primeiro (mais rápida e sem limite)
    2. Se falhar, usa ReceitaWS
    """
    print(f"Consultando CNPJ: {cnpj}")
    
    # Primeira tentativa: BrasilAPI
    print("Tentativa 1: BrasilAPI...")
    resultado = consultar_brasilapi(cnpj)
    
    if resultado.get('status') == 'OK' and resultado.get('nome'):
        print("✅ Sucesso com BrasilAPI!")
        return resultado
    else:
        print(f"❌ BrasilAPI falhou: {resultado.get('message', 'Dados incompletos')}")
    
    # Segunda tentativa: ReceitaWS
    print("Tentativa 2: ReceitaWS...")
    resultado = consultar_receitaws(cnpj)
    
    if resultado.get('status') == 'OK' and resultado.get('nome'):
        print("✅ Sucesso com ReceitaWS!")
        return resultado
    else:
        print(f"❌ ReceitaWS falhou: {resultado.get('message', 'Dados incompletos')}")
    
    # Se ambas falharam
    return {
        'status': 'ERROR', 
        'message': 'Não foi possível consultar o CNPJ em nenhuma das APIs disponíveis'
    }

def main():
    # Testa com diferentes CNPJs
    cnpjs_teste = [
        "33000167000101",  # Petrobras
        "11222333000181",  # CNPJ fictício
        "33.000.167/0001-01",  # Petrobras com formatação
    ]
    
    for cnpj in cnpjs_teste:
        print(f"\n{'='*60}")
        resultado = consultar_cnpj_com_fallback(cnpj)
        
        if resultado.get('status') == 'OK':
            print(f"Razão Social: {resultado.get('nome', 'N/A')}")
            print(f"Nome Fantasia: {resultado.get('fantasia', 'N/A')}")
            print(f"Situação: {resultado.get('situacao', 'N/A')}")
            print(f"CNPJ: {resultado.get('cnpj', 'N/A')}")
            print(f"Município: {resultado.get('municipio', 'N/A')}")
            print(f"UF: {resultado.get('uf', 'N/A')}")
        else:
            print(f"Erro: {resultado.get('message', 'Erro desconhecido')}")
        
        time.sleep(2)  # Evita rate limiting

if __name__ == "__main__":
    main()
