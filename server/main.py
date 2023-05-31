import logging
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routers import users

sys.path.insert(0,'/server')
# from core import setting

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.INFO)
logger = logging.getLogger()

app = FastAPI()

app.add_middleware( CORSMiddleware, allow_origins=['*'] )

app.include_router(users.router)

logger.info(f"Include router")

if __name__ == "__main__":
    uvicorn.run(app,
                host="0.0.0.0",
                port=8080,
                log_level="info",
                proxy_headers=True,
                forwarded_allow_ips='*')
