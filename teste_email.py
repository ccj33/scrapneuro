# 🚀 TESTE DE CONFIGURAÇÃO DE EMAIL
# Script simples para testar se as configurações de email estão funcionando

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def testar_email():
    """Testa a configuração de email do GitHub Secrets"""

    print("🧪 INICIANDO TESTE DE CONFIGURAÇÃO DE EMAIL")
    print("=" * 50)

    # ⚠️ CONFIGURAÇÃO (do GitHub Secrets)
    EMAIL_REMETENTE = os.environ.get("EMAIL_USER", "seu_email@gmail.com")
    SENHA_EMAIL = os.environ.get("EMAIL_PASSWORD", "sua_senha_app")
    SMTP_SERVIDOR = "smtp.gmail.com"
    SMTP_PORTA = 587

    print("🔍 VERIFICANDO VARIÁVEIS DE AMBIENTE:")
    print(f"   EMAIL_USER definido: {'✅ Sim' if os.environ.get('EMAIL_USER') else '❌ Não'}")
    print(f"   EMAIL_PASSWORD definido: {'✅ Sim' if os.environ.get('EMAIL_PASSWORD') else '❌ Não'}")
    print()

    print("📧 CONFIGURAÇÕES ATUAIS:")
    print(f"   Remetente: {EMAIL_REMETENTE}")
    print(f"   Servidor: {SMTP_SERVIDOR}:{SMTP_PORTA}")
    print(f"   Senha definida: {'✅ Sim' if SENHA_EMAIL != 'sua_senha_app' else '❌ Não'}")
    print()

    # Verificar se as credenciais estão configuradas
    if EMAIL_REMETENTE == "seu_email@gmail.com" or SENHA_EMAIL == "sua_senha_app":
        print("❌ ERRO: Credenciais de email não configuradas!")
        print()
        print("🔧 COMO CONFIGURAR NO GITHUB:")
        print("   1. Acesse seu repositório no GitHub")
        print("   2. Vá em: Settings > Secrets and variables > Actions")
        print("   3. Clique em: New repository secret")
        print("   4. Adicione EMAIL_USER com seu email do Gmail")
        print("   5. Adicione EMAIL_PASSWORD com sua senha de aplicativo")
        print()
        print("📝 NOTA SOBRE SENHA DO GMAIL:")
        print("   - Ative a verificação em 2 etapas no Gmail")
        print("   - Gere uma senha de aplicativo em:")
        print("     https://myaccount.google.com/apppasswords")
        print("   - Use essa senha (16 caracteres) no EMAIL_PASSWORD")
        return False

    # 📧 EMAIL DE TESTE
    destinatario = EMAIL_REMETENTE  # Enviar para si mesmo
    assunto = "🧪 TESTE - Scrap Neuro Email Configuration"
    corpo = """
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1>✅ Configuração de Email Funcionando!</h1>
        <p>Este é um email de teste automático do sistema Scrap Neuro.</p>
        <p>Se você recebeu este email, significa que:</p>
        <ul>
            <li>✅ As credenciais estão corretas</li>
            <li>✅ O servidor SMTP está funcionando</li>
            <li>✅ O sistema de email está operacional</li>
        </ul>
        <p><strong>Data do teste:</strong> {}</p>
        <hr>
        <p style="color: #666; font-size: 12px;">
            Sistema: Scrap Neuro - Multi-site scraping<br>
            Este é um email automático de teste.
        </p>
    </body>
    </html>
    """.format(os.environ.get('GITHUB_RUN_NUMBER', 'Local Test'))

    print("📧 ENVIANDO EMAIL DE TESTE...")
    print(f"   Para: {destinatario}")
    print(f"   Assunto: {assunto}")

    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'html'))

        print("🔗 Conectando ao servidor SMTP...")
        servidor = smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA)
        servidor.starttls()

        print("🔐 Fazendo login...")
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)

        print("📤 Enviando email...")
        servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        servidor.quit()

        print("✅ EMAIL DE TESTE ENVIADO COM SUCESSO!")
        print(f"   📧 Verifique sua caixa de entrada: {destinatario}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ ERRO DE AUTENTICAÇÃO: {str(e)}")
        print("🔧 Verifique:")
        print("   - Se a senha de aplicativo está correta")
        print("   - Se a verificação em 2 etapas está ativa")
        print("   - Se você gerou uma nova senha de aplicativo")

    except smtplib.SMTPConnectError as e:
        print(f"❌ ERRO DE CONEXÃO: {str(e)}")
        print("🔧 Verifique sua conexão com a internet")

    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
        print(f"   Tipo: {type(e).__name__}")

    return False

if __name__ == "__main__":
    print("🚀 SCRAP NEURO - TESTE DE EMAIL")
    print("=" * 50)
    sucesso = testar_email()

    if sucesso:
        print("\n🎉 Configuração de email está funcionando perfeitamente!")
        print("💡 Agora você pode usar o sistema de relatórios automático.")
    else:
        print("\n❌ Configuração de email precisa ser corrigida.")
        print("🔄 Execute novamente após configurar as credenciais.")

    print("=" * 50)</contents>
</xai:function_call">Write file created: teste_email.py
</xai:function_call name="search_replace">
<parameter name="file_path">requirements.txt
