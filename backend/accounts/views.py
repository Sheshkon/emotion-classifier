from accounts.forms import UserCreationForm, PasswordResetForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import PasswordResetView


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class PasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset_form.html'
