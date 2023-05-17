from threading import Thread, Lock
from time import sleep

l = Lock()

def ciapa():
    l.acquire()

    while l.locked():
        print("Ciao")
        sleep(2)

def ciapa2():
    l.release()
    l.acquire()

    while l.locked():
        print("hey")
        sleep(2)

t = Thread(target = ciapa)

t.start()

sleep(10)

t2 = Thread(target = ciapa2)

t2.start()

sleep(10)