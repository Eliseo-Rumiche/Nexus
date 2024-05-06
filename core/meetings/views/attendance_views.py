from typing import Any
from django.views.generic import TemplateView
from core.meetings.models import Attendance

class AttendanceView(TemplateView):
    template_name="attendance.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data =  super().get_context_data(**kwargs)
        data['attendances'] = Attendance.objects.filter(meeting = self.kwargs['pk'])
        return data
    
    