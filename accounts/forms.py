from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
   
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

   
    def clean_email(self):
        email = self.cleaned_data['email']

        dup_email = CustomUser.objects.filter(email=email, email_verified=True)
        if dup_email.exists():
            raise forms.ValidationError('Account with this email address already exists.')
        return email.lower()



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

