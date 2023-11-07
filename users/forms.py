from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from users.models import Profile


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})


class SignupForm(forms.Form):
    error_css_class = "invalid-feedback"
    username = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    password = forms.CharField(
        max_length=70, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password_confirmation = forms.CharField(
        max_length=70, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError("Username is already in use.")
        return username

    def clean(self):
        data = super().clean()

        password = data["password"]
        password_confirmation = data["password_confirmation"]

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")

        return data

    def save(self):
        data = self.cleaned_data
        data.pop("password_confirmation")

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()
