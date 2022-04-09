from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from .models import Post
from django import forms

class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


contactus_subjects = ['Contact', 'Feeback', 'Post Recomendation']

CONTACTUS_FORM_CHOICES = [
    (subject, subject) for subject in contactus_subjects
]


class ContactUsForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'contactus_name'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'id': 'contactus_email'}))
    subject = forms.CharField(label='Subject', widget=forms.Select(attrs={'id': 'contactus_subject'},choices=CONTACTUS_FORM_CHOICES)) #is it a feedback, a recomendation or just wanting to contact the owner of the website
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={'id': 'contactus_body'}))
    contactus_honeypot = forms.CharField(widget=forms.TextInput(attrs={"type":"hidden", 'id':"contactus_honeypot"}), required=False) #  honeypot is used to avoid spamming by bots.


