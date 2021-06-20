from django.http import HttpResponse, Http404

from django.template import loader

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import login, authenticate

import uuid

from subscriptions.models import Subscription

# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.
from datetime import datetime


def home(request):
	try:
		subscription = Subscription.objects.get(email=request.user.username)
		api_key = subscription.api_key
		print (api_key)
	except Exception as e:
		print (e)
		api_key = None
	template = loader.get_template('website/index.html')
	context = {
		'api_key' : api_key
	}
	return HttpResponse(template.render(context, request))

def create_subscription(user):
	subscription = Subscription(pub_date = datetime.now(), api_key = uuid.uuid4(), email = user.username)
	subscription.save()


def signup(request):
	template = loader.get_template('website/signup.html')
	context = {}
	error_msg = None

	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			create_subscription(user)
			return redirect('home')
		else:
			error_msg = form.errors
			form = UserCreationForm()
			

	else:
		form = UserCreationForm()
	return render(request, 'website/signup.html', {'form': form, 'error_msg': error_msg}) 
