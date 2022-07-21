from django.urls import path
#from django.contrib.auth.views import LoginView,LogoutView
from apps.venta import views

from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='venta'),
    ]
 
