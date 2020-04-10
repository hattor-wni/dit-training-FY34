from contextlib import closing
import sqlite3

from flask import Flask, jsonify, request

db_file = '/app/db/database.db'
app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def query_db(sql):
    with closing(sqlite3.connect(db_file)) as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(sql)
        response = c.fetchall()
        return response

@app.route('/', methods=['POST'])
def query():
    sql = request.form.get('sql', None)

    if sql is None:
        return jsonify([])
    else:
        return jsonify(query_db(sql))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, threaded=True, debug=True) # is this actually threadable?
