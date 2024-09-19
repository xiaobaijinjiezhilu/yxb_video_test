# config:utf-8
from django.contrib import admin
from django.urls import path, include
from yxb_app.client import urls as client_urls
from yxb_app.dashboard import urls as dashboard_urls

urlpatterns = [
    path('client/', include(client_urls)),
    path('dashboard/', include(dashboard_urls))

]
