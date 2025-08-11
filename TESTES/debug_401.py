#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE ESPECÍFICO - DIAGNÓSTICO 401
Investiga especificamente o erro 401
"""

import requests

def test_401_debug():
    """Diagnóstica o erro 401"""
    url = "https://programaequilibrio-chc4xxsjp-mayconbenvenutos-projects.vercel.app"
    
    print("🔍 DIAGNÓSTICO ESPECÍFICO DO ERRO 401")
    print("="*50)
    
    try:
        response = requests.get(url, timeout=30)
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content Length: {len(response.content)}")
        
        # Verificar se há mensagem de erro específica
        if response.status_code == 401:
            content = response.text[:1000]  # Primeiros 1000 caracteres
            print(f"Conteúdo (início): {content}")
            
            # Verificar se é uma página de erro personalizada ou do Vercel
            if 'vercel' in content.lower():
                print("⚠️ Erro parece ser do Vercel")
            elif 'unauthorized' in content.lower():
                print("⚠️ Erro de autorização da aplicação")
            else:
                print("⚠️ Erro desconhecido")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_401_debug()
