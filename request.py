from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging

def check_availability(url, driver_path='/usr/local/bin/chromedriver'):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure headless mode
    chrome_options.add_argument("--no-sandbox")  # Avoid sandbox issues
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome resource problems
    chrome_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration

    service = Service(driver_path)
    driver = None

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        src = driver.page_source
    except Exception as e:
        logging.error(f"Error occurred while accessing the URL: {e}")
        return "Ошибка"
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logging.error(f"Error occurred while quitting the WebDriver: {e}")

    soup = BeautifulSoup(src, "lxml")
    search_strings = ["нет в наличии", "добавить в корзину"]
    results = [text for text in soup.stripped_strings if text in search_strings]

    for result in results:
        if "нет в наличии" == result:
            logging.info("Нет в наличии")
            return "Нет в наличии"
        elif "добавить в корзину" == result:
            logging.info("Есть в наличии")
            return "Есть в наличии"

    logging.warning("Страница не содержит ожидаемых строк")
    return "Ошибка"