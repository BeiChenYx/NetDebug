"""
asyncio 新线程协程
"""
import asyncio
import time
from threading import Thread


now = lambda : time.time()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def do_some_work(x):
    print('Waiting {}'.format(x))
    await asyncio.sleep(x)
    print('Done after {}s'.format(x))

def more_work(x):
    print('More work {}'.format(x))
    time.sleep(x)
    print('Finished more work {}'.format(x))

start = now()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()

asyncio.run_coroutine_threadsafe(do_some_work(6), new_loop)
asyncio.run_coroutine_threadsafe(do_some_work(4), new_loop)
print('TIME: {}'.format(time.time() - start))

"""
上述例子， 主线程中创建一个new_loop, 然后在另外的子线程中
开启一个无限事件循环。主线程通过run_coroutine_threadsafe
新注册协程对象。这样就能在子线程中进行事件循环的并发操作
同时主线程又不会被阻塞.
"""
