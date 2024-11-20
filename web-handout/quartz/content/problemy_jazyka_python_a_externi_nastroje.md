---
title: Problémy jazyka Python a externí nástroje
---

## Problémy jazyka Python
- Účelem paralelizace je maximalizovat použití výpočetních zdrojů, nejde tím ale Python trochu naproti?
	- Python je znám pro svou **nevýkonnost**
	    - dynamický jazyk - spoustu režie za běhu programu (GC, typová kontrola...)
	- **Omezení GIL** - jedno vlákno na jeden proces (dnes již volitelný)
    - použití více vláken pro výpočet náročné na CPU nepřináší žádné výrazné zrychlení (pokud nějaké)
- Vlákna mají v Pythonu ale stále využití, pokud čekají často na externí události (čtení/zápis, databáze, obsluha klienta...)
	- Framework **asyncio**
		- poskytuje základ pro tvorbu a správu síťové komunikace, webové servery, práci s databází, fronty
	- **aiohttp**
		- knihovna založená na _asyncio_ používaná pro asynchronní HTTP požadavky

### Řešení výkonnosti a paralelizace v Pythonu
- Existuje řada přístupů, jak obejít omezení GIL a celkově zrychlit výpočet

#### Použití knihovny _multiprocessing_
- Před verzí CPython 3.13 se dalo opravdové paralelizace dosáhnout pouze vytvářením nových procesů
- Tvorba a správa procesů však je obecně dražší a náročnější (nesdílejí paměť) než u vláken

#### Použití jiných implementací Pythonu
- Existují jiné implementace Pythonu, které se mírně odchylují od standardní implementace (CPython)
- Některé implementují techniky, které mohou běh programu za jistých okolností zrychlit

##### JIT kompilace
- Dynamicky kompiluje často používané části kódu do strojového kódu, který se za běhu programu dále optimalizuje
- Výhodné obzvláště pro dlouhotrvající procesy
- Příklady:
	- **Numba** - optimalizován pro **číselné operace**
	    - využívá NumPy a jeho struktur
	    - není potřeba v kódu provádět žádné výrazné změny
	    - příslušně označený kód se zkompiluje do strojového kódu, rychlost pak může být porovnatelný s kódem psaný v C či C++
		- nejvíce při práci s čísly, poli a NumPy funkcemi
		- možnost paralelizace operací, které nevyžadují Python interpret 
			- (nepřestupují ke specifickým objektům Pythonu)
	- **PyPy** (Python in Python)
	- **Jyphon** - implementace v Javě - bez GIL
	    - překlad do mezikódu, který je následně vykonáván v JVM
	    - možné integrovat kód v Pythonu do aplikací v Javě
	- IronPython - obdoba Jyphon pro .NET - bez GIL
	    - CLR
	    
- Příklad Numba

```python
# Převzato z https://numba.readthedocs.io/en/stable/user/5minguide.html

from numba import jit
import numpy as np

# Posloupnost 0...99 je převedena na tvar matice 10x10 [[0...9], [10...19]...[90...99]]
x = np.arange(100).reshape(10, 10)

# Pouhé přidání dekorátoru "@numba.jit" při jeho prvním zavolání zajistí kompilaci funkce do strojového kódu
@jit
def go_fast(a):
    trace = 0.0
    for i in range(a.shape[0]):
		trace += np.tanh(a[i, i])  # Použití funkcí NumPy
    return a + trace               # Přičtení "trace" ke každému prvku matice
print(go_fast(x))


@jit(nopython=True, parallel=True) 
def parallel_sum(arr): 
	total = 0 
	for i in prange(len(arr)):  # speciální konstrukt umožňující paralelní vykonání
		total += arr[i] 
	return total
```

#### Statická kompilace do nižšího jazyka
- Kompilace kódu v Python do sdílené knihovny v C nebo C++ (v podobě `'.so'` nebo ` .dll`), který lze přímo volat v Pythonu
- Příklady jsou: Cyphon, mypyc...
	- rozšiřují syntaxi o typové notace, které umožňují optimalizaci kompilovaného kódu
