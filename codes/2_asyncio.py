import asyncio

# Definování korutiny
async def download_file(id):
    print("Stahuji soubor {}".format(id))
    # Simulace čekání na stažení nějakého souboru
    await asyncio.sleep(1)
    print("Soubor {} byl stažen.".format(id))

async def main():
    # Vytvoření více tasků
    tasks = []
    for i in range(5):
        tasks.append(asyncio.create_task(download_file(i)))
    await asyncio.gather(*tasks)

asyncio.run(main()) #hlavní Event-Loop