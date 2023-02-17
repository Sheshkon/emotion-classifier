from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required

from accounts.forms import UserCreationForm, PasswordResetForm, UpdateUserForm, UpdateProfileForm
from calcs.models import ImageClassifier


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration/signup.html'


class LoginView(LoginView):
    template_name = 'accounts/registration/login.html'
    success_url = reverse_lazy('home')


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'


class PasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'accounts/registration/password_reset_form.html'


@login_required()
def profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='accounts-profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        calcs_image_count = ImageClassifier.objects.filter(profile_id=request.user.profile).count()

    return render(request, 'accounts/profile.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'calcs_image_count': calcs_image_count})
