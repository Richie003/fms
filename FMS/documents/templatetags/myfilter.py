from django import template
from django.db.models import Q
from django.http import HttpResponseRedirect, request
from django.shortcuts import redirect
from django.template.defaultfilters import stringfilter
from accounts.models import UserBio
from django.urls import reverse

from documents.models import *
from documents.forms import FolderDataForm

register = template.Library()


@register.filter(safe=True)
def truncate(value):
    value = value
    if len(value) > 10:
        trunc = value[0:10]
    else:
        trunc = value
    return trunc


@register.filter(autoescape=True, is_safe=True)
@stringfilter
def get_objects(value):
    query = FileTable.objects.filter(associate_folder=value)
    # if value:
    #     new = query.filter(
    #         Q(associate_folder__icontains=value)
    #     )
    return query


@register.inclusion_tag('documents/bio.html', takes_context=True)
def bio(context):
    request_user = context['request'].user
    bios = UserBio.objects.get(user=request_user)
    # print(bios)
    return {'bios': bios}

@register.inclusion_tag('documents/folder_form.html', takes_context=True)
def folder_creation(context):
    request_user = context['request'].user
    # print(request_user)
    post_requests = context['request'].POST
    method_requests = context['request'].method
    # files_requests = context['request'].FILES
    form = FolderDataForm
    if method_requests == 'POST':
        if 'folder-add' in post_requests:
            form = FolderDataForm(post_requests or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request_user
                instance.save()
            return redirect('/')
    return {'form': form}
