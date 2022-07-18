from django.urls import path

from apps.seguridad import views

#from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='login'),
    ]
 
