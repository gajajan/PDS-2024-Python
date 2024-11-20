import threading, time

event = threading.Event()

# První vlákno bude čekat než je podmínka splněna
def wait_function():
    print("Vlákno 1 čeká na splnění podmínky.")
    event.wait()
    print("Vlákno 1 obdrželo signál o splnění podmínky.")

# Druhé vlákno chvíly pracuje a následně nastaví event na True
def signal_function():
    time.sleep(2)
    event.set()
    print("Vlákno 2 splnilo podmínku.")

def thread_run():
    thread1 = threading.Thread(target=wait_function)
    thread2 = threading.Thread(target=signal_function)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    print("Vlákna dokončila práci.")

thread_run()