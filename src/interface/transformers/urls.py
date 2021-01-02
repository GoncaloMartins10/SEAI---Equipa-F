from django.urls import path

from . import views


urlpatterns = [
    path('', views.main, name='transformer_main'),
    path('<slug:id_transformer>/medicoes/', views.get_medicoes),
]

