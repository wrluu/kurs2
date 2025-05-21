import pytest

from src.vacancies import Vacancy


def test_vacancy_init(vacancy_Python_developer):
    """Тест инициализации экземпляра объекта Vacancy"""
    assert vacancy_Python_developer.name == "Python_developer"
    assert vacancy_Python_developer.url == "https://hh.ru/applicant/vacancy_response?vacancyId=117286365"
    assert vacancy_Python_developer.salary_from == 100000
    assert vacancy_Python_developer.salary_to == 120000
    assert vacancy_Python_developer.description == "Разработка и поддержка, back end части веб-приложений."


def test_create_vacancy_without_name(vacancy_without_name):
    """Тест на создание вакансии с отсутствием названия."""
    with pytest.raises(ValueError, match="Название вакансии и URL обязательны."):
        Vacancy(**vacancy_without_name)


def test_create_vacancy_without_url(vacancy_without_url):
    """Тест на создание вакансии с отсутствием url."""
    with pytest.raises(ValueError, match="Название вакансии и URL обязательны."):
        Vacancy(**vacancy_without_url)


def test_create_vacancy_negative_salary(vacancy_with_negative_salary):
    """Тест на создание вакансии с отрицательной зарплатой."""
    with pytest.raises(ValueError, match="Зарплата не может быть меньше 0."):
        Vacancy(**vacancy_with_negative_salary)


def test_create_vacancy_where_salary_to_more_salary_from(vacancy_with_salary_to_less_salary_from):
    """Тест на создание вакансии с зарплатой от больше чем зарплата до."""
    with pytest.raises(ValueError, match="Минимальная зарплата не может быть больше максимальной."):
        Vacancy(**vacancy_with_salary_to_less_salary_from)


def test_str_method(vacancy_Python_developer):
    """Тест на метод __str__."""

    assert (
        str(vacancy_Python_developer)
        == "Вакансия: Python_developer, Зарплата: 100000-120000, URL: https://hh.ru/applicant/vacancy_response?vacancyId=117286365"
    )


def test_vacancy_comparison_lt(vacancy_Python_developer, vacancy_system_administrator):
    """Тест на сравнение вакансий по средней зарплате (меньше)."""

    assert vacancy_Python_developer > vacancy_system_administrator


def test_vacancy_comparison_gt(vacancy_system_administrator, vacancy_Python_developer):
    """Тест на сравнение вакансий по средней зарплате (больше)."""

    assert vacancy_system_administrator < vacancy_Python_developer


def test_from_platform(platform_data):
    """Тест на метод from_platform."""
    vacancies = Vacancy.from_platform(platform_data)

    assert len(vacancies) == 2

    for vacancy in vacancies:
        assert isinstance(vacancy, Vacancy)

    assert vacancies[0].name == "Программист"
    assert vacancies[0].url == "https://example.com/job1"
    assert vacancies[0].salary_from == 80000
    assert vacancies[0].salary_to == 150000
    assert vacancies[0].description == "Отдел разработки"

    assert vacancies[1].name == "Тестировщик"
    assert vacancies[1].url == "https://example.com/job2"
    assert vacancies[1].salary_from == 60000
    assert vacancies[1].salary_to == 100000
    assert vacancies[1].description == "Отдел тестирования"


def test_vacancy_str_method(capsys, vacancy_Python_developer):
    """Тест метода __str__ класса Vacancy с использованием capsys."""
    print(vacancy_Python_developer)
    captured = capsys.readouterr()
    expected_output = "Вакансия: Python_developer, Зарплата: 100000-120000, URL: https://hh.ru/applicant/vacancy_response?vacancyId=117286365\n"
    assert captured.out == expected_output


def test_vacancy_comparison_lt(vacancy_Python_developer, vacancy_system_administrator):
    """Тест оператора < (__lt__) для сравнения вакансий по средней зарплате."""
    assert vacancy_system_administrator < vacancy_Python_developer
    assert not vacancy_Python_developer < vacancy_system_administrator


def test_validate_invalid_salary():
    """Тестирование валидации зарплаты в классе Vacancy."""
    with pytest.raises(ValueError, match="Зарплата не может быть меньше 0."):
        vacancy = Vacancy(name="Программист Python", url="https://example.com", salary_from=-100000)
