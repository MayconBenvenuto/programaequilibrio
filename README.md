# Programa Equilíbrio - Belz Conecta Saúde

Sistema de Diagnóstico Corporativo de Saúde Mental e Ergonomia

## 📋 Sobre o Projeto

O **Programa Equilíbrio** é uma aplicação web desenvolvida para a **Belz Conecta Saúde** que oferece um diagnóstico corporativo completo focado em duas áreas principais:

- 🧠 **Saúde Mental**: Avaliação de fatores de estresse, burnout e bem-estar psicológico
- 🔧 **Ergonomia**: Análise do ambiente de trabalho e prevenção de lesões ocupacionais

## 🚀 Funcionalidades

### ✨ Principais Recursos

- **Formulário de Dados da Empresa**: Coleta informações básicas da organização
- **Questionário Interativo**: 10 perguntas estratégicas sobre saúde mental e ergonomia
- **Análise Inteligente**: Processamento automático das respostas com recomendações
- **Relatório Completo**: Visualização detalhada dos resultados
- **Export em PDF**: Download do diagnóstico completo com logo e bordas arredondadas
- **Interface Responsiva**: Funciona em desktop, tablet e mobile
- **Design Moderno**: Interface com emojis informativos e visual profissional

### 📊 Estrutura do Questionário

1. **🧠 Fatores de estresse** - Identificação das principais fontes de estresse
2. **📊 Afastamentos por transtornos mentais** - Histórico de problemas de saúde mental
3. **😴 Sinais de esgotamento** - Detecção precoce de burnout
4. **🎭 Ações de saúde mental realizadas** - Mapeamento de iniciativas existentes
5. **🏢 Perfil da atividade** - Tipo de ambiente de trabalho
6. **🦴 Queixas de dores físicas** - Identificação de problemas ergonômicos
7. **🔍 Avaliação ergonômica** - Histórico de diagnósticos técnicos
8. **🏃 Ações preventivas em ergonomia** - Iniciativas ergonômicas implementadas
9. **🎯 Prioridade do RH** - Nível de importância estratégica
10. **🤝 Necessidade de apoio externo** - Abertura para parcerias

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.13 + Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.1.3
- **PDF**: ReportLab 4.0.4 + Pillow (para imagens)
- **Ícones**: Font Awesome 6.0.0
- **Responsividade**: Bootstrap Grid System

## 📦 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clone do repositório)

### Desenvolvimento Local

1. **Clone ou baixe o projeto**
   ```bash
   git clone [url-do-repositorio]
   cd programaequilibrio
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute a aplicação**
   ```bash
   python main.py
   ```

6. **Acesse o sistema**
   - Abra seu navegador
   - Vá para: `http://localhost:5000`

## 🚀 Deploy em Produção

### 📋 requirements.txt

Certifique-se de que o arquivo `requirements.txt` contém:

```txt
Flask==2.3.3
reportlab==4.0.4
Pillow==10.0.1
gunicorn==21.2.0
```

### 🖥️ Deploy em Servidor Linux (Ubuntu/Debian)

#### 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
sudo apt install python3 python3-pip python3-venv nginx -y

# Instalar supervisor para gerenciar processos
sudo apt install supervisor -y
```

#### 2. Configurar o Projeto

```bash
# Ir para diretório de projetos
cd /var/www/

# Clonar projeto
sudo git clone [url-do-repositorio] programaequilibrio
sudo chown -R www-data:www-data programaequilibrio
cd programaequilibrio

# Criar ambiente virtual
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install -r requirements.txt
```

#### 3. Configurar Gunicorn

Criar arquivo `/var/www/programaequilibrio/gunicorn.conf.py`:

```python
bind = "127.0.0.1:5000"
workers = 2
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
user = "www-data"
group = "www-data"
tmp_upload_dir = None
```

#### 4. Configurar Supervisor

Criar arquivo `/etc/supervisor/conf.d/programaequilibrio.conf`:

```ini
[program:programaequilibrio]
command=/var/www/programaequilibrio/.venv/bin/gunicorn -c gunicorn.conf.py main:app
directory=/var/www/programaequilibrio
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/programaequilibrio.log
```

#### 5. Configurar Nginx

Criar arquivo `/etc/nginx/sites-available/programaequilibrio`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;  # Substitua pelo seu domínio
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 50M;
    }
    
    location /static/ {
        alias /var/www/programaequilibrio/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

#### 6. Ativar Configurações

```bash
# Ativar site no Nginx
sudo ln -s /etc/nginx/sites-available/programaequilibrio /etc/nginx/sites-enabled/

