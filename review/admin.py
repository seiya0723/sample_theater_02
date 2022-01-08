from django.contrib import admin
from .models import Movie,Comment,Category
from django.utils.html import format_html


class MovieAdmin(admin.ModelAdmin):
    #ここの順番をいじればそのとおりになる。
    list_display = [ "title","dt","release","description","category","format_img" ]

    #画像を表示させる
    def format_img(self,obj):
        if obj.img:
            return format_html('<img src="{}" alt="画像" style="width:15rem">', obj.img.url)


admin.site.register(Movie,MovieAdmin)
admin.site.register(Comment)
admin.site.register(Category)
