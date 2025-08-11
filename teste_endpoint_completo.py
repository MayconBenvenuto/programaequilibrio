import requests
import json

# Testar o endpoint exatamente como o frontend faz
url = "http://127.0.0.1:5000/validar_cnpj"
data = {"cnpj": "32.997.318/0001-85"}

print("=== TESTE COMPLETO DO ENDPOINT ===")
print(f"URL: {url}")
print(f"Dados enviados: {data}")
print()

try:
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print()
    
    if response.status_code == 200:
        response_data = response.json()
        print("Resposta JSON:")
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
        
        print("\nVerificação de campos críticos:")
        print(f"- valid: {response_data.get('valid')}")
        print(f"- cnpj_validado: {response_data.get('cnpj_validado')}")
        print(f"- tem dados_empresa: {'dados_empresa' in response_data}")
        print(f"- message: {response_data.get('message')}")
        
        if 'dados_empresa' in response_data:
            dados = response_data['dados_empresa']
            print(f"- razao_social: {dados.get('razao_social')}")
            print(f"- situacao: {dados.get('situacao')}")
    else:
        print("Erro na requisição:")
        print(response.text)
        
except Exception as e:
    print(f"Erro: {e}")
