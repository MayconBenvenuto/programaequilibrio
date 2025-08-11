import requests
import json
import time

def teste_brasilapi(cnpj):
    """Testa a BrasilAPI"""
    print(f"\n=== Testando BrasilAPI ===")
    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Razão Social: {data.get('company_name', 'N/A')}")
            print(f"Nome Fantasia: {data.get('trade_name', 'N/A')}")
            print(f"Situação: {data.get('registration_status', 'N/A')}")
            print(f"CEP: {data.get('zip_code', 'N/A')}")
            return data
        else:
            print(f"Erro: {response.text}")
            return None
    except Exception as e:
        print(f"Erro na BrasilAPI: {e}")
        return None

def teste_cnpj_ws(cnpj):
    """Testa a CNPJ.ws"""
    print(f"\n=== Testando CNPJ.ws ===")
    try:
        url = f"https://www.cnpj.ws/cnpj/{cnpj}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Razão Social: {data.get('nome', 'N/A')}")
            print(f"Nome Fantasia: {data.get('fantasia', 'N/A')}")
            print(f"Situação: {data.get('situacao', 'N/A')}")
            print(f"CEP: {data.get('cep', 'N/A')}")
            return data
        else:
            print(f"Erro: {response.text}")
            return None
    except Exception as e:
        print(f"Erro na CNPJ.ws: {e}")
        return None

def teste_receitaws(cnpj):
    """Testa a ReceitaWS (atual)"""
    print(f"\n=== Testando ReceitaWS ===")
    try:
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                print(f"Razão Social: {data.get('nome', 'N/A')}")
                print(f"Nome Fantasia: {data.get('fantasia', 'N/A')}")
                print(f"Situação: {data.get('situacao', 'N/A')}")
                print(f"CEP: {data.get('cep', 'N/A')}")
                return data
            else:
                print(f"Erro: {data.get('message', 'Erro desconhecido')}")
                return None
        else:
            print(f"Erro HTTP: {response.text}")
            return None
    except Exception as e:
        print(f"Erro na ReceitaWS: {e}")
        return None

def teste_cnpja(cnpj):
    """Testa a CNPJA (requer token, mas tem versão free)"""
    print(f"\n=== Testando CNPJA ===")
    try:
        url = f"https://api.cnpja.com/office/{cnpj}"
        # Versão gratuita - sem token
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Razão Social: {data.get('company', {}).get('name', 'N/A')}")
            print(f"Nome Fantasia: {data.get('alias', 'N/A')}")
            print(f"Situação: {data.get('status', {}).get('text', 'N/A')}")
            print(f"CEP: {data.get('address', {}).get('zip', 'N/A')}")
            return data
        else:
            print(f"Erro: {response.text}")
            return None
    except Exception as e:
        print(f"Erro na CNPJA: {e}")
        return None

def main():
    # CNPJ da Petrobras para teste
    cnpj = "33000167000101"
    
    print(f"Testando APIs com CNPJ: {cnpj}")
    
    # Testa todas as APIs
    apis = [
        ("BrasilAPI", teste_brasilapi),
        ("CNPJ.ws", teste_cnpj_ws),
        ("ReceitaWS", teste_receitaws),
        ("CNPJA", teste_cnpja)
    ]
    
    resultados = {}
    
    for nome, func in apis:
        resultado = func(cnpj)
        resultados[nome] = resultado
        time.sleep(1)  # Evita rate limiting
    
    print(f"\n=== RESUMO DOS RESULTADOS ===")
    for nome, resultado in resultados.items():
        status = "✅ Funcionou" if resultado else "❌ Falhou"
        print(f"{nome}: {status}")
    
    # Mostra qual API funcionou melhor
    funcionando = [nome for nome, resultado in resultados.items() if resultado]
    if funcionando:
        print(f"\nAPIs funcionando: {', '.join(funcionando)}")
        print(f"Recomendação: Usar {funcionando[0]} como principal")
    else:
        print("\n❌ Nenhuma API funcionou!")

if __name__ == "__main__":
    main()
