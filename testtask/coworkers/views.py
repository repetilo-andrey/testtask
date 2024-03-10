from django.shortcuts import render

from coworkers.models import Coworker


def main_page(request):
    a = Coworker.objects.filter(headman_id__isnull=True).first().get_family()
    print (a)
    return render(request, template_name='main_page.html', context={'coworkers': []})
