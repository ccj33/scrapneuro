# 🚀 SCRAPER FAPEMIG COMPLETO - VERSÃO FINAL
# Script único e completo para extrair editais FAPEMIG com datas
# Uso: python scraper_fapemig_final.py

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import re
import time
import csv
from bs4 import BeautifulSoup

def setup_driver():
    """Configura o driver do Edge para scraping ULTRA-RÁPIDO em modo headless com TIMEOUTS"""
    service = Service()
    options = webdriver.EdgeOptions()

    # 🚀 MODO HEADLESS - navegador invisível e super rápido
    options.add_argument('--headless=new')

    # ⚡ CONFIGURAÇÕES DE PERFORMANCE MÁXIMA
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-images')  # Carrega 10x mais rápido
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-ipc-flooding-protection')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-field-trial-config')
    options.add_argument('--disable-back-forward-cache')
    options.add_argument('--disable-hang-monitor')
    options.add_argument('--disable-prompt-on-repost')
    options.add_argument('--force-color-profile=srgb')
    options.add_argument('--metrics-recording-only')
    options.add_argument('--no-first-run')
    options.add_argument('--enable-automation')
    options.add_argument('--password-store=basic')
    options.add_argument('--use-mock-keychain')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-pings')
    options.add_argument('--no-service-autorun')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # 🏃‍♂️ CONFIGURAÇÕES DE VELOCIDADE EXTRA
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-plugins-discovery')
    options.add_argument('--disable-print-preview')
    options.add_argument('--disable-component-extensions-with-background-pages')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-translate')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--metrics-recording-only')
    options.add_argument('--mute-audio')
    options.add_argument('--no-crash-upload')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-login-animations')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-permissions-api')
    options.add_argument('--disable-session-crashed-bubble')
    options.add_argument('--disable-infobars')

    # 🌐 CONFIGURAÇÕES DE REDE PARA VELOCIDADE MÁXIMA
    options.add_argument('--disable-cache')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-offline-load-stale-cache')
    options.add_argument('--disk-cache-dir=/dev/null')
    options.add_argument('--media-cache-size=1')

    driver = webdriver.Edge(service=service, options=options)

    # ⏱️ CONFIGURAR TIMEOUTS PARA EVITAR TRAVAMENTOS
    driver.set_page_load_timeout(30)  # Timeout de 30 segundos para carregar página
    driver.implicitly_wait(10)        # Timeout implícito de 10 segundos

    return driver

def scrape_cnpq_completo():
    """
    Faz scraping simplificado e eficiente dos editais CNPq
    Baseado na análise: tudo está no HTML, não precisa clicar!
    """
    driver = None
    editais = []

    try:
        driver = setup_driver()
        print("🌐 Acessando CNPq...")
        driver.get("http://memoria2.cnpq.br/web/guest/chamadas-publicas")
        time.sleep(2)  # Tempo reduzido, não precisa esperar tanto

        print("🔍 Analisando HTML CNPq...")

        # 🎯 PEGAR TODO O CONTEÚDO DO CORPO DA PÁGINA
        page_source = driver.page_source

        # 💾 Salvar HTML para debug (OPCIONAL - remover se não precisar)
        # with open('debug_cnpq.html', 'w', encoding='utf-8') as f:
        #     f.write(page_source)
        # print("   📄 HTML salvo em debug_cnpq.html para análise")

        # 🎯 Procurar por <h4> que contenha Nº e 2025 (padrão correto dos editais)
        import re
        h4_pattern = r'<h4[^>]*>([^<]*Nº[^<]*2025[^<]*)</h4>'
        h4_matches = re.findall(h4_pattern, page_source, re.IGNORECASE)

        print(f"   🔍 Encontrados {len(h4_matches)} editais CNPq com padrão <h4>")

        raw_blocks = []
        # ⏱️ LIMITAR PROCESSAMENTO PARA EVITAR LOOP INFINITO
        max_editais = min(len(h4_matches), 20)  # Máximo 20 editais por fonte
        print(f"   📊 Processando até {max_editais} editais CNPq (limite de segurança)")

        for i, titulo in enumerate(h4_matches[:max_editais]):  # Limitar processamento
            # Pegar o bloco completo do edital a partir do <h4>
            h4_pos = page_source.find(f'<h4>{titulo}</h4>')
            if h4_pos != -1:
                # Pegar um bloco grande após o h4 (até próximo h4 ou fim da seção)
                block_start = h4_pos
                next_h4_pos = page_source.find('<h4>', h4_pos + 1)
                if next_h4_pos != -1:
                    block_content = page_source[block_start:next_h4_pos]
                else:
                    # Último edital, pegar até o final da seção de resultados
                    end_patterns = ['</div>', '</section>', '<div class="footer">']
                    block_end = len(page_source)
                    for pattern in end_patterns:
                        pos = page_source.find(pattern, block_start)
                        if pos != -1 and pos < block_end:
                            block_end = pos
                    block_content = page_source[block_start:block_end]

                raw_blocks.append(f'<h4>{titulo}</h4>{block_content}')

        if not raw_blocks:
            print("   ⚠️ Nenhum edital encontrado com padrão <h4>")
            # Fallback para o método anterior
            blocks = page_source.split("Chamada")
            if len(blocks) > 1:
                raw_blocks = blocks[1:8]  # Pegar apenas primeiros 7
                print(f"   🔄 Fallback: usando primeiros {len(raw_blocks)} blocos 'Chamada'")

        print(f"📋 {len(raw_blocks)} blocos de editais CNPq encontrados")

        for i, block in enumerate(raw_blocks):
            try:
                print(f"\n📄 Processando CNPq {i+1}...")

                # 🎯 EXTRAIR TÍTULO COMPLETO (melhorado)
                titulo_match = re.search(r'<h4[^>]*>([^<]+)</h4>', block)
                if titulo_match:
                    titulo = titulo_match.group(1).strip()
                    # Pegar também linhas seguintes para título completo
                    lines = block.split('\n')
                    titulo_completo = [titulo]

                    # Pegar próximas 2-3 linhas se forem continuação do título
                    for i, line in enumerate(lines):
                        if '<h4' in line and titulo_match.group(1) in line:
                            for j in range(i+1, min(i+4, len(lines))):
                                next_line = lines[j].strip()
                                if next_line and len(next_line) > 5 and not next_line.startswith('*') and not next_line.startswith('['):
                                    titulo_completo.append(next_line)
                                elif next_line and '**Inscrições:**' in next_line:
                                    break

                    titulo = ' '.join(titulo_completo)
                else:
                    # Fallback para linhas de texto
                    lines = block.split('\n')
                    titulo = ""
                    for line in lines[:5]:
                        line = line.strip()
                        if line and not line.startswith('[') and not line.startswith('*') and len(line) > 10:
                            titulo = line
                            break

                # Limpar título
                titulo = re.sub(r'\s+', ' ', titulo).strip()

                if not titulo:
                    continue

                print(f"   📝 Título: {titulo[:50]}...")

                # 📅 EXTRAIR PERÍODO DE INSCRIÇÕES (como você mostrou!)
                data_insc = ''
                datas_match = re.findall(r'\*\*Inscrições:\*\*\s*\n*([^\n]*\d{2}/\d{2}/\d{4}[^\n]*\d{2}/\d{2}/\d{4}[^\n]*)', block, re.MULTILINE)
                if datas_match:
                    # Pegar a primeira ocorrência limpa
                    for match in datas_match:
                        match = match.strip()
                        if match and len(match) > 10:
                            data_insc = match
                            break

                # Se não encontrou, tentar outro padrão
                if not data_insc:
                    datas_match = re.findall(r'\d{2}/\d{2}/\d{4}\s*a\s*\d{2}/\d{2}/\d{4}', block)
                    if datas_match:
                        data_insc = datas_match[0]

                # 📝 EXTRAIR DESCRIÇÃO
                descricao_encontrada = ""
                # Pegar texto entre </h4> e "**Inscrições:**"
                desc_match = re.search(r'</h4>(.+?)\*\*Inscrições:\*\*', block, re.DOTALL)
                if desc_match:
                    desc_text = desc_match.group(1).strip()
                    # Remover tags HTML e limpar
                    desc_text = re.sub(r'<[^>]+>', '', desc_text)
                    # Limpar linhas vazias e pegar primeiros parágrafos
                    paragraphs = [p.strip() for p in desc_text.split('\n') if p.strip() and len(p.strip()) > 20]
                    if paragraphs:
                        descricao_encontrada = paragraphs[0][:300] + "..." if len(paragraphs[0]) > 300 else paragraphs[0]

                # 🔗 EXTRAIR LINK DA CHAMADA
                url = ""
                # Primeiro tentar href com "chamadaDivulgada"
                match_url = re.search(r'href="([^"]*chamadaDivulgada[^"]*)"', block)
                if match_url:
                    url = match_url.group(1)
                else:
                    # Tentar Link Permanente
                    match_perm = re.search(r'Link Permanente.*?http[^\s\n<"]+', block)
                    if match_perm:
                        perm_match = re.search(r'(http[^\s\n<"]+)', match_perm.group(0))
                        if perm_match:
                            url = perm_match.group(1)
                    else:
                        # Último recurso: qualquer link http válido
                        match_any = re.search(r'http[^\s\n<"]+', block)
                        if match_any:
                            url = match_any.group(0)

                # Usar URL principal como fallback
                if not url:
                    url = "http://memoria2.cnpq.br/web/guest/chamadas-publicas"

                # 🎯 CRIAR ENTRADA CNPq SIMPLIFICADA
                edital_info = {
                    'titulo': titulo,
                    'data': data_insc,
                    'descricao': descricao_encontrada,
                    'url': url,
                    'fonte': 'cnpq'
                }

                editais.append(edital_info)

                print(f"   📅 Data inscrição: {data_insc}")
                print(f"   🔗 URL: {url[:50]}...")

            except Exception as e:
                print(f"   ❌ Erro ao processar bloco CNPq {i+1}: {str(e)}")
                continue

        print(f"\n🎉 CNPq concluído: {len(editais)} editais processados com sucesso!")
        return editais

    except Exception as e:
        print(f"❌ Erro geral CNPq: {str(e)}")
        return []

    finally:
        # 🔒 GARANTIR FECHAMENTO DO DRIVER
        if driver:
            try:
                driver.quit()
                print("✅ Driver CNPq fechado com sucesso")
            except Exception as e:
                print(f"⚠️  Erro ao fechar driver CNPq: {e}")

