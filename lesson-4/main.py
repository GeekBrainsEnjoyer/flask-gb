import requests
from threading import Thread
import asyncio
import aiohttp
import aiofiles
import time
from multiprocessing import Process
import argparse

urls = ['https://i.pinimg.com/originals/59/54/b4/5954b408c66525ad932faa693a647e3f.jpg',
        'https://i.pinimg.com/564x/6f/0c/7d/6f0c7dd236a49fef3d2c7ad9def7f87c.jpg',
        'https://i.pinimg.com/564x/dc/92/1e/dc921ec2e07f9437dc51f2a10694578d.jpg',
        'https://i.pinimg.com/564x/e1/dc/6e/e1dc6e2bfdc03bb824e4304e7cb13354.jpg',
        'https://i.pinimg.com/564x/aa/ee/b7/aaeeb7276ffe0509e396512a62badbd9.jpg']


def download_sync(url, method_name=''):
    response = requests.get(url).content
    filename = url.split('/')[-1]
    with open(f'{method_name}_{filename}', 'wb') as img:
        img.write(response)
        print(
            f"{method_name} Downloaded ...{url[18:]} in {time.time()-start_time:.2f} seconds")


async def download_async(url, method_name=''):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            filename = url.split('/')[-1]
            async with aiofiles.open(f'{method_name}_{filename}', 'wb') as img:
                await img.write(await response.read())
                print(
                    f"{method_name} Downloaded ...{url[18:]} in {time.time()-start_time:.2f} seconds")

threads = []
processes = []
start_time = time.time()


async def main(urls):
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_async(url, 'asunc'))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter urls.')
    parser.add_argument('urls', nargs='*', type=str, default=urls)
    arg = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(arg.urls))

    for url in arg.urls:
        process = Process(target=download_sync, args=(url, 'process', ))
        processes.append(process)
        process.start()

    for url in arg.urls:
        thread = Thread(target=download_sync, args=[url, 'thread'])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    for process in processes:
        process.join()
