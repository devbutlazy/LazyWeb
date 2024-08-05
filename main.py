import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from database.database import create_tables
from routers.blogs.blogs import router as blog_router
from routers.blogs.telegram import main
from routers.contact import router as message_router, limiter
from routers.visits import router as visits_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    print("The app is starting up")
    yield
    print("The app is shutting down")


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

app.state.limiter = limiter  # type: ignore
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

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
    asyncio.run(main())