def scrape_ufmg_editais():
    """
    Faz scraping dos editais da Prograd/UFMG
    Baseado na análise: lista de editais com links e datas
    """
    driver = None
    editais = []

    try:
        driver = setup_driver()
        print("🌐 Acessando UFMG - Prograd Editais...")
        base_url = "https://www.ufmg.br/prograd/editais-chamadas/"

        # 📄 DETERMINAR NÚMERO DE PÁGINAS
        driver.get(base_url)
        time.sleep(2)

        # Procurar por "Página X de Y" para determinar total de páginas
        page_text = driver.find_element(By.TAG_NAME, "body").text
        total_pages = 1

        # Procurar padrão "Página 1 de X"
        import re
        page_match = re.search(r'Página \d+ de (\d+)', page_text)
        if page_match:
            total_pages = int(page_match.group(1))
            print(f"📄 Encontradas {total_pages} páginas de editais UFMG")

        # 🔄 PROCESSAR CADA PÁGINA (limitado para não travar)
        max_pages = min(total_pages, 5)  # Máximo 5 páginas para não travar
        for page_num in range(1, max_pages + 1):
            if page_num == 1:
                url = base_url
            else:
                url = f"{base_url}page/{page_num}/"

            print(f"\n📄 Processando página {page_num} de {total_pages}...")

            if page_num > 1:
                driver.get(url)
                time.sleep(2)

            # 🎯 ENCONTRAR TODOS OS LINKS DE EDITAIS
            # Procurar por links que contenham "Edital" ou "Chamada"
            edital_links = driver.find_elements(By.XPATH,
                "//a[contains(text(), 'Edital') or contains(text(), 'Chamada') or contains(text(), 'Seleção')]")

            print(f"📋 Encontrados {len(edital_links)} editais nesta página")

            # 📝 PROCESSAR CADA EDITAL (com limite de segurança)
            max_links_per_page = min(len(edital_links), 15)  # Máximo 15 editais por página
            print(f"   📊 Processando até {max_links_per_page} editais desta página")

            for i, link in enumerate(edital_links[:max_links_per_page]):  # Limitar processamento
                try:
                    # 🔗 EXTRAIR LINK DO PDF
                    pdf_url = link.get_attribute("href")

                    # 🎯 EXTRAIR NOME COMPLETO DO EDITAL (melhorado)
                    nome_edital = link.text.strip()

                    # Para UFMG, pegar também o texto do elemento pai para título completo
                    if pdf_url and 'ufmg' in pdf_url.lower():
                        try:
                            parent_element = link.find_element(By.XPATH, "..")
                            parent_text = parent_element.text
                            # Usar o texto do elemento pai que geralmente contém o título completo
                            if len(parent_text.strip()) > len(nome_edital):
                                nome_edital = parent_text.strip()
                        except:
                            pass

                    # Limpar quebras de linha e múltiplos espaços
                    nome_edital = re.sub(r'\s+', ' ', nome_edital)
                    nome_edital = nome_edital.replace('\n', ' ').replace('\r', ' ')

                    # 📅 EXTRAIR DATA DE ABERTURA
                    data_abertura = ""

                    # Procurar pelo texto irmão do link
                    try:
                        parent_element = link.find_element(By.XPATH, "..")
                        parent_text = parent_element.text

                        # Procurar por "Aberto em:"
                        if "Aberto em:" in parent_text:
                            # Extrair a data após "Aberto em:"
                            data_match = re.search(r'Aberto em:\s*([^\n\r]+)', parent_text)
                            if data_match:
                                data_abertura = data_match.group(1).strip()
                    except:
                        pass

                    # 🎯 CRIAR ENTRADA UFMG
                    if nome_edital and pdf_url:  # Só adiciona se tem nome e PDF
                        edital_info = {
                            'titulo': nome_edital,
                            'data': data_abertura,
                            'url': pdf_url,
                            'fonte': 'ufmg_prograd'
                        }

                        editais.append(edital_info)

                        print(f"   ✅ {nome_edital[:50]}...")
                        print(f"   📅 Data: {data_abertura}")
                        print(f"   🔗 PDF: {pdf_url[:50]}...")

                except Exception as e:
                    print(f"   ❌ Erro ao processar edital: {str(e)}")
                    continue

        print(f"\n🎉 UFMG concluído: {len(editais)} editais processados com sucesso!")
        return editais

    except Exception as e:
        print(f"❌ Erro geral UFMG: {str(e)}")
        return []

    finally:
        # 🔒 GARANTIR FECHAMENTO DO DRIVER
        if driver:
            try:
                driver.quit()
                print("✅ Driver UFMG fechado com sucesso")
            except Exception as e:
                print(f"⚠️  Erro ao fechar driver UFMG: {e}")

