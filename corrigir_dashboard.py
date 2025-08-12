#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corrigir o problema do dashboard admin
Testa as queries e corrige a estrutura do banco se necessário
"""

import os
import sys
from datetime import datetime

# Importar dependências do projeto
try:
    from main import supabase
    print("✅ Dependências do projeto importadas com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar dependências: {e}")
    sys.exit(1)

def testar_consultas():
    """Testa as consultas do dashboard"""
    print("\n🔍 TESTANDO CONSULTAS DO DASHBOARD")
    print("=" * 50)
    
    # 1. Testar view de estatísticas
    print("\n1️⃣ Testando vw_estatisticas_admin...")
    try:
        stats_result = supabase.table('vw_estatisticas_admin').select('*').execute()
        print(f"   📊 Resultado: {len(stats_result.data)} registros")
        if stats_result.data:
            print(f"   📈 Primeiro registro: {stats_result.data[0]}")
        else:
            print("   ⚠️ Nenhum dado encontrado na view de estatísticas")
    except Exception as e:
        print(f"   ❌ Erro ao consultar view de estatísticas: {e}")
    
    # 2. Testar view de diagnósticos completos
    print("\n2️⃣ Testando vw_diagnosticos_completos...")
    try:
        recent_result = supabase.table('vw_diagnosticos_completos').select('*').limit(5).execute()
        print(f"   📊 Resultado: {len(recent_result.data)} registros")
        if recent_result.data:
            print(f"   📋 Primeiro registro: {recent_result.data[0]}")
        else:
            print("   ⚠️ Nenhum dado encontrado na view de diagnósticos")
    except Exception as e:
        print(f"   ❌ Erro ao consultar view de diagnósticos: {e}")
    
    # 3. Testar tabelas base diretamente
    print("\n3️⃣ Testando tabelas base...")
    try:
        empresas_result = supabase.table('empresas').select('id, razao_social, created_at').limit(5).execute()
        print(f"   🏢 Empresas encontradas: {len(empresas_result.data)}")
        
        diagnosticos_result = supabase.table('diagnosticos').select('id, nivel_risco, created_at').limit(5).execute()
        print(f"   📋 Diagnósticos encontrados: {len(diagnosticos_result.data)}")
        
        if empresas_result.data:
            print(f"   📝 Exemplo empresa: {empresas_result.data[0]['razao_social']}")
        
        if diagnosticos_result.data:
            print(f"   📊 Exemplo diagnóstico: Nível {diagnosticos_result.data[0]['nivel_risco']}")
            
    except Exception as e:
        print(f"   ❌ Erro ao consultar tabelas base: {e}")

def criar_view_estatisticas_simples():
    """Cria uma view de estatísticas mais simples e funcional"""
    print("\n🔧 CRIANDO VIEW DE ESTATÍSTICAS CORRIGIDA")
    print("=" * 50)
    
    view_sql = """
    CREATE OR REPLACE VIEW vw_estatisticas_admin_simples AS
    SELECT 
        COUNT(DISTINCT e.id) as total_empresas,
        COUNT(d.id) as total_diagnosticos,
        COUNT(CASE WHEN d.nivel_risco = 'Alto' THEN 1 END) as diagnosticos_risco_alto,
        COUNT(CASE WHEN d.nivel_risco = 'Moderado' THEN 1 END) as diagnosticos_risco_moderado,
        COUNT(CASE WHEN d.nivel_risco = 'Baixo' THEN 1 END) as diagnosticos_risco_baixo,
        COALESCE(SUM(e.num_colaboradores), 0) as total_colaboradores_analisados
    FROM empresas e
    LEFT JOIN diagnosticos d ON e.id = d.empresa_id;
    """
    
    try:
        result = supabase.rpc('execute_sql', {'query': view_sql}).execute()
        print("✅ View vw_estatisticas_admin_simples criada com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar view: {e}")
        return False

def testar_nova_view():
    """Testa a nova view de estatísticas"""
    print("\n🧪 TESTANDO NOVA VIEW")
    print("=" * 50)
    
    try:
        stats_result = supabase.table('vw_estatisticas_admin_simples').select('*').execute()
        print(f"✅ Nova view funcionando!")
        if stats_result.data:
            stats = stats_result.data[0]
            print(f"   🏢 Total empresas: {stats.get('total_empresas', 0)}")
            print(f"   📋 Total diagnósticos: {stats.get('total_diagnosticos', 0)}")
            print(f"   🔴 Alto risco: {stats.get('diagnosticos_risco_alto', 0)}")
            print(f"   🟡 Risco moderado: {stats.get('diagnosticos_risco_moderado', 0)}")
            print(f"   🟢 Baixo risco: {stats.get('diagnosticos_risco_baixo', 0)}")
            print(f"   👥 Total colaboradores: {stats.get('total_colaboradores_analisados', 0)}")
            return stats
        else:
            print("⚠️ View criada mas sem dados")
            return {}
    except Exception as e:
        print(f"❌ Erro ao testar nova view: {e}")
        return {}

def main():
    print("🔧 DIAGNÓSTICO E CORREÇÃO DO DASHBOARD ADMIN")
    print("=" * 60)
    
    # Testar consultas atuais
    testar_consultas()
    
    # Criar view corrigida
    if criar_view_estatisticas_simples():
        # Testar nova view
        stats = testar_nova_view()
        
        if stats and stats.get('total_empresas', 0) > 0:
            print(f"\n🎉 SUCESSO! Dashboard deve funcionar agora.")
            print(f"📊 {stats['total_empresas']} empresas e {stats['total_diagnosticos']} diagnósticos encontrados.")
        else:
            print(f"\n⚠️ View criada mas ainda sem dados suficientes.")
    
    print(f"\n✅ Diagnóstico concluído!")

if __name__ == "__main__":
    main()
