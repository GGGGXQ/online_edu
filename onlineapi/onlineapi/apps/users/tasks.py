from celery import shared_task
from ronglianyunapi import send_sms as sms
import logging


logger = logging.getLogger('django')


@shared_task(name='send_sms')
def send_sms(tid, mobile, datas):
    """异步发送短信"""
    try:
        return sms(tid, mobile, datas)
    except Exception as e:
        logger.error(f"手机号{mobile}，发送短信失败错误：{e}")

@shared_task(name='send_sms1')
def send_sms1():
    logger.info("send_sms1 执行了")  # 使用 INFO 级别
    return {"status": "success", "message": "send_sms1 执行了"}
