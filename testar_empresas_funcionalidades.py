#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar as funcionalidades de Ver Detalhes e Exportar PDF
das empresas no painel administrativo.
"""

import sys
import os
import requests
import json
from urllib.parse import quote, unquote

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurações
BASE_URL = "http://localhost:5000"
ADMIN_LOGIN_URL = f"{BASE_URL}/admin/login"
EMPRESAS_URL = f"{BASE_URL}/admin/empresas"

def fazer_login_admin(session):
    """Faz login no painel administrativo"""
    print("🔐 Fazendo login como admin...")
    
    # Primeiro, pegar a página de login para obter o token CSRF se necessário
    login_page = session.get(ADMIN_LOGIN_URL)
    
    # Dados de login (usando as credenciais do sistema)
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    # Fazer login
    response = session.post(ADMIN_LOGIN_URL, data=login_data, allow_redirects=False)
    
    if response.status_code == 302 or response.status_code == 200:
        print("✅ Login realizado com sucesso")
        return True
    else:
        print(f"❌ Erro no login: {response.status_code}")
        return False

def testar_detalhes_empresa(session, cnpj):
    """Testa a funcionalidade Ver Detalhes da empresa"""
    print(f"\n🔍 Testando Ver Detalhes para CNPJ: {cnpj}")
    
    # Codificar CNPJ para URL
    cnpj_encoded = quote(cnpj)
    detalhes_url = f"{BASE_URL}/admin/empresa_detalhes/{cnpj_encoded}"
    
    print(f"📋 URL de teste: {detalhes_url}")
    
    try:
        response = session.get(detalhes_url)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Detalhes obtidos com sucesso!")
            print(f"   📊 Dados recebidos:")
            print(f"   - Razão Social: {data.get('razao_social', 'N/A')}")
            print(f"   - CNPJ: {data.get('cnpj', 'N/A')}")
            print(f"   - RH Responsável: {data.get('rh_responsavel', 'N/A')}")
            print(f"   - Nível de Risco: {data.get('nivel_risco', 'N/A')}")
            print(f"   - Data Diagnóstico: {data.get('data_diagnostico', 'N/A')}")
            return True
        elif response.status_code == 404:
            print("❌ Empresa não encontrada (404)")
            return False
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def testar_exportar_pdf(session, cnpj):
    """Testa a funcionalidade Exportar PDF da empresa"""
    print(f"\n📄 Testando Exportar PDF para CNPJ: {cnpj}")
    
    # Codificar CNPJ para URL
    cnpj_encoded = quote(cnpj)
    pdf_url = f"{BASE_URL}/admin/exportar_empresa_pdf/{cnpj_encoded}"
    
    print(f"📋 URL de teste: {pdf_url}")
    
    try:
        response = session.get(pdf_url)
        
        if response.status_code == 200:
            # Verificar se realmente é um PDF
            content_type = response.headers.get('content-type', '')
            if 'pdf' in content_type.lower():
                print("✅ PDF gerado com sucesso!")
                print(f"   📊 Content-Type: {content_type}")
                print(f"   📊 Tamanho: {len(response.content)} bytes")
                
                # Salvar PDF para verificação manual (opcional)
                cnpj_clean = cnpj.replace('/', '_').replace('.', '_').replace('-', '_')
                filename = f"teste_pdf_{cnpj_clean}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   💾 PDF salvo como: {filename}")
                return True
            else:
                print(f"❌ Resposta não é um PDF. Content-Type: {content_type}")
                print(f"   Conteúdo: {response.text[:200]}...")
                return False
        elif response.status_code == 404:
            print("❌ Empresa não encontrada (404)")
            return False
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def listar_empresas(session):
    """Lista algumas empresas cadastradas para teste"""
    print("\n📋 Buscando empresas cadastradas...")
    
    try:
        response = session.get(EMPRESAS_URL)
        
        if response.status_code == 200:
            print("✅ Página de empresas acessada com sucesso")
            
            # Procurar por CNPJs na página HTML (método simples)
            content = response.text
            
            # Extrair CNPJs do HTML usando regex simples
            import re
            cnpj_pattern = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
            cnpjs = re.findall(cnpj_pattern, content)
            
            if cnpjs:
                print(f"   📊 Encontrados {len(cnpjs)} CNPJs:")
                for i, cnpj in enumerate(cnpjs[:5], 1):  # Mostrar apenas os primeiros 5
                    print(f"   {i}. {cnpj}")
                return cnpjs[:3]  # Retornar os primeiros 3 para teste
            else:
                print("   ⚠️ Nenhum CNPJ encontrado na página")
                return []
        else:
            print(f"❌ Erro ao acessar página de empresas: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return []

def main():
    print("🚀 INICIANDO TESTES DAS FUNCIONALIDADES DE EMPRESAS")
    print("=" * 60)
    
    # Criar sessão para manter cookies
    session = requests.Session()
    
    try:
        # 1. Fazer login
        if not fazer_login_admin(session):
            print("❌ Não foi possível fazer login. Verifique as credenciais.")
            return
        
        # 2. Listar empresas
        cnpjs_teste = listar_empresas(session)
        
        if not cnpjs_teste:
            print("\n⚠️ Nenhuma empresa encontrada para teste.")
            print("💡 Sugestão: Execute o script 'popular_banco_demo.py' primeiro.")
            return
        
        # 3. Testar funcionalidades para cada CNPJ
        sucessos_detalhes = 0
        sucessos_pdf = 0
        
        for cnpj in cnpjs_teste:
            print(f"\n{'=' * 40}")
            print(f"🏢 TESTANDO EMPRESA: {cnpj}")
            print(f"{'=' * 40}")
            
            # Testar Ver Detalhes
            if testar_detalhes_empresa(session, cnpj):
                sucessos_detalhes += 1
            
            # Testar Exportar PDF
            if testar_exportar_pdf(session, cnpj):
                sucessos_pdf += 1
        
        # 4. Relatório final
        print(f"\n{'=' * 60}")
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print(f"{'=' * 60}")
        print(f"🏢 Empresas testadas: {len(cnpjs_teste)}")
        print(f"✅ Ver Detalhes funcionando: {sucessos_detalhes}/{len(cnpjs_teste)}")
        print(f"📄 Exportar PDF funcionando: {sucessos_pdf}/{len(cnpjs_teste)}")
        
        if sucessos_detalhes == len(cnpjs_teste) and sucessos_pdf == len(cnpjs_teste):
            print("\n🎉 TODOS OS TESTES PASSARAM! ✅")
        elif sucessos_detalhes > 0 or sucessos_pdf > 0:
            print("\n⚠️ ALGUNS TESTES FALHARAM - Verifique os logs acima")
        else:
            print("\n❌ TODOS OS TESTES FALHARAM - Verifique a configuração")
    
    except KeyboardInterrupt:
        print("\n🛑 Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'=' * 60}")
    print("🏁 TESTES FINALIZADOS")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
