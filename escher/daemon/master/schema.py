#!/usr/bin/env python

import asyncio
import websockets


async def master(ws, path):
    name = await ws.recv()
    print(f"< {name}")
    await ws.send('hey')


asyncio.get_event_loop().run_until_complete(websockets.serve(master, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
