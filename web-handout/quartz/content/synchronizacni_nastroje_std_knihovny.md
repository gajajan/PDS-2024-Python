---
title: Synchronizační nástroje standardní knihovny Pythonu
---

Python, stejně jako ostatní programovací jazyky, nabízí ve své standardní knihovně řadu nástrojů pro synchronizaci mezi procesy a vlákny, což usnadňuje psaní paralelního kódu. Knihovna obsahuje dva základní moduly pro paralelizaci:
* `threading`: pro paralelizaci pomocí vláken.
* `multiprocessing`: pro pravý paralelizmus pomocí procesů.

Moduly obsahují různé nástroje pro synchronizaci jako jsou zámky, semafory, bariéry nebo mechanizmy pro sdílená data, což umožňuje vývojářům bezpečné spuštění paralelního kódu.

# Modul Threading

Tento modul umožňuje vytvářet a spravovat jednoduchá vlákna v rámci jednoho procesu. Práce s vlákny má nízkou režii, takže jsou vhodná především pro operace, které často čekají na dokončení vstupně-výstupních úloh. Vzato jsou ale omezena Global Interpreter Lockem. GIL umožňuje, aby v daném okamžiku mohlo být vykonáváno pouze jedno vlákno, i když běží na vícejádrovém procesoru. Tohle omezení braní pravému paralelismu, což znamená, že vlákna nejsou vhodná pro výpočetně náročné úlohy.

Vlákna jsou tedy vhodná pro operace, kde závisí na rychlosti I/O operací:
* Čtení/zápis do souboru.
* Síťové požadavky.
* Grafické uživatelské rozhraní.

Vlákna z modulu `threading` sdílí paměť v rámci jednoho procesu, což umožňuje snadnou komunikaci mezi nimi, ale zároveň se můžeme lehce dopustit chyby, při manipulaci se sdílenými daty.

Abychom mohli pracovat s vlákny, musíme nejdřív modul importovat.
```python
import threading
```
### Klíčové koncepty

#### Třída Thread
Úplným základem pro práci s vlákny je třída Thread. Každá instance této třídy reprezentuje jedno vlákno. Vlákno vykoná konkrétní funkce, kterou mu předáme při jeho vytvoření, spolu se předanými argumenty.
Vlákno se spouští metodou `.start()` a může běžet paralelně s hlavním programem.  
Pokud je potřeba, aby hlavní proces počkal na dokončení vlákna, lze využít metody `.join()`.

```python
t = threading.Thread(target=some_function, args=(some_arg,))
t.start()
# Nějaký kód
t.join()
```

Další užitečné funkce:
* `is_alive()` - vrací True, pokud je vlákno stále aktivní. Pokud skončilo, vrací False.
* `getName()` - vrací název vlákna.
* `setName()` -  můžeme změnit název vlákna.
* `local()` - pro ukládání hodnot specifických pro konkrétní vlákna.
#### Třída Lock
Zámek je synchronizační mechanismus, který brání souběžnému přístupu více vláken ke sdíleným zdrojům. Zajišťuje, že v daný okamžik může ke sdíleným prostředkům přistupovat pouze jedno vlákno, čímž zabraňuje možným konfliktům.
Funkce `acquire()` se používá pro zamčení určitého bloku kódu. Pokud se jiné vlákno bude snažit dostat k zámku, zablokuje se, dokud nebude zámek uvolněn. 
Funkce `release()` se využívá pro odemčení zámku. 
V Pythonu je možnost využít příkazu `with`, který automaticky obalí kód těmito funkcemi, což zvyšuje čitelnost a jednoduchost kódu.

```python
lock = threading.Lock()

def function():
	# Nějaký kód
	with lock:  
	    # Další kód
```

**Varianta RLock:**
RLock řeší situace, kdy vlákno, které už drží zámek, potřebuje tento zámek získat znovu. To je užitečné především v rekurzivních funkcích využívající zámek, nebo při použití více zamykacích operací ve stejném vlákně.

```python
lock = threading.RLock()
def recursive_function():
	with lock:
		# Nějaký kód
		recursive_function()
```

