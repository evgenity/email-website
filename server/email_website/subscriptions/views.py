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

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def send_email(receiver_email, msg):
	port = 465  # For starttls
	smtp_server = "smtp.gmail.com"
	sender_email = "email.website.form@gmail.com"
	password = 'qecmid-pagwan-jodmA4'
	context = ssl.create_default_context()

	message = MIMEMultipart("alternative")
	message["Subject"] = "Form comleted"
	message["From"] = sender_email
	message["To"] = receiver_email

	# Create the plain-text and HTML version of your message
	text = """\
	Hi,
	How are you?"""

	html = """\
	<html>
	  <body>
	    <p>Hi,<br>
	       {}
	    </p>
	  </body>
	</html>
	""".format(msg)
	print(html)

	# Turn these into plain/html MIMEText objects
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)
	message.attach(part2)

	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message.as_string())
	pass

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
		send_email(receiver_email=subscription.email, msg=str(post_data))
	else:
		post_data = None
	return render(request, 'subscriptions/form.html', {
		'subscription': subscription,
		'post_data': post_data,
        'api_key': api_key
    })