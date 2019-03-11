import  sqlite3

conn=sqlite3.connect('blogdb.db')

c=conn.cursor()

c.execute('''INSERT INTO AUTHORS VALUES ('anonymouscoward','ac','Anonymous','Coward',datetime('now')''')
c.execute('''INSERT INTO AUTHORS VALUES ('tirth1','qwerty','Tirth','Shah',datetime('now'))''')
c.execute('''INSERT INTO AUTHORS VALUES ('jainam1','asdfg','Jainam','Mehta',datetime('now'))''')
c.execute('''INSERT INTO AUTHORS VALUES ('kishore1','zxcvb','Kishore','Lamture',datetime('now'))''')

c.execute('''INSERT INTO ARTICLES (USER_ID,TITLE,DATE_CREATED,LAST_MODIFIED,CONTENT) VALUES ('tirth1','First article',datetime('now'),datetime('now'),'Hello all.! This is my first Article.')''')
c.execute('''INSERT INTO ARTICLES (USER_ID,TITLE,DATE_CREATED,LAST_MODIFIED,CONTENT) VALUES ('jainam1','First article',datetime('now'),datetime('now'),'Hello all.! This is my first Article.')''')
c.execute('''INSERT INTO ARTICLES (USER_ID,TITLE,DATE_CREATED,LAST_MODIFIED,CONTENT) VALUES ('tirth1','CSUF article',datetime('now'),datetime('now'),'I study Back-end engineering at CSUF.')''')

c.execute('''INSERT INTO TAGS (TAG_NAME) VALUES ('csuf')''')
c.execute('''INSERT INTO TAGS (TAG_NAME) VALUES ('first')''')
c.execute('''INSERT INTO TAGS (TAG_NAME) VALUES ('class')''')
c.execute('''INSERT INTO TAGS (TAG_NAME) VALUES ('start')''')
c.execute('''INSERT INTO TAGS (TAG_NAME) VALUES ('project')''')

c.execute('''INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (1,'kishore1',datetime('now'),'GO!')''')
c.execute('''INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (1,'tirth1',datetime('now'),'Thanks!')''')
c.execute('''INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (2,'kishore1',datetime('now'),'Keep it up')''')
c.execute('''INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (3,'kishore1',datetime('now'),'GOOD LUCK!')''')
c.execute('''INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (3,'jainam1',datetime('now'),'WOW!')''')
c.execute('''INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (2,'tirth1',datetime('now'),'Welcome!')''')

c.execute('''INSERT INTO ARTICLE_TAG VALUES (1,2)''')
c.execute('''INSERT INTO ARTICLE_TAG VALUES (1,4)''')
c.execute('''INSERT INTO ARTICLE_TAG VALUES (2,2)''')
c.execute('''INSERT INTO ARTICLE_TAG VALUES (2,4)''')
c.execute('''INSERT INTO ARTICLE_TAG VALUES (3,1)''')
c.execute('''INSERT INTO ARTICLE_TAG VALUES (3,3)''')
c.execute('''INSERT INTO ARTICLE_TAG VALUES (3,5)''')


conn.commit()

conn.close()
