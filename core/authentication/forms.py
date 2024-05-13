from django import forms
from django.contrib.auth.models import User, Permission
from django.db.models import Q

class UserForm(forms.ModelForm):
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        permissions_choices = []
        permissions = Permission.objects.filter(
            Q(content_type__model='user') |
            Q(content_type__app_label='meetings') |
            Q(content_type__app_label='employee') 
        )

        for perm in permissions:
                
            if 'Can add' in perm.name:
                text = perm.name.replace('Can add', 'Agregar')
            elif 'Can change' in perm.name:
                text = perm.name.replace('Can change', 'Actualizar')
            elif 'Can delete' in perm.name:
                text = perm.name.replace('Can delete', 'Eliminar')
            elif 'Can view' in perm.name:
                text = perm.name.replace('Can view', 'Visualizar')
            else:
                text = perm.name
            
            if 'user' in perm.name:
                text = text.replace("user", "Usuario")
            
            permissions_choices.append((perm.id, text))

        self.fields['user_permissions'].choices = permissions_choices

    class Meta:
        model = User
        fields = ("username",'first_name','last_name', "email","password", "user_permissions")
        labels = {
            "username": "Nombre De Usuario",
            "first_name" : "Nombre",
            "last_name" : "Apellidos",
            "email": "Correo Electronico",
            "password": "Contraseña",
            "user_permissions": "Permisos"
        }
        widgets = {
            "password": forms.PasswordInput(render_value=True),
            "user_permissions": forms.CheckboxSelectMultiple()
        }
        
        help_texts = {
            "user_permissions" :"Permisos específicos para este usuario."
        }
        
    def save(self, commit=True):
        data = self.data or {}
        form = super()

        try:
            if form.is_valid():
                u = form.save(commit=False)
                psw = self.cleaned_data.get("password")

                if u.pk is None:
                    u.set_password(psw)

                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != psw:
                        u.set_password(psw)
                u.save()
                
                u.user_permissions.clear()
                user_permissions = self.cleaned_data.get('user_permissions')
                for g in user_permissions:
                    u.user_permissions.add(g)
                    
        except Exception as e:
            data["error"] = str(e)

        return data
