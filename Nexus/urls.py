"""
URL configuration for Nexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from core.employee.views.worker_views import WorkerView, WorkerDetailView
from core.employee.views.position_views import PositionView
from core.employee.views.field_views import FieldView
from core.meetings.views.meeting_views import MeetingView
from core.meetings.views.attendance_views import AttendanceView
from core.authentication.views import Login, LogoutView, UserView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('', RedirectView.as_view(pattern_name='meeting')),
    
    path("worker/", WorkerView.as_view(), name="worker"),
    path("worker/<pk>", WorkerDetailView.as_view(), name="worker_detail"),
    path("position/", PositionView.as_view(), name="position"),
    path("field/", FieldView.as_view(), name="field"),
    path("meeting/", MeetingView.as_view(), name="meeting"),
    path("attendance/<int:pk>", AttendanceView.as_view(), name="attendances"),
    
    path("login/", Login.as_view(), name="Login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
