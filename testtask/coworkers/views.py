from django.shortcuts import render

from coworkers.models import Coworker


def main_page(request):
    root_coworkers = Coworker.objects.filter(parent_id__isnull=True).order_by('pib')
    show_list = []
    for root_coworker in root_coworkers:
        show_list.append([root_coworker.serialize_short(), root_coworker.get_descendants().filter(level=1).order_by('pib')])
    return render(request, template_name='hierarchy.html', context={'coworkers': show_list})

