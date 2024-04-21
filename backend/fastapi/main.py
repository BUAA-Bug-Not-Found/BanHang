import uvicorn
from fastapi import FastAPI

from banhang import user
from scripts import recreate_db

app = FastAPI()

app.include_router(user.router)



if __name__ == "__main__":
    recreate_db.upgrade_sqlite_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)