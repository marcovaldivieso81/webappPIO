from django.urls import path
#from django.contrib.auth.views import LoginView,LogoutView
from apps.configuracion import views
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='configuracion'),
    ]
 
