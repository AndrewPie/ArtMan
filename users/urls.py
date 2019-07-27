from django.urls import path

from django.contrib.auth.views import LoginView
from .views import Login,SignUp,Logout

app_name = 'users'

urlpatterns = [
    path('signup/',SignUp.as_view(), name = 'signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/',Logout.as_view(),name='logout'),
]