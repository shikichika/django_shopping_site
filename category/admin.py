from django.contrib import admin

#table 追加
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    #slugを自動的に作成
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug')


admin.site.register(Category, CategoryAdmin)



