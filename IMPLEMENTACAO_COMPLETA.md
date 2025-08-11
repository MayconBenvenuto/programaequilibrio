# Programa Equilíbrio - Sistema de Diagnóstico Corporativo

## 📋 Visão Geral

O Sistema de Diagnóstico Corporativo do Programa Equilíbrio é uma aplicação web desenvolvida para a Belz Conecta Saúde que permite:

- ✅ **Validação de CNPJ** com consulta automática à Receita Federal
- ✅ **Campo WhatsApp** para contato direto
- ✅ **Banco de dados Supabase** para armazenamento seguro
- ✅ **Painel administrativo** para visualização de relatórios
- ✅ **Prevenção de fraudes** através de validação de dados empresariais

## 🚀 Funcionalidades Implementadas

### 1. Validação de CNPJ e Dados Empresariais

- Validação de formato usando `validate-docbr`
- Consulta automática na API ReceitaWS
- Verificação de situação da empresa (apenas empresas ativas)
- Preenchimento automático de dados cadastrais

### 2. Formulário Aprimorado

- Campo obrigatório para WhatsApp
- Validação em tempo real
- Máscaras para campos de entrada
- Interface responsiva e intuitiva

### 3. Banco de Dados Supabase

- Estrutura completa de tabelas
- Relacionamentos otimizados
- Views para relatórios
- Triggers automáticos
- Políticas de segurança (RLS)

### 4. Painel Administrativo

- Dashboard com estatísticas em tempo real
- Listagem de empresas cadastradas
- Filtros e busca avançada
- Visualização de diagnósticos
- Gráficos interativos

## 🛠 Configuração do Ambiente

### 1. Instalação de Dependências

```bash
# Instalar dependências Python
pip install -r requirements.txt
```

### 2. Configuração do Supabase

1. Acesse [supabase.com](https://supabase.com) e crie uma conta
2. Crie um novo projeto
3. Execute o script SQL fornecido (`database_structure.sql`) no SQL Editor do Supabase
4. Obtenha sua URL e chave pública do projeto

### 3. Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```bash
# Configurações do Supabase
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_publica_do_supabase

# Chave secreta do Flask
FLASK_SECRET_KEY=sua_chave_secreta_muito_segura

# API do ReceitaWS (já configurada)
RECEITAWS_API_URL=https://www.receitaws.com.br/v1/cnpj/
```

### 4. Executar o Sistema

```bash
# Desenvolvimento local
python main.py

# Produção (Vercel)
# O sistema já está configurado para deploy automático
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais

1. **empresas**
   - Dados cadastrais das empresas
   - Informações de contato (incluindo WhatsApp)
   - Dados obtidos da Receita Federal

2. **diagnosticos**
   - Respostas dos questionários
   - Análises geradas
   - Níveis de risco
   - Ações recomendadas

3. **admin_users**
   - Usuários do painel administrativo
   - Controle de acesso e permissões

### Views e Funções

- `vw_diagnosticos_completos`: Join completo para relatórios
- `vw_estatisticas_admin`: Estatísticas para dashboard
- `buscar_empresa_por_cnpj()`: Função de busca otimizada

## 🔐 Sistema de Administração

### Acesso Padrão

- **URL**: `/admin/login`
- **Usuário**: `admin`
- **Senha**: `admin123`

### Funcionalidades Administrativas

1. **Dashboard**
   - Total de empresas atendidas
   - Diagnósticos realizados
   - Colaboradores analisados
   - Distribuição por nível de risco

2. **Gestão de Empresas**
   - Lista completa de empresas
   - Busca por razão social, CNPJ ou responsável
   - Visualização de contatos (email e WhatsApp)
   - Exportação de relatórios

## 🛡️ Segurança e Prevenção de Fraudes

### Validações Implementadas

1. **CNPJ**
   - Validação de dígitos verificadores
   - Consulta na Receita Federal
   - Verificação de situação da empresa

2. **Dados Empresariais**
   - Cross-check com dados oficiais
   - Detecção de inconsistências
   - Histórico de modificações

3. **Controle de Acesso**
   - Sistema de autenticação seguro
   - Sessões com timeout
   - Logs de atividades administrativas

## 📊 Fluxo de Uso

### Para Empresas

1. Acesso ao questionário
2. Inserção e validação do CNPJ
3. Preenchimento automático dos dados
4. Completar informações obrigatórias (WhatsApp, etc.)
5. Responder ao questionário
6. Receber diagnóstico e PDF

### Para Administradores

1. Login no painel administrativo
2. Visualizar dashboard com estatísticas
3. Gerenciar empresas cadastradas
4. Acompanhar diagnósticos realizados
5. Exportar relatórios

## 🔧 Manutenção e Suporte

### Logs e Monitoramento

- Logs de validação de CNPJ
- Histórico de diagnósticos
- Métricas de uso do sistema
- Alertas de tentativas de fraude

### Backup e Recuperação

- Backup automático no Supabase
- Exportação periódica de dados
- Plano de recuperação de desastres

### Atualizações

- Sistema versionado
- Deploy automatizado via Vercel
- Rollback automático em caso de falhas

## 🎯 Próximos Passos

### Melhorias Sugeridas

1. **Relatórios Avançados**
   - Dashboards personalizáveis
   - Exportação em múltiplos formatos
   - Análises preditivas

2. **Integração WhatsApp**
   - Envio automático de resultados
   - Notificações de acompanhamento
   - Chat bot para suporte

3. **API Externa**
   - Endpoints para integrações
   - Webhook para notificações
   - SDK para desenvolvedores

4. **Mobile App**
   - Aplicativo nativo
   - Sincronização offline
   - Notificações push

## 📞 Contato e Suporte

- **Email**: <admin@belzconectasaude.com.br>
- **Desenvolvedor**: Maycon Benvenuto
- **Sistema**: Programa Equilíbrio - Belz Conecta Saúde

---

**⚠️ IMPORTANTE**:

- Altere a senha padrão do admin em produção
- Configure corretamente as variáveis de ambiente
- Execute o script SQL no Supabase antes do primeiro uso
- Mantenha backups regulares dos dados
