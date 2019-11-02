#!/usr/bin/python3

import cgi
from datetime import datetime
import time

time_fmt = "%Y-%m-%d %H:%M:%S"
req_time = datetime.now().strftime(time_fmt)
time.sleep(10)
res_time = datetime.now().strftime(time_fmt)

print("Content-Type: text/plain")
print()   
print(f"[{req_time}] ...zzz\n[{res_time}] Good morning, world...")
