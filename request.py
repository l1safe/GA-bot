from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://goldapple.ru/19000180989-lazy-soft-paw"

def check_availability(url):
    driver = webdriver.Edge()
    driver.get(url)
    src = driver.page_source
    driver.quit()
    soup = BeautifulSoup(src, "lxml")
    ne_v_nalichii = soup.find("button", class_="TpmxJ BTMSE I3NIg SITf1 a1fxJ")
    if "узнать о поступлении" in ne_v_nalichii.text:
        print("Нет в наличии")
        return (" Нет в наличии")
    elif "добавить в корзину":
        print("Есть в наличии")
        return ("Есть в наличии")
    else:
        print("Ошибка")
        return "Ошибка"

