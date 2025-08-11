# 🔓 REMOVER PROTEÇÃO DE AUTENTICAÇÃO - VERCEL

## 📋 **PASSO A PASSO - PAINEL WEB**

### **1. Acesse o Dashboard**
🌐 https://vercel.com/dashboard

### **2. Encontre o Projeto**
- Procure por `programaequilibrio` na lista de projetos
- Clique no nome do projeto

### **3. Vá para Settings**
- No menu lateral, clique em `Settings`
- Ou use a URL direta: https://vercel.com/mayconbenvenutos-projects/programaequilibrio/settings

### **4. Seção Security**
- No menu de Settings, clique em `Security`
- Ou vá direto: https://vercel.com/mayconbenvenutos-projects/programaequilibrio/settings/security

### **5. Desativar Proteções**
Procure e **DESATIVE** as seguintes opções (se estiverem ativadas):

#### **🔒 Password Protection**
- Se houver uma seção "Password Protection"
- Clique em `Remove` ou `Disable`

#### **🔐 Vercel Authentication**
- Procure por "Vercel Authentication" ou "SSO"
- Se estiver ON, clique para desativar (OFF)

#### **🌐 Domain Access**
- Verifique se não há restrições de domínio
- Se houver, remova as restrições

#### **👥 Team Access**
- Certifique-se que está configurado como "Public" ou "Anyone with link"
- Se estiver "Team only", mude para público

### **6. Salvar Alterações**
- Clique em `Save` ou `Update` se necessário
- Aguarde as alterações serem aplicadas

### **7. Aguardar Propagação**
- As mudanças podem levar alguns minutos para propagar
- Teste a URL após 2-3 minutos

---

## 🖥️ **MÉTODO 2: Via CLI Vercel**

### **Verificar Configurações Atuais**
```bash
vercel project ls
vercel inspect
```

### **Remover Proteções (se disponível)**
```bash
vercel project rm programaequilibrio
# Depois criar novo projeto
vercel --prod
```

---

## 🧪 **MÉTODO 3: Criar Novo Projeto Limpo**

Se as configurações não puderem ser alteradas:

### **1. Deletar Projeto Atual**
```bash
vercel project rm programaequilibrio
```

### **2. Criar Novo Deploy**
```bash
vercel --prod
```

### **3. Escolher Configurações Públicas**
- Quando perguntado sobre configurações
- Escolha sempre as opções públicas/abertas

---

## ✅ **COMO VERIFICAR SE FUNCIONOU**

Após fazer as alterações, teste:

```bash
# Testar via curl (se disponível)
curl -I https://programaequilibrio.vercel.app

# Ou usar Python
python -c "import requests; r=requests.get('https://programaequilibrio.vercel.app'); print(r.status_code)"
```

**Status esperado:** 200 (em vez de 401)

---

## 🎯 **OBSERVAÇÕES IMPORTANTES**

1. **Localização mais comum:** Settings > Security
2. **Nomes alternativos:** "Access Control", "Privacy", "Authentication"
3. **Tempo de propagação:** 2-5 minutos
4. **Teste múltiplas URLs:** Às vezes só uma URL específica é liberada

---

## 🆘 **SE NÃO ENCONTRAR AS CONFIGURAÇÕES**

Envie um screenshot da tela de Settings do seu projeto e eu te ajudo a localizar exatamente onde estão as configurações de segurança!