def scrape_fapemig_completo():
    """
    🆕 SCRAPING DO SITE NOVO DA FAPEMIG (2025)
    Site: https://fapemig.br/oportunidades/chamadas-e-editais
    """
    driver = None
    editais = []

    try:
        driver = setup_driver()
        print("🌐 Acessando NOVO site FAPEMIG...")
        driver.get("https://fapemig.br/oportunidades/chamadas-e-editais")
        time.sleep(5)  # Aguardar carregamento completo

        print("🔍 Analisando HTML do site novo...")
        page_source = driver.page_source

        # 💾 Salvar HTML para debug
        with open('debug_fapemig_novo.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print("   📄 HTML salvo em debug_fapemig_novo.html")

        # 🎯 PROCURAR CARDS DE EDITAIS NO SITE NOVO
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Procurar por diferentes padrões de cards
        card_selectors = [
            'div[class*="card"]',
            'div[class*="edital"]', 
            'div[class*="chamada"]',
            'section[class*="card"]',
            'article[class*="card"]'
        ]

        cards_encontrados = []
        for selector in card_selectors:
            cards = soup.select(selector)
            if cards:
                print(f"   ✅ Encontrados {len(cards)} cards com selector: {selector}")
                cards_encontrados = cards
                break

        if not cards_encontrados:
            # Fallback: procurar por texto que contenha "Chamada" ou "Edital"
            print("   🔍 Procurando por texto 'Chamada' ou 'Edital'...")
            elementos_com_chamada = soup.find_all(string=lambda text: text and any(palavra in text.lower() for palavra in ['chamada', 'edital', 'fapemig']))
            
            for elemento in elementos_com_chamada:
                # Pegar o elemento pai (card)
                card = elemento.find_parent(['div', 'section', 'article'])
                if card and card not in cards_encontrados:
                    cards_encontrados.append(card)

        print(f"📋 {len(cards_encontrados)} cards de editais encontrados")

        # ⏱️ LIMITAR PROCESSAMENTO
        max_cards = min(len(cards_encontrados), 30)
        print(f"   📊 Processando até {max_cards} cards (limite de segurança)")

        for i, card in enumerate(cards_encontrados[:max_cards]):
            try:
                print(f"\n📄 Processando card FAPEMIG {i+1}...")

                # 🎯 EXTRAIR TÍTULO
                titulo = ""
                # Procurar por diferentes tipos de título
                titulo_selectors = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b']
                
                for selector in titulo_selectors:
                    titulo_elem = card.find(selector)
                    if titulo_elem and titulo_elem.get_text(strip=True):
                        titulo = titulo_elem.get_text(strip=True)
                        if len(titulo) > 10:  # Título válido
                            break

                # Se não encontrou título, pegar texto destacado
                if not titulo:
                    texto_completo = card.get_text(separator=' ', strip=True)
                    linhas = texto_completo.split('\n')
                    for linha in linhas[:5]:  # Primeiras 5 linhas
                        if len(linha.strip()) > 15 and any(palavra in linha.lower() for palavra in ['chamada', 'edital', 'fapemig', '2025']):
                            titulo = linha.strip()
                            break

                print(f"   📝 Título: {titulo[:60]}...")

                # 📅 EXTRAIR DATAS
                datas_encontradas = []
                texto_card = card.get_text()
                
                # Padrões de data para o site novo
                data_patterns = [
                    r'submissão até (\d{1,2}/\d{1,2}/\d{4})',
                    r'Submissão até (\d{1,2}/\d{1,2}/\d{4})',
                    r'prazo.*?(\d{1,2}/\d{1,2}/\d{4})',
                    r'até (\d{1,2}/\d{1,2}/\d{4})',
                    r'(\d{1,2}/\d{1,2}/\d{4})',
                    r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})'
                ]

                for pattern in data_patterns:
                    matches = re.findall(pattern, texto_card, re.IGNORECASE)
                    for match in matches:
                        if match and match.strip():
                            datas_encontradas.append(match.strip())

                # 💰 EXTRAIR VALORES
                valor = ""
                valor_patterns = [
                    r'R\$\s*([\d.,]+)',
                    r'R\$\s*([\d.,]+)\s*milhões?',
                    r'R\$\s*([\d.,]+)\s*mil',
                    r'([\d.,]+)\s*milhões?',
                    r'([\d.,]+)\s*mil'
                ]

                for pattern in valor_patterns:
                    match = re.search(pattern, texto_card, re.IGNORECASE)
                    if match:
                        valor = match.group(0)
                        break

                # 📝 EXTRAIR DESCRIÇÃO
                descricao = ""
                texto_limpo = card.get_text(separator=' ', strip=True)
                sentences = texto_limpo.split('.')
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if (len(sentence) > 30 and len(sentence) < 300 and
                        not any(skip_word in sentence.lower() for skip_word in [
                            'http', 'www.', '.br', 'email:', 'telefone:', 'endereço',
                            'cep', 'belo horizonte', 'av.', 'rua', 'transparência'
                        ])):
                        if any(keyword in sentence.lower() for keyword in [
                            'edital', 'chamada', 'processo', 'programa', 'pesquisa',
                            'inovação', 'desenvolvimento', 'tecnologia', 'científica'
                        ]):
                            descricao = sentence[:250] + "..." if len(sentence) > 250 else sentence
                            break

                # 🔗 LINKS
                links = []
                for link in card.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('/'):
                        href = "https://fapemig.br" + href
                    elif not href.startswith('http'):
                        href = "https://fapemig.br/" + href
                    links.append(href)

                # 🎯 CRIAR ENTRADA FAPEMIG NOVA
                if titulo:  # Só adiciona se encontrou título
                    edital_info = {
                        'titulo': titulo,
                        'data': ', '.join(set(datas_encontradas)) if datas_encontradas else '',
                        'valor': valor,
                        'descricao': descricao,
                        'url': links[0] if links else "https://fapemig.br/oportunidades/chamadas-e-editais",
                        'links': '; '.join(links) if links else '',
                        'fonte': 'fapemig_novo_2025'
                    }

                    editais.append(edital_info)

                    print("   ✅ Card processado!")
                    print(f"   📅 Datas: {len(set(datas_encontradas))}")
                    if valor:
                        print(f"   💰 Valor: {valor}")
                    if descricao:
                        print(f"   📝 Descrição: {descricao[:50]}...")

            except Exception as e:
                print(f"   ❌ Erro ao processar card {i+1}: {str(e)}")
                continue

        print(f"\n🎉 FAPEMIG NOVO concluído: {len(editais)} editais processados!")
        return editais

    except Exception as e:
        print(f"❌ Erro geral FAPEMIG NOVO: {str(e)}")
        return []

    finally:
        if driver:
            try:
                driver.quit()
                print("✅ Driver FAPEMIG NOVO fechado")
            except Exception as e:
                print(f"⚠️  Erro ao fechar driver: {e}")

