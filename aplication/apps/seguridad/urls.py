from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from apps.seguridad import views

from django.conf.urls.static import static

urlpatterns=[
    #path('',views.home,name='login'),
    path('',LoginView.as_view(template_name='seguridad/home.html',redirect_authenticated_user=True),name='login'),
    path('logout/',LogoutView.as_view(template_name='account/home.html'),name='logout'),

    ]

