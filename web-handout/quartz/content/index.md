---
title: PDS 2024 - Python Web Handout
---

Vítejte na úvodní stránce handoutu, který vám poskytne základy a praktické ukázky pro pochopení paralelního programování a distribuovaných systémů s využitím jazyka Python. Tento materiál je rozdělen do několika tématických částí, které vás postupně provedou od teoretického úvodu až po pokročilejší použití externích nástrojů a technologií.

---

## Obsah

1. [Úvod do paralelizace v Pythonu](uvod_do_paralelizace.md)
   Základní pojmy, motivace a přehled konceptů paralelního výpočtu. Proč a kdy tyto přístupy používat?  

2. [Synchronizační nástroje standardní knihovny Pythonu](synchronizacni_nastroje_std_knihovny.md)
   Představení nástrojů jako **threading**, **multiprocessing** a dalších, které Python nabízí pro práci s paralelními úlohami. Jak zvládat synchronizaci a předcházet problémům?

3. [Problémy Pythonu a externí nástroje](problemy_jazyka_python_a_externi_nastroje.md)
   Omezení Pythonu při paralelním zpracování (GIL, výkon) a jak je řešit. Představení knihoven a nástrojů jako **Celery**, **Dask**, nebo **Ray**.

4. [Práce s RabbitMQ](rabbitmq.md)  
   Použití **RabbitMQ** pro realizaci distribuovaných úloh. Základy front zpráv, výhody použití a praktická implementace v Pythonu.

5. [Komunikace pomocí soketů a HTTP](socket_http.md)  
   Implementace komunikace mezi procesy nebo systémy pomocí soketů a protokolu HTTP. Základy práce se standardními knihovnami Pythonu pro tyto účely.

---

## Ukázkové kódy

Všechny ukázky uvedené v handoutu si můžete prohlédnout a spustit. Kódy jsou uspořádány ve složce `codes`, která je rozdělena podle kapitol:  

- **Kapitola 2:** [Synchronizační nástroje (`threading` a `multiprocessing`)](codes/synchronization_tools/)  
- **Kapitola 3:** [Ukázky s externími nástroji (`Dask`, `Celery`, `Ray`)](codes/external_tools/)  
- **Kapitola 4:** [RabbitMQ - Implementace front zpráv](codes/rabbitmq_examples/)  
- **Kapitola 5:** [Sokety a HTTP - Komunikace mezi procesy](codes/socket_http/)  

Každý adresář obsahuje README s krátkým popisem kódů a instrukce k jejich spuštění.

---

## Doporučení k práci s handoutem

Každá sekce obsahuje teoretický úvod i praktické ukázky, které si můžete vyzkoušet. Pro lepší pochopení doporučujeme pracovat s obsahem sekvenčně a zkoušet ukázkové kódy na vlastním počítači. Pokud narazíte na problém, doporučujeme se vrátit k teoretické části dané kapitoly.

---

## Další kroky

Začněte prvním tématem: [Úvod do paralelního programování a distribuovaných systémů](uvod_do_paralelizace.md). Pokud máte nějaké dotazy nebo problémy, neváhejte se obrátit na contributory [tohoto repozitáře](https://github.com/Tarasa24/PDS-2024-Python).
