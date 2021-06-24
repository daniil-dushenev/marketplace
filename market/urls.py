from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('page/<int:pk>/', views.homepage, name='homepage'),
    path('item/<int:pk>/', views.item_page, name='item_page'),
    path('create/', views.create, name='create'),
    path('edit/<int:pk>/', views.edit, name='edit')
]
