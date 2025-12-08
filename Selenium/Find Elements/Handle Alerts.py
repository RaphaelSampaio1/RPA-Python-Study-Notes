from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

def iniciar_driver():
    chrome_options = Options()

    arguments = [
        "lang=pt-BR",
        "--start-maximized",
        "disable-notifications",
        "--disable-infobars",
        "--disable-blink-features=AutomationControlled",
        "--enable-logging",
        "--disable-backgrounding-occluded-windows"
    ]

    for arg in arguments:
        chrome_options.add_argument(arg)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


"""
FIRST  ALERT HADLE = Line 49 (Accept)
SECOND ALERT HADLE = Line 63 (Dismiss)
THIRD  ALERT HADLE = Line 72 (Type alert)
"""


driver = iniciar_driver()
driver.get("https://cursoautomacao.netlify.app/")
sleep(2)

# Situação 1 - Fechar alerta
# descer a página até elementos estarem visívei
driver.execute_script("window.scrollTo(0, 500);")
sleep(2)

# digitar meu nome
driver.find_element(By.ID, "nome").send_keys("Raphael Sampaio")
sleep(2)

# clicar em alerta
driver.find_element(By.ID, "buttonalerta").click()
sleep(2)

# clicar em ok para fechar alerta
alert1 = driver.switch_to.alert
alert1.accept()
sleep(5)


# Situação 2 - Confirmar ou cancelar alerta
# clicar no campo de confirmar
driver.find_element(By.ID, "buttonconfirmar").click()
sleep(2)

# Clicar em ok ou cancelar
alert2 = driver.switch_to.alert
alert2.dismiss()  # cancelar

# Situação 3 - Inserir dados em alerta e depois confirmar ou cancelar esses dados, além de fechar a alerta posterior
# Clicar em fazer pergunta
driver.find_element(By.ID, "botaoPrompt").click()
sleep(2)

# Escrever no campo do alerta
alert3 = driver.switch_to.alert
alert3.send_keys("04 de Abril de 2026")
sleep(2)

# Dar ok
alert3.accept()
sleep(1)
alert3.accept()

input('')



# Situação 2 - Confirmar ou cancelar alerta
# clicar no campo de confirmar
# Clicar em ok ou cancelar
