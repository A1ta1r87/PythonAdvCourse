import time
import random
import asyncio
import aiohttp

URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


async def fetch_async(session, pid):
    start = time.time()
    sleepy_time = random.randint(2, 10)
    print('Fetch async process {} started, sleeping for {} seconds'.format(
        pid, sleepy_time))

    await asyncio.sleep(sleepy_time)

    async with session.get(URL) as response:
        datetime = response.headers.get('Date')

    response.close()
    return 'Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start)


async def asynchronous():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        futures = [fetch_async(session, i) for i in range(1, MAX_CLIENTS + 1)]

        for i, future in enumerate(asyncio.as_completed(futures)):
            result = await future
            print('{} {}'.format(">>" * (i + 1), result))

    print("Process took: {:.2f} seconds".format(time.time() - start))


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()