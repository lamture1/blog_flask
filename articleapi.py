import json
import sqlite3
from flask import Flask,g,request,jsonify
from datetime import datetime
from flask_basicauth import BasicAuth

class Authentication(BasicAuth):
    def check_credentials(self,username, password):
        cursor = get_db().cursor().execute("SELECT USER_ID,PASSWORD FROM AUTHORS WHERE USER_ID =?",(username,))
        data = cursor.fetchall()
        if len(data) > 0:
            if data[0][0] == username and data[0][1] == password:
                return True
        return False

app=Flask(__name__)
basic_auth = Authentication(app)
Database='blogdb.db'

def get_db():
    db=getattr(g,'_database',None)
    if db is None:
        db=g._database=sqlite3.connect(Database)
        print("Database instance created.")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db=getattr(g,'_database',None)
    if db is not None:
        db.close()

@app.route('/Article',methods=['POST'])
@basic_auth.required
def addarticle():
    success:bool=False
    cur=get_db().cursor()
    try:
        req_data=request.get_json()
        uid=request.authorization['username']
        #artid=req_data['artid']
        title=req_data['title']
        content=req_data['content']
        #print(uid+title+content)
        cur.execute("INSERT INTO ARTICLES (USER_ID,TITLE,DATE_CREATED,LAST_MODIFIED,CONTENT) VALUES (?,?,?,?,?)",(uid,title,datetime.now(),datetime.now(),content,))
        #cur.execute("SELECT * FROM ARTICLES WHERE USER_ID=?",(uid,))
        rec=cur.fetchall()
        print(rec)
        get_db().commit()
        success=True
    except:
        get_db().rollback()
        print("Error")
        success=False
    finally:
        if success:
            return jsonify(message="Passed"), 201
        else:
            return jsonify(message="Fail"), 409

# @app.route('/Article',methods=['GET'])
# def retrarticle():
#     success:bool=False
#     cur=get_db().cursor()
#     message = ""
#     try:
#         req_data=request.get_json()
#         artid=req_data['artid']
#         cur.execute("SELECT * FROM ARTICLES WHERE ARTICLE_ID=?",(artid,))
#         rec=cur.fetchall()
#         s=jsonify(rec)
#         message = s
#         get_db().commit()
#         success=True
#     except:
#         get_db().rollback()
#         print("Error")
#         success=False
#     finally:
#         if success:
#             return message, 200
#         else:
#             return jsonify(message = " Fail "), 409

@app.route('/Article',methods=['PATCH'])
@basic_auth.required
def updatearticle():
    success:bool=False
    cur=get_db().cursor()
    message = ""
    try:
        req_data=request.get_json()
        artid=req_data['artid']
        title=req_data['title']
        content=req_data['content']
        uid = request.authorization['username']
        cur.execute("SELECT USER_ID FROM ARTICLES WHERE ARTICLE_ID=?",(artid))
        results = cur.fetchall()
        if results[0][0] == uid:
            cur.execute("UPDATE ARTICLES SET TITLE=?, CONTENT=?, LAST_MODIFIED=? WHERE ARTICLE_ID=?",(title,content,datetime.now(),artid,))
            cur.execute("SELECT * FROM ARTICLES WHERE ARTICLE_ID=?",(artid,))
            rec=cur.fetchall()
            print(rec)
            s=jsonify(rec)
            message = s
            success=True
        get_db().commit()
    except:
        get_db().rollback()
        print("Error")
        success=False
    finally:
        if success:
            return message, 200
        else:
            return jsonify(message="Fail"), 409

@app.route('/Article',methods=['DELETE'])
@basic_auth.required
def delarticle():
    success:bool=False
    cur=get_db().cursor()
    try:
        req_data=request.get_json()
        artid=req_data['artid']
        uid = request.authorization['username']
        cur.execute("SELECT USER_ID FROM ARTICLES WHERE ARTICLE_ID=?",(artid,))
        results_user = cur.fetchall()
        print(results_user[0][0])
        if results_user[0][0] == uid:
            cur.execute("DELETE FROM ARTICLES WHERE ARTICLE_ID=?",(artid,))
            success=True
        get_db().commit()
    except:
        get_db().rollback()
        print("Error")
        success=False
    finally:
        if success:
            return jsonify(message="Passed"), 200
        else:
            return jsonify(message="Fail"), 409

