from django.urls import path
import grapes_backend_app.views

urlpatterns = [
    path("login", grapes_backend_app.views.login, name = "login")
]