def salvar_resultados(editais):
    """Salva os resultados em JSON e CSV com organização unificada"""

    # Nomes padronizados para sempre sobrescrever os mesmos arquivos
    json_filename = 'editais_scraping.json'
    csv_filename = 'editais_scraping.csv'

    # Salvar JSON
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(editais, f, ensure_ascii=False, indent=2)

    # Salvar CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fonte', 'Título', 'Data', 'Descrição', 'URL', 'Anexos'])

        for edital in editais:
            writer.writerow([
                edital.get('fonte', '').upper(),
                edital.get('titulo', ''),
                edital.get('data', ''),
                edital.get('descricao', ''),
                edital.get('url', ''),
                edital.get('anexos', '')
            ])

    print(f"💾 ✓ Resultados salvos em {json_filename} e {csv_filename}")
    print(f"📊 Total: {len(editais)} editais de {len(set(e.get('fonte', '') for e in editais))} fontes")

def filtrar_ufmg_2025(editais):
    """Filtra apenas editais da UFMG de 2025"""
    editais_ufmg_2025 = []
    for edital in editais:
        if edital.get('fonte') == 'ufmg_prograd':
            data = edital.get('data', '')
            titulo = edital.get('titulo', '')
            # Verifica se tem 2025 na data OU no título
            if '2025' in data or '2025' in titulo:
                editais_ufmg_2025.append(edital)
                print(f"🎯 INCLUÍDO: {titulo[:50]}... (Data: {data})")
            else:
                print(f"❌ EXCLUÍDO: {titulo[:50]}... (Data: {data})")
    return editais_ufmg_2025

