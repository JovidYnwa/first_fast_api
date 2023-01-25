from fastapi import FastAPI
import uvicorn
from endpoints.gems_endpoints import gem_router
from endpoints.user_endpoints import user_router
from populate import create_gems_db



app = FastAPI()
app.include_router(gem_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    #2:49
