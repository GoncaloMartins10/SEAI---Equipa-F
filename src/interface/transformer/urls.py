from django.urls import path

from . import views


app_name = 'transformer'
urlpatterns = [
            path('', views.index, name='index'),
            path('<slug:id_transformer>/', views.get_transformer, name='get_transformer')
        ]

