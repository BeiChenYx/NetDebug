"""
asyncio 绑定回调
在task执行完成的时候可以获取执行的结果，回调的最后
一个参数是future对象，通过该对象可以获取协程返回值
"""
import time
import asyncio

now = lambda: time.time()

async def do_some_work(x):
    print('waiting: ', x)
    return "Done after %s" % x

def callback(future):
    print('callback: ', future.result())

start = now()
coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
print(task)

# 添加回调函数
task.add_done_callback(callback)
print(task)

loop.run_until_complete(task)

print('Time: ', now() - start)

"""
通过add_done_callback方法给task任务添加回调
函数，当task执行完成的时候就会调用回到函数。
并通过参数future获取协程执行结果. 这里我们
创建的task和回调里的future对象实际是同一个
对象.
"""