def main():
    """Função principal - RELATÓRIO COMPLETO TODOS OS SITES com TIMEOUT GLOBAL"""
    print("🚀 SCRAPER COMPLETO - FAPEMIG + CNPq + UFMG")
    print("⚡ Relatório com todos os editais de todos os sites")
    print("⏱️ Timeout global: 10 minutos")
    print("=" * 70)

    # ⏱️ TIMER GLOBAL PARA EVITAR TRAVAMENTOS
    import signal

    def timeout_handler(signum, frame):
        print("\n❌ TIMEOUT GLOBAL: Processo excedeu 10 minutos!")
        print("🔄 Finalizando execução para evitar travamento...")
        raise TimeoutError("Processo excedeu tempo limite")

    # Configurar timeout de 10 minutos (600 segundos)
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(600)  # 10 minutos

    try:
        # Executar scraping de todos os sites
        print("\n🏛️  PROCESSANDO FAPEMIG...")
        editais_fapemig = scrape_fapemig_completo()

        print("\n🔬 PROCESSANDO CNPq...")
        editais_cnpq = scrape_cnpq_completo()

        print("\n🎓 PROCESSANDO UFMG...")
        editais_ufmg = scrape_ufmg_editais()

        # Filtrar apenas editais UFMG de 2025
        print(f"🔍 Antes do filtro: {len(editais_ufmg)} editais UFMG")
        editais_ufmg_2025 = filtrar_ufmg_2025(editais_ufmg)
        print(f"🎯 Filtrados {len(editais_ufmg_2025)} editais UFMG de 2025")

        # Combinar todos os editais (FAPEMIG + CNPq + UFMG 2025 apenas)
        todos_editais = editais_fapemig + editais_cnpq + editais_ufmg_2025

        # Mostrar links principais
        link_fapemig = "http://www.fapemig.br/pt/chamadas_abertas_oportunidades_fapemig/"
        link_cnpq = "http://memoria2.cnpq.br/web/guest/chamadas-publicas"
        link_ufmg = "https://www.ufmg.br/prograd/editais-chamadas/"

        print("\n🔗 LINKS PRINCIPAIS:")
        print(f"🏛️  FAPEMIG: {link_fapemig}")
        print(f"🔬 CNPq: {link_cnpq}")
        print(f"🎓 UFMG: {link_ufmg}")
        print("=" * 70)

        print("\n🎯 RESULTADO FINAL - FAPEMIG + CNPq + UFMG 2025")
        print(f"📊 FAPEMIG: {len(editais_fapemig)} editais")
        print(f"📊 CNPq: {len(editais_cnpq)} editais")
        print(f"📊 UFMG 2025: {len(editais_ufmg_2025)} editais")
        print(f"📊 TOTAL GERAL: {len(todos_editais)} editais")

        editais_com_datas = [e for e in todos_editais if e.get('data')]
        print(f"✅ Com datas específicas: {len(editais_com_datas)}")

        # Mostrar estatísticas por fonte
        fapemig_com_datas = [e for e in editais_fapemig if e.get('data')]
        cnpq_com_datas = [e for e in editais_cnpq if e.get('data')]
        ufmg_2025_com_datas = [e for e in editais_ufmg_2025 if e.get('data')]

        print(f"🏛️  FAPEMIG com datas: {len(fapemig_com_datas)}")
        print(f"🔬 CNPq com datas: {len(cnpq_com_datas)}")
        print(f"🎓 UFMG 2025 com datas: {len(ufmg_2025_com_datas)}")

        # Mostrar alguns exemplos de cada fonte
        print("\n📋 EXEMPLO DE EDITAIS POR FONTE:")

        if editais_fapemig:
            print("\n🏛️  FAPEMIG:")
            for i, edital in enumerate(editais_fapemig[:2], 1):
                print(f"   {i}. {edital['titulo'][:50]}...")
                if edital.get('data'):
                    print(f"      📅 {edital['data']}")

        if editais_cnpq:
            print("\n🔬 CNPq:")
            for i, edital in enumerate(editais_cnpq[:2], 1):
                print(f"   {i}. {edital['titulo'][:50]}...")
                if edital.get('data'):
                    print(f"      📅 {edital['data']}")

        if editais_ufmg_2025:
            print("\n🎓 UFMG 2025:")
            for i, edital in enumerate(editais_ufmg_2025[:3], 1):
                print(f"   {i}. {edital['titulo'][:50]}...")
                if edital.get('data'):
                    print(f"      📅 {edital['data']}")

        if todos_editais:
            salvar_resultados(todos_editais)
            print("\n✅ Scraping concluído!")
            print(f"📁 Arquivos salvos: editais_scraping.json e .csv")
            print(f"🏛️  FAPEMIG: {link_fapemig}")
            print(f"🔬 CNPq: {link_cnpq}")
            print(f"🎓 UFMG: {link_ufmg}")
            print("📊 Relatório completo de todos os sites")
        else:
            print("\n❌ Nenhum edital encontrado.")

    except TimeoutError as e:
        print(f"\n❌ ERRO DE TIMEOUT: {str(e)}")
        print("🔧 O processo foi interrompido por exceder o tempo limite de 10 minutos")
        print("💡 Tente executar novamente ou verifique a conexão com a internet")

    except Exception as e:
        print(f"\n❌ ERRO GERAL: {str(e)}")
        print(f"🔧 Tipo do erro: {type(e).__name__}")

    finally:
        # Desabilitar o timer quando terminar
        signal.alarm(0)
        print("\n✅ Processo finalizado")

    print("=" * 70)

def enviar_email(destinatario, assunto, corpo):
    """
    Função para enviar email com relatório de editais
    """
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # ⚠️  CONFIGURAR SUAS CREDENCIAIS DE EMAIL AQUI
    EMAIL_REMETENTE = os.environ.get("EMAIL_USER", "seu_email@gmail.com")  # Do GitHub Secrets
    SENHA_EMAIL = os.environ.get("EMAIL_PASSWORD", "sua_senha_app")        # Do GitHub Secrets
    SMTP_SERVIDOR = "smtp.gmail.com"
    SMTP_PORTA = 587

    print(f"📧 Tentando enviar email para: {destinatario}")
    print(f"📧 Remetente: {EMAIL_REMETENTE}")
    print(f"📧 Servidor SMTP: {SMTP_SERVIDOR}:{SMTP_PORTA}")

    # 🔍 DEBUG: Verificar variáveis de ambiente
    import os
    print("🔍 DEBUG - Variáveis de ambiente:")
    print(f"   EMAIL_USER definido: {'Sim' if os.environ.get('EMAIL_USER') else 'Não'}")
    print(f"   EMAIL_PASSWORD definido: {'Sim' if os.environ.get('EMAIL_PASSWORD') else 'Não'}")
    print(f"   EMAIL_USER valor: {os.environ.get('EMAIL_USER', 'NÃO DEFINIDO')[:10]}...")
    print(f"   EMAIL_PASSWORD valor: {'*' * len(os.environ.get('EMAIL_PASSWORD', '')) if os.environ.get('EMAIL_PASSWORD') else 'NÃO DEFINIDO'}")

    # Verificar se as credenciais estão configuradas
    if EMAIL_REMETENTE == "seu_email@gmail.com" or SENHA_EMAIL == "sua_senha_app":
        print("❌ ERRO: Credenciais de email não configuradas!")
        print("🔧 Configure EMAIL_USER e EMAIL_PASSWORD no GitHub Secrets")
        print("🔧 No GitHub: Settings > Secrets and variables > Actions > New repository secret")
        return False

    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = destinatario
        msg['Subject'] = assunto

        # Adicionar corpo
        msg.attach(MIMEText(corpo, 'html'))

        print("🔗 Conectando ao servidor SMTP...")
        print(f"   Servidor: {SMTP_SERVIDOR}")
        print(f"   Porta: {SMTP_PORTA}")
        print(f"   Usuário: {EMAIL_REMETENTE}")

        # Conectar e enviar
        print("🔗 Criando conexão SMTP...")
        servidor = smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA)
        print("🔗 Iniciando TLS...")
        servidor.starttls()
        print("🔗 Fazendo login...")
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
        print("🔗 Enviando email...")
        servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        print("🔗 Fechando conexão...")
        servidor.quit()

        print(f"✅ Email enviado com sucesso para: {destinatario}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ ERRO DE AUTENTICAÇÃO: {str(e)}")
        print("🔧 Verifique se a senha do aplicativo está correta no GitHub Secrets")
        print("🔧 Para Gmail: Ative a verificação em 2 etapas e gere uma senha de aplicativo")
        return False

    except smtplib.SMTPConnectError as e:
        print(f"❌ ERRO DE CONEXÃO: {str(e)}")
        print("🔧 Verifique a conexão com a internet e as configurações do servidor SMTP")
        return False

    except Exception as e:
        print(f"❌ ERRO GERAL ao enviar email: {str(e)}")
        print(f"🔧 Tipo do erro: {type(e).__name__}")
        return False

