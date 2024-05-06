from typing import Any
from django.views.generic  import ListView
from core.employee.models import Field
from core.employee.forms import FieldForm
from django.http.response import JsonResponse

class FieldView(ListView):
    template_name = "field.html"
    model = Field
    context_object_name = "fields"
    
    
    def post(self, request):
        data = {}
        try:
            action = request.POST["action"]

            if action == "active_disactive":
                field = Field.objects.get(id=request.POST["id"])
                field.status = not field.status
                field.save()

            elif action == "detail":
                field = Field.objects.get(id=request.POST["id"])
                data["data"] = field.toJson()
                
            elif action == "deleted":
                field = Field.objects.get(id=request.POST["id"])
                field.delete()

            elif action in ["add", "edit"]:
                if action == "add":
                    form = FieldForm(request.POST)
                else:
                    instance = Field.objects.get(id=request.POST["id"])
                    form = FieldForm(request.POST, instance=instance)

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
        context['Form'] = FieldForm
        context['model'] = 'Área'
        return context
    

    
    
