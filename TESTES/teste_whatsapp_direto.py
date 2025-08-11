#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DE SALVAMENTO DE WHATSAPP (DIRETO NO BANCO)
Testa se o campo WhatsApp está sendo salvo corretamente no banco de dados
"""

import sys
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import uuid
from datetime import datetime, timezone

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carrega as variáveis de ambiente
load_dotenv()

def testar_whatsapp_banco():
    """Testa o salvamento do WhatsApp diretamente no banco"""
    print("="*60)
    print("🧪 TESTE DE SALVAMENTO DE WHATSAPP (DIRETO)")
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
        
        # Dados de teste incluindo WhatsApp
        empresa_teste = {
            "razao_social": "Empresa Teste WhatsApp Ltda",
            "nome_fantasia": "Empresa Teste WhatsApp",
            "cnpj": "12.345.678/0001-99",
            "email": "teste@whatsapp.com.br",
            "telefone": "(11) 98765-4321",
            "whatsapp": "(11) 98765-4321",  # Campo WhatsApp
            "endereco": {"rua": "Rua Teste, 123", "cidade": "São Paulo"},
            "rh_responsavel": "João Teste",
            "cargo_rh": "Gerente de RH",
            "setor_atividade": "Comércio Eletrônico",
            "num_colaboradores": 10
        }
        
        print("📊 Inserindo empresa com WhatsApp...")
        
        # Insere no banco
        result = supabase.table("empresas").insert(empresa_teste).execute()
        
        if result.data:
            empresa_id = result.data[0]["id"]
            print(f"✅ Empresa inserida com sucesso! ID: {empresa_id}")
            
            # Verifica se o WhatsApp foi salvo corretamente
            print("🔍 Verificando se WhatsApp foi salvo...")
            
            consulta = supabase.table("empresas").select("*").eq("id", empresa_id).execute()
            
            if consulta.data:
                empresa_salva = consulta.data[0]
                whatsapp_salvo = empresa_salva.get("whatsapp")
                
                if whatsapp_salvo:
                    print(f"✅ WhatsApp salvo corretamente: {whatsapp_salvo}")
                    
                    # Verifica se todos os campos foram salvos
                    print("\n📋 CAMPOS SALVOS:")
                    print(f"   • Razão Social: {empresa_salva.get('razao_social')}")
                    print(f"   • Nome Fantasia: {empresa_salva.get('nome_fantasia')}")
                    print(f"   • Email: {empresa_salva.get('email')}")
                    print(f"   • Telefone: {empresa_salva.get('telefone')}")
                    print(f"   • WhatsApp: {empresa_salva.get('whatsapp')}")
                    print(f"   • CNPJ: {empresa_salva.get('cnpj')}")
                    print(f"   • RH Responsável: {empresa_salva.get('rh_responsavel')}")
                    print(f"   • Setor: {empresa_salva.get('setor_atividade')}")
                    print(f"   • Funcionários: {empresa_salva.get('num_colaboradores')}")
                    
                    # Remove dados de teste
                    supabase.table("empresas").delete().eq("id", empresa_id).execute()
                    print("🧹 Dados de teste removidos")
                    
                    return True
                else:
                    print("❌ Campo WhatsApp não foi salvo!")
                    return False
            else:
                print("❌ Não foi possível consultar a empresa!")
                return False
        else:
            print("❌ Falha ao inserir empresa!")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        return False

def main():
    """Executa os testes"""
    sucesso = testar_whatsapp_banco()
    
    print("\n" + "="*60)
    print("📊 RESUMO DO TESTE DE WHATSAPP")
    print("="*60)
    
    if sucesso:
        print("🎉 TESTE PASSOU!")
        print("💡 O campo WhatsApp está funcionando corretamente")
    else:
        print("❌ TESTE FALHOU!")
        print("💡 Há problemas com o salvamento do WhatsApp")

if __name__ == "__main__":
    main()
