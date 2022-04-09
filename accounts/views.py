from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib import messages #import messages
from django.core.mail import EmailMessage
from django.urls import reverse

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

import json
def signup(request):

	if not request.method == 'POST': 
		form = CustomUserCreationForm()
		return render(request, 'registration/signup.html', {'form': form})


	# if method is POST
	 
	form = CustomUserCreationForm(request.POST) # initialize form

	if not form.is_valid():
		err = form.errors
		return reverse('signup', json.dumps({
			'err': err,
		}))
	
	# form is valid...

	user = form.save(commit=False)
	user.email_verified = False
	user.save()
	current_site = get_current_site(request)
	mail_subject = 'Activate your account.'
	message = render_to_string('registration/activate_account.html', {
		'user': user,
		'domain': current_site.domain,
		'uid':urlsafe_base64_encode(force_bytes(user.pk)),
		'token':account_activation_token.make_token(user),
	})
	to_email = form.cleaned_data.get('email')
	email = EmailMessage(
		mail_subject, message, to=[to_email]
	)
	email.send()
	messages.success(request, 'Confirm Email')
	return redirect('signup')	




from django.shortcuts import render, redirect
from django.core.mail import message, send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from .models import CustomUser
from django.contrib import messages #import messages





from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.vary import vary_on_cookie
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Pythonista',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'konpython@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					# return redirect("home")
			else:
				messages.error(request, "No users associated with this email address found.Please ensure that the address you typed is correct!")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        login(request, user)
        user_dup_check = CustomUser.objects.filter(email=user.email, email_verified=False).all() # check if there are multiple not confirmed emails
        user_dup_check.delete()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')