from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def iniciar_driver(driver):
    chrome_options = Options()

    arguments = [
        "lang=pt-BR",
        "window-size=800,800",
        "disable-notifications",
        "incognito",
        "--disable-infobars",
        "--disable-blink-features=AutomationControlled",
        "--enable-logging",
        "--disable-backgrounding-occluded-windows"
    ]

    """TODAS AS CHROME OPTIONS MAIS USADAS (ATUAIS) + MOTIVO
    Use somente as que fazem sentido. Aqui está o catálogo completo para profissionais de automação.

    ===================== BÁSICAS =====================

    --start-maximized
        Abre o navegador maximizado. Útil para evitar erros de elementos fora da tela.

    --window-size=800,600
        Define tamanho fixo. Bom para padronizar screenshots.

    --lang=pt-BR / en-US
        Define idioma inicial. Pode alterar textos de sites.

    --incognito
        Abre o navegador em modo anônimo. Evita cache/cookies.

    --headless=new
        Roda sem abrir janela. Melhor para servidores CI/CD.

    --disable-notifications
        Bloqueia pop-ups de notificações.

    --disable-gpu
        Evita erros em ambientes sem GPU (Linux VMs).

    ==================== RENDER / PERFORMANCE ====================

    --disable-extensions
        Remove todas extensões. Reduz interferências.

    --disable-popup-blocking
        Permite pop-ups quando são necessários (login flows).

    --disable-infobars
        Remove “Chrome is being controlled by automated software”.

    --disable-dev-shm-usage
        Evita travamentos em servidores Docker (compartilhamento de memória).

    --no-sandbox
        Necessário em muitos servidores Linux sem permissões elevadas.

    --disable-blink-features=AutomationControlled
        Reduz detecção de automação. Útil para sites que bloqueiam bots.

    --remote-allow-origins=*
        Evita erro de segurança do Chrome 111+.

    ==================== PRIVACIDADE / REDUÇÃO DE RASTRO ====================

    --disable-web-security
        Desativa CORS e Same-Origin Policy. Só use para automação local, nunca em produção.

    --ignore-certificate-errors
        Aceita automaticamente certificados HTTPS inválidos.

    --disable-features=IsolateOrigins,site-per-process
        Evita isolamento de processo. Útil quando sites quebram no Selenium.

    ==================== REDES / PROXY ====================

    --proxy-server=IP:PORT
        Define proxy.

    --proxy-bypass-list=localhost
        Evita proxy em hosts específicos.

    --dns-prefetch-disable
        Evita prefetch de DNS (controle maior para testes de rede).

    ==================== LOGS / DEBUG ====================

    --enable-logging
        Ativa logs detalhados.

    --v=1
        Nível de verbosidade dos logs do Chrome.

    --log-level=3
        Reduz quantidade de logs do Chrome (0–3).

    ==================== MOBILE / EMULAÇÃO ====================

    --user-agent="STRING"
        Força user-agent (desktop, mobile, bot, bypass etc.)

    --window-size=360,640
        Emula resolução mobile (mas não faz mobile completo sem DevTools).

    ==================== DOWNLOADS ====================

    --no-default-browser-check
        Evita pop-up de “definir navegador padrão”.

    --safebrowsing-disable-download-protection
        Evita bloqueio de downloads automatizados.

    ==================== OUTROS ÚTEIS ====================

    --disable-background-timer-throttling
        Evita que JavaScript seja reduzido em abas em background.

    --disable-backgrounding-occluded-windows
        Mantém execução mesmo com janela minimizada.

    --allow-running-insecure-content
        Permite carregar HTTP dentro de HTTPS.

    --disable-sync
        Desativa sincronização do Chrome.

    --force-device-scale-factor=1
        Controla escala, útil para screenshots e layout fixo.

    """

    for arg in arguments:
        chrome_options.add_argument(arg)


    #============================ ADICIONAIS PARA DOWNLOADS AUTOMÁTICOS ============================#

    caminho_padrao_para_download = r"C:\Users\WIN11\Downloads"  # Lista de opções experimentais(nem todas estão documentadas) https://chromium.googlesource.com/chromium/src/+/32352ad08ee673a4d43e8593ce988b224f6482d3/chrome/common/pref_names.cc
    chrome_options.add_experimental_option("prefs", {
    'download. default_directory': caminho_padrao_para_download, 
    'download. directory_upgrade' : True, # Atualiza diretório para dietório passado acima
    'download. prompt_for_download': False, # Seta se o navegar deve pedir ou não para fazer download
    "profile.default_content_setting_values.notifications": 2, # Desabilita notificações
    # Allow multiple downoads
    "profile. default_content_setting_values. automatic_downloads": 1,

    })
    driver = webdriver.Chrome(options=chrome_options)
    return driver

if __name__ == "__main__":
    driver = iniciar_driver(driver=None)
    driver.get('https://www.devaprender.com')
    input("")