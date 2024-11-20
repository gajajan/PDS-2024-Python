import multiprocessing
from multiprocessing import Process, Queue

def producer(conn,q):
    q.put("Queue Message")
    conn.send("Pipe Message")
    conn.close()

def consumer(conn,q):
    msg = q.get()
    print(msg)
    msg = conn.recv()
    print(msg)
    conn.close()

def process_run():
    q = multiprocessing.Queue()
    conn1, conn2 = multiprocessing.Pipe()

    p1 = Process(target=producer, args=(conn1,q,))
    p2 = Process(target=consumer, args=(conn2,q,))
    p1.start()
    p2.start()

if __name__ == "__main__":
    process_run()