"""
asyncio aiohttp 异步http请求
如果需要并发http请求, 通常是用requests, 但
requests是同步的库，如果想异步的话需要引入
aiohttp, 引入一个类：
from aiohttp import ClientSession, 首先要
建立一个session对象，然后用session对象区打开
网页. session可以进行多项操作，比如post, get,
put, head等;
基本用法:
    async with ClientSession() as session:
        async with session.get(url) as respone:
"""

# aiohttp异步实现的例子:
import asyncio
from aiohttp import ClientSession


tasks = list()
url = "https://www.baidu.com/{}"
async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as respone:
            respone = await respone.read()
            print(respone)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello(url))

"""
首先async def 关键字定义了这个异步函数, await关键字
加在需要等待的操作前面，respone.read()等待request
响应，是个耗时IO操作, 然后使用ClientSession类发起请求.
"""

