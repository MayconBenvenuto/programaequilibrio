#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para popular o banco de dados com empresas fictícias para demonstração
Execute: python popular_banco_demo.py
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar dependências do projeto
try:
    from main import supabase, converter_faixa_colaboradores, gerar_analise
    print("✅ Dependências do projeto importadas com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar dependências: {e}")
    print("Execute este script a partir do diretório raiz do projeto")
    sys.exit(1)

# Dados fictícios das empresas para demonstração
EMPRESAS_DEMO = [
    {
        "razao_social": "TechNova Solutions Ltda (exemplo)",
        "nome_fantasia": "TechNova (exemplo)",
        "cnpj": "12.345.678/0001-90",
        "email": "rh@technova-exemplo.com",
        "telefone": "(11) 3456-7890",
        "whatsapp": "(11) 94567-8901",
        "endereco": {
            "logradouro": "Av. Paulista, 1000",
            "complemento": "Sala 501",
            "bairro": "Bela Vista",
            "cidade": "São Paulo",
            "uf": "SP",
            "cep": "01310-100"
        },
        "num_colaboradores": "101-250",
        "setor_atividade": "Tecnologia da Informação",
        "rh_responsavel": "Ana Silva (exemplo)",
        "cargo_rh": "Gerente de RH"
    },
    {
        "razao_social": "Indústria MetalMax S.A. (exemplo)",
        "nome_fantasia": "MetalMax (exemplo)",
        "cnpj": "23.456.789/0001-01",
        "email": "recursos.humanos@metalmax-exemplo.com",
        "telefone": "(11) 2345-6789",
        "whatsapp": "(11) 93456-7890",
        "endereco": {
            "logradouro": "Rod. Anhanguera, Km 25",
            "complemento": "Galpão A",
            "bairro": "Distrito Industrial",
            "cidade": "Jundiaí",
            "uf": "SP",
            "cep": "13214-000"
        },
        "num_colaboradores": "501-1000",
        "setor_atividade": "Indústria Metalúrgica",
        "rh_responsavel": "Carlos Mendes (exemplo)",
        "cargo_rh": "Coordenador de Pessoas"
    },
    {
        "razao_social": "ConsultPro Assessoria Empresarial Ltda (exemplo)",
        "nome_fantasia": "ConsultPro (exemplo)",
        "cnpj": "34.567.890/0001-12",
        "email": "gestao@consultpro-exemplo.com",
        "telefone": "(11) 3567-8901",
        "whatsapp": "(11) 95678-9012",
        "endereco": {
            "logradouro": "R. Augusta, 2500",
            "complemento": "Conjunto 1203",
            "bairro": "Jardins",
            "cidade": "São Paulo",
            "uf": "SP",
            "cep": "01412-100"
        },
        "num_colaboradores": "51-100",
        "setor_atividade": "Consultoria Empresarial",
        "rh_responsavel": "Mariana Costa (exemplo)",
        "cargo_rh": "Analista de RH Sênior"
    },
    {
        "razao_social": "EcoVerde Sustentabilidade Ltda (exemplo)",
        "nome_fantasia": "EcoVerde (exemplo)",
        "cnpj": "45.678.901/0001-23",
        "email": "pessoas@ecoverde-exemplo.com",
        "telefone": "(11) 4567-8901",
        "whatsapp": "(11) 96789-0123",
        "endereco": {
            "logradouro": "Av. Faria Lima, 3000",
            "complemento": "14º andar",
            "bairro": "Itaim Bibi",
            "cidade": "São Paulo",
            "uf": "SP",
            "cep": "04538-132"
        },
        "num_colaboradores": "251-500",
        "setor_atividade": "Sustentabilidade e Meio Ambiente",
        "rh_responsavel": "Roberto Lima (exemplo)",
        "cargo_rh": "Diretor de Gente & Gestão"
    },
    {
        "razao_social": "LogiTransporte Express Ltda (exemplo)",
        "nome_fantasia": "LogiExpress (exemplo)",
        "cnpj": "56.789.012/0001-34",
        "email": "rh@logiexpress-exemplo.com",
        "telefone": "(11) 5678-9012",
        "whatsapp": "(11) 97890-1234",
        "endereco": {
            "logradouro": "R. do Porto, 500",
            "complemento": "",
            "bairro": "Centro",
            "cidade": "Santos",
            "uf": "SP",
            "cep": "11010-140"
        },
        "num_colaboradores": "101-250",
        "setor_atividade": "Logística e Transporte",
        "rh_responsavel": "Fernanda Oliveira (exemplo)",
        "cargo_rh": "Supervisora de RH"
    },
    {
        "razao_social": "CreativeAgency Publicidade Ltda (exemplo)",
        "nome_fantasia": "Creative Agency (exemplo)",
        "cnpj": "67.890.123/0001-45",
        "email": "talento@creative-exemplo.com",
        "telefone": "(11) 6789-0123",
        "whatsapp": "(11) 98901-2345",
        "endereco": {
            "logradouro": "R. Oscar Freire, 1200",
            "complemento": "Cobertura",
            "bairro": "Jardins",
            "cidade": "São Paulo",
            "uf": "SP",
            "cep": "01426-001"
        },
        "num_colaboradores": "51-100",
        "setor_atividade": "Publicidade e Marketing",
        "rh_responsavel": "Julia Santos (exemplo)",
        "cargo_rh": "People & Culture Manager"
    },
    {
        "razao_social": "HealthCare Plus Serviços Médicos Ltda (exemplo)",
        "nome_fantasia": "HealthCare Plus (exemplo)",
        "cnpj": "78.901.234/0001-56",
        "email": "administrativo@healthcare-exemplo.com",
        "telefone": "(11) 7890-1234",
        "whatsapp": "(11) 99012-3456",
        "endereco": {
            "logradouro": "Av. Dr. Arnaldo, 800",
            "complemento": "Bloco B",
            "bairro": "Sumaré",
            "cidade": "São Paulo",
            "uf": "SP",
            "cep": "01246-903"
        },
        "num_colaboradores": "1000+",
        "setor_atividade": "Serviços de Saúde",
        "rh_responsavel": "Dr. Eduardo Pereira (exemplo)",
        "cargo_rh": "Gerente Administrativo"
    },
    {
        "razao_social": "EduFuturo Instituto de Ensino Ltda (exemplo)",
        "nome_fantasia": "EduFuturo (exemplo)",
        "cnpj": "89.012.345/0001-67",
        "email": "coordenacao@edufuturo-exemplo.com",
        "telefone": "(11) 8901-2345",
        "whatsapp": "(11) 90123-4567",
        "endereco": {
            "logradouro": "R. Consolação, 2000",
            "complemento": "Prédio Principal",
            "bairro": "Consolação",
            "cidade": "São Paulo",
            "uf": "SP",
            "cep": "01302-001"
        },
        "num_colaboradores": "251-500",
        "setor_atividade": "Educação",
        "rh_responsavel": "Profa. Lucia Rodrigues (exemplo)",
        "cargo_rh": "Coordenadora de Recursos Humanos"
    },
    {
        "razao_social": "RetailShop Comércio e Varejo Ltda (exemplo)",
        "nome_fantasia": "RetailShop (exemplo)",
        "cnpj": "90.123.456/0001-78",
        "email": "gestao@retailshop-exemplo.com",
        "telefone": "(11) 9012-3456",
        "whatsapp": "(11) 91234-5678",
        "endereco": {
            "logradouro": "Av. Rebouças, 3000",
            "complemento": "Loja Térrea",
            "bairro": "Pinheiros",
            "cidade": "São Paulo",
            "uf": "SP",
            "cep": "05402-600"
        },
        "num_colaboradores": "101-250",
        "setor_atividade": "Comércio e Varejo",
        "rh_responsavel": "Pedro Almeida (exemplo)",
        "cargo_rh": "Analista de Pessoas"
    },
    {
        "razao_social": "FinanceMax Gestão Financeira S.A. (exemplo)",
        "nome_fantasia": "FinanceMax (exemplo)",
        "cnpj": "01.234.567/0001-89",
        "email": "recursos@financemax-exemplo.com",
        "telefone": "(11) 0123-4567",
        "whatsapp": "(11) 92345-6789",
        "endereco": {
            "logradouro": "Av. Brigadeiro Faria Lima, 4000",
            "complemento": "25º andar",
            "bairro": "Vila Olímpia",
            "cidade": "São Paulo",
            "uf": "SP",
            "cep": "04538-132"
        },
        "num_colaboradores": "501-1000",
        "setor_atividade": "Serviços Financeiros",
        "rh_responsavel": "Beatriz Ferreira (exemplo)",
        "cargo_rh": "Head de People Experience"
    }
]

