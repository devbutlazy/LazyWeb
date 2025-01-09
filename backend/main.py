import argparse
import asyncio
import subprocess

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.config import Config
from uvicorn.server import Server

from config.config import settings
from core.logger.logger import logger
from core.telegram.handlers.common_handlers import router as common_router
from core.telegram.handlers.commands_handlers import router as post_router

from core.api.routers.blog import router as blog_router
from core.api.routers.message import router as message_router
from core.api.routers.visit import router as visit_router


def init_routers(app: FastAPI) -> None:
    """
    Include routers from the presentation layerCommandStart

    :param app: The FastAPI application.
    :return: None
    """
    app.include_router(visit_router)
    app.include_router(blog_router)
    app.include_router(message_router)


def handle_arguments(args: argparse.Namespace) -> None:
    """
    Manage Alembic migrations and start the processes.

    :param args: The parsed arguments from the command line.
    :return: None
    """
    if args.create:
        logger.info("[~] Creating migration")
        subprocess.run(["alembic", "revision", "--autogenerate"])
        logger.info("[+] Migration created, switching to it")
        subprocess.run(["alembic", "upgrade", "head"])
        logger.info("[+] Migration switched")

    elif args.upgrade:
        logger.info("[~] Upgrading to latest migration")
        subprocess.run(["alembic", "upgrade", "head"])
        logger.info("[+] Migration up-to-date")

    asyncio.run(start_processes())


async def start_telegram_bot() -> None:
    """
    Start the Telegram bot.

    :return: None
    """
    logger.info("[+] Telegram bot started\n")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_routers(post_router, common_router)

    await dp.start_polling(bot)


async def start_processes() -> None:
    """
    Start all the processes.

    :return: None
    """
    app = FastAPI(docs_url=None, redoc_url=None)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    config = Config(app=app, host="0.0.0.0", port=8000, loop="asyncio")
    server = Server(config=config)

    init_routers(app)
    await asyncio.gather(start_telegram_bot(), server.serve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Manage Alembic migrations and start the processes."
    )

    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="Create a new Alembic revision and switch to it",
    )
    parser.add_argument(
        "-u",
        "--upgrade",
        action="store_true",
        help="Upgrade the database to the latest Alembic revision",
    )

    handle_arguments(parser.parse_args())
