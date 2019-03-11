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

# @app.route('/Tag',methods=['POST'])
# @basic_auth.required
# def addtag():
#     success:bool=False
#     cur=get_db().cursor()
#     try:
#         req_data=request.get_json()
#         tag=req_data['tag']
#         cur.execute("INSERT INTO TAGS (TAG_NAME) VALUES (?)",(tag,))
#         get_db().commit()
#         success=True
#     except:
#         get_db().rollback()
#         success=False
#     finally:
#         if success:
#             return jsonify(message="Passed"), 201
#         else:
#             return jsonify(message="Fail"), 409

@app.route('/Tag',methods=['POST'])
@basic_auth.required
def connectag():
    success:bool=False
    cur=get_db().cursor()
    try:
        req_data=request.get_json()
        tag=req_data['tag']
        artid=req_data['artid']
        cur.execute("SELECT TAG_ID FROM TAGS WHERE TAG_NAME=?",(tag,))
        rec=cur.fetchall()
        rowsaffected=len(rec) #changed here because it was not getting row count because its already been fetched
        # print(rowsaffected) #prints -1 if 0 rows affected
        if rowsaffected == -1:
            #print(rec)
            cur.execute("INSERT INTO TAGS (TAG_NAME) VALUES (?)",(tag,))
            cur.execute("SELECT TAG_ID FROM TAGS WHERE TAG_NAME=?",(tag,))
            rec2=cur.fetchall()
            tid=rec2[0][0]
            #print(rec2)
            cur.execute("INSERT INTO ARTICLE_TAG VALUES (?,?)",(artid,tid,))
            success=True
        else:
            tid=rec[0][0]
            cur.execute("INSERT INTO ARTICLE_TAG VALUES (?,?)",(artid,tid,))
            success=True
        get_db().commit()

    except:
        get_db().rollback()
        success=False
    finally:
        if success:
            return jsonify(message="Data successfully inserted"), 201
        else:
            return jsonify(message="failed to insert data"), 409

@app.route('/Tag',methods=['DELETE'])
@basic_auth.required
def getarticle():
    success:bool=False
    cur=get_db().cursor()
    try:
        req_data=request.get_json()
        artid= req_data['artid']
        tags:[]=req_data['tag']
        for tag in tags:
            print("in for loop" + str(artid))
            cur.execute("DELETE FROM ARTICLE_TAG WHERE ARTICLE_ID=? AND TAG_ID IN (SELECT TAG_ID FROM TAGS WHERE TAG_NAME=?)",(artid,str(tag),))
        get_db().commit()
        success=True
    except:
        get_db().rollback()
        success=False
    finally:
        if success:
            return jsonify(message="Data successfully deleted"), 200
        else:
            return jsonify(message="failed to delete data"), 409

# @app.route('/Tag',methods=['GET'])
# def gettag():
#     success:bool=False
#     cur=get_db().cursor()
#     try:
#         req_data=request.get_json()
#         artid=req_data['artid']
#         cur.execute("SELECT * FROM TAGS WHERE TAG_ID IN (SELECT TAG_ID FROM ARTICLE_TAG WHERE ARTICLE_ID=?)",(artid,))
#         rec=cur.fetchall()
#         print(rec)
#         s=jsonify(rec)
#         print(s)
#         get_db().commit()
#         success=True
#     except:
#         get_db().rollback()
#         success=False
#     finally:
#         if success:
#             return s, 200
#         else:
#             return jsonify(message="failed to fetch data"), 409

# @app.route('/Tag',methods=['GET'])
# def getart():
#     success:bool=False
#     cur=get_db().cursor()
#     s = ""
#     try:
#         req_data=request.get_json()
#         tag=req_data['tag']
#         print(tag)
#         cur.execute("SELECT ARTICLE_ID FROM ARTICLE_TAG WHERE TAG_ID IN (SELECT TAG_ID FROM TAGS WHERE TAG_NAME=?)",(tag,))
#         rec=cur.fetchall()
#         s = jsonify(rec)
#         get_db().commit()
#         success=True
#     except:
#         get_db().rollback()
#         success=False
#     finally:
#         if success:
#             return s, 200
#         else:
#             return jsonify(message="failed to fetch data"), 409


if __name__=="__main__":
    app.run(debug = True)
