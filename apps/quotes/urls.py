from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('processRegister/', views.processRegister),
    path('processLogin/', views.processLogin),
    path('dashboard/', views.dashboard),
    path('user/<int:id>/', views.show),
    path('addQuote/', views.addQuote),
    path('deleteQuote/<int:id>/', views.deleteQuote),
    path('likeQuote/<int:id>/', views.likeQuote),
    path('account/', views.profile),
    path('account/update/', views.update),
    path('logout/', views.logout),
]