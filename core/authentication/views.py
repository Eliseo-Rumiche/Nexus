from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from typing import Any
from django.views.generic import ListView
from django.http.response import JsonResponse
from core.authentication.forms import UserForm
from django.forms import model_to_dict
from core.authentication.mixin import LoginRequiredMixin
from core.authentication.utils import ValidatePermission


# Create your views here.


class Login(LoginView):
    template_name = "login.html"


class UserView(LoginRequiredMixin,ListView):
    template_name = "user.html"
    model = User
    context_object_name = "users"
    permission ="auth.view_user"

    def post(self, request):
        data = {}
        try:
            action = request.POST["action"]

            if action == "active_disactive":
                ValidatePermission("auth.change_user", request)
                user = User.objects.get(id=request.POST["id"])
                user.is_active = not user.is_active
                user.save()

            elif action == "detail":
                ValidatePermission("auth.change_user", request)
                user = User.objects.get(id=request.POST["id"])
                json = model_to_dict(
                    user,
                    {"username", "first_name", "last_name", "email", "password", "id"},
                )
                json["user_permissions"] = [p.pk for p in user.user_permissions.all()]
                data["data"] = json

            elif action == "deleted":
                ValidatePermission("auth.delete_user", request)
                user = User.objects.get(id=request.POST["id"])
                user.delete()

            elif action in ["add", "edit"]:
                if action == "add":
                    ValidatePermission("auth.add_user", request)
                    form = UserForm(request.POST)
                else:
                    ValidatePermission("auth.change_user", request)
                    instance = User.objects.get(id=request.POST["id"])
                    form = UserForm(request.POST, instance=instance)

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
        context = super().get_context_data(**kwargs)
        context["Form"] = UserForm
        context["model"] = "Usuario"
        return context
