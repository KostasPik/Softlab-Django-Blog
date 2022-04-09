
from django.contrib.auth import login
from django.core import mail
from django.forms import ValidationError
from django.http import request
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Post, Tag, Comment
from newsletter.models import NewsletterSubscriber
from http import HTTPStatus
from .utils import make_token
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
# from .tests import test, delete_all_post_objects, populate_course_db

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.validators import validate_email

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT) # cache timeout (Caching is not yet enabled).



#django postgres dependencies BEGIN
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank,SearchVector
#django postgres dependencies END




def home(request):
    posts = Post.objects.filter(published=True).defer('post_time','published', 'related_posts').prefetch_related('tags')[:19] # return last 19 posts
    context = {
        'posts': posts,
    }
    return render(request, 'home.html', context)


def search(request):
    if not 'keyword' in request.GET: # if we don't have a keyword search query.
        return redirect('home')
    
    keyword = request.GET['keyword'] #  if we have a keyword search query.
    
    if not keyword: # if keyword string is empty.
        return redirect('home')
    
    #if we actually have a search keyword...
    posts = Post.objects.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword)).order_by("-post_time")
    paginator = Paginator(posts, per_page=5) # paginate data 
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'posts.html', {"posts": page_obj, 'page_obj':page_obj, "keyword": keyword})



def posts(request, tag_slug=None):   

    if tag_slug: # if we want all posts that have a specific tag ....
        tag = Tag.objects.filter(slug=tag_slug).first() # get the tag (we want to display the name and we only have the slug)
        tag_name = tag.name
        posts = Post.objects.filter(tags__slug__in=[tag_slug]).defer('body').order_by("-post_time").all() # get all posts that have the specific tag
    else: #if we want all posts in general 
        posts = Post.objects.defer('body').order_by("-post_time").all() # get all posts
        tag_name = None # the user didn't ask for specific tag posts

    paginator = Paginator(posts, per_page=5) # paginate data
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)

    return render(request, 'posts.html', {"posts": paged_posts, 'page_obj': paged_posts,'tag': tag_name})



def post_details(request, post_slug): # read a specific post
    post = Post.objects.filter(slug=post_slug, published=True).first()
    comments = Comment.objects.filter(post__slug=post_slug, active=True).all() # get all comments of the specific post that are visible.
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_details.html', context)


# def get_post_comments(request, post_slug):
#     comments = Comment.objects.filter(post__slug=post_slug, active=True).all()  
#     return comments





@csrf_exempt
def new_subscriber(request):   

    if not request.method == "POST":
        return redirect('home')
    
    if request.POST.get('honeypot', None): # if honeypot field has a value, then that means that a bot submitted the form.
        return JsonResponse({'msg': 'You must be a bot.'}, status=HTTPStatus.OK)
    
    email = request.POST.get('email', None).strip().lower() # sanitize input
    newsletter_check_dup = NewsletterSubscriber.objects.filter(email=email, email_verified=True) # check if the emails is already confirmed and saved in the db.

    if newsletter_check_dup.exists():
        return JsonResponse({'msg': 'Subscriber with this email already exists.'}, status=HTTPStatus.OK)

    try:
        validate_email(email) # is the email valid?
        subscriber = NewsletterSubscriber(email=email, email_verified=False)
    except ValidationError:
        return JsonResponse({'msg': 'There is a problem with the email you provided.'}, status=HTTPStatus.OK)

    token = make_token(email, subscriber.pk) # make the verification token
    current_site = get_current_site(request)
    mail_subject = 'Confirm Subscription To Our Site'
    message = render_to_string('newsletter/newsletter_activation_template.txt', {
        'subscriber': subscriber,
        'domain': current_site.domain,
        'token': token,
        'email': email,
    })
    subscriber.token = token
    subscriber.save() # save the entry in the database.
    to_email = email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send() # send the email for verification.
    return JsonResponse({'msg': 'Please confirm your email by clicking the link we sent to your email.'}, status=HTTPStatus.OK)
    #email sending end






def activate_newsletter_subscription(request, email, token):
    try:
        user = NewsletterSubscriber.objects.filter(email=email, token=token, email_verified=False) # try to find the entry.
    except(TypeError, ValueError, OverflowError, NewsletterSubscriber.DoesNotExist):
        user = None
    
    if not user:
        return HttpResponse('Activation link is invalid!')
    
    # if user exists....
    user.email_verified = True # if the entry exists then verify the email.
    user.update(token=None, email_verified=True)
    not_confirmed_users = NewsletterSubscriber.objects.filter(email=email, email_verified=False).all().delete() #delete all users that had made an entry with that email but had not confirmed their email subsciption.
    # now each verified email is unique in the database.
    return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    

    