def enviar_relatorio_automatico():
    """
    Função para enviar relatório automático baseado no dia da semana
    COM TODOS OS EDITAIS DE TODOS OS SITES
    """
    import datetime

    hoje = datetime.datetime.now()
    dia_semana = hoje.weekday()  # 0 = segunda, 6 = domingo
    dia_mes = hoje.day

    print("📅 Verificando condições para envio automático...")
    print(f"📅 Hoje é dia {dia_mes} do mês")
    print(f"📅 Dia da semana: {dia_semana} (0=segunda, 6=domingo)")
    print(f"📅 Data completa: {hoje.strftime('%d/%m/%Y %H:%M:%S')}")

    # 📧 CONFIGURAÇÃO DOS DESTINATÁRIOS
    EMAIL_DIARIO = "ccjota51@gmail.com"        # Recebe TODO DIA

    # 📧 DESTINATÁRIOS SEMANAIS (segunda-feira às 5h)
    DESTINATARIOS_SEMANAIS = [
        "mirelle_celiane@hotmail.com",
        "clevioferreira@gmail.com",
        "gustavo.augustoprs@gmail.com",
        "laviniagudulaufmg@gmail.com"
    ]

    print(f"📧 Email diário: {EMAIL_DIARIO}")
    print(f"📧 Destinatários semanais: {len(DESTINATARIOS_SEMANAIS)} pessoas")
    for i, email in enumerate(DESTINATARIOS_SEMANAIS, 1):
        print(f"   {i}. {email}")

    # ✅ ENVIO DIÁRIO ATIVADO (workflow roda todo dia às 5:00)
    deve_enviar_diario = True   # TODO DIA

    # 📅 VERIFICAR SE É SEGUNDA-FEIRA (0 = segunda-feira)
    deve_enviar_semanal = (dia_semana == 0)  # Só segunda-feira

    print(f"📧 Deve enviar relatório diário: {deve_enviar_diario}")
    print(f"📧 Deve enviar relatório semanal: {deve_enviar_semanal}")

    if not deve_enviar_diario and not deve_enviar_semanal:
        print("📧 Nenhuma condição de envio atendida hoje. Próximo envio:")
        print("📧 - Diariamente no dia 5 de cada mês")
        print("📧 - Semanalmente toda segunda-feira")
        return

    # Executar scraping de TODOS os sites
    print("\n🔄 Executando scraping completo para relatório...")
    try:
        editais_fapemig = scrape_fapemig_completo()
        editais_cnpq = scrape_cnpq_completo()
        editais_ufmg = scrape_ufmg_editais()

        # Filtrar apenas editais UFMG de 2025
        print(f"🔍 Antes do filtro: {len(editais_ufmg)} editais UFMG")
        editais_ufmg_2025 = filtrar_ufmg_2025(editais_ufmg)
        print(f"🎯 Filtrados {len(editais_ufmg_2025)} editais UFMG de 2025")

        # Combinar todos os editais (FAPEMIG + CNPq + UFMG 2025 apenas)
        todos_editais = editais_fapemig + editais_cnpq + editais_ufmg_2025

        print(f"📊 Total de editais para relatório: {len(todos_editais)}")

        # 📧 Todo dia 5 da manhã
        if deve_enviar_diario:
            print("\n📧 ENVIANDO RELATÓRIO DIÁRIO...")
            assunto = f"📅 RELATÓRIO DIÁRIO - FAPEMIG + CNPq + UFMG 2025 - {hoje.strftime('%d/%m/%Y')}"

            corpo_email = criar_corpo_email_diario_completo(todos_editais, hoje, editais_fapemig, editais_cnpq, editais_ufmg_2025)
            sucesso = enviar_email(EMAIL_DIARIO, assunto, corpo_email)

            if sucesso:
                print("✅ Relatório diário enviado com sucesso!")
            else:
                print("❌ Falha ao enviar relatório diário!")

        # 📧 Toda segunda-feira - ENVIAR PARA TODOS OS DESTINATÁRIOS
        if deve_enviar_semanal:
            print("\n📧 ENVIANDO RELATÓRIO SEMANAL PARA TODOS OS DESTINATÁRIOS...")
            assunto = f"📊 RELATÓRIO SEMANAL - FAPEMIG + CNPq + UFMG 2025 - Semana {hoje.strftime('%d/%m/%Y')}"

            corpo_email = criar_corpo_email_semanal_completo(todos_editais, hoje, editais_fapemig, editais_cnpq, editais_ufmg_2025)

            # Enviar para cada destinatário da lista
            sucessos = 0
            falhas = 0

            for i, destinatario in enumerate(DESTINATARIOS_SEMANAIS, 1):
                print(f"📧 Enviando para {i}/{len(DESTINATARIOS_SEMANAIS)}: {destinatario}")
                sucesso = enviar_email(destinatario, assunto, corpo_email)

                if sucesso:
                    sucessos += 1
                    print(f"   ✅ Sucesso: {destinatario}")
                else:
                    falhas += 1
                    print(f"   ❌ Falha: {destinatario}")

            print(f"\n📊 RESULTADO DO ENVIO SEMANAL:")
            print(f"   ✅ Sucessos: {sucessos}")
            print(f"   ❌ Falhas: {falhas}")
            print(f"   📧 Total: {len(DESTINATARIOS_SEMANAIS)} destinatários")

    except Exception as e:
        print(f"❌ ERRO GERAL no envio automático: {str(e)}")
        print(f"🔧 Tipo do erro: {type(e).__name__}")
        import traceback
        print("🔧 Traceback completo:")
        traceback.print_exc()

