"""
=============================================================================
SCRIPT DE EXTRAÇÃO DE CURSOS DO e-MEC
=============================================================================

Site alvo: https://emec.mec.gov.br/
Objetivo: Extrair lista de cursos de uma IES (Instituição de Ensino Superior)

ESTRUTURA DO SITE:
- Página principal carrega com aba "DETALHES DA IES" ativa
- Ao clicar em "GRADUAÇÃO", um iframe é carregado dinamicamente
- Dentro desse iframe, há uma tabela com id="listar-ies-cadastro"
- A tabela tem paginação (botão "Próximo" para ir para página 2, 3, etc.)

HTML RELEVANTE (simplificado):
<div class="tabArea">
    <a class="tab" id="tab_estatica">Instituição de Educação Superior</a>
    <a class="tab" id="tab_interativa">Curso</a>  <!-- Aba de GRADUAÇÃO -->
</div>

<div id="consulta_interativa" style="display: none">
    <iframe class="tabContent" name="tabIframe2" src="/emec/consulta-ies/...">
        <!-- Dentro deste iframe: -->
        <table id="listar-ies-cadastro">
            <thead>
                <tr><th>Curso</th><th>Quantidade</th></tr>
            </thead>
            <tbody>
                <tr class="corDetalhe_1">
                    <td>ADMINISTRAÇÃO</td>
                    <td>14</td>
                </tr>
                ...
            </tbody>
            <tfoot>
                <a title="Próximo" href="javascript:;" onclick="...">Próximo</a>
            </tfoot>
        </table>
    </iframe>
</div>

DESAFIOS:
1. Cloudflare anti-bot → resolvido com undetected_chromedriver
2. Conteúdo dentro de iframe → precisa switch_to.frame()
3. Iframe carregado dinamicamente → precisa clicar na aba primeiro
4. Não sabemos o nome exato do iframe → iteramos todos os iframes
5. Paginação dentro do iframe → precisa clicar "Próximo" no contexto certo

=============================================================================
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from time import sleep
import pandas as pd

# =============================================================================
# 1. CONFIGURAÇÃO DO CHROME (undetected_chromedriver para bypass Cloudflare)
# =============================================================================

option = uc.ChromeOptions()

# Lista de argumentos para configurar o Chrome
arguments = [
    '--lang=pt-BR',                    # Define idioma do navegador
    '--window-size=1920,1080',         # Tamanho da janela (importante para elementos responsivos)
    '--no-sandbox',                    # Necessário em alguns ambientes Linux/Docker
    '--disable-dev-shm-usage',         # Evita problemas de memória compartilhada
    '--enable-logging',                # Habilita logs do Chrome
    '--disable-infobars',              # Remove barra "Chrome está sendo controlado"
    '--disable-notifications',         # Bloqueia pop-ups de notificação
    '--disable-popup-blocking',        # Permite pop-ups (se necessário)
    '--remote-allow-origins=*',        # Permite conexões remotas (necessário em versões recentes)
    '--ignore-certificate-errors',     # Ignora erros de certificado SSL
    
    # IMPORTANTE: Usar perfil do Chrome existente para:
    # - Manter sessões logadas
    # - Evitar verificações de "novo dispositivo"
    # - Ter extensões/configurações já prontas
    r'--user-data-dir=C:\Users\Win11\AppData\Local\Google\Chrome\User Data',
    r'--profile-directory=Profile 1'   # Troque por 'Default' se for o perfil principal
]

# Adiciona cada argumento ao ChromeOptions
for arg in arguments:
    option.add_argument(arg)

# Inicializa o driver com as opções configuradas
site = uc.Chrome(options=option)

# WebDriverWait: ferramenta para esperar elementos aparecerem (até 20 segundos)
wait = WebDriverWait(site, 20)

# =============================================================================
# 2. ACESSO À PÁGINA INICIAL
# =============================================================================

# URL de exemplo: detalhamento de uma IES específica
# Estrutura: /detalhamento/{hash_ies}/{codigo_base64}
URL = "https://emec.mec.gov.br/emec/consulta-cadastro/detalhamento/d96957f455f6405d14c6542552b0f6eb/NDcy"

site.get(URL)
print(">>> Website acessado")

# Sleep para dar tempo ao Cloudflare processar
# Em produção, você pode usar WebDriverWait com condições específicas
sleep(10)

# =============================================================================
# 3. CLICAR NA ABA "GRADUAÇÃO" (que carrega o iframe de cursos)
# =============================================================================

print(">>> Clicando na aba 'GRADUAÇÃO'...")

# Pega todas as abas (elementos <a> com class="tab")
# HTML: <a class="tab" id="tab_interativa">Curso</a>
abas = site.find_elements(By.CSS_SELECTOR, "a.tab")

clicou = False
for aba in abas:
    # Verifica se o texto da aba contém "GRADUA" (funciona para "GRADUAÇÃO" ou "GRADUACAO")
    if "GRADUA" in aba.text.upper():
        # Usa JavaScript para clicar (mais confiável que .click() em alguns casos)
        site.execute_script("arguments[0].click();", aba)
        clicou = True
        print(f">>> Aba '{aba.text}' clicada com sucesso")
        break

if not clicou:
    raise Exception("❌ Não encontrei a aba GRADUAÇÃO na página.")

# Aguarda o iframe carregar após o clique
sleep(5)

# =============================================================================
# 4. ENCONTRAR O IFRAME CORRETO (sem depender de nome fixo)
# =============================================================================

print(">>> Procurando iframe com a tabela de cursos...")

# IMPORTANTE: Volta para o contexto principal (DOM pai)
# Isso garante que estamos "fora" de qualquer iframe antes de começar
site.switch_to.default_content()

# Pega TODOS os iframes da página
# HTML: <iframe class="tabContent" name="tabIframe2" src="..."></iframe>
iframes = site.find_elements(By.TAG_NAME, "iframe")
print(f">>> Total de iframes encontrados na página: {len(iframes)}")

# Lista para armazenar os cursos extraídos
cursos = []

# Variável para guardar qual iframe tem a tabela
iframe_com_tabela = None

# =============================================================================
# 5. ITERAR PELOS IFRAMES ATÉ ACHAR A TABELA
# =============================================================================

for idx, iframe in enumerate(iframes):
    try:
        # Volta pro contexto principal antes de entrar no próximo iframe
        site.switch_to.default_content()
        
        # Entra no iframe atual
        site.switch_to.frame(iframe)
        print(f">>> Testando iframe {idx}...")

        # Tenta achar a tabela com id="listar-ies-cadastro"
        # Se não existir neste iframe, vai dar exceção e pula pro próximo
        table = site.find_element(By.ID, "listar-ies-cadastro")
        
        # Se chegou aqui, ACHOU a tabela!
        print(f"✅ TABELA ENCONTRADA no iframe {idx}")
        iframe_com_tabela = iframe

        # =============================================================================
        # 6. EXTRAIR DADOS DA TABELA (PÁGINA 1)
        # =============================================================================
        
        # Pega todas as linhas do <tbody>
        # HTML: <tr class="corDetalhe_1"> ou <tr class="corDetalhe_2">
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f">>> Encontradas {len(rows)} linhas na página 1")

        # Itera por cada linha
        for row in rows:
            # Pega todas as células <td> da linha
            tds = row.find_elements(By.TAG_NAME, "td")
            
            # Valida se tem pelo menos 2 colunas (Curso e Quantidade)
            if len(tds) < 2:
                continue
            
            # Extrai o texto de cada célula
            # HTML: <td><a><div>&nbsp;&nbsp;ADMINISTRAÇÃO</div></a></td>
            curso = tds[0].text.strip()          # Coluna 1: Nome do curso
            quantidade = tds[1].text.strip()     # Coluna 2: Quantidade
            
            # Só adiciona se o curso não estiver vazio
            if curso:
                cursos.append({
                    "curso": curso,
                    "quantidade": quantidade
                })
                print(f"   Curso: {curso} | Quantidade: {quantidade}")
        
        # Achou a tabela, não precisa testar outros iframes
        break

    except Exception as e:
        # Este iframe não tem a tabela, continua pro próximo
        # (Não imprime erro para não poluir o log)
        continue

# =============================================================================
# 7. VALIDAÇÃO: TABELA FOI ENCONTRADA?
# =============================================================================

if iframe_com_tabela is None:
    print("❌ NENHUM iframe com a tabela 'listar-ies-cadastro' foi encontrado.")
    
    # Salva o HTML para debug
    with open("debug_sem_tabela.html", "w", encoding="utf-8") as f:
        f.write(site.page_source)
    print(">>> HTML salvo em 'debug_sem_tabela.html' para análise")
    
    # Encerra o script
    input("\nPressione ENTER para fechar...")
    site.quit()
    exit()

print(f"\n>>> Total extraído (página 1): {len(cursos)}")

# =============================================================================
# 8. PAGINAÇÃO (ir para página 2, 3, etc.)
# =============================================================================

# IMPORTANTE: Ainda estamos dentro do iframe correto
# A paginação também está dentro do mesmo iframe

try:
    print("\n>>> Tentando ir para página 2...")
    
    # Procura o botão "Próximo" dentro do iframe
    # HTML: <a title="Próximo" href="javascript:;" onclick="...">
    botao_proximo = site.find_element(
        By.XPATH,
        "//a[@title='Próximo' or @title='Proximo']"  # Aceita com ou sem acento
    )
    
    # Clica no botão usando JavaScript (mais confiável)
    site.execute_script("arguments[0].click();", botao_proximo)
    
    # Aguarda a página 2 carregar
    sleep(4)

    # =============================================================================
    # 9. EXTRAIR DADOS DA PÁGINA 2
    # =============================================================================
    
    # Pega a tabela novamente (agora com dados da página 2)
    table = site.find_element(By.ID, "listar-ies-cadastro")
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    print(f">>> Encontradas {len(rows)} linhas na página 2")

    # Mesmo processo de extração
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")
        if len(tds) < 2:
            continue
        
        curso = tds[0].text.strip()
        quantidade = tds[1].text.strip()
        
        if curso:
            cursos.append({
                "curso": curso,
                "quantidade": quantidade
            })
            print(f"   Curso: {curso} | Quantidade: {quantidade}")

except Exception as e:
    # Se não conseguir paginar (ex: só tem 1 página), não é erro crítico
    print(f">>> Não foi possível navegar para página 2: {e}")
    print(">>> (Provavelmente só existe 1 página de resultados)")

# =============================================================================
# 10. SALVAR RESULTADOS EM EXCEL
# =============================================================================

print(f"\n{'='*60}")
print(f">>> TOTAL GERAL EXTRAÍDO: {len(cursos)} cursos")
print(f"{'='*60}\n")

if cursos:
    # Converte lista de dicionários para DataFrame do pandas
    df = pd.DataFrame(cursos)
    
    # Salva em arquivo Excel
    df.to_excel("cursos_emec.xlsx", index=False)
    print("✅ Dados salvos em 'cursos_emec.xlsx'")
    
    # Mostra preview dos primeiros 5 cursos
    print("\n📊 Preview dos dados:")
    print(df.head())
else:
    print("⚠️ Nenhum curso foi extraído.")

# =============================================================================
# 11. FINALIZAÇÃO
# =============================================================================

input("\n✅ Extração concluída! Pressione ENTER para fechar o navegador...")
site.quit()

"""
=============================================================================
PONTOS DE ATENÇÃO PARA ADAPTAR ESTE CÓDIGO:
=============================================================================

