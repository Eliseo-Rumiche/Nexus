from django.contrib import admin
from core.employee.models import Worker,Field, Position

# Register your models here.

# admin.site.register(Worker)

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    list_filter = ('position','status','field')
    ordering = ('name',)
    
    
admin.site.register(Position)