# Testar configuração Nginx
sudo nginx -t

# Recarregar Supervisor e Nginx
sudo supervisorctl reread
sudo supervisorctl update
sudo systemctl restart nginx
```

### 🔒 Configurar HTTPS com Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com

# Renovação automática
sudo crontab -e
# Adicionar linha:
0 3 * * * certbot renew --quiet
```

### ☁️ Deploy na AWS EC2

#### 1. Criar Instância EC2

- Escolha Ubuntu 20.04 LTS ou superior
- Tipo: t2.micro (para testes) ou t2.small (produção)
- Configure Security Group:
  - HTTP (80)
  - HTTPS (443)
  - SSH (22)

#### 2. Conectar e Configurar

```bash
# Conectar via SSH
ssh -i sua-chave.pem ubuntu@ip-da-instancia

# Seguir passos de "Deploy em Servidor Linux" acima
```

#### 3. Configurar Elastic IP (Opcional)

- No Console AWS, vá em EC2 > Elastic IPs
- Aloque um IP estático
- Associe à sua instância

### 🐋 Deploy com Docker

#### 1. Criar Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "2", "main:app"]
```

#### 2. Criar docker-compose.yml

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./static:/app/static:ro
    environment:
      - FLASK_ENV=production
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/var/www/static:ro
    depends_on:
      - web
    restart: unless-stopped
```

#### 3. Executar

```bash
# Build e executar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### ⚡ Deploy na Vercel (Recomendado)

A Vercel oferece deploy simples e gratuito para aplicações Flask.

#### **1. Preparar o Projeto**

Os seguintes arquivos já estão configurados:
- ✅ `vercel.json` - Configuração da Vercel
- ✅ `requirements.txt` - Dependências otimizadas
- ✅ `main.py` - Configurado para produção

#### **2. Deploy via CLI**

```bash
# Instalar Vercel CLI
npm i -g vercel

# Fazer login
vercel login

# Deploy
vercel

# Deploy em produção
vercel --prod
```

#### **3. Deploy via GitHub (Mais Fácil)**

1. **Criar Repositório no GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/programa-equilibrio.git
   git push -u origin main
   ```

