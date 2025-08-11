## 🚀 CHECKLIST DEPLOY VERCEL - PROGRAMA EQUILÍBRIO

### ✅ ARQUIVOS VERIFICADOS E PRONTOS:

#### 📁 **Estrutura do Projeto:**
```
programaequilibrio/
├── api/
│   └── index.py ✅ (Configurado corretamente)
├── main.py ✅ (Aplicação principal funcionando)
├── vercel.json ✅ (Configuração correta)
├── requirements.txt ✅ (Todas dependências listadas)
├── templates/ ✅ (Templates HTML funcionando)
├── static/ ✅ (CSS, JS, imagens)
└── TESTES/ ✅ (100% dos testes passando)
```

#### 🔧 **CONFIGURAÇÕES NECESSÁRIAS:**

**1. Variáveis de Ambiente na Vercel:**
```
SUPABASE_URL=https://nkbqprwmrbzlhfcfqyth.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
RECEITAWS_API_URL=https://receitaws.com.br/v1/cnpj/
RECEITAWS_TIMEOUT=30
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
FLASK_SECRET_KEY=belz_conecta_programa_equilibrio_2024
DEBUG=False
FLASK_ENV=production
PYTHON_VERSION=3.9
```

**2. Configurações do Projeto Vercel:**
- **Framework:** Other
- **Build Command:** (deixar vazio)
- **Output Directory:** (deixar vazio)
- **Install Command:** pip install -r requirements.txt

### 📋 **PASSOS PARA CRIAR O PROJETO:**

1. **Acesse:** https://vercel.com/dashboard
2. **Clique:** "Add New..." → "Project"
3. **Selecione:** Import Git Repository
4. **Escolha:** MayconBenvenuto/programaequilibrio
5. **Configure:** 
   - Project Name: `programa-equilibrio`
   - Framework Preset: `Other`
   - Build and Output Settings: manter padrão
6. **Deploy:** Clique em "Deploy"

### ⚡ **APÓS O DEPLOY:**

1. **Configurar Variáveis de Ambiente:**
   - Settings → Environment Variables
   - Adicionar todas as variáveis listadas acima

2. **Testar URLs:**
   - `https://programa-equilibrio.vercel.app/` (Página inicial)
   - `https://programa-equilibrio.vercel.app/validar_cnpj` (API)
   - `https://programa-equilibrio.vercel.app/questionario` (Questionário)
   - `https://programa-equilibrio.vercel.app/admin/login` (Admin)

### 🔍 **DIFERENÇAS DA ÚLTIMA TENTATIVA:**
- ✅ Template questionário.html corrigido
- ✅ Todos os testes locais passando (100%)
- ✅ Estrutura api/index.py mantida
- ✅ vercel.json corrigido
- ✅ Projeto será recriado do zero (sem cache/problemas antigos)

### 🆘 **EM CASO DE PROBLEMAS:**
- Verificar logs: Vercel Dashboard → Functions → View Details
- Testar localmente primeiro: python main.py
- Verificar variáveis de ambiente na aba Settings

---
**Status:** ✅ PRONTO PARA DEPLOY
**Última validação:** 11/08/2025 15:14
**Testes locais:** 5/5 PASSANDO (100%)
