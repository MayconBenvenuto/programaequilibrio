import requests
import json

def testar_endpoint():
    """Testa o endpoint /validar_cnpj"""
    print("🧪 TESTANDO ENDPOINT /validar_cnpj")
    print("=" * 40)
    
    try:
        url = "http://localhost:5000/validar_cnpj"
        data = {"cnpj": "33000167000101"}
        
        print(f"📡 Fazendo requisição POST para {url}")
        print(f"Dados: {data}")
        
        response = requests.post(url, json=data, timeout=30)
        
        print(f"Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta recebida:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Erro HTTP: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Servidor não está rodando ou não acessível")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    testar_endpoint()
