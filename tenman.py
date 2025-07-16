import threading
import requests

def fetch_url(url, index):
    response = requests.get(url)
    print(f"Thread {index}: Status code {response.status_code}")

urls = [
    "https://httpbin.org/delay/10",  # Simulates a 2-second delay
    "https://httpbin.org/delay/10",
    "https://httpbin.org/delay/10",
    "https://httpbin.org/delay/10",
]

threads = []

for i, url in enumerate(urls):
    t = threading.Thread(target=fetch_url, args=(url, i))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("All API calls completed.")











import asyncio
import httpx

async def fetch_url(url, index):
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url)
        print(f"Task {index}: Status code {response.status_code}")

async def main():
    urls = [
        "https://httpbin.org/delay/10",
        "https://httpbin.org/delay/10",
        "https://httpbin.org/delay/10",
        "https://httpbin.org/delay/10",
    ]
    tasks = [fetch_url(url, i) for i, url in enumerate(urls)]
    await asyncio.gather(*tasks)


asyncio.run(main())








import asyncio
import time

async def worker(name, delay):
    print(f"{name} started at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(f"{name} finished at {time.strftime('%X')} after {delay}s")

async def main():
    tasks = []
    for i in range(5):
        # Each worker waits for i+1 seconds
        tasks.append(asyncio.create_task(worker(f"Worker-{i+1}", i+1)))
    await asyncio.gather(*tasks)


print("Program start.")
asyncio.run(main())
print("Program done.")