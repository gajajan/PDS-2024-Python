import threading, time

cond = threading.Condition()

# Konzumer bude čekat na splnění podmínky producenta
def consumer(id):
    with cond:
        cond.wait()
        print("Konzumer {} obdržel zprávu.".format(id))

# Producent udělá práci a oznámi dokončení některému z konzumentů
def producer():
    time.sleep(2)
    for i in range(5):
        with cond:
            print("Producent vyprodukoval zprávu.")
            cond.notify()
            time.sleep(2)

def thread_run():
    threads = []
    prod_thread = threading.Thread(target=producer)
    prod_thread.start()
    for i in range(5):
        cons_thread = threading.Thread(target=consumer, args=(i,))
        threads.append(cons_thread)
        cons_thread.start()

    prod_thread.join()
    for cons_thread in threads:
        cons_thread.join()
    print("Vlákna dokončila práci.")

thread_run()