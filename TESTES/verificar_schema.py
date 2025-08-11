#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICAR SCHEMA DA TABELA EMPRESAS
"""

import sys
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carrega as variáveis de ambiente
load_dotenv()

def verificar_schema():
    """Verifica o schema real da tabela empresas"""
    print("="*60)
    print("🔍 VERIFICANDO SCHEMA DA TABELA EMPRESAS")
    print("="*60)
    
    try:
        # Configuração do Supabase
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            print("❌ Variáveis de ambiente não encontradas!")
            return False
        
        # Cria cliente Supabase
        supabase: Client = create_client(url, key)
        print("✅ Conexão com Supabase estabelecida!")
        
        # Faz uma consulta básica para ver as colunas
        print("📊 Consultando estrutura da tabela...")
        
        # Consulta um registro (se existir) ou faz select vazio
        result = supabase.table("empresas").select("*").limit(1).execute()
        
        if result.data:
            print("📋 Colunas encontradas na tabela 'empresas':")
            for col in result.data[0].keys():
                print(f"   • {col}")
        else:
            # Se não há dados, vamos tentar inserir um registro mínimo para ver o erro
            print("📋 Tentando inserir dados mínimos para descobrir colunas...")
            try:
                test_data = {"nome": "teste"}
                supabase.table("empresas").insert(test_data).execute()
            except Exception as e:
                print(f"Erro esperado: {e}")
        
        return True
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    verificar_schema()
