from django.contrib import admin
from django.contrib.admin.decorators import register
# Register your models here.
from .models import NewsletterSubscriber


# admin.site.register(NewsletterSubscriber)


@register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'email_verified', 'date_joined']
    list_filter = ('email_verified', 'date_joined')