1. CLOUDFLARE/ANTI-BOT:
   - Se o site usar Cloudflare, mantenha undetected_chromedriver
   - Se não, pode usar selenium.webdriver.Chrome normal

2. IFRAMES:
   - Sempre use switch_to.default_content() antes de procurar iframes
   - Sempre use switch_to.frame(iframe) antes de procurar elementos dentro
   - Se não souber o nome do iframe, itere todos como fizemos aqui

3. SELETORES:
   - Prioridade: ID > CLASS > CSS > XPATH
   - IDs são únicos e mais rápidos
   - Classes podem se repetir
   - XPATH é poderoso mas mais lento e frágil

4. PAGINAÇÃO:
   - Identifique se a paginação recarrega a página ou usa AJAX
   - Se usar AJAX (como aqui), precisa de sleep ou WebDriverWait
   - Sempre verifique se existe próxima página antes de clicar

5. DEBUGGING:
   - Sempre salve page_source quando algo der errado
   - Use prints para acompanhar o fluxo
   - Teste cada etapa separadamente antes de juntar tudo

6. PERFORMANCE:
   - Substitua sleep() por WebDriverWait quando possível
   - Exemplo: wait.until(EC.presence_of_element_located((By.ID, "tabela")))

=============================================================================
EXEMPLO DE ADAPTAÇÃO PARA OUTRO SITE:
=============================================================================

1. Abra o site no Chrome
2. Clique F12 (DevTools)
3. Inspecione o elemento que você quer extrair
4. Veja se está dentro de um <iframe>
5. Anote o ID, CLASS ou estrutura do elemento
6. Adapte os seletores deste código
7. Teste passo a passo

=============================================================================
"""
