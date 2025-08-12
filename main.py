import sys
import os
from flask import Flask, render_template, request, jsonify, send_file, url_for, redirect, session, flash
import json
import re
from datetime import datetime
import io
import base64
import requests

# Importações condicionais para evitar erros na Vercel
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.units import inch
    PDF_GENERATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ [IMPORT] PDF generation não disponível: {e}")
    PDF_GENERATION_AVAILABLE = False

try:
    from supabase import create_client, Client
    SUPABASE_MODULE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ [IMPORT] Supabase module não disponível: {e}")
    SUPABASE_MODULE_AVAILABLE = False

try:
    from decouple import config
    CONFIG_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ [IMPORT] Decouple não disponível: {e}")
    CONFIG_AVAILABLE = False
    # Fallback para usar os.environ diretamente
    def config(key, default=None, cast=None):
        value = os.environ.get(key, default)
        if cast and value is not None:
            try:
                return cast(value)
            except (ValueError, TypeError):
                return default
        return value

try:
    from validate_docbr import CNPJ
    import hashlib
    import secrets
    from functools import wraps
    VALIDATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ [IMPORT] Validation libraries não disponíveis: {e}")
    VALIDATION_AVAILABLE = False
    # Definir validação básica de fallback
    def validar_cnpj(cnpj):
        if not cnpj:
            return False
        digits = re.sub(r'\D', '', cnpj)
        return len(digits) == 14
    
    import hashlib
    import secrets
    from functools import wraps

print(f"📋 [STARTUP] Status das dependências:")
print(f"   PDF Generation: {PDF_GENERATION_AVAILABLE}")  
print(f"   Supabase Module: {SUPABASE_MODULE_AVAILABLE}")
print(f"   Config: {CONFIG_AVAILABLE}")
print(f"   Validation: {VALIDATION_AVAILABLE}")
from validate_docbr import CNPJ
import hashlib
import secrets
from functools import wraps

app = Flask(__name__)

# Configurações da aplicação usando variáveis de ambiente
app.secret_key = config('FLASK_SECRET_KEY', default='dev-key-change-in-production')
app.config['DEBUG'] = config('DEBUG', default=False, cast=bool)
app.config['PERMANENT_SESSION_LIFETIME'] = config('PERMANENT_SESSION_LIFETIME', default=3600, cast=int)

# Configurações de segurança - ajustadas para funcionar em dev e produção
import os
is_production = os.environ.get('VERCEL') or os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_SECURE'] = config('SESSION_COOKIE_SECURE', default=is_production, cast=bool)
app.config['SESSION_COOKIE_HTTPONLY'] = config('SESSION_COOKIE_HTTPONLY', default=True, cast=bool)
app.config['SESSION_COOKIE_SAMESITE'] = config('SESSION_COOKIE_SAMESITE', default='Lax')

# Configuração simples que funciona na Vercel
app.static_folder = 'static'
app.template_folder = 'templates'

print(f"🔧 [CONFIG] Is production: {is_production}")
print(f"🔧 [CONFIG] Static folder: {app.static_folder}")
print(f"🔧 [CONFIG] Template folder: {app.template_folder}")

# Configuração do Supabase com tratamento robusto
supabase = None
try:
    SUPABASE_URL = config('SUPABASE_URL', default='')
    SUPABASE_KEY = config('SUPABASE_ANON_KEY', default=config('SUPABASE_KEY', default=''))
    
    if SUPABASE_URL and SUPABASE_KEY and SUPABASE_MODULE_AVAILABLE:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ [SUPABASE] Cliente configurado com sucesso")
    else:
        print("⚠️ [SUPABASE] Configurações incompletas ou módulo indisponível")
        print(f"   URL presente: {bool(SUPABASE_URL)}")
        print(f"   KEY presente: {bool(SUPABASE_KEY)}")
        print(f"   Módulo disponível: {SUPABASE_MODULE_AVAILABLE}")
except Exception as e:
    print(f"❌ [SUPABASE] Erro na inicialização: {str(e)}")
    supabase = None

# Validador de CNPJ
cnpj_validator = CNPJ()

# APIs externas
RECEITAWS_API_URL = config('RECEITAWS_API_URL', default='https://www.receitaws.com.br/v1/cnpj/')
RECEITAWS_TIMEOUT = config('RECEITAWS_TIMEOUT', default=15, cast=int)
VIACEP_API_URL = config('VIACEP_API_URL', default='https://viacep.com.br/ws/')
VIACEP_TIMEOUT = config('VIACEP_TIMEOUT', default=10, cast=int)

# Configurações de administração
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@conecta.com')
ADMIN_PASSWORD = config('ADMIN_PASSWORD', default='admin123')
ADMIN_NAME = config('ADMIN_NAME', default='Administrador')
ADMIN_SESSION_TIMEOUT = config('ADMIN_SESSION_TIMEOUT', default=7200, cast=int)

