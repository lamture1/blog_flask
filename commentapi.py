import sqlite3
from flask import Flask,request,g,jsonify
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
    db=getattr(g, '_database',None)
    if db is None:
        db = g._database = sqlite3.connect(Database)
        print("Database instance created.")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db=getattr(g,'_database',None)
    if db is not None:
        db.close()

@app.route('/Comment',methods=['POST'])
def newcmnt():
    success:bool = False
    cur=get_db().cursor()
    try:
        req_data=request.get_json()
        artid=req_data['artid']
        uid=""
        pwd=""
        if request.headers.get('authorization') is not None:
            uid=request.authorization["username"]
            pwd=request.authorization["password"]
        cmnt=req_data['cmnt']
        cur.execute("SELECT USER_ID,PASSWORD FROM AUTHORS WHERE USER_ID =?",(uid,))
        results = cur.fetchall()
        print(str(results) + "results printed")
        if(len(results) > 0):
            if results[0][1] == pwd:
                cur.execute("INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (?,?,?,?)",(artid,uid,datetime.now(),cmnt))
            else:
                cur.execute("INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (?,?,?,?)",(artid,"Anonymous Coward",datetime.now(),cmnt))
        else:
            cur.execute("INSERT INTO COMMENTS (ARTICLE_ID,USER_ID,DATE_CREATED,CONTENT) VALUES (?,?,?,?)",(artid,"Anonymous Coward",datetime.now(),cmnt))
        get_db().commit()
        success=True
    except:
        get_db().rollback()
        success=False
    finally:
        if success:
            return jsonify(message="Passed"), 201
        else:
            return jsonify(message="Fail"), 409

@app.route('/Comment',methods=['DELETE'])
@basic_auth.required
def delcmnt():
    success:bool=False
    cur=get_db().cursor()
    try:
        req_data=request.get_json()
        cmntid=req_data['cmntid']
        uid=request.authorization['username']
        cur.execute("SELECT * FROM COMMENTS WHERE COMMENT_ID=?",(cmntid,))
        rec=cur.fetchall()
        if rec[0][2]==uid:
            cur.execute("DELETE FROM COMMENTS WHERE COMMENT_ID=?",(rec[0][0],))
            success=True
        get_db().commit()
    except:
        get_db().rollback()
        success=False
    finally:
        if success:
            return jsonify(message="Passed"), 200
        else:
            return jsonify(message="Fail"), 409

@app.route('/Comment',methods=['GET'])
def countcmnt():
    success:bool=False
    message = ""
    cur=get_db().cursor()
    try:
        req_data=request.get_json()
        artid=req_data['artid']
        cur.execute('SELECT COUNT(*) FROM COMMENTS WHERE ARTICLE_ID=?',(artid,))
        rec=cur.fetchall()
        message = rec[0][0]
        get_db().commit()
        success=True
    except:
        get_db().rollback()
        success=False
    finally:
        if success:
            return jsonify(message), 200
        else:
            return jsonify(message="Fail"), 409

# @app.route('/Comment',methods=['GET'])
# def retcmnt():
#     success:bool=False
#     message=""
#     cur=get_db().cursor()
#     try:
#         req_data=request.get_json()
#         artid=req_data['artid']
#         n=req_data['n']
#         cur.execute('SELECT CONTENT FROM COMMENTS WHERE ARTICLE_ID=? ORDER BY DATE_CREATED DESC LIMIT ?',(artid,n,))
#         rec=cur.fetchall()
#         message = rec
#         print(rec)
#         get_db().commit()
#         success=True
#     except:
#         get_db().rollback()
#         success=False
#     finally:
#         if success:
#             return jsonify(message), 200
#         else:
#             return jsonify(message="Fail"), 409


if __name__=="__main__":
    app.run(debug=True)