def criar_corpo_email_diario_completo(todos_editais, data, fapemig_editais, cnpq_editais, ufmg_editais):
    """Criar corpo do email diário COM TODOS OS SITES"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 5px; text-align: center; }}
            .fonte-section {{ background: #f8f9fa; margin: 20px 0; padding: 15px; border-radius: 8px; }}
            .fapemig {{ border-left: 4px solid #007bff; }}
            .cnpq {{ border-left: 4px solid #28a745; }}
            .ufmg {{ border-left: 4px solid #ffc107; }}
            .edital {{ background: #fff; margin: 8px 0; padding: 12px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            .data {{ color: #dc3545; font-weight: bold; font-size: 14px; }}
            .titulo {{ font-weight: bold; color: #333; font-size: 14px; }}
            .fonte-badge {{ display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; color: white; }}
            .fapemig-badge {{ background: #007bff; }}
            .cnpq-badge {{ background: #28a745; }}
            .ufmg-badge {{ background: #ffc107; color: #000; }}
            .stats {{ background: #e7f3ff; padding: 15px; margin: 20px 0; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 RELATÓRIO DIÁRIO COMPLETO</h1>
            <h2>FAPEMIG + CNPq + UFMG 2025</h2>
            <p>📅 Data: {data.strftime('%d/%m/%Y')}</p>
        </div>

        <div class="stats">
            <h2>📊 Resumo Geral do Dia</h2>
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div>
                    <h3 style="color: #007bff;">🏛️ FAPEMIG</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #007bff;">{len(fapemig_editais)}</p>
                    <p>editais</p>
                </div>
                <div>
                    <h3 style="color: #28a745;">🔬 CNPq</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #28a745;">{len(cnpq_editais)}</p>
                    <p>editais</p>
                </div>
                <div>
                    <h3 style="color: #ffc107;">🎓 UFMG 2025</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #ffc107;">{len(ufmg_editais)}</p>
                    <p>editais 2025</p>
                </div>
                <div>
                    <h3 style="color: #6c757d;">📊 TOTAL</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #6c757d;">{len(todos_editais)}</p>
                    <p>editais</p>
                </div>
            </div>
        </div>
    """

    # 📧 Seção UFMG (PRIMEIRA - como solicitado)
    if ufmg_editais:
        html += f"""
        <div class="fonte-section ufmg">
            <h2>🎓 UFMG - Universidade Federal de Minas Gerais (Apenas 2025)</h2>
            <p style="color: #666;"><strong>{len(ufmg_editais)} editais encontrados</strong></p>
        """

        for i, edital in enumerate(ufmg_editais, 1):
            html += f"""
            <div class="edital">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <h4>{i}. {edital['titulo']}</h4>
                        <p class="data">📅 {edital.get('data', 'Data não informada')}</p>
                    </div>
                    <span class="fonte-badge ufmg-badge">UFMG 2025</span>
                </div>
                <p>🔗 <a href="{edital.get('url', '#')}" target="_blank">Ver edital completo (PDF)</a></p>
            </div>
            """

        html += "</div>"

    # 📧 Seção CNPq (SEGUNDA)
    if cnpq_editais:
        html += f"""
        <div class="fonte-section cnpq">
            <h2>🔬 CNPq - Conselho Nacional de Desenvolvimento Científico e Tecnológico</h2>
            <p style="color: #666;"><strong>{len(cnpq_editais)} editais encontrados</strong></p>
        """

        for i, edital in enumerate(cnpq_editais, 1):
            html += f"""
            <div class="edital">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <h4>{i}. {edital['titulo']}</h4>
                        <p class="data">📅 {edital.get('data', 'Data não informada')}</p>
                        {'<p>📝 ' + edital.get('descricao', '') + '</p>' if edital.get('descricao') else ''}
                    </div>
                    <span class="fonte-badge cnpq-badge">CNPq</span>
                </div>
                <p>🔗 <a href="{edital.get('url', '#')}" target="_blank">Ver edital completo</a></p>
            </div>
            """

        html += "</div>"

    # 📧 Seção FAPEMIG (TERCEIRA)
    if fapemig_editais:
        html += f"""
        <div class="fonte-section fapemig">
            <h2>🏛️ FAPEMIG - Fundação de Amparo à Pesquisa do Estado de Minas Gerais</h2>
            <p style="color: #666;"><strong>{len(fapemig_editais)} editais encontrados</strong></p>
        """

        for i, edital in enumerate(fapemig_editais, 1):
            html += f"""
            <div class="edital">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <h4>{i}. {edital['titulo']}</h4>
                        <p class="data">📅 {edital.get('data', 'Data não informada')}</p>
                        {'<p>📎 Anexos: ' + edital.get('anexos', 'Nenhum') + '</p>' if edital.get('anexos') else ''}
                    </div>
                    <span class="fonte-badge fapemig-badge">FAPEMIG</span>
                </div>
                <p>🔗 <a href="{edital.get('url', '#')}" target="_blank">Ver edital completo</a></p>
            </div>
            """

        html += "</div>"

    html += """
        <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center;">
            <h3>📧 Sobre este relatório diário</h3>
            <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
                <li>🤖 <strong>Gerado automaticamente</strong> pelo sistema de scraping completo</li>
                <li>📅 <strong>Enviado diariamente</strong> no dia 5 de cada mês às 5:00 da manhã</li>
                <li>🏛️ <strong>FAPEMIG:</strong> Editais de pesquisa e inovação de Minas Gerais</li>
                <li>🔬 <strong>CNPq:</strong> Editais nacionais de desenvolvimento científico</li>
                <li>🎓 <strong>UFMG:</strong> Apenas editais de 2025 da Pró-Reitoria de Graduação</li>
                <li>⚡ <strong>Sistema:</strong> Scrap Neuro - Multi-site scraping</li>
            </ul>

            <p style="margin-top: 20px; color: #666; font-style: italic;">
                💡 Este relatório contém todos os editais ativos encontrados automaticamente
            </p>
        </div>
    </body>
    </html>
    """

    return html

