from multiprocessing import Process
import time, random

def process_function(process_id):
    print("Proces {} začal práci.".format(process_id))
    time.sleep(random.randint(1, 5))
    print("Proces {} dokončil práci.".format(process_id))

def process_run():
    processes = []
    for i in range(5):
        p = Process(target=process_function, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    print("Všechny procesy dokončili práci")

if __name__ == "__main__":
    process_run()