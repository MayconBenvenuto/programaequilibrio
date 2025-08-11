# 🔐 CREDENCIAIS DE ACESSO ADMIN - PROGRAMA EQUILÍBRIO

## 📍 Como Acessar o Painel Administrativo

### 🌐 URLs de Acesso

**Local (Desenvolvimento):**
```
http://localhost:5000/admin/login
```

**Produção (Vercel):**
```
https://seu-site.vercel.app/admin/login
```

## 🔑 Credenciais de Login

### 💻 **Modo Local/Desenvolvimento:**

**Usuário:** `admin`  
**Senha:** `admin123`

**OU**

**Usuário:** `admin@conecta.com`  
**Senha:** `admin123`

### 🚀 **Sistema de Fallback (quando Supabase não está disponível):**

O sistema agora possui um **fallback automático** que permite login mesmo quando:
- ❌ Supabase está indisponível
- ❌ Problemas de conectividade com banco de dados
- ❌ Configuração incorreta do Supabase

**Credenciais de Fallback:**
1. **Usuário:** `admin` | **Senha:** `admin123`
2. **Usuário:** Valor da variável `ADMIN_EMAIL` | **Senha:** Valor da variável `ADMIN_PASSWORD`

## ⚙️ Configuração via Variáveis de Ambiente

Para personalizar as credenciais, defina no arquivo `.env`:

```env
# Credenciais do Administrador
ADMIN_EMAIL=seu-admin@empresa.com
ADMIN_PASSWORD=SuaSenhaSegura123!
ADMIN_NAME=Seu Nome Completo
ADMIN_SESSION_TIMEOUT=7200
```

## 🔧 Como Fazer Login

1. **Acesse a URL de login**
2. **Digite as credenciais:**
   - Campo "Usuário/Email": `admin` ou `admin@conecta.com`
   - Campo "Senha": `admin123`
3. **Clique em "Entrar"**

## 🎯 Funcionalidades Disponíveis Após o Login

### 📊 Dashboard Principal
- Estatísticas gerais do sistema
- Total de empresas cadastradas
- Total de diagnósticos realizados
- Gráficos e relatórios

### 🏢 Gestão de Empresas
- Lista todas as empresas cadastradas
- Busca por CNPJ, nome ou cidade
- Visualizar detalhes e histórico
- Exportar dados

### 📈 Relatórios
- Diagnósticos por período
- Análise de maturidade
- Exportação de dados

## 🚨 Solução de Problemas

### ❌ "Sistema de administração indisponível"

**Solução:** O sistema agora possui fallback automático. Se aparecer essa mensagem, use:
- **Usuário:** `admin`
- **Senha:** `admin123`

### ❌ "Credenciais inválidas"

**Verifique:**
- Username: `admin` (não `admin@conecta.com` se estiver no modo fallback)
- Senha: `admin123` (exata, case-sensitive)
- Não há espaços antes/depois

### ❌ "Erro no sistema de autenticação"

**Causa:** Problemas de conectividade com Supabase  
**Solução:** O sistema automaticamente usa fallback local

## 🔒 Segurança

⚠️ **ATENÇÃO:** 
- As credenciais padrão (`admin/admin123`) são para **desenvolvimento apenas**
- Em **produção**, sempre altere as credenciais via variáveis de ambiente
- Use senhas fortes e únicas
- Configure HTTPS em produção

## 📝 Logs de Debugging

O sistema agora inclui logs detalhados no console para ajudar no debugging:

```
✅ [ADMIN] Login bem-sucedido (fallback) - usuário: admin
❌ [ADMIN] Credenciais inválidas (fallback) - usuário: teste
🔍 [ADMIN] Tentando login com Supabase - usuário: admin
```

---

**Data de Atualização:** 11/08/2025  
**Versão:** 2.0 (Com sistema de fallback)  
**Status:** ✅ Funcionando com fallback automático
