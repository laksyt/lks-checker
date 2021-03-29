import asyncio
from types import SimpleNamespace

from aiohttp import ClientSession, TraceRequestStartParams
from aiohttp.tracing import TraceConfig, TraceRequestEndParams, TraceRequestExceptionParams


def create_request_timer() -> TraceConfig:
    trace_config = TraceConfig()
    trace_config.on_request_start.append(_on_request_start)
    trace_config.on_request_end.append(_on_request_end)
    trace_config.on_request_exception.append(_on_request_exception)
    return trace_config


async def _on_request_start(
        session: ClientSession,
        context: SimpleNamespace,
        params: TraceRequestStartParams
):
    context.time_start = asyncio.get_event_loop().time()


async def _on_request_end(
        session: ClientSession,
        context: SimpleNamespace,
        params: TraceRequestEndParams
):
    context.time_end = asyncio.get_event_loop().time()
    params.response.time = context.time_end - context.time_start


async def _on_request_exception(
        session: ClientSession,
        context: SimpleNamespace,
        params: TraceRequestExceptionParams
):
    context.time_exception = asyncio.get_event_loop().time()
    params.exception.time = context.time_exception - context.time_start
