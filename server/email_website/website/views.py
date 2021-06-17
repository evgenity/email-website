from django.http import HttpResponse, Http404

from django.template import loader

def home(request):
    template = loader.get_template('website/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))