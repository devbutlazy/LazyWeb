from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from contextlib import asynccontextmanager

from routers.visits import router as visits_router
from routers.contact import router as message_router
from routers.blogs.blogs import router as blog_router

from database.database import create_tables, drop_tables
from routers.blogs.telegram import main


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    print("The app is starting up")
    yield
    print("The app is shutting down")


app = FastAPI()
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(visits_router)
app.include_router(message_router)
app.include_router(blog_router)

if __name__ == "__main__":
    asyncio.run(main())
