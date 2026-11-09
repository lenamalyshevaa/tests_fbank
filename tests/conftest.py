import os

import pytest
from selenium import webdriver

from tests.pages.transfer_page import TransferPage

BASE_URL = os.getenv("BASE_URL", "http://localhost:9999")

# на счету 30 000 ₽, в резерве 10 000 ₽ -> доступно 20 000 ₽
BALANCE = 30000
RESERVED = 10000


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "1") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,1000")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(1)
    yield drv
    drv.quit()


@pytest.fixture
def page(driver):
    return TransferPage(driver, BASE_URL).open(BALANCE, RESERVED)


@pytest.fixture
def rub_page(page):
    """Выбран рублёвый счёт и введён корректный номер карты."""
    return page.choose_account("Рубли").enter_card("5559000000000001")
