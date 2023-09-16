import telebot
from time import sleep
from setup import TOKEN, CHAT_ID
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

class Magalu:
    def __init__(self, driver):
        self.driver = driver
        
        
# Inicialize o driver do Selenium
ff = webdriver.Chrome()
ff.get('https://www.magazineluiza.com.br/selecao/ofertasdodia/')
html = ff.page_source
soup = bs(html, 'html.parser')
bot = telebot.TeleBot(token=TOKEN, parse_mode='MARKDOWN')

links = soup.find_all('ul')
for link in links:
    box = link.find_all('li', class_="sc-dxlmjS gjCMbP")
    for item in box:
        product_title = item.find('h2', class_='sc-ijtseF ypydh').text
        price_original = item.find('p', {'data-testid': 'price-original'}).text
        price_value = item.find('p', {'data-testid': 'price-value'}).text
        product_link = item.find('a', class_='sc-kOPcWz dSFUBN sc-jRBLiq ZHFfJ sc-jRBLiq ZHFfJ')['href']
        
        print(f'''

Título: {product_title}
Preço Original: {price_original}
Preço com Desconto: {price_value}
Link: https://www.magazineluiza.com.br/{product_link}

''')

        # Encontre a URL da imagem
        image_url = item.find('img', {'data-testid': 'image'})['src']
        
        # Baixe a imagem
        image_response = requests.get(image_url)
        with open('product_image.jpg', 'wb') as image_file:
            image_file.write(image_response.content)
        
        # Envie a mensagem para o Telegram com a imagem
        with open('product_image.jpg', 'rb') as image_file:
            bot.send_photo(CHAT_ID, image_file, caption=f'''
Título: {product_title}
Preço Original: {price_original}
Preço com Desconto: {price_value}
Link: https://www.magazineluiza.com.br/{product_link}
''')
        
        sleep(60)

# Feche o driver do Selenium
ff.quit()
