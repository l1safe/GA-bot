from bs4 import BeautifulSoup
from selenium import webdriver

def check_availability(url):
    driver = webdriver.Edge()
    driver.get(url)
    src = driver.page_source
    driver.quit()
    soup = BeautifulSoup(src, "lxml")
    search_strings = ["нет в наличии", "добавить в корзину"]
    results = [text for text in soup.stripped_strings if text in search_strings]
    for i in results:
        if "нет в наличии" == i:
            print("Нет в наличии")
            return (" Нет в наличии")
        elif "добавить в корзину":
            print("Есть в наличии")
            return ("Есть в наличии")
        else:
            print("Ошибка")
            return "Ошибка"
