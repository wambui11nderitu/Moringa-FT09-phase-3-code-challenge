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

# Make sure to define the get_db_connection() function to establish a database connection.
def get_db_connection():
    import sqlite3
    return sqlite3.connect('database.db')
