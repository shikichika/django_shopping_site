from django.contrib import admin

#追加
from django.contrib.auth.admin import UserAdmin
from .models import Account


#管理画面でのサイト管理者のパスワードなどを非表示・閲覧するだけなどにする
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined','is_active')
    #押したらリンクに飛ぶようにする
    list_display_links = ('email', 'first_name', 'last_name')
    #読むだけ
    readonly_fields = ('last_login', 'date_joined')

    #date_joinedで新しい順にする
    ordering = ('date_joined',)

    #こういう書き方が必要
    filter_horizontal =()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)


