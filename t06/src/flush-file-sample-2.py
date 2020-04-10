import time

f = open('out.txt', 'w')
while True:
    f.write('abcdefghijklmnopqrstuvwxyz')
    f.flush()
    time.sleep(1)
