"""
asyncio 定义一个协程

使用async关键字定义一个协程，
协程不能直接运行，需要将协程加入
到一个事件循环loop中;
asyncio.get_event_loop创建一个
事件循环，然后使用run_until_complete
将协程注册到事件循环中, 并启动事件
循环.
"""

import time
import asyncio

now = lambda : time.time()

async def do_some_work(x):
    """
    协程函数
    """
    print('waiting:', x)

start = now()

# 这里是一个协程对象，这个时候do_some_work函数并没有执行
coroutine = do_some_work(2)
print(corutine)

# 创建一个事件循环
loop = asyncio.get_event_loop()

# 将协程加入到事件循环中
loop.run_until_complete(coroutine)

print('Time: ', now() - start)

