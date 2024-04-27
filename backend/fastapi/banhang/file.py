from fastapi import APIRouter, File, UploadFile
import oss2
import uuid
import os

from fastapi.responses import StreamingResponse
from mimetypes import guess_type
from banhang.BanHangException import UniException


class OSS_config:
    def __init__(self):
        self.endpoint = None
        self.bucket_name = None
        self.access_key_id = None
        self.access_key_secret = None

    @property
    def ACCESS_KEY_ID(self):
        if not self.access_key_id:
            self.access_key_id = os.getenv("ACCESS_KEY_ID")
        return self.access_key_id
    @property
    def ACCESS_KEY_SECRET(self):
        if not self.access_key_secret:
            self.access_key_secret = os.getenv("ACCESS_KEY_SECRET")
        return self.access_key_secret
    @property
    def BUCKET_NAME(self):
        if not self.bucket_name:
            self.bucket_name = os.getenv("BUCKET_NAME")
        return self.bucket_name
    @property
    def ENDPOINT(self):
        if not self.endpoint:
            self.endpoint = os.getenv("ENDPOINT")
        return self.endpoint

oss_config = OSS_config()

router = APIRouter()

@router.post("/uploadfile/", tags=['file'])
async def upload_file(file: UploadFile):
    auth = oss2.Auth(oss_config.ACCESS_KEY_ID, oss_config.ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, oss_config.ENDPOINT, oss_config.BUCKET_NAME)
    file_content = await file.read()
    root, extension = os.path.splitext(file.filename)
    oss_name = uuid.uuid4().hex + extension
    with open(oss_name, "wb") as f:
        f.write(file_content)
    result = bucket.put_object_from_file(oss_name, oss_name)
    os.remove(oss_name)
    if result.status == 200:
        return {"response": "success",
                "fileUrl": oss_config.ENDPOINT + "/" + oss_name}
    else:
        return {"response": "error"}

@router.get("/downloadfile/", tags=['file'])
def download_file(filename:str):
    auth = oss2.Auth(oss_config.ACCESS_KEY_ID, oss_config.ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, oss_config.ENDPOINT, oss_config.BUCKET_NAME)
    if not os.path.exists("./download"):
        os.mkdir("./download")
    if os.path.exists("./download/" + filename):
        os.remove("./download/" + filename)
    try:
        res = bucket.get_object(filename)
        return StreamingResponse(res, media_type=guess_type(filename)[0] or "text/plain")
    except:
        raise UniException(key="desceiption", value = "文件名错误")

