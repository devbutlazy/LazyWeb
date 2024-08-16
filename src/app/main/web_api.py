from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_routers(app: FastAPI) -> None:
    """
    Include routers from the presentation layer
    """
    ...


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


if __name__ == "__main__":
    create_app()
