from django.core.exceptions import ValidationError
from django.forms import EmailField

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm


class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True,
                       help_text=_("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")

        return email
