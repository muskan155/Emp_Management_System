from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import viewsets
from .form import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    if request.method == "POST":
        file = request.FILES['csv']
        df = pd.read_csv(file)

        # Print column names for debugging
        print("DataFrame columns:", df.columns)

        # Check if required columns are present
        if 'starttime' in df.columns and 'endtime' in df.columns:
            # Define your time constraints
            early_start_time = pd.to_datetime("13:30").time()  # Consider early before 13:30
            late_start_time = pd.to_datetime("13:35").time()  # Consider on time between 13:30 and 13:35
            standard_end_time = pd.to_datetime("21:45").time()
            
            new_data = []
            for i in range(len(df)):
                try:
                    start_time = pd.to_datetime(df['starttime'][i]).time()
                    end_time = pd.to_datetime(df['endtime'][i]).time()
                except Exception as e:
                    print(f"Error parsing time at row {i}: {e}")
                    continue
                
                # Determine start status
                if start_time < early_start_time:
                    start_status = "Early"
                elif early_start_time <= start_time <= late_start_time:
                    start_status = "In time"
                else:
                    start_status = "Delayed"
                
                # Calculate hours worked and overtime
                start_timestamp = pd.Timestamp.combine(pd.Timestamp.today(), start_time)
                end_timestamp = pd.Timestamp.combine(pd.Timestamp.today(), end_time)
                standard_end_timestamp = pd.Timestamp.combine(pd.Timestamp.today(), standard_end_time)

                total_worked_duration = standard_end_timestamp - start_timestamp
                hours_worked_in_seconds = total_worked_duration.total_seconds()

                # Convert to minutes
                total_worked_minutes = int(hours_worked_in_seconds // 60)

                if end_time > standard_end_time:
                    overtime_duration = end_timestamp - standard_end_timestamp
                    overtime_seconds = overtime_duration.total_seconds()
                    overtime_minutes = int(overtime_seconds // 60)
                else:
                    overtime_minutes = 0

                # Append data for displaying in the HTML table
                new_data.append({
                    "Name": df['name'][i],
                    "Start Time": start_time.strftime('%H:%M'),
                    "End Time": end_time.strftime('%H:%M'),
                    "Start Status": start_status,
                    "Total Hours Worked": f"{total_worked_minutes // 60} hrs and {total_worked_minutes % 60} mins",
                    "Overtime Hours": f"{overtime_minutes // 60} hrs and {overtime_minutes % 60} mins" if overtime_minutes > 0 else "No overtime",
                })

                # Save to the database (store time in minutes)
                Employee.objects.create(
                    name=df['name'][i],
                    start_time=start_time,
                    end_time=end_time,
                    status=start_status,
                    total_hours_worked=total_worked_minutes,  # Store total hours worked in minutes
                    overtime_status=overtime_minutes  # Store overtime in minutes
                )
            
            # Return the new data as an HTML table
            return HttpResponse(pd.DataFrame(new_data).to_html())
        else:
            return HttpResponse("CSV file does not contain 'starttime' or 'endtime' columns.")
    else:
        return render(request, 'index.html')

class EmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return HttpResponse("Invalid login")
        else:
            return HttpResponse("Invalid form")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_page(request):
    logout(request)
    return redirect('login')

def register_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            return render(request, 'register.html', {'form': form, 'error': 'Invalid form submission'})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

