from models import models, BaseModel
from django.utils.html import format_html


# Create your models here.
class Nav(BaseModel):
    """导航菜单"""
    POSITION_OPTION = (
        (0, "顶部导航"),
        (1, "脚部导航"),
    )

    link = models.CharField(max_length=255, verbose_name="导航链接")
    is_http = models.BooleanField(default=False, verbose_name="是否是外部链接")
    position = models.IntegerField(choices=POSITION_OPTION, default=0)

    class Meta:
        db_table = 'ol_nav'
        verbose_name = "导航菜单"
        verbose_name_plural = verbose_name


class Banner(BaseModel):
    image = models.ImageField(upload_to="banner/%Y/", verbose_name="图片地址")
    link = models.CharField(max_length=500, verbose_name="链接地址")
    note = models.CharField(max_length=150, verbose_name="备注信息")
    is_http = models.BooleanField(default=False, verbose_name="是否是外部链接", help_text="站点链接地址：http://www.baidu.com/book<br>站点链接地址：/book/")

    class Meta:
        db_table = "ol_banner"
        verbose_name = "轮播广告"
        verbose_name_plural = verbose_name

    def image_html(self):
        if self.image:
            return format_html(f'<img style="border-radius: 0%;max-height: 100px; max-width: 400px;" src="{self.image.url}">')
        return ""

    image_html.short_description = "广告图片"
    image_html.allow_tags = True
    image_html.admin_order_field = "image"
