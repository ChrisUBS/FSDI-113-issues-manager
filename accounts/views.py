from django.views.generic import CreateView, FormView, TemplateView
from .forms import CustomUserCreationForm, CustomPasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

class signUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

class CustomPasswordChangeView(LoginRequiredMixin, FormView):
    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        # messages.success(self.request, 'Your password has been successfully updated.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors in the form.')
        return super().form_invalid(form)

class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/password_change_done.html"