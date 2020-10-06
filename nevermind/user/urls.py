from django.urls import path
from . import views

urlpatterns = [
  path('issession', views.issession, name = 'issession'),
  path('getprofile', views.getprofile, name = 'getprofile'),
  path('login', views.login, name = 'login'),
  path('logout', views.logout, name = 'logout'),
  path('emailauth', views.emailauth, name = 'emailauth'),
  path('register', views.register, name = 'register'),
  path('unregister', views.unregister, name = 'unregister'),
]
