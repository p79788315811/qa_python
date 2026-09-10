import pytest

class TestBooksCollector:
    # Тесты для метода add_new_book
    def test_add_new_book_add_one_book(self, collector):
        collector.add_new_book("Книга")
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book("Первая книга")
        collector.add_new_book("Вторая книга")
        assert len(collector.get_books_genre()) == 2

    # Тесты для метода set_book_genre
    def test_set_book_genre_valid(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        assert collector.get_book_genre("Книга") == "Фантастика"

    def test_set_book_genre_nonexistent_book(self, collector):
        collector.set_book_genre("Неизвестная книга", "Фантастика")
        assert collector.get_book_genre("Неизвестная книга") is None

    # Тесты для метода get_list_of_favorites_books
    def test_get_list_of_favorites_books_empty(self, collector):
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_not_empty(self, collector):
        collector.add_new_book("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")
        assert collector.get_list_of_favorites_books() == ["Любимая книга"]

    # Тесты для метода get_books_with_specific_genre
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Книга А")
        collector.set_book_genre("Книга А", "Фантастика")
        collector.add_new_book("Книга Б")
        collector.set_book_genre("Книга Б", "Фантастика")
        result = collector.get_books_with_specific_genre("Фантастика")
        assert set(result) == {"Книга А", "Книга Б"}

    # Тесты для метода get_books_for_children
    def test_get_books_for_children_excludes_adult_genres(self, collector):
        collector.add_new_book("Мульт про зайца")
        collector.set_book_genre("Мульт про зайца", "Мультфильмы")
        collector.add_new_book("Страшная история")
        collector.set_book_genre("Страшная история", "Ужасы")
        collector.add_new_book("Детективная загадка")
        collector.set_book_genre("Детективная загадка", "Детективы")
        children_books = collector.get_books_for_children()
        assert "Мульт про зайца" in children_books
        assert "Страшная история" not in children_books
        assert "Детективная загадка" not in children_books

    # Тесты для метода get_books_genre
    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book("Книга 1")
        result = collector.get_books_genre()
        assert isinstance(result, dict)
        assert result is collector.books_genre
