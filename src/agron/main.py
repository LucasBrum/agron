from fastapi import FastAPI

from agron.adapters.inbound.api import router

app = FastAPI(title="Agron")
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}