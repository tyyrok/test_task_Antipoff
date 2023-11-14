from django.contrib import admin
from django.urls import path

from api.views import HistoryView, QueryView, ResultView, PingView

urlpatterns = [
    path('ping/', PingView.as_view()),
    path('query/', QueryView.as_view()),
    path('result/<str:number>/', ResultView.as_view()),
    path('history/<str:number>/', HistoryView.as_view()),
]