from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from time import sleep
import pandas as pd

# Configuração básica do Chrome com undetected_chromedriver
option = uc.ChromeOptions()

arguments = [
    '--lang=pt-BR',                         # Define o idioma do navegador
    '--window-size=1920,1080',             # Tamanho da janela (fullscreen "fake")
    '--no-sandbox',                        # Padrão em ambientes automatizados
    '--disable-dev-shm-usage',             # Evita problemas de memória compartilhada
    '--enable-logging',                    # Habilita logs do Chrome
    '--disable-infobars',                  # Remove barras de informação ("Chrome está sendo controlado...")
    '--disable-notifications',             # Desativa notificações
    '--disable-popup-blocking',            # Evita bloqueio de popups que você talvez precise
    '--remote-allow-origins=*',            # Libera algumas restrições de origem
    '--ignore-certificate-errors',         # Ignora erros de certificado SSL
    # Usa o perfil real do Chrome, para reaproveitar cookies, logins, etc.
    r'--user-data-dir=C:\Users\Win11\AppData\Local\Google\Chrome\User Data',
    r'--profile-directory=Profile 1'
]

for arg in arguments:
    option.add_argument(arg)

# Cria o navegador usando undetected_chromedriver (tenta evitar bloqueios tipo Cloudflare)
site = uc.Chrome(options=option)

# WebDriverWait para esperas explícitas, se você quiser usar depois
wait = WebDriverWait(site, 20)

# URL específica da instituição/IES
URL = "https://emec.mec.gov.br/emec/consulta-cadastro/detalhamento/d96957f455f6405d14c6542552b0f6eb/NDcy"
site.get(URL)
print(">>> Website acessado")

# Dá um tempo para a página carregar (incluindo JS inicial)
sleep(4.3)  # valor empírico, você pode trocar por espera explícita depois

try:
    # ===============================
    # DOM PRINCIPAL x IFRAME
    # ===============================
    # DOM principal = "estrutura" da página que o Selenium vê inicialmente.
    # Aqui no DOM principal existe uma DIV com id="consulta_cadastro".
    # Dentro dessa DIV, o site coloca um IFRAME que carrega OUTRA página
    # (detalhes da IES, com as abas vermelhas, incluindo "Graduação").
    #
    # Para acessar os elementos que estão DENTRO do iframe,
    # primeiro você precisa:
    # 1) Encontrar o elemento <iframe>
    # 2) Dar switch_to.frame(iframe)
    # Depois disso, o Selenium passa a "enxergar" o DOM interno do iframe.

    # 1) Localiza a DIV no DOM principal que contém o iframe de detalhes
    consulta_cadastro = site.find_element(By.ID, "consulta_cadastro")

    # Dentro dessa DIV, procura o elemento <iframe>
    iframe = consulta_cadastro.find_element(By.TAG_NAME, "iframe")

    # Agora faz o "switch" para o DOM interno desse iframe.
    # Aqui é como se você mudasse de "página pai" para "página filha".
    site.switch_to.frame(iframe)
    print(">>> Entrou no iframe de detalhes")

    # A partir daqui, todos os find_element vão olhar para DENTRO do iframe,
    # não mais para o DOM principal.

    # 2) Achar diretamente o <li id="cursos"> dentro do iframe
    # Esse <li> é a aba "Graduação", com título "Relação de Cursos de Graduação".
    li_cursos = site.find_element(By.ID, "cursos")
    print(">>> Elemento 'cursos' encontrado. Texto:", li_cursos.text.strip())

    # 3) Clicar na aba "cursos" (Graduação)
    # Isso dispara o JavaScript da página para carregar a lista de cursos
    # (geralmente abrindo outra URL ou outro iframe com a tabela).
    li_cursos.click()
    print(">>> Clique em 'cursos' realizado")

except Exception as e:
    # Captura qualquer erro que aconteça (não achou elemento, timeout, etc.)
    print(f"1 ERRO: {e}")

# Mantém o navegador aberto até você apertar ENTER (útil para inspecionar o resultado)
input("\nPressione ENTER para fechar...")
site.quit()