#### Třída Semaphore
Semafor je synchronizační nástroj, který umožňuje řídit přístup k omezenému počtu sdílených zdrojů. Na rozdíl od zámku, který povoluje přístup pouze jednomu vláknu, semafor umožňuje přístup více vláknům současně. 
Semafor si udržuje interní počítadlo `count`, které určuje počet vláken, které mohou přistoupit ke zdroji. Při inicializaci semaforu se zadává maximální hodnota tohoto počítadla.
Funkce `acquire()`, zjistí jestli hodnota `count` je 0. Pokud ano, vlákno se zablokuje, pokud ne, `count` se dekrementuje. 
Funkce `release()` inkrementuje počítadlo. 
Stejně jako u zámku lze využít příkazu `with`.

```python
sem = threading.Semaphore(limit)

def function():
	# Nějaký kód
	with sem:
		# kritická sekce
```

#### Třída Barrier
Bariéra se může využít tehdy, kdy je potřeba, aby všechna vlákna dosáhla určitého místa v programu předtím, než budou pokračovat. To znamená, že vlákna budou čekat na ostatní, dokud všechna nedosáhnou bariéry. Bariéry jsou vhodné, pokud vlákna pracují ve fázích. Program tedy čeká, až všechna vlákna dokončí jednu fázi, a teprve poté se může pokračovat do fáze další.
Při vytváření bariéry se nastavuje počet vláken, na které se bude čekat. 
Funkce `wait()` zajistí, že vlákno bude zablokováno, dokud stanovený počet vláken nedosáhne bariéry.

```python
barrier = threading.Barrier(limit)

def function():
	# Nějaký kód
	barrier.wait()
	# Další kód
```

#### Třída Event
Event je jednoduchý mechanizmus, který umožňuje vláknům spolu komunikovat. Event obsahuje interní příznak, který může nabývat hodnot `True` nebo `False`. Ostatní vlákna tak mohou čekat, až bude příznak nastaven, předtím než budou pokračovat v činnosti. Jinak řečeno, vlákna čekají než je konkrétní podmínka splněna.

Pro práci s Eventem používají tyto funkce:
* `set()` pro nastavení příznaku na `True`.
* `clear()` pro resetování příznaku na `False`.
* `wait()` zablokuje vlákno dokud není hodnota příznaku `True`.

Je zde i možnost předat funkci `wait()` argument `timeout`, který umožňuje specifikovat maximální dobu. Pokud nebude příznak v tomto časovém limitu nastaven, metoda `wait()` se ukončí.

```python
event = threading.Event()

def function1():
	# Nějaký kód
	event.wait()
	# Další kód kód

def function2():
	# Nějaký kód
	event.set()
	# Další kód kód
```

#### Třída Condition
Na závěr máme nástroj `Condition`, který funguje obdobně jako `Event` s menšími rozdíly. Třída je propojena se synchronizačním nástrojem `Lock`, který je s každou instancí implicitně spojen. Tento zámek funguje stejně jako ten ze třídy `Lock`.

Pro práci s Condition používáme funkce:
* `wait()` zablokuje vlákno dokud není splněna podmínka, nebo nevyprší čas předaný v argumentu `timeout`.
* `notify()` pro odblokování jednoho čekajícího vlákna.
* `notify_all()` pro odblokování všech čekajících vláken.

```python
cond = threading.Condition()

def function1():
	with cond:
		# Nějaký kód
		cond.wait()
		# Další kód kód

def function2():
	with cond:
		# Nějaký kód
		cond.notify()
		# Další kód kód
```

## Modul Multiprocessing

Tento modul umožňuje využití pravého paralelismu vytvářením nezávislých procesů, každý s vlastním paměťovým prostorem. Na rozdíl od vláken z modulu `threading`, procesy nejsou omezeny limitacemi GIL. Procesy jsou vhodné především pro výpočetně náročnější úkoly, které mohou být spuštěny na více jádrech procesoru.

Výhodou nezávislosti procesů je, že jejich paměťové prostory jsou oddělené. To snižuje rizika spojená s prací se sdílenými prostředky, ale vzato zvyšuje nároky na paměť. Modul ale poskytuje mnoho nástrojů pro bezpečnou komunikaci a sdílení zdrojů.

### Klíčové koncepty

#### Třída Process

Úplným základem modulu multiprocessing je třída Process, jejíž instance reprezentuje samotný proces. Tvorba procesu probíhá úplně stejně jako tvorba vláken. Tedy při tvorbě předáme funkci, kterou proces vykoná, společně s předaným argumentem. Proces se následně spustí metodou `.start()`. Hlavní proces může počkat na dokončení práce pomocí metody `.join()`.

```python
from multiprocessing import Process

p = Process(target=some_function, args=(some_arg,))  
p.start()
# Nějaký kód
p.join()
```

