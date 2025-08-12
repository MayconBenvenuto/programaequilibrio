#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Debug completo das consultas do dashboard
"""

import os
import sys

# Importar dependências do projeto
try:
    from main import supabase
    print("✅ Supabase conectado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def debug_view_estatisticas():
    """Debug da view de estatísticas"""
    print("\n🔍 DEBUG: vw_estatisticas_admin")
    print("=" * 50)
    
    try:
        result = supabase.table('vw_estatisticas_admin').select('*').execute()
        print(f"📊 Registros encontrados: {len(result.data)}")
        
        for i, row in enumerate(result.data):
            print(f"\n   Registro {i+1}:")
            print(f"   - total_empresas: {row.get('total_empresas')} (tipo: {type(row.get('total_empresas'))})")
            print(f"   - total_diagnosticos: {row.get('total_diagnosticos')} (tipo: {type(row.get('total_diagnosticos'))})")
            print(f"   - diagnosticos_risco_alto: {row.get('diagnosticos_risco_alto')} (tipo: {type(row.get('diagnosticos_risco_alto'))})")
            print(f"   - diagnosticos_risco_moderado: {row.get('diagnosticos_risco_moderado')} (tipo: {type(row.get('diagnosticos_risco_moderado'))})")
            print(f"   - diagnosticos_risco_baixo: {row.get('diagnosticos_risco_baixo')} (tipo: {type(row.get('diagnosticos_risco_baixo'))})")
            print(f"   - total_colaboradores_analisados: {row.get('total_colaboradores_analisados')} (tipo: {type(row.get('total_colaboradores_analisados'))})")
            print(f"   - mes_ano: {row.get('mes_ano')}")
        
        return result.data
    except Exception as e:
        print(f"❌ Erro ao consultar view: {e}")
        return []

def debug_agregacao(data):
    """Debug da lógica de agregação"""
    print(f"\n🧮 DEBUG: Lógica de Agregação")
    print("=" * 50)
    
    if not data:
        print("❌ Nenhum dado para agregar")
        return {}
    
    total_empresas = 0
    total_diagnosticos = 0
    diagnosticos_risco_alto = 0
    diagnosticos_risco_moderado = 0
    diagnosticos_risco_baixo = 0
    total_colaboradores = 0
    
    print("🔄 Processando registros:")
    
    for i, row in enumerate(data):
        print(f"\n   Processando registro {i+1}:")
        
        # Total empresas - pegar o máximo
        if row.get('total_empresas'):
            old_total = total_empresas
            total_empresas = max(total_empresas, int(row['total_empresas']))
            print(f"   - Empresas: {old_total} -> {total_empresas} (valor atual: {row['total_empresas']})")
        else:
            print(f"   - Empresas: {total_empresas} (sem alteração - valor: {row.get('total_empresas')})")
        
        # Total diagnósticos - somar
        if row.get('total_diagnosticos'):
            old_total = total_diagnosticos
            total_diagnosticos += int(row['total_diagnosticos'])
            print(f"   - Diagnósticos: {old_total} -> {total_diagnosticos} (adicionado: {row['total_diagnosticos']})")
        else:
            print(f"   - Diagnósticos: {total_diagnosticos} (sem alteração - valor: {row.get('total_diagnosticos')})")
        
        # Risco alto - somar
        if row.get('diagnosticos_risco_alto'):
            old_total = diagnosticos_risco_alto
            diagnosticos_risco_alto += int(row['diagnosticos_risco_alto'])
            print(f"   - Alto risco: {old_total} -> {diagnosticos_risco_alto} (adicionado: {row['diagnosticos_risco_alto']})")
        
        # Risco moderado - somar
        if row.get('diagnosticos_risco_moderado'):
            old_total = diagnosticos_risco_moderado
            diagnosticos_risco_moderado += int(row['diagnosticos_risco_moderado'])
            print(f"   - Risco moderado: {old_total} -> {diagnosticos_risco_moderado} (adicionado: {row['diagnosticos_risco_moderado']})")
        
        # Risco baixo - somar
        if row.get('diagnosticos_risco_baixo'):
            old_total = diagnosticos_risco_baixo
            diagnosticos_risco_baixo += int(row['diagnosticos_risco_baixo'])
            print(f"   - Baixo risco: {old_total} -> {diagnosticos_risco_baixo} (adicionado: {row['diagnosticos_risco_baixo']})")
        
        # Total colaboradores - pegar o máximo
        if row.get('total_colaboradores_analisados'):
            old_total = total_colaboradores
            total_colaboradores = max(total_colaboradores, int(row['total_colaboradores_analisados']))
            print(f"   - Colaboradores: {old_total} -> {total_colaboradores} (valor atual: {row['total_colaboradores_analisados']})")
    
    resultado = {
        'total_empresas': total_empresas,
        'total_diagnosticos': total_diagnosticos,
        'diagnosticos_risco_alto': diagnosticos_risco_alto,
        'diagnosticos_risco_moderado': diagnosticos_risco_moderado,
        'diagnosticos_risco_baixo': diagnosticos_risco_baixo,
        'total_colaboradores_analisados': total_colaboradores
    }
    
    print(f"\n📊 RESULTADO FINAL:")
    for key, value in resultado.items():
        print(f"   {key}: {value}")
    
    return resultado

def debug_consultas_diretas():
    """Debug das tabelas base diretamente"""
    print(f"\n📋 DEBUG: Consultas Diretas")
    print("=" * 50)
    
    try:
        # Empresas
        empresas = supabase.table('empresas').select('id, razao_social').execute()
        print(f"🏢 Empresas na tabela: {len(empresas.data)}")
        for emp in empresas.data[:3]:
            print(f"   - {emp['razao_social']}")
        
        # Diagnósticos
        diagnosticos = supabase.table('diagnosticos').select('id, nivel_risco, empresa_id').execute()
        print(f"📋 Diagnósticos na tabela: {len(diagnosticos.data)}")
        
        # Contar por nível de risco
        alto = len([d for d in diagnosticos.data if d['nivel_risco'] == 'Alto'])
        moderado = len([d for d in diagnosticos.data if d['nivel_risco'] == 'Moderado'])
        baixo = len([d for d in diagnosticos.data if d['nivel_risco'] == 'Baixo'])
        
        print(f"   - Alto risco: {alto}")
        print(f"   - Risco moderado: {moderado}")
        print(f"   - Baixo risco: {baixo}")
        
        return {
            'total_empresas': len(empresas.data),
            'total_diagnosticos': len(diagnosticos.data),
            'diagnosticos_risco_alto': alto,
            'diagnosticos_risco_moderado': moderado,
            'diagnosticos_risco_baixo': baixo
        }
        
    except Exception as e:
        print(f"❌ Erro nas consultas diretas: {e}")
        return {}

def main():
    print("🔍 DEBUG COMPLETO DAS CONSULTAS DO DASHBOARD")
    print("=" * 60)
    
    # 1. Debug da view
    view_data = debug_view_estatisticas()
    
    # 2. Debug da agregação
    if view_data:
        agregacao_result = debug_agregacao(view_data)
    else:
        agregacao_result = {}
    
    # 3. Debug das consultas diretas
    consulta_direta = debug_consultas_diretas()
    
    # 4. Comparação
    print(f"\n🔍 COMPARAÇÃO DE RESULTADOS:")
    print("=" * 50)
    print(f"View + Agregação:")
    print(f"   Empresas: {agregacao_result.get('total_empresas', 0)}")
    print(f"   Diagnósticos: {agregacao_result.get('total_diagnosticos', 0)}")
    
    print(f"\nConsulta Direta:")
    print(f"   Empresas: {consulta_direta.get('total_empresas', 0)}")
    print(f"   Diagnósticos: {consulta_direta.get('total_diagnosticos', 0)}")
    
    if agregacao_result != consulta_direta:
        print(f"⚠️ DIFERENÇAS DETECTADAS!")
    else:
        print(f"✅ Resultados consistentes")

if __name__ == "__main__":
    main()
