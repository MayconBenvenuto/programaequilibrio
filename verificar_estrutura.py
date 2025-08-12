#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from main import supabase

# Verificar empresas
print("🏢 Verificando estrutura das empresas...")
result_empresas = supabase.table('empresas').select('*').execute()
print(f"Total de empresas: {len(result_empresas.data)}")

if result_empresas.data:
    print("\nEstrutura da primeira empresa:")
    primeira_empresa = result_empresas.data[0]
    for key, value in primeira_empresa.items():
        print(f"  {key}: {value}")
    
    print("\nTodas as empresas:")
    for i, emp in enumerate(result_empresas.data):
        # Tentar diferentes possíveis nomes de campos
        nome = emp.get('nome_empresa') or emp.get('nome') or emp.get('razao_social') or f"Empresa {emp.get('id', 'sem ID')}"
        print(f"{i+1}. {nome}")

# Verificar diagnósticos
print("\n🔍 Verificando diagnósticos...")
result_diagnosticos = supabase.table('diagnosticos').select('*').execute()
print(f"Total de diagnósticos: {len(result_diagnosticos.data)}")

if result_diagnosticos.data:
    print("\nEstrutura do primeiro diagnóstico:")
    primeiro_diag = result_diagnosticos.data[0]
    for key, value in primeiro_diag.items():
        print(f"  {key}: {value}")