def criar_corpo_email_semanal_completo(todos_editais, data, fapemig_editais, cnpq_editais, ufmg_editais):
    """Criar corpo do email semanal COM TODOS OS SITES"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
            .fonte-section {{ background: #f8f9fa; margin: 25px 0; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .fapemig {{ border-left: 5px solid #007bff; background: linear-gradient(to right, #f8f9ff 0%, #fff 100%); }}
            .cnpq {{ border-left: 5px solid #28a745; background: linear-gradient(to right, #f0fff0 0%, #fff 100%); }}
            .ufmg {{ border-left: 5px solid #ffc107; background: linear-gradient(to right, #fffef0 0%, #fff 100%); }}
            .edital {{ background: #fff; margin: 10px 0; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: all 0.3s ease; }}
            .edital:hover {{ transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.15); }}
            .data {{ color: #dc3545; font-weight: bold; font-size: 15px; background: #ffe6e6; padding: 5px 10px; border-radius: 15px; display: inline-block; margin: 5px 0; }}
            .titulo {{ font-weight: bold; color: #333; font-size: 16px; }}
            .urgente {{ background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border-left: 5px solid #ffc107; animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.8; }} 100% {{ opacity: 1; }} }}
            .fonte-badge {{ display: inline-block; padding: 4px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; color: white; margin-left: 10px; }}
            .fapemig-badge {{ background: #007bff; }}
            .cnpq-badge {{ background: #28a745; }}
            .ufmg-badge {{ background: #ffc107; color: #000; }}
            .stats {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; margin: 25px 0; border-radius: 10px; text-align: center; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin-top: 15px; }}
            .stat-item {{ background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px; }}
            .stat-number {{ font-size: 28px; font-weight: bold; color: #fff; }}
            .stat-label {{ font-size: 12px; color: rgba(255,255,255,0.9); text-transform: uppercase; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 RELATÓRIO SEMANAL COMPLETO</h1>
            <h2>FAPEMIG + CNPq + UFMG 2025</h2>
            <p style="font-size: 18px;">Semana de {data.strftime('%d/%m/%Y')}</p>
        </div>

        <div class="stats">
            <h2>🎯 RESUMO GERAL DA SEMANA</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{len(fapemig_editais)}</div>
                    <div class="stat-label">🏛️ FAPEMIG</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(cnpq_editais)}</div>
                    <div class="stat-label">🔬 CNPq</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(ufmg_editais)}</div>
                    <div class="stat-label">🎓 UFMG 2025</div>
                </div>
                <div class="stat-item">
                    <div style="font-size: 32px; color: #fff;">{len(todos_editais)}</div>
                    <div class="stat-label">📊 TOTAL</div>
                </div>
            </div>
        </div>
    """

    # 📧 Seção UFMG (PRIMEIRA - como solicitado)
    if ufmg_editais:
        html += f"""
        <div class="fonte-section ufmg">
            <h2>🎓 UFMG - Universidade Federal de Minas Gerais (Apenas 2025)</h2>
            <p style="color: #ffc107; font-weight: bold; font-size: 16px;">{len(ufmg_editais)} editais encontrados</p>
        """

        for i, edital in enumerate(ufmg_editais, 1):
            urgente_class = "urgente" if any(prazo in edital.get('data', '') for prazo in ['01/', '02/', '03/']) else ""

            html += f"""
            <div class="edital {urgente_class}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <h4 class="titulo">{i}. {edital['titulo']}</h4>
                        <p class="data">📅 Data limite: {edital.get('data', 'Data não informada')}</p>
                    </div>
                    <span class="fonte-badge ufmg-badge">UFMG 2025</span>
                </div>
                <p style="margin-top: 10px;">🔗 <a href="{edital.get('url', '#')}" target="_blank" style="color: #ffc107; text-decoration: none; font-weight: bold;">Ver edital completo (PDF)</a></p>
            </div>
            """

        html += "</div>"

    # 📧 Seção CNPq (SEGUNDA)
    if cnpq_editais:
        html += f"""
        <div class="fonte-section cnpq">
            <h2>🔬 CNPq - Conselho Nacional de Desenvolvimento Científico e Tecnológico</h2>
            <p style="color: #28a745; font-weight: bold; font-size: 16px;">{len(cnpq_editais)} editais encontrados</p>
        """

        for i, edital in enumerate(cnpq_editais, 1):
            urgente_class = "urgente" if any(prazo in edital.get('data', '') for prazo in ['01/', '02/', '03/']) else ""

            html += f"""
            <div class="edital {urgente_class}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <h4 class="titulo">{i}. {edital['titulo']}</h4>
                        <p class="data">📅 Data limite: {edital.get('data', 'Data não informada')}</p>
                        {'<p>📝 ' + edital.get('descricao', '')[:200] + '...</p>' if edital.get('descricao') else ''}
                    </div>
                    <span class="fonte-badge cnpq-badge">CNPq</span>
                </div>
                <p style="margin-top: 10px;">🔗 <a href="{edital.get('url', '#')}" target="_blank" style="color: #28a745; text-decoration: none; font-weight: bold;">Ver edital completo</a></p>
            </div>
            """

        html += "</div>"

    # 📧 Seção FAPEMIG (TERCEIRA)
    if fapemig_editais:
        html += f"""
        <div class="fonte-section fapemig">
            <h2>🏛️ FAPEMIG - Fundação de Amparo à Pesquisa do Estado de Minas Gerais</h2>
            <p style="color: #007bff; font-weight: bold; font-size: 16px;">{len(fapemig_editais)} editais encontrados</p>
        """

        for i, edital in enumerate(fapemig_editais, 1):
            urgente_class = "urgente" if any(prazo in edital.get('data', '') for prazo in ['01/', '02/', '03/']) else ""

            html += f"""
            <div class="edital {urgente_class}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <h4 class="titulo">{i}. {edital['titulo']}</h4>
                        <p class="data">📅 Data limite: {edital.get('data', 'Data não informada')}</p>
                        {'<p>📎 Anexos: ' + edital.get('anexos', 'Nenhum') + '</p>' if edital.get('anexos') else ''}
                    </div>
                    <span class="fonte-badge fapemig-badge">FAPEMIG</span>
                </div>
                <p style="margin-top: 10px;">🔗 <a href="{edital.get('url', '#')}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Ver edital completo</a></p>
            </div>
            """

        html += "</div>"

    html += """
        <div style="margin-top: 50px; padding: 25px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 15px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
            <h2>📧 SOBRE ESTE RELATÓRIO SEMANAL</h2>
            <div style="max-width: 800px; margin: 0 auto;">
                <ul style="text-align: left; line-height: 1.8;">
                    <li>🤖 <strong>Gerado automaticamente</strong> pelo sistema de scraping multi-site</li>
                    <li>📅 <strong>Enviado toda segunda-feira</strong> às 5:00 da manhã</li>
                    <li>🏛️ <strong>FAPEMIG:</strong> Editais de pesquisa e inovação do estado de Minas Gerais</li>
                    <li>🔬 <strong>CNPq:</strong> Editais nacionais de desenvolvimento científico e tecnológico</li>
                    <li>🎓 <strong>UFMG:</strong> Apenas editais de 2025 da Pró-Reitoria de Graduação</li>
                    <li>⚡ <strong>Sistema:</strong> Scrap Neuro - Multi-site scraping avançado</li>
                    <li>📊 <strong>Contém:</strong> Todos os editais ativos com nome, data e links diretos</li>
                </ul>

                <div style="margin-top: 25px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px;">
                    <p style="margin: 0; font-style: italic;">
                        💡 <strong>Dica:</strong> Os editais com fundo amarelo pulsante têm prazos próximos!
                    </p>
                    <p style="margin: 10px 0 0 0; font-size: 14px;">
                        🎯 <strong>Total semanal:</strong> {len(todos_editais)} editais (FAPEMIG + CNPq + UFMG 2025)
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    import sys

    # Verificar se é apenas teste de email
    if len(sys.argv) > 1 and sys.argv[1] == "--teste-email":
        print("🧪 Executando apenas teste de email...")
        from teste_email import testar_email
        testar_email()
        exit(0)

    main()

    # 🚀 ENVIAR RELATÓRIO AUTOMÁTICO APÓS O SCRAPING
    print("\n📧 ENVIANDO RELATÓRIO AUTOMÁTICO...")
    try:
        enviar_relatorio_automatico()
        print("✅ Relatório automático enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar relatório automático: {str(e)}")
        print("🔄 Continuando sem envio de email...")
