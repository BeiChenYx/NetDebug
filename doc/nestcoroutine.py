"""
asyncio 协程嵌套
使用async可以定义协程，协程用于耗时的IO操作,
也可以封装更多的IO操作过程，这样就实现了嵌套
的协程， 即一个协程中await了另外一个协程
如此连接起来.
"""
import asyncio
import time


now = lambda: time.time()

async def do_some_work(x):
    print('waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after %s' % x

async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3),
    ]

    dones, pendings = await asyncio.wait(tasks)
    for task in dones:
        print('Task result: ', task.result())

    # results = await asyncio.gather(*tasks)
    # for task in results:
        # print('Task result: ', result)

start = now()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print('Time: ', now() - start)


"""
# 不在main协程函数里处理结果，直接返回await的内容，
# 那么最外层的run_until_complete将会返回main协程的
# 结果, 代码如下:
async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3),
    ]

    return await asyncio.gather(*tasks)
    # return await asyncio.wait(tasks)

start = now()

loop = asyncio.get_event_loop()
results = loop.run_until_complete(main())
for result in results:
    print('Task result: ', result)

# done, pending = loop.run_until_complete(main())
# for task in done:
    # print('Task result: ', task.result())

print('Time: ', now() - start)
"""

"""
# 也可以使用asyncio的as_completed方法
async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3),
    ]
    for task in asyncio.as_completed(tasks):
        result = await task
        print("Task result: {}".formart(result))
"""

# 从上面可以看出， 协程的调用和组合非常灵活，
# 主要提现在对于结果的处理， 如何返回，如何挂起
