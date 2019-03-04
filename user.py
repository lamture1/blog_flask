import sqlite3
from flask import Flask,request,g,jsonify
from datetime import datetime
app = Flask(__name__)

DATABASE = 'blogdb.db'

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
    success:bool = False
    cur = get_db().cursor()
    try:
        uid = request.form['uid']
        pwd = request.form['pwd']
        fname = request.form['fname']
        lname = request.form['lname']
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
def deleteuser():
    success:bool = False
    cur = get_db().cursor()
    try:
        uid = request.form['uid']
        pwd = request.form['pwd']
        cur.execute("SELECT PASSWORD FROM AUTHORS WHERE USER_ID =?",(uid,))
        passwords = cur.fetchall()
        if passwords[0][0] == pwd:
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
def updateuser():
    success:bool = False
    cur = get_db().cursor()
    try:
        uid = request.form['uid']
        opwd = request.form['opwd']
        npwd = request.form['npwd']
        cur.execute("SELECT PASSWORD FROM AUTHORS WHERE USER_ID = ?",(uid,))
        passwords = cur.fetchall()
        print(passwords)
        if passwords[0][0] == opwd:
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
    app.run()