# Respostas variadas para gerar diagnósticos diferentes
RESPOSTAS_VARIEDADE = [
    # Perfil 1: Baixo risco
    {
        '1': ['clima_organizacional'],
        '2': ['frequencia_baixa'],
        '3': ['programa_completo'],
        '4': ['comunicacao_excelente'],
        '5': ['nivel_alto'],
        '6': ['beneficios_excelentes'],
        '7': ['sistema_completo'],
        '8': ['comunicacao_excelente'],
        '9': ['equipamento_ergonomico'],
        '10': ['treinamento_completo'],
        '11': ['feedback_constante'],
        '12': ['politicas_completas']
    },
    # Perfil 2: Risco moderado
    {
        '1': ['alta_carga', 'clima_organizacional'],
        '2': ['frequencia_moderada'],
        '3': ['programa_basico'],
        '4': ['comunicacao_regular'],
        '5': ['nivel_medio'],
        '6': ['beneficios_tradicionais'],
        '7': ['sistema_basico'],
        '8': ['comunicacao_regular'],
        '9': ['equipamento_adequado'],
        '10': ['treinamento_regular'],
        '11': ['feedback_regular'],
        '12': ['politicas_basicas']
    },
    # Perfil 3: Alto risco
    {
        '1': ['alta_carga', 'metas_excessivas', 'falta_reconhecimento'],
        '2': ['frequencia_alta'],
        '3': ['programa_inexistente'],
        '4': ['comunicacao_deficiente'],
        '5': ['nivel_baixo'],
        '6': ['beneficios_limitados'],
        '7': ['sistema_inexistente'],
        '8': ['comunicacao_limitada'],
        '9': ['equipamento_inadequado'],
        '10': ['treinamento_basico'],
        '11': ['feedback_limitado'],
        '12': ['politicas_basicas']
    },
    # Perfil 4: Misto (variado)
    {
        '1': ['alta_carga'],
        '2': ['frequencia_moderada'],
        '3': ['programa_basico'],
        '4': ['comunicacao_deficiente'],
        '5': ['nivel_medio'],
        '6': ['beneficios_tradicionais'],
        '7': ['sistema_basico'],
        '8': ['comunicacao_regular'],
        '9': ['equipamento_adequado'],
        '10': ['treinamento_basico'],
        '11': ['feedback_regular'],
        '12': ['politicas_completas']
    }
]

