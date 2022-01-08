from django.shortcuts import render,redirect
from django.views import View

from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Q

from .models import Category,Movie,Comment
from .forms import CommentForm,YearMonthForm


class ContextView(View):

    def context(self):
        context = {}
        context["categories"] = Category.objects.order_by("-dt")
        context["monthly"] = Movie.objects.annotate(monthly_date=TruncMonth("release")).values("monthly_date").annotate(count=Count("id")).values("monthly_date", "count").order_by("-monthly_date")


        #新着コメントを10件だけ表示
        context["new_comments"] = Comment.objects.order_by("-dt")[:10]

        return context


class IndexView(ContextView):

    def get(self, request, *args, **kwargs):
        context = self.context()
        movies = Movie.objects.order_by("-dt")

        #年月の指定がされている場合、バリデーションOKになる。そこで年月検索を行う
        form = YearMonthForm(request.GET)

        #バリデーションチェック(yearとmonthがそれぞれ数値型であり、monthの場合は1~12の値である)
        if form.is_valid():
            #form.clean()はフォームクラスで指定したフィールドの型に従って型変換をする(つまり、yearとmonthは数値型になる)
            cleaned = form.clean()
            #cleanedにyearとmonthを指定して、受け取った値で検索。型変換されているので、それぞれ数値型
            movies = Movie.objects.filter(release__year=cleaned["year"],release__month=cleaned["month"]).order_by("-dt")

        if "category" in request.GET:
            print(request.GET["category"])

            if request.GET["category"] == "":
                movies = Movie.objects.filter(category=None).order_by("-dt")
            else:
                movies = Movie.objects.filter(category__name=request.GET["category"]).order_by("-dt")

        if "search" in request.GET:
            #TODO:ここで検索処理を実行
            print(request.GET["search"])

            #(1)キーワードが空欄もしくはスペースのみの場合、トップページにリダイレクト
            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("review:index")

            #『バイオハザード 主演』["バイオハザード","主演"]
            search = request.GET["search"].replace("　"," ")
            search_list = search.split(" ")

            query       = Q()
            for word in search_list:
                # 空欄の場合は次のループへ
                if word == "":
                    continue

                # TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
                query &= Q(title__contains=word)

            movies = Movie.objects.filter(query).order_by("-dt")

        context["movies"] = movies

        return render(request,"review/index.html",context)

index   = IndexView.as_view()

class SingleView(ContextView):
    def get(self, request, pk, *args, **kwargs):
        context = self.context()

        #ここで必要なデータを検索している
        context["movie"] = Movie.objects.filter(id=pk).first()
        context["comments"] = Comment.objects.filter(target=pk).order_by("-dt")

        if not context["movie"]:
            return redirect("review:index")

        return render(request,"review/single.html",context)

    def post(self, request, pk, *args, **kwargs):

        #TODO:ここでpkをセットする
        copied              = request.POST.copy()
        copied["target"]    = pk
        form                = CommentForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect("review:single",pk)

single   = SingleView.as_view()
