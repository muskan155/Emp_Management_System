from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.

def index(request):
    data={
        'name':'ram'
    }
    return render(request,'index.html',data)


def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')

def news(request):
    return render(request,'news.html')

def students(request,id):
    return render(request,'students.html', {'studentId':id})

def import_excel(request):
    if request.method=="POST":
        file = request.FILES['excel_file']
        df = pd.read_excel(file, engine='openpyxl')  # Reads the Excel file
     
        data_html = df.to_html()

        return HttpResponse(data_html)
    else:
        return render(request, 'import-excel.html')