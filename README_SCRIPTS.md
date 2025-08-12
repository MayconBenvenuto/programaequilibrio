# 🏢 Scripts de População do Banco de Dados

Este diretório contém scripts para popular o banco de dados com empresas fictícias para demonstração.

## 📋 Scripts Disponíveis

### 1. `popular_banco_demo.py` (Recomendado)
Script completo que cadastra 10 empresas fictícias diretamente no Supabase.

**Funcionalidades:**
- ✅ Cadastra 10 empresas com dados realistas
- ✅ Gera diagnósticos com níveis de risco variados
- ✅ Adiciona datas aleatórias para simular histórico
- ✅ Todos os nomes têm "(exemplo)" para identificação
- ✅ Relatório de sucesso/falha no final

### 2. `testar_populacao.py` (Teste Simples)
Script de teste que cadastra 1 empresa via API pública.

**Funcionalidades:**
- ✅ Testa a API de cadastro
- ✅ Mais rápido para validação
- ✅ Usa endpoint público

## 🚀 Como Executar

### Opção 1: Script Completo (Recomendado)

```bash
# No diretório raiz do projeto
cd "C:\Users\Maycon\OneDrive\Documentos\scripts\BELZ\programaequilibrio"

# Executar o script
python popular_banco_demo.py
```

**Pré-requisitos:**
- Variáveis de ambiente configuradas (SUPABASE_URL, SUPABASE_ANON_KEY)
- Dependências do projeto instaladas

### Opção 2: Teste Via API

```bash
# Executar teste simples
python testar_populacao.py
```

**Pré-requisitos:**
- Apenas requests instalado
- Aplicação rodando em produção

## 📊 Dados que Serão Criados

### Empresas Fictícias:
1. **TechNova Solutions Ltda (exemplo)** - Tecnologia (175 colaboradores)
2. **Indústria MetalMax S.A. (exemplo)** - Metalúrgica (750 colaboradores)
3. **ConsultPro Assessoria Empresarial Ltda (exemplo)** - Consultoria (75 colaboradores)
4. **EcoVerde Sustentabilidade Ltda (exemplo)** - Sustentabilidade (375 colaboradores)
5. **LogiTransporte Express Ltda (exemplo)** - Logística (175 colaboradores)
6. **CreativeAgency Publicidade Ltda (exemplo)** - Publicidade (75 colaboradores)
7. **HealthCare Plus Serviços Médicos Ltda (exemplo)** - Saúde (1500 colaboradores)
8. **EduFuturo Instituto de Ensino Ltda (exemplo)** - Educação (375 colaboradores)
9. **RetailShop Comércio e Varejo Ltda (exemplo)** - Varejo (175 colaboradores)
10. **FinanceMax Gestão Financeira S.A. (exemplo)** - Financeiro (750 colaboradores)

### Variação de Diagnósticos:
- 🟢 **Baixo Risco**: Empresas bem estruturadas
- 🟡 **Risco Moderado**: Empresas com alguns pontos de atenção
- 🔴 **Alto Risco**: Empresas que precisam de intervenção urgente
- 🔄 **Misto**: Combinações variadas

## 📈 Resultados Esperados

Após execução, você terá:
- ✅ **Dashboard populado** com estatísticas realistas
- ✅ **Gráficos funcionais** com dados reais
- ✅ **Lista de empresas** no painel admin
- ✅ **Histórico de diagnósticos** distribuído ao longo do tempo
- ✅ **Dados para demonstração** claramente identificados

## 🔍 Verificação

Após executar os scripts:

1. **Acesse o painel admin**: https://programaequilibrio.vercel.app/admin
2. **Verifique o dashboard**: Gráficos devem mostrar dados
3. **Lista de empresas**: Deve conter as empresas "(exemplo)"
4. **Teste o sistema**: Faça um diagnóstico real para comparar

## ⚠️ Observações Importantes

- 🏷️ **Identificação**: Todas as empresas têm "(exemplo)" no nome
- 🗑️ **Limpeza**: Para remover, filtre por empresas com "(exemplo)"
- 🔒 **Segurança**: CNPJs são fictícios e inválidos para uso real
- 📧 **E-mails**: Domínios de exemplo não existem
- 📞 **Contatos**: Telefones são fictícios

## 🛠️ Resolução de Problemas

### Erro de Conexão Supabase
```
❌ ERRO: Não foi possível conectar ao Supabase
```
**Solução**: Verifique as variáveis de ambiente `SUPABASE_URL` e `SUPABASE_ANON_KEY`

### Erro de Importação
```
❌ Erro ao importar dependências
```
**Solução**: Execute o script a partir do diretório raiz do projeto

### Falhas no Cadastro
```
❌ Falha ao cadastrar empresa
```
**Solução**: Verifique logs detalhados e conexão com banco

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs detalhados
2. Confirme conexão com Supabase
3. Teste primeiro com `testar_populacao.py`
4. Verifique se a aplicação está funcionando normalmente
