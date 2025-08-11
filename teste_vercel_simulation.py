import sys
import os

# Simular ambiente da Vercel
os.environ['VERCEL'] = '1'

# Adicionar path
root_dir = os.path.join(os.path.dirname(__file__), '.')
sys.path.insert(0, root_dir)

# Testar importação como na Vercel
print("=== TESTE SIMULAÇÃO VERCEL ===")
print("Tentando importar main.py...")

try:
    from main import app, validar_cnpj_route
    print("✅ Importação bem-sucedida!")
    
    # Testar o endpoint específico
    with app.test_client() as client:
        print("\n📡 Testando endpoint /validar_cnpj...")
        
        response = client.post('/validar_cnpj', 
                             json={'cnpj': '32.997.318/0001-85'},
                             headers={'Content-Type': 'application/json'})
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print("Resposta:")
            import json
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verificar dados críticos
            print(f"\n🔍 Verificação:")
            print(f"- valid: {data.get('valid')}")
            print(f"- cnpj_validado: {data.get('cnpj_validado')}")
            print(f"- has dados_empresa: {'dados_empresa' in data}")
        else:
            print(f"❌ Erro: {response.data}")
            
except Exception as e:
    print(f"❌ Erro na importação: {e}")
    import traceback
    traceback.print_exc()
