#!/usr/bin/env python3
"""
Teste rápido da nova implementação
"""

import sys
import os
import json

# Adiciona o diretório principal ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🧪 TESTE RÁPIDO - VALIDAÇÃO CNPJ COM MÚLTIPLAS APIs")
    print("=" * 55)
    
    try:
        from main import consultar_cnpj_com_fallback, validar_cnpj
        print("✅ Importações realizadas com sucesso")
        
        # Teste com CNPJ da Petrobras
        cnpj = "33000167000101"
        print(f"\n🔍 Testando CNPJ: {cnpj}")
        
        # Validar formato
        if not validar_cnpj(cnpj):
            print("❌ CNPJ inválido")
            return False
        
        print("✅ Formato válido")
        
        # Consultar dados
        dados = consultar_cnpj_com_fallback(cnpj)
        
        if dados and dados.get('razao_social'):
            print("🎉 SUCESSO!")
            print(f"   Empresa: {dados.get('razao_social')}")
            print(f"   Situação: {dados.get('situacao')}")
            print(f"   Cidade: {dados.get('endereco', {}).get('municipio')}")
            print(f"   Estado: {dados.get('endereco', {}).get('uf')}")
            print("\n✅ Sistema funcionando corretamente com múltiplas APIs!")
            return True
        else:
            print("❌ Não foi possível obter dados da empresa")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    sucesso = main()
    
    if sucesso:
        print("\n" + "="*55)
        print("🚀 PRONTO PARA USAR!")
        print("As melhorias foram implementadas com sucesso.")
        print("O erro 'Erro ao carregar dados da empresa' deve estar resolvido.")
        print("\n💡 Para aplicar em produção:")
        print("1. git add .")
        print("2. git commit -m 'feat: múltiplas APIs para validação CNPJ'")
        print("3. git push origin main")
    else:
        print("\n⚠️ PROBLEMAS ENCONTRADOS")
        print("Verifique os logs acima para mais informações.")
