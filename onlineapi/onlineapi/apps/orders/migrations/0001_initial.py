# Generated by Django 5.1.7 on 2025-04-28 10:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("courses", "0004_rename_courseactivity_courseactivityprice_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(default="", max_length=255, verbose_name="名称"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="是否删除"),
                ),
                ("orders", models.IntegerField(default=0, verbose_name="序号")),
                ("is_show", models.BooleanField(default=True, verbose_name="是否显示")),
                (
                    "created_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="添加时间"),
                ),
                (
                    "updated_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="订单总价",
                    ),
                ),
                (
                    "real_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        verbose_name="实付金额",
                    ),
                ),
                (
                    "order_number",
                    models.CharField(max_length=64, verbose_name="订单号"),
                ),
                (
                    "pay_type",
                    models.SmallIntegerField(
                        choices=[(0, "支付宝"), (1, "微信"), (2, "余额")],
                        default=1,
                        verbose_name="支付方式",
                    ),
                ),
                (
                    "order_desc",
                    models.TextField(
                        blank=True, max_length=500, null=True, verbose_name="订单描述"
                    ),
                ),
                (
                    "pay_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="支付时间"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="user_order",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="下单用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单记录",
                "verbose_name_plural": "订单记录",
                "db_table": "ol_order",
            },
        ),
        migrations.CreateModel(
            name="OrderDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(default="", max_length=255, verbose_name="名称"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="是否删除"),
                ),
                ("orders", models.IntegerField(default=0, verbose_name="序号")),
                ("is_show", models.BooleanField(default=True, verbose_name="是否显示")),
                (
                    "created_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="添加时间"),
                ),
                (
                    "updated_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="课程原价"
                    ),
                ),
                (
                    "real_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="课程实价"
                    ),
                ),
                (
                    "discount_name",
                    models.CharField(
                        default="", max_length=120, verbose_name="优惠类型"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="course_orders",
                        to="courses.course",
                        verbose_name="课程",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="order_course",
                        to="orders.order",
                        verbose_name="订单",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单详情",
                "verbose_name_plural": "订单详情",
                "db_table": "ol_order_course",
            },
        ),
    ]
