import uvicorn
from fastapi import FastAPI

from banhang import user

from scripts import  recreate_db

app = FastAPI()

app.include_router(user.router)

def main():
    recreate_db.upgrade_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()