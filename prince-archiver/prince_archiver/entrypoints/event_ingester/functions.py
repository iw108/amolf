import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from prince_archiver.adapters.file import PathManager
from prince_archiver.adapters.streams import Stream
from prince_archiver.service_layer.streams import IncomingMessage

from .settings import Settings

LOGGER = logging.getLogger(__name__)


@dataclass
class State:
    settings: Settings
    stream: Stream
    path_manager: PathManager


async def run_trim(ctx: dict):
    state: State = ctx["state"]
    trim_to = datetime.now(tz=UTC) - timedelta(days=5)
    await state.stream.trim(trim_to)


async def delete_src(ctx: dict):
    LOGGER.info("Deleting src files")

    state: State = ctx["state"]
    end = datetime.now(tz=UTC) - state.settings.SRC_LIFESPAN
    start = end - timedelta(hours=3)

    async for message in state.stream.range(start, end, msg_cls=IncomingMessage):
        data = message.processed_data()
        if data.system not in state.settings.SRC_SYSTEMS_DELETE:
            continue

        src_dir = state.path_manager.get_src_dir(data.system, data.local_path)
        if src_dir.exists():
            LOGGER.info("[%s] Deleting src directory", data.ref_id)
            await src_dir.rm()
