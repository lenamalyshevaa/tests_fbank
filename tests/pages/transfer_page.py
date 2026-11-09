from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TransferPage:
    """Главная страница F-Bank: выбор счёта и перевод на карту."""

    CARD_INPUT = (By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']")
    AMOUNT_INPUT = (By.CSS_SELECTOR, "input[placeholder='1000']")
    COMMISSION = (By.ID, "comission")
    TRANSFER_BUTTON = (By.XPATH, "//button[.//text()='Перевести']")
    NOT_ENOUGH_MONEY = (By.XPATH, "//span[text()='Недостаточно средств на счете']")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self, balance, reserved):
        self.driver.get(f"{self.base_url}/?balance={balance}&reserved={reserved}")
        return self

    def choose_account(self, title):
        self.driver.find_element(By.XPATH, f"//h2[text()='{title}']").click()
        return self

    def enter_card(self, number):
        self.driver.find_element(*self.CARD_INPUT).send_keys(number)
        return self

    def enter_amount(self, amount):
        field = self.driver.find_element(*self.AMOUNT_INPUT)
        # Ctrl+A не работает на macOS, поэтому стираем значение посимвольно
        for _ in field.get_attribute("value"):
            field.send_keys(Keys.BACKSPACE)
        field.send_keys(amount)
        return self

    def card_value(self):
        return self.driver.find_element(*self.CARD_INPUT).get_attribute("value")

    def amount_value(self):
        return self.driver.find_element(*self.AMOUNT_INPUT).get_attribute("value")

    def amount_field_shown(self):
        return len(self.driver.find_elements(*self.AMOUNT_INPUT)) > 0

    def commission(self):
        return self.driver.find_element(*self.COMMISSION).text

    def account_balance(self, label):
        return self.driver.find_element(By.ID, f"{label}-sum").text

    def account_reserved(self, label):
        return self.driver.find_element(By.ID, f"{label}-reserved").text

    def transfer_available(self):
        return len(self.driver.find_elements(*self.TRANSFER_BUTTON)) > 0

    def not_enough_money_shown(self):
        return len(self.driver.find_elements(*self.NOT_ENOUGH_MONEY)) > 0

    def transfer(self):
        """Нажимает «Перевести» и возвращает текст всплывающего сообщения."""
        self.driver.find_element(*self.TRANSFER_BUTTON).click()
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text
