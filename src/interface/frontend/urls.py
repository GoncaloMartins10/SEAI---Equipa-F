from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('transformer/', views.index, name='home_page'),
    path('transformer/<slug:transformer_id>', views.index, name='transformer_page'),
]
