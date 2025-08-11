# 🔧 Guia de Configuração do .env

## 📋 Como Configurar as Variáveis de Ambiente

### 1. Copie o Arquivo de Exemplo

```bash
cp .env.example .env
```

### 2. Configure Suas Variáveis

Edite o arquivo `.env` com suas configurações reais:

## 🔑 Configurações Obrigatórias

### Supabase (Banco de Dados)

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua_chave_publica_aqui
```

**Como obter:**
1. Acesse [supabase.com](https://supabase.com)
2. Crie/acesse seu projeto
3. Vá em Settings > API
4. Copie a URL e a chave pública (anon key)

### Segurança da Aplicação

```env
FLASK_SECRET_KEY=uma-chave-super-secreta-de-pelo-menos-32-caracteres
```

**Como gerar:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

## ⚙️ Configurações Administrativas

### Credenciais do Admin

```env
ADMIN_EMAIL=seu-admin@empresa.com
ADMIN_PASSWORD=SuaSenhaSegura123!
ADMIN_NAME=Seu Nome Completo
```

**⚠️ IMPORTANTE:** Mude as credenciais padrão!

## 🌐 Configurações por Ambiente

### 🔧 Desenvolvimento Local

```env
FLASK_ENV=development
DEBUG=True
SESSION_COOKIE_SECURE=False
```

### 🚀 Produção

```env
FLASK_ENV=production
DEBUG=False
SESSION_COOKIE_SECURE=True
```

## 📊 Configurações Avançadas (Opcionais)

### APIs Externas

```env
# Timeouts das APIs (em segundos)
RECEITAWS_TIMEOUT=15
VIACEP_TIMEOUT=10
```

### Segurança

```env
# Tempo de sessão (em segundos)
PERMANENT_SESSION_LIFETIME=3600
ADMIN_SESSION_TIMEOUT=7200

# Proteção CSRF
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600
```

### Logs

```env
LOG_LEVEL=INFO
LOG_FILE=/var/log/programaequilibrio.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5
```

### Email (Opcional)

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app
```

## 🔒 Boas Práticas de Segurança

### ✅ Sempre Faça

1. **Use senhas fortes** (mín. 12 caracteres)
2. **Gere chaves secretas únicas** para cada ambiente
3. **Configure HTTPS** em produção
4. **Mantenha .env fora do Git** (já está no .gitignore)
5. **Use variáveis diferentes** para dev/prod

### ❌ Nunca Faça

1. **Não commite** o arquivo .env
2. **Não use** credenciais padrão em produção
3. **Não compartilhe** chaves de produção
4. **Não use HTTP** em produção
5. **Não deixe DEBUG=True** em produção

## 🚀 Configuração para Deploy

### Vercel

Configure no dashboard:
- Settings > Environment Variables
- Adicione todas as variáveis do .env

### Heroku

```bash
heroku config:set FLASK_SECRET_KEY=sua-chave
heroku config:set SUPABASE_URL=sua-url
heroku config:set SUPABASE_ANON_KEY=sua-chave
# ... outras variáveis
```

### Docker

Use arquivo `.env` ou configure no `docker-compose.yml`:

```yaml
environment:
  - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
  - SUPABASE_URL=${SUPABASE_URL}
  - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
```

## 🆘 Solução de Problemas

### "Configurações do Supabase não encontradas"

```env
# Verifique se as variáveis estão corretas:
SUPABASE_URL=https://projeto.supabase.co  # ✅ Correto
SUPABASE_ANON_KEY=eyJ...                 # ✅ Correto (chave longa)

# Erros comuns:
SUPABASE_URL=projeto.supabase.co         # ❌ Falta https://
SUPABASE_KEY=eyJ...                      # ❌ Nome errado (deveria ser ANON_KEY)
```

### "Admin não consegue fazer login"

```env
# Verifique as credenciais:
ADMIN_EMAIL=admin@conecta.com           # ✅ Email válido
ADMIN_PASSWORD=admin123                 # ⚠️ Mude em produção!
```

### "Erro de chave secreta"

```env
# Chave muito curta ou padrão:
FLASK_SECRET_KEY=123                    # ❌ Muito simples
FLASK_SECRET_KEY=sua-chave-secreta-super-segura-aqui  # ❌ Valor padrão

# Correto:
FLASK_SECRET_KEY=f8d9a7b6c5e4d3c2b1a0  # ✅ Única e segura
```

## 📝 Template Completo

Aqui está um template completo para copiar:

```env
# ========================================
# PROGRAMA EQUILÍBRIO - CONFIGURAÇÕES
# ========================================

# Aplicação
FLASK_ENV=production
DEBUG=False
FLASK_SECRET_KEY=sua-chave-unica-aqui
PORT=5000

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua_chave_publica_aqui

# Administração
ADMIN_EMAIL=admin@empresa.com
ADMIN_PASSWORD=SenhaSegura123!
ADMIN_NAME=Administrador
ADMIN_SESSION_TIMEOUT=7200

# APIs
RECEITAWS_TIMEOUT=15
VIACEP_TIMEOUT=10

# Segurança
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600

# Logs
LOG_LEVEL=INFO
LOG_FILE=/var/log/programaequilibrio.log
```

---

**🔥 Lembre-se:** Sempre teste suas configurações antes de fazer deploy!
