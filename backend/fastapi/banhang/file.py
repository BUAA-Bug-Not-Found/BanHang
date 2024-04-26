from fastapi import APIRouter, File, UploadFile
import oss2
import uuid
import os

ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ACCESS_KEY_SECRET")
BUCKET_NAME = os.getenv("BUCKET_NAME")
ENDPOINT = os.getenv("ENDPOINT")



router = APIRouter()

@router.post("/uploadfile/", tags=['file'])
async def upload_file(file: UploadFile):
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)
    file_content = await file.read()
    root, extension = os.path.splitext(file.filename)
    oss_name = uuid.uuid4().hex + extension
    with open(oss_name, "wb") as f:
        # 2.3 将获取的fileb文件内容，写入到新文件中
        f.write(file_content)
    result = bucket.put_object_from_file(oss_name, oss_name)
    if result.status == 200:
        return {"response": "success",
                "fileUrl": ENDPOINT + "/" + oss_name}
    else:
        return {"response": "error"}

