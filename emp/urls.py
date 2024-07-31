from django.urls import path,include
from . import views
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'/employee', EmployeeView)

urlpatterns = [
    path('',views.index,name='index'),
    path('api', include(router.urls)),
    path('login', views.login_page,name='login')

]
