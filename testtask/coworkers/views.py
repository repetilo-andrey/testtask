import random

from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from coworkers.forms import CoworkerForm
from coworkers.models import Coworker


def hierarchy(request):
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

    coworkers = Coworker.objects.all().select_related('parent')
    if search:
        coworkers = coworkers.filter(Q(pib__icontains=search) | Q(start_date__icontains=search) |
                                     Q(position__icontains=search) | Q(email__icontains=search) |
                                     Q(parent__pib__icontains=search))

    sort = '-' + sort if order == 'desc' else sort
    coworkers = coworkers.order_by(sort)

    total = coworkers.count()
    coworkers = coworkers[offset:limit + offset]
    editable = request.user.is_authenticated
    return Response({'total': total, 'rows': [coworker.serialize(editable=editable) for coworker in coworkers]},
                    status=status.HTTP_200_OK)


def coworker_view(request, coworker_id=None):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    coworker = None
    if coworker_id:
        coworker = get_object_or_404(Coworker, pk=coworker_id)
    if request.method == 'POST':
        form = CoworkerForm(request.POST, instance=coworker)
        if form.is_valid():
            if coworker_id:
                if coworker.parent != form.cleaned_data.get('parent'):
                    # move lower_coworkers to another parents
                    manage_lower_coworkers(coworker)
                form.save()
            else:
                coworker = form.save()
            return redirect(reverse('coworker_edit_view', args=[coworker.id]))
    else:
        form = CoworkerForm(instance=coworker)
    return render(request, 'coworker_form.html', {'form': form})


def coworker_delete_view(request, coworker_id=None):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    coworker = None
    if coworker_id:
        coworker = get_object_or_404(Coworker, pk=coworker_id)
    if request.method == 'POST':
        # move lower_coworkers to another parents
        manage_lower_coworkers(coworker)
        coworker.delete()
        return redirect('table_data')
    return redirect(reverse('coworker_edit_view', args=[coworker_id]))


def manage_lower_coworkers(coworker):
    lower_coworkers = coworker.get_descendants().filter(level__gt=coworker.level)
    new_parents = find_new_parents(coworker)
    for lower_coworker in lower_coworkers:
        lower_coworker.parent = random.choice(new_parents)


def find_new_parents(coworker):
    if coworker.is_root_node():
        same_lvl = Coworker.objects.filter(level=0)
    else:
        same_lvl = coworker.get_family()().filter(level=coworker.level)
        if len(same_lvl) == 0:
            same_lvl = coworker.get_family()().filter(level__lt=coworker.level)
    return list(same_lvl)
