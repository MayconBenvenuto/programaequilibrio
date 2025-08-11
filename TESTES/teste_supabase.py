#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Banco Supabase - Programa Equilíbrio
Testa a conexão e operações básicas com o banco Supabase
"""

import os
import sys
import json
from datetime import datetime
from supabase import create_client, Client
from decouple import config

# Configurações do Supabase (ajuste conforme necessário)
SUPABASE_URL = config('SUPABASE_URL', default='your_supabase_url_here')
SUPABASE_KEY = config('SUPABASE_ANON_KEY', default='your_supabase_anon_key_here')

def test_supabase_connection():
    """Testa a conexão com o Supabase"""
    print("🧪 Testando conexão com Supabase...")
    
    try:
        if SUPABASE_URL == 'your_supabase_url_here' or SUPABASE_KEY == 'your_supabase_anon_key_here':
            print("❌ Configurações do Supabase não encontradas!")
            print("💡 Configure SUPABASE_URL e SUPABASE_ANON_KEY no arquivo .env")
            return False
        
        # Cria cliente Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Testa uma consulta simples
        response = supabase.table('empresas').select('id').limit(1).execute()
        
        print("✅ Conexão com Supabase estabelecida!")
        print(f"📊 URL: {SUPABASE_URL}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com Supabase: {e}")
        return False

def test_database_tables():
    """Testa se as tabelas necessárias existem"""
    print("\n🧪 Testando estrutura de tabelas...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        tables_to_test = [
            'empresas',
            'diagnosticos', 
            'admin_users'
        ]
        
        results = {}
        
        for table in tables_to_test:
            try:
                # Tenta fazer uma consulta simples na tabela
                response = supabase.table(table).select('*').limit(1).execute()
                print(f"✅ Tabela '{table}' existe e é acessível")
                results[table] = True
            except Exception as e:
                print(f"❌ Problema com tabela '{table}': {e}")
                results[table] = False
        
        return results
        
    except Exception as e:
        print(f"❌ Erro geral ao testar tabelas: {e}")
        return {}

def test_insert_operation():
    """Testa operação de inserção"""
    print("\n🧪 Testando inserção de dados...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Dados de teste
        test_empresa = {
            "cnpj": "11111111000191",
            "razao_social": "Empresa Teste",
            "nome_fantasia": "Teste Ltda",
            "email": "teste@teste.com",
            "telefone": "(11) 99999-9999",
            "whatsapp": "(11) 99999-9999",
            "endereco": {"logradouro": "Rua Teste, 123", "cidade": "São Paulo"},
            "num_colaboradores": 50,
            "setor_atividade": "Tecnologia",
            "rh_responsavel": "João Silva",
            "cargo_rh": "Gerente de RH"
        }
        
        # Primeiro, remove registro de teste se existir
        supabase.table('empresas').delete().eq('cnpj', test_empresa['cnpj']).execute()
        
        # Insere registro de teste
        response = supabase.table('empresas').insert(test_empresa).execute()
        
        if response.data:
            empresa_id = response.data[0]['id']
            print(f"✅ Inserção bem-sucedida! ID: {empresa_id}")
            
            # Agora testa inserir um diagnóstico
            test_diagnostico = {
                "empresa_id": empresa_id,
                "respostas": {
                    "pergunta_1": 5,
                    "pergunta_2": 4,
                    "pergunta_3": 3,
                    "pergunta_4": 5,
                    "pergunta_5": 4,
                    "pergunta_6": 3,
                    "pergunta_7": 5,
                    "pergunta_8": 4,
                    "pergunta_9": 3,
                    "pergunta_10": 5
                },
                "analise": {
                    "pontuacao_total": 41,
                    "nivel_risco": "Intermediário",
                    "areas_foco": ["Saúde Mental", "Ergonomia"],
                    "questoes_criticas": 2,
                    "acoes_recomendadas": ["Treinamento", "Avaliação"]
                },
                "nivel_risco": "Intermediário",
                "questoes_criticas": 2,
                "areas_foco": ["Saúde Mental", "Ergonomia"],
                "acoes_recomendadas": ["Treinamento", "Avaliação"]
            }
            
            diag_response = supabase.table('diagnosticos').insert(test_diagnostico).execute()
            
            if diag_response.data:
                print("✅ Diagnóstico de teste inserido com sucesso!")
                
                # Remove dados de teste
                supabase.table('diagnosticos').delete().eq('empresa_id', empresa_id).execute()
                supabase.table('empresas').delete().eq('id', empresa_id).execute()
                print("🧹 Dados de teste removidos")
                
                return True
            else:
                print("❌ Falha ao inserir diagnóstico de teste")
                return False
        else:
            print("❌ Falha na inserção de empresa de teste")
            return False
            
    except Exception as e:
        print(f"❌ Erro na operação de inserção: {e}")
        return False

def test_view_access():
    """Testa acesso à view de diagnósticos completos"""
    print("\n🧪 Testando acesso à view...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Testa a view de diagnósticos completos
        response = supabase.table('vw_diagnosticos_completos').select('*').limit(5).execute()
        
        if response.data is not None:
            count = len(response.data)
            print(f"✅ View acessível! Encontrados {count} registros")
            
            if count > 0:
                # Mostra um exemplo
                exemplo = response.data[0]
                print(f"📋 Exemplo - Empresa: {exemplo.get('empresa_nome', 'N/A')}")
                print(f"📊 Nível: {exemplo.get('nivel', 'N/A')}")
            
            return True
        else:
            print("❌ View não acessível ou vazia")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao acessar view: {e}")
        return False

def test_admin_authentication():
    """Testa se existe pelo menos um usuário admin"""
    print("\n🧪 Testando usuários administrativos...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        response = supabase.table('admin_users').select('email, is_active').eq('is_active', True).execute()
        
        if response.data:
            active_admins = len(response.data)
            print(f"✅ Encontrados {active_admins} administradores ativos")
            
            for admin in response.data:
                print(f"👤 Admin: {admin.get('email', 'N/A')}")
            
            return True
        else:
            print("⚠️ Nenhum administrador ativo encontrado!")
            print("💡 Execute o script de criação de admin primeiro")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar admins: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 TESTE DE BANCO SUPABASE")
    print("=" * 60)
    
    # Lista de testes
    tests = [
        ("Conexão", test_supabase_connection),
        ("Tabelas", test_database_tables),
        ("Inserção", test_insert_operation),
        ("View", test_view_access),
        ("Admins", test_admin_authentication)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        if test_name == "Tabelas":
            # Teste especial que retorna dict
            table_results = test_func()
            if table_results:
                success = all(table_results.values())
                results.append((test_name, success))
                if not success:
                    failed_tables = [table for table, status in table_results.items() if not status]
                    print(f"❌ Tabelas com problema: {', '.join(failed_tables)}")
            else:
                results.append((test_name, False))
        else:
            # Testes normais
            success = test_func()
            results.append((test_name, success))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES DE BANCO")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"🔍 {test_name}: {status}")
    
    print(f"\n🎯 RESULTADO GERAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES DE BANCO PASSARAM!")
        print("💡 O banco Supabase está configurado corretamente.")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("💡 Verifique as configurações do Supabase e execute a estrutura de banco.")

if __name__ == "__main__":
    main()
