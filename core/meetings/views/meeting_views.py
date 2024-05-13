from typing import Any
from django.views.generic  import ListView
from core.meetings.models import Meeting
from core.meetings.forms import MeetingForm
from django.http.response import JsonResponse
from core.authentication.mixin import LoginRequiredMixin
from core.authentication.utils import ValidatePermission

class MeetingView(LoginRequiredMixin,ListView):
    template_name = "meeting.html"
    model = Meeting
    context_object_name = "meetings"
    permission = "meetings.view_meeting"
    
    
    def post(self, request):
        data = {}
        try:
            action = request.POST["action"]

            if action == "active_disactive":
                ValidatePermission("meetings.change_meeting",request)
                meetings = Meeting.objects.get(id=request.POST["id"])
                meetings.status = not meetings.status
                meetings.save()

            elif action == "detail":
                ValidatePermission("meetings.change_meeting",request)
                meetings = Meeting.objects.get(id=request.POST["id"])
                data["data"] = meetings.toJson()
                
            elif action == "deleted":
                ValidatePermission("meetings.delete_meeting",request)
                meetings = Meeting.objects.get(id=request.POST["id"])
                meetings.delete()

            elif action in ["add", "edit"]:
                if action == "add":
                    ValidatePermission("meetings.add_meeting",request)
                    form = MeetingForm(request.POST)
                else:
                    ValidatePermission("meetings.change_meeting",request)
                    instance = Meeting.objects.get(id=request.POST["id"])
                    form = MeetingForm(request.POST, instance=instance)

                if form.is_valid():
                    form.save()
                else:
                    data["error"] = form.errors

            else:
                raise Exception("accion no encontrada")

        except Exception as e:
            data["error"] = str(e)
        
        return JsonResponse(data)
                    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['Form'] = MeetingForm
        context['model'] = 'Reunión'
        return context
    

    
    
