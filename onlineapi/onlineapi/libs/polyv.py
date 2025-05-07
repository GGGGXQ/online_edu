import time
import requests
import hashlib


class PolyvPlayer(object):
    def __init__(self, userId, secretkey, tokenUrl):
        """初始化，提供用户id和秘钥"""
        self.userId = userId
        self.secretKey = secretkey
        self.tokenUrl = tokenUrl

    def tomd5(self, text):
        """计算字符串的MD5"""
        md5 = hashlib.md5()
        md5.update(text.encode('utf-8'))
        return md5.hexdigest()

    # 获取播放加密视频数据的token
    def get_video_token(self, videoId, viewerIp, viewerId=None, viewerName='', extraParams='HTML5'):
        """
        生成保利威视频播放token
        :param videoId: 视频ID
        :param viewerIp: 观看者IP
        :param viewerId: 观看者ID（可选）
        :param viewerName: 观看者昵称（可选）
        :param extraParams: 扩展参数（默认HTML5）
        :return: 视频播放token
        """
        ts = int(time.time() * 1000)  # 时间戳

        # 构建基础参数字典 - 将None值转换为空字符串
        plain = {
            "userId": self.userId,
            "videoId": videoId,
            "ts": ts,
            "viewerId": str(viewerId) if viewerId is not None else "",  # 强制转换
            "viewerIp": viewerIp,
            "viewerName": str(viewerName),  # 确保字符串
            "extraParams": str(extraParams)  # 确保字符串
        }

        # 按ASCII升序排列并构建字符串
        key_temp = sorted(plain)
        plain_string = ''.join([f"{k}{plain[k]}" for k in key_temp])

        # 首尾拼接秘钥并计算MD5
        sign_data = f"{self.secretKey}{plain_string}{self.secretKey}"
        sign = self.tomd5(sign_data).upper()

        # 添加签名并发送请求
        plain["sign"] = sign

        try:
            response = requests.post(
                url=self.tokenUrl,
                headers={"Content-type": "application/x-www-form-urlencoded"},
                data=plain
            )
            response.raise_for_status()  # 抛出HTTP错误
            result = response.json()
            return result.get("data", {}).get("token", "")
        except (requests.HTTPError, ValueError) as e:
            print(f"请求失败: {str(e)}")
            return ""
