import  views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path('',views.home),
     path('login',views.login),
     path('loginview',views.home),
     path('dashboard', views.dash),
     path('logout',views.logout),
     path('workform',views.work_entry),
     path('dashboard_manager',views.manager_login)

    ] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