- **Cyphon**
	- umožňuje také volat funkce existujících knihoven C/C++
	- V souboru `.pyx` zapisujeme kód v Pythonu, které se následně zkompiluje do C/C++

```python
# Explicitní typování
cdef int x = 10

# Použití funkce z externí knihovny C
cdef extern from "math.h":
	double sqrt(double x)

def calc_square_root(double x):
	return sqrt(x)

# Paralelizace bez GIL
from cython.parallel import prange
def parallel_sum(int n):
	cdef int i, total = 0
	with nogil:
		for i in prange(n, nogil=True):
			total += i return total
```

- **MyPyc**
  - využívá statické typování MyPy

```python
# mathlib.py
def multiply(x: int, y: int) -> int:
    return x * y

# příkazem "mypyc --strict mathlib.py" se vytvoří "C extension", který lze v Pythonu importotvat jako běžný modul

# main.py
import mathlib as m
print(m.add(4, 20)) 

```

#### Externí knihovny psané v nízkoúrovňových jazycích
- Především v C a C++
- Optimalizované pro úlohy náročné na procesor
	- především zpracovávání velkých číselných dat
- Python pak slouží spíše jako jakási řídící vrstva, která deleguje náročné výpočty externím modulům implementovaných v nižších jazycích
- Zpracování v jiném jazyce nejsou limitovány GIL
#### Nepoužívat Python
- Požadujeme-li aplikace náročný výpočet na procesoru, měli bychom spíše zvolit jiný jazyk


### Externí nástroje využívající paralelizaci
- Existují knihovny, které ke složitým výpočtům na velkých datech využívají paralelizaci
#### Dask
- Knihovna navržena pro **paralelizaci při zpracovávání velkých dat**, ale i pro **distribuované výpočty** (clustery)
- Umožňuje pracovat s daty, které překračují velikost dostupné paměti - "_out-of-core computing_"
- Vlastnosti:
	- **Plánování úloh (_tasks_)**
		- úlohu rozděluje do menších částí a sestavuje graf závislostí, podle kterého se následně řídí výpočet
		- X -> Y -> Z
		- Y -> W
		- Před vykonáním Z musí být vykonán Y, přičemž W může běžet souběžně se Z
	- Správa **grafu úloh**
		- Dask před samotným výpočtem provádí analýzu a optimalizaci grafu
	- **Líné vyhodnocování**
		- výpočet není výkonán ihned, ale je vložen do grafu úloh
- Vykonávání plánovaných úloh lze realizovat pomocí:
	- **ThreadedScheduler**
		- využívá vláken v Pythonu pro paralelní vykonávání úloh
		- vhodný pro úlohy čekající na I/O
	- **MultiprocessingScheduler**
		- pro parelelní běh jsou vyhrazeny samostatné procesy
	- **DistributedScheduler**
		- vykonávání napříč stroji či clustery
- Využívá knihoven jako NumPy, Pandas či jiných pro rychlejší nízkoúrovňové výpočty

```python
import dask.array as dusky

# Naivní příklad paralelizace...

# Vytvoří matici 10000x10000, ta je rozdělena na části 1000x1000 (chunks), které se zpracují nezávisle na sobě
x = dusky.random.random((10000, 10000), chunks=(1000, 1000))
y = x + x.T

result = y.sum().compute()
```

```python

# Líné vyhodnocování, odkladání výpočtu

@dask.delayed
def inc(x):
   return x + 1

@dask.delayed
def add(x, y):
   return x + y

a = inc(1)       # nic nevykoná
b = inc(2)       # nic nevykoná
c = add(a, b)    # nic nevykoná

c = c.compute()  # Vykoná všechny výpočty výše
```

#### Další...
- Ray, Celery
