from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('processRegister/', views.processRegister),
    path('processLogin/', views.processLogin),
    path('profile/', views.profile),
    path('logout/', views.logout),
]