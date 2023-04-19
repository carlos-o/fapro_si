from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from settings import LOGGING_CONFIG, CACHE_TIME
from validation import validate_date
from utils import convert_datetime
from parse import ParseSii
from exceptions import NotFound
from redis_om import get_redis_connection
import logging.config
import logging



logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()

REDIS_CLIENT = get_redis_connection(
    host="redis",
    port=6379,
    decode_responses=True
)


@app.get("/")
def index():
    return "works"


@app.get("/uf/{date}")
async def get_fomento_unit(date: str):
    """
    """
    if not validate_date(date):
        logger.error("date format is incorrect")
        raise HTTPException(status_code=400, detail="date format is incorrect, try dd-mm-yyy")
    try:
        converted_date = convert_datetime(date)
    except ValueError as e:
        logger.error(f"{str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    # check in redis
    uf_price_date = REDIS_CLIENT.get(date)
    if uf_price_date is None:
        parse_sii_instance = ParseSii(converted_date)
        try:
            uf_price_date = parse_sii_instance.get_uf_sii()
        except NotFound as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        if uf_price_date is None:
            raise HTTPException(status_code=400, detail="Uf from specific date does not exists")
        REDIS_CLIENT.set(date, uf_price_date)
        REDIS_CLIENT.expire(date, CACHE_TIME)
        return JSONResponse(content={"uf": uf_price_date}, status_code=200)
    return JSONResponse(content={"uf": float(uf_price_date)}, status_code=200)
