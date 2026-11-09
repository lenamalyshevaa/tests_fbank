# Тестирование сервиса F-Bank

[![Selenium tests](https://github.com/lenamalyshevaa/tests_fbank/actions/workflows/tests.yml/badge.svg)](https://github.com/lenamalyshevaa/tests_fbank/actions/workflows/tests.yml)

Итоговое задание по дисциплине «Тестирование прикладного ПО».

Тестируется учебный сервис F-Bank для перевода денег со счёта на карту.

## Где что смотреть

| Что | Ссылка |
|-----|--------|
| **Баг-репорты (Issues)** | [Issues](https://github.com/lenamalyshevaa/tests_fbank/issues) |
| **Баг-репорты (файл)** | [docs/bug-reports.md](https://github.com/lenamalyshevaa/tests_fbank/blob/main/docs/bug-reports.md) |
| **Тест-кейсы ручного тестирования** | [docs/test-cases.md](https://github.com/lenamalyshevaa/tests_fbank/blob/main/docs/test-cases.md) |
| **Автотесты (Selenium + pytest)** | [tests/](https://github.com/lenamalyshevaa/tests_fbank/tree/main/tests) |
| **Настройка CI** | [.github/workflows/tests.yml](https://github.com/lenamalyshevaa/tests_fbank/blob/main/.github/workflows/tests.yml) |
| **Сборки в GitHub Actions** | [вкладка Actions](https://github.com/lenamalyshevaa/tests_fbank/actions/workflows/tests.yml) |

### Найденные дефекты

| ID | Issue | Дефект | Серьёзность | Тест-кейс | Автотест |
|----|-------|--------|-------------|-----------|----------|
| [BUG-1](https://github.com/lenamalyshevaa/tests_fbank/blob/main/docs/bug-reports.md#bug-1) | [#1](https://github.com/lenamalyshevaa/tests_fbank/issues/1) | В поле «Номер карты» можно ввести 17 цифр | Major | TC-4 | `test_card_number_max_16_digits` |
| [BUG-2](https://github.com/lenamalyshevaa/tests_fbank/blob/main/docs/bug-reports.md#bug-2) | [#2](https://github.com/lenamalyshevaa/tests_fbank/issues/2) | Можно перевести отрицательную сумму | Critical | TC-5 | `test_negative_amount_not_allowed` |
| [BUG-3](https://github.com/lenamalyshevaa/tests_fbank/blob/main/docs/bug-reports.md#bug-3) | [#3](https://github.com/lenamalyshevaa/tests_fbank/issues/3) | Нельзя перевести сумму, которая с комиссией ровно равна остатку | Major | TC-12 | `test_available_balance_boundary[exactly_limit]` |
| [BUG-4](https://github.com/lenamalyshevaa/tests_fbank/blob/main/docs/bug-reports.md#bug-4) | [#4](https://github.com/lenamalyshevaa/tests_fbank/issues/4) | На валютных счетах не проверяется их собственный остаток | Critical | TC-13 | `test_foreign_account_uses_own_balance` |
| [BUG-5](https://github.com/lenamalyshevaa/tests_fbank/blob/main/docs/bug-reports.md#bug-5) | [#5](https://github.com/lenamalyshevaa/tests_fbank/issues/5) | Можно перевести 0 ₽ | Minor | TC-14 | `test_zero_amount_not_allowed` |

Сборка в CI красная, потому что автотесты на эти дефекты падают (6 failed, 14 passed).

## Что есть в репозитории

- `app/` — сам сервис (собранный фронтенд из архива)
- `docs/test-cases.md` — тест-кейсы ручного тестирования
- `docs/bug-reports.md` — баг-репорты на найденные дефекты
- `tests/` — автотесты на Selenium + pytest
  - `pages/transfer_page.py` — Page Object главной страницы
  - `test_transfer.py` — автотесты по основным тест-кейсам TC-1 ... TC-5
  - `test_edge_cases.py` — граничные значения и редкие сценарии TC-6 ... TC-15
- `.github/workflows/tests.yml` — запуск автотестов в GitHub Actions

## Результаты

**Ручное тестирование.** Проведено 5 основных тестов, 2 из них нашли разные дефекты:

- [BUG-1](docs/bug-reports.md#bug-1): в поле «Номер карты» можно ввести 17 цифр
- [BUG-2](docs/bug-reports.md#bug-2): можно перевести отрицательную сумму

Дополнительные проверки граничных значений (TC-6 ... TC-15) нашли ещё три дефекта:

- [BUG-3](docs/bug-reports.md#bug-3): нельзя перевести сумму, которая с комиссией ровно равна остатку
- [BUG-4](docs/bug-reports.md#bug-4): на валютных счетах не проверяется их собственный остаток
- [BUG-5](docs/bug-reports.md#bug-5): можно перевести 0 ₽

**Автоматизированное тестирование.** На каждый тест-кейс есть автотест, на каждый дефект есть автотест, который на нём падает. Всего 20 запусков тестов: 14 проходят, 6 падают на дефектах, поэтому сборка в CI красная.

## Как запустить локально

Нужны Python 3.10+ и Google Chrome.

```bash
pip install -r requirements.txt

# запустить сервис
python -m http.server 9999 --directory app

# в другом терминале запустить тесты
pytest
```

Сервис открывается по адресу http://localhost:9999/?balance=30000&reserved=10000

Чтобы видеть браузер во время прогона: `HEADLESS=0 pytest`.
