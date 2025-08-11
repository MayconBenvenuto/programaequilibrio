import sys
sys.path.append('.')

from main import gerar_analise
import json

# Carregar dados de teste
with open('test_dados.json', 'r') as f:
    dados = json.load(f)

print("Dados de entrada:", dados)

try:
    resultado = gerar_analise(dados)
    print("Resultado da análise:", resultado)
    print("Sucesso!")
except Exception as e:
    print("Erro:", e)
    import traceback
    traceback.print_exc()
