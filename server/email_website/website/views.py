from django.http import HttpResponse, Http404

from django.template import loader

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import login, authenticate


# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.


def home(request):
    template = loader.get_template('website/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def signup(request):
	template = loader.get_template('website/signup.html')
	context = {}

	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')

		# return HttpResponse(template.render(context, request))
		
	else:
		form = UserCreationForm()
	return render(request, 'website/signup.html', {'form': form}) 
		# user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		# user.save()
	# return render(request, 'subscriptions/form.html', {
	# 	'subscription': subscription,
	# 	'post_data': post_data,
 #        'api_key': api_key
 #    })