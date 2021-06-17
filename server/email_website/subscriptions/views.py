from django.http import HttpResponse, Http404

from django.template import loader

from .models import Subscription, FormData

from django.shortcuts import get_object_or_404, render

from datetime import datetime

def index(request):
    latest_subscription_list = Subscription.objects.order_by('-pub_date')[:5]
    template = loader.get_template('subscriptions/index.html')
    context = {
        'latest_subscription_list': latest_subscription_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, subscription_id):
	subscription = get_object_or_404(Subscription, pk=subscription_id)
	return render(request, 'subscriptions/detail.html', {'subscription': subscription})


def form(request, api_key):
	try:
		subscription = Subscription.objects.get(api_key=api_key)
	except:
		return HttpResponse('YOUR_API_KEY is not recognised. Please get a key on your profile page at https://email-website.com and use it.')
	if request.method == 'POST':
		post_data = request.POST.dict()
		post_data.pop("csrfmiddlewaretoken", None)
		form_data = FormData(subscription = subscription, form_data = str(post_data), send_date=datetime.now())
		form_data.save()
	else:
		post_data = None
	return render(request, 'subscriptions/form.html', {
		'subscription': subscription,
		'post_data': post_data,
        'api_key': api_key
    })