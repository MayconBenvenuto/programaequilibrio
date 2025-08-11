#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO DE CONFIGURAÇÃO VERCEL
Identifica problemas de configuração em produção
"""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def diagnosticar_configuracao():
    """Diagnostica configurações essenciais"""
    print("="*80)
    print("🔍 DIAGNÓSTICO DE CONFIGURAÇÃO PARA VERCEL")
    print("="*80)
    
    # Verificar variáveis de ambiente essenciais
    variaveis_essenciais = [
        ('SUPABASE_URL', 'URL do banco de dados Supabase'),
        ('SUPABASE_ANON_KEY', 'Chave anônima do Supabase'),
        ('FLASK_SECRET_KEY', 'Chave secreta do Flask'),
        ('ADMIN_EMAIL', 'Email do administrador'),
        ('ADMIN_PASSWORD', 'Senha do administrador')
    ]
    
    print("📋 VERIFICANDO VARIÁVEIS DE AMBIENTE:")
    problemas = []
    
    for var, desc in variaveis_essenciais:
        valor = os.getenv(var)
        if valor:
            # Mascarar valores sensíveis
            if 'KEY' in var or 'PASSWORD' in var:
                valor_mostrado = f"{valor[:8]}...{valor[-4:]}" if len(valor) > 12 else "***"
            else:
                valor_mostrado = valor
            print(f"   ✅ {var}: {valor_mostrado}")
        else:
            print(f"   ❌ {var}: NÃO ENCONTRADA - {desc}")
            problemas.append((var, desc))
    
    return problemas

def gerar_guia_vercel():
    """Gera guia de configuração para Vercel"""
    print(f"\n📄 GERANDO GUIA DE CONFIGURAÇÃO PARA VERCEL:")
    
    # Valores das variáveis (do .env atual)
    variaveis = {
        'FLASK_ENV': 'production',
        'DEBUG': 'false',
        'FLASK_SECRET_KEY': os.getenv('FLASK_SECRET_KEY', 'ProgramaEquilibrio2025!@#$%SuperSecretKey789XYZ'),
        'SUPABASE_URL': os.getenv('SUPABASE_URL', 'https://xzjbnohtfuppilpzvvqy.supabase.co'),
        'SUPABASE_ANON_KEY': os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6amJub2h0ZnVwcGlscHp2dnF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ5MjUzOTgsImV4cCI6MjA3MDUwMTM5OH0.qXDZrGjacFYOOdQcftzBj1Zkutt3jTIf-tjGFsb3Za8'),
        'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL', 'admin@conecta.com'),
        'ADMIN_PASSWORD': os.getenv('ADMIN_PASSWORD', 'Admin123!Conecta'),
        'ADMIN_NAME': 'Administrador Sistema',
        'RECEITAWS_API_URL': 'https://www.receitaws.com.br/v1/cnpj/',
        'VIACEP_API_URL': 'https://viacep.com.br/ws/',
        'SESSION_COOKIE_SECURE': 'true',
        'SESSION_COOKIE_HTTPONLY': 'true',
        'PERMANENT_SESSION_LIFETIME': '3600'
    }
    
    # Gerar conteúdo
    conteudo = []
    conteudo.append("# ====================================================================")
    conteudo.append("# CONFIGURAÇÃO DE VARIÁVEIS DE AMBIENTE PARA VERCEL")
    conteudo.append("# ====================================================================")
    conteudo.append("#")
    conteudo.append("# INSTRUÇÕES:")
    conteudo.append("# 1. Acesse: https://vercel.com/dashboard")
    conteudo.append("# 2. Selecione seu projeto 'programaequilibrio'")
    conteudo.append("# 3. Vá em 'Settings' > 'Environment Variables'")
    conteudo.append("# 4. Adicione cada variável abaixo:")
    conteudo.append("#")
    conteudo.append("# VARIÁVEIS OBRIGATÓRIAS:")
    conteudo.append("")
    
    for var, valor in variaveis.items():
        if valor:
            conteudo.append(f"# {var}")
            conteudo.append(f"{var}={valor}")
            conteudo.append("")
    
    conteudo.append("# ====================================================================")
    conteudo.append("# APÓS CONFIGURAR:")
    conteudo.append("# 1. Clique em 'Redeploy' no painel da Vercel")
    conteudo.append("# 2. Aguarde o deploy completar")
    conteudo.append("# 3. Teste a aplicação")
    conteudo.append("# ====================================================================")
    
    # Salvar arquivo
    with open('VERCEL_CONFIG_VARS.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(conteudo))
    
    print("   ✅ Arquivo 'VERCEL_CONFIG_VARS.txt' criado")

def main():
    problemas = diagnosticar_configuracao()
    gerar_guia_vercel()
    
    print("\n" + "="*80)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("="*80)
    
    if not problemas:
        print("🎉 CONFIGURAÇÃO LOCALMENTE OK!")
        print("✅ Todas as variáveis de ambiente estão configuradas localmente")
        print("")
        print("🚨 PROBLEMA IDENTIFICADO:")
        print("   O erro 'Internal Server Error' em produção indica que")
        print("   as variáveis de ambiente NÃO ESTÃO configuradas na Vercel!")
        print("")
        print("🔧 SOLUÇÃO:")
        print("   1. Use o arquivo 'VERCEL_CONFIG_VARS.txt' gerado")
        print("   2. Configure cada variável no painel da Vercel")
        print("   3. Faça um redeploy")
    else:
        print("❌ PROBLEMAS LOCAIS ENCONTRADOS!")
        print(f"🔧 {len(problemas)} variáveis faltando localmente:")
        for var, desc in problemas:
            print(f"   - {var}: {desc}")
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. 📋 Abra o arquivo 'VERCEL_CONFIG_VARS.txt'")
    print("2. 🌐 Acesse https://vercel.com/dashboard")
    print("3. ⚙️  Configure as variáveis de ambiente")
    print("4. 🚀 Faça um redeploy")
    print("5. 🧪 Teste a aplicação em produção")
    
    return len(problemas) == 0

if __name__ == "__main__":
    main()
