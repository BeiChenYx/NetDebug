"""
asyncio 阻塞 await
使用async可以定义协程对象，使用await可以针对
耗时的操作进行挂起，就像生成器里的yield一样，
函数让出控制权。协程遇到await，事件循环将会
挂起该协程，执行别的协程，直到其他的协程也
挂起或执行完毕，再进行下一个协程的执行.

耗时的操作一般都是一些IO操作，例如网络请求,
文件读取等， 我们使用asyncio.sleep函数来模拟
IO操作，协程的目的也是让这些IO操作异步化.
"""
import asyncio
import time

now = lambda : time.time()

async def do_some_work(x):
    print('waiting: ', x)
    # await 后面就是调用耗时的操作
    await asyncio.sleep(x)
    return "Done after %s" % x

start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

print("Task result: ", task.result())
print("Time: ", now() - start)


"""
在await asyncio.sleep(x), 因为这里sleep了，模拟了
阻塞或者耗时操作，这个时候就会让出控制权. 即当遇到
阻塞调用的函数的时候，使用await方法将协程的控制权
让出，以便loop调用其他的协程。
"""
