# python3 协程, asycnio,  async/await, aiohttp 学习笔记

## 协程

协程和多线程相比有何优势?

1. 最大优势在于效率， 协程的执行效率高，因为不是线程切换，也不是函数调用，
   而是使用CPU中断，和定时器一样，当协程切换时是触发cpu中断隐藏效率相当高.
2. 不需要多线程的锁机制，因为只有一个线程，也不存在资源竞争问题;

协程是一个线程执行，若想利用多核CPU, 可以考虑多进程 + 协程

### Python3中协程的实现

Python对协程的支持是通过generator实现的.
在generator中， 不但可以通过for循环来迭代，还可以调用next()函数获取由yield
语句返回的下一个值，但是Python的yield不但可以返回一个值，它还可以接收调用
者发出的参数.

传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列
和等待，很容易导致死锁问题.

如果改用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者
执行完毕后，切换回生产者继续生产，类似现在的工业4.0中的客户下单，工厂再生产
的模式，效率极高.

```python
def consumer():
	r = ''
	while True:
		n = yield r
		if not n:
			return
		print('[CONSUMER] Consuming %s...' % n)
		r = '200 ok'

def produce(c):
	c.send(None)
	n = 0
	while n < 5:
		n = n + 1
		print("[PROCUCER] Producing %s..." % n)
		r = c.send(n)
		print('[PRODUCER] Consumer return: %s' % r)
	c.close()

c = consumer()
produce(c)
```

执行结果:
```text
[PROCUCER] Producing 1...
[CONSUMER] Consuming 1...
[PRODUCER] Consumer return: 200 ok
[PROCUCER] Producing 2...
[CONSUMER] Consuming 2...
[PRODUCER] Consumer return: 200 ok
[PROCUCER] Producing 3...
[CONSUMER] Consuming 3...
[PRODUCER] Consumer return: 200 ok
[PROCUCER] Producing 4...
[CONSUMER] Consuming 4...
[PRODUCER] Consumer return: 200 ok
[PROCUCER] Producing 5...
[CONSUMER] Consuming 5...
[PRODUCER] Consumer return: 200 ok
```

consumer函数是一个generator, 把一个consumer传入produce后:
1. 首先调用c.send(None) 启动生成器;
2. 然后, 一旦生产了东西, 通过c.send(n)切换到consumer执行;
3. consumer通过yield拿到消息, 处理, 又通过yield把结果传回;
4. produce拿到了consumer处理的结果, 继续生产下一条消息;
5. produce决定不生产了, 通过c.close()关闭consumer, 整个过程结束;

## asyncio

在python3.4标准库中引入了asyncio, 直接内置了对异步IO的支持.
asyncio的编程模型就是一个消息循环，在asyncio模块只能怪获取EventLoop的
引用，然后将要执行的协程扔到EventLoop中执行，就实现了异步IO.

使用asyncio实现hello word
```python
import asyncio


@asyncio.coroutine
def hello():
    print('Hello world!')
    r = yield from asyncio.sleep(1)
    print('Hello again!')
    
loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
```

通过打印出线程的名字可以看到是一个线程执行两个协程

```python
import threading

@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    r = yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())
    
loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
```

使用真正的IO操作
```python
import asyncio
@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from write.drain()
    while True:
        line = yield from reader.readline()
        if line = b'\r\n':
@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from write.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()
    
loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
```

## async/await

在python3.5中引入了新语法async和await, 可以让corutine代码更简洁
只需要把 @asyncio.coroutine替换为async,yield from替换为await就行

```python
import asyncio

async def hello():
	print('Hello world!')
	r = await asyncio.sleep(1)
	print('Hello again!')
    
loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
```

## aiohttp

asyncio可以实现单线程并发IO操作。如果仅用在客户端，发挥的威力不大。如果把asyncio用在服务器端，例如Web服务器，由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持。

asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架。

> pip install aiohttp
