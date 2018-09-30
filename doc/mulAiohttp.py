"""
asyncio aiohttp 异步http请求
如果我们需要请求多个URL，同步的做饭访问
多个URL只需要加个for循环就可以，但异步就
有点麻烦，在之前的基础上需要将hello()包装
在asyncio的Future对象中, 然后将Future对象
列表作为任务传递给事件循环.
"""

# aiohttp异步实现的例子:
import time
import asyncio
from aiohttp import ClientSession


tasks = list()
url = "https://www.baidu.com/{}"
async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as respone:
            respone = await respone.read()
            # print(respone)
            print('Hello World: {}'.format(time.time()))

def run():
    for i in range(5):
        task = asyncio.ensure_future(hello(url.format(1)))
        tasks.append(task)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    run()
    loop.run_until_complete(asyncio.wait(tasks))

"""
Hello World: 1538274299.2925723
Hello World: 1538274299.2961936
Hello World: 1538274299.2976756
Hello World: 1538274299.3064506
Hello World: 1538274299.31017
"""

