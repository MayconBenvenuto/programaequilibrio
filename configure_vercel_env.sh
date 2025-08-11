#!/bin/bash
# ========================================
# CONFIGURAÇÃO DE VARIÁVEIS DE AMBIENTE VIA VERCEL CLI
# ========================================

echo "🚀 Configurando variáveis de ambiente no Vercel..."
echo "📋 Total de variáveis: 12"
echo ""

# VARIÁVEIS ESSENCIAIS DA APLICAÇÃO
echo "⚙️ Configurando variáveis da aplicação..."
vercel env add FLASK_ENV "production"
vercel env add DEBUG "false"
vercel env add FLASK_SECRET_KEY "ProgramaEquilibrio2025!@#$%SuperSecretKey789XYZ"

# CONFIGURAÇÕES DO BANCO SUPABASE (CRÍTICAS!)
echo "🗄️ Configurando banco Supabase..."
vercel env add SUPABASE_URL "https://xzjbnohtfuppilpzvvqy.supabase.co"
vercel env add SUPABASE_ANON_KEY "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6amJub2h0ZnVwcGlscHp2dnF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ5MjUzOTgsImV4cCI6MjA3MDUwMTM5OH0.qXDZrGjacFYOOdQcftzBj1Zkutt3jTIf-tjGFsb3Za8"

# CONFIGURAÇÕES DE ADMINISTRAÇÃO
echo "👤 Configurando administração..."
vercel env add ADMIN_EMAIL "admin@conecta.com"
vercel env add ADMIN_PASSWORD "Admin123!Conecta"
vercel env add ADMIN_NAME "Administrador Sistema"

# APIs EXTERNAS
echo "🌐 Configurando APIs externas..."
vercel env add RECEITAWS_API_URL "https://www.receitaws.com.br/v1/cnpj/"
vercel env add VIACEP_API_URL "https://viacep.com.br/ws/"

# CONFIGURAÇÕES DE SEGURANÇA
echo "🔒 Configurando segurança..."
vercel env add SESSION_COOKIE_SECURE "true"
vercel env add SESSION_COOKIE_HTTPONLY "true"
vercel env add PERMANENT_SESSION_LIFETIME "3600"

echo ""
echo "✅ Configuração concluída!"
echo "🚀 Execute agora: vercel --prod"
echo "📊 Para verificar: vercel env ls"
