import sqlite3

conn = sqlite3.connect('blogdb.db')

c=conn.cursor()

c.execute('''CREATE TABLE AUTHORS (
        USER_ID TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL,
        FNAME TEXT NOT NULL,
        LNAME TEXT,
        DATE NUMERIC NOT NULL
        )''')
print('Authors table created.')

c.execute('''CREATE TABLE ARTICLES (
        ARTICLE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        USER_ID TEXT NOT NULL,
        TITLE TEXT,
        DATE_CREATED NUMERIC NOT NULL,
        LAST_MODIFIED NUMERIC NOT NULL,
        CONTENT TEXT,
        FOREIGN KEY (USER_ID) REFERENCES AUTHORS(USER_ID) ON DELETE CASCADE
        )''')
print('Articles table created.')

c.execute('''CREATE TABLE COMMENTS (
        COMMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        ARTICLE_ID INTEGER NOT NULL REFERENCES ARTICLES(ARTICLE_ID) ON DELETE CASCADE,
        USER_ID TEXT NOT NULL REFERENCES AUTHORS(USER_ID),
        DATE_CREATED NUMERIC NOT NULL,
        CONTENT TEXT
        )''')
print('Comments table created.')

c.execute('''CREATE TABLE TAGS (
        TAG_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        TAG_NAME TEXT NOT NULL
        )''')
print('Tags table created.')

c.execute('''CREATE TABLE ARTICLE_TAG (
        ARTICLE_ID INTEGER NOT NULL REFERENCES ARTICLES(ARTICLE_ID) ON DELETE CASCADE,
        TAG_ID INTEGER NOT NULL REFERENCES TAGS(TAG_ID),
        PRIMARY KEY(ARTICLE_ID,TAG_ID)
        )''')
print('Article-Tag table created')

conn.commit()

conn.close()
