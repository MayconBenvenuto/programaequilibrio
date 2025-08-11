#!/usr/bin/env python3
"""
Teste simples para verificar se o main.py pode ser importado
"""

try:
    print("🔍 Testando importação do main.py...")
    from main import app
    print("✅ main.py importado com sucesso!")
    
    print("🧪 Testando configuração do Flask...")
    print(f"App name: {app.name}")
    print(f"Debug mode: {app.debug}")
    print("✅ Configuração do Flask OK!")
    
    # Testar se as rotas estão carregadas
    print("🛣️ Testando rotas disponíveis...")
    for rule in app.url_map.iter_rules():
        print(f"   - {rule.rule} [{', '.join(rule.methods)}]")
    print("✅ Rotas carregadas!")
    
    print("🎉 Tudo funcionando! O app pode ser executado.")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()