Na procesy lze navíc volat metoda `.terminate()`, která vynutí ukončení běžícího procesu. Měla by se používat omezeně, jelikož může dojít k uvedení sdílených zdrojů do nekonzistentního stavu.

Užitečné atributy procesu:
* `name` - vrací jméno procesu, lze nastavit při jeho vytváření.
* `pid` - vrací id procesu, které přidělí operační systém.
* `daemon` - vrací příznak, jestli je proces nastaven jako daemon. Daemon proces běží na pozadí a je automaticky ukončen, pokud rodičovský proces skončí.
* `is_alive` - vrací příznak zda proces ještě pracuje.

#### Třída Pool

Tato třída umožňuje efektivní správu procesů. Automatizuje proces jejich vytváření a umožňuje rozdělení práce mezi různá jádra procesoru. Obvykle se používá při zpracování kolekcí dat, kde každému prvku kolekce přiřadí jeden proces, který na něj aplikuje určenou funkci. Výsledky jednotlivých procesů jsou následně zkombinovány do jednoho výstupu.

Při vytváření poolu musíme předat informaci o tom, kolik procesů se využije. Následně zavoláme funkci `.map()`, která aplikuje zadanou funkci na každý prvek z kolekce dat. Výsledek se uloží do proměnné.

```python
from multiprocessing import Process, Pool

# Řekneme Poolu s kolika procesy má pracovat
pool = Pool(processes=num_of_processes) 

result = pool.map(some_function, iterable_data)
```

#### Sdílení dat

Pro sdílení dat mezi procesy se používají objekty `Value` a `Array`. Tyto objekty umožňují bezpečnou správu sdílené paměti mezi procesy.
* `Value` reprezentuje jednu sdílenou proměnnou.
* `Array` reprezentuje pole sdílených dat.

Konstruktor těchto objektů požaduje datový typ (Např.: 'i' - integer, 'f' - float, 'c' - char) a hodnotu. Následně s objektem Array můžeme pracovat jako s polem a s value můžeme pracovat pomocí `.value`.

Je vhodné dále využít vhodných synchronizačních nástrojů pro práci se sdílenými proměnnými.

```python
from multiprocessing import Process, Value, Array

# Definice objektů
value = Value('i', init_value)  
result = Array('i', size)

# Funkce, která využívá objektů pro sdílení dat
def example_function(data,value,result):  
    for i, num in range(5):  
        result[i] = num * num  
        value.value += num
```

#### Komunikace mezi procesy

Meziprocesová komunikace je další způsob, jak si procesy mohou vyměňovat data a koordinovat činnosti. Modul `multiprocessing` pro komunikaci poskytuje dva základní objekty `Queue` a `Pipe`.
`Queue` je datová struktura typu *First-In-First-Out (FIFO)*, která umožňuje procesům bezpečně odesílat a přijímat data. Libovolné množství procesů může sdílet jednu frontu, což zajišťuje efektivní komunikaci mezi nimi. Práce s frontou je intuitivní – prvky se přidávají na konec a odebírají z čela. To odpovídá principu běžné fronty.

```python
from multiprocessing import Process, Queue

# Definice fronty
queue = Queue()

# Funkce, která posílá zprávu ostatním procesům
def producer(queue): 
	while True:
		queue.put("Message") 

# Funkce která čte zprávy od ostatních procesů
def consumer(queue): 
	while True:
		message = queue.get() 
```

`Pipe` poskytuje obousměrný komunikační kanál mezi dvěma procesy. Lze je využívat obousměrně nebo jen jednosměrně. Práce s nimi je jednoduchá, ale nelze využít pro více než dva procesy.

```python
from multiprocessing import Process, Pipe

# Definice Pipy
conn1, conn2 = multiprocessing.Pipe()

# Funkce, která pošle zprávu přes Pipe
def producer(conn1):
    conn.send("Pipe Message")  
    conn.close()

# Funkce, která získa zprávu přes Pipe
def consumer(conn2)
	msg = conn.recv()
	conn.close()

```

#### Synchronizace
Modul obsahuje stejné synchronizační nástroje jako modul `threading`. Tedy nástroje `Lock`, `Semaphore`, `Barrier`, `Event`, `Condition`. Tyto nástroje fungují stejně jako v modulu `threading`, takže je znovu nemusíme vysvětlovat. 

