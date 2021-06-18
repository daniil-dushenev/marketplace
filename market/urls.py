from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('item/<int:pk>/', views.item_page, name='item_page')
]
