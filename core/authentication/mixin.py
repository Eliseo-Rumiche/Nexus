from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    permission : str = None
    redirect_perm_url : str = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        if self.permission : 
            if not  request.user.has_perm(self.permission):
                return redirect(self.redirect_perm_url or 'meeting')
                
        return super().dispatch(request, *args, **kwargs)