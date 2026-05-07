from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin): # LoginRequiredMixin cause you can't have a role without being logged in anyways
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if self.required_role is None:
            raise ValueError("Hi! Please remember to have `required_role = [role name]` in your code. You can see the role names in accounts/models.py")

        if request.user.profile.role != self.required_role:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)