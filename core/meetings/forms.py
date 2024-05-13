from django import forms
from core.meetings.models import Meeting, Attendance
from core.employee.models import Worker

select_choices = (
    (0, 'No'),
    (1, 'Si'),
)

class DateInput(forms.DateInput):
    input_type = 'date'
       
    
    
class MeetingForm(forms.ModelForm):
    
    
    send_notification = forms.BooleanField(
        required=False,
        widget=forms.Select(choices=select_choices),
        label="Enviar Notificación (Whatsapp)",
        help_text="Proximamente ...."
        )
    
    class Meta:
        model = Meeting
        fields = "__all__"
        widgets = {
            'date': DateInput
        }

    def save(self, commit=True):
        if not commit:
            return meeting
            
        meeting: Meeting = super().save(commit=False)
        
        workers = Worker.objects.filter(status = True)
        if self.cleaned_data['type'] == "A":
            workers = workers.filter(field = self.cleaned_data['field'] )
            
        elif self.cleaned_data['type'] == "D":
            workers = workers.filter(position__name__icontains="director")
        
        meeting.save()
        
        if self.cleaned_data['type'] != meeting.type:
            Attendance.objects.filter(meeting = meeting).delete()    
            for worker in workers:
                attendance = Attendance()
                attendance.meeting = meeting
                attendance.worker = worker
                attendance.save()
            
        return meeting

    def clean(self):
        cleaned_data = super().clean()  
        
        meeting_type = cleaned_data.get("type")
        field = cleaned_data.get("field")
        if meeting_type == "A" and field == None:
            self.add_error('field', 'Selecione área.')
