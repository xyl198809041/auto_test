import time
import asyncio
import threading
import types


async def aaa():
    print(1)
    await asyncio.sleep(1)
    print(2)
    return 1


async def f():
    return await aaa()


async def main():
    task = [asyncio.ensure_future(f()) for i in range(10)]
    task = [await t for t in task]
    return task


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # task=[f() for i in range(10)]
    # loop.run_until_complete(asyncio.wait(task))
    # loop.run_until_complete(f())

    # task = [f() for i in range(10)]
    asyncio.run(main())
    print(2)
