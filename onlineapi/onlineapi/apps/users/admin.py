from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, _
from .models import User, Credit


# Register your models here.
class UserModelAdmin(UserAdmin):
    list_display = ["id", "username", "avatar_small", "money", "credit", "mobile"]
    fieldsets = (
        (None, {'fields': ('username', 'password', 'avatar')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    ordering = ('id',)
    list_editable = ["credit"]

    def save_model(self, request, obj, form, change):
        if change:
            """更新数据"""
            user = User.objects.get(pk=obj.id)
            has_credit = user.credit
            new_credit = obj.credit
            Credit.objects.create(
                user=user,
                number=int(new_credit - has_credit),
                operation=2,
            )


admin.site.register(User, UserModelAdmin)


class CreditModelAdmin(admin.ModelAdmin):
    """积分流水的模型管理器"""
    list_display = ["id", "user", "number", "__str__"]


admin.site.register(Credit, CreditModelAdmin)
