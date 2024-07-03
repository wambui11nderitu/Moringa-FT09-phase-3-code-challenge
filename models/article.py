class Article:
    def __init__(self, article_id, title, content, author_id, magazine_id):
        self.id = article_id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def author(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
        author_data = cursor.fetchone()
        connection.close()
        return Author(author_data['id'], author_data['name']) if author_data else None

    def magazine(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
        magazine_data = cursor.fetchone()
        connection.close()
        return Magazine(magazine_data['id'], magazine_data['name'], magazine_data['category']) if magazine_data else None

    @staticmethod
    def get_articles_by_author(author_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (author_id,))
        articles_data = cursor.fetchall()
        connection.close()
        return [Article(data['id'], data['title'], data['content'], data['author_id'], data['magazine_id']) for data in articles_data]

    @staticmethod
    def get_articles_by_magazine(magazine_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (magazine_id,))
        articles_data = cursor.fetchall()
        connection.close()
        return [Article(data['id'], data['title'], data['content'], data['author_id'], data['magazine_id']) for data in articles_data]

# Make sure to define the get_db_connection() function to establish a database connection.
def get_db_connection():
    import sqlite3
    return sqlite3.connect('database.db')

class Author:
    def __init__(self, author_id, name):
        self._id = author_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def articles(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT a.id, a.title FROM articles a
            WHERE a.author_id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    @property
    def magazines(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT m.id, m.name FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        connection.close()
        return magazines

class Magazine:
    def __init__(self, magazine_id, name, category):
        self.id = magazine_id
        self.name = name
        self.category = category
