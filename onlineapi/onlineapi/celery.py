import os
from celery import Celery


# 必须在实例化celery应用之前执行
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineapi.settings.dev')

# 实例化celery应用对象
app = Celery('onlineapi')
# 指定任务队列名称
app.conf.task_default_queue = 'Celery'
# 把配置写在django的项目配置中
app.config_from_object('django.conf:settings', namespace='CELERY')  # 设置django中配置信息以"CELERY_"开头为celery的配置信息
# 自动根据配置查找django的所有子应用下的tasks任务文件
app.autodiscover_tasks()
