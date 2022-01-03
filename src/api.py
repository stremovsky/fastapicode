from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseSettings, BaseModel
from starlette_exporter import PrometheusMiddleware, handle_metrics
import redis


# pydantic reads case insensitive environment variables into fields in this class
class Settings(BaseSettings):
    redis_url: str


app = FastAPI()
app.add_middleware(
    PrometheusMiddleware,
    app_name="exam",
    group_paths=True,
    prefix="exam",
    skip_paths=["/healthcheck"],
)
app.add_route("/prom-metrics", handle_metrics)
settings = Settings()
redis_con = None


@app.on_event("startup")
def startup_event():
    global redis_con
    redis_con = redis.from_url(settings.redis_url)


@app.get("/get/{item_id}")
def get_data(item_id: str):
    data = redis_con.get(item_id)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {item_id: data}


class Item(BaseModel):
    id: str
    data: str


@app.post("/set", status_code=status.HTTP_201_CREATED)
def set_data(item: Item, response: Response):
    if redis_con.get(item.id):
        response.status_code = status.HTTP_200_OK
    redis_con.set(item.id, item.data)
    return {"status": "ok"}
