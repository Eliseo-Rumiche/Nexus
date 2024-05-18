from django import forms
from core.employee.models import Position, Field, Worker


class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = "__all__"


class FieldForm(forms.ModelForm):

    class Meta:
        model = Field
        fields = "__all__"


class DateInput(forms.DateInput):
    input_type = "date"


class WorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = [
            "name",
            "last_name",
            "phone_number",
            "email",
            "address",
            "birth_date",
            "field",
            "position",
            "facebook_url",
            "instagram_url",
            "status",
        ]
        widgets = {"birth_date": DateInput}
