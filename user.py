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

app = Flask(__name__)

DATABASE = 'blogdb.db'
basic_auth = Authentication(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        print("database instance is created")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/User',methods=['POST'])
def adduser():
    print("In add user")
    success:bool = False
    cur = get_db().cursor()
    try:
        req_data = request.get_json()
        uid = req_data['uid']
        pwd = req_data['pwd']
        fname = req_data['fname']
        lname = req_data['lname']
        print(uid)
        cur.execute("INSERT INTO AUTHORS(USER_ID, PASSWORD, FNAME, LNAME, DATE) VALUES (?, ?, ?, ?, ?)",(uid,pwd,fname,lname,datetime.now()))
        get_db().commit()
        success = True
    except:
        get_db().rollback()
        success = False
    finally:
        if success:
            return jsonify(message="Passed"), 201
        else:
            return jsonify(message="Fail"), 409

@app.route('/User',methods=['DELETE'])
@basic_auth.required
def deleteuser():
    success:bool = False
    cur = get_db().cursor()
    try:
        uid = request.authorization["username"]
        pwd = request.authorization["password"]
        cur.execute("DELETE FROM AUTHORS WHERE USER_ID= ?",(uid,))
        cur.execute("UPDATE COMMENTS SET USER_ID='ANONYMOUS COWARD' WHERE USER_ID=?",(uid,))
        success = True
        get_db().commit()
    except:
        get_db().rollback()
        print("Error")
    finally:
        if success:
            return jsonify(message="Data successfully deleted"), 200
        else:
            return jsonify(message="failed to delete data"), 409

@app.route('/User',methods=['PATCH'])
@basic_auth.required
def updateuser():
    success:bool = False
    cur = get_db().cursor()
    req_data = request.get_json()
    try:
        uid = request.authorization["username"]
        opwd = request.authorization["password"]
        npwd = req_data['npwd']
        cur.execute("UPDATE AUTHORS SET PASSWORD=? WHERE USER_ID=?",(npwd,uid,))
        print("HURRAY")
        success = True
        get_db().commit()
    except:
        get_db().rollback()
        print("ERROR")
    finally:
        if success:
            return jsonify(message="Data successfully updated"), 200
        else:
            return jsonify(message="failed to update data"), 409

if __name__ == "__main__":
    app.run(debug=True)
