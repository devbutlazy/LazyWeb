import asyncio
import threading
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import create_tables, drop_tables
from routers.blogs.telegram import main

from routers.blogs.blogs import router as blog_router
from routers.contact import router as message_router
from routers.visits import router as visits_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    print("The app is starting up")
    yield
    print("The app is shutting down")


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(visits_router)
app.include_router(message_router)
app.include_router(blog_router)


if __name__ == "__main__":
    threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)).start()
    asyncio.run(main())
