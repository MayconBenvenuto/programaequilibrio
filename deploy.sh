#!/bin/bash

# Script de Deploy Automático - Programa Equilíbrio
# Belz Conecta Saúde

set -e  # Parar execução em caso de erro

echo "🚀 Iniciando deploy do Programa Equilíbrio..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para exibir status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# Verificar se está rodando como root (necessário para algumas operações)
if [[ $EUID -eq 0 ]]; then
   print_warning "Rodando como root. Recomenda-se usar sudo apenas quando necessário."
fi

# 1. Atualizar sistema
print_status "Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências do sistema
print_status "Instalando dependências do sistema..."
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git curl

# 3. Parar serviços se já estiverem rodando
print_status "Parando serviços existentes..."
sudo systemctl stop nginx || true
sudo supervisorctl stop programaequilibrio || true

# 4. Configurar diretório do projeto
PROJECT_DIR="/var/www/programaequilibrio"
print_status "Configurando diretório do projeto em $PROJECT_DIR..."

if [ -d "$PROJECT_DIR" ]; then
    print_warning "Diretório já existe. Fazendo backup..."
    sudo mv "$PROJECT_DIR" "/var/www/programaequilibrio.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 5. Clonar/copiar projeto
print_status "Copiando arquivos do projeto..."
sudo mkdir -p "$PROJECT_DIR"
sudo cp -r . "$PROJECT_DIR/"
sudo chown -R www-data:www-data "$PROJECT_DIR"

# 6. Configurar ambiente virtual
print_status "Configurando ambiente virtual Python..."
cd "$PROJECT_DIR"
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install --upgrade pip
sudo -u www-data .venv/bin/pip install -r requirements.txt

# 7. Criar configuração do Gunicorn se não existir
if [ ! -f "$PROJECT_DIR/gunicorn.conf.py" ]; then
    print_status "Criando configuração do Gunicorn..."
    sudo tee "$PROJECT_DIR/gunicorn.conf.py" > /dev/null <<EOF
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
EOF
fi

# 8. Configurar Supervisor
print_status "Configurando Supervisor..."
sudo tee /etc/supervisor/conf.d/programaequilibrio.conf > /dev/null <<EOF
[program:programaequilibrio]
command=$PROJECT_DIR/.venv/bin/gunicorn -c gunicorn.conf.py main:app
directory=$PROJECT_DIR
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/programaequilibrio.log
environment=PATH="$PROJECT_DIR/.venv/bin"
EOF

# 9. Configurar Nginx
print_status "Configurando Nginx..."
sudo tee /etc/nginx/sites-available/programaequilibrio > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    location /static/ {
        alias $PROJECT_DIR/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# 10. Ativar site Nginx
print_status "Ativando site no Nginx..."
sudo ln -sf /etc/nginx/sites-available/programaequilibrio /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 11. Testar configurações
print_status "Testando configurações..."
sudo nginx -t
if [ $? -ne 0 ]; then
    print_error "Erro na configuração do Nginx!"
    exit 1
fi

# 12. Recarregar serviços
print_status "Iniciando serviços..."
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start programaequilibrio
sudo systemctl restart nginx
sudo systemctl enable nginx

# 13. Configurar firewall (opcional)
if command -v ufw &> /dev/null; then
    print_status "Configurando firewall..."
    sudo ufw allow ssh
    sudo ufw allow 'Nginx Full'
    sudo ufw --force enable
fi

# 14. Verificar se serviços estão funcionando
print_status "Verificando serviços..."
sleep 5

# Verificar Supervisor
if sudo supervisorctl status programaequilibrio | grep -q RUNNING; then
    print_success "Gunicorn está rodando via Supervisor"
else
    print_error "Problema com Gunicorn/Supervisor"
    sudo supervisorctl status programaequilibrio
fi

# Verificar Nginx
if sudo systemctl is-active --quiet nginx; then
    print_success "Nginx está ativo"
else
    print_error "Problema com Nginx"
fi

# 15. Testar aplicação
print_status "Testando aplicação..."
if curl -f http://localhost/ > /dev/null 2>&1; then
    print_success "Aplicação respondendo corretamente!"
else
    print_warning "Aplicação pode não estar respondendo corretamente"
fi

# 16. Mostrar informações finais
print_success "Deploy concluído!"
echo ""
echo "📋 Informações do Deploy:"
echo "  • Diretório: $PROJECT_DIR"
echo "  • URL: http://$(curl -s ifconfig.me || echo 'SEU-IP-AQUI')"
echo "  • Logs Gunicorn: /var/log/supervisor/programaequilibrio.log"
echo "  • Logs Nginx: /var/log/nginx/"
echo ""
echo "🔧 Comandos úteis:"
echo "  • Reiniciar app: sudo supervisorctl restart programaequilibrio"
echo "  • Ver logs: sudo tail -f /var/log/supervisor/programaequilibrio.log"
echo "  • Status: sudo supervisorctl status"
echo ""
print_success "Sistema está pronto para uso! 🚀"
