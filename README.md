# 🚀 SISTEMA COMPLETO DE RELATÓRIOS AUTOMÁTICOS

Sistema avançado para **extrair editais de múltiplas fontes** e **enviar relatórios automáticos por email**!

## ⚡ **CARACTERÍSTICAS PRINCIPAIS:**

### 🔍 **SCRAPING INTELIGENTE:**
- ✅ **FAPEMIG** - Todos os editais com nomes completos
- ✅ **CNPq** - Todos os editais nacionais com descrições
- ✅ **UFMG** - Apenas editais de 2025 (filtrados automaticamente)
- ✅ **Modo invisível** (headless) - navegador não abre
- ✅ **Nomes completos** (não apenas códigos)
- ✅ **Datas específicas** de cada edital
- ✅ **Links diretos** para PDFs

### 📧 **AUTOMAÇÃO DE EMAILS:**
- ✅ **Email diário** - Todo dia 5 do mês às 5:00
- ✅ **Email semanal** - Toda segunda-feira às 5:00
- ✅ **Destinatários específicos** para cada tipo
- ✅ **Conteúdo personalizado** e profissional
- ✅ **GitHub Actions** - Automação completa

## 📦 **INSTALAÇÃO:**

```bash
pip install -r requirements.txt
```

## 🚀 **CONFIGURAÇÃO DO GITHUB ACTIONS:**

### **PASSO 1: Configurar Secrets no GitHub**

1. Vá no seu repositório GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret:**
   - **EMAIL_USER:** seu_email@gmail.com
   - **EMAIL_PASSWORD:** sua_senha_app_gmail

### **PASSO 2: Configurar Gmail**

1. **Ative verificação em 2 etapas** no Gmail
2. **Gere uma senha de app:**
   - https://support.google.com/accounts/answer/185833
   - Selecione "Mail" e "Windows Computer"
   - Copie a senha gerada (16 caracteres)

### **PASSO 3: Upload dos arquivos**

Faça upload de todos os arquivos para seu repositório GitHub:
- `fapemig_scraper.py`
- `requirements.txt`
- `.github/workflows/email-reports.yml`

## 📧 **COMO FUNCIONA:**

O sistema executa **automaticamente** todo dia 5 e toda segunda-feira:

### 📅 **RELATÓRIO DIÁRIO (Dia 5) - Para ccjota51@gmail.com:**
```
🚀 RELATÓRIO DIÁRIO COMPLETO
FAPEMIG + CNPq + UFMG 2025
📅 Data: 05/12/2024

📊 Resumo Geral do Dia
🏛️ FAPEMIG: 8 editais
🔬 CNPq: 6 editais
🎓 UFMG 2025: 8 editais
📊 TOTAL: 22 editais

[Lista completa de TODOS os editais com nomes completos]
```

### 📊 **RELATÓRIO SEMANAL (Segunda-feira) - Para clevioferreira@gmail.com:**
```
📊 RELATÓRIO SEMANAL COMPLETO
FAPEMIG + CNPq + UFMG 2025
Semana de 09/12/2024

🎯 RESUMO GERAL DA SEMANA
🏛️ FAPEMIG: 8 editais
🔬 CNPq: 6 editais
🎓 UFMG 2025: 8 editais
📊 TOTAL: 22 editais

[Lista completa organizada por fonte]
```

## 🎯 **RESULTADO FINAL:**

### 📋 **EDITAIS EXTRAÍDOS:**

#### 🏛️ **FAPEMIG (8 editais):**
- **CHAMADA FAPEMIG 011/2025 - DEEP TECH - INSERÇÃO NO MERCADO E TRAÇÃO COMERCIAL**
- **Chamada 016/2024 - Participação Coletiva em Eventos Técnicos no País - 3ª Entrada**
- **CHAMADA 005/2025 - ORGANIZAÇÃO DE EVENTOS DE CARÁTER TÉCNICO CIENTÍFICO - 2ª ENTRADA**
- **PORTARIA FAPEMIG 021/2024 - CADASTRAMENTO DAS FUNDAÇÕES DE APOIO - FA**
- E outros 4 editais com nomes completos...

#### 🔬 **CNPq (6 editais):**
- **Chamada CNPq/MMA/CONFAP/FAPs Nº 15/2025 - SinBiose** (com descrição completa)
- **MCTI/CNPq/DFG Nº 14/2025** (com descrição completa)
- **Chamada Pública MCTI/CNPq nº 16/2025** (com descrição completa)
- E outros 3 editais com nomes completos...

#### 🎓 **UFMG 2025 (8 editais):**
- **Edital PROEX nº 08/2025 – Programa de Apoio Integrado a Eventos – PAIE**
- **Edital Nº 1874/2025 – Seleção ampliada de estudantes para o Programa de Educação pelo Trabalho em Saúde – PET-Saúde 2025 – 2027**
- **Edital Nº 1751/2025 – Programa de auxílio financeiro para Mobilidade Acadêmica Nacional e Intercampi 2025/2**
- E outros 5 editais de 2025 com nomes completos...

## 📁 **ARQUIVOS GERADOS:**

- `editais_scraping.json` - Dados estruturados completos
- `editais_scraping.csv` - Formato Excel para fácil visualização

## 🎯 **AUTOMAÇÃO NO GITHUB:**

O workflow `.github/workflows/email-reports.yml` executa automaticamente:

```yaml
name: Relatórios Automáticos de Editais
on:
  schedule:
    - cron: '0 5 5 * *'     # Todo dia 5 às 5:00 UTC
    - cron: '0 5 * * 1'     # Toda segunda às 5:00 UTC
```

## 🚀 **COMO USAR MANUALMENTE:**

```bash
python fapemig_scraper.py
```

---

## ⚠️ **IMPORTANTE:**

- **Não esqueça** de configurar os secrets no GitHub
- **Use senha de app** do Gmail, não sua senha normal
- **Os emails são enviados automaticamente** - não precisa fazer nada depois de configurar
- **Total: 22 editais organizados** com nomes completos e identificação clara da fonte

---

**🎉 Sistema completo funcionando! Receberá emails automáticos com todos os editais de todas as fontes!**
