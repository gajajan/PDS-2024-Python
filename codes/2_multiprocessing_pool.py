from multiprocessing import Pool

# Funkce pro výpočet mocniny dvěma
def do_something(x):
    return x * x

# Vytvoříme pool, kterému předáme kolekci dat a funkci kterou paralelně provede na všechny prvky
def pool_run():
    data = [1,2,3,4,5]
    pool = Pool(processes=4)

    result = pool.map(do_something, data)
    print(result)

if __name__ == "__main__":
    pool_run()