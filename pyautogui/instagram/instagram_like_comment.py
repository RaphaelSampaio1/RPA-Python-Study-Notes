import pyautogui
import webbrowser
from time import sleep
import random

class InstagramBot:
    def __init__(self, comments: list[str], page_url: str, browser_path: str = None):
        self.comments = comments
        self.page_url = page_url
        self.browser_path = browser_path
        self.first_time = True  # controla se é a primeira execução na página

    def navegar_pagina(self):
        if self.browser_path:
            webbrowser.get(f'"{self.browser_path}" %s').open(self.page_url)
        else:
            webbrowser.open(self.page_url)
        sleep(5)

    def like_and_comment(self):
        # clicar no post correto
        if self.first_time:
            pyautogui.click(752, 819)  # primeiro post
            self.first_time = False
        else:
            # avança para o próximo post (seta para a direita)
            pyautogui.press("right")
        sleep(3)

        # clicar no campo de comentário
        pyautogui.click(1307, 1079)
        sleep(1.3)

        # escrever comentário
        pyautogui.write(random.choice(self.comments), interval=0.05)
        pyautogui.hotkey("enter")
        sleep(2)

        print("Comentário enviado. Indo para a próxima postagem.")
        sleep(5)

    def run(self):
        run_time = 5
        count = 0

        self.navegar_pagina()
        while count < run_time:
            self.like_and_comment()
            count += 1
            print(f"Postagem {count} concluída.")
            sleep(5)


if __name__ == "__main__":
    comment_list = [
        "Seu conteúdo é abençoado demais!",
        "Passou a ser meu conteúdo favorito!",
        "Parabéns pelos seus vídeos de verdade!",
        "Muito bom!",
    ]

    page_urls = [
        "https://www.instagram.com/tomasiamaria__/",
        "https://www.instagram.com/leticiaalmeidaflorencio/"
    ]

    browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    for url in page_urls:
        bot = InstagramBot(comment_list, url, browser_path)
        bot.run()