def add_comment(request, post_pk):

    if not request.method == 'POST':
        return redirect('home')
    
    honeypot = request.POST.get('honeypot', None) # if honeypot field has a value then a bot submitted the form.

    if honeypot:    
        return JsonResponse({'msg': 'You must be a bot.'}, status=HTTPStatus.OK)

    name = request.POST.get('name', None).strip().title()
    body = request.POST.get('body', None).strip()
    parent_pk = request.POST.get('parent_pk', None) # does it have a parent, meaning is it a reply to some other comment?

    if not len(body) > 5: # if comment body is not longer than 5 chars.
        return JsonResponse({'msg': 'Comment length must be longer than 5 characters.'}, status=HTTPStatus.OK)


    post = Post.objects.filter(pk=post_pk).first()

    if not post: #if post doen't exist
        return JsonResponse({'msg': 'Post not found.'}, status=HTTPStatus.OK)

    if parent_pk: # if it is a reply.... (has a parent)
        parent_pk = int(parent_pk)
        parent_comment = Comment.objects.filter(pk=parent_pk).first()
        Comment.objects.create(name=name, post=post, body=body, active=True , parent=parent_comment)
        return JsonResponse({'msg': 'Comment Created'}, status=HTTPStatus.OK)
    else:
        Comment.objects.create(name=name, post=post, body=body, active=True , parent=None)
        return JsonResponse({'msg': 'Comment Created'}, status=HTTPStatus.OK)






        

from .forms import PostCreationForm



from .forms import ContactUsForm, contactus_subjects

@csrf_exempt
def contact_us(request): 

    if not request.method == 'POST':
        contactus_form = ContactUsForm()
        return render(request, 'contact_us/contact_us.html' ,{'contactus_form': contactus_form})

    contactus_honeypot = request.POST.get('contactus_honeypot', None)
    if contactus_honeypot:
        return JsonResponse({'msg': 'You must be a bot.'}, status=HTTPStatus.OK)

    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    subject = request.POST.get('subject', None)
    contactus_body = request.POST.get('body', None).strip()

    if not contactus_body or not len(contactus_body)>10:
        return JsonResponse({'msg':'Feedback body needs to be longer than 10 characters.'}, status=HTTPStatus.OK)


    #check if subject is in the list begin
    valid_subject = False                       # check if the subject is valid ( is one of the available options )
    for list_subject in contactus_subjects:
        if subject == list_subject:
            mail_subject = subject
            valid_subject = True
            break
    if not valid_subject:
        return JsonResponse({'msg': 'Something went wrong, please refresh and try again. Thank you for your patience.'})
    #check if subject is in the list end


    message = render_to_string('contact_us/contactus_email_template.txt', {
                'name': name,
                'body': contactus_body,  
                'email': email,
            })
    to_email = 'konpython@gmail.com'
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return JsonResponse({'msg':'Thank you so much for contacting us, it means the world to us. Have a great day!'}, status=HTTPStatus.OK)


#stripe begin


import json
import stripe
stripe.api_key = getattr(settings, "STRIPE_API_KEY")



def buy_coffee(request): # buy me a coffee for the article. Implementation using the stripe API.

    intent = stripe.PaymentIntent.create(
        amount = 1099, #cents
        currency = "eur",
        automatic_payment_methods = {"enabled": True},
    )

    context = {
        'price': None,
        'image_url': None,
        'client_secret': intent.client_secret,
        'success_url': 'http://127.0.0.1:8000/success/',
    }

    return render(request, 'buy_coffee/checkout.html', context)




def buy_coffee(request):
    if request.method == 'POST':
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Buy the author a coffee.',
                        'images': ['https://cdn-icons-png.flaticon.com/512/184/184483.png'],
                        'description': 'Coffee helps me write tutorials that you read and enjoy! If you like them, and want to see more of them feel free to buy me a coffee!',
                    },
                    'unit_amount': 200,
                },
                'quantity': 1,
                'adjustable_quantity': {
                        'enabled': True,
                    },
            }],
            mode='payment',
            success_url = 'http://127.0.0.1:8000/buy_coffee/success/',
            cancel_url = 'http://127.0.0.1:8000/',
        )
        return redirect(session.url)


def checkout(request):
    intent = stripe.PaymentIntent.create(
        amount = 1099, #cents
        currency = "eur",
        automatic_payment_methods = {"enabled": True},
    )
    context = {
        'client_secret': intent.client_secret,
        'success_url': 'http://127.0.0.1:8000/success/',
    }
    return render(request, 'stripe/checkout.html', context)

def success(request):
    return render(request, 'stripe/success.html', {})

def coffee_success(request):
    return render(request, 'buy_coffee/success.html', {})



#stripe end


