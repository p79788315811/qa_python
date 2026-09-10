import pytest

from main import BooksCollector

@pytest.fixture
def collector():

    """Создает свежий экземпляр BooksCollector для каждого теста.
"""
    return BooksCollector()