@app.route('/Article',methods=['GET'])
def retrnmeta():
    success:bool=False
    cur=get_db().cursor()
    message = ""
    try:
        req_data=request.get_json()
        n=req_data['n']
        cur.execute('''SELECT ARTICLES.ARTICLE_ID,USER_ID,TITLE,DATE_CREATED,LAST_MODIFIED,TOTALCMNT FROM
        (SELECT ARTICLE_ID,COUNT(*) AS TOTALCMNT FROM COMMENTS WHERE ARTICLE_ID IN
        (SELECT ARTICLE_ID FROM ARTICLES ORDER BY LAST_MODIFIED DESC LIMIT ?)
        GROUP BY ARTICLE_ID) VW JOIN ARTICLES ON ARTICLES.ARTICLE_ID=VW.ARTICLE_ID''',(n,))
        rec=cur.fetchall()
        s=jsonify(rec)
        message = s
        get_db().commit()
        success=True
    except:
        get_db().rollback()
        print("Error")
        success=False
    finally:
        if success:
            return message, 200
        else:
            return jsonify(message = " Fail"), 409

# @app.route('/Article',methods=['GET'])
# def retrncontent():
#     success:bool=False
#     cur=get_db().cursor()
#     try:
#         req_data=request.get_json()
#         n=req_data['n']
#         n=int(n)
#         list1=[0]*1
#         # print(n)
#         # print(list1)
#
#         cur.execute("SELECT * FROM ARTICLES ORDER BY LAST_MODIFIED DESC LIMIT ?",(n,))
#         first=cur.fetchall()
#         #print(first)
#         first=list(first)
#         list1[0]=first
#
#         cur.execute('''SELECT ART.ARTICLE_ID AS ID,USER_ID,CONTENT FROM (
#                     SELECT ARTICLE_ID FROM ARTICLES ORDER BY LAST_MODIFIED DESC LIMIT ?) ART
#                     INNER JOIN COMMENTS ON ART.ARTICLE_ID=COMMENTS.ARTICLE_ID ORDER BY ID DESC''',(n,))
#         second=cur.fetchall()
#         #print(second)
#         second=list(second)
#         list1.append(second)
#
#         cur.execute('''SELECT B.ID,TAG_NAME FROM (
#                     SELECT ART.ARTICLE_ID AS ID,TAG_ID FROM (
#                     SELECT ARTICLE_ID FROM ARTICLES ORDER BY LAST_MODIFIED DESC LIMIT ?
#                     ) ART INNER JOIN ARTICLE_TAG ON ART.ARTICLE_ID=ARTICLE_TAG.ARTICLE_ID
#                     ) B INNER JOIN TAGS ON B.TAG_ID=TAGS.TAG_ID ORDER BY B.ID DESC''',(n,))
#         third=cur.fetchall()
#         #print(third)
#         third=list(third)
#         list1.append(third)
#
#         print("---------------------------------")
#         list1=list(list1)
#         print(list1)
#         print("---------------------------------")
#
#         # cur.execute("SELECT ARTICLE_ID FROM ARTICLES ORDER BY LAST_MODIFIED DESC LIMIT ?",(n,))
#         # artid=cur.fetchall()
#         # artidlist=[0]*1
#         # print(n)
#         # for i in range(n):
#         #     artidlist.extend(artid[i])
#         # del artidlist[0]
#         # print(artidlist)
#
#         s=jsonify(list1)
#         get_db().commit()
#         success=True
#     except:
#         get_db().rollback()
#         print("Error")
#         success=False
#     finally:
#         if success:
#             return s, 200
#         else:
#             return jsonify(message="Fail"), 409


if __name__=="__main__":
    app.run(debug=True)
