import constants, random
from django.core.management.base import BaseCommand, CommandError
from courses.models import Teacher
from faker import Faker
from django.conf import settings


def add_teacher(options):
    """添加授课老师的测试数据"""
    faker = Faker(["zh_CN"])
    for i in range(options["number"]):
        Teacher.objects.create(
            name=faker.unique.name(),  # 唯一的姓名
            avatar="teacher/avtar.jpg",
            role=random.randint(0, 2),
            title="老师",
            signature="从业3年，管理班级无数",
            brief=f"从业3年，管理班级无数，联系电话：{faker.unique.phone_number()}，邮箱地址：{faker.unique.company_email()}",
        )
    print("添加授课老师的测试数据完成...")


def add_direction(options):
    """添加学习方向的测试数据"""
    print("添加学习方向的测试数据")


class Command(BaseCommand):
    help = '添加课程相关测试数据'

    def add_arguments(self, parser):
        # 位置参数，必填项
        # parser.add_arguments(
        #     '--table',
        #     action='store_true',
        #     help='Delete poll instead of closing it'
        # )
        # 命令参数
        parser.add_argument(
            '--type',
            dest='type',
            default='teacher',
            type=str,
            help='测试数据类型',
        )

        parser.add_argument(
            '--number',
            dest='number',
            default=10,
            type=int,
            help='添加数据的数量',
        )

    # 命令执行的核心方法
    def handle(self, *args, **options):
        """添加测试数据"""
        print("添加测试数据")
        if options['type'] == 'teacher':
            add_teacher(options)
        elif options['type'] == 'direction':
            add_direction(options)

        # Teacher.objects.create(
        #     name="赵小明",
        #     avatar="teacher/avatar.jpg",
        #     role=1,
        #     title="老师",
        #     signature="从业3年，管理班级无数",
        #     brief="从业3年，管理班级无数",
        # )

