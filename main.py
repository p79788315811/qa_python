class BooksCollector:
    def __init__(self):

        self.books_genre = {}  # словарь: книга -> жанр
        self.favorites = []     # список избранных книг

    def add_new_book(self, name):

        if (not self.books_genre.get(name)
                and 0 < len(name) < 41
                and name.strip()):
            self.books_genre[name] = ''

    def set_book_genre(self, book_name, genre):

        if book_name in self.books_genre:
            self.books_genre[book_name] = genre

    def get_book_genre(self, book_name):

        return self.books_genre.get(book_name)

    def get_books_with_specific_genre(self, genre):

        books = []
        for book, book_genre in self.books_genre.items():
            if book_genre == genre:
                books.append(book)
        return books

    def add_book_in_favorites(self, book_name):

        if book_name in self.books_genre and book_name not in self.favorites:
            self.favorites.append(book_name)

    def delete_book_from_favorites(self, book_name):

        if book_name in self.favorites:
            self.favorites.remove(book_name)

    def get_list_of_favorites_books(self):

        return self.favorites

    def get_books_for_children(self):

        adult_genres = {'Ужасы', 'Детективы'}
        children_books = []

        for book, genre in self.books_genre.items():
            if genre not in adult_genres:
                children_books.append(book)

        return children_books

    def get_books_genre(self):

        return self.books_genre

    def get_books_rating(self):

        return self.books_genre
