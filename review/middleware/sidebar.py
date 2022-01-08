from django.db.models.functions import TruncMonth
from django.db.models import Count

from ..models import Category,Movie


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.CATEGORIES = Category.objects.order_by("-dt")
        request.MONTHLY = Movie.objects.annotate(monthly_date=TruncMonth("release")).values("monthly_date").annotate(count=Count("id")).values("monthly_date","count").order_by("-monthly_date")
        print("こちらはMIDDLEWAREです")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response