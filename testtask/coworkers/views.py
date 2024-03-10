from django.shortcuts import render

from coworkers.models import Coworker


def main_page(request):
    return render(request, template_name='main_page.html', context={'coworkers': []})
