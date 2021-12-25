from unittest import result
import asyncio
import requests
import time
import aiohttp


def write_image(data):
    filename = f"image/cat-{time.monotonic()}.png"
    with open(filename,"wb") as file:
        file.write(data)



async def get_content(url,session):
    async with session.get(url = url) as responce:
        data = await responce.read()
        write_image(data)


async def main():
    url = "https://loremflickr.com/320/240"
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(11):
            task = asyncio.create_task(get_content(url,session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(time.time()-start)

