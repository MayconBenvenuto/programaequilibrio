import requests

url = "https://programaequilibrio-b96ofix2c-mayconbenvenutos-projects.vercel.app"

try:
    response = requests.get(url, timeout=15)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
    
    if response.status_code == 200:
        print("✅ SUCESSO! Aplicação funcionando")
        if "Programa Equilíbrio" in response.text:
            print("✅ Conteúdo correto detectado")
        else:
            print("⚠️ Conteúdo carregado mas título não encontrado")
            print(f"Primeiros 200 chars: {response.text[:200]}")
    elif response.status_code == 401:
        print("❌ Erro 401: Authentication Required")
    elif response.status_code == 500:
        print("❌ Erro 500: Internal Server Error")
        print(f"Conteúdo: {response.text[:300]}")
    else:
        print(f"❌ Erro {response.status_code}")
        print(f"Conteúdo: {response.text[:300]}")
        
except Exception as e:
    print(f"Erro: {e}")
