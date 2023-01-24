from fastapi import FastAPI
import uvicorn
from endpoints.gems_endpoints import gem_router

app = FastAPI()
app.include_router(gem_router)

if __name__ == "__main__":
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
