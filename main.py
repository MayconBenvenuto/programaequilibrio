from flask import Flask, render_template, request, jsonify, send_file, url_for, redirect
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import io
import base64

app = Flask(__name__)

# Configuração para arquivos estáticos e templates
app.static_folder = 'static'
app.template_folder = 'templates'

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
        
        # Salvar dados temporariamente
        with open('temp_diagnostico.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        # Gerar análise
        analise = gerar_analise(dados)
        
        return jsonify({
            'status': 'success',
            'analise': analise,
            'redirect': '/resultado'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/resultado')
def resultado():
    try:
        with open('temp_diagnostico.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        analise = gerar_analise(dados)
        return render_template('resultado.html', dados=dados, analise=analise)
    except FileNotFoundError:
        return redirect('/')

@app.route('/gerar_pdf')
def gerar_pdf():
    try:
        # Verificar se o arquivo existe
        if not os.path.exists('temp_diagnostico.json'):
            return jsonify({'error': 'Dados do diagnóstico não encontrados. Refaça o questionário.'}), 404
        
        with open('temp_diagnostico.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print(f"Dados carregados: {dados}")  # Debug
        
        analise = gerar_analise(dados)
        print(f"Análise gerada: {analise}")  # Debug
        
        pdf_buffer = criar_pdf_relatorio(dados, analise)
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

def gerar_analise(dados):
    """Gera análise baseada nas respostas do questionário"""
    respostas = dados.get('respostas', {})
    
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

def criar_pdf_relatorio(dados, analise):
    """Cria um relatório PDF profissional com a logo da Belz Conecta Saúde"""
    buffer = io.BytesIO()
    
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
        canvas.drawRightString(width - 30, y_start + 15, f"Relatório gerado em: {analise['data_diagnostico']}")
        
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
    
    dados_empresa = dados.get('dados_empresa', {})
    empresa_info = [
        f"Empresa: {dados_empresa.get('razao_social', 'N/A')}",
        f"CNPJ: {dados_empresa.get('cnpj', 'N/A')}",
        f"RH Responsável: {dados_empresa.get('rh_responsavel', 'N/A')}",
        f"Cargo: {dados_empresa.get('cargo', 'N/A')}",
        f"E-mail: {dados_empresa.get('email', 'N/A')}",
        f"Número de Colaboradores: {dados_empresa.get('num_colaboradores', 'N/A')}"
    ]
    
    current_y = draw_info_box(p, 50, current_y, "Dados Cadastrais", empresa_info)
    current_y -= 20
    
    # Resumo do Diagnóstico
    current_y = draw_section_header(p, 50, current_y, "🎯 RESUMO DO DIAGNÓSTICO")
    
    resumo_info = [
        f"Nível de Risco: {analise['nivel_risco']}",
        f"Questões Críticas Identificadas: {analise['questoes_criticas']}",
        f"Áreas de Foco: {', '.join(analise['areas_foco']) if analise['areas_foco'] else 'Prevenção Geral'}",
        f"Total de Ações Recomendadas: {len(analise['acoes_recomendadas'])}"
    ]
    
    # Cor baseada no nível de risco
    if "Alto" in analise['nivel_risco']:
        cor_resumo = "#dc3545"
    elif "Moderado" in analise['nivel_risco']:
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
    
    for i, acao in enumerate(analise['acoes_recomendadas']):
        if "Comunicação" in acao:
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
    timeline_items = [
        ("🚨 IMEDIATO (0-30 dias)", [acao for acao in analise['acoes_recomendadas'] if "Comunicação" in acao], "#dc3545"),
        ("⚠️ MÉDIO PRAZO (30-60 dias)", [acao for acao in analise['acoes_recomendadas'] if "Ergonômica" in acao], "#fd7e14"),
        ("📊 LONGO PRAZO (60+ dias)", ["Implementar pesquisas de clima trimestrais", "Criar programa de saúde ocupacional permanente"], "#28a745")
    ]
    
    for fase, acoes, cor in timeline_items:
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
