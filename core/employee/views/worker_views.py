from typing import Any
from django.views.generic  import ListView
from core.employee.models import Worker
from core.employee.forms import WorkerForm
from django.http.response import JsonResponse

class WorkerView(ListView):
    template_name = "worker.html"
    model = Worker
    context_object_name = "workers"
    
    
    def post(self, request):
        data = {}
        try:
            action = request.POST["action"]

            if action == "active_disactive":
                worker = Worker.objects.get(id=request.POST["id"])
                worker.status = not worker.status
                worker.save()

            elif action == "detail":
                worker = Worker.objects.get(id=request.POST["id"])
                data["data"] = worker.toJson()
                
            elif action == "deleted":
                worker = Worker.objects.get(id=request.POST["id"])
                worker.delete()

            elif action in ["add", "edit"]:
                if action == "add":
                    form = WorkerForm(request.POST)
                else:
                    instance = Worker.objects.get(id=request.POST["id"])
                    form = WorkerForm(request.POST, instance=instance)

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
        context['Form'] = WorkerForm
        context['model'] = 'Trabajador'
        return context
    

    
    