Při použití těchto nástrojů v kontextu modulu `multiprocessing` je však důležité mít na paměti, že pracují s procesy místo vláken. To znamená, že synchronizační primitiva musí být schopna fungovat mezi oddělenými procesy. Modul `multiprocessing` tuto izolaci zajišťuje pomocí mechanismů meziprocesové komunikace (IPC) pomocí:
- Sdílené paměti.
- Pipe a Queue.
- Souborů nebo socketů.

## Modul Asyncio

Tento modul poskytuje nástroje pro asynchronní programování v Pythonu. To umožňuje různým úkolům běžet nezávisle s možností mezi sebou přepínat, aby neblokovaly celý proces. Z toho důvodu je tento modul vhodný pro vstupně-výstupní operace jako čtení souborů, práce s databází nebo zpracování HTTP požadavků.

V Pythonu, na rozdíl od vláken a procesů, `asyncio` umožňuje vytvořit úkoly, které sdílí stejné vlákno, a přepínají se mez sebou bez blokování tohoto vlákna. Proto jsou vhodné pro I/O operace, jelikož nemusíme zbytečně čekat na jejich dokončení.

Abychom mohli pracovat s modulem, potřebujeme ho prvně importovat.
```python
import asyncio
```

### Klíčové koncepty

#### Event Loop
Základním konceptem modulu je událostní smyčka (Event Loop). Ta je zodpovědná za plánování, koordinaci a správu asynchronních úloh. V Pythonu se smyčkou nepracuje přímo, ale využívá se funkcí.
Ke spuštění se využívá funkce `.run()`, které se předá korutina.

```python
asnycio.run(main())
```

#### Coroutine
Korutina je speciální typ asynchronní funkce, kterou máme možnost zastavit a znovu ji spustit později. To je velmi důležité pro asynchronní programování, kde se korutiny mohou vzdávat činnosti.
Funkce se stane asynchronní pokud ji definujeme pomocí klíčového slova `async`. Korutina se může vzdát činnosti použitím klíčového slova `await`, což umožní dalším korutinám běh, mezitím co čekají na dokončení nějaké I/O operace.

```python
async def coroutine(): 
	do_something()
	# Simulace nějaké I/O operace, na kterou je potřeba počkat
	await asyncio.sleep(1) 

asyncio.run(coroutine())
```

#### Task
Úlohy umožňují obalit korutinu a naplánovat její běh v Event Loopu, a také umožňují spustit několik korutin paralelně. Úloha po spuštění běží na pozadí, a tak neblokují hlavní vlákno.
Během toho co se úloha vykonává ve smyčce, můžeme sledovat její postup, zjistit výsledky nebo odchytávat výjimky. Úlohu vytvoříme pomocí funkce `.create_task()`, které se předá korutina jako argument.

```python
task = asyncio.create_task(coroutine(arg))
await task
```

Mezitím co se úloha provádí, můžeme s ní pracovat pomocí různých vestavených metod. 
* `.result()` vrátí výsledek úlohy po tom co je dokončena.
* `.exception()` umožňuje odchytit výjimku, kterou korutina vyvolala. 
* `.cancel()` se pokusí zrušit vykonávání úlohy.

Pomocí funkce `asnycio.gather()` můžeme spustit několik úloh paralelně. Následně můžeme získat výsledky z jednotlivých úloh.

```python
results = await asyncio.gather(task1, task2)
# Nebo
results = await asyncio.gather(*tasks)
```

Dalším užitečným nástrojem je funkce `.wait_for()`, která umožňuje nastavit maximální čas čekání na dokončení nějaké I/O operace. Pokud při čekání na obsloužení nějaké I/O operace čekáme delší dobu, vyvolá se výjimka `TimeoutError`.

```python
# Korutina bude provádět čekání na dokončení operace déle než 3 sekundy
async def coroutine():
	await asnycio.sleep(5)

try: 
	# Nastavíme max dobu čekání 3 sekundy
	result = await asyncio.wait_for(coroutine(), timeout=3)
except asyncio.TimeoutError:
	print("Timeout.")
```

#### Synchronizace

Opět jako v modulu `threading` a `multiprocessing`, i modul `asyncio` poskytuje stejné synchronizační nástroje jako je zámek, semafor, nebo třeba i frontu. Je zde i možnost využít klíčového slova `async` společně s `with` pro bezpečnější kód.

```python
sem = asyncio.Semaphore()

async with sem:
	await asyncio.sleep(5)
```