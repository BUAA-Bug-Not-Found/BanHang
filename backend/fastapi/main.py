import uvicorn
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI

from banhang import user, blog, question, file, message

from scripts import recreate_db, buaa_api_renewer

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from banhang.BanHangException import UniException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=False)  # 如果需要开启开发者工具栏，请在其中传入debug=True。 注意提交到dev前一定要改回False或删去debug参数


@app.exception_handler(UniException)
async def unicorn_exception_handler(request: Request, exc: UniException):
    exc.others[exc.key] = exc.value
    return JSONResponse(
        status_code=400,
        content=exc.others,
    )


app.include_router(user.router)
app.include_router(blog.router)
app.include_router(question.router)
app.include_router(file.router)
app.include_router(message.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://lyhtool.tpddns.cn:8000",
                   "http://127.0.0.1:8080",
                   "http://127.0.0.1:8080",
                   "http://localhost:8080",
                   "http://localhost",
                   "https://localhost",
                   "https://banhang.lyhtool.com:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    buaa_api_renewer.scheduler.start()
    print('启动事件循环')


@app.on_event("shutdown")
async def shutdown_event():
    buaa_api_renewer.scheduler.shutdown()


DEBUG = True


def main():
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    )
    ## 在app实例化时传入debug=True来开启debugTool
    recreate_db.upgrade_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
