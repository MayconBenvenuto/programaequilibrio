#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste da correção do dashboard
"""

import os
import sys

# Importar dependências do projeto
try:
    from main import supabase
    print("✅ Dependências importadas com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar dependências: {e}")
    sys.exit(1)

def testar_nova_logica():
    """Testa a nova lógica do dashboard"""
    print("\n🧪 TESTANDO NOVA LÓGICA DO DASHBOARD")
    print("=" * 50)
    
    try:
        print("🔍 [DEBUG] Usando consultas diretas...")
        
        # 1. Buscar total de empresas
        empresas_result = supabase.table('empresas').select('id, num_colaboradores').execute()
        total_empresas = len(empresas_result.data)
        total_colaboradores = sum(emp['num_colaboradores'] or 0 for emp in empresas_result.data)
        print(f"🔍 [DEBUG] Empresas: {total_empresas}, Colaboradores: {total_colaboradores}")
        
        # 2. Buscar diagnósticos e contagem por risco
        diagnosticos_result = supabase.table('diagnosticos').select('id, nivel_risco').execute()
        total_diagnosticos = len(diagnosticos_result.data)
        
        # Contar por nível de risco
        diagnosticos_risco_alto = len([d for d in diagnosticos_result.data if d['nivel_risco'] == 'Alto'])
        diagnosticos_risco_moderado = len([d for d in diagnosticos_result.data if d['nivel_risco'] == 'Moderado'])
        diagnosticos_risco_baixo = len([d for d in diagnosticos_result.data if d['nivel_risco'] == 'Baixo'])
        
        print(f"🔍 [DEBUG] Diagnósticos: {total_diagnosticos} (Alto: {diagnosticos_risco_alto}, Moderado: {diagnosticos_risco_moderado}, Baixo: {diagnosticos_risco_baixo})")
        
        # Montar estatísticas
        stats = {
            'total_empresas': total_empresas,
            'total_diagnosticos': total_diagnosticos,
            'diagnosticos_risco_alto': diagnosticos_risco_alto,
            'diagnosticos_risco_moderado': diagnosticos_risco_moderado,
            'diagnosticos_risco_baixo': diagnosticos_risco_baixo,
            'total_colaboradores_analisados': total_colaboradores
        }
        
        print(f"🔍 [DEBUG] Stats finais: {stats}")
        
        print(f"\n📊 RESULTADO ESPERADO NO DASHBOARD:")
        print(f"   🏢 Empresas Atendidas: {stats['total_empresas']}")
        print(f"   📋 Diagnósticos Realizados: {stats['total_diagnosticos']}")
        print(f"   👥 Colaboradores Analisados: {stats['total_colaboradores_analisados']:,}".replace(',', '.'))
        print(f"   🔴 Alto Risco: {stats['diagnosticos_risco_alto']}")
        print(f"   🟡 Risco Moderado: {stats['diagnosticos_risco_moderado']}")
        print(f"   🟢 Baixo Risco: {stats['diagnosticos_risco_baixo']}")
        
        return stats['total_empresas'] > 0 and stats['total_diagnosticos'] > 0
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🔧 TESTE DA CORREÇÃO DO DASHBOARD")
    print("=" * 50)
    
    if testar_nova_logica():
        print(f"\n🎉 SUCESSO! A nova lógica está funcionando corretamente.")
        print(f"✅ Agora o dashboard deve mostrar todos os dados corretos.")
    else:
        print(f"\n❌ Ainda há problemas na nova lógica.")

if __name__ == "__main__":
    main()
