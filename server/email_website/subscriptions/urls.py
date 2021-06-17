from django.urls import path

from . import views

app_name = 'subscriptions'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:subscription_id>/', views.detail, name='detail'),
    path('form/<str:api_key>/', views.form, name='form'),
]