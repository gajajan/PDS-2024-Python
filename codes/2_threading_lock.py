import threading

# Definice zámku a globální proměnné pro počítadlo.
lock = threading.Lock()
count = 0

# Vlákno pro čítač.
# Zamkneme blok kódu, který přistupuje ke sdlílené proměnné.
def counter():
    with lock:
        global count
        count = count + 1
        print(count)

def thread_run():
    threads = []
    for i in range(5):
        thread = threading.Thread(target=counter)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

thread_run()