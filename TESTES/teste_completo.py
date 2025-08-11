#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Completo do Sistema - Programa Equilíbrio
Executa todos os testes e fornece relatório completo
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def run_test_script(script_name):
    """Executa um script de teste e captura o resultado"""
    print(f"\n🚀 Executando {script_name}...")
    print("=" * 60)
    
    try:
        # Executa o script
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Mostra a saída
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erro ao executar {script_name}: {e}")
        return False

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("🧪 Verificando dependências...")
    
    required_packages = [
        'flask',
        'requests',
        'supabase',
        'validate_docbr',
        'python-decouple',
        'reportlab'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NÃO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Pacotes faltando: {', '.join(missing_packages)}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def check_environment_vars():
    """Verifica se as variáveis de ambiente estão configuradas"""
    print("\n🧪 Verificando variáveis de ambiente...")
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY'
    ]
    
    optional_vars = [
        'FLASK_SECRET_KEY',
        'ADMIN_EMAIL',
        'ADMIN_PASSWORD'
    ]
    
    missing_required = []
    missing_optional = []
    
    # Verifica variáveis obrigatórias
    for var in required_vars:
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here':
            print(f"   ✅ {var}")
        else:
            print(f"   ❌ {var} - NÃO CONFIGURADA")
            missing_required.append(var)
    
    # Verifica variáveis opcionais
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}")
        else:
            print(f"   ⚠️ {var} - OPCIONAL, não configurada")
            missing_optional.append(var)
    
    if missing_required:
        print(f"\n❌ Variáveis obrigatórias faltando: {', '.join(missing_required)}")
        print("💡 Configure no arquivo .env")
        return False
    
    if missing_optional:
        print(f"\n⚠️ Variáveis opcionais faltando: {', '.join(missing_optional)}")
        print("💡 Sistema funcionará, mas algumas funcionalidades podem estar limitadas")
    
    return True

def check_application_running():
    """Verifica se a aplicação está rodando"""
    print("\n🧪 Verificando se a aplicação está rodando...")
    
    try:
        import requests
        response = requests.get("http://localhost:5000", timeout=5)
        
        if response.status_code == 200:
            print("✅ Aplicação está rodando!")
            return True
        else:
            print(f"❌ Aplicação respondeu com status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Aplicação não está rodando!")
        print("💡 Execute: python main.py")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar aplicação: {e}")
        return False

def main():
    """Função principal"""
    start_time = datetime.now()
    
    print("=" * 80)
    print("🧪 TESTE COMPLETO DO SISTEMA - PROGRAMA EQUILÍBRIO")
    print("=" * 80)
    print(f"📅 Iniciado em: {start_time.strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 80)
    
    # Lista de testes
    pre_tests = [
        ("Dependências", check_dependencies),
        ("Variáveis de Ambiente", check_environment_vars),
        ("Aplicação Rodando", check_application_running)
    ]
    
    test_scripts = [
        "teste_conexao.py",
        "teste_cnpj.py", 
        "teste_apis.py",
        "teste_supabase.py"
    ]
    
    # Resultados
    pre_test_results = []
    script_results = []
    
    # Executa pré-testes
    print("\n📋 PRÉ-TESTES (CONFIGURAÇÃO)")
    print("=" * 50)
    
    for test_name, test_func in pre_tests:
        success = test_func()
        pre_test_results.append((test_name, success))
        
        if not success and test_name in ["Dependências", "Variáveis de Ambiente"]:
            print(f"\n❌ Pré-teste '{test_name}' falhou!")
            print("💡 Configure o ambiente antes de prosseguir.")
            return
    
    # Executa testes dos scripts
    print("\n\n📋 TESTES FUNCIONAIS")
    print("=" * 50)
    
    for script in test_scripts:
        script_path = os.path.join(os.path.dirname(__file__), script)
        
        if os.path.exists(script_path):
            success = run_test_script(script)
            script_results.append((script, success))
        else:
            print(f"⚠️ Script {script} não encontrado!")
            script_results.append((script, False))
        
        # Pausa entre testes
        time.sleep(2)
    
    # Relatório final
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO FINAL DE TESTES")
    print("=" * 80)
    
    print(f"⏱️ Duração total: {duration.total_seconds():.1f} segundos")
    print(f"📅 Finalizado em: {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Resultados dos pré-testes
    print(f"\n🔧 PRÉ-TESTES:")
    pre_passed = 0
    for test_name, success in pre_test_results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"   {status} {test_name}")
        if success:
            pre_passed += 1
    
    # Resultados dos testes funcionais
    print(f"\n🧪 TESTES FUNCIONAIS:")
    func_passed = 0
    for script, success in script_results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"   {status} {script}")
        if success:
            func_passed += 1
    
    # Resumo geral
    total_pre = len(pre_test_results)
    total_func = len(script_results)
    total_passed = pre_passed + func_passed
    total_tests = total_pre + total_func
    
    print(f"\n🎯 RESUMO GERAL:")
    print(f"   📋 Total de testes: {total_tests}")
    print(f"   ✅ Testes aprovados: {total_passed}")
    print(f"   ❌ Testes falhados: {total_tests - total_passed}")
    print(f"   📊 Taxa de sucesso: {(total_passed/total_tests)*100:.1f}%")
    
    # Conclusão
    if total_passed == total_tests:
        print(f"\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL! 🎉")
        print(f"💡 Todos os componentes estão funcionando perfeitamente.")
        print(f"🚀 O sistema está pronto para uso em produção!")
    elif pre_passed == total_pre and func_passed > 0:
        print(f"\n✅ SISTEMA PARCIALMENTE FUNCIONAL")
        print(f"💡 Configuração básica OK, alguns componentes podem precisar de ajustes.")
        print(f"🔧 Revise os testes que falharam para melhorar a funcionalidade.")
    else:
        print(f"\n❌ SISTEMA COM PROBLEMAS SÉRIOS")
        print(f"💡 Há problemas na configuração básica ou dependências.")
        print(f"🔧 Configure o ambiente e execute os testes novamente.")
    
    # Recomendações
    print(f"\n💡 PRÓXIMOS PASSOS:")
    if total_passed == total_tests:
        print(f"   1. ✅ Sistema pronto! Faça um teste manual completo")
        print(f"   2. ✅ Configure o domínio de produção")
        print(f"   3. ✅ Execute backup do banco de dados")
        print(f"   4. ✅ Configure monitoramento de logs")
    else:
        print(f"   1. 🔧 Corrija os problemas identificados nos testes")
        print(f"   2. 🔧 Execute este teste novamente")
        print(f"   3. 🔧 Verifique logs da aplicação para detalhes")
        print(f"   4. 🔧 Consulte a documentação para configuração")

if __name__ == "__main__":
    main()
