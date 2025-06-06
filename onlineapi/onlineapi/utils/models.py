from django.db import models


class BaseModel(models.Model):
    """
    公共模型
    保存项目中的所有模型公共属性和公共方法的声明
    """
    name = models.CharField(max_length=255, default="", verbose_name="名称")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    orders = models.IntegerField(default=0, verbose_name="序号")
    is_show = models.BooleanField(default=True, verbose_name="是否显示")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True
