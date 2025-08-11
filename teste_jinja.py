from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
import sys
import os

try:
    # Configurar o ambiente Jinja2
    template_dir = 'templates'
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Tentar carregar o template
    print("🔍 Testando template 'questionario.html'...")
    template = env.get_template('questionario.html')
    print("✅ Template carregado sem erro de sintaxe!")
    
    # Tentar renderizar com dados de teste
    perguntas_teste = [
        {
            'id': 1,
            'pergunta': 'Teste pergunta',
            'opcoes': ['Opção 1', 'Opção 2']
        }
    ]
    
    resultado = template.render(perguntas=perguntas_teste)
    print("✅ Template renderizado com sucesso!")
    print(f"📏 Tamanho do HTML: {len(resultado)} caracteres")
    
except TemplateSyntaxError as e:
    print(f"❌ Erro de sintaxe no template:")
    print(f"   Linha {e.lineno}: {e.message}")
    if e.filename:
        print(f"   Arquivo: {e.filename}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Erro geral: {e}")
    sys.exit(1)

print("🎉 Template está funcionando perfeitamente!")
