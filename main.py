from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from routers.visits_counter import router as visits_router
from routers.message_handler import router as message_router
from source.database import create_tables


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
