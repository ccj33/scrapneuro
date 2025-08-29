#!/usr/bin/env python3
"""
🧪 SCRIPT DE TESTE DO ENVIO SEMANAL
Testa o sistema de envio semanal sem verificar data/hora

Uso: python teste_semanal.py
"""

import datetime
import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar as funções do scraper principal
from fapemig_scraper import (
    scrape_fapemig_completo,
    scrape_cnpq_completo,
    scrape_ufmg_editais,
    filtrar_ufmg_2025,
    salvar_resultados,
    enviar_email,
    criar_corpo_email_semanal_completo
)

def main():
    """Função principal do teste semanal"""
    print("🧪 TESTE DO SISTEMA DE ENVIO SEMANAL")
    print("=" * 50)

    # 📅 Data atual (forçada para teste)
    agora = datetime.datetime.now()

    print("📅 Data do teste:", agora.strftime('%d/%m/%Y %H:%M:%S'))

    # 📧 DESTINATÁRIOS SEMANAIS (para teste)
    DESTINATARIOS_SEMANAIS = [
        "mirelle_celiane@hotmail.com",
        "clevioferreira@gmail.com",
        "gustavo.augustoprs@gmail.com",
        "laviniagudulaufmg@gmail.com"
    ]

    print(f"\n📧 Destinatários para teste: {len(DESTINATARIOS_SEMANAIS)} pessoas")
    for i, email in enumerate(DESTINATARIOS_SEMANAIS, 1):
        print(f"   {i}. {email}")

    print("
⚠️  ATENÇÃO: Este é um teste!"    print("📧 Os emails serão enviados REALMENTE para os destinatários!")
    resposta = input("\n❓ Deseja continuar com o teste? (s/N): ").lower().strip()

    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("❌ Teste cancelado pelo usuário.")
        return False

    print("\n🚀 INICIANDO TESTE DO ENVIO SEMANAL...")
    print("=" * 50)

    try:
        # 🔄 Executar scraping de todos os sites (versão reduzida para teste)
        print("\n🏛️  TESTANDO FAPEMIG...")
        editais_fapemig = scrape_fapemig_completo()

        print("\n🔬 TESTANDO CNPq...")
        editais_cnpq = scrape_cnpq_completo()

        print("\n🎓 TESTANDO UFMG...")
        editais_ufmg = scrape_ufmg_editais()

        # Filtrar apenas editais UFMG de 2025
        print(f"\n🔍 Antes do filtro: {len(editais_ufmg)} editais UFMG")
        editais_ufmg_2025 = filtrar_ufmg_2025(editais_ufmg)
        print(f"🎯 Filtrados {len(editais_ufmg_2025)} editais UFMG de 2025")

        # Combinar todos os editais
        todos_editais = editais_fapemig + editais_cnpq + editais_ufmg_2025

        print("
📊 RESUMO DOS EDITAIS ENCONTRADOS NO TESTE:"        print(f"   🏛️  FAPEMIG: {len(editais_fapemig)} editais")
        print(f"   🔬 CNPq: {len(editais_cnpq)} editais")
        print(f"   🎓 UFMG 2025: {len(editais_ufmg_2025)} editais")
        print(f"   📊 TOTAL: {len(todos_editais)} editais")

        # 💾 Salvar resultados em arquivos
        salvar_resultados(todos_editais)

        # 📧 Preparar email de teste
        assunto = f"🧪 TESTE - RELATÓRIO SEMANAL - FAPEMIG + CNPq + UFMG 2025 - {agora.strftime('%d/%m/%Y')}"

        if todos_editais:
            corpo_email = criar_corpo_email_semanal_completo(todos_editais, agora, editais_fapemig, editais_cnpq, editais_ufmg_2025)
        else:
            corpo_email = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h1>🧪 TESTE - RELATÓRIO SEMANAL</h1>
                <h2 style="color: #ff6b6b;">⚠️ TESTE DO SISTEMA</h2>
                <p><strong>Data do teste:</strong> {agora.strftime('%d/%m/%Y %H:%M')}</p>
                <p>Olá,</p>
                <p>Este é um <strong>TESTE</strong> do sistema de envio semanal automático.</p>
                <p>Não foram encontrados editais ativos nos sites monitorados.</p>
                <ul>
                    <li>🏛️ FAPEMIG: {len(editais_fapemig)} editais</li>
                    <li>🔬 CNPq: {len(editais_cnpq)} editais</li>
                    <li>🎓 UFMG 2025: {len(editais_ufmg_2025)} editais</li>
                </ul>
                <p>O sistema está funcionando corretamente! ✅</p>
                <br>
                <p>Atenciosamente,<br>Sistema Scrap Neuro - Teste</p>
            </body>
            </html>
            """

        # 📧 Enviar para TODOS os destinatários (teste real)
        print("
📧 ENVIANDO EMAILS DE TESTE..."        print("⚠️  ATENÇÃO: Emails serão enviados REALMENTE!")
        input("❓ Pressione ENTER para continuar com o envio...")

        sucessos = 0
        falhas = 0

        for i, destinatario in enumerate(DESTINATARIOS_SEMANAIS, 1):
            print(f"\n📧 [{i}/{len(DESTINATARIOS_SEMANAIS)}] Enviando TESTE para: {destinatario}")

            sucesso = enviar_email(destinatario, assunto, corpo_email)

            if sucesso:
                sucessos += 1
                print(f"   ✅ TESTE ENVIADO com sucesso!")
            else:
                falhas += 1
                print(f"   ❌ FALHA no teste!")

        # 📊 Resultado final do teste
        print("
📊 RESULTADO FINAL DO TESTE:"        print(f"   🧪 Tipo: Teste de Envio Semanal")
        print(f"   📅 Data: {agora.strftime('%d/%m/%Y %H:%M')}")
        print(f"   📧 Total de destinatários: {len(DESTINATARIOS_SEMANAIS)}")
        print(f"   ✅ Testes bem-sucedidos: {sucessos}")
        print(f"   ❌ Falhas: {falhas}")
        print(f"   📊 Taxa de sucesso: {(sucessos/len(DESTINATARIOS_SEMANAIS)*100):.1f}%")

        if sucessos == len(DESTINATARIOS_SEMANAIS):
            print("\n🎉 TESTE CONCLUÍDO COM 100% DE SUCESSO!")
            print("✅ Sistema de envio semanal está funcionando perfeitamente!")
            return True
        elif sucessos > 0:
            print(f"\n⚠️ TESTE CONCLUÍDO COM SUCESSO PARCIAL ({sucessos}/{len(DESTINATARIOS_SEMANAIS)})")
            return True
        else:
            print("\n❌ TODOS OS TESTES FALHARAM!")
            return False

    except Exception as e:
        print(f"\n❌ ERRO GERAL no teste semanal: {str(e)}")
        print(f"🔧 Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Iniciando teste do sistema de envio semanal...")
    sucesso = main()

    if sucesso:
        print("\n✅ Teste finalizado com sucesso!")
        sys.exit(0)
    else:
        print("\n❌ Teste finalizado com falhas!")
        sys.exit(1)
