from fastapi import FastAPI

from app.api.v1.routers.nid import router as nid_router


def create_app() -> FastAPI:
    app = FastAPI(title="Bangladesh NID OCR Service")

    app.include_router(nid_router, prefix="/api/v1")


    @app.get("/health", tags=["health"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app

app = create_app()
