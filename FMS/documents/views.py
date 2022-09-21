from email import message
import json
import random

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import UserAdminCreationForm
from django.views.decorators.csrf import csrf_protect
from accounts.models import UserBio
from urllib.parse import quote_plus
from .models import FileData, Folder
from .forms import FileDataForm, FolderDataForm
import secrets
import urllib, mimetypes
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
import os
from django.template.defaultfilters import filesizeformat
# from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from wsgiref.util import FileWrapper
from django.contrib import messages


# Create your views here.
@csrf_protect
def index(request):
    user = request.user
    if user.is_authenticated:
        symbols = ['!', '@', '_', '*', '&', '%', '$', '#', '-', '(', ')']
        nums = random.randint(100, 300)
        symbol = random.choice(symbols)
        randomm = secrets.token_hex()
        randomm = '%s%s%s%s' % (symbol, randomm[:4], symbol, nums)
        folder_data = Folder.objects.all().filter(user=request.user)
        file_data = FileData.objects.all().filter(user=request.user, associate_folder='Images')
        folder_count = folder_data.count()
        # nums = secrets.token_urlsafe()
        form1 = UserAdminCreationForm
        form = FileDataForm
        form2 = FolderDataForm
        if request.method == 'POST':
            if 'user_create' in request.POST:
                form1 = UserAdminCreationForm(request.POST or None, request.FILES)
                if form1.is_valid():
                    username = form1.cleaned_data.get('username')
                    instance = form1.save(commit=False)
                    instance.ip = request.META['REMOTE_ADDR']
                    instance.save()
                    return redirect('login')
        # the files data
            if 'file-add' in request.POST:
                form = FileDataForm(request.POST or None, request.FILES)
                if form.is_valid():
                    file_doc = form.cleaned_data.get('file')
                    if file_doc is None:
                        messages.warning(request, 'No file selected')
                    else:
                        # content_type = file_doc.content_type.split('/')[0]
                        # print(content_type)
                        # if content_type in settings.CONTENT_TYPES:
                        #     if file_doc._size > settings.MAX_UPLOAD_SIZE:
                        #         return HttpResponse(f'{file_doc} Too big')
                        #     else:
                        instance = form.save(commit=False)
                        instance.user = user
                        instance.save()
                    return redirect('home')
            if 'folder-add' in request.POST:
                form2 = FolderDataForm(request.POST or None)
                if form2.is_valid():
                    instance = form2.save(commit=False)
                    instance.user = user
                    instance.save()
                    return redirect('home')
    # the end of the file datas
        context = {
            'folder_data': folder_data,
            'file_data': file_data,
            'form': form,
            'form2': form2,
            'form1': form1,
            'randomm': randomm,
            'folder_count': folder_count
        }
        return render(request, 'index/index.html', context)

    else:
        return redirect('login')

# Returns the folders belonging to logged in user
def get_folders(request):
    data=[]
    folder_data = Folder.objects.all().filter(user=request.user)
    for i in folder_data:
        item = {
            'name':i.folder,
            'created':i.created
        }
        data=data.append(item)
        return JsonResponse({'folder':data})
    return JsonResponse()

def remove_folder(request, pk):
    folder = Folder.objects.get(pk=pk)
    folder.delete()

    return HttpResponse('success', content_type='text/plain')

def remove_file(request, pk):
    file = FileData.objects.get(pk=pk)
    file.delete()

    return HttpResponse('success', content_type='text/plain')

def remove_all(request):
    if request.method == "POST":
        file_id = request.POST.getlist('checked-file')
        print(file_id)
        for i in file_id:
            file = FileData.objects.get(pk=i)
            file.delete()
            data = {
                'mssg': 'Done!'
            }
            return JsonResponse(data, safe=False)
    return redirect(f'/')

def folderItems(request, name):
    user = request.user
    folder_items = FileData.objects.filter(user = request.user, associate_folder=name)
    file_count = folder_items.count()
    context = {
        'folder_items': folder_items,
        'file_count': file_count
    }

    return render(request, 'index/files.html', context)

def download(request,file_name):
        file_path = settings.MEDIA_ROOT +'/'+ file_name
        file_wrapper = FileWrapper(open(file_path,'rb'))
        file_mimetype = mimetypes.guess_type(file_path)
        response = HttpResponse(file_wrapper, content_type=file_mimetype )
        response['X-Sendfile'] = file_path
        response['Content-Length'] = os.stat(file_path).st_size
        response['Content-Disposition'] = 'attachment; filename=%s' % str(file_name)
        return response