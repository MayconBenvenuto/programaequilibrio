import requests
import sys

try:
    resp = requests.get('http://localhost:5000/questionario?cnpj=11222333000181')
    print(f'Status: {resp.status_code}')
    
    if resp.status_code == 200:
        print('✅ Template funcionando!')
        if "Total de perguntas:" in resp.text:
            print('✅ Perguntas carregadas!')
        else:
            print('❌ Perguntas não encontradas')
    else:
        print('❌ Erro no template')
        print('Content preview:', resp.text[:500])
        
except requests.exceptions.ConnectionError:
    print('❌ Servidor não está rodando na porta 5000')
    sys.exit(1)
except Exception as e:
    print(f'❌ Erro: {e}')
    sys.exit(1)
