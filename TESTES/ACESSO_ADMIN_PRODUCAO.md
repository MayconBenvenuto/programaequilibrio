# 🌐 Acesso ao Painel Admin em Produção

## 📍 URLs de Acesso em Produção

### 🚀 Vercel (Recomendado)

```url
https://seu-projeto.vercel.app/admin/login
```

### 🐳 Docker/VPS

```url
https://seudominio.com/admin/login
```

### ☁️ Heroku

```url
https://seu-app.herokuapp.com/admin/login
```

## 🔐 Configuração de Segurança em Produção

### 1. Alterar Credenciais Padrão

⚠️ **CRÍTICO:** Nunca use as credenciais padrão em produção!

#### Via Variáveis de Ambiente (Recomendado)

```bash
# No seu .env de produção
ADMIN_EMAIL=seu-admin@empresa.com
ADMIN_PASSWORD=SuaSenhaSegura123!@#
FLASK_SECRET_KEY=chave-secreta-super-complexa-aqui
```

#### Via SQL no Banco de Produção

```sql
-- 1. Primeiro, gere o hash da senha (use bcrypt)
-- 2. Execute no Supabase SQL Editor:

UPDATE admin_users 
SET 
    email = 'seu-admin@empresa.com',
    senha_hash = '$2b$12$hash_da_sua_senha_aqui',
    nome = 'Seu Nome Completo'
WHERE email = 'admin@conecta.com';
```

### 2. Configurar HTTPS (SSL)

#### Para Vercel (Automático)

```json
// vercel.json
{
  "functions": {
    "main.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/main.py"
    }
  ],
  "headers": [
    {
      "source": "/admin/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options", 
          "value": "nosniff"
        }
      ]
    }
  ]
}
```

#### Para VPS/Docker

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name seudominio.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/private.key;
    
    location /admin {
        # Proteções extras para área admin
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛡️ Segurança Avançada

### 1. Autenticação em Duas Etapas (2FA)

Adicione ao `main.py`:

```python
import pyotp
import qrcode
from io import BytesIO
import base64

@app.route('/admin/setup-2fa')
@admin_required
def setup_2fa():
    """Configurar autenticação em duas etapas"""
    user = get_current_admin()
    
    if not user.get('totp_secret'):
        # Gerar nova chave TOTP
        secret = pyotp.random_base32()
        
        # Atualizar usuário com a chave
        supabase.table('admin_users').update({
            'totp_secret': secret
        }).eq('id', user['id']).execute()
        
        # Gerar QR Code
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user['email'],
            issuer_name="Programa Equilíbrio"
        )
        
        # Criar QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code = base64.b64encode(buffer.getvalue()).decode()
        
        return render_template('admin/setup_2fa.html', 
                             qr_code=qr_code, secret=secret)
```

### 2. Whitelist de IPs

```python
# Lista de IPs permitidos para admin
ADMIN_ALLOWED_IPS = [
    '192.168.1.100',  # Seu IP do escritório
    '203.0.113.0/24'  # Rede da empresa
]

def check_admin_ip():
    """Verifica se IP está na whitelist"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    return client_ip in ADMIN_ALLOWED_IPS

@app.before_request
def limit_admin_access():
    """Limita acesso admin por IP"""
    if request.path.startswith('/admin/') and not check_admin_ip():
        abort(403, "Acesso negado para este IP")
```

## 🚀 Deploy em Produção

### Opção 1: Vercel (Mais Simples)

1. **Configure o projeto:**

```bash
# Instale Vercel CLI
npm i -g vercel

# No diretório do projeto
vercel login
vercel
```

1. **Configure variáveis no Vercel:**

- Acesse dashboard do Vercel
- Vá em Settings > Environment Variables
- Adicione:
  - `SUPABASE_URL`: sua URL do Supabase
  - `SUPABASE_ANON_KEY`: sua chave do Supabase
  - `FLASK_SECRET_KEY`: chave secreta forte
  - `ADMIN_EMAIL`: email do admin
  - `ADMIN_PASSWORD`: senha do admin

1. **URL final:**

```url
https://seu-projeto.vercel.app/admin/login
```

### Opção 2: VPS com Docker

1. **Dockerfile para produção:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

1. **docker-compose.yml:**

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
    restart: unless-stopped
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - web
```

### Opção 3: Heroku

1. **Configure o Heroku:**

```bash
# Instale Heroku CLI
# Faça login e crie app
heroku create seu-app-nome

# Configure variáveis
heroku config:set SUPABASE_URL=sua_url
heroku config:set SUPABASE_ANON_KEY=sua_chave
heroku config:set FLASK_SECRET_KEY=chave_secreta
```

1. **Procfile:**

```text
web: gunicorn main:app
```

## 🔒 Checklist de Segurança Pré-Deploy

### ✅ Obrigatório

- [ ] Alterar credenciais padrão do admin
- [ ] Configurar HTTPS/SSL
- [ ] Definir `FLASK_SECRET_KEY` forte
- [ ] Configurar variáveis de ambiente
- [ ] Testar conexão com Supabase em produção
- [ ] Verificar logs de erro

### ✅ Recomendado

- [ ] Implementar 2FA
- [ ] Configurar whitelist de IPs
- [ ] Configurar rate limiting
- [ ] Implementar logs de auditoria
- [ ] Configurar backup automático
- [ ] Testar recuperação de desastres

### ✅ Avançado

- [ ] Configurar CDN (Cloudflare)
- [ ] Implementar WAF (Web Application Firewall)
- [ ] Configurar monitoramento (Sentry)
- [ ] Implementar cache Redis
- [ ] Configurar alertas de segurança

## 🆘 Recuperação de Acesso

### Se Perdeu Acesso ao Admin

1. **Via Supabase SQL Editor:**

```sql
-- Resetar senha (use hash bcrypt real)
UPDATE admin_users 
SET senha_hash = '$2b$12$nova_senha_hash_aqui'
WHERE email = 'seu-email@admin.com';
```

1. **Criar novo admin de emergência:**

```sql
INSERT INTO admin_users (email, senha_hash, nome, ativo, criado_em)
VALUES (
    'emergencia@admin.com',
    '$2b$12$hash_da_senha_emergencia',
    'Admin Emergência',
    true,
    NOW()
);
```

## 📊 Monitoramento em Produção

### Logs Importantes

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.before_request  
def log_admin_access():
    """Log todos os acessos à área admin"""
    if request.path.startswith('/admin/'):
        logging.info(f"Admin access: {request.remote_addr} -> {request.path}")
```

### Métricas para Acompanhar

- Tentativas de login falhadas
- Tempo de resposta das páginas admin
- Uso de recursos (CPU/Memória)
- Acessos por país/região
- Erros 500 na área admin

---

**🔥 IMPORTANTE:** Sempre teste o acesso admin em produção imediatamente após o deploy para garantir que tudo funciona corretamente!
