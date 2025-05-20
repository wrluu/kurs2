import pytest
import responses

from src.api_hh import HHJobPlatform


@pytest.fixture
def hh_platform():
    """Фикстура создаёт объект класса HHJobPlatform."""
    return HHJobPlatform()


def test_hh_api_init(hh_platform):
    """Проверка инициализации базового URL."""
    assert hh_platform.base_url == "https://api.hh.ru/vacancies"


@responses.activate
def test_connect_success(hh_platform):
    """Тест успешного подключения к API."""
    responses.add(responses.GET, "https://api.hh.ru/vacancies", status=200)
    assert hh_platform.connect() is True


@responses.activate
def test_get_vacancies_success(hh_platform):
    """Тест успешного получения списка вакансий."""
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json={
            "items": [{"id": 1, "name": "Developer"}],
        },
        status=200,
    )
    vacancies = hh_platform.get_vacancies("developer")
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Developer"


@responses.activate
def test_get_vacancies_failure(hh_platform):
    """Тест обработки ошибки при получении вакансий."""
    responses.add(responses.GET, "https://api.hh.ru/vacancies", status=404)
    vacancies = hh_platform.get_vacancies("Python")
    assert vacancies == []
