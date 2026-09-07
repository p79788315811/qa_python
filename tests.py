import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    """Создает свежий экземпляр BooksCollector для каждого теста"""
    return BooksCollector()


class TestAddNewBook:
    """Тесты метода add_new_book"""

    @pytest.mark.parametrize("name", [
        "Книга",
        "Короткая книга",
        "Название ровно 40 символов!!!!!!!!!!!!!!"  # 40 символов
    ])
    def test_add_valid_books(self, collector, name):
        collector.add_new_book(name)
        assert name in collector.books_genre
        assert collector.books_genre[name] == ""  # Жанр пустой после добавления

    @pytest.mark.parametrize("name", [
        "",  # Пустая строка
        "Слишком длинное название, которое точно больше сорока символов, потому что тут много букв",  # >40 символов
        "   ",  # Только пробелы (длина > 0, но невалидное)
    ])
    def test_add_invalid_names_rejected(self, collector, name):
        collector.add_new_book(name)
        assert name not in collector.books_genre

    def test_no_duplicates(self, collector):
        name = "Уникальная книга"
        collector.add_new_book(name)
        collector.add_new_book(name)  # Попытка добавить повторно
        # Книга должна быть только одна
        assert len(collector.books_genre) == 1
        assert list(collector.books_genre.keys()).count(name) == 1


class TestSetBookGenre:
    """Тесты метода set_book_genre"""

    @pytest.mark.parametrize("book_name, genre", [
        ("Книга 1", "Фантастика"),
        ("Книга 2", "Мультфильмы"),
        ("Книга 3", "Комедии"),
    ])
    def test_set_valid_genre(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    def test_set_genre_for_nonexistent_book(self, collector):
        # Пытаемся установить жанр для книги, которой нет
        collector.set_book_genre("Неизвестная книга", "Фантастика")
        assert "Неизвестная книга" not in collector.books_genre

    def test_set_invalid_genre_ignored(self, collector):
        book_name = "Книга"
        collector.add_new_book(book_name)
        # "Фэнтези" нет в списке разрешенных жанров (genre), поэтому не должно примениться
        collector.set_book_genre(book_name, "Фэнтези")
        assert collector.get_book_genre(book_name) != "Фэнтези"
        assert collector.get_book_genre(book_name) == ""


class TestGetBookGenre:
    """Тесты метода get_book_genre"""

    def test_get_existing_genre(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Детективы")
        assert collector.get_book_genre("Книга") == "Детективы"

    def test_get_missing_book_returns_none(self, collector):
        assert collector.get_book_genre("Отсутствует") is None


class TestFavorites:
    """Тесты методов работы с избранным"""

    def test_add_to_favorites(self, collector):
        collector.add_new_book("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")
        assert "Любимая книга" in collector.get_list_of_favorites_books()

    def test_no_duplicates_in_favorites(self, collector):
        collector.add_new_book("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")  # Повторный вызов
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_delete_from_favorites(self, collector):
        collector.add_new_book("Книга X")
        collector.add_book_in_favorites("Книга X")
        collector.delete_book_from_favorites("Книга X")
        assert "Книга X" not in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_get_empty_favorites_list(self, collector):
        assert collector.get_list_of_favorites_books() == []


class TestFiltering:
    """Тесты методов фильтрации книг"""

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Книга А")
        collector.set_book_genre("Книга А", "Фантастика")

        collector.add_new_book("Книга Б")
        collector.set_book_genre("Книга Б", "Фантастика")

        result = collector.get_books_with_specific_genre("Фантастика")
        assert set(result) == {"Книга А", "Книга Б"}

    def test_get_books_for_children_excludes_adult_genres(self, collector):
        # Книги для детей
        collector.add_new_book("Мульт про зайца")
        collector.set_book_genre("Мульт про зайца", "Мультфильмы")

        # Книги НЕ для детей (есть в genre_age_rating)
        collector.add_new_book("Страшная история")
        collector.set_book_genre("Страшная история", "Ужасы")

        collector.add_new_book("Детективная загадка")
        collector.set_book_genre("Детективная загадка", "Детективы")

        children_books = collector.get_books_for_children()

        assert "Мульт про зайца" in children_books
        assert "Страшная история" not in children_books
        assert "Детективная загадка" not in children_books

    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book("Книга 1")
        result = collector.get_books_genre()
        assert isinstance(result, dict)
        # Возвращается тот же самый объект словаря
        assert result is collector.books_genre
