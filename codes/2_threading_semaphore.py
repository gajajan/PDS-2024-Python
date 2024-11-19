import threading, time

# Vytvoříme semafor, určíme max počet přístupů.
sem = threading.Semaphore(3)

# Vlákno pro práci se zdrojem, zkontrolujeme semafor.
# Pokud může, přistoupí ke zdroji.
# Pokud ne, čeká.
def resource(thread_id):
    print("Vlákno {} čeká na přístup ke zdroji.".format(thread_id))
    with sem:
        print("Vlákno {} přístoupilo ke zdroji.".format(thread_id))
        time.sleep(2);

    print("Vlákno {} dokončilo práci se zdrojem.".format(thread_id))

def thread_run():
    threads = []
    for i in range(5):
        thread = threading.Thread(target=resource, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Všechna vlákna dokončila práci.")

thread_run()