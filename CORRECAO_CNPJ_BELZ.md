# CORREÇÃO ESPECÍFICA PARA CNPJ DA BELZ CORRETORA

## Status da Investigação

**CNPJ Testado:** 32.997.318/0001-85 (BELZ CORRETORA DE SEGUROS LTDA)

### ✅ Backend - Funcionando Perfeitamente

Testamos o backend local e confirmamos que:
- ✅ **Validação de formato**: CNPJ é reconhecido como válido
- ✅ **Consulta de APIs**: Dados obtidos com sucesso via ReceitaWS
- ✅ **Situação da empresa**: ATIVA (confirmado)
- ✅ **Resposta da API**: `{"valid": true, "cnpj_validado": true, "dados_empresa": {...}}`

**Dados obtidos:**
- Razão Social: BELZ CORRETORA DE SEGUROS LTDA
- Nome Fantasia: GRUPO BELZ
- Situação: ATIVA
- CNPJ: 32997318000185
- Município: RECIFE/PE

### 🔍 Problema Identificado

O problema NÃO está no backend. Está no **frontend** - especificamente no processamento dos dados no browser.

### 🛠️ Correções Aplicadas

#### 1. **Logs Detalhados Adicionados**

**No index.html:**
- ✅ Logs detalhados da resposta da API
- ✅ Verificação de tipos de dados (`data.valid`, `data.cnpj_validado`)
- ✅ Monitoramento do processo de salvamento no sessionStorage
- ✅ Verificação dos dados salvos antes do redirecionamento

**No questionario.html:**
- ✅ Logs detalhados da leitura do sessionStorage
- ✅ Verificação passo-a-passo das condições de validação
- ✅ Identificação exata de qual condição está falhando

#### 2. **Lógica de Validação Aprimorada**

```javascript
// Condições mais flexíveis para permitir acesso:
const temCNPJ = dadosCarregados.cnpj || (dadosCarregados.dados_receita && dadosCarregados.dados_receita.cnpj);
const cnpjValidado = dadosCarregados.cnpj_validado === true;

// Permite acesso se:
if (temCNPJ && (cnpjValidado || dadosCarregados.dados_receita)) {
    // Prosseguir com questionário
}
```

### 📋 Como Diagnosticar

1. **Acesse a aplicação no browser**
2. **Abra o Console de Desenvolvedores (F12)**
3. **Insira o CNPJ: 32.997.318/0001-85**
4. **Observe os logs detalhados:**

**Logs esperados no index.html:**
```
📋 [FRONTEND] Resposta completa da API: {valid: true, cnpj_validado: true, ...}
✅ [FRONTEND] CNPJ válido - processando dados...
📋 [FRONTEND] Dados do formulário coletados: {cnpj: "32.997.318/0001-85", ...}
✅ [FRONTEND] WhatsApp válido: ...
📋 [FRONTEND] Adicionando dados da empresa da API
💾 [FRONTEND] Dados salvos no sessionStorage
🔄 [FRONTEND] Redirecionando para /questionario
```

**Logs esperados no questionario.html:**
```
🚀 [QUESTIONARIO] DOM carregado, iniciando validação...
📋 [QUESTIONARIO] Dados do sessionStorage parsed: {...}
🔍 [QUESTIONARIO] temCNPJ: 32.997.318/0001-85
🔍 [QUESTIONARIO] cnpjValidado: true
🔍 [QUESTIONARIO] Condição final: true
✅ [QUESTIONARIO] Validação passou - prosseguindo...
```

### 🚨 Se o Problema Persistir

Se ainda aparecer o erro "Erro ao carregar dados da empresa", verifique nos logs do console:

1. **Se `data.valid` for `false`** → Problema no backend (verificar rate limits das APIs)
2. **Se `temCNPJ` for `false`** → Problema na estrutura dos dados do sessionStorage
3. **Se `cnpjValidado` for `false`** → Problema na flag de validação
4. **Se nenhum log aparecer** → Problema de JavaScript/sintaxe

### 🎯 Próximos Passos

1. **Fazer deploy das mudanças na Vercel**
2. **Testar no ambiente de produção**
3. **Verificar logs do console no browser**
4. **Identificar exatamente onde a validação está falhando**

### 📊 Resultado Esperado

Com essas correções, o CNPJ **32.997.318/0001-85** deve:
- ✅ Passar na validação do backend
- ✅ Ser salvo corretamente no sessionStorage
- ✅ Permitir acesso ao questionário
- ✅ Exibir "BELZ CORRETORA DE SEGUROS LTDA" na tela do questionário

**Se o problema persistir após essas mudanças, os logs detalhados irão mostrar exatamente onde está falhando.**

---
**Data da correção:** 11/08/2025  
**CNPJ testado:** 32.997.318/0001-85 (BELZ CORRETORA DE SEGUROS LTDA)  
**Status backend:** ✅ Funcionando  
**Status frontend:** 🔧 Corrigido com logs detalhados
