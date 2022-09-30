from django.urls import reverse
from django.db import models



class Category(models.Model):
    category_name = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 100, unique = True)
    description = models.CharField(max_length = 255)
    #upload 先を掲載
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    #テーブル名が単数　categorysになっているのを修正
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    #context_prosessorのカテゴリごとのURLを返す ({% url '' category.slug %}を使わない方法)
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])        

    def __str__(self):
        return self.category_name


