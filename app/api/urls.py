from django.contrib import admin
from django.urls import path

from api.views import HistoryView, QueryView, ResultView, PingView

urlpatterns = [
    path('ping/', PingView.as_view()),
    path('query/', QueryView.as_view()),
    path('result/', ResultView.as_view()),
    path('history/', HistoryView.as_view()),
]