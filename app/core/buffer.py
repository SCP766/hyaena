from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
FlushCallback = Callable[[list[T]], Awaitable[None]]


class IngestionBuffer(Generic[T]):
    """
    In-process async buffer. Flushes when batch_size is reached
    or flush_interval_ms elapses — whichever comes first.

    Acceptable data loss: buffered-but-unflushed items on process crash.
    This is intentional for error monitoring — losing a few events
    during a crash is acceptable and preferable to blocking callers.
    """

    def __init__(
        self,
        flush_callback: FlushCallback[T],
        batch_size: int = 100,
        flush_interval_ms: int = 500,
    ) -> None:
        self._queue: asyncio.Queue[T] = asyncio.Queue()
        self._flush_callback = flush_callback
        self._batch_size = batch_size
        self._flush_interval = flush_interval_ms / 1000
        self._task: asyncio.Task[None] | None = None

    async def push(self, item: T) -> None:
        await self._queue.put(item)

    async def start(self) -> None:
        self._task = asyncio.create_task(self._worker())
        logger.info("IngestionBuffer started")

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
        await self._flush_remaining()
        logger.info("IngestionBuffer stopped")

    async def _worker(self) -> None:
        while True:
            batch: list[T] = []
            try:
                deadline = asyncio.get_event_loop().time() + self._flush_interval
                while len(batch) < self._batch_size:
                    remaining = deadline - asyncio.get_event_loop().time()
                    if remaining <= 0:
                        break
                    try:
                        item = await asyncio.wait_for(
                            self._queue.get(),
                            timeout=remaining,
                        )
                        batch.append(item)
                    except asyncio.TimeoutError:
                        break
                if batch:
                    await self._flush_callback(batch)
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("IngestionBuffer flush failed")

    async def _flush_remaining(self) -> None:
        batch: list[T] = []
        while not self._queue.empty():
            batch.append(self._queue.get_nowait())
        if batch:
            try:
                await self._flush_callback(batch)
            except Exception:
                logger.exception("IngestionBuffer final flush failed")
