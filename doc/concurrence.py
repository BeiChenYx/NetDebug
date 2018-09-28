"""
asyncio 并发
"""
import asyncio
import time


now = lambda : time.time()

async def do_some_work(x):
    print('Waiting: ', x, '-', now())
    await asyncio.sleep(x)
    return "Done after %d" % x

start = now()

coroutine1 = do_some_work(1)
coroutine2 = do_some_work(2)
coroutine3 = do_some_work(4)

tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3),
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print('Task result: ', task.result())

print("Time: ", now() - start)

"""
总事件为4s左右，4s的阻塞事件，足够前面两个协程执行完毕。
如果是同步顺序的任务，那么至少要7s， 此时我们使用了
asyncio实现了并发。
asyncio.wait(tasks)也可以使用asyncio.gather(*tasks),
前者接受一个task列表, 后者接受一堆task, 两者具体区别:
asyncio.gather:
    Return a future aggregating results from the given 
coroutine objects or futures.

    All futures must share the same event loop. If all 
the tasks are done successfully, the returned future’s
result is the list of results (in the order of the 
original sequence, not necessarily the order of results 
arrival). If return_exceptions is true, exceptions in the 
tasks are treated the same as successful results, and 
gathered in the result list; otherwise, the first raised 
exception will be immediately propagated to the returned future.

asyncio.wait:
    Wait for the Futures and coroutine objects given by
the sequence futures to complete. Coroutines will be 
wrapped in Tasks. Returns two sets of Future: (done, pending).

    The sequence futures must not be empty.

    timeout can be used to control the maximum number of
seconds to wait before returning. timeout can be an int or
float. If timeout is not specified or None, there is no
limit to the wait time.

    return_when indicates when this function should return.
"""
