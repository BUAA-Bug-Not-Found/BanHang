import uvicorn
from fastapi import FastAPI, HTTPException

from banhang import user

app = FastAPI()

app.include_router(user.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)