def gerar_data_aleatoria(dias_atras_min=1, dias_atras_max=180):
    """Gera uma data aleatória nos últimos X dias"""
    hoje = datetime.now()
    dias_atras = random.randint(dias_atras_min, dias_atras_max)
    data_gerada = hoje - timedelta(days=dias_atras)
    return data_gerada.isoformat()

def cadastrar_empresa_completa(dados_empresa):
    """Cadastra uma empresa completa com diagnóstico"""
    
    if not supabase:
        print("❌ ERRO: Supabase não configurado")
        return False
        
    try:
        print(f"\n📋 Processando: {dados_empresa['razao_social']}")
        
        # Converter num_colaboradores para inteiro
        num_colaboradores_int = converter_faixa_colaboradores(dados_empresa['num_colaboradores'])
        
        # Preparar dados da empresa
        dados_empresa_bd = {
            'razao_social': dados_empresa['razao_social'],
            'nome_fantasia': dados_empresa['nome_fantasia'],
            'cnpj': dados_empresa['cnpj'],
            'email': dados_empresa['email'],
            'telefone': dados_empresa['telefone'],
            'whatsapp': dados_empresa['whatsapp'],
            'endereco': dados_empresa['endereco'],
            'num_colaboradores': num_colaboradores_int,
            'setor_atividade': dados_empresa['setor_atividade'],
            'rh_responsavel': dados_empresa['rh_responsavel'],
            'cargo_rh': dados_empresa['cargo_rh'],
            'created_at': gerar_data_aleatoria(),
            'updated_at': gerar_data_aleatoria()
        }
        
        # Inserir empresa
        print("   👔 Cadastrando empresa...")
        empresa_result = supabase.table('empresas').insert(dados_empresa_bd).execute()
        
        if not empresa_result.data:
            print(f"   ❌ Falha ao cadastrar empresa")
            return False
            
        empresa_id = empresa_result.data[0]['id']
        print(f"   ✅ Empresa cadastrada - ID: {empresa_id}")
        
        # Gerar respostas variadas
        respostas = random.choice(RESPOSTAS_VARIEDADE)
        
        # Gerar análise
        print("   🧠 Gerando análise...")
        analise = gerar_analise(respostas)
        
        # Dados do diagnóstico
        data_diagnostico = gerar_data_aleatoria(1, 90)  # Últimos 3 meses
        dados_diagnostico = {
            'empresa_id': empresa_id,
            'respostas': respostas,
            'analise': analise,
            'nivel_risco': analise.get('nivel_risco', 'Baixo'),
            'questoes_criticas': analise.get('questoes_criticas', 0),
            'areas_foco': analise.get('areas_foco', []),
            'acoes_recomendadas': analise.get('acoes_recomendadas', []),
            'status': 'concluido',
            'created_at': data_diagnostico,
            'updated_at': data_diagnostico
        }
        
        # Inserir diagnóstico
        print("   📊 Cadastrando diagnóstico...")
        diagnostico_result = supabase.table('diagnosticos').insert(dados_diagnostico).execute()
        
        if diagnostico_result.data:
            diagnostico_id = diagnostico_result.data[0]['id']
            print(f"   ✅ Diagnóstico cadastrado - ID: {diagnostico_id}")
            print(f"   🎯 Nível de risco: {analise.get('nivel_risco', 'Baixo')}")
            return True
        else:
            print(f"   ❌ Falha ao cadastrar diagnóstico")
            return False
            
    except Exception as e:
        print(f"   ❌ ERRO ao processar {dados_empresa['razao_social']}: {str(e)}")
        return False

