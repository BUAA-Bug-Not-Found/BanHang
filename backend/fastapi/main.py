import uvicorn
from fastapi import FastAPI

from banhang import user, blog, file

from scripts import  recreate_db

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from banhang.BanHangException import UniException


app = FastAPI()
@app.exception_handler(UniException)
async def unicorn_exception_handler(request: Request, exc: UniException):
    exc.others[exc.key] = exc.value
    return JSONResponse(
        status_code=400,
        content=exc.others,
    )

app.include_router(user.router)
app.include_router(blog.router)
app.include_router(file.router)

DEBUG = True
def main():
    recreate_db.upgrade_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()