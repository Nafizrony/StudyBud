from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>',views.profile,name='profile'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
]
