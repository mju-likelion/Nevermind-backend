from django.urls import path
from . import views

urlpatterns = [
	path('add', views.add, name = 'add'),
	path('get', views.get, name = 'get'),
	path('update', views.update, name = 'update'),
	path('delete', views.delete, name = 'delete'),
]

