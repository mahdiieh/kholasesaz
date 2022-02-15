from django.contrib import admin
from django.urls import path, include
from project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='home'),
    path('login/', views.loginuser, name='loginuser'),
    path('signup/', views.signupuser, name='signupuser'),
    path('loguot/', views.logoutuser, name='logoutuser'),
    path('summary/', views.summaryServices, name='summaryServices'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('/captcha', include("captcha.urls")),
    path('edit/', views.edit, name='edit'),
    path('allsummaries/', views.allsummaries, name='allsummaries'),
    path('summary/<int:summary_pk>', views.viewsummaries, name='viewsummaries'),
    path('summary/<int:summary_pk>/delete', views.deletesummary, name='deletesummary'),
]
