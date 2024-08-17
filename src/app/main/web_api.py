import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from uvicorn.config import Config
from uvicorn.server import Server

from ..presentation.telegram.handlers.post_handlers import router as post_router
from ..presentation.telegram.handlers.common_handlers import router as common_router
from ..infrastructure.database import create_tables
from .config.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    print("The app is starting up")
    yield
    print("The app is shutting down")


def init_routers(app: FastAPI) -> None:
    """
    Include routers from the presentation layerCommandStart
    """
    ...


async def start_telegram_bot() -> None:
    print("[+] Telegram bot started")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_routers(post_router, common_router)

    await dp.start_polling(bot)


async def start_processes() -> None:
    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    config = Config(app=app, host="0.0.0.0", port=8000, loop="asyncio")
    server = Server(config=config)

    await asyncio.gather(start_telegram_bot(), server.serve())


if __name__ == "__main__":
    asyncio.run(start_processes())
