from django.db import models

# Create your models here.


class NewsletterSubscriber(models.Model):
    email = models.EmailField(max_length=100)
    email_verified = models.BooleanField(default=False) #   is the subscriber verified by email?
    token = models.CharField(max_length=100, null=True) #   the verification token.
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
       
       verbose_name = 'Subscriber'
       verbose_name_plural = "Subscribers"

       indexes = [
            models.Index(fields=['email','email_verified']),
        ]

    def __str__(self):
        return self.email