2. **Conectar à Vercel**:
   - Acesse https://vercel.com
   - Clique em "New Project"
   - Conecte com GitHub
   - Selecione seu repositório
   - Configure:
     - Framework: **Other**
     - Root Directory: **/** (raiz)
     - Build Command: **(deixe vazio)**
     - Output Directory: **(deixe vazio)**
   - Clique em "Deploy"

3. **Deploy Automático**:
   - Cada push no GitHub fará deploy automático
   - URL será fornecida automaticamente

#### **4. Variáveis de Ambiente (se necessário)**

No dashboard da Vercel:
- Settings → Environment Variables
- Adicione se precisar:
  ```
  FLASK_ENV=production
  DEBUG=False
  ```

### 📊 Monitoramento em Produção

#### 1. Logs do Sistema

```bash
# Ver logs Supervisor
sudo tail -f /var/log/supervisor/programaequilibrio.log

# Ver logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### 2. Monitoramento de Performance

```bash
# CPU e Memória
htop

# Conexões de rede
netstat -tulpn | grep :5000

# Espaço em disco
df -h
```

### 🔧 Configurações de Produção

#### 1. Variáveis de Ambiente

Criar arquivo `.env`:

```env
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=False
```

#### 2. Modificar main.py para produção

```python
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    app.run(
        debug=debug_mode,
        host='0.0.0.0',
        port=port
    )
```

### 🛡️ Segurança em Produção

#### 1. Firewall

```bash
# Configurar UFW
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

#### 2. Backup Automatizado

```bash
# Criar script de backup
sudo nano /usr/local/bin/backup-programaequilibrio.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/programaequilibrio"
DATE=$(date +"%Y%m%d_%H%M%S")

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz /var/www/programaequilibrio

# Manter apenas últimos 7 backups
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
```

```bash
# Tornar executável
sudo chmod +x /usr/local/bin/backup-programaequilibrio.sh

# Agendar no cron (backup diário)
sudo crontab -e
# Adicionar:
0 2 * * * /usr/local/bin/backup-programaequilibrio.sh
```

## 📁 Estrutura do Projeto

```
programaequilibrio/
├── main.py                 # Aplicação principal Flask
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
├── temp_diagnostico.json  # Dados temporários (criado automaticamente)
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial
│   ├── questionario.html # Formulário de perguntas
│   └── resultado.html    # Página de resultados
└── static/               # Arquivos estáticos
    ├── css/
    │   └── style.css     # Estilos customizados
    └── js/
        └── main.js       # JavaScript principal
```

## 🎯 Como Usar

### 1. Página Inicial
- Preencha os dados da empresa (Razão Social, CNPJ, RH Responsável, etc.)
- Clique em "Iniciar Diagnóstico"

### 2. Questionário
- Responda as 10 perguntas do diagnóstico
- Use os botões "Anterior" e "Próxima" para navegar
- Acompanhe o progresso na barra superior
- Clique em "Finalizar Diagnóstico" na última pergunta

### 3. Resultado
- Visualize o resumo do diagnóstico
- Veja as recomendações de ações primárias
- Confira o plano de ação sugerido
- Exporte o relatório completo em PDF

## 📊 Sistema de Análise

O sistema analisa as respostas e gera automaticamente:

### Métricas Calculadas
- **Questões Críticas**: Número de áreas que precisam de atenção imediata
- **Ações Recomendadas**: Programas específicos sugeridos
- **Horas de Treinamento**: Estimativa de tempo necessário

### Recomendações Automáticas

**🧠 Saúde Mental**
- **Programa**: Comunicação Não Violenta e Segurança Psicológica
- **Duração**: 5 horas
- **Público**: Todos os colaboradores + Lideranças

**🔧 Ergonomia**
- **Consultoria**: Avaliação Ergonômica Completa
- **Duração**: 16 horas
- **Público**: RH + Lideranças + SESMT

### Plano de Ação Temporizado
- **🚨 Imediatas (30 dias)**: Ações críticas de saúde mental
- **⚠️ Médio Prazo (60 dias)**: Avaliações ergonômicas
- **📊 Contínuas (90+ dias)**: Monitoramento e indicadores

## 🎨 Personalização

### Cores e Marca
As cores principais podem ser alteradas no arquivo `static/css/style.css`:

```css
:root {
    --primary-color: #2B5AA0;  /* Azul Belz */
    --secondary-color: #E8F4FD; /* Azul claro */
    --success-color: #28a745;   /* Verde */
    --warning-color: #ffc107;   /* Amarelo */
    --danger-color: #dc3545;    /* Vermelho */
}
```

### Perguntas do Questionário
As perguntas podem ser modificadas no arquivo `main.py` na variável `PERGUNTAS`.

## 🔧 Configurações Avançadas

### Modo Debug
Para desenvolvimento, o debug está habilitado por padrão. Para produção, altere:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Porta Personalizada
Para usar uma porta diferente:

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Porta 8080
```

### SSL/HTTPS
Para usar HTTPS em produção, adicione os certificados:

```python
app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
```

## 📄 Geração de PDF

O sistema gera automaticamente um relatório PDF com:

- ✅ Dados da empresa
- ✅ Resumo visual com gráficos
- ✅ Recomendações detalhadas
- ✅ Plano de ação temporal
- ✅ Branding da Belz Conecta Saúde

## 🐛 Solução de Problemas

### Erro: Porta já em uso
```bash
# Windows - mate o processo na porta 5000
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F

# Linux/Mac
sudo lsof -t -i tcp:5000 | xargs kill -9
```

### Erro: Módulo não encontrado
```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt
```

### Erro: Permissão negada
```bash
# Execute como administrador (Windows)
# Ou use sudo (Linux/Mac)
```

### � Checklist de Deploy

#### ✅ Antes do Deploy

