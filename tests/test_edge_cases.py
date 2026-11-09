"""Дополнительные проверки: граничные значения и редкие сценарии (TC-6 ... TC-15)."""

import re

import pytest


def digits(text):
    return re.sub(r"\D", "", text)


# TC-6
def test_balance_and_reserve_from_url(page):
    assert digits(page.account_balance("rub")) == "30000"
    assert digits(page.account_reserved("rub")) == "10000"


# TC-7, TC-8: граница длины номера карты
@pytest.mark.parametrize(
    "card, amount_shown",
    [
        ("555900000000000", False),  # 15 цифр — поле суммы не появляется
        ("5559000000000001", True),  # 16 цифр — появляется
    ],
    ids=["15_digits", "16_digits"],
)
def test_amount_field_depends_on_card_length(page, card, amount_shown):
    page.choose_account("Рубли").enter_card(card)

    assert page.amount_field_shown() == amount_shown


# TC-9
def test_card_number_ignores_letters_and_symbols(page):
    page.choose_account("Рубли").enter_card("5559-abcd 0000_0000 0001")

    assert page.card_value() == "5559 0000 0000 0001"


# TC-10
def test_amount_ignores_letters(rub_page):
    rub_page.enter_amount("1a2b3")

    assert rub_page.amount_value() == "123"


# TC-11: комиссия на разных суммах
@pytest.mark.parametrize("amount, commission", [("100", "10"), ("1000", "100"), ("12300", "1230")])
def test_commission_for_different_amounts(rub_page, amount, commission):
    rub_page.enter_amount(amount)

    assert rub_page.commission() == commission


# TC-12, BUG-3: граница доступного остатка
@pytest.mark.parametrize(
    "amount, allowed",
    [
        ("18180", True),   # 18 180 + 1 810 комиссии = 19 990 < 20 000
        ("18190", True),   # 18 190 + 1 810 комиссии = 20 000 — ровно весь остаток (BUG-3)
        ("18200", False),  # 18 200 + 1 820 комиссии = 20 020 > 20 000
    ],
    ids=["below_limit", "exactly_limit", "above_limit"],
)
def test_available_balance_boundary(rub_page, amount, allowed):
    rub_page.enter_amount(amount)

    assert rub_page.transfer_available() == allowed
    assert rub_page.not_enough_money_shown() != allowed


# TC-13, BUG-4: проверка остатка на валютном счёте
@pytest.mark.parametrize(
    "account, amount",
    [
        ("Евро", "1000"),     # доступно 300 - 26 = 274 €
        ("Доллары", "5000"),  # доступно 100 $
    ],
    ids=["euro", "usd"],
)
def test_foreign_account_uses_own_balance(page, account, amount):
    page.choose_account(account).enter_card("5559000000000001").enter_amount(amount)

    assert page.not_enough_money_shown(), f"Со счёта «{account}» можно перевести {amount}, хотя средств не хватает"
    assert not page.transfer_available()


# TC-14, BUG-5: перевод нулевой суммы
def test_zero_amount_not_allowed(rub_page):
    rub_page.enter_amount("0")

    assert not rub_page.transfer_available(), "Кнопка «Перевести» доступна для суммы 0 ₽"


# TC-15: текст сообщения для максимальной допустимой суммы
def test_transfer_message_for_big_amount(rub_page):
    rub_page.enter_amount("18180")

    assert rub_page.transfer() == "Перевод 18180 ₽ на карту 5559000000000001 принят банком!"
