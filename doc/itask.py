"""
asyncio 创建一个task
协程对象不能直接运行, 在注册事件
的时候，其实是run_until_complete
方法将协程包装成为一个任务(task)
对象，task对象是Future类的子类
保存了协程运行后的状态，用于未来
获取协程的结果.
"""
import time
import asyncio


now = lambda : time.time()

async def do_some_work(x):
    print('waiting: ', x)

start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = loop.create_task(coroutine)
print(task)

loop.run_until_complete(task)

print(task)
print("Time: ", now() - start)


"""
创建task后，在task加入事件循环之前为pending
状态，当完成后，状态为finished
关于上面通过loop.create_task(coroutine)创建
task,同样可以通过asyncio.ensure_future(coroutin)
创建task, 这个两个的区别在于create_task是在
Python 3.4.2中添加了，用来支持老的python版本
"""
