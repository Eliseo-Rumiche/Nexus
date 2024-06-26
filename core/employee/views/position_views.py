from typing import Any
from django.views.generic  import ListView
from core.employee.models import Position
from core.employee.forms import PositionForm
from django.http.response import JsonResponse
from core.authentication.mixin import LoginRequiredMixin
from core.authentication.utils import ValidatePermission

class PositionView(LoginRequiredMixin,ListView):
    template_name = "position.html"
    model = Position
    context_object_name = "positions"
    permission = "employee.view_position"
    
    
    def post(self, request):
        data = {}
        try:
            action = request.POST["action"]

            if action == "active_disactive":
                ValidatePermission("employee.change_position",request)
                position = Position.objects.get(id=request.POST["id"])
                position.status = not position.status
                position.save()

            elif action == "detail":
                ValidatePermission("employee.change_position",request)
                position = Position.objects.get(id=request.POST["id"])
                data["data"] = position.toJson()
                
            elif action == "deleted":
                ValidatePermission("employee.delete_position",request)
                position = Position.objects.get(id=request.POST["id"])
                position.delete()

            elif action in ["add", "edit"]:
                if action == "add":
                    ValidatePermission("employee.add_position",request)
                    form = PositionForm(request.POST)
                else:
                    ValidatePermission("employee.change_position",request)
                    instance = Position.objects.get(id=request.POST["id"])
                    form = PositionForm(request.POST, instance=instance)

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
        context['Form'] = PositionForm
        context['model'] = 'Cargo'
        return context
    

    
    
