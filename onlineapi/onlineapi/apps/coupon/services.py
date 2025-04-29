import json
from django_redis import get_redis_connection
from courses.models import Course


def get_user_coupon_list(user_id):
    """获取指定用户拥有的所有优惠券列表"""
    redis = get_redis_connection("coupon")
    coupon_list = redis.keys(f"{user_id}:*")

    try:
        coupon_id_list = [item.decode() for item in coupon_list]
    except:
        coupon_id_list = []
    coupon_data = []
    # 遍历redis中所有的优惠券数据并转换数据格式
    for coupon_key in coupon_id_list:
        coupon_item = {"user_coupon_id": int(coupon_key.split(":")[-1])}
        coupon_hash = redis.hgetall(coupon_key)
        for key, value in coupon_hash.items():
            key = key.decode()
            value = value.decode()
            if key in ["to_course", "to_category", "to_direction"]:
                value = json.loads(value)
            coupon_item[key] = value
        coupon_data.append(coupon_item)

    return coupon_data


def get_user_enable_coupon_list(user_id):
    """
    获取指定用户本次下单的可用优惠券列表
    根据当前本次客户端购买商品课程进行比较， 获取当前用户的当前可用优惠券
    """
    redis = get_redis_connection("cart")
    # 先获取所有优惠券列表
    coupon_data = get_user_coupon_list(user_id)
    # 获取指定用户的购物车中的勾选商品【与优惠券的适用范围进行对比，找出能用的优惠券】
    cart_hash =redis.hgetall(f"cart{user_id}")
    # 获取被勾选的商品课程的ID列表
    course_id_list = {int(key.decode()) for key, value in cart_hash.items() if value == b'1'}
    # 获取被勾选的商品课程的模型对象
    course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()

    category_id_list = set()
    direction_id_list = set()
    for course in course_list:
        category_id_list.add(int(course.category.id))
        direction_id_list.add(int(course.direction.id))
    enable_coupon_list = []
    for item in coupon_data:
        coupon_type = int(item.get("coupon_type"))
        if coupon_type == 0:
            # 通用优惠券类型
            item["enable_course"] = "__all__"
            enable_coupon_list.append(item)
        elif coupon_type == 3:
            # 指定课程优惠券
            coupon_course = {int(course_item["course__id"]) for course_item in item.get("to_course")}
            enable_coupon_list.append(item)
        elif coupon_type == 2:
            # 指定分类优惠券
            coupon_category = {int(category_item["category__id"]) for category_item in item.get("to_category")}
            ret = category_id_list & coupon_category
            if len(ret) > 0:
                item["enable_course"] = {int(course.id) for course in course_list if course.category.id in ret}
                enable_coupon_list.append(item)
        elif coupon_type == 1:
            # 指定学习方向优惠券
            coupon_direction = {int(direction_item["direction__id"]) for direction_item in item.get("to_direction")}
            ret = direction_id_list & coupon_direction
            if len(ret) > 0:
                item["enable_course"] = {int(course.id) for course in course_list if course.direction.id in ret}
                enable_coupon_list.append(item)
    return enable_coupon_list
