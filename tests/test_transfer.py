"""Автотесты по тест-кейсам ручного тестирования TC-1 ... TC-5."""

CARD = "5559000000000001"


# TC-1
def test_transfer_valid_amount(rub_page):
    rub_page.enter_amount("1000")

    assert rub_page.transfer() == f"Перевод 1000 ₽ на карту {CARD} принят банком!"


# TC-2
def test_commission_is_10_percent(rub_page):
    rub_page.enter_amount("5000")

    assert rub_page.commission() == "500"


# TC-3
def test_amount_more_than_available(rub_page):
    rub_page.enter_amount("19000")  # 19 000 + 1 900 комиссии > 20 000 доступно

    assert rub_page.not_enough_money_shown()
    assert not rub_page.transfer_available()


# TC-4, BUG-1: в поле карты можно ввести 17 цифр
def test_card_number_max_16_digits(page):
    page.choose_account("Рубли").enter_card(CARD + "1")

    assert page.card_value() == "5559 0000 0000 0001"


# TC-5, BUG-2: можно перевести отрицательную сумму
def test_negative_amount_not_allowed(rub_page):
    rub_page.enter_amount("-1000")

    assert not rub_page.transfer_available(), "Кнопка «Перевести» доступна для суммы -1000 ₽"
