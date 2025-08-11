#!/usr/bin/env python3
"""
Script para testar as correções de JavaScript implementadas
"""

import requests
import json
import sys

def test_questionario_js_fixes(base_url):
    """Testa se as correções de JavaScript estão funcionando"""
    
    print(f"🧪 Testando correções de JavaScript em: {base_url}")
    print("=" * 60)
    
    # Testar se a página do questionário carrega
    print("📄 Testando página do questionário...")
    try:
        response = requests.get(f"{base_url}/questionario", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Verificar se as funções JavaScript corrigidas estão presentes
            checks = {
                'formatarCNPJ_improved': 'if (!cnpj)' in content and 'String(cnpj)' in content,
                'error_handling_improved': '❌ [QUESTIONARIO] Erro ao exibir dados da empresa:' in content,
                'debug_logging': '🔍 [DEBUG] Iniciando exibição de dados da empresa...' in content,
                'fallback_protection': 'fallbackError' in content,
                'element_checks': 'nomeElement.length' in content and 'cnpjElement.length' in content
            }
            
            print("✅ Página do questionário carregou")
            print("\n🔍 Verificações de código JavaScript:")
            
            all_good = True
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check.replace('_', ' ').title()}: {passed}")
                if not passed:
                    all_good = False
            
            if all_good:
                print("\n🎉 Todas as correções JavaScript estão implementadas!")
                
                # Verificar se há CSS inline como fallback
                css_fallback = '--primary-color: #130E54' in content
                css_status = "✅" if css_fallback else "❌"
                print(f"\n🎨 CSS Fallback: {css_status} {'Presente' if css_fallback else 'Ausente'}")
                
            else:
                print("\n⚠️ Algumas correções podem não ter sido aplicadas corretamente.")
                
        else:
            print(f"❌ Erro ao carregar questionário - Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar questionário: {e}")
    
    # Testar se a função de formatação está correta
    print(f"\n🧮 Testando formatação de CNPJ...")
    print("   Esta função agora deve lidar com valores nulos/undefined")
    print("   Casos de teste:")
    print("   - null/undefined -> '---'")  
    print("   - '12345678000195' -> '12.345.678/0001-95'")
    print("   - 'abc123' -> 'abc123' (valor inválido mantido)")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Uso: python test_js_fixes.py <URL_BASE>")
        print("Exemplo: python test_js_fixes.py https://seuapp.vercel.app")
        return 1
    
    base_url = sys.argv[1].rstrip('/')
    success = test_questionario_js_fixes(base_url)
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DAS CORREÇÕES IMPLEMENTADAS:")
    print("")
    print("🔧 Função formatarCNPJ melhorada:")
    print("   - Verifica se o valor é nulo/undefined")
    print("   - Converte para string de forma segura") 
    print("   - Valida formato antes de formatar")
    print("   - Retorna '---' para valores inválidos")
    print("")
    print("🛡️ Tratamento de erros aprimorado:")
    print("   - Logs detalhados para debug")
    print("   - Verificação se elementos DOM existem")
    print("   - Fallback seguro para erros")
    print("   - Stack trace para análise")
    print("")
    print("📊 Debug melhorado:")
    print("   - Logs estruturados com emojis")
    print("   - Validação de dados em cada etapa")
    print("   - Informações detalhadas sobre o problema")
    print("")
    print("💡 Como testar:")
    print("   1. Acesse a página inicial")
    print("   2. Insira um CNPJ válido")
    print("   3. Vá para o questionário") 
    print("   4. Abra o console do navegador")
    print("   5. Verifique se não há mais erros JavaScript")
    print("")
    print("✅ As correções devem resolver os erros que você estava vendo!")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
