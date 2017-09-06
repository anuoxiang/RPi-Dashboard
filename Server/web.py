from flask import Flask, abort, request
import sqlite3
import json
import redis
import time

con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS `main_table` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `hostname`	TEXT NOT NULL,
        `ip`	TEXT NOT NULL,
        `time`	NUMERIC NOT NULL
    );""")

app = Flask(__name__)


@app.route('/foo', methods=['POST'])
def foo():
    if not request.json:
        abort(400)
    print request.json
    
    cur.execute("""INSERT INTO main_table(hostname,ip,create_time) VALUES('%s', '%s', %d);"""
                % (request.json["hostname"], request.remote_addr, int(time.time())))
    
    return json.dumps(request.json)


@app.route('/Ref', methods=['GET'])
def ref():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
