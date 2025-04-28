import oss2, uuid, os
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()  # 确保.env在当前目录
    ALIYUN_OSS_ACCESS_KEY_ID = os.getenv("OSS_ACCESS_KEY_ID")
    ALIYUN_OSS_ACCESS_KEY_SECRET = os.getenv("OSS_ACCESS_KEY_SECRET")
    ALIYUN_OSS_BUCKET_NAME = os.getenv("OSS_BUCKET_NAME")
    ALIYUN_OSS_ENDPOINT = os.getenv("OSS_ENDPOINT")
    OSS_SERVER_URL = f"https://{ALIYUN_OSS_BUCKET_NAME}.{ALIYUN_OSS_ENDPOINT}"

    # 创建命名空间操作实例对象
    auth = oss2.Auth(ALIYUN_OSS_ACCESS_KEY_ID, ALIYUN_OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ALIYUN_OSS_ENDPOINT, ALIYUN_OSS_BUCKET_NAME)

    # 上传文件
    image = f"demo/{str(uuid.uuid4())}.jpg"
    with open('../onlineapi/uploads/teacher/avatar.jpg', "rb") as f:
        result = bucket.put_object(image, f.read())
        print(result)
        print(result.status)
        print(f"{OSS_SERVER_URL}/{image}")