- [ ] Testar aplicação localmente
- [ ] Verificar todas as dependências no `requirements.txt`
- [ ] Configurar variáveis de ambiente (`.env`)
- [ ] Testar geração de PDF
- [ ] Verificar se logo está no diretório `static/images/`
- [ ] Criar backup dos dados (se aplicável)
- [ ] Documentar credenciais de acesso

#### ✅ Durante o Deploy

- [ ] Configurar servidor/plataforma
- [ ] Instalar dependências
- [ ] Configurar proxy reverso (Nginx)
- [ ] Configurar SSL/HTTPS
- [ ] Testar conectividade
- [ ] Configurar monitoramento
- [ ] Configurar backups automáticos

#### ✅ Após o Deploy

- [ ] Testar todas as funcionalidades
- [ ] Verificar logs de erro
- [ ] Configurar alertas
- [ ] Documentar URLs de produção
- [ ] Treinar usuários finais
- [ ] Criar procedimentos de manutenção

### 🎯 URLs Importantes (Produção)

Depois do deploy, as seguintes URLs estarão disponíveis:

- **Principal**: `https://seu-dominio.com/`
- **Questionário**: `https://seu-dominio.com/questionario`  
- **Health Check**: `https://seu-dominio.com/health`
- **Arquivos Estáticos**: `https://seu-dominio.com/static/`

### 🆘 Troubleshooting

#### Problemas Comuns

1. **Erro 502 Bad Gateway**
   ```bash
   # Verificar se Gunicorn está rodando
   sudo supervisorctl status programaequilibrio
   
   # Reiniciar se necessário
   sudo supervisorctl restart programaequilibrio
   ```

2. **PDF não gera / Logo não aparece**
   ```bash
   # Verificar permissões do diretório static
   ls -la static/images/logo-conecta.png
   
   # Corrigir permissões se necessário
   sudo chown www-data:www-data static/images/logo-conecta.png
   ```

3. **Porta já em uso**
   ```bash
   # Linux: encontrar processo na porta
   sudo lsof -t -i tcp:5000 | xargs kill -9
   
   # Windows: matar processo na porta
   netstat -ano | findstr :5000
   taskkill /PID [PID_NUMBER] /F
   ```

4. **Erro de importação PIL/Pillow**
   ```bash
   # Instalar dependências de sistema (Ubuntu/Debian)
   sudo apt install libjpeg-dev zlib1g-dev libfreetype6-dev
   
   # Reinstalar Pillow
   pip uninstall Pillow
   pip install Pillow
   ```

### 📱 Contato para Suporte

- **Desenvolvedor**: GitHub Copilot
- **Empresa**: Belz Conecta Saúde  
- **Sistema**: Programa Equilíbrio v1.0
- **Data**: Agosto 2025

---

## 📂 Arquivos de Deploy Incluídos

Este repositório já inclui todos os arquivos necessários para deploy:

- `requirements.txt` - Dependências Python
- `Procfile` - Configuração Heroku
- `runtime.txt` - Versão Python para Heroku  
- `Dockerfile` - Configuração Docker
- `docker-compose.yml` - Orquestração de containers
- `nginx.conf` - Configuração Nginx
- `.env.example` - Exemplo de variáveis de ambiente

## 📊 Estrutura Final do Projeto

```
programaequilibrio/
├── main.py                    # Aplicação Flask principal
├── requirements.txt           # Dependências Python
├── Procfile                  # Config Heroku
├── runtime.txt               # Versão Python
├── Dockerfile               # Config Docker
├── docker-compose.yml       # Orquestração
├── nginx.conf              # Config Nginx
├── .env.example            # Variáveis exemplo
├── README.md               # Esta documentação
├── temp_diagnostico.json   # Cache temporário
├── templates/              # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── questionario.html
│   └── resultado.html
└── static/                 # Arquivos estáticos
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
        └── logo-conecta.png
```

## 📈 Próximas Funcionalidades

- [ ] Dashboard administrativo
- [ ] Histórico de diagnósticos
- [ ] Comparativo temporal
- [ ] API para integração
- [ ] App mobile
- [ ] Relatórios gerenciais
- [ ] Sistema de notificações
- [ ] Multi-idiomas

## 📄 Licença

© 2025 Belz Conecta Saúde - Todos os direitos reservados.

---

**Desenvolvido com ❤️ para a Belz Conecta Saúde**
