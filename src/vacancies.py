from typing import Dict, List


class Vacancy:
    """Класс, представляющий вакансию с атрибутами"""
    __slots__ = ["name", "url", "salary_from", "salary_to", "description"]

    def __init__(self, name, url, salary_from=None, salary_to=None, description=None):
        self.name = name
        self.url = url
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_to is not None else 0
        self.description = description or "Описание не указано"

        self._validate()

    def _validate(self):
        """Проверка данных вакансии"""
        if not self.name or not self.url:
            raise ValueError("Название вакансии и URL обязательны.")

        if self.salary_from < 0 or self.salary_to < 0:
            raise ValueError("Зарплата не может быть отрицательной.")

        if self.salary_from > self.salary_to and self.salary_to != 0:
            raise ValueError("Минимальная зарплата не может быть больше максимальной.")

    def __str__(self):
        """Строковое представление объекта Vacancy"""
        return f"Вакансия: {self.name}, Зарплата: {self.salary_from}-{self.salary_to}, URL: {self.url}"

    def __lt__(self, other):
        """Сравнивает две вакансии по средней зарплате"""
        avg_salary_self = (self.salary_from + self.salary_to) / 2
        avg_salary_other = (other.salary_from + other.salary_to) / 2
        return avg_salary_self < avg_salary_other

    def __gt__(self, other):
        """Сравнивает две вакансии по средней зарплате"""
        avg_salary_self = (self.salary_from + self.salary_to) / 2
        avg_salary_other = (other.salary_from + other.salary_to) / 2
        return avg_salary_self > avg_salary_other

    @staticmethod
    def from_platform(platform_data: List[Dict]):
        """Создает список объектов Vacancy из данных платформ"""
        vacancies = []
        for job_data in platform_data:
            name = job_data.get("name", "Название не указано")
            url = job_data.get("apply_alternate_url", "")

            salary_from = job_data.get("salary", {}).get("from", 0) if job_data.get("salary") else 0
            salary_to = job_data.get("salary", {}).get("to", 0) if job_data.get("salary") else 0

            department = job_data.get("department")
            description = department.get("name", "Описание не указано") if department else "Описание не указано"

            vacancy = Vacancy(name=name, url=url, salary_from=salary_from, salary_to=salary_to, description=description)
            vacancies.append(vacancy)
        return vacancies

    def to_dict(self):
        """Конвертирует объект Vacancy в словарь"""
        return {
            "name": self.name,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "description": self.description,
        }
