from abc import ABC, abstractmethod

"""Абстрактный класс должен быть интерфейсом для всех платформ"""


class JobPlatformAPI(ABC):
    @abstractmethod
    def connect(self):
        """Метод для подключения к API платформы"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str, page: int = 1):
        """Метод для получения списка вакансий по поисковому запросу"""
        pass
