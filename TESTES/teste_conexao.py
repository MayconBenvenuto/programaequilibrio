#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Conexão Básica - Programa Equilíbrio
Verifica se a aplicação está funcionando corretamente
"""

import requests
import sys
import os

# URL base da aplicação (ajuste se necessário)
BASE_URL = "http://localhost:5000"

def test_basic_connection():
    """Testa a conexão básica com a aplicação"""
    try:
        print("🧪 Testando conexão básica...")
        response = requests.get(BASE_URL, timeout=10)
        
        if response.status_code == 200:
            print("✅ Aplicação respondendo corretamente!")
            print(f"📊 Status Code: {response.status_code}")
            print(f"📝 Content-Type: {response.headers.get('content-type', 'N/A')}")
            return True
        else:
            print(f"❌ Aplicação retornou status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão! Verifique se a aplicação está rodando.")
        print("💡 Execute: python main.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout na conexão!")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_routes():
    """Testa as rotas principais da aplicação"""
    routes = [
        "/",
        "/questionario",
        "/admin/login"
    ]
    
    print("\n🧪 Testando rotas principais...")
    results = {}
    
    for route in routes:
        try:
            url = BASE_URL + route
            print(f"🔍 Testando: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {route} - OK")
                results[route] = True
            elif response.status_code == 302:
                print(f"🔀 {route} - Redirecionamento (normal para algumas rotas)")
                results[route] = True
            else:
                print(f"❌ {route} - Status {response.status_code}")
                results[route] = False
                
        except Exception as e:
            print(f"❌ {route} - Erro: {e}")
            results[route] = False
    
    return results

def main():
    """Função principal"""
    print("=" * 50)
    print("🧪 TESTE DE CONEXÃO BÁSICA")
    print("=" * 50)
    
    # Teste 1: Conexão básica
    if not test_basic_connection():
        print("\n❌ Falha na conexão básica. Verifique se a aplicação está rodando.")
        sys.exit(1)
    
    # Teste 2: Rotas principais
    route_results = test_routes()
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    total_routes = len(route_results)
    successful_routes = sum(1 for success in route_results.values() if success)
    
    print(f"🎯 Rotas testadas: {total_routes}")
    print(f"✅ Rotas funcionando: {successful_routes}")
    print(f"❌ Rotas com problema: {total_routes - successful_routes}")
    
    if successful_routes == total_routes:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("💡 A aplicação está funcionando corretamente.")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("💡 Verifique os logs acima para detalhes.")
        
        # Mostra rotas com problema
        failed_routes = [route for route, success in route_results.items() if not success]
        if failed_routes:
            print(f"🔍 Rotas com problema: {', '.join(failed_routes)}")

if __name__ == "__main__":
    main()
