from typing import Any
from django.views.generic import TemplateView
from core.meetings.models import Attendance, Meeting
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from core.authentication.mixin import LoginRequiredMixin
from core.authentication.utils import ValidatePermission


class AttendanceView(LoginRequiredMixin,TemplateView):
    template_name = "attendance.html"
    permission = "meetings.view_attendance"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            worker = request.POST["worker"]
            attendance = self.get_attendances().filter(worker=worker)
            if attendance.exists():
                ValidatePermission("meetings.change_attendance", request)
                attendance = attendance.first()
                attendance.status = request.POST["status"]
                attendance.save()
            else:
                raise Exception("Error al marcar asistencia")

        except Exception as e:
            data["error"] = str(e)

        return JsonResponse(data)

    def get_meeting(self):
        return get_object_or_404(Meeting, pk=self.kwargs["pk"])

    def get_attendances(self):
        return Attendance.objects.filter(meeting=self.kwargs["pk"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["meeting"] = self.get_meeting()
        data["attendances"] = self.get_attendances()
        return data
