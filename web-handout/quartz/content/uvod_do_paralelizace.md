---
title: Úvod do paralelizace v Pythonu
---

## 1990: Počátky Pythonu a zaměření na jednoduchost
Python byl vytvořen [Guidem van Rossumem](https://en.wikipedia.org/wiki/Guido_van_Rossum) jako jazyk zaměřený na čitelnost a jednoduchost. První verze Pythonu z roku 1990 nepočítala s pokročilými nástroji pro paralelizaci, což bylo částečně dáno tím, že hardware v té době nebyl tak paralelizací posedlý jako dnes. Vývojáři se většinou spoléhali na jednovláknové aplikace, protože vícejádrové procesory a masivní paralelizace byly stále v plenkách. Tento důraz na jednoduchost ovlivnil mnoho rozhodnutí v návrhu Pythonu, včetně způsobu správy paměti, což se později stalo významným faktorem v omezení paralelizace.

## 2000: Zavedení GIL (Global Interpreter Lock)
Rok 2000 přinesl vydání Python [2.0](https://www.python.org/download/releases/2.0/), které zavedlo několik klíčových funkcí, včetně automatického *garbage collectoru* založeného na počítání referencí. Tento přístup přinesl výhody, jako je snadné sledování a uvolňování nevyužívaných objektů. Nicméně tento systém není přirozeně *thread-safe*, což znamená, že pokud by více vláken manipulovalo s referenčním počítadlem současně, mohlo by dojít k problémům, jako jsou race conditions, úniky paměti nebo chybná dealokace objektů.

Aby se tyto problémy vyřešily, vývojáři Pythonu implementovali **Global Interpreter Lock (GIL)**. Tento zámek zajišťuje, že v daném okamžiku může pouze jedno vlákno vykonávat Python kód v rámci interpretace. GIL chrání referenční počítání a další interní mechanismy Pythonu před konflikty mezi vlákny.

Přestože GIL zjednodušil návrh a umožnil stabilní provoz v prostředí s více vlákny, přišel za cenu omezené paralelizace. 
- **Efektivní paralelizace na úrovní vláken je nemožná**: Pouze jedno vlákno může aktivně vykonávat Python kód, i když je k dispozici více jader CPU. To znamená, že vlákna nezvyšují výkon při výpočetně náročných úlohách.
- **I/O-bound aplikace stále profilují**: GIL se uvolňuje při operacích, jako je čtení/zápis do souborů nebo sítě, což znamená, že více vláken může efektivně spravovat I/O-bound úlohy.

Zavedení GIL mělo dlouhodobé důsledky na to, jak je Python vnímán a používán. Nedávno *Rada pro řízení vývoje Pythonu (Python Steering Council)* oznámila svůj závěr schválit [PEP 703](https://peps.python.org/pep-0703/), návrh na vytvoření verze Pythonu bez GIL. Tento krok má velký vliv na budoucí vývoj Pythonu. Od verze [3.13](https://docs.python.org/3/whatsnew/3.13.html) je možné nainstalovat verzi Pythonu neobsahující GIL. Tato funkčnost ještě není dostupná v oficiálních verzích Pythonu a je potřeba ji doinstalovat:
```bash
apt install python3.13-full python3.13-nogil
```
Poté je možno spustit Python bez GILu:
```bash
PYTHON_GIL=0 python3.13-nogil test.py
```

## 2008: Přidání knihovny multiprocessing pro paralelizaci pomocí procesů
V roce 2008, s vydáním Pythonu [2.6](https://www.python.org/download/releases/2.6/) a [3.0](https://www.python.org/download/releases/3.0/), došlo k významnému kroku v možnosti paralelizace v Pythonu. Byl přidán modul `multiprocessing`. Tento krok měl zásadní význam, protože *obcházel* omezení GIL, který bránil efektivní paralelizaci na úrovni vláken.

Modul multiprocessing umožňuje programátorům vytvářet a spravovat samostatné procesy, které běží nezávisle na sobě, každý ve své vlastní paměťové oblasti. Na rozdíl od vláken, která sdílejí společnou paměť v rámci jednoho procesu, procesy běží ve svých vlastních prostorách a jsou vzájemně izolované. Tato izolace znamená, že každý proces si vytváří svůj vlastní *Python interpreter*, což znamená, že každý proces má vlastní GIL a vlastní prostor pro správu paměti. Tímto způsobem se vyhneme omezení GIL, které jinak brání paralelizaci na úrovni vláken. Každý proces může běžet na jiném CPU nebo jádru, což umožňuje efektivní využívání více jader procesoru a plně využít potenciál moderního vícejádrového hardwaru.

## Další důležitá data k paralelizaci Pythonu
- **2010 (Python [3.2](https://www.python.org/download/releases/3.2/))**: Python získal modul **concurrent.futures**, který poskytl jednodušší rozhraní pro práci s procesy a vlákny prostřednictvím **Executor API**. To umožnilo psát paralelní kód přehledněji a konzistentněji.
- **2018 (Python [3.7](https://www.python.org/downloads/release/python-370/))**: Modul **asyncio** byl stabilizován a stal se jedním z hlavních nástrojů pro asynchronní programování. Ačkoliv asyncio nespadá přímo pod paralelizaci, umožňuje efektivní správu vstupně-výstupních (I/O) operací, což je důležité pro moderní webové a síťové aplikace.