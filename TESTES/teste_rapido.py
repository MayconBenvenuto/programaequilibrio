import requests

url = "https://programaequilibrio-doo09wbtt-mayconbenvenutos-projects.vercel.app"

try:
    response = requests.get(url, timeout=15)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
    
    if response.status_code == 200:
        print("✅ SUCESSO! Aplicação funcionando")
        print(f"Conteúdo: {response.text}")
    elif response.status_code == 401:
        print("❌ Erro 401: Authentication Required")
        print("🔧 Problema de configuração da conta/organização Vercel")
    elif response.status_code == 500:
        print("❌ Erro 500: Internal Server Error")
        print(f"Conteúdo: {response.text[:300]}")
    else:
        print(f"❌ Erro {response.status_code}")
        print(f"Conteúdo: {response.text[:300]}")
        
except Exception as e:
    print(f"Erro: {e}")
