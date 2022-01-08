from django.db import models
from django.utils import timezone
# Create your models here.

#モデルにバリデーションルールを指定させる
from django.core.validators import MinValueValidator,MaxValueValidator

from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(verbose_name="カテゴリ名",max_length=30)
    dt = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)

    def __str__(self):
        return self.name


class Movie(models.Model):

    title = models.CharField(verbose_name="映画タイトル", max_length=100)
    dt = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    release = models.DateField(verbose_name="映画の公開日",null=True,blank=True)
    description = models.CharField(verbose_name="映画説明", max_length=1000, null=True,blank=True)
    img = models.ImageField(verbose_name="映画ジャケット画像",upload_to="review/movie/",null=True,blank=True)
    category = models.ForeignKey(Category,verbose_name="カテゴリ",on_delete=models.PROTECT,null=True,blank=True)

    def __str__(self):
        return self.title


    #TODO:コメント数をカウントする。
    #外部キーに繋がったコメント数をカウントするには、https://noauto-nolife.com/post/django-foreign-count/が有効だが、今回の場合はモデルにメソッドを追加して、参照したほうが良い。
    def comment_count(self):
        return Comment.objects.filter(target=self.id).count()


    #TODO:星の平均点を求める
    #参照元:https://docs.djangoproject.com/en/4.0/topics/db/aggregation/#cheat-sheet
    def average_star(self):
       score    = Comment.objects.filter(target=self.id).aggregate(Avg("star"))
       return score["star__avg"]
 



class Comment(models.Model):
    dt = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    content = models.CharField(verbose_name="コメント本文", max_length=200)
    target = models.ForeignKey(Movie,verbose_name="対象映画",on_delete=models.CASCADE)

    #星の数値は最小で1、最大で5を指定。これ以外はバリデーションエラーになる。
    star = models.IntegerField(verbose_name="星",validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.content
