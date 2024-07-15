from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('news',views.news,name='news'),
    path('students/<id>',views.students,name='students'),
    path('import-excel', views.import_excel,name='import-excel'),
]
