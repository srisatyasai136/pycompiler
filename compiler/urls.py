# # compiler/urls.py
# from django.urls import path
# from .views import home

# urlpatterns = [
#     path("", home, name="home"),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('run/', views.run_code, name='run_code'),
]
