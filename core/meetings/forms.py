from django import forms
from core.meetings.models import Meeting, Attendance
from core.employee.models import Worker

select_choices = (
    (0, "No"),
    (1, "Si"),
)


class DateTimeInput(forms.DateInput):
    input_type = "datetime-local"


class MeetingForm(forms.ModelForm):

    organizer = forms.ModelChoiceField(
        label="Organizador",
        queryset=Worker.objects.filter(
            position__name__icontains="director", status=True
        ),
    )

    class Meta:
        model = Meeting
        fields = "__all__"
        widgets = {"date": DateTimeInput}

    def save(self, commit=True):
        if not commit:
            return meeting

        meeting: Meeting = super().save(commit=False)
        workers = Worker.objects.filter(status=True)
        if self.cleaned_data["type"] == "A":
            workers = workers.filter(field=self.cleaned_data["field"])

        elif self.cleaned_data["type"] == "D":
            workers = workers.filter(position__name__icontains="director")

        if meeting.pk is not None:

            meet = Meeting.objects.get(pk=meeting.pk)
            if meet.type == "A" and meeting.type == "A" and meet.field == meeting.field:
                meeting.save()
                return meeting

            if meet.type == meeting.type and meeting.type != "A":
                meeting.save()
                return meeting

        meeting.save()
        Attendance.objects.filter(meeting=meeting).delete()
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
            self.add_error("field", "Selecione área.")


class AddAttendanceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.meeting_pk = kwargs.pop("meeting_pk", None)
        super().__init__(*args, **kwargs)
        self.fields["workers"] = forms.ModelMultipleChoiceField(
            label="Trabajadores",
            queryset=Worker.objects.filter(status=True).exclude(
                attendance__meeting__pk=self.meeting_pk
            ),
        )
