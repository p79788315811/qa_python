import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# 1. Добавление новой книги: валидное имя (до 40 символов), книга добавляется один раз
@pytest.mark.parametrize("name", [
    "Книга",
    # Используем гарантированно короткую строку, чтобы не зависеть от подсчёта символов
    "Короткая книга",
])
def test_add_new_book_valid(collector, name):
    collector.add_new_book(name)
    assert name in collector.books_genre
    assert collector.books_genre[name] == ""  # без жанра

    # Повторное добавление не должно дублировать
    collector.add_new_book(name)
    assert len([k for k in collector.books_genre.keys() if k == name]) == 1


# 2. Добавление книги: невалидные имена (пустая строка, слишком длинная строка)
@pytest.mark.parametrize("name", [
    "",
    "Эта строка точно длиннее сорока символов, потому что тут больше сорока знаков!!!",
])
def test_add_new_book_invalid(collector, name):
    collector.add_new_book(name)
    assert name not in collector.books_genre


# 3. Установка жанра: корректный жанр, книга есть в словаре
@pytest.mark.parametrize("name, genre", [
    ("Книга", "Фантастика"),
    ("Другая книга", "Комедии"),
])
def test_set_book_genre_valid(collector, name, genre):
    collector.add_new_book(name)
    collector.set_book_genre(name, genre)
    assert collector.get_book_genre(name) == genre


# 4. Установка жанра: некорректный жанр или книги нет в словаре
@pytest.mark.parametrize("name, genre, expected_unchanged", [
    ("Книга", "Неизвестный жанр", True),      # жанр не из списка
    ("Неизвестная книга", "Фантастика", True),  # книги нет в books_genre
])
def test_set_book_genre_invalid(collector, name, genre, expected_unchanged):
    if name != "Неизвестная книга":
        collector.add_new_book(name)

    collector.set_book_genre(name, genre)

    if name in collector.books_genre:
        current_genre = collector.get_book_genre(name)
        assert current_genre != genre or current_genre == ""
    else:
        assert name not in collector.books_genre


# 5. Получение жанра по имени: книга есть, книги нет
@pytest.mark.parametrize("name, expected_genre", [
    ("Книга", "Фантастика"),
    ("Отсутствует", None),
])
def test_get_book_genre(collector, name, expected_genre):
    if name == "Книга":
        collector.add_new_book(name)
        collector.set_book_genre(name, "Фантастика")

    assert collector.get_book_genre(name) == expected_genre


# 6. Список книг с конкретным жанром: есть книги этого жанра, нет книг этого жанра
@pytest.mark.parametrize("genre, books_to_add, expected_result", [
    ("Фантастика", ["Книга А", "Книга Б"], ["Книга А", "Книга Б"]),
    ("Ужасы", ["Книга В"], []),  # НЕ ставим жанр «Ужасы» — поэтому список пустой
])
def test_get_books_with_specific_genre(collector, genre, books_to_add, expected_result):
    for b in books_to_add:
        collector.add_new_book(b)
        # Устанавливаем жанр только для «Фантастика», чтобы проверить оба случая
        if genre == "Фантастика":
            collector.set_book_genre(b, genre)

    result = collector.get_books_with_specific_genre(genre)
    assert set(result) == set(expected_result)


# 7. Текущий словарь books_genre: проверяем, что возвращается именно он
def test_get_books_genre(collector):
    collector.add_new_book("Книга 1")
    collector.add_new_book("Книга 2")
    collector.set_book_genre("Книга 1", "Детективы")

    result = collector.get_books_genre()
    assert isinstance(result, dict)
    assert result is collector.books_genre  # это тот же самый объект


# 8. Книги для детей: исключаем жанры с возрастным рейтингом
def test_get_books_for_children(collector):
    collector.add_new_book("Детская книга")
    collector.add_new_book("Страшная книга")
    collector.set_book_genre("Детская книга", "Мультфильмы")
    collector.set_book_genre("Страшная книга", "Ужасы")

    children_books = collector.get_books_for_children()
    assert "Детская книга" in children_books
    assert "Страшная книга" not in children_books


# 9. Добавление в избранное: книга есть в books_genre, нельзя добавить дважды
@pytest.mark.parametrize("name, already_in_fav, expected_count", [
    ("Любимая книга", False, 1),
    ("Ещё одна любимая", True, 1),  # уже в избранном — количество не увеличится
])
def test_add_book_in_favorites(collector, name, already_in_fav, expected_count):
    collector.add_new_book(name)
    if already_in_fav:
        collector.add_book_in_favorites(name)

    collector.add_book_in_favorites(name)
    assert len(collector.favorites) == expected_count
    assert name in collector.favorites


# 10. Удаление из избранного и получение списка избранного
def test_delete_book_from_favorites_and_list(collector):
    collector.add_new_book("Книга X")
    collector.add_book_in_favorites("Книга X")

    assert "Книга X" in collector.get_list_of_favorites_books()

    collector.delete_book_from_favorites("Книга X")
    assert "Книга X" not in collector.get_list_of_favorites_books()
    assert len(collector.get_list_of_favorites_books()) == 0
