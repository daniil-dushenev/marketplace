from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('endreg/', views.endreg, name='endreg'),
    path('profile/', views.profile, name='profile'),
    path('profile/unput/', views.profile_inpt, name='profile_inpt')
]
