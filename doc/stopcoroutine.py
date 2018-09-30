"""
asyncio 协程的停止
future 对象有几个状态:

    * Pending
    * Running
    * Done
    * Cancelled
创建future的时候，task为pending, 事件循环调用执行
的时候当然就是running, 调用完毕就是done, 如果需要
停止事件循环，就需要先把task取消.
可以使用asyncio.Task获取事件循环的task
"""
import asyncio
import time


now = lambda : time.time()

async def do_some_work(x):
    print("waiting: ", x)
    await asyncio.sleep(x)
    return "Done after {}s".format(x)


coroutine1 = do_some_work(1)
coroutine2 = do_some_work(2)
coroutine3 = do_some_work(3)

tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3),
]

start = now()

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt as e:
    print(asyncio.Task.all_tasks())
    for task in asyncio.Task.all_tasks():
        print(task.cancel())
    loop.stop()
    loop.run_forever()
finally:
    loop.close()

print("Time: ", now() - start)

"""
loop stop 之后还需要再次开启事件循环，最后在close
不然还会抛出异常.
循环task, 逐个cancel是一种方案，可是正如前面我们把
task的列表封装在main函数中，main函数外进行事件循环
的调用，这个时候，main相当于最外出的一个task, 那么
处理包装的main函数即可。
"""
