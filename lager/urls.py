from django.urls import path
from . import views

app_name = 'lager'

urlpatterns = [
    path('', views.index, name='index'),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
]