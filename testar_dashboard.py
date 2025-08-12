#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar o dashboard corrigido
"""

import os
import sys

# Importar dependências do projeto
try:
    from main import supabase
    print("✅ Dependências do projeto importadas com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar dependências: {e}")
    sys.exit(1)

def testar_dashboard_corrigido():
    """Testa a lógica corrigida do dashboard"""
    print("\n🧪 TESTANDO LÓGICA CORRIGIDA DO DASHBOARD")
    print("=" * 50)
    
    try:
        # Buscar estatísticas totais (mesmo código do dashboard)
        stats_result = supabase.table('vw_estatisticas_admin').select('*').execute()
        
        print(f"📊 Dados brutos da view: {len(stats_result.data)} registros")
        for i, row in enumerate(stats_result.data):
            print(f"   Mês {i+1}: {row['mes_ano']} - {row['total_diagnosticos']} diagnósticos")
        
        if stats_result.data:
            # Agregar dados de todos os meses (mesmo código do dashboard)
            total_empresas = 0
            total_diagnosticos = 0
            diagnosticos_risco_alto = 0
            diagnosticos_risco_moderado = 0
            diagnosticos_risco_baixo = 0
            total_colaboradores = 0
            
            for row in stats_result.data:
                if row['total_empresas']:
                    total_empresas = max(total_empresas, row['total_empresas'])
                if row['total_diagnosticos']:
                    total_diagnosticos += row['total_diagnosticos']
                if row['diagnosticos_risco_alto']:
                    diagnosticos_risco_alto += row['diagnosticos_risco_alto']
                if row['diagnosticos_risco_moderado']:
                    diagnosticos_risco_moderado += row['diagnosticos_risco_moderado']
                if row['diagnosticos_risco_baixo']:
                    diagnosticos_risco_baixo += row['diagnosticos_risco_baixo']
                if row['total_colaboradores_analisados']:
                    total_colaboradores = max(total_colaboradores, row['total_colaboradores_analisados'])
            
            stats = {
                'total_empresas': total_empresas,
                'total_diagnosticos': total_diagnosticos,
                'diagnosticos_risco_alto': diagnosticos_risco_alto,
                'diagnosticos_risco_moderado': diagnosticos_risco_moderado,
                'diagnosticos_risco_baixo': diagnosticos_risco_baixo,
                'total_colaboradores_analisados': total_colaboradores
            }
            
            print(f"\n📈 ESTATÍSTICAS FINAIS:")
            print(f"   🏢 Total empresas: {stats['total_empresas']}")
            print(f"   📋 Total diagnósticos: {stats['total_diagnosticos']}")
            print(f"   🔴 Alto risco: {stats['diagnosticos_risco_alto']}")
            print(f"   🟡 Risco moderado: {stats['diagnosticos_risco_moderado']}")
            print(f"   🟢 Baixo risco: {stats['diagnosticos_risco_baixo']}")
            print(f"   👥 Total colaboradores: {stats['total_colaboradores_analisados']}")
            
            return True
        else:
            print("⚠️ Nenhum dado encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def testar_diagnosticos_recentes():
    """Testa a consulta de diagnósticos recentes"""
    print("\n📋 TESTANDO DIAGNÓSTICOS RECENTES")
    print("=" * 50)
    
    try:
        recent_result = supabase.table('vw_diagnosticos_completos').select('*').limit(10).execute()
        
        print(f"📊 {len(recent_result.data)} diagnósticos recentes encontrados")
        
        for i, diag in enumerate(recent_result.data[:3]):  # Mostrar apenas os 3 primeiros
            print(f"   {i+1}. {diag['razao_social']} - Risco {diag['nivel_risco']} ({diag['data_diagnostico'][:10]})")
        
        return len(recent_result.data) > 0
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🧪 TESTE DO DASHBOARD CORRIGIDO")
    print("=" * 50)
    
    stats_ok = testar_dashboard_corrigido()
    diagnosticos_ok = testar_diagnosticos_recentes()
    
    if stats_ok and diagnosticos_ok:
        print(f"\n🎉 SUCESSO! Dashboard deve estar funcionando corretamente agora!")
        print(f"✅ Estatísticas: OK")
        print(f"✅ Diagnósticos recentes: OK")
    else:
        print(f"\n⚠️ Ainda há problemas:")
        print(f"   Estatísticas: {'✅' if stats_ok else '❌'}")
        print(f"   Diagnósticos: {'✅' if diagnosticos_ok else '❌'}")

if __name__ == "__main__":
    main()
