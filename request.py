from bs4 import BeautifulSoup
import requests

url = 'https://goldapple.ru/19000180989-lazy-soft-paw'

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
allNews = soup.find('button', class_='SjlhL _4oeL0 +a2KR Mh4g1 MtOhv')
print(allNews)
for data in allNews:
    text_content = data.text.strip() 
    print(f"Found text: '{text_content}'")  
    if text_content == 'нет в наличии':
        print('Нету в наличии')
    else: 
        print('Можно заказать')