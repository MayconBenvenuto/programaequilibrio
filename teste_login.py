import sys
sys.path.append('.')

try:
    from main import app, ADMIN_EMAIL, ADMIN_PASSWORD, supabase
    print('✅ Importação bem-sucedida')
    print(f'ADMIN_EMAIL: {ADMIN_EMAIL}')
    print(f'ADMIN_PASSWORD: {ADMIN_PASSWORD}')
    print(f'Supabase disponível: {supabase is not None}')
    
    with app.test_client() as client:
        print('\n🧪 Testando endpoint de login...')
        
        # Testar GET (página de login)
        response = client.get('/admin/login')
        print(f'GET /admin/login - Status: {response.status_code}')
        
        # Testar POST (login)
        print('\n📤 Enviando credenciais: admin/admin123')
        response = client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=False)
        
        print(f'POST /admin/login - Status: {response.status_code}')
        print(f'Headers: {dict(response.headers)}')
        
        if response.status_code == 302:
            print(f'✅ Redirecionamento para: {response.headers.get("Location")}')
        elif response.status_code == 200:
            print('⚠️ Status 200 - verificando conteúdo...')
            content = response.get_data(as_text=True)
            if 'Login Administrativo' in content:
                print('❌ Voltou para página de login')
                # Procurar mensagens de erro
                if 'alert-danger' in content or 'Credenciais inválidas' in content:
                    print('🔍 Mensagem de erro encontrada na página')
            else:
                print('❓ Conteúdo desconhecido')
        
except Exception as e:
    print(f'❌ Erro: {e}')
    import traceback
    traceback.print_exc()
