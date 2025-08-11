from flask import Flask, render_template, request, jsonify, send_file, url_for, redirect, session, flash
import json
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import io
import base64
import requests
from supabase import create_client, Client
from decouple import config
from validate_docbr import CNPJ
import hashlib
import secrets
from functools import wraps

app = Flask(__name__)

# Configurações
app.secret_key = config('FLASK_SECRET_KEY', default='dev-key-change-in-production')
app.static_folder = 'static'
app.template_folder = 'templates'

# Configuração do Supabase
SUPABASE_URL = config('SUPABASE_URL', default='')
SUPABASE_KEY = config('SUPABASE_KEY', default='')

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
    print("⚠️  Configurações do Supabase não encontradas. Funcionalidades de banco de dados estarão limitadas.")

# Validador de CNPJ
cnpj_validator = CNPJ()

# API ReceitaWS
RECEITAWS_API_URL = config('RECEITAWS_API_URL', default='https://www.receitaws.com.br/v1/cnpj/')

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
        
        # Faz a requisição para a API
        response = requests.get(f"{RECEITAWS_API_URL}{cnpj_limpo}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verifica se houve erro na consulta
            if data.get('status') == 'ERROR':
                return None
            
            return {
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
        else:
            return None
            
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None

def salvar_empresa_diagnostico(dados_empresa, respostas, analise):
    """Salva empresa e diagnóstico no Supabase"""
    if not supabase:
        return None, None
    
    try:
        # Verificar se empresa já existe
        empresa_existente = supabase.table('empresas').select('*').eq('cnpj', dados_empresa['cnpj']).execute()
        
        if empresa_existente.data:
            # Empresa já existe, usar ID existente
            empresa_id = empresa_existente.data[0]['id']
            
            # Atualizar dados da empresa se necessário
            supabase.table('empresas').update({
                'rh_responsavel': dados_empresa['rh_responsavel'],
                'cargo_rh': dados_empresa['cargo'],
                'email': dados_empresa['email'],
                'whatsapp': dados_empresa.get('whatsapp', ''),
                'num_colaboradores': dados_empresa['num_colaboradores']
            }).eq('id', empresa_id).execute()
            
        else:
            # Criar nova empresa
            nova_empresa = supabase.table('empresas').insert({
                'razao_social': dados_empresa['razao_social'],
                'nome_fantasia': dados_empresa.get('nome_fantasia', ''),
                'cnpj': dados_empresa['cnpj'],
                'email': dados_empresa['email'],
                'telefone': dados_empresa.get('telefone', ''),
                'whatsapp': dados_empresa.get('whatsapp', ''),
                'endereco': dados_empresa.get('endereco', {}),
                'num_colaboradores': dados_empresa['num_colaboradores'],
                'setor_atividade': dados_empresa.get('atividade_principal', ''),
                'rh_responsavel': dados_empresa['rh_responsavel'],
                'cargo_rh': dados_empresa['cargo']
            }).execute()
            
            empresa_id = nova_empresa.data[0]['id']
        
        # Salvar diagnóstico
        novo_diagnostico = supabase.table('diagnosticos').insert({
            'empresa_id': empresa_id,
            'respostas': respostas,
            'analise': analise,
            'nivel_risco': analise['nivel_risco'],
            'questoes_criticas': analise['questoes_criticas'],
            'areas_foco': analise['areas_foco'],
            'acoes_recomendadas': analise['acoes_recomendadas'],
            'status': 'concluido'
        }).execute()
        
        return empresa_id, novo_diagnostico.data[0]['id']
        
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
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
    
    if not cnpj:
        return jsonify({'valid': False, 'message': 'CNPJ é obrigatório'})
    
    # Validar formato do CNPJ
    if not validar_cnpj(cnpj):
        return jsonify({'valid': False, 'message': 'CNPJ inválido'})
    
    # Consultar dados na ReceitaWS
    dados_empresa = consultar_cnpj_receita_ws(cnpj)
    
    if not dados_empresa:
        return jsonify({'valid': False, 'message': 'CNPJ não encontrado ou erro na consulta'})
    
    if dados_empresa.get('situacao') != 'ATIVA':
        return jsonify({
            'valid': False, 
            'message': f'Empresa com situação: {dados_empresa.get("situacao", "INATIVA")}. Apenas empresas ativas podem realizar o diagnóstico.'
        })
    
    return jsonify({
        'valid': True,
        'dados_empresa': dados_empresa,
        'message': 'CNPJ válido e empresa ativa'
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionario')
def questionario():
    return render_template('questionario.html', perguntas=PERGUNTAS)

@app.route('/processar_questionario', methods=['POST'])
def processar_questionario():
    try:
        dados = request.get_json()
        
        # Validar dados obrigatórios
        if 'dados_empresa' not in dados or 'respostas' not in dados:
            return jsonify({
                'status': 'error',
                'message': 'Dados incompletos'
            }), 400
        
        dados_empresa = dados['dados_empresa']
        respostas = dados['respostas']
        
        # Validar CNPJ novamente
        if not validar_cnpj(dados_empresa.get('cnpj', '')):
            return jsonify({
                'status': 'error',
                'message': 'CNPJ inválido'
            }), 400
        
        # Gerar análise
        analise = gerar_analise(respostas)
        
        # Salvar no banco de dados (Supabase)
        empresa_id, diagnostico_id = salvar_empresa_diagnostico(dados_empresa, respostas, analise)
        
        # Salvar dados temporariamente para geração do PDF
        dados_completos = {
            'dados_empresa': dados_empresa,
            'respostas': respostas,
            'analise': analise,
            'empresa_id': empresa_id,
            'diagnostico_id': diagnostico_id
        }
        
        with open('temp_diagnostico.json', 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, ensure_ascii=False, indent=2, default=str)
        
        return jsonify({
            'status': 'success',
            'analise': analise,
            'empresa_id': empresa_id,
            'diagnostico_id': diagnostico_id,
            'redirect': '/resultado'
        })
    except Exception as e:
        print(f"Erro no processamento: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.route('/resultado')
def resultado():
    try:
        with open('temp_diagnostico.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        return render_template('resultado.html', dados=dados)
    except FileNotFoundError:
        flash('Dados do diagnóstico não encontrados. Por favor, refaça o questionário.', 'error')
        return redirect('/')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not supabase:
            flash('Sistema de administração indisponível', 'error')
            return render_template('admin/login.html')
        
        try:
            # Buscar usuário no banco
            user_result = supabase.table('admin_users').select('*').eq('username', username).eq('is_active', True).execute()
            
            if user_result.data:
                user = user_result.data[0]
                
                # Verificar senha (em produção, use hash seguro)
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                # Para simplificar, vamos aceitar a senha 'admin123' para o usuário admin
                if username == 'admin' and password == 'admin123':
                    session['admin_user'] = {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'role': user['role']
                    }
                    
                    # Atualizar último login
                    supabase.table('admin_users').update({
                        'last_login': datetime.now().isoformat()
                    }).eq('id', user['id']).execute()
                    
                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Credenciais inválidas', 'error')
            else:
                flash('Usuário não encontrado', 'error')
                
        except Exception as e:
            flash('Erro no sistema de autenticação', 'error')
            print(f"Erro no login: {e}")
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_user', None)
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@requires_admin
def admin_dashboard():
    if not supabase:
        flash('Sistema de administração indisponível', 'error')
        return redirect('/')
    
    try:
        # Buscar estatísticas
        stats_result = supabase.table('vw_estatisticas_admin').select('*').limit(1).execute()
        stats = stats_result.data[0] if stats_result.data else {}
        
        # Buscar diagnósticos recentes
        recent_result = supabase.table('vw_diagnosticos_completos').select('*').limit(10).execute()
        recent_diagnosticos = recent_result.data
        
        return render_template('admin/dashboard.html', 
                               stats=stats, 
                               recent_diagnosticos=recent_diagnosticos)
    except Exception as e:
        flash('Erro ao carregar dados do dashboard', 'error')
        print(f"Erro no dashboard: {e}")
        return render_template('admin/dashboard.html', stats={}, recent_diagnosticos=[])

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

# Para Vercel - exportar a aplicação
if __name__ != '__main__':
    # Configurações para produção na Vercel
    app.config['DEBUG'] = False
