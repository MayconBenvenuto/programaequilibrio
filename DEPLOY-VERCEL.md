# 🚀 Deploy na Vercel - Guia Rápido

## Pré-requisitos
- Conta no GitHub (gratuita)
- Conta na Vercel (gratuita)
- Node.js instalado (para CLI - opcional)

## Método 1: Deploy via GitHub (Recomendado - Mais Fácil)

### 1. Criar repositório no GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/programa-equilibrio.git
git push -u origin main
```

### 2. Deploy na Vercel
1. Acesse https://vercel.com
2. Clique em "New Project"
3. Conecte com GitHub
4. Selecione seu repositório
5. Configure:
   - Framework: **Other**
   - Root Directory: **/** (padrão)
   - Build Command: **(deixe vazio)**
   - Output Directory: **(deixe vazio)**
6. Clique em "Deploy"

### 3. Pronto! 🎉
- URL será fornecida automaticamente
- Deploy automático a cada push no GitHub

## Método 2: Deploy via CLI

### 1. Instalar Vercel CLI
```bash
npm i -g vercel
```

### 2. Login e Deploy
```bash
vercel login
vercel
vercel --prod
```

## Arquivos Incluídos
- ✅ `vercel.json` - Configuração da Vercel
- ✅ `requirements.txt` - Dependências otimizadas
- ✅ `main.py` - Configurado para produção

## ⚠️ Possíveis Problemas

### Erro: "functions property cannot be used with builds"
Se aparecer este erro:
```
The `functions` property cannot be used in conjunction with the `builds` property
```
**Solução:** O `vercel.json` já foi corrigido para usar apenas `builds`.

### Erro: "No Python files found"
**Solução:** Certifique-se que `main.py` está na raiz do projeto.

### Erro: "Module not found"
**Solução:** Verifique se todas as dependências estão em `requirements.txt`.

## Suporte
- Documentação Vercel: https://vercel.com/docs
- Vercel + Python: https://vercel.com/docs/functions/serverless-functions/runtimes/python
