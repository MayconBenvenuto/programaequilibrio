#!/usr/bin/env python3
"""
Teste para verificar se a correção do PDF funcionou
"""
import requests

def testar_pdf():
    print("🧪 Testando correção do PDF...")
    
    # URL de teste (rota sem autenticação)
    url = "http://127.0.0.1:5000/test/exportar_empresa_pdf/32.997.318/0001-85"
    
    try:
        print(f"🔗 Acessando: {url}")
        
        # Fazer requisição
        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"📏 Content-Length: {response.headers.get('Content-Length', 'N/A')}")
        
        if response.status_code == 200:
            # Verificar se é realmente um PDF
            if response.content.startswith(b'%PDF'):
                print("✅ PDF gerado com sucesso!")
                print(f"📄 Tamanho do arquivo: {len(response.content)} bytes")
                
                # Salvar arquivo de teste
                with open('teste_pdf_baixado.pdf', 'wb') as f:
                    f.write(response.content)
                print("💾 PDF salvo como 'teste_pdf_baixado.pdf' para verificação")
                
            else:
                print("❌ Resposta não é um PDF válido")
                print(f"🔍 Primeiros 100 caracteres: {response.content[:100]}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"🔍 Resposta: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    testar_pdf()
