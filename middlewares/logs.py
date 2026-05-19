from fastapi import Request
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/user_api.log', encoding='utf-8', level=logging.INFO)
logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)

async def logs(request, call_next):
    
    init = time.time()
    method = request.method
    route = request.url.path
    user = request.headers.get('X-User-Id')
    
    r = await call_next(request)

    end = time.time()

    req_duration = end - init

    logger.info(f"{method} {route} - User: {user}, {req_duration} ms")

    return r