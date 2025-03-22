import base64, json, time, hashlib


if __name__ == '__main__':
    # typ: token类型 jwt or Bear
    # alg: 加密算法 通常使用HMAC SHA256
    """jwt头部的生成"""
    header_data = {"typ": "jwt", "alg": "HS256"}
    header = base64.b64encode(
        json.dumps(header_data).encode()
    ).decode()
    # print(header)
    # eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9

    """jwt载荷的生成"""
    iat = int(time.time())
    payload_data = {
        "sub": "root",
        "exp": iat + 3600,
        "iat": iat,
        "name": "testname",
        "avatar": "1.png",
        "user_id": 1,
        "admin": True,
        "acc_pwd": "QiLCJhbGciOiJIUzI1NiJ9QiLCJhbGciOiJIUzI1NiJ9QiLCJhbGciOiJIUzI1NiJ9",
    }
    payload = base64.b64encode(json.dumps(payload_data).encode()).decode()
    # print(payload)
    # eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNzQyNjI3NzUwLCAiaWF0IjogMTc0MjYyNDE1MCwgIm5hbWUiOiAidGVzdG5hbWUiLCAiYXZhdGFyIjogIjEucG5nIiwgInVzZXJfaWQiOiAxLCAiYWRtaW4iOiB0cnVlLCAiYWNjX3B3ZCI6ICJRaUxDSmhiR2NpT2lKSVV6STFOaUo5UWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjkifQ

    secret = 'django-insecure-hbcv-y9ux0&8qhtkgmh1skvw#v7ru%t(z-#chw#9g5x1r3z=$p'
    data = header + payload + secret
    HS256 = hashlib.sha256()
    HS256.update(data.encode('utf-8'))
    signatrue = HS256.hexdigest()
    # print(signatrue)
    # 79b6b35551f07f2588d198d61a52f8112ea56f9c1f03ce2ee2213c6538e6a33b

    token = f"{header}.{payload}.{signatrue}"
    # print(token)
    # eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9.eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNzQyNjI4MDkwLCAiaWF0IjogMTc0MjYyNDQ5MCwgIm5hbWUiOiAidGVzdG5hbWUiLCAiYXZhdGFyIjogIjEucG5nIiwgInVzZXJfaWQiOiAxLCAiYWRtaW4iOiB0cnVlLCAiYWNjX3B3ZCI6ICJRaUxDSmhiR2NpT2lKSVV6STFOaUo5UWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjkifQ==.f3a2a791b12a752ea9d9acb11cfb76a973c7c314a02f93a4a48bb7b869ad0ed4

    # 验证
    token2 = 'eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9.eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNzQyNjI4MDkwLCAiaWF0IjogMTc0MjYyNDQ5MCwgIm5hbWUiOiAidGVzdG5hbWUiLCAiYXZhdGFyIjogIjEucG5nIiwgInVzZXJfaWQiOiAxLCAiYWRtaW4iOiB0cnVlLCAiYWNjX3B3ZCI6ICJRaUxDSmhiR2NpT2lKSVV6STFOaUo5UWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjkifQ==.f3a2a791b12a752ea9d9acb11cfb76a973c7c314a02f93a4a48bb7b869ad0ed4'
    header2, payload2, signatrue2 = token2.split('.')
    # 是否过期
    payload2_data = json.loads(base64.b64decode(payload2.encode()))
    print(payload2_data)
    exp = int(payload2_data.get("exp", None))
    if exp is not None and exp < int(time.time()):
        print("token过期！！！")
    else:
        print("没有过期")

    # 验证是否有效，是否被篡改
    secret2 = 'django-insecure-hbcv-y9ux0&8qhtkgmh1skvw#v7ru%t(z-#chw#9g5x1r3z=$p'
    data = header + payload + secret2
    HS256 = hashlib.sha256()
    HS256.update(data.encode('utf-8'))
    new_signatrue = HS256.hexdigest()

    if new_signatrue == signatrue:
        print("认证成功！")
    else:
        print("认证失败！")

