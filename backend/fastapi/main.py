import uvicorn
from fastapi import FastAPI

from banhang import user

from orm.database import db_init, db_test

app = FastAPI()

app.include_router(user.router)

def main():
    db_test()
    # uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()