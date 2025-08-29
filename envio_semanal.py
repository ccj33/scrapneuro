#!/usr/bin/env python3
"""
🚀 SCRIPT DE ENVIO SEMANAL AUTOMÁTICO
Script específico para enviar relatórios semanais toda segunda-feira às 5h

Uso: python envio_semanal.py
"""

import datetime
import sys
import os

# Adicionar o diretório atual ao path para importar o módulo principal
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
    """Função principal do envio semanal"""
    print("🚀 ENVIO SEMANAL AUTOMÁTICO - SEGUNDA-FEIRA 5H")
    print("=" * 60)

    # 📅 Verificar data e hora atual
    agora = datetime.datetime.now()
    dia_semana = agora.weekday()  # 0 = segunda, 6 = domingo
    hora_atual = agora.hour

    print("📅 Data atual:", agora.strftime('%d/%m/%Y %H:%M:%S'))
    print(f"📅 Dia da semana: {dia_semana} (0=segunda, 6=domingo)")
    print(f"📅 Hora atual: {hora_atual}h")

    # 📧 DESTINATÁRIOS SEMANAIS (segunda-feira às 5h)
    DESTINATARIOS_SEMANAIS = [
        "mirelle_celiane@hotmail.com",
        "clevioferreira@gmail.com",
        "gustavo.augustoprs@gmail.com",
        "laviniagudulaufmg@gmail.com"
    ]

    print(f"\n📧 Destinatários semanais: {len(DESTINATARIOS_SEMANAIS)} pessoas")
    for i, email in enumerate(DESTINATARIOS_SEMANAIS, 1):
        print(f"   {i}. {email}")

    # 🔍 Verificar se é segunda-feira
    if dia_semana != 0:  # 0 = segunda-feira
        print(f"\n❌ HOJE NÃO É SEGUNDA-FEIRA (dia {dia_semana})")
        print("📅 Aguardando próxima segunda-feira...")
        return False

    # ⏰ Verificar se é aproximadamente 5 da manhã (com tolerância de 1 hora)
    if not (4 <= hora_atual <= 6):
        print(f"\n❌ NÃO É HORA DO ENVIO (hora {hora_atual})")
        print("⏰ O envio semanal acontece às 5:00 da manhã")
        return False

    print("\n✅ CONDIÇÕES ATENDIDAS - INICIANDO ENVIO SEMANAL...")
    print("=" * 60)

    try:
        # 🔄 Executar scraping de todos os sites
        print("\n🏛️  PROCESSANDO FAPEMIG...")
        editais_fapemig = scrape_fapemig_completo()

        print("\n🔬 PROCESSANDO CNPq...")
        editais_cnpq = scrape_cnpq_completo()

        print("\n🎓 PROCESSANDO UFMG...")
        editais_ufmg = scrape_ufmg_editais()

        # Filtrar apenas editais UFMG de 2025
        print(f"\n🔍 Antes do filtro: {len(editais_ufmg)} editais UFMG")
        editais_ufmg_2025 = filtrar_ufmg_2025(editais_ufmg)
        print(f"🎯 Filtrados {len(editais_ufmg_2025)} editais UFMG de 2025")

        # Combinar todos os editais
        todos_editais = editais_fapemig + editais_cnpq + editais_ufmg_2025

        print("\n📊 RESUMO DOS EDITAIS ENCONTRADOS:")
        print(f"   🏛️  FAPEMIG: {len(editais_fapemig)} editais")
        print(f"   🔬 CNPq: {len(editais_cnpq)} editais")
        print(f"   🎓 UFMG 2025: {len(editais_ufmg_2025)} editais")
        print(f"   📊 TOTAL: {len(todos_editais)} editais")

        if not todos_editais:
            print("\n❌ NENHUM EDITAL ENCONTRADO!")
            print("📧 Enviando notificação de ausência de editais...")

            assunto = f"📊 RELATÓRIO SEMANAL - SEM EDITAIS - {agora.strftime('%d/%m/%Y')}"
            corpo_sem_editais = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h1>📊 RELATÓRIO SEMANAL - SEM EDITAIS</h1>
                <p><strong>Data:</strong> {agora.strftime('%d/%m/%Y')}</p>
                <p>Olá,</p>
                <p>Não foram encontrados editais ativos nos sites monitorados nesta semana.</p>
                <ul>
                    <li>🏛️ FAPEMIG: {len(editais_fapemig)} editais</li>
                    <li>🔬 CNPq: {len(editais_cnpq)} editais</li>
                    <li>🎓 UFMG 2025: {len(editais_ufmg_2025)} editais</li>
                </ul>
                <p>O sistema continuará monitorando os sites para próximos editais.</p>
                <br>
                <p>Atenciosamente,<br>Sistema Scrap Neuro</p>
            </body>
            </html>
            """

            # Mesmo sem editais, enviar notificação
            for destinatario in DESTINATARIOS_SEMANAIS:
                enviar_email(destinatario, assunto, corpo_sem_editais)

            return True

        # 💾 Salvar resultados em arquivos
        salvar_resultados(todos_editais)

        # 📧 Preparar email semanal
        assunto = f"📊 RELATÓRIO SEMANAL - FAPEMIG + CNPq + UFMG 2025 - Semana {agora.strftime('%d/%m/%Y')}"
        corpo_email = criar_corpo_email_semanal_completo(todos_editais, agora, editais_fapemig, editais_cnpq, editais_ufmg_2025)

        # 📧 Enviar para todos os destinatários
        print("\n📧 ENVIANDO RELATÓRIOS SEMANAIS...")
        sucessos = 0
        falhas = 0

        for i, destinatario in enumerate(DESTINATARIOS_SEMANAIS, 1):
            print(f"\n📧 [{i}/{len(DESTINATARIOS_SEMANAIS)}] Enviando para: {destinatario}")

            sucesso = enviar_email(destinatario, assunto, corpo_email)

            if sucesso:
                sucessos += 1
                print(f"   ✅ ENVIADO com sucesso!")
            else:
                falhas += 1
                print(f"   ❌ FALHA no envio!")

        # 📊 Resultado final
        print("\n📊 RESULTADO FINAL DO ENVIO SEMANAL:")
        print(f"   📅 Data: {agora.strftime('%d/%m/%Y %H:%M')}")
        print(f"   📧 Total de destinatários: {len(DESTINATARIOS_SEMANAIS)}")
        print(f"   ✅ Envios bem-sucedidos: {sucessos}")
        print(f"   ❌ Falhas: {falhas}")
        print(f"   📊 Taxa de sucesso: {(sucessos/len(DESTINATARIOS_SEMANAIS)*100):.1f}%")

        if sucessos > 0:
            print("\n🎉 ENVIO SEMANAL CONCLUÍDO COM SUCESSO!")
            return True
        else:
            print("\n❌ TODOS OS ENVIOS FALHARAM!")
            return False

    except Exception as e:
        print(f"\n❌ ERRO GERAL no envio semanal: {str(e)}")
        print(f"🔧 Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando envio semanal automático...")
    sucesso = main()

    if sucesso:
        print("\n✅ Script de envio semanal finalizado com sucesso!")
        sys.exit(0)
    else:
        print("\n❌ Script de envio semanal finalizado com falhas!")
        sys.exit(1)
