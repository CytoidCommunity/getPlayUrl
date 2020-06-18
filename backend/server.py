from asyncio import Queue, wait_for, TimeoutError
from typing import Optional

from fastapi import FastAPI, WebSocket, HTTPException, status

app = FastAPI()
jobs = Queue()


@app.get('/')
async def _():
    pass


@app.get('/playUrl')
async def _(cid: int, quality: Optional[int] = 4):
    waiter = Queue()
    await jobs.put((cid, quality, waiter))
    try:
        return await wait_for(waiter.get(), 10)
    except TimeoutError:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, 'No available workers!')


@app.websocket('/ws')
async def _(ws: WebSocket):
    await ws.accept()
    while True:
        job = await jobs.get()
        cid, quality, waiter = job
        try:
            await ws.send_json({'cid': cid, 'quality': quality})
            res = await ws.receive_json()
        except:
            await jobs.put(job)
            return
        await waiter.put(res)
