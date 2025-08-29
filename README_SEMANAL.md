# 📧 Sistema de Envio Semanal Automático

## 🎯 Visão Geral

Este sistema foi configurado para enviar **automaticamente** relatórios semanais de editais para 4 destinatários específicos, toda **segunda-feira às 5:00 da manhã**.

### 👥 Destinatários

Os relatórios semanais são enviados para:

1. **mirelle_celiane@hotmail.com**
2. **clevioferreira@gmail.com**
3. **gustavo.augustoprs@gmail.com**
4. **laviniagudulaufmg@gmail.com**

## 🕐 Agendamento Automático

- **Frequência**: Toda segunda-feira
- **Horário**: 5:00 da manhã (BRT)
- **Timezone**: UTC-3 (Horário de Brasília)
- **Execução**: Automática via GitHub Actions

## 📊 Conteúdo dos Relatórios

Cada relatório semanal contém:

- 🏛️ **Editais FAPEMIG** (Fundação de Amparo à Pesquisa de Minas Gerais)
- 🔬 **Editais CNPq** (Conselho Nacional de Desenvolvimento Científico)
- 🎓 **Editais UFMG 2025** (Universidade Federal de Minas Gerais - apenas 2025)
- 📈 Estatísticas consolidadas
- 🔗 Links diretos para todos os editais

## 🚀 Como Funciona

### 1. Automação GitHub Actions

O arquivo `.github/workflows/envio-semanal.yml` contém:

```yaml
name: 📧 Envio Semanal de Editais - Segunda-feira 5h
on:
  schedule:
    - cron: '0 8 * * 1'    # Toda segunda-feira às 8:00 UTC (5:00 BRT)
```

### 2. Script de Envio (`envio_semanal.py`)

Script dedicado que:
- ✅ Verifica se é segunda-feira
- ✅ Executa scraping de todos os sites
- ✅ Gera relatório semanal
- ✅ Envia para todos os destinatários
- ✅ Registra logs detalhados

### 3. Configuração de Email

**IMPORTANTE**: Configure as credenciais no GitHub Secrets:

1. Vá para o repositório no GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Adicione:
   - `EMAIL_USER`: seu_email@gmail.com
   - `EMAIL_PASSWORD`: senha_app_gerada

## 🧪 Teste do Sistema

Para testar o sistema sem aguardar segunda-feira:

```bash
python teste_semanal.py
```

⚠️ **ATENÇÃO**: O teste enviará emails reais para todos os destinatários!

## 📁 Arquivos do Sistema

```
scrapneuro/
├── fapemig_scraper.py      # Script principal (modificado)
├── envio_semanal.py        # Script de envio semanal
├── teste_semanal.py        # Script de teste
├── requirements.txt        # Dependências atualizadas
├── .github/
│   └── workflows/
│       ├── email-reports.yml       # Workflow diário (existente)
│       └── envio-semanal.yml       # NOVO: Workflow semanal
└── README_SEMANAL.md       # Este arquivo
```

## 🔧 Configuração Inicial

### 1. Credenciais de Email

```bash
# Para Gmail (exemplo):
# 1. Ative verificação em 2 etapas
# 2. Gere senha de aplicativo em:
#    https://myaccount.google.com/apppasswords
# 3. Use a senha gerada no EMAIL_PASSWORD
```

### 2. Dependências

```bash
pip install -r requirements.txt
```

### 3. Teste Local

```bash
# Teste completo do sistema
python teste_semanal.py

# Ou apenas scraping sem envio
python fapemig_scraper.py
```

## 📊 Monitoramento

### Logs no GitHub Actions

1. Vá para a aba **Actions** do repositório
2. Clique no workflow **📧 Envio Semanal de Editais**
3. Veja os logs de execução
4. Status: ✅ Success ou ❌ Failure

### Arquivos Gerados

Após cada execução, são criados:
- `editais_scraping.json` - Dados estruturados
- `editais_scraping.csv` - Planilha para Excel

## 🚨 Solução de Problemas

### Email não está sendo enviado

1. **Verifique credenciais** no GitHub Secrets
2. **Confirme senha do aplicativo** (não senha normal)
3. **Verifique logs** do GitHub Actions

### Scraping falhando

1. **Sites podem estar temporariamente indisponíveis**
2. **Estrutura HTML pode ter mudado**
3. **Verifique logs** para detalhes específicos

### Execução manual

Para executar manualmente (sem aguardar segunda-feira):

1. Vá para **Actions** no GitHub
2. Selecione **📧 Envio Semanal de Editais**
3. Clique **Run workflow**

## 🎯 Status Atual

✅ **Sistema configurado e pronto**
- Destinatários atualizados
- Workflow semanal criado
- Scripts de automação prontos
- Teste implementado

📅 **Próximo envio**: Toda segunda-feira às 5:00

---

## 📞 Suporte

Em caso de dúvidas ou problemas:
1. Verifique os logs no GitHub Actions
2. Execute o teste local: `python teste_semanal.py`
3. Verifique credenciais de email

**Sistema Scrap Neuro - Envio Semanal Automático** 🤖✨
