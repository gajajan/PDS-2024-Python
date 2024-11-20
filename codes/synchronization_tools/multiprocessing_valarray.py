from multiprocessing import Process, Value, Array

# Funkce vypočítá mocniny dvou v poli a udělá součet všech hodnot.
def process_function(data,sum,squares):
    for i, num in enumerate(data):
        squares[i] = num * num
        sum.value += squares[i]

def process_run():
    data = [1,2,3,4]

    # Vytvoříme objekty pro sdílení proměnných mezi procesy
    sum = Value('i', 0)
    squares = Array('i', 4)

    p = Process(target=process_function, args=(data,sum,squares,))
    p.start()

    p.join()
    print("Squares: {}".format(squares[:]))
    print("Sum: {}".format(sum.value))

if __name__ == "__main__":
    process_run()