def main():
    print("🏢 SCRIPT DE POPULAÇÃO DO BANCO DE DADOS")
    print("=====================================")
    print("Este script vai cadastrar 10 empresas fictícias para demonstração")
    print("")
    
    # Verificar conexão com Supabase
    if not supabase:
        print("❌ ERRO: Não foi possível conectar ao Supabase")
        print("Verifique as variáveis de ambiente SUPABASE_URL e SUPABASE_ANON_KEY")
        return
        
    print("✅ Conexão com Supabase estabelecida")
    
    # Confirmar execução
    resposta = input("\n🤔 Deseja prosseguir com o cadastro das empresas? (s/n): ").lower()
    if resposta != 's':
        print("❌ Operação cancelada pelo usuário")
        return
    
    print("\n🚀 Iniciando cadastro das empresas...\n")
    
    sucessos = 0
    falhas = 0
    
    for i, empresa in enumerate(EMPRESAS_DEMO, 1):
        print(f"📈 Progresso: {i}/10")
        
        if cadastrar_empresa_completa(empresa):
            sucessos += 1
            print("   ✅ Sucesso!")
        else:
            falhas += 1
            print("   ❌ Falhou!")
            
    print(f"\n{'='*50}")
    print("📊 RELATÓRIO FINAL")
    print(f"{'='*50}")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"📈 Total: {sucessos + falhas}")
    
    if sucessos > 0:
        print(f"\n🎉 {sucessos} empresas foram cadastradas com sucesso!")
        print("📊 Agora você pode visualizar os dados no painel administrativo")
        print("🌐 Acesse: https://programaequilibrio.vercel.app/admin")
    
    if falhas > 0:
        print(f"\n⚠️ {falhas} empresas falharam no cadastro")
        print("Verifique os logs acima para mais detalhes")

if __name__ == "__main__":
    main()
