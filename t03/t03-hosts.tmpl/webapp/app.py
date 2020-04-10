from datetime import datetime
import time

from flask import Flask

app = Flask(__name__)

@app.route('/sleepy', methods=['GET'])
def response_after_sleep():
    time_fmt = "%Y-%m-%d %H:%M:%S"
    req_time = datetime.now().strftime(time_fmt)
    time.sleep(10)
    res_time = datetime.now().strftime(time_fmt)
    return f"[{req_time}] ...zzz\n[{res_time}] Good morning, world..."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, threaded=False, debug=True)
