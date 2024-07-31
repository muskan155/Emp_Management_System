from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import viewsets


# Create your views here.
def index(request):
    if request.method == "POST":
        file = request.FILES['excel']
        df = pd.read_excel(file, engine='openpyxl')
        early_start_time = pd.to_datetime("08:45").time()
        late_start_time = pd.to_datetime("09:00").time()
        standard_end_time = pd.to_datetime("17:00").time()
        new_data = []
        for i in range(len(df)):
            start_time = df['starttime'][i]
            end_time = df['endtime'][i]
            if early_start_time <= start_time <= late_start_time:
                start_status = "In time"
            elif start_time < early_start_time:
                start_status = "Early"
            else:
                start_status = "Delayed"
            
            start_timestamp = pd.Timestamp.combine(pd.Timestamp.today(), start_time)
            end_timestamp = pd.Timestamp.combine(pd.Timestamp.today(), end_time)
            standard_end_timestamp = pd.Timestamp.combine(pd.Timestamp.today(), standard_end_time)

            total_worked = standard_end_timestamp - start_timestamp
            hours_worked = total_worked.total_seconds() / 3600

            if end_time > standard_end_time:
                overtime_duration = end_timestamp - standard_end_timestamp
                normal_hours_duration = standard_end_timestamp - start_timestamp
                overtime_hours = overtime_duration.total_seconds() / 3600
            else:
                overtime_duration = pd.Timedelta(0)
                normal_hours_duration = end_timestamp - start_timestamp
                overtime_hours = 0



            new_data.append({
                # "Employee ID": df['emp_id'][i],
                "Name": df['name'][i],
                "Start Time": start_time.strftime('%H:%M'),
                "End Time": end_time.strftime('%H:%M'),
                "Start Status": start_status,
                "Total Hours Worked": round(hours_worked, 2),
                "Overtime Hours": round(overtime_hours, 2) if overtime_hours > 0 else 0,
            })

            Employee.objects.create(
                name=df['name'][i],
                start_time=start_time,
                end_time=end_time,
                status=start_status,
                total_hours_worked=round(hours_worked, 2),
                overtime_status=round(overtime_hours, 2) if overtime_hours > 0 else 0
            )

        return HttpResponse(pd.DataFrame(new_data).to_html())
       

    else:
        return render(request, 'index.html')
    
class EmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
   