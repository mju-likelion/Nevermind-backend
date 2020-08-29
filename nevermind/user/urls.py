from django.urls import path
from . import views

urlpatterns = [
  path('issession', views.issession, name = 'issession'),
  path('login', views.login, name = 'login'),
  path('logout', views.logout, name = 'logout'),
  path('register', views.register, name = 'register'),
  path('unregister', views.unregister, name = 'unregister'),
]
