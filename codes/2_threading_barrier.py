import threading, time

# Vytvoříme bariéru, určíme kolik vláken k ní musí dojít, než je propustí.
barrier = threading.Barrier(3)

# Vlákno vykonává práci a následně čeká než tu stejnou práci nedokončí ostatní vlákna.
# Pak vlákna pokračují vykonáváním další práce.
def thread_function(thread_id):
    print("Vlákno {} vykonává 1. fázi".format(thread_id))
    time.sleep(2)

    print("Vlákno {} čeká u bariéry.".format(thread_id))
    barrier.wait()

    print("Vlákno {} vykonává 2. fázi".format(thread_id))
    time.sleep(2)

def thread_run():
    threads = []
    for i in range(3):
        thread = threading.Thread(target=thread_function, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Všechna vlákna dokončila práci.")

thread_run()