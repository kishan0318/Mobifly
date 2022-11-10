from django.urls import path
from .views import *


urlpatterns = [
    path('signup',SignupApi.as_view()),
    path('login',Login.as_view()),
    path("LoginApi",Login.as_view()),
    path('SignupApiAdmin',SignupApiAdmin.as_view()),

]
