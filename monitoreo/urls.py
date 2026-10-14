from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("importar/", views.importar_csv, name="importar_csv"),
    path("health/", views.health, name="health"),
]
