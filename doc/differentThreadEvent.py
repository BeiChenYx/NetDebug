"""
asyncio 不同线程的事件循环
很多时候，我们的事件循环用于注册协程，而有的
协程需要动态的添加到事件循环中。
一个简单的方式就是使用多线程。当前线程创建一个
事件循环，然后在新建一个线程，在新建线程中启动
事件循环，当前线程就不会阻塞;
"""
import asyncio
import time
from threading import Thread


now = lambda : time.time()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def more_work(x):
    print('More work {}'.format(x))
    time.sleep(x)
    print("Finished more work {}".format(x))

start = now()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop, ))
t.start()

new_loop.call_soon_threadsafe(more_work, 6)
new_loop.call_soon_threadsafe(more_work, 3)
print('TIME: {}'.format(time.time() - start))
time.sleep(10)
new_loop.close()
print('close loop')

"""
启动上述代码后，当前线程不会被阻塞, 新线程中会按照顺序
执行call_soon_threadsafe方法注册的more_work方法，后者
因为time.sleep()操作是同步阻塞的，因此运行完毕more_work
需要大致6 + 3 秒
"""



