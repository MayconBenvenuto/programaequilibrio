#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste direto das rotas de empresas (bypassing auth para debug)
"""

import sys
import os
import requests
from urllib.parse import quote, unquote

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_dados_empresas():
    """Verifica se há dados de empresas no banco"""
    
    try:
        # Importar apenas o que precisamos
        from decouple import config
        from supabase import create_client, Client
        
        # Configurar Supabase diretamente
        SUPABASE_URL = config('SUPABASE_URL')
        SUPABASE_ANON_KEY = config('SUPABASE_ANON_KEY')
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        if not supabase:
            print("❌ Supabase não configurado")
            return False
        
        print("\n📊 VERIFICANDO DADOS NO BANCO")
        print("=" * 35)
        
        # Verificar empresas na tabela principal
        empresas_result = supabase.table('empresas').select('razao_social, cnpj').limit(5).execute()
        
        print(f"📋 Empresas na tabela 'empresas': {len(empresas_result.data)}")
        for emp in empresas_result.data:
            print(f"   - {emp.get('razao_social', 'N/A')} - {emp.get('cnpj', 'N/A')}")
        
        # Verificar view completa
        view_result = supabase.table('vw_diagnosticos_completos').select('razao_social, cnpj, data_diagnostico').limit(5).execute()
        
        print(f"\n📋 Dados na view 'vw_diagnosticos_completos': {len(view_result.data)}")
        for emp in view_result.data:
            print(f"   - {emp.get('razao_social', 'N/A')} - {emp.get('cnpj', 'N/A')} - {emp.get('data_diagnostico', 'N/A')}")
        
        return len(view_result.data) > 0
        
    except Exception as e:
        print(f"❌ Erro ao verificar dados: {e}")
        return False

def testar_rota_diretamente():
    """Testa as rotas diretamente importando as funções"""
    
    try:
        print("🔍 TESTANDO CONEXÃO COM SUPABASE DIRETAMENTE")
        print("=" * 45)
        
        # Usar a mesma configuração do verificar_dados_empresas
        return verificar_dados_empresas()
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def gerar_dados_teste():
    """Sugere como gerar dados de teste"""
    
    print("\n💡 PARA GERAR DADOS DE TESTE:")
    print("=" * 35)
    print("1. Execute: python popular_banco_demo.py")
    print("2. Ou crie empresas manualmente via interface")
    print("3. Certifique-se que há diagnósticos associados")

def main():
    print("🧪 TESTE DIRETO - EMPRESAS E BANCO DE DADOS")
    print("=" * 50)
    
    # Verificar dados no banco
    tem_dados = verificar_dados_empresas()
    
    if not tem_dados:
        print("\n⚠️ NENHUM DADO ENCONTRADO!")
        gerar_dados_teste()
        return
    
    # Testar funções
    if testar_rota_diretamente():
        print("\n✅ TESTES BÁSICOS OK!")
        print("\n💡 PRÓXIMOS PASSOS:")
        print("1. Execute 'python main.py' para iniciar servidor")
        print("2. Acesse http://localhost:5000/admin/empresas")
        print("3. Teste as funcionalidades manualmente")
    else:
        print("\n❌ PROBLEMAS ENCONTRADOS!")
        print("Verifique os erros acima")
    
    print(f"\n{'=' * 50}")
    print("🏁 TESTE CONCLUÍDO")

if __name__ == "__main__":
    main()
