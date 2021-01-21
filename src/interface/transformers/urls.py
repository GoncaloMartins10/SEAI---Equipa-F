from django.urls import path

from . import views


urlpatterns = [
    path('', views.main, name='transformer_main'),
    path('<slug:id_transformer>/medicoes/', views.get_medicoes, name='transformer_measurements'),
    path('<slug:id_transformer>/HI/', views.HI, name='transformer_HI'),
    path('<slug:id_transformer>/report/', views.report, name='transformer_report'),
    path('train_model/', views.train_model, name='ML_training'),
    path('infer/', views.infer, name='ML_infer'),
]

