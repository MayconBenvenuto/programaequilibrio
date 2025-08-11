#!/usr/bin/env python3
"""
Script de teste para verificar configurações antes do deploy na Vercel
"""

import os
import sys
import requests
from pathlib import Path

def test_static_files():
    """Testa se os arquivos estáticos existem"""
    print("🔍 Testando arquivos estáticos...")
    
    static_files = [
        'static/css/style.css',
        'static/js/main.js',
        'static/images/logo-conecta.png'
    ]
    
    for file_path in static_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} - {size} bytes")
        else:
            print(f"❌ {file_path} - Arquivo não encontrado!")
            return False
    
    return True

def test_templates():
    """Testa se os templates existem"""
    print("\n🔍 Testando templates...")
    
    template_files = [
        'templates/base.html',
        'templates/index.html',
        'templates/questionario.html',
        'templates/resultado.html',
        'templates/admin/base.html',
        'templates/admin/login.html'
    ]
    
    for file_path in template_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} - {size} bytes")
        else:
            print(f"❌ {file_path} - Arquivo não encontrado!")
            return False
    
    return True

def test_vercel_config():
    """Testa configuração da Vercel"""
    print("\n🔍 Testando configuração da Vercel...")
    
    config_files = [
        'vercel.json',
        'api/index.py',
        'requirements.txt'
    ]
    
    for file_path in config_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} - {size} bytes")
        else:
            print(f"❌ {file_path} - Arquivo não encontrado!")
            return False
    
    return True

def test_imports():
    """Testa se as importações estão funcionando"""
    print("\n🔍 Testando importações...")
    
    try:
        sys.path.append('.')
        import main
        print("✅ main.py importado com sucesso")
        
        app = main.app
        print(f"✅ Flask app configurado: {app.name}")
        print(f"✅ Static folder: {app.static_folder}")
        print(f"✅ Template folder: {app.template_folder}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar: {e}")
        return False

def test_cdn_accessibility():
    """Testa se os CDNs estão acessíveis"""
    print("\n🔍 Testando acessibilidade dos CDNs...")
    
    cdns = [
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
    ]
    
    for cdn in cdns:
        try:
            response = requests.head(cdn, timeout=5)
            if response.status_code == 200:
                print(f"✅ {cdn} - OK")
            else:
                print(f"⚠️ {cdn} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {cdn} - Erro: {e}")
            return False
    
    return True

def main():
    print("🚀 Teste de Configuração para Deploy na Vercel")
    print("=" * 50)
    
    tests = [
        test_static_files,
        test_templates,
        test_vercel_config,
        test_imports,
        test_cdn_accessibility
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro no teste {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES:")
    
    if all(results):
        print("✅ Todos os testes passaram! Projeto pronto para deploy.")
        return 0
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    exit(main())
