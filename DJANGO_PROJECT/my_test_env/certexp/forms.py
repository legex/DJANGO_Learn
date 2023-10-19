from django import forms

class ServerCertificateForm(forms.Form):
    operation=forms.CharField(required=True, label='Enter Server to be operated (EX: expressway, cms, mutare, ucm)')
    server=forms.CharField(required=False)
    alert_day=forms.DateField()
    service=forms.CharField(required=False, label='Enter Service Type (Example: tomcat, CallManager)')

    class Meta():
        fields =['operation','server','Days']