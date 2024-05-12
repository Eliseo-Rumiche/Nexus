from typing import Any
from django.views.generic  import ListView, DetailView
from core.employee.models import Worker
from core.meetings.models import Attendance
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
    

class WorkerDetailView(DetailView):
    model=Worker
    template_name = 'worker_detail.html'
    
    def get_attendances(self):
        return Attendance.objects.filter(worker = self.get_object())
    
    def get_present_attendances(self):
        return self.get_attendances().filter(status = "P")
    
    def get_absent_attendances(self):
        return self.get_attendances().filter(status = "A")
    
    def get_excused_attendances(self):
        return self.get_attendances().filter(status = "E")
    
    def get_unmarked_attendance(self):
        return self.get_attendances().filter(status = None)
    
    def get_chart_data(self):
        total_attendances = self.get_attendances().count()
        present_attendances = self.get_present_attendances().count()
        absent_attendances  = self.get_absent_attendances().count()
        excused_attendances = self.get_excused_attendances().count()
        unmarked_attendaces = self.get_unmarked_attendance().count()
        present_attendances =round((present_attendances *100)/ total_attendances,2)
        absent_attendances = round((absent_attendances*100)/total_attendances,2)
        excused_attendances = round((excused_attendances*100)/total_attendances,2)
        unmarked_attendaces = round((unmarked_attendaces *100)/total_attendances,2)
        
        data = {
            "labels": ['Presente', 'Ausente', 'Justificado', 'sin marcar'],
            "series": [present_attendances, absent_attendances, excused_attendances, unmarked_attendaces],
        }
        return data
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['total_attendances'] = self.get_attendances().count()
        context['chart_data'] = self.get_chart_data()
        context['present_attendances'] = self.get_present_attendances
        context['absent_attendances'] = self.get_absent_attendances
        context['excused_attendances'] = self.get_excused_attendances
        context['unmarked_attendances'] = self.get_unmarked_attendance
        context['last_attendances'] = self.get_attendances().order_by("-meeting__date")[:6]
        return context
        
    
