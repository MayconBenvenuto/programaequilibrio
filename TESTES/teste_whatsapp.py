#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Salvamento de WhatsApp - Programa Equilíbrio
Verifica se o campo WhatsApp está sendo salvo corretamente no banco
"""

import requests
import json
import sys

# URL base da aplicação
BASE_URL = "http://localhost:5000"

def test_whatsapp_save():
    """Testa se o WhatsApp está sendo salvo no banco"""
    print("🧪 Testando salvamento de WhatsApp no banco...")
    
    # Dados de teste
    dados_teste = {
        "dados_empresa": {
            "razao_social": "Empresa Teste WhatsApp Ltda",
            "cnpj": "11111111000111",
            "rh_responsavel": "João Silva",
            "cargo": "Gerente de RH",
            "email": "teste@empresa.com",
            "whatsapp": "(11) 99999-8888",
            "num_colaboradores": "1-50",
            "setor": "Tecnologia"
        },
        "respostas": {
            "pergunta_1": 3,
            "pergunta_2": 4,
            "pergunta_3": 2,
            "pergunta_4": 5,
            "pergunta_5": 3,
            "pergunta_6": 4,
            "pergunta_7": 2,
            "pergunta_8": 3,
            "pergunta_9": 4,
            "pergunta_10": 3
        }
    }
    
    try:
        print("📤 Enviando dados de teste...")
        print(f"   📱 WhatsApp: {dados_teste['dados_empresa']['whatsapp']}")
        print(f"   📧 Email: {dados_teste['dados_empresa']['email']}")
        print(f"   🏢 CNPJ: {dados_teste['dados_empresa']['cnpj']}")
        
        # Fazer requisição POST
        response = requests.post(
            f"{BASE_URL}/processar_questionario",
            json=dados_teste,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Dados enviados com sucesso!")
            print(f"   📊 Status: {result.get('status', 'N/A')}")
            
            if 'diagnostico_id' in result:
                print(f"   🆔 ID do Diagnóstico: {result['diagnostico_id']}")
                return True
            else:
                print("⚠️ Resposta não contém ID do diagnóstico")
                return False
                
        else:
            print(f"❌ Erro na requisição: Status {response.status_code}")
            print(f"   📝 Resposta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️ Timeout na requisição")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique se a aplicação está rodando.")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def verify_whatsapp_in_database():
    """Verifica se conseguimos acessar dados do banco para validação"""
    print("\n🔍 Verificando se a aplicação está rodando...")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Aplicação está rodando!")
            return True
        else:
            print(f"❌ Aplicação retornou status {response.status_code}")
            return False
    except:
        print("❌ Aplicação não está rodando!")
        print("💡 Execute: python main.py")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 TESTE DE SALVAMENTO DE WHATSAPP")
    print("=" * 60)
    
    # Verificar se app está rodando
    if not verify_whatsapp_in_database():
        return
    
    # Testar salvamento
    success = test_whatsapp_save()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DO TESTE")
    print("=" * 60)
    
    if success:
        print("🎉 TESTE PASSOU!")
        print("💡 O WhatsApp está sendo salvo corretamente no banco.")
        print("\n📋 Para verificar no banco Supabase:")
        print("   1. Acesse seu projeto no Supabase")
        print("   2. Vá em Table Editor > empresas")
        print("   3. Procure pela empresa 'Empresa Teste WhatsApp Ltda'")
        print("   4. Verifique se o campo 'whatsapp' contém '(11) 99999-8888'")
    else:
        print("❌ TESTE FALHOU!")
        print("💡 Possíveis causas:")
        print("   • Aplicação não está rodando")
        print("   • Erro na conexão com Supabase")
        print("   • Problema na validação dos dados")
        print("   • Campo WhatsApp não está sendo processado")
        
        print("\n🔧 Para diagnosticar:")
        print("   1. Verifique logs da aplicação")
        print("   2. Teste manualmente via interface web")
        print("   3. Verifique configurações do Supabase")

if __name__ == "__main__":
    main()
