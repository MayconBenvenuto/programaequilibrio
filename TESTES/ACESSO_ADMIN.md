# 🔐 Guia de Acesso ao Painel Administrativo

## 📍 Como Acessar o Painel Admin

### 1. URL de Acesso

```url
http://localhost:5000/admin/login
```

### 2. Credenciais Padrão

**Usuário:** `admin@conecta.com`  
**Senha:** `admin123`

⚠️ **IMPORTANTE:** Altere essas credenciais em produção!

## 🎯 Funcionalidades Disponíveis

### 📊 Dashboard Principal

- **URL:** `http://localhost:5000/admin/dashboard`
- **Funcionalidades:**
  - Estatísticas gerais do sistema
  - Total de empresas cadastradas
  - Total de diagnósticos realizados
  - Gráfico de diagnósticos por mês
  - Distribuição por nível de maturidade

### 🏢 Gestão de Empresas

- **URL:** `http://localhost:5000/admin/empresas`
- **Funcionalidades:**
  - Lista todas as empresas cadastradas
  - Busca por CNPJ, nome ou cidade
  - Visualizar detalhes completos da empresa
  - Ver histórico de diagnósticos
  - Exportar dados para Excel/CSV

### 👤 Gestão de Usuários Admin

- **URL:** `http://localhost:5000/admin/usuarios`
- **Funcionalidades:**
  - Criar novos administradores
  - Ativar/desativar usuários
  - Alterar permissões
  - Histórico de acessos

## 🔧 Como Criar Novos Administradores

### Opção 1: Via Interface Web

1. Faça login no painel admin
2. Acesse "Usuários" no menu
3. Clique em "Novo Administrador"
4. Preencha os dados e salve

### Opção 2: Via Banco de Dados (SQL)

```sql
INSERT INTO admin_users (email, senha_hash, nome, ativo, criado_em)
VALUES (
    'novo@admin.com',
    '$2b$12$hash_da_senha_aqui',
    'Nome do Admin',
    true,
    NOW()
);
```

### Opção 3: Via Script Python

```python
from werkzeug.security import generate_password_hash
from supabase import create_client

# Configure suas credenciais Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Dados do novo admin
email = "novo@admin.com"
senha = "nova_senha_segura"
nome = "Nome do Administrador"

# Hash da senha
senha_hash = generate_password_hash(senha)

# Inserir no banco
supabase.table('admin_users').insert({
    'email': email,
    'senha_hash': senha_hash,
    'nome': nome,
    'ativo': True
}).execute()
```

## 📈 Como Interpretar os Dados

### Níveis de Maturidade

- **🟢 Avançado (41-50 pontos):** Empresa com excelente gestão
- **🟡 Intermediário (26-40 pontos):** Empresa em desenvolvimento
- **🟠 Básico (11-25 pontos):** Empresa com gestão inicial
- **🔴 Crítico (0-10 pontos):** Empresa precisa de atenção urgente

### Métricas Importantes

- **Taxa de Conversão:** % de visitantes que completam o diagnóstico
- **Crescimento Mensal:** Comparação com mês anterior
- **Distribuição Regional:** Onde estão concentradas as empresas
- **Segmentação por Porte:** Micro, pequena, média, grande empresa

## 🔒 Segurança e Boas Práticas

### ✅ Recomendações de Segurança

1. **Altere a senha padrão imediatamente**
2. **Use senhas fortes (mín. 12 caracteres)**
3. **Ative autenticação em duas etapas (se disponível)**
4. **Faça logout sempre após o uso**
5. **Acesse apenas de redes confiáveis**

### 🚨 Monitoramento

- Verifique logs de acesso regularmente
- Monitore tentativas de login suspeitas
- Mantenha backup dos dados
- Atualize o sistema regularmente

## 🆘 Solução de Problemas

### ❌ "Credenciais Inválidas"

1. Verifique se o email está correto
2. Verifique se a senha está correta
3. Verifique se o usuário está ativo no banco
4. Limpe cache do navegador

### ❌ "Erro 500 - Erro Interno"

1. Verifique conexão com banco de dados
2. Verifique logs da aplicação
3. Verifique configurações do Supabase
4. Reinicie a aplicação

### ❌ "Página Não Encontrada"

1. Verifique se a aplicação está rodando
2. Verifique se a URL está correta
3. Verifique se as rotas admin estão configuradas

## 📞 Suporte

### 🔍 Logs de Debug

Para ativar logs detalhados, configure:

```python
app.config['DEBUG'] = True
```

### 📊 Monitoramento de Performance

- Monitore tempo de resposta das páginas
- Verifique uso de memória da aplicação
- Monitore conexões com banco de dados
- Acompanhe estatísticas de uso

### 💾 Backup de Dados

Recomendação: Backup diário automático

```sql
-- Comando para backup (PostgreSQL)
pg_dump -h seu_host -U seu_usuario -d programa_equilibrio > backup_$(date +%Y%m%d).sql
```

## 🚀 Próximos Passos

1. **Teste completo do sistema** - Execute todos os testes
2. **Configure domínio personalizado** - Para produção
3. **Configure SSL/HTTPS** - Segurança essencial
4. **Monitore logs** - Identifique problemas rapidamente
5. **Treine usuários** - Como usar o painel admin

---

**🎯 Sistema pronto para uso!** O painel administrativo está completamente funcional e seguro.
