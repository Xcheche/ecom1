from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("about/", views.about, name="about"),
    path("signup/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("", views.dashboard, name="dashboard"),
]
