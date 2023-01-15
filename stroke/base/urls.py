from django.contrib import admin
from django.urls import path

from .views import home, result, predict, change_lang, home_page_return

urlpatterns = [
    path('', home, name='home'),
    path('predict/<str:lang>/<int:pk>/', predict, name='predict'),
    path(r'^.+$', home_page_return, name='home_page_return'),
    path('/result/<str:lang>/', result, name='result'),
    path('<str:lang>/', change_lang, name='change_lang'),
]