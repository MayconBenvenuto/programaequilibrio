#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from main import supabase

# Verificar empresas
print("🏢 Verificando empresas cadastradas...")
result_empresas = supabase.table('empresas').select('*').execute()
print(f"Total de empresas: {len(result_empresas.data)}")

if result_empresas.data:
    print("\nPrimeiras 5 empresas:")
    for i, emp in enumerate(result_empresas.data[:5]):
        print(f"{i+1}. {emp['nome_empresa']} (ID: {emp['id']})")

# Verificar diagnósticos
print("\n🔍 Verificando diagnósticos...")
result_diagnosticos = supabase.table('diagnosticos').select('*').execute()
print(f"Total de diagnósticos: {len(result_diagnosticos.data)}")

if result_diagnosticos.data:
    print("\nPrimeiros 3 diagnósticos:")
    for i, diag in enumerate(result_diagnosticos.data[:3]):
        print(f"{i+1}. Empresa ID: {diag['empresa_id']}, Data: {diag.get('created_at', 'N/A')}")

# Verificar se existem dados com "(exemplo)"
print("\n🔍 Verificando empresas de exemplo...")
result_exemplos = supabase.table('empresas').select('*').ilike('nome_empresa', '%exemplo%').execute()
print(f"Empresas com '(exemplo)': {len(result_exemplos.data)}")

if result_exemplos.data:
    for emp in result_exemplos.data:
        print(f"- {emp['nome_empresa']}")
