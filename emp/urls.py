from django.urls import path
from .views import*
from .import views

urlpatterns = [
    path('',views.index,name='index'),
     path('employee/<int:id>/', EmployeeDetail.as_view(), name='employee-detail'),

]
