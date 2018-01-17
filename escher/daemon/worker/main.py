#!/usr/bin/env python

import asyncio

import time
import websockets
from moleskin import moleskin as M


async def hello(uri, i):
    async with websockets.connect(uri) as ws:
        await ws.send("Hello world!")
        a = await ws.recv()
        print(a)
        time.sleep(1.0)


asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8765', 1))
asyncio.get_event_loop().run_forever()
