from django.shortcuts import render
from django.http import HttpResponse
from .forms import ServerCertificateForm
import datetime
from .certificate_decode import certificate_decode

server_list=['expressway',
             'CMS', 
             'mutare', 
             'finesse']

def certcheck(request):
    form = ServerCertificateForm(request.POST)
    if form.is_valid():
        operation= form.cleaned_data['operation']
        server=form.cleaned_data['server']
        alert_needed_on=form.cleaned_data['alert_day']
        if operation in server_list:
            time_delta= certificate_decode(server) - datetime.date.today()
            final_alert=certificate_decode(server)- alert_needed_on
            return render(request, 'certexp/certificate.html', {'days_left':time_delta.days,'final_alert':final_alert.days})
        elif operation=='UCM':
            SERVER = '172.26.200.120'
            service=form.cleaned_data['service']
            url = f'https://{SERVER}/platformcom/api/v1/certmgr/config/identity/certificate?service={service}'
            time_delta= certificate_decode(server) - datetime.date.today()
            final_alert=certificate_decode(server)- alert_needed_on
            return HttpResponse(f'<h1>Alert! Alert! your certificates are expiring in {time_delta.days} days for {service} service, please renew ASAP!!</h1>')
    else:
        return render(request, 'certexp/serverinfo.html', {'form': form})
    