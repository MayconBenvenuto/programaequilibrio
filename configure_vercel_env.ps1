# ========================================
# CONFIGURAÇÃO DE VARIÁVEIS DE AMBIENTE VIA VERCEL CLI (PowerShell)
# ========================================

Write-Host "🚀 Configurando variáveis de ambiente no Vercel..." -ForegroundColor Green
Write-Host "📋 Total de variáveis: 12" -ForegroundColor Yellow
Write-Host ""

# Verificar se Vercel CLI está instalado
try {
    $vercelVersion = vercel --version
    Write-Host "✅ Vercel CLI encontrado: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI não encontrado!" -ForegroundColor Red
    Write-Host "💡 Instale com: npm i -g vercel" -ForegroundColor Yellow
    exit 1
}

# VARIÁVEIS ESSENCIAIS DA APLICAÇÃO
Write-Host "⚙️ Configurando variáveis da aplicação..." -ForegroundColor Cyan
vercel env add FLASK_ENV production
vercel env add DEBUG false
vercel env add FLASK_SECRET_KEY "ProgramaEquilibrio2025!@#$%SuperSecretKey789XYZ"

# CONFIGURAÇÕES DO BANCO SUPABASE (CRÍTICAS!)
Write-Host "🗄️ Configurando banco Supabase..." -ForegroundColor Cyan
vercel env add SUPABASE_URL "https://xzjbnohtfuppilpzvvqy.supabase.co"
vercel env add SUPABASE_ANON_KEY "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6amJub2h0ZnVwcGlscHp2dnF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ5MjUzOTgsImV4cCI6MjA3MDUwMTM5OH0.qXDZrGjacFYOOdQcftzBj1Zkutt3jTIf-tjGFsb3Za8"

# CONFIGURAÇÕES DE ADMINISTRAÇÃO
Write-Host "👤 Configurando administração..." -ForegroundColor Cyan
vercel env add ADMIN_EMAIL "admin@conecta.com"
vercel env add ADMIN_PASSWORD "Admin123!Conecta"
vercel env add ADMIN_NAME "Administrador Sistema"

# APIs EXTERNAS
Write-Host "🌐 Configurando APIs externas..." -ForegroundColor Cyan
vercel env add RECEITAWS_API_URL "https://www.receitaws.com.br/v1/cnpj/"
vercel env add VIACEP_API_URL "https://viacep.com.br/ws/"

# CONFIGURAÇÕES DE SEGURANÇA
Write-Host "🔒 Configurando segurança..." -ForegroundColor Cyan
vercel env add SESSION_COOKIE_SECURE true
vercel env add SESSION_COOKIE_HTTPONLY true
vercel env add PERMANENT_SESSION_LIFETIME 3600

Write-Host ""
Write-Host "✅ Configuração concluída!" -ForegroundColor Green
Write-Host "🚀 Execute agora: vercel --prod" -ForegroundColor Yellow
Write-Host "📊 Para verificar: vercel env ls" -ForegroundColor Yellow
