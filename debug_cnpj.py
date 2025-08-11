import requests
import json
import time

print("🔍 TESTE DE DEBUGGING - CNPJ E SESSIONSTORAGE")
print("=" * 60)

# Testar validação CNPJ
cnpj_teste = "11222333000181"
print(f"🏢 Testando CNPJ: {cnpj_teste}")

response = requests.post(
    "http://localhost:5000/validar_cnpj", 
    headers={"Content-Type": "application/json"},
    json={"cnpj": cnpj_teste}
)

print(f"📊 Status da validação: {response.status_code}")
print(f"📋 Resposta da API:")

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    print("\n🔍 SIMULANDO DADOS DO SESSIONSTORAGE:")
    print("=" * 40)
    
    # Simular os dados que seriam salvos no sessionStorage
    dados_form = {
        "cnpj": cnpj_teste,
        "razao_social": "Teste Empresa Ltda",
        "nome_fantasia": "Teste",
        "rh_responsavel": "João Silva", 
        "cargo": "Gerente RH",
        "email": "joao@teste.com.br",
        "whatsapp": "(11) 99999-9999",
        "num_colaboradores": "51-100",
        "setor": "Tecnologia"
    }
    
    # Adicionar dados da ReceitaWS (se válido)
    if data.get('valid'):
        dados_form['dados_receita'] = data.get('dados_empresa', {})
        dados_form['cnpj_validado'] = True
    
    print("Dados que seriam salvos no sessionStorage:")
    print(json.dumps(dados_form, indent=2, ensure_ascii=False))
    
    print("\n✅ VERIFICAÇÕES:")
    print(f"cnpj_validado: {dados_form.get('cnpj_validado')}")
    print(f"dados_receita existe: {'dados_receita' in dados_form}")
    print(f"dados_receita tem conteúdo: {bool(dados_form.get('dados_receita'))}")
    
    if dados_form.get('dados_receita'):
        receita = dados_form.get('dados_receita')
        print(f"dados_receita.razao_social: {receita.get('razao_social')}")
        print(f"dados_receita.cnpj: {receita.get('cnpj')}")
        
else:
    print(f"❌ Erro na validação: {response.text}")
