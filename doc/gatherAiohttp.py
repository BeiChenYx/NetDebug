"""
asyncio aiohttp 异步http请求
将aiohttp的响应结果收集到一个列表中
可通过
asyncio.gather(*task) 或
asyncio.wait(task)
将响应全部
收集起来
"""

# aiohttp异步实现的例子:
import time
import asyncio
from aiohttp import ClientSession


tasks = list()
url = "https://www.baidu.com/{}"
async def hello(url, semaphore):
    # async with ClientSession() as session:
        # async with session.get(url) as respone:
            # print('Hello World: {}'.format(time.time()))
            # return await respone.read()
    """
    上面这个存在一个异常可能性
    当并发达到1000个就会出现select对打开的文件字符
    超过了限制，需要限制并发数量, 并发数量在500到600
    一般处理速度最快。
    """
    async with semaphore:
        async with ClientSession() as session:
            async with session.get(url) as respone:
                print('Hello World: {}'.format(time.time()))
                return await respone.read()

async def run():
    semaphore = asyncio.Semaphore(500)
    to_get = [
        hello(url.format(i), semaphore) for i in range(1000)
    ]
    await asyncio.wait(to_get)
    # for i in range(5):
        # task = asyncio.ensure_future(hello(url.format(1)))
        # tasks.append(task)

    # result = loop.run_until_complete(asyncio.gather(*tasks))
    # print(len(result))


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # run()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

"""
# Hello World: 1538275193.2545464
# Hello World: 1538275193.2580657
# Hello World: 1538275193.2627192
# Hello World: 1538275193.2675781
# Hello World: 1538275193.2697988
# 5
"""

