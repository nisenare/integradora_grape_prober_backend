from django.urls import path, include
import grapes_backend_app.views

urlpatterns = [
    path("", grapes_backend_app.views.home, name="home"),
    path("login_form/", grapes_backend_app.views.login, name = "login_form"), 
    path("dashboard/<int:page_num>", grapes_backend_app.views.dashboard, name = "dashboard"), 
    path('accounts/', include("django.contrib.auth.urls"), name = "accounts"),
]