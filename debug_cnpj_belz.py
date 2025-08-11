import sys
sys.path.append('.')

from main import validar_cnpj, consultar_cnpj_com_fallback
import json

# Testar o CNPJ específico da Belz
cnpj_belz = "32.997.318/0001-85"
cnpj_limpo = "32997318000185"

print("=== TESTE CNPJ BELZ CORRETORA ===")
print(f"CNPJ: {cnpj_belz}")
print(f"CNPJ limpo: {cnpj_limpo}")
print()

print("1. Testando validação de formato:")
formato_ok = validar_cnpj(cnpj_belz)
print(f"   Formato válido: {formato_ok}")
print()

print("2. Testando consulta de dados:")
dados = consultar_cnpj_com_fallback(cnpj_belz)
print(f"   Dados encontrados: {dados is not None}")

if dados:
    print("   Dados retornados:")
    for key, value in dados.items():
        if isinstance(value, dict):
            print(f"   - {key}: {list(value.keys())}")
        else:
            print(f"   - {key}: {value}")
    
    print()
    print("   Situação da empresa:")
    situacao = dados.get('situacao', '')
    print(f"   - situacao: '{situacao}'")
    print(f"   - situacao.upper(): '{situacao.upper()}'")
    print(f"   - é ATIVA: {situacao.upper() == 'ATIVA'}")
else:
    print("   ❌ Nenhum dado foi encontrado!")
    
print("\n=== SIMULAÇÃO DO ENDPOINT /validar_cnpj ===")

# Simular a lógica do endpoint
if not cnpj_belz:
    print("❌ CNPJ vazio")
elif not validar_cnpj(cnpj_belz):
    print("❌ Formato inválido") 
else:
    dados_empresa = consultar_cnpj_com_fallback(cnpj_belz)
    
    if dados_empresa:
        situacao = dados_empresa.get('situacao', '').upper()
        print(f"✅ Dados encontrados, situação: '{situacao}'")
        
        if situacao and situacao != 'ATIVA':
            print(f"❌ Empresa não ativa: {situacao}")
            print("   Resposta: {'valid': False, 'message': 'Empresa não ativa'}")
        else:
            print("✅ Empresa ativa ou situação não definida")
            print("   Resposta: {'valid': True, 'dados_empresa': {...}, 'cnpj_validado': True}")
    else:
        print("⚠️ Dados não encontrados, mas CNPJ é válido")
        print("   Resposta: {'valid': True, 'cnpj_validado': True, 'message': 'CNPJ válido'}")
