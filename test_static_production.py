#!/usr/bin/env python3
"""
Script para testar arquivos estáticos na produção Vercel
"""

import requests
import sys

def test_static_files_production(base_url):
    """Testa se os arquivos estáticos estão sendo servidos na produção"""
    
    print(f"🌐 Testando arquivos estáticos em: {base_url}")
    print("=" * 50)
    
    # Arquivos estáticos para testar
    static_files = [
        '/static/css/style.css',
        '/static/js/main.js', 
        '/static/images/logo-conecta.png'
    ]
    
    # Testar URLs de debug
    debug_urls = [
        '/debug/static',
        '/test/urls'
    ]
    
    results = []
    
    # Testar arquivos estáticos
    print("📁 Testando arquivos estáticos:")
    for file_path in static_files:
        url = base_url + file_path
        try:
            response = requests.get(url, timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            size = len(response.content) if response.status_code == 200 else 0
            print(f"{status} {file_path} - Status: {response.status_code}, Size: {size} bytes")
            
            # Verificar Content-Type para CSS
            if file_path.endswith('.css') and response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'text/css' in content_type or 'text/plain' in content_type:
                    print(f"   ✅ Content-Type: {content_type}")
                else:
                    print(f"   ⚠️ Content-Type: {content_type} (pode estar incorreto)")
                    
        except Exception as e:
            print(f"❌ {file_path} - Erro: {e}")
            results.append(False)
            continue
            
        results.append(response.status_code == 200)
    
    print("\n🔍 Testando URLs de debug:")
    for debug_url in debug_urls:
        url = base_url + debug_url
        try:
            response = requests.get(url, timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {debug_url} - Status: {response.status_code}")
            
            if response.status_code == 200 and debug_url == '/test/urls':
                try:
                    data = response.json()
                    print(f"   URLs geradas:")
                    for key, value in data.items():
                        print(f"     {key}: {value}")
                except:
                    print(f"   Não foi possível parsear JSON")
                    
        except Exception as e:
            print(f"❌ {debug_url} - Erro: {e}")
    
    # Testar página principal para verificar se CSS está carregando
    print(f"\n🏠 Testando página principal:")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Verificar se há referências ao CSS
            css_link_present = 'css/style.css' in content
            logo_present = 'logo-conecta.png' in content
            
            print(f"✅ Página principal carregou")
            print(f"   CSS referenciado: {'✅' if css_link_present else '❌'}")
            print(f"   Logo referenciado: {'✅' if logo_present else '❌'}")
            
            # Verificar se há CSS inline de fallback
            fallback_css = ':root' in content and '--primary-color: #130E54' in content
            print(f"   CSS fallback presente: {'✅' if fallback_css else '❌'}")
            
        else:
            print(f"❌ Página principal - Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Página principal - Erro: {e}")
    
    print("\n" + "=" * 50)
    print("📋 RESUMO:")
    
    css_working = any(results[:1])  # Primeiro é CSS
    if css_working:
        print("✅ CSS está sendo servido corretamente!")
    else:
        print("❌ CSS não está carregando. Verifique a configuração da Vercel.")
        print("💡 O fallback CSS inline deve manter a aparência correta.")
    
    return all(results)

def main():
    if len(sys.argv) != 2:
        print("Uso: python test_static_production.py <URL_BASE>")
        print("Exemplo: python test_static_production.py https://seuapp.vercel.app")
        return 1
    
    base_url = sys.argv[1].rstrip('/')
    success = test_static_files_production(base_url)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
