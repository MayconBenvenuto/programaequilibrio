# 🧪 Testes do Sistema - Programa Equilíbrio

## 📋 Guia de Testes

Este diretório contém scripts para testar todas as funcionalidades do sistema.

## 🔧 Como Executar os Testes

### 1. Teste de Conexão Básica

```bash
python teste_conexao.py
```

### 2. Teste de Validação de CNPJ

```bash
python teste_cnpj.py
```

### 3. Teste do Banco Supabase

```bash
python teste_supabase.py
```

### 4. Teste das APIs Externas

```bash
python teste_apis.py
```

### 5. Teste Completo do Sistema

```bash
python teste_completo.py
```

## 🎯 CNPJs para Teste

### CNPJs Válidos (Empresas Reais)

- **11.222.333/0001-81** - Magazine Luiza S.A.
- **07.526.557/0001-00** - Natura Cosméticos S.A.
- **33.000.167/0001-01** - Itaú Unibanco S.A.
- **02.558.157/0001-62** - Via Varejo S.A.

### CNPJs de Teste (Válidos mas Fictícios)

- **11.111.111/0001-11** - Para testes gerais
- **22.222.222/0001-22** - Para testes de erro
- **33.333.333/0001-33** - Para testes de validação

### CNPJs Inválidos (Para Teste de Erro)

- **12.345.678/0001-00** - Formato correto mas inválido
- **00.000.000/0000-00** - CNPJ zerado
- **123.456.789-10** - Formato incorreto

## 📊 Resultados Esperados

### ✅ Teste Bem-sucedido

- Status 200 para todas as rotas
- Validação de CNPJ funcionando
- Conexão com Supabase ativa
- API ReceitaWS respondendo

### ❌ Possíveis Problemas

- Status 500: Erro interno do servidor
- Timeout: APIs externas indisponíveis
- 404: Rotas não encontradas
- Erro de banco: Configuração Supabase incorreta

## 🚀 Próximos Passos

Após executar os testes:

1. Verifique os logs de erro
2. Configure as variáveis de ambiente se necessário
3. Teste o painel administrativo
4. Faça um diagnóstico completo de ponta a ponta
