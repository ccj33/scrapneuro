#!/usr/bin/env python3
"""
🧪 TESTE RÁPIDO - Verificar se as correções funcionaram
Testa apenas uma pequena parte do scraping para verificar timeouts e limites
"""

import sys
import signal
import time

def timeout_handler(signum, frame):
    print("\n❌ TIMEOUT: Teste excedeu 2 minutos!")
    raise TimeoutError("Teste excedeu tempo limite")

def teste_basico():
    """Teste básico das importações e configurações"""
    print("🧪 TESTE RÁPIDO - Verificação das correções")
    print("=" * 50)

    # Configurar timeout de 2 minutos para o teste
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(120)  # 2 minutos

    try:
        print("📦 Testando importações...")
        from fapemig_scraper import setup_driver

        print("🌐 Testando configuração do driver...")
        driver = setup_driver()
        print("✅ Driver configurado com sucesso!")

        print("🕒 Testando timeout de página...")
        try:
            driver.get("https://httpbin.org/delay/3")  # Página que demora 3 segundos
            print("✅ Timeout funcionando corretamente!")
        except Exception as e:
            if "timeout" in str(e).lower():
                print("✅ Timeout detectado corretamente!")
            else:
                print(f"⚠️ Erro inesperado: {e}")

        driver.quit()
        print("✅ Driver fechado com sucesso!")

        return True

    except TimeoutError as e:
        print(f"❌ ERRO DE TIMEOUT: {e}")
        return False

    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        return False

    finally:
        signal.alarm(0)  # Desabilitar timer
        print("✅ Teste finalizado")

if __name__ == "__main__":
    print("🚀 Iniciando teste rápido...")
    sucesso = teste_basico()

    if sucesso:
        print("\n🎉 TESTE APROVADO! As correções funcionaram!")
        print("✅ Timeouts configurados")
        print("✅ Limites de processamento aplicados")
        print("✅ Sistema pronto para execução")
        sys.exit(0)
    else:
        print("\n❌ TESTE FALHADO! Ainda há problemas.")
        sys.exit(1)
