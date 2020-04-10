from contextlib import closing
import sqlite3

db_file = '/app/db/database.db'

with closing(sqlite3.connect(db_file)) as conn:
    c = conn.cursor()
    c.executescript("""
      CREATE TABLE users(
        username,
        password,
        firstname,
        lastname,
        age
      );

      INSERT INTO users VALUES(
        'taro',
        'aaaa',
        'Taro',
        'Yamada',
        20
      );

      INSERT INTO users VALUES(
        'jiro',
        'abcdefgh',
        'Jiro',
        'Yamada',
        18
      );

      INSERT INTO users VALUES(
        'hanako',
        '1234567890',
        'Hanako',
        'Chiba',
        25
      );
    """)

    conn.commit()
