from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import CondicionView

urlpatterns = [
    path('condicion', CondicionView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
