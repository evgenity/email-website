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
    subscription = Subscription.objects.filter(api_key=api_key)[0]
    post_data = request.POST.dict()
    post_data.pop("csrfmiddlewaretoken", None)
    if request.method == 'POST':
    	form_data = FormData(subscription = subscription, form_data = str(post_data), send_date=datetime.now())
    	form_data.save()
    return render(request, 'subscriptions/form.html', {
        'subscription': subscription,
        'error_message': post_data,
        'api_key': api_key
    })