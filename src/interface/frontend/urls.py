from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('transformer/', views.index, name='transformer_page'),
]
