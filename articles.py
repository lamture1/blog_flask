import sqlite3
from flask import Flask,request;
app = Flask(__name__)

@app.route('/Article', methods=['POST'])
def add_user():
    if request.method == 'POST':
        print("In the post")
        try:
            uid = request.form['uid']
            pwd = request.form['pwd']
            fname = request.form['fname']
            lname = request.form['lname']
            timestamp = request.form['timestamp']
            with sqlite3.connect("test.db") as con:
                con.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)",(uid,pwd,fname,lname,timestamp))
                con.commit()
                msg = "Record successfully added"
                print(msg)
        except:
            con.rollback()
            msg = "error in insert operation"
            print(msg)
        finally:
            return "connection closed"
            con.close()
if __name__ == "__main__":
    app.run()
