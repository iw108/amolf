import asyncio
import logging
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass
from functools import partial
from typing import AsyncGenerator

from arq import ArqRedis

from prince_archiver.adapters.file import PathManager
from prince_archiver.adapters.streams import Consumer, Stream
from prince_archiver.file import managed_file_system
from prince_archiver.service_layer.handlers.export import (
    Exporter,
    ExportHandler,
    Publisher,
)
from prince_archiver.service_layer.handlers.utils import get_target_key
from prince_archiver.service_layer.streams import Group, IncomingMessage, Streams

from .settings import Settings
from .stream import Ingester, message_handler

LOGGER = logging.getLogger(__name__)


@dataclass
class State:
    stop_event: asyncio.Event
    stream_ingester: Ingester
    export_handler: ExportHandler


@asynccontextmanager
async def get_managed_state(
    redis: ArqRedis,
    *,
    settings: Settings | None = None,
) -> AsyncGenerator[State, None]:
    exit_stack = await AsyncExitStack().__aenter__()

    settings = settings or Settings()

    s3 = await exit_stack.enter_async_context(managed_file_system(settings))

    stop_event = asyncio.Event()

    stream = Stream(redis=redis, stream=Streams.imaging_events)

    yield State(
        stop_event=stop_event,
        stream_ingester=Ingester(
            streamer=stream.stream_group(
                Consumer(group_name=Group.upload_worker),
                msg_cls=IncomingMessage,
                stop_event=stop_event,
            ),
            handler=partial(message_handler, redis=redis),
        ),
        export_handler=ExportHandler(
            stream=stream,
            exporter=Exporter(
                s3=s3,
                key_generator=partial(
                    get_target_key,
                    bucket=settings.AWS_BUCKET_NAME,
                ),
                path_manager=PathManager(settings.SRC_DIR),
            ),
            publisher=Publisher(
                stream=Stream(
                    redis=redis,
                    stream=Streams.upload_events,
                )
            ),
        ),
    )

    await exit_stack.aclose()
