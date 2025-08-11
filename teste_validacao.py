from main import validar_cnpj

print('Testando validação de CNPJ:')
print(f'CNPJ 11.222.333/0001-81 válido: {validar_cnpj("11.222.333/0001-81")}')
print(f'CNPJ 11222333000181 válido: {validar_cnpj("11222333000181")}')
print(f'CNPJ inválido: {validar_cnpj("123456")}')
