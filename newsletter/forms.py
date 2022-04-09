from django.db.models.fields import CharField
from django.forms import ModelForm
from django import forms
from .models import NewsletterSubscriber
import time


class NewsletterSubscriberForm(ModelForm):
    honeypot = forms.CharField(max_length=50,widget=forms.TextInput(attrs={"type":"hidden", "required": 'False', 'id':"honeypot"}), required=False) #   honeypot helps avoid spamming by bots.
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']


    

    def __init__(self, *args, **kwargs):
        super(NewsletterSubscriberForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = "Recipient's email"
        self.fields['email'].widget.attrs['id'] = 'newsletter-email'
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['email'].widget.attrs['required'] = 'true'
        