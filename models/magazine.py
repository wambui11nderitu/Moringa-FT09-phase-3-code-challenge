from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = id
        self._name = name
        self._category = category
        if id is None and name is not None and category is not None:
            self._create_in_db()

    def _create_in_db(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        self._id = cursor.lastrowid
        connection.commit()
        connection.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value
        self._update_db('name', value)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value
        self._update_db('category', value)

    def _update_db(self, field, value):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f'UPDATE magazines SET {field} = ? WHERE id = ?', (value, self._id))
        connection.commit()
        connection.close()

    def articles(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT a.id, a.title FROM articles a
            JOIN magazines m ON a.magazine_id = m.id
            WHERE m.id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    def contributors(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT au.id, au.name FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
        ''', (self._id,))
        contributors = cursor.fetchall()
        connection.close()
        return contributors

    def article_titles(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        titles = [row['title'] for row in cursor.fetchall()]
        connection.close()
        return titles if titles else None

    def contributing_authors(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT au.id, au.name FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
            GROUP BY au.id
            HAVING COUNT(a.id) > 2
        ''', (self._id,))
        authors = cursor.fetchall()
        connection.close()
        return authors if authors else None

    def __repr__(self):
        return f'<Magazine {self.name}>'

