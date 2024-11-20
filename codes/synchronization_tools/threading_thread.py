import threading, time, random

# Vlákno pro práci. Uspíme na náhodný čas pro simulaci práce.
def thread_function(thread_id):
    print("Vlákno {} začalo práci.".format(thread_id))
    time.sleep(random.randint(1, 5))
    print("Vlákno {} dokončilo práci.".format(thread_id))

def thread_run():
    threads = []
    for thread_id in range(1, 5):
        thread = threading.Thread(target=thread_function, args=(thread_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Všechny vlákna dokončili práci.")

thread_run()