def requires_admin(f):
    """Decorator para rotas que requerem autenticação de admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def validar_cnpj(cnpj):
    """Valida CNPJ usando a biblioteca validate-docbr"""
    if not cnpj:
        return False
    
    # Remove formatação
    cnpj_limpo = re.sub(r'[^\d]', '', cnpj)
    
    return cnpj_validator.validate(cnpj_limpo)

def consultar_cnpj_receita_ws(cnpj):
    """Consulta dados da empresa na ReceitaWS"""
    try:
        # Remove formatação do CNPJ
        cnpj_limpo = re.sub(r'[^\d]', '', cnpj)
        print(f"🔍 [ReceitaWS] Consultando CNPJ: {cnpj_limpo}")
        
        # Faz a requisição para a API usando timeout configurado
        response = requests.get(f"{RECEITAWS_API_URL}{cnpj_limpo}", timeout=RECEITAWS_TIMEOUT)
        print(f"📡 [ReceitaWS] Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📋 [ReceitaWS] Dados brutos recebidos:")
            print(f"   Status API: {data.get('status', 'N/A')}")
            print(f"   Nome: {data.get('nome', 'N/A')}")
            print(f"   Fantasia: {data.get('fantasia', 'N/A')}")
            print(f"   Situação: {data.get('situacao', 'N/A')}")
            print(f"   Município: {data.get('municipio', 'N/A')}")
            print(f"   UF: {data.get('uf', 'N/A')}")
            
            # Verifica se houve erro na consulta
            if data.get('status') == 'ERROR':
                print(f"❌ [ReceitaWS] API retornou erro: {data.get('message', 'Erro não especificado')}")
                return None
            
            resultado = {
                'razao_social': data.get('nome', ''),
                'nome_fantasia': data.get('fantasia', ''),
                'cnpj': cnpj_limpo,
                'situacao': data.get('situacao', ''),
                'atividade_principal': data.get('atividade_principal', [{}])[0].get('text', '') if data.get('atividade_principal') else '',
                'endereco': {
                    'logradouro': data.get('logradouro', ''),
                    'numero': data.get('numero', ''),
                    'complemento': data.get('complemento', ''),
                    'bairro': data.get('bairro', ''),
                    'municipio': data.get('municipio', ''),
                    'uf': data.get('uf', ''),
                    'cep': data.get('cep', '')
                },
                'telefone': data.get('telefone', ''),
                'email': data.get('email', ''),
                'data_abertura': data.get('abertura', '')
            }
            
            print(f"✅ [ReceitaWS] Dados processados:")
            print(f"   Razão Social: '{resultado.get('razao_social')}'")
            print(f"   Situação: '{resultado.get('situacao')}'")
            print(f"   Tem razão social: {bool(resultado.get('razao_social'))}")
            
            return resultado
        else:
            print(f"❌ [ReceitaWS] Erro HTTP {response.status_code}: {response.text[:200]}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ [ReceitaWS] Erro de requisição: {e}")
        return None
    except Exception:
        return None

def consultar_brasilapi(cnpj):
    """Consulta CNPJ na BrasilAPI com tratamento adequado"""
    try:
        # Remove caracteres especiais do CNPJ
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verifica se tem dados essenciais
            if not data.get('legal_name'):
                return None
            
            # Converte para formato compatível com ReceitaWS
            return {
                'razao_social': data.get('legal_name', ''),
                'nome_fantasia': data.get('trade_name', ''),
                'cnpj': cnpj_limpo,
                'situacao': data.get('registration_status', ''),
                'atividade_principal': '',  # BrasilAPI tem estrutura diferente
                'endereco': {
                    'logradouro': data.get('address', {}).get('street', ''),
                    'numero': data.get('address', {}).get('number', ''),
                    'complemento': data.get('address', {}).get('details', ''),
                    'bairro': data.get('address', {}).get('district', ''),
                    'municipio': data.get('address', {}).get('city', ''),
                    'uf': data.get('address', {}).get('state', ''),
                    'cep': data.get('address', {}).get('zip_code', '')
                },
                'telefone': data.get('phone', ''),
                'email': data.get('email', ''),
                'data_abertura': data.get('founded', '')
            }
            
        return None
            
    except Exception as e:
        print(f"Erro na BrasilAPI: {e}")
        return None

def consultar_cnpj_com_fallback(cnpj):
    """
    Consulta CNPJ usando múltiplas APIs como fallback
    1. Tenta BrasilAPI primeiro (mais rápida e sem limite rigoroso)
    2. Se falhar, usa ReceitaWS
    """
    print(f"🔍 [FALLBACK] Consultando CNPJ: {cnpj}")
    
    # Primeira tentativa: BrasilAPI
    print("📡 [FALLBACK] Tentativa 1: BrasilAPI...")
    resultado = consultar_brasilapi(cnpj)
    
    if resultado and resultado.get('razao_social'):
        print(f"✅ [FALLBACK] Sucesso com BrasilAPI!")
        print(f"   Razão Social encontrada: '{resultado.get('razao_social')}'")
        return resultado
    else:
        print("⚠️ [FALLBACK] BrasilAPI não retornou dados completos")
        if resultado:
            print(f"   Dados BrasilAPI: razao_social='{resultado.get('razao_social')}', situacao='{resultado.get('situacao')}'")
    
    # Segunda tentativa: ReceitaWS
    print("📡 [FALLBACK] Tentativa 2: ReceitaWS...")
    resultado = consultar_cnpj_receita_ws(cnpj)
    
    if resultado and resultado.get('razao_social'):
        print(f"✅ [FALLBACK] Sucesso com ReceitaWS!")
        print(f"   Razão Social encontrada: '{resultado.get('razao_social')}'")
        return resultado
    else:
        print("⚠️ [FALLBACK] ReceitaWS não retornou dados completos")
        if resultado:
            print(f"   Dados ReceitaWS: razao_social='{resultado.get('razao_social')}', situacao='{resultado.get('situacao')}'")
    
    # Se ambas falharam
    print("❌ [FALLBACK] Nenhuma API retornou dados válidos")
    print(f"   BrasilAPI resultado: {type(resultado)}")
    print(f"   ReceitaWS resultado: {type(resultado)}")
    return None
    
    # Segunda tentativa: ReceitaWS
    print("📡 Tentativa 2: ReceitaWS...")
    resultado = consultar_cnpj_receita_ws(cnpj)
    
    if resultado and resultado.get('razao_social'):
        print("✅ Sucesso com ReceitaWS!")
        return resultado
    else:
        print("⚠️ ReceitaWS não retornou dados completos")
    
    # Se ambas falharam
    print("❌ Nenhuma API retornou dados válidos")
    return None

def converter_faixa_colaboradores(faixa_str):
    """Converte faixa de colaboradores (string) para número inteiro médio"""
    if not faixa_str or faixa_str == '':
        return 0
    
    # Mapeamento das faixas para valores médios
    mapeamento_faixas = {
        '1-50': 25,
        '51-100': 75,
        '101-250': 175,
        '251-500': 375,
        '501-1000': 750,
        '1000+': 1500
    }
    
    # Se for um número diretamente, retornar como int
    if str(faixa_str).isdigit():
        return int(faixa_str)
    
    # Buscar no mapeamento
    faixa_normalizada = str(faixa_str).strip()
    if faixa_normalizada in mapeamento_faixas:
        print(f"🔄 Convertendo '{faixa_str}' para {mapeamento_faixas[faixa_normalizada]} colaboradores")
        return mapeamento_faixas[faixa_normalizada]
    
    # Tentar extrair números da string (ex: "251-500" -> 375)
    import re
    numeros = re.findall(r'\d+', str(faixa_str))
    if len(numeros) >= 2:
        inicio = int(numeros[0])
        fim = int(numeros[1])
        media = (inicio + fim) // 2
        print(f"🔄 Extraindo números de '{faixa_str}': {inicio}-{fim} -> média {media}")
        return media
    elif len(numeros) == 1:
        numero = int(numeros[0])
        print(f"🔄 Extraindo número único de '{faixa_str}': {numero}")
        return numero
    
    # Fallback: retornar 50 como padrão
    print(f"⚠️ Não foi possível converter '{faixa_str}', usando 50 como padrão")
    return 50

def salvar_empresa_diagnostico(dados_empresa, respostas, analise):
    """Salva empresa e diagnóstico no Supabase"""
    print("🔍 Iniciando salvamento no Supabase...")
    
    if not supabase:
        print("❌ ERRO: Cliente Supabase não inicializado")
        return None, None
    
    try:
        cnpj = dados_empresa.get('cnpj', '')
        print(f"📋 Verificando empresa existente com CNPJ: {cnpj}")
        
        # Verificar se empresa já existe
        empresa_existente = supabase.table('empresas').select('*').eq('cnpj', cnpj).execute()
        
        if empresa_existente.data:
            # Empresa já existe, usar ID existente
            empresa_id = empresa_existente.data[0]['id']
            print(f"🔄 Empresa existente encontrada. ID: {empresa_id}")
            
            # Atualizar dados da empresa se necessário
            dados_update = {
                'rh_responsavel': dados_empresa.get('rh_responsavel', ''),
                'cargo_rh': dados_empresa.get('cargo', ''),
                'email': dados_empresa.get('email', ''),
                'whatsapp': dados_empresa.get('whatsapp', ''),
                'num_colaboradores': converter_faixa_colaboradores(dados_empresa.get('num_colaboradores', 0)),
                'setor_atividade': dados_empresa.get('setor', dados_empresa.get('atividade_principal', '')),
                'updated_at': 'NOW()'
            }
            
            print(f"📝 Atualizando empresa com dados: {dados_update}")
            update_result = supabase.table('empresas').update(dados_update).eq('id', empresa_id).execute()
            
            if update_result.data:
                print("✅ Empresa atualizada com sucesso")
            else:
                print("⚠️ Empresa não foi atualizada, mas continuando...")
            
        else:
            # Criar nova empresa
            print("🆕 Criando nova empresa...")
            dados_nova_empresa = {
                'razao_social': dados_empresa.get('razao_social', ''),
                'nome_fantasia': dados_empresa.get('nome_fantasia', ''),
                'cnpj': cnpj,
                'email': dados_empresa.get('email', ''),
                'telefone': dados_empresa.get('telefone', ''),
                'whatsapp': dados_empresa.get('whatsapp', ''),
                'endereco': dados_empresa.get('endereco', {}),
                'num_colaboradores': converter_faixa_colaboradores(dados_empresa.get('num_colaboradores', 0)),
                'setor_atividade': dados_empresa.get('setor', dados_empresa.get('atividade_principal', '')),
                'rh_responsavel': dados_empresa.get('rh_responsavel', ''),
                'cargo_rh': dados_empresa.get('cargo', '')
            }
            
            print(f"📝 Inserindo nova empresa: {dados_nova_empresa}")
            nova_empresa = supabase.table('empresas').insert(dados_nova_empresa).execute()
            
            if nova_empresa.data:
                empresa_id = nova_empresa.data[0]['id']
                print(f"✅ Nova empresa criada com ID: {empresa_id}")
            else:
                print(f"❌ ERRO: Falha ao criar nova empresa. Resposta: {nova_empresa}")
                return None, None
        
        # Salvar diagnóstico
        print(f"📊 Salvando diagnóstico para empresa ID: {empresa_id}")
        
        dados_diagnostico = {
            'empresa_id': empresa_id,
            'respostas': respostas,
            'analise': analise,
            'nivel_risco': analise.get('nivel_risco', ''),
            'questoes_criticas': analise.get('questoes_criticas', 0),
            'areas_foco': analise.get('areas_foco', []),
            'acoes_recomendadas': analise.get('acoes_recomendadas', []),
            'status': 'concluido'
        }
        
        print(f"📝 Inserindo diagnóstico: {dados_diagnostico}")
        novo_diagnostico = supabase.table('diagnosticos').insert(dados_diagnostico).execute()
        
        if novo_diagnostico.data:
            diagnostico_id = novo_diagnostico.data[0]['id']
            print(f"✅ Diagnóstico salvo com ID: {diagnostico_id}")
            return empresa_id, diagnostico_id
        else:
            print(f"❌ ERRO: Falha ao salvar diagnóstico. Resposta: {novo_diagnostico}")
            return empresa_id, None
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao salvar no banco: {str(e)}")
        print(f"❌ Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None, None

# Dados das perguntas do questionário
PERGUNTAS = [
    {
        "id": 1,
        "titulo": "🧠 1. Quais são os principais fatores de estresse percebidos entre os colaboradores atualmente?",
        "objetivo": "Identificar fontes de estresse no ambiente de trabalho",
        "opcoes": [
            {"valor": "alta_carga", "texto": "⚡ Alta carga de trabalho"},
            {"valor": "metas_excessivas", "texto": "🎯 Metas excessivas"},
            {"valor": "clima_organizacional", "texto": "🌡️ Clima organizacional"},
            {"valor": "falta_reconhecimento", "texto": "🏆 Falta de reconhecimento"}
        ]
    },
    {
        "id": 2,
        "titulo": "📊 2. A empresa já registrou casos recentes de afastamento por transtornos mentais (ansiedade, depressão, burnout)?",
        "objetivo": "Avaliar a incidência de problemas de saúde mental",
        "opcoes": [
            {"valor": "frequencia_alta", "texto": "🚨 Sim, com frequência alta"},
            {"valor": "frequencia_moderada", "texto": "⚠️ Sim, com frequência moderada"},
            {"valor": "poucos_casos", "texto": "📉 Sim, poucos casos"},
            {"valor": "nao", "texto": "✅ Não"}
        ]
    },
    {
        "id": 3,
        "titulo": "😴 3. O RH identifica sinais de esgotamento ou desmotivação em algum grupo de colaboradores?",
        "objetivo": "Detectar sinais precoces de burnout e desmotivação",
        "opcoes": [
            {"valor": "critico", "texto": "🚨 Sim, em nível crítico"},
            {"valor": "moderado", "texto": "⚠️ Sim, em nível moderado"},
            {"valor": "leve", "texto": "📊 Sim, sinais leves"},
            {"valor": "nao", "texto": "✅ Não"}
        ]
    },
    {
        "id": 4,
        "titulo": "🎭 4. Quais ações de saúde mental já foram realizadas nos últimos 12 meses?",
        "objetivo": "Mapear ações já implementadas",
        "opcoes": [
            {"valor": "nenhuma", "texto": "❌ Nenhuma"},
            {"valor": "palestras", "texto": "🎤 Palestras"},
            {"valor": "atendimento", "texto": "🧠 Atendimento psicológico"},
            {"valor": "multiplas", "texto": "🔄 Múltiplas ações (palestras, dinâmicas, parcerias)"}
        ]
    },
    {
        "id": 5,
        "titulo": "🏢 5. Qual o perfil predominante da atividade dos colaboradores?",
        "objetivo": "Identificar o tipo de ambiente de trabalho",
        "opcoes": [
            {"valor": "administrativo", "texto": "💻 Administrativo (escritório)"},
            {"valor": "producao", "texto": "🏭 Produção (chão de fábrica)"},
            {"valor": "externo", "texto": "🚗 Externo (rua)"},
            {"valor": "misto", "texto": "🔄 Misto"}
        ]
    },
    {
        "id": 6,
        "titulo": "🦴 6. Há registro de queixas frequentes de dores físicas relacionadas ao trabalho?",
        "objetivo": "Identificar problemas ergonômicos existentes",
        "opcoes": [
            {"valor": "frequentes", "texto": "🚨 Sim, queixas frequentes"},
            {"valor": "ocasionais", "texto": "⚠️ Sim, queixas ocasionais"},
            {"valor": "raras", "texto": "📉 Sim, queixas raras"},
            {"valor": "nao", "texto": "✅ Não"}
        ]
    },
    {
        "id": 7,
        "titulo": "🔍 7. A empresa já realizou avaliação ergonômica do ambiente de trabalho nos últimos 12 meses?",
        "objetivo": "Verificar se há diagnóstico ergonômico recente",
        "opcoes": [
            {"valor": "completa", "texto": "✅ Sim, avaliação completa"},
            {"valor": "parcial", "texto": "📊 Sim, avaliação parcial"},
            {"valor": "nao_recente", "texto": "⏰ Não recentemente (mais de 12 meses)"},
            {"valor": "nunca", "texto": "❌ Nunca foi realizada"}
        ]
    },
    {
        "id": 8,
        "titulo": "🏃 8. Quais ações preventivas em ergonomia já foram implementadas?",
        "objetivo": "Mapear ações ergonômicas existentes",
        "opcoes": [
            {"valor": "nenhuma", "texto": "❌ Nenhuma ação"},
            {"valor": "treinamentos", "texto": "📚 Treinamentos pontuais"},
            {"valor": "ajustes", "texto": "🔧 Ajustes de mobiliário"},
            {"valor": "programa", "texto": "📋 Programa estruturado"}
        ]
    },
    {
        "id": 9,
        "titulo": "⏰ 9. Qual a jornada de trabalho predominante na empresa?",
        "objetivo": "Avaliar impacto da jornada no bem-estar",
        "opcoes": [
            {"valor": "padrao", "texto": "⏰ Padrão (8h diárias)"},
            {"valor": "estendida", "texto": "⏳ Estendida (9h+ diárias)"},
            {"valor": "turnos", "texto": "🔄 Turnos/Escala"},
            {"valor": "flexivel", "texto": "🏠 Flexível/Home office"}
        ]
    },
    {
        "id": 10,
        "titulo": "📈 10. Como a empresa avalia a necessidade de investimento em saúde ocupacional?",
        "objetivo": "Medir engajamento e priorização do tema",
        "opcoes": [
            {"valor": "prioritaria", "texto": "🚀 Prioritária e urgente"},
            {"valor": "importante", "texto": "📊 Importante, mas não urgente"},
            {"valor": "secundaria", "texto": "⚖️ Secundária"},
            {"valor": "desnecessaria", "texto": "❓ Não vê necessidade"}
        ]
    }
]

@app.route('/validar_cnpj', methods=['POST'])
def validar_cnpj_route():
    """Endpoint para validar CNPJ e buscar dados da empresa"""
    data = request.get_json()
    cnpj = data.get('cnpj', '').strip()
    
    print(f"\n🔍 [ROUTE] /validar_cnpj chamada")
    print(f"   CNPJ recebido: '{cnpj}'")
    
    if not cnpj:
        print(f"❌ [ROUTE] CNPJ vazio")
        return jsonify({'valid': False, 'message': 'CNPJ é obrigatório'})
    
    # Validar formato do CNPJ
    formato_valido = validar_cnpj(cnpj)
    print(f"📋 [ROUTE] Formato válido: {formato_valido}")
    
    if not formato_valido:
        print(f"❌ [ROUTE] CNPJ com formato inválido")
        return jsonify({'valid': False, 'message': 'CNPJ inválido'})
    
    # Consultar dados usando múltiplas APIs
    print(f"🔍 [ROUTE] Iniciando consulta de dados...")
    dados_empresa = consultar_cnpj_com_fallback(cnpj)
    
    print(f"📊 [ROUTE] Resultado da consulta:")
    print(f"   Dados encontrados: {dados_empresa is not None}")
    
    if dados_empresa:
        print(f"   Razão Social: '{dados_empresa.get('razao_social')}'")
        print(f"   Situação: '{dados_empresa.get('situacao')}'")
        print(f"   CNPJ: '{dados_empresa.get('cnpj')}'")
        print(f"   Município: '{dados_empresa.get('endereco', {}).get('municipio')}'")
        
        # Verificar se empresa está ativa
        situacao = dados_empresa.get('situacao', '').upper()
        print(f"📋 [ROUTE] Verificando situação: '{situacao}'")
        
        if situacao and situacao != 'ATIVA':
            print(f"⚠️ [ROUTE] Empresa não ativa: {situacao}")
            return jsonify({
                'valid': False, 
                'message': f'Empresa com situação: {dados_empresa.get("situacao", "INATIVA")}. Apenas empresas ativas podem realizar o diagnóstico.'
            })
    
    # CNPJ válido no formato - permitir prosseguir mesmo sem dados completos
    resposta = {
        'valid': True,
        'cnpj_validado': True,
        'message': 'CNPJ válido'
    }
    
    # Adicionar dados da empresa se disponível
    if dados_empresa:
        resposta['dados_empresa'] = dados_empresa
        resposta['message'] = 'CNPJ válido e dados da empresa obtidos'
    else:
        print(f"⚠️ [ROUTE] Dados da empresa não encontrados, mas CNPJ é válido")
        resposta['message'] = 'CNPJ válido, mas dados da empresa não puderam ser obtidos'
    
    print(f"✅ [ROUTE] Sucesso! Retornando dados:")
    print(f"   valid: {resposta['valid']}")
    print(f"   cnpj_validado: {resposta['cnpj_validado']}")
    if 'dados_empresa' in resposta:
        print(f"   dados_empresa keys: {list(resposta['dados_empresa'].keys())}")
    else:
        print(f"   dados_empresa: não disponível")
    
    return jsonify(resposta)

@app.route('/')
def index():
    return render_template('index.html', hide_navbar=True)

@app.route('/questionario')
def questionario():
    return render_template('questionario.html', perguntas=PERGUNTAS)

@app.route('/processar_questionario', methods=['POST'])
def processar_questionario():
    try:
        print("=== INICIANDO PROCESSAMENTO ===")
        print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Request method: {request.method}")
        print(f"📍 Request path: {request.path}")
        print(f"🔍 Content-Type: {request.content_type}")
        
        # Log completo dos dados recebidos
        try:
            dados = request.get_json()
            print(f"📦 Dados recebidos (type: {type(dados)}): {dados}")
            
            # Log específico de campos críticos
            if dados and isinstance(dados, dict):
                print("=== ANÁLISE DETALHADA DOS DADOS ===")
                print(f"🔑 Keys principais: {list(dados.keys())}")
                
                if 'dados_empresa' in dados:
                    empresa = dados['dados_empresa']
                    print(f"👔 Empresa keys: {list(empresa.keys()) if isinstance(empresa, dict) else 'NOT DICT'}")
                    print(f"📋 CNPJ: {empresa.get('cnpj') if isinstance(empresa, dict) else 'N/A'}")
                    print(f"📧 Email: {empresa.get('email') if isinstance(empresa, dict) else 'N/A'}")
                    print(f"📱 WhatsApp: {empresa.get('whatsapp') if isinstance(empresa, dict) else 'N/A'}")
                
                if 'respostas' in dados:
                    respostas = dados['respostas']
                    print(f"📝 Respostas type: {type(respostas)}")
                    print(f"📝 Respostas keys: {list(respostas.keys()) if isinstance(respostas, dict) else 'NOT DICT'}")
                    print(f"📝 Total respostas: {len(respostas) if isinstance(respostas, dict) else 'N/A'}")
                
                print("=====================================")
            else:
                print("❌ DADOS NULOS OU INVÁLIDOS")
                
        except Exception as log_error:
            print(f"❌ ERRO ao fazer log dos dados: {str(log_error)}")
            dados = request.get_json()  # Tentar novamente sem log
        
        # Verificar configuração do Supabase
        if not supabase:
            print("❌ ERRO: Supabase não configurado!")
            print(f"SUPABASE_URL: {'✅ OK' if SUPABASE_URL else '❌ MISSING'}")
            print(f"SUPABASE_KEY: {'✅ OK' if SUPABASE_KEY else '❌ MISSING'}")
            return jsonify({
                'status': 'error',
                'message': 'Banco de dados não configurado. Verifique as variáveis de ambiente.'
            }), 500
        
        if not dados:
            print("❌ ERRO: Dados JSON não recebidos")
            return jsonify({
                'status': 'error',
                'message': 'Dados não recebidos'
            }), 400
        
        # Debug: imprimir dados recebidos
        print("=== DEBUG: Dados recebidos ===")
        if 'dados_empresa' in dados:
            empresa = dados['dados_empresa']
            print(f"WhatsApp recebido: {empresa.get('whatsapp', 'NÃO INFORMADO')}")
            print(f"Email recebido: {empresa.get('email', 'NÃO INFORMADO')}")
            print(f"Setor recebido: {empresa.get('setor', 'NÃO INFORMADO')}")
            print(f"CNPJ recebido: {empresa.get('cnpj', 'NÃO INFORMADO')}")
        print("=============================")
        
        # Validar dados obrigatórios
        if 'dados_empresa' not in dados or 'respostas' not in dados:
            print("❌ ERRO: Dados obrigatórios faltando")
            return jsonify({
                'status': 'error',
                'message': 'Dados incompletos'
            }), 400
        
        dados_empresa = dados['dados_empresa']
        respostas = dados['respostas']
        
        # Validar CNPJ novamente
        cnpj = dados_empresa.get('cnpj', '')
        if not cnpj or not validar_cnpj(cnpj):
            print(f"❌ ERRO: CNPJ inválido: {cnpj}")
            return jsonify({
                'status': 'error',
                'message': 'CNPJ inválido'
            }), 400
        
        print("✅ Dados validados com sucesso")
        
        # Gerar análise
        print("🧮 Gerando análise...")
        analise = gerar_analise(respostas)
        print("✅ Análise gerada")
        
        # Salvar no banco de dados (Supabase)
        print("💾 Salvando no banco de dados...")
        empresa_id, diagnostico_id = salvar_empresa_diagnostico(dados_empresa, respostas, analise)
        
        if not empresa_id or not diagnostico_id:
            print("❌ ERRO: Falha ao salvar no banco de dados")
            return jsonify({
                'status': 'error',
                'message': 'Erro ao salvar dados no banco. Tente novamente.'
            }), 500
        
        print(f"✅ Dados salvos - Empresa ID: {empresa_id}, Diagnóstico ID: {diagnostico_id}")
        
        # Salvar dados para a página de resultado
        dados_completos = {
            'dados_empresa': dados_empresa,
            'respostas': respostas,
            'analise': analise,
            'empresa_id': empresa_id,
            'diagnostico_id': diagnostico_id
        }
        
        # Método 1: Salvar na sessão (mais confiável para serverless)
        try:
            session['diagnostico_data'] = dados_completos
            print("✅ Dados salvos na sessão")
        except Exception as session_error:
            print(f"⚠️ Erro ao salvar na sessão: {session_error}")
        
        # Método 2: Arquivo temporário (fallback)
        try:
            with open('temp_diagnostico.json', 'w', encoding='utf-8') as f:
                json.dump(dados_completos, f, ensure_ascii=False, indent=2, default=str)
            print("✅ Arquivo temporário criado")
        except Exception as temp_error:
            print(f"⚠️ Aviso: Erro ao criar arquivo temporário: {temp_error}")
            # Não bloquear o processo por causa do arquivo temporário
        
        print("🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO")
        
        return jsonify({
            'status': 'success',
            'analise': analise,
            'empresa_id': empresa_id,
            'diagnostico_id': diagnostico_id,
            'redirect': f'/resultado?diagnostico_id={diagnostico_id}'
        })
        
    except Exception as e:
        print("=" * 60)
        print("❌ ERRO CRÍTICO no processamento")
        print("=" * 60)
        print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"❌ Erro: {str(e)}")
        print(f"❌ Tipo: {type(e).__name__}")
        print(f"📍 Módulo: {e.__class__.__module__}")
        
        # Stack trace completo
        import traceback
        print("📚 Stack trace completo:")
        traceback.print_exc()
        
        # Tentar capturar dados do request para debug
        try:
            print("🔍 DEBUG - Dados do request:")
            print(f"   Method: {request.method}")
            print(f"   Path: {request.path}")
            print(f"   Content-Type: {request.content_type}")
            print(f"   Content-Length: {request.content_length}")
            
            # Tentar pegar dados do JSON novamente
            try:
                debug_data = request.get_json()
                if debug_data:
                    print(f"   JSON válido: Sim (keys: {list(debug_data.keys()) if isinstance(debug_data, dict) else 'não é dict'})")
                else:
                    print("   JSON válido: Não")
            except Exception as json_error:
                print(f"   JSON Error: {json_error}")
                
        except Exception as debug_error:
            print(f"⚠️ Erro no debug: {debug_error}")
        
        print("=" * 60)
        
        return jsonify({
            'status': 'error',
            'message': f'Erro interno do servidor: {type(e).__name__}',
            'details': str(e)
        }), 500

@app.route('/resultado')
def resultado():
    """Página de resultados do diagnóstico"""
    try:
        # Tentar diferentes formas de obter os dados
        dados = None
        
        # Método 1: Verificar se há dados na sessão
        if 'diagnostico_data' in session:
            print("📊 Dados encontrados na sessão")
            dados = session['diagnostico_data']
            # Limpar da sessão após usar
            session.pop('diagnostico_data', None)
        
        # Método 2: Tentar ler arquivo temporário (fallback)
        elif os.path.exists('temp_diagnostico.json'):
            print("📄 Lendo dados do arquivo temporário")
            with open('temp_diagnostico.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Remover arquivo após usar
            try:
                os.remove('temp_diagnostico.json')
                print("🗑️ Arquivo temporário removido")
            except:
                pass
        
        # Método 3: Tentar buscar no banco pelo ID (se disponível)
        elif request.args.get('diagnostico_id') and supabase:
            diagnostico_id = request.args.get('diagnostico_id')
            print(f"🔍 Buscando diagnóstico no banco: {diagnostico_id}")
            
            try:
                # Buscar diagnóstico no Supabase
                resultado_query = supabase.table('diagnosticos').select('*, empresas(*)').eq('id', diagnostico_id).execute()
                
                if resultado_query.data:
                    diagnostico = resultado_query.data[0]
                    dados = {
                        'dados_empresa': diagnostico['empresas'],
                        'respostas': diagnostico['respostas'],
                        'analise': diagnostico['analise'],
                        'empresa_id': diagnostico['empresa_id'],
                        'diagnostico_id': diagnostico['id']
                    }
                    print("✅ Dados recuperados do banco de dados")
            except Exception as db_error:
                print(f"❌ Erro ao buscar no banco: {db_error}")
        
        if dados:
            print("✅ Renderizando página de resultado com dados")
            return render_template('resultado.html', dados=dados)
        else:
            print("❌ Nenhum dado encontrado para resultado")
            flash('Dados do diagnóstico não encontrados. Por favor, refaça o questionário.', 'error')
            return redirect('/')
            
    except Exception as e:
        print(f"❌ Erro na página de resultado: {e}")
        flash('Erro ao carregar resultado. Por favor, refaça o questionário.', 'error')
        return redirect('/')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        print(f"🔍 [ADMIN] Tentativa de login - usuário: '{username}', senha: {'*' * len(password)}")
        print(f"🔍 [ADMIN] Supabase disponível: {supabase is not None}")
        
        # Sistema de fallback para quando Supabase não está disponível
        if not supabase:
            print("⚠️ [ADMIN] Supabase indisponível - usando autenticação local")
            
            # Verificar credenciais padrão (fallback)
            if ((username == 'admin' and password == 'admin123') or 
                (username == ADMIN_EMAIL and password == ADMIN_PASSWORD)):
                
                print(f"✅ [ADMIN] Login bem-sucedido (fallback) - usuário: {username}")
                
                session['admin_user'] = {
                    'id': 'admin-local',
                    'username': username,
                    'email': username if '@' in username else ADMIN_EMAIL,
                    'role': 'super_admin',
                    'auth_method': 'fallback'
                }
                
                print(f"💾 [ADMIN] Sessão criada: {session.get('admin_user')}")
                flash('Login realizado com sucesso! (Modo local)', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                print(f"❌ [ADMIN] Credenciais inválidas (fallback) - usuário: {username}")
                flash('Credenciais inválidas. Use: admin/admin123 ou as configuradas nas variáveis de ambiente.', 'error')
                return render_template('admin/login.html')
        
        # Lógica original com Supabase
        try:
            print(f"🔍 [ADMIN] Tentando login com Supabase - usuário: {username}")
            
            # Buscar usuário no banco
            user_result = supabase.table('admin_users').select('*').eq('username', username).eq('is_active', True).execute()
            
            if user_result.data:
                user = user_result.data[0]
                print(f"👤 [ADMIN] Usuário encontrado no banco: {user['username']}")
                
                # Verificar senha (em produção, use hash seguro)
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                # Para simplificar, vamos aceitar a senha 'admin123' para o usuário admin
                if username == 'admin' and password == 'admin123':
                    session['admin_user'] = {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'role': user['role'],
                        'auth_method': 'supabase'
                    }
                    
                    # Atualizar último login
                    supabase.table('admin_users').update({
                        'last_login': datetime.now().isoformat()
                    }).eq('id', user['id']).execute()
                    
                    print(f"✅ [ADMIN] Login bem-sucedido (Supabase) - usuário: {username}")
                    print(f"💾 [ADMIN] Sessão criada: {session.get('admin_user')}")
                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    print(f"❌ [ADMIN] Senha incorreta para usuário: {username}")
                    flash('Credenciais inválidas', 'error')
            else:
                print(f"❌ [ADMIN] Usuário não encontrado no banco: {username}")
                flash('Usuário não encontrado', 'error')
                
        except Exception as e:
            print(f"❌ [ADMIN] Erro no sistema de autenticação: {e}")
            flash('Erro no sistema de autenticação', 'error')
    else:
        print("📄 [ADMIN] Exibindo página de login")
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    print(f"🚪 [ADMIN] Logout - usuário: {session.get('admin_user', {}).get('username', 'N/A')}")
    session.pop('admin_user', None)
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('admin_login'))

# Rota de debug temporária para verificar sessão
@app.route('/admin/debug')
def admin_debug():
    debug_info = {
        'session_data': dict(session),
        'has_admin_user': 'admin_user' in session,
        'session_cookie_secure': app.config.get('SESSION_COOKIE_SECURE'),
        'session_cookie_httponly': app.config.get('SESSION_COOKIE_HTTPONLY'),
        'session_cookie_samesite': app.config.get('SESSION_COOKIE_SAMESITE'),
        'is_production': os.environ.get('VERCEL') or os.environ.get('FLASK_ENV') == 'production',
        'flask_secret_key_set': bool(app.secret_key),
    }
    return jsonify(debug_info)

# Rota de debug para testar estatísticas
@app.route('/debug/stats')
def debug_stats():
    """Debug route para verificar estatísticas do dashboard"""
    try:
        if not supabase:
            return jsonify({'error': 'Supabase não configurado'})
        
        # Testar conexão básica
        empresas = supabase.table('empresas').select('id').limit(1).execute()
        diagnosticos = supabase.table('diagnosticos').select('id').limit(1).execute()
        
        # Testar view
        stats_result = supabase.table('vw_estatisticas_admin').select('*').execute()
        
        return jsonify({
            'supabase_ok': bool(supabase),
            'empresas_count': len(empresas.data) if empresas.data else 0,
            'diagnosticos_count': len(diagnosticos.data) if diagnosticos.data else 0,
            'view_result_count': len(stats_result.data) if stats_result.data else 0,
            'view_data': stats_result.data[:2] if stats_result.data else [],
            'env_vars': {
                'SUPABASE_URL': bool(os.environ.get('SUPABASE_URL')),
                'SUPABASE_ANON_KEY': bool(os.environ.get('SUPABASE_ANON_KEY')),
                'VERCEL': bool(os.environ.get('VERCEL')),
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# Rota de debug para verificar arquivos estáticos
@app.route('/debug/static')
def debug_static():
    """Debug route para verificar configuração de arquivos estáticos"""
    import glob
    
    debug_info = {
        'static_folder': app.static_folder,
        'static_url_path': app.static_url_path,
        'template_folder': app.template_folder,
        'is_production': os.environ.get('VERCEL') or os.environ.get('FLASK_ENV') == 'production',
        'static_folder_exists': os.path.exists(app.static_folder) if app.static_folder else False,
        'template_folder_exists': os.path.exists(app.template_folder) if app.template_folder else False,
        'current_dir': os.getcwd(),
        'file_structure': {}
    }
    
    # Listar arquivos estáticos se a pasta existir
    if debug_info['static_folder_exists']:
        try:
            static_files = []
            for root, dirs, files in os.walk(app.static_folder):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), app.static_folder)
                    static_files.append(rel_path)
            debug_info['static_files'] = static_files[:20]  # Limitar para não sobrecarregar
        except Exception as e:
            debug_info['static_files_error'] = str(e)
    
    return jsonify(debug_info)

@app.route('/test/urls')
def test_urls():
    """Testa geração de URLs para arquivos estáticos"""
    from flask import url_for
    
    test_urls = {
        'css_url': url_for('static', filename='css/style.css'),
        'js_url': url_for('static', filename='js/main.js'),
        'logo_url': url_for('static', filename='images/logo-conecta.png'),
        'base_static_url': url_for('static', filename=''),
        'full_css_url': request.url_root.rstrip('/') + url_for('static', filename='css/style.css'),
        'request_url_root': request.url_root,
        'static_folder': app.static_folder,
        'static_url_path': app.static_url_path
    }
    
    return jsonify(test_urls)

@app.route('/test/fix')
def test_fix():
    """Teste se o fix foi aplicado"""
    return jsonify({
        'status': 'fixed',
        'timestamp': datetime.now().isoformat(),
        'version': 'v2.0',
        'fix_applied': True
    })

@app.route('/admin')
@app.route('/admin/dashboard')
@requires_admin
def admin_dashboard():
    if not supabase:
        flash('Sistema de administração indisponível', 'error')
        return redirect('/')
    
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
        
        # Buscar diagnósticos recentes
        recent_result = supabase.table('vw_diagnosticos_completos').select('*').limit(10).execute()
        recent_diagnosticos = recent_result.data
        
        # Buscar dados mensais para gráfico (últimos 6 meses)
        monthly_data = []
        try:
            monthly_query = """
                SELECT 
                    DATE_TRUNC('month', created_at) as mes,
                    COUNT(*) as total
                FROM diagnosticos 
                WHERE created_at >= NOW() - INTERVAL '6 months'
                GROUP BY DATE_TRUNC('month', created_at)
                ORDER BY mes
            """
            monthly_result = supabase.rpc('execute_sql', {'query': monthly_query}).execute()
            
            if monthly_result.data:
                monthly_data = monthly_result.data
            else:
                # Fallback: buscar de forma mais simples
                all_diagnosticos = supabase.table('diagnosticos').select('created_at').execute()
                
                # Processar dados no Python
                from collections import defaultdict
                from datetime import datetime, timedelta
                import calendar
                
                # Contar diagnósticos por mês
                monthly_counts = defaultdict(int)
                
                for diag in all_diagnosticos.data:
                    try:
                        created_date = datetime.fromisoformat(diag['created_at'].replace('Z', '+00:00'))
                        month_key = created_date.strftime('%Y-%m')
                        monthly_counts[month_key] += 1
                    except:
                        continue
                
                # Gerar últimos 6 meses
                monthly_data = []
                today = datetime.now()
                for i in range(5, -1, -1):  # Últimos 6 meses
                    month_date = today.replace(day=1) - timedelta(days=30*i)
                    month_key = month_date.strftime('%Y-%m')
                    month_name = calendar.month_name[month_date.month][:3]  # Jan, Feb, etc
                    
                    monthly_data.append({
                        'mes': month_key,
                        'mes_nome': month_name,
                        'total': monthly_counts.get(month_key, 0)
                    })
                    
        except Exception as monthly_error:
            print(f"Erro ao buscar dados mensais: {monthly_error}")
            # Dados de fallback
            monthly_data = [
                {'mes': '2025-02', 'mes_nome': 'Fev', 'total': 0},
                {'mes': '2025-03', 'mes_nome': 'Mar', 'total': 0},
                {'mes': '2025-04', 'mes_nome': 'Abr', 'total': 0},
                {'mes': '2025-05', 'mes_nome': 'Mai', 'total': 0},
                {'mes': '2025-06', 'mes_nome': 'Jun', 'total': 0},
                {'mes': '2025-08', 'mes_nome': 'Ago', 'total': len(recent_diagnosticos)}
            ]
        
        return render_template('admin/dashboard.html', 
                               stats=stats, 
                               recent_diagnosticos=recent_diagnosticos,
                               monthly_data=monthly_data)
    except Exception as e:
        flash('Erro ao carregar dados do dashboard', 'error')
        print(f"Erro no dashboard: {e}")
        return render_template('admin/dashboard.html', 
                               stats={}, 
                               recent_diagnosticos=[], 
                               monthly_data=[])

@app.route('/admin/empresas')
@requires_admin
def admin_empresas():
    if not supabase:
        flash('Sistema de administração indisponível', 'error')
        return redirect('/')
    
    try:
        # Parâmetros de filtro
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        per_page = 20
        
        # Query base
        query = supabase.table('vw_diagnosticos_completos').select('*')
        
        # Aplicar filtro de busca
        if search:
            query = query.or_(f'razao_social.ilike.%{search}%,cnpj.ilike.%{search}%,rh_responsavel.ilike.%{search}%')
        
        # Aplicar paginação
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        result = query.range(start, end).order('data_diagnostico', desc=True).execute()
        empresas = result.data
        
        return render_template('admin/empresas.html', 
                               empresas=empresas, 
                               search=search,
                               page=page)
    except Exception as e:
        flash('Erro ao carregar lista de empresas', 'error')
        print(f"Erro ao buscar empresas: {e}")
        return render_template('admin/empresas.html', empresas=[], search='', page=1)

@app.route('/admin/empresa/<empresa_id>')
@requires_admin
def admin_empresa_detalhes(empresa_id):
    if not supabase:
        flash('Sistema de administração indisponível', 'error')
        return redirect('/')
    
    try:
        # Buscar dados da empresa
        empresa_result = supabase.table('empresas').select('*').eq('id', empresa_id).execute()
        if not empresa_result.data:
            flash('Empresa não encontrada', 'error')
            return redirect(url_for('admin_empresas'))
        
        empresa = empresa_result.data[0]
        
        # Buscar todos os diagnósticos da empresa
        diagnosticos_result = supabase.table('diagnosticos').select('*').eq('empresa_id', empresa_id).order('created_at', desc=True).execute()
        diagnosticos = diagnosticos_result.data
        
        return render_template('admin/empresa_detalhes.html', 
                               empresa=empresa, 
                               diagnosticos=diagnosticos)
    except Exception as e:
        flash('Erro ao carregar detalhes da empresa', 'error')
        print(f"Erro ao buscar empresa: {e}")
        return redirect(url_for('admin_empresas'))

@app.route('/gerar_pdf')
def gerar_pdf():
    try:
        # Verificar se o arquivo existe
        if not os.path.exists('temp_diagnostico.json'):
            return jsonify({'error': 'Dados do diagnóstico não encontrados. Refaça o questionário.'}), 404
        
        with open('temp_diagnostico.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print(f"Dados carregados: {dados}")  # Debug
        
        pdf_buffer = criar_pdf_relatorio(dados)
        print("PDF criado com sucesso")  # Debug
        
        return send_file(
            io.BytesIO(pdf_buffer),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'diagnostico_programa_equilibrio_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        print(f"Erro na geração de PDF: {str(e)}")  # Debug
        return jsonify({'error': f'Erro ao gerar PDF: {str(e)}'}), 500

def gerar_analise(respostas):
    """Gera análise baseada nas respostas do questionário"""
    
    # Análise de saúde mental
    questoes_criticas = 0
    acoes_recomendadas = []
    areas_foco = []
    
    # Análise questão por questão
    if respostas.get('1') == 'alta_carga':
        questoes_criticas += 1
        acoes_recomendadas.append("Programa: Comunicação Não Violenta e Segurança Psicológica")
        areas_foco.append("Saúde Mental")
    
    if respostas.get('2') in ['frequencia_alta', 'frequencia_moderada']:
        questoes_criticas += 2
        acoes_recomendadas.append("Programa: Prevenção e Manejo do Estresse Ocupacional")
        areas_foco.append("Saúde Mental")
    
    if respostas.get('3') in ['critico', 'moderado']:
        questoes_criticas += 1
        areas_foco.append("Saúde Mental")
    
    if respostas.get('6') in ['frequentes', 'ocasionais']:
        questoes_criticas += 1
        acoes_recomendadas.append("Programa: Avaliação Ergonômica Completa")
        areas_foco.append("Ergonomia")
    
    if respostas.get('7') in ['nunca', 'nao_recente']:
        questoes_criticas += 1
        acoes_recomendadas.append("Programa: Implementação de Ergonomia no Trabalho")
        areas_foco.append("Ergonomia")
    
    # Se não há ações específicas, adicionar ações preventivas
    if not acoes_recomendadas:
        acoes_recomendadas.append("Programa: Promoção de Bem-estar no Trabalho")
    
    # Determinar nível de risco
    if questoes_criticas >= 4:
        nivel_risco = "Alto"
    elif questoes_criticas >= 2:
        nivel_risco = "Moderado" 
    else:
        nivel_risco = "Baixo"
    
    return {
        'questoes_criticas': questoes_criticas,
        'nivel_risco': nivel_risco,
        'areas_foco': list(set(areas_foco)),
        'acoes_recomendadas': list(set(acoes_recomendadas)),
        'data_diagnostico': datetime.now().strftime("%d/%m/%Y")
    }

def criar_pdf_relatorio(dados):
    """Cria um relatório PDF profissional com a logo da Belz Conecta Saúde"""
    buffer = io.BytesIO()
    
    # Extrair dados
    dados_empresa = dados.get('dados_empresa', {})
    analise = dados.get('analise', {})
    
    # Configuração da página
    width, height = A4
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Função helper para centralizar texto
    def draw_centered_text(canvas, x, y, text, font_size=12):
        canvas.setFont("Helvetica", font_size)
        text_width = canvas.stringWidth(str(text))
        canvas.drawString(x - text_width/2, y, str(text))
    
    def draw_header_with_logo(canvas, y_start):
        """Desenha cabeçalho profissional com logo"""
        # Background do header com bordas arredondadas superiores usando roundRect
        canvas.setFillColor(HexColor("#130E54"))
        canvas.roundRect(0, y_start, width, 100, radius=15, fill=True, stroke=False)
        
        # Tentar carregar logo
        logo_path = os.path.join('static', 'images', 'logo-conecta.png')
        print(f"Tentando carregar logo do caminho: {logo_path}")
        print(f"Logo existe? {os.path.exists(logo_path)}")
        
        if os.path.exists(logo_path):
            try:
                # Tentativa 1: Usar diretamente o PNG com mask='auto' para transparência
                print("Tentando carregar logo diretamente com transparência...")
                canvas.drawImage(logo_path, 20, y_start + 25, width=120, height=45, mask='auto', preserveAspectRatio=True)
                print("Logo carregada diretamente com transparência!")
                
            except Exception as e1:
                print(f"Erro ao carregar com transparência: {e1}")
                try:
                    # Tentativa 2: Usar PIL mas manter transparência
                    from PIL import Image
                    print("PIL importado, tentando manter transparência...")
                    
                    img = Image.open(logo_path)
                    print(f"Logo aberta. Modo: {img.mode}, Tamanho: {img.size}")
                    
                    # Para PNG com transparência, salvar como PNG temporário ao invés de JPEG
                    if img.mode == 'RGBA':
                        # Manter como RGBA para preservar transparência
                        temp_path = 'temp_logo.png'
                        img.save(temp_path, 'PNG')
                        print("Logo salva como PNG temporário (mantendo transparência)")
                    else:
                        # Se não tem transparência, converter para RGB
                        img = img.convert('RGB')
                        temp_path = 'temp_logo.jpg'
                        img.save(temp_path, 'JPEG', quality=95)
                        print("Logo salva como JPEG temporário")
                    
                    # Calcular dimensões mantendo aspect ratio
                    logo_width = 75
                    logo_height = int(100 * img.size[1] / img.size[0])
                    
                    if logo_height > 50:
                        logo_height = 50
                        logo_width = int(50 * img.size[0] / img.size[1])
                    
                    print(f"Dimensões da logo: {logo_width}x{logo_height}")
                    
                    # Desenhar com mask='auto' se for PNG, sem mask se for JPEG
                    if temp_path.endswith('.png'):
                        canvas.drawImage(temp_path, 20, y_start + 25, width=logo_width, height=logo_height, mask='auto')
                    else:
                        canvas.drawImage(temp_path, 20, y_start + 25, width=logo_width, height=logo_height)
                    
                    print("Logo desenhada com PIL")
                    os.remove(temp_path)
                    
                except Exception as e2:
                    print(f"Erro com PIL: {e2}")
                    # Placeholder sem fundo preto
                    canvas.setFillColor(HexColor("#FFFFFF"))
                    canvas.circle(50, y_start + 50, 20, fill=True)
                    canvas.setFillColor(HexColor("#130E54"))
                    canvas.setFont("Helvetica-Bold", 10)
                    canvas.drawString(42, y_start + 46, "BELZ")
        else:
            # Logo não existe, desenhar placeholder
            print("Logo não encontrada, usando placeholder")
            canvas.setFillColor(HexColor("#FFFFFF"))
            canvas.circle(50, y_start + 50, 20, fill=True)
            canvas.setFillColor(HexColor("#130E54"))
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(42, y_start + 46, "BELZ")
        
        # Título principal - ajustado para dar mais espaço à logo
        canvas.setFillColor(HexColor("#FFFFFF"))
        canvas.setFont("Helvetica-Bold", 24)
        canvas.drawString(150, y_start + 55, "BELZ CONECTA SAÚDE")
        
        # Subtítulo - alinhado com o título
        canvas.setFont("Helvetica", 14)
        canvas.drawString(150, y_start + 35, "Programa Equilíbrio - Diagnóstico Corporativo")
        
        # Data do relatório
        canvas.setFont("Helvetica", 10)
        canvas.drawRightString(width - 30, y_start + 15, f"Relatório gerado em: {analise.get('data_diagnostico', datetime.now().strftime('%d/%m/%Y'))}")
        
        return y_start - 20
    
    def draw_section_header(canvas, x, y, title, color="#130E54"):
        """Desenha cabeçalho de seção estilizado com bordas arredondadas"""
        canvas.setFillColor(HexColor(color))
        
        # Usar roundRect para bordas arredondadas
        rect_x = x - 10
        rect_y = y - 5
        rect_width = width - 80
        rect_height = 30
        radius = 10  # raio das bordas arredondadas
        
        canvas.roundRect(rect_x, rect_y, rect_width, rect_height, radius=radius, fill=True, stroke=False)
        
        canvas.setFillColor(HexColor("#FFFFFF"))
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(x, y+10, title)
        
        return y - 40
    
    def draw_info_box(canvas, x, y, title, content, box_color="#f6f6f6", text_color="#000000"):
        """Desenha caixa de informação estilizada com bordas arredondadas"""
        box_height = len(content) * 15 + 40
        radius = 8  # raio das bordas arredondadas
        
        # Fundo com bordas arredondadas
        canvas.setFillColor(HexColor(box_color))
        canvas.roundRect(x, y - box_height, 500, box_height, radius=radius, fill=True, stroke=False)
        
        # Borda com bordas arredondadas
        canvas.setStrokeColor(HexColor("#130E54"))
        canvas.setLineWidth(1)
        canvas.roundRect(x, y - box_height, 500, box_height, radius=radius, fill=False, stroke=True)
        
        # Title
        canvas.setFillColor(HexColor("#130E54"))
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(x + 15, y - 20, title)
        
        # Content
        canvas.setFillColor(HexColor(text_color))
        canvas.setFont("Helvetica", 10)
        y_content = y - 40
        for line in content:
            canvas.drawString(x + 15, y_content, line)
            y_content -= 15
        
        return y - box_height - 20
    
    def draw_action_card(canvas, x, y, acao, categoria, cor):
        """Desenha card de ação profissional"""
        card_height = 80
        
        # Card background with shadow effect
        canvas.setFillColor(HexColor("#e0e0e0"))
        canvas.roundRect(x+3, y - card_height-3, 500, card_height, 10, fill=True)
        canvas.setFillColor(HexColor(cor))
        canvas.roundRect(x, y - card_height, 500, card_height, 10, fill=True)
        
        # Content
        canvas.setFillColor(HexColor("#FFFFFF"))
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(x + 20, y - 25, acao)
        
        canvas.setFont("Helvetica", 10)
        canvas.drawString(x + 20, y - 45, f"Categoria: {categoria}")
        
        # Detalhes baseados na categoria
        if "Mental" in categoria:
            duracao = "Duração: 5 horas | Público: Todos os colaboradores + Lideranças"
        else:
            duracao = "Duração: 16 horas | Público: RH + Lideranças + SESMT"
        
        canvas.drawString(x + 20, y - 60, duracao)
        
        return y - card_height - 15
    
    # Começar o documento
    current_y = height - 20
    
    # Header com logo
    current_y = draw_header_with_logo(p, current_y - 80)
    current_y -= 40
    
    # Dados da Empresa
    current_y = draw_section_header(p, 50, current_y, "📋 INFORMAÇÕES DA EMPRESA")
    
    empresa_info = [
        f"Empresa: {dados_empresa.get('razao_social', 'N/A')}",
        f"Nome Fantasia: {dados_empresa.get('nome_fantasia', 'N/A')}",
        f"CNPJ: {dados_empresa.get('cnpj', 'N/A')}",
        f"RH Responsável: {dados_empresa.get('rh_responsavel', 'N/A')}",
        f"Cargo: {dados_empresa.get('cargo', 'N/A')}",
        f"E-mail: {dados_empresa.get('email', 'N/A')}",
        f"WhatsApp: {dados_empresa.get('whatsapp', 'N/A')}",
        f"Número de Colaboradores: {dados_empresa.get('num_colaboradores', 'N/A')}"
    ]
    
    current_y = draw_info_box(p, 50, current_y, "Dados Cadastrais", empresa_info)
    current_y -= 20
    
    # Resumo do Diagnóstico
    current_y = draw_section_header(p, 50, current_y, "🎯 RESUMO DO DIAGNÓSTICO")
    
    resumo_info = [
        f"Nível de Risco: {analise.get('nivel_risco', 'N/A')}",
        f"Questões Críticas Identificadas: {analise.get('questoes_criticas', 0)}",
        f"Áreas de Foco: {', '.join(analise.get('areas_foco', [])) if analise.get('areas_foco') else 'Prevenção Geral'}",
        f"Total de Ações Recomendadas: {len(analise.get('acoes_recomendadas', []))}"
    ]
    
    # Cor baseada no nível de risco
    nivel_risco = analise.get('nivel_risco', 'Baixo')
    if "Alto" in nivel_risco:
        cor_resumo = "#dc3545"
    elif "Moderado" in nivel_risco:
        cor_resumo = "#fd7e14"
    else:
        cor_resumo = "#28a745"
    
    current_y = draw_info_box(p, 50, current_y, "Status Atual", resumo_info, cor_resumo, "#FFFFFF")
    
    # Nova página para ações
    p.showPage()
    current_y = height - 50
    
    # Ações Recomendadas
    current_y = draw_section_header(p, 50, current_y, "🚀 AÇÕES RECOMENDADAS")
    current_y -= 20
    
    for i, acao in enumerate(analise.get('acoes_recomendadas', [])):
        if "Comunicação" in acao or "Mental" in acao:
            categoria = "🧠 Saúde Mental"
            cor = "#dc3545"
        else:
            categoria = "🔧 Ergonomia"
            cor = "#fd7e14"
        
        current_y = draw_action_card(p, 50, current_y, acao, categoria, cor)
        
        # Nova página se necessário
        if current_y < 150:
            p.showPage()
            current_y = height - 50
    
    # Plano de Ação Timeline
    if current_y < 300:
        p.showPage()
        current_y = height - 50
    
    current_y = draw_section_header(p, 50, current_y, "📅 CRONOGRAMA DE IMPLEMENTAÇÃO")
    current_y -= 20
    
    # Timeline visual
    acoes_recomendadas = analise.get('acoes_recomendadas', [])
    timeline_items = [
        ("🚨 IMEDIATO (0-30 dias)", [acao for acao in acoes_recomendadas if "Comunicação" in acao or "Mental" in acao], "#dc3545"),
        ("⚠️ MÉDIO PRAZO (30-60 dias)", [acao for acao in acoes_recomendadas if "Ergonômica" in acao or "Ergonomia" in acao], "#fd7e14"),
        ("📊 LONGO PRAZO (60+ dias)", ["Implementar pesquisas de clima trimestrais", "Criar programa de saúde ocupacional permanente"], "#28a745")
    ]
    
    for fase, acoes, cor in timeline_items:
        if acoes:  # Só mostrar se houver ações
            current_y = draw_info_box(p, 50, current_y, fase, [f"• {acao}" for acao in acoes], cor, "#FFFFFF")
            current_y -= 10
    
    # Footer profissional
    p.setFillColor(HexColor("#f6f6f6"))
    p.rect(0, 0, width, 50, fill=True)
    
    p.setFillColor(HexColor("#130E54"))
    p.setFont("Helvetica", 10)
    draw_centered_text(p, width/2, 25, "Belz Conecta Saúde - Programa Equilíbrio | www.belzconectasaude.com.br")
    draw_centered_text(p, width/2, 10, "Este relatório é confidencial e destinado exclusivamente à empresa solicitante")
    
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

if __name__ == '__main__':
    # Criar diretórios necessários
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    # Para desenvolvimento local
    app.run(debug=True, host='0.0.0.0', port=5000)
