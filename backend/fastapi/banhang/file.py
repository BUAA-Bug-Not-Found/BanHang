from fastapi import APIRouter, UploadFile
import oss2
import uuid
import os

from PIL import Image
from tools.check_user import check_user, authorize
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from typing import Optional
from starlette.background import BackgroundTask

import threading


class OSS_config:
    def __init__(self):
        self.endpoint = None
        self.bucket_name = None
        self.access_key_id = None
        self.access_key_secret = None

    @property
    def ACCESS_KEY_ID(self):
        if not self.access_key_id:
            self.access_key_id = os.getenv("OSS_ACCESS_KEY_ID")
        return self.access_key_id

    @property
    def ACCESS_KEY_SECRET(self):
        if not self.access_key_secret:
            self.access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET")
        return self.access_key_secret

    @property
    def BUCKET_NAME(self):
        if not self.bucket_name:
            self.bucket_name = os.getenv("OSS_BUCKET_NAME")
        return self.bucket_name

    @property
    def ENDPOINT(self):
        if not self.endpoint:
            self.endpoint = os.getenv("OSS_ENDPOINT")
        return self.endpoint

    @property
    def CNAME(self):
        if not self.endpoint:
            self.endpoint = os.getenv("OSS_CNAME")
        return self.endpoint


oss_config = OSS_config()

router = APIRouter()


@router.post("/uploadfile/", tags=['File'])
async def upload_file(file: UploadFile, current_user: Optional[dict] = Depends(authorize)):
    if current_user == None:
        return {"response": "error"}
    auth = oss2.Auth(oss_config.ACCESS_KEY_ID, oss_config.ACCESS_KEY_SECRET)
    if oss_config.CNAME:
        bucket = oss2.Bucket(auth, oss_config.CNAME, oss_config.BUCKET_NAME, is_cname=True)
    else:
        bucket = oss2.Bucket(auth, oss_config.ENDPOINT, oss_config.BUCKET_NAME)
    file_content = await file.read()
    root, extension = os.path.splitext(file.filename)
    local_file_path = uuid.uuid4().hex + extension
    oss_file_path = str(current_user['uid']) + "/file/" + uuid.uuid4().hex + extension
    with open(local_file_path, "wb") as f:
        f.write(file_content)
    result = bucket.put_object_from_file(oss_file_path, local_file_path)
    os.remove(local_file_path)
    if result.status == 200:
        return {"response": "success",
                "fileUrl": "https://" + (oss_config.CNAME if oss_config.CNAME else (
                            oss_config.BUCKET_NAME + "." + oss_config.ENDPOINT)) + "/" + oss_file_path}
    else:
        return {"response": "error"}


@router.post("/uploadAvatar/", tags=['File'])
async def upload_avatar(file: UploadFile, current_user: Optional[dict] = Depends(authorize)):
    if current_user == None:
        return {"response": "error"}
    auth = oss2.Auth(oss_config.ACCESS_KEY_ID, oss_config.ACCESS_KEY_SECRET)
    if oss_config.CNAME:
        bucket = oss2.Bucket(auth, oss_config.CNAME, oss_config.BUCKET_NAME, is_cname=True)
    else:
        bucket = oss2.Bucket(auth, oss_config.ENDPOINT, oss_config.BUCKET_NAME)
    file_content = await file.read()
    root, extension = os.path.splitext(file.filename)
    local_file_path = uuid.uuid4().hex + extension
    local_resized_file_path = uuid.uuid4().hex + extension
    oss_file_path = str(current_user['uid']) + "/avatar/" + uuid.uuid4().hex + extension
    with open(local_file_path, "wb") as f:
        f.write(file_content)
    try:
        resize_image(local_file_path, local_resized_file_path)
        os.remove(local_file_path)
    except Exception as e:
        os.remove(local_file_path)
        return {"response": "error", "description": str(e)}
    result = bucket.put_object_from_file(key=oss_file_path, filename=local_resized_file_path)
    os.remove(local_resized_file_path)
    if result.status == 200:
        return {"response": "success",
                "fileUrl": "https://" + (oss_config.CNAME if oss_config.CNAME else (
                            oss_config.BUCKET_NAME + "." + oss_config.ENDPOINT)) + "/" + oss_file_path}
    else:
        return {"response": "error"}


def resize_image(image_path, output_path, size=(500, 500)):
    with Image.open(image_path) as img:
        img_resized = img.resize(size, Image.LANCZOS)
        img_resized.save(output_path)


@router.post("/getAppLastVersion/", tags=['File'])
def get_app_last_version():
    auth = oss2.Auth(oss_config.ACCESS_KEY_ID, oss_config.ACCESS_KEY_SECRET)
    if oss_config.CNAME:
        bucket = oss2.Bucket(auth, oss_config.CNAME, oss_config.BUCKET_NAME, is_cname=True)
    else:
        bucket = oss2.Bucket(auth, oss_config.ENDPOINT, oss_config.BUCKET_NAME)
    realeases = bucket.list_objects_v2(prefix="releases/", delimiter="/").object_list
    last_release = sorted(realeases, key=lambda x: x.last_modified)[-1]
    file_path = last_release.key
    version = ".".join(file_path.split(".")[:-1]).split("-")[1:]
    return {"response": "success",
            "version": version,
            "fileUrl": "https://" + (oss_config.CNAME if oss_config.CNAME else (
                        oss_config.BUCKET_NAME + "." + oss_config.ENDPOINT)) + "/" + file_path}


file_lock = threading.Lock()


@router.get('/genfile', tags=['File'])
def gen_file(filename: str, content: str):
    file_lock.acquire()
    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')
    try:
        with open(f'./tmp/{filename}', 'w') as f:
            f.write(content)
        return FileResponse(
            f'./tmp/{filename}',
            filename=f"{filename}",
            background=BackgroundTask(lambda: os.remove(f'./tmp/{filename}')),
        )
    finally:
        file_lock.release()
        print('release')
