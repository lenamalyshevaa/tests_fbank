# Тестирование сервиса F-Bank

[![Selenium tests](https://github.com/lenamalyshevaa/tests_fbank/actions/workflows/tests.yml/badge.svg)](https://github.com/lenamalyshevaa/tests_fbank/actions/workflows/tests.yml)

Итоговое задание по дисциплине «Тестирование прикладного ПО».

Тестируется учебный сервис F-Bank для перевода денег со счёта на карту.

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
