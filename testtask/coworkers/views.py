from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from coworkers.models import Coworker


def main_page(request):
    root_coworkers = Coworker.objects.filter(parent_id__isnull=True).order_by('pib')
    show_list = []
    for root_coworker in root_coworkers:
        show_list.append([root_coworker.serialize_short(), root_coworker.get_descendants().filter(level=1).order_by('pib')])
    context = {'coworkers': show_list, 'more_coworkers_url': reverse('more_coworkers')}
    return render(request, template_name='hierarchy.html', context=context)


@api_view(['GET'])
def more_coworkers(request):
    obj_id = request.query_params.get('obj_id')
    coworker = Coworker.objects.filter(id=obj_id).first()
    if not coworker:
        return Response(status=status.HTTP_404_NOT_FOUND)
    lower_coworkers = coworker.get_descendants().filter(level__gt=coworker.level)
    data = {'coworkers': lower_coworkers, 'parent_id': obj_id}
    coworkers_html = render_to_string('hierarchy_more_coworkers.html', data)
    return Response({'html': coworkers_html}, status=status.HTTP_200_OK)


def table_data(request):
    return render(request, template_name='table_data.html', context={'table_data_json': reverse('table_data_json')})


@api_view(['GET'])
def table_data_json(request):
    search = request.query_params.get('search')
    offset = int(request.query_params.get('offset'))
    limit = int(request.query_params.get('limit'))
    sort = request.query_params.get('sort') or 'id'
    order = request.query_params.get('order')

    coworkers = Coworker.objects.all()
    if search:
        coworkers = coworkers.filter(Q(pib__icontains=search) | Q(start_date__icontains=search) |
                                     Q(position__icontains=search) | Q(email__icontains=search))

    if order == 'desc':
        sort = '-' + sort
    coworkers = coworkers.order_by(sort)

    total = coworkers.count()
    coworkers = coworkers[offset:limit + offset]
    return Response({'total': total, 'rows': [coworker.serialize(editable=True) for coworker in coworkers]}, status=status.HTTP_200_OK)
