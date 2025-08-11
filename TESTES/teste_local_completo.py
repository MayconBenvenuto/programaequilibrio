#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTES LOCAIS - PROGRAMA EQUILÍBRIO
Verifica se todas as funcionalidades estão funcionando corretamente
"""

import requests
import json
from datetime import datetime
import time

BASE_URL = "http://localhost:5000"

def test_home_page():
    """Testa a página inicial"""
    print("🏠 TESTANDO PÁGINA INICIAL")
    print("-" * 40)
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # Verificações básicas
            checks = {
                "HTML válido": "<html" in content.lower(),
                "Título presente": "programa equilíbrio" in content.lower(),
                "CSS carregado": "css" in content.lower(),
                "JavaScript presente": "script" in content.lower(),
                "Formulário CNPJ": "cnpj" in content.lower()
            }
            
            print(f"✅ Status: {response.status_code}")
            for check, result in checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check}")
            
            return all(checks.values())
        else:
            print(f"❌ Erro: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_cnpj_validation():
    """Testa a validação de CNPJ"""
    print("\n📋 TESTANDO VALIDAÇÃO DE CNPJ")
    print("-" * 40)
    
    try:
        url = f"{BASE_URL}/validar_cnpj"
        
        # Teste com CNPJ válido
        test_cnpj = "11.222.333/0001-81"
        data = {"cnpj": test_cnpj}
        
        response = requests.post(url, json=data, timeout=15)
        
        print(f"🔍 Testando CNPJ: {test_cnpj}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ Resposta JSON válida")
                print(f"📝 Resultado: {result}")
                return True
            except:
                print("❌ Resposta não é JSON válido")
                return False
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"📄 Conteúdo: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_questionario_page():
    """Testa a página do questionário"""
    print("\n❓ TESTANDO PÁGINA DO QUESTIONÁRIO")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/questionario", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            checks = {
                "Página carregou": True,
                "Perguntas presentes": "pergunta" in content.lower(),
                "Formulário presente": "form" in content.lower(),
                "JavaScript presente": "script" in content.lower()
            }
            
            print(f"✅ Status: {response.status_code}")
            for check, result in checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check}")
            
            return all(checks.values())
        else:
            print(f"❌ Erro: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_admin_login():
    """Testa o acesso administrativo"""
    print("\n👤 TESTANDO LOGIN ADMINISTRATIVO")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/admin/login", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            checks = {
                "Página de login carregou": True,
                "Formulário de login": "login" in content.lower(),
                "Campos username/password": "username" in content.lower() and "password" in content.lower()
            }
            
            print(f"✅ Status: {response.status_code}")
            for check, result in checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check}")
            
            return all(checks.values())
        else:
            print(f"❌ Erro: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_static_files():
    """Testa se arquivos estáticos estão sendo servidos"""
    print("\n🎨 TESTANDO ARQUIVOS ESTÁTICOS")
    print("-" * 40)
    
    static_files = [
        "/static/css/style.css",
        "/static/js/main.js",
        "/static/images/logo-conecta.png"
    ]
    
    results = {}
    
    for file_path in static_files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}", timeout=5)
            results[file_path] = response.status_code == 200
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {file_path}: {response.status_code}")
        except:
            results[file_path] = False
            print(f"❌ {file_path}: Erro de conexão")
    
    return any(results.values())  # Pelo menos um arquivo deve funcionar

def generate_test_report(results):
    """Gera relatório dos testes"""
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL DOS TESTES LOCAIS")
    print("=" * 60)
    
    print(f"🕒 Teste realizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🌐 URL testada: {BASE_URL}")
    print()
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print("📋 RESULTADOS:")
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {test_name}: {status}")
    
    print()
    print("📊 RESUMO:")
    print(f"   Total de testes: {total_tests}")
    print(f"   Testes aprovados: {passed_tests}")
    print(f"   Testes reprovados: {total_tests - passed_tests}")
    print(f"   Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print()
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema pronto para deploy na Vercel")
        return True
    else:
        print()
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Corrigir problemas antes do deploy")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES LOCAIS DO PROGRAMA EQUILÍBRIO")
    print(f"🎯 Testando: {BASE_URL}")
    print()
    
    # Aguardar um pouco para garantir que o servidor está rodando
    print("⏳ Aguardando servidor estar pronto...")
    time.sleep(2)
    
    # Executar testes
    results = {
        "Página Inicial": test_home_page(),
        "Validação CNPJ": test_cnpj_validation(),
        "Página Questionário": test_questionario_page(),
        "Login Administrativo": test_admin_login(),
        "Arquivos Estáticos": test_static_files()
    }
    
    # Gerar relatório
    success = generate_test_report(results)
    
    return success

if __name__ == "__main__":
    main()
