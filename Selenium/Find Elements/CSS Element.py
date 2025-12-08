from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


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

driver = iniciar_driver()
driver.get("https://cursoautomacao.netlify.app/")


checkbox = driver.find_element(By.CSS_SELECTOR, "input[class='form-check-input']") 
"""                                              TAG[Atributte='value']  OR  TAG.class  OR  TAG#id  """     


input('')