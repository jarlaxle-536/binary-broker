from django.http import HttpResponse
from django.template import loader

def main(request):
    template = loader.get_template('main_page.html')
    context = dict()
    return HttpResponse(template.render(context, request))
