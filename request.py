from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def check_availability(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Set up the ChromeDriver
    service = Service('/usr/local/bin/chromedriver')  # Path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        src = driver.page_source
    finally:
        driver.quit()

    # Use BeautifulSoup to parse the content
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(src, "lxml")
    search_strings = ["нет в наличии", "добавить в корзину"]
    results = [text for text in soup.stripped_strings if text in search_strings]

    for i in results:
        if "нет в наличии" == i:
            print("Нет в наличии")
            return "Нет в наличии"
        elif "добавить в корзину" == i:
            print("Есть в наличии")
            return "Есть в наличии"

    print("Ошибка")
    return "Ошибка"
