from typing import Any
from django.views.generic  import ListView
from core.meetings.models import Meeting
from core.meetings.forms import MeetingForm
from django.http.response import JsonResponse

class MeetingView(ListView):
    template_name = "meeting.html"
    model = Meeting
    context_object_name = "meetings"
    
    
    def post(self, request):
        data = {}
        try:
            action = request.POST["action"]

            if action == "active_disactive":
                meetings = Meeting.objects.get(id=request.POST["id"])
                meetings.status = not meetings.status
                meetings.save()

            elif action == "detail":
                meetings = Meeting.objects.get(id=request.POST["id"])
                data["data"] = meetings.toJson()
                
            elif action == "deleted":
                meetings = Meeting.objects.get(id=request.POST["id"])
                meetings.delete()

            elif action in ["add", "edit"]:
                if action == "add":
                    form = MeetingForm(request.POST)
                else:
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
        context['model'] = 'Reunion'
        return context
    

    
    
