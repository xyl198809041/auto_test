import asyncio
import time


# Python 协程属于可等待对象，因此可以在其他协程中被等待 Python异步非阻塞雏形
async def nested():
    time.sleep(2)
    # await asyncio.sleep(2)
    print('我是异步内的任务，我已经完成了')
    return 45


async def main():
    print(time.strftime('%X'))
    start_time = time.time()
    task = asyncio.create_task(nested())  # 使用task去执行协程，就可以达到异步的效果，我们任务在这里是已经开启了协程，只是结果在其他位置等待。因此这个代码预期就是异步的。
    # await nested() # 这种调用会等待协程完成之后在继续向下执行，也就是协程会阻塞在这里，常用于同步协程
    # await task # 它会等待任务完成返回后 往下执行，如果在Python中想完成异步非阻塞 就需要先开启任务，然后执行其他操作，在某个地方等待task完成后返回 并退出
    print('我会不会先出现...')
    print('耗时：', time.time() - start_time)
    # nested()
    # print(await nested())
    # await task # 类似与线程的join方法，不同的时，这个放的位置决定着谁先执行，例如我们放到程序最后，将看到协程是最后才执行，await的意思可以看作是等待协程的结果。
    # a = await task  # 等待的主要目的就是为了获取协程的结果
    # print(a)
    # 注意这里的时间，和多线程类似的，当多线程没有join时，主线程会马上结束但是不会杀死子线程。这里也是一样，如果不等待协程的结果，主程序结束后不会杀死协程，协程将继续执行完毕
    print(time.strftime('%X'))


asyncio.run(main())
time.sleep(3)
