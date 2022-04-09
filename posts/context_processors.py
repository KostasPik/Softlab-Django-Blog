from .models import  Tag
from newsletter.forms import NewsletterSubscriberForm
from .forms import ContactUsForm


# def get_categories(request):
#     categories = Category.objects.all()
#     return {'categories': categories}


def get_tags(request):
    tags = Tag.objects.all()
    return {'tags': tags}
    

def newsletter_form(request):
    newsletter_form = NewsletterSubscriberForm()
    return {
        'newsletter_form': newsletter_form
    }

def feedback_form(request):
    contactus_form = ContactUsForm()
    return {'contactus_form': contactus_form}
