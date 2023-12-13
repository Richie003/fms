import uuid, random, urllib, mimetypes, os, secrets
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from accounts.forms import UserAdminCreationForm
from accounts.models import User
from django.views.decorators.csrf import csrf_protect
from .models import FileTable, FileData, Folder, Share, Notification, save_file, save_subfolder
from .forms import FileDataForm, FolderDataForm
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from .utils import sendEmail, datetime_converter

from django.conf import settings
from django.contrib import messages


# Create your views here.
@login_required
@csrf_protect
def index(request):
    """
        The `index` function retrieves folder and file data for a specific user, handles form submissions
        for adding files and folders, and renders the data and forms on the index.html template.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by the
        user. It contains information about the request, such as the user making the request, the method
        used (GET or POST), any data sent with the request, and more. In this code, the `request` object
        :return: a rendered HTML template called "index/index.html" with the context variables
        "folder_data", "file_data", "form", "form2", and "folder_count".
    """
    user = request.user
    folder_data = Folder.objects.all().filter(user=request.user)
    file_data = FileTable.objects.all().filter(
        user=request.user
    )
    folder_count = folder_data.count()
    form = FileDataForm
    form2 = FolderDataForm
    if request.method == "POST":
        # the files data
        if "file-add" in request.POST:
            form = FileDataForm(request.POST or None, request.FILES)
            if form.is_valid():
                file_doc = form.cleaned_data.get("file")
                extras = {
                    "user":request.user.id,
                    "folder":request.POST.get("associate_folder")
                }
                save_file(
                    file_doc, 
                    extras
                )
                if file_doc is None:
                    messages.warning(request, "No file selected")
                else:
                    instance = form.save(commit=False)
                    instance.user_id = request.user.id
                    instance.save()
                return redirect("home")
        if "folder-add" in request.POST:
            form2 = FolderDataForm(request.POST or None)
            if form2.is_valid():
                instance = form2.save(commit=False)
                instance.user = user
                instance.save()
                return redirect("home")
    # the end of the file datas
    context = {
        "folder_data": folder_data,
        "file_data": file_data,
        "form": form,
        "form2": form2,
        "folder_count": folder_count,
    }
    return render(request, "index/index.html", context)

# Returns the folders belonging to logged in user
def get_folders(request):
    data = []
    try:
        folder_data = sorted(Folder.objects.all().filter(user=request.user))
        print(folder_data)
        for i in folder_data:
            item = {"name": i.folder, "created": i.created}
            data = data.append(item)
            return JsonResponse({"folder": data}, safe=False)
    except Exception as e:
        return JsonResponse({'folder':'no folder yet'}, safe=False)
    return JsonResponse({'folder': 'No folder yet'})

def dropzone_file(request):
    if request.method == "POST":
        folder = request.POST.get('hidden_folder_name')
        file = request.FILES.get('file')
        FileData.objects.create(user_id=request.user.id, file=file)
        save_file(file,{"user":request.user.id, "folder":folder})
        return HttpResponse('Done')
    return JsonResponse({"message":"Error"}, safe=False)

def remove_folder(request, pk):
    folder = Folder.objects.get(pk=pk)
    folder.delete()

    return HttpResponse("success", content_type="text/plain")


def create_subfolder(request):
    REQ = request.POST
    user = request.user.id
    parent_folder = REQ["parent_folder"]
    folder = REQ["folder"]
    data = {
        "user":user,
        "parent_folder":parent_folder,
        "folder":folder
    }
    save_subfolder(
        data = data
    )
    return JsonResponse({"res":"success"}, safe=True)

def remove_file(request, pk):
    file = FileTable.objects.get(pk=pk)
    file.delete()

    return HttpResponse("success", content_type="text/plain")


def remove_all(request):
    if request.method == "POST":
        file_ids = request.POST.getlist("files_ids[]")
        print(f"IDs:{file_ids}")
        for i in file_ids:
            file = FileTable.objects.get(pk=int(i))
            file.delete()
        return JsonResponse({"mssg": "Done!"}, safe=False)


def folderItems(request, name):
    try:
        folder_items = FileTable.objects.filter(user_id=request.user.id, associate_folder=name)
        file_count = folder_items.count()
        context = {"folder_items": folder_items, "file_count": file_count, "name":name}

        return render(request, "index/files.html", context)
    except Exception as e:
        return e


def generate_share_url(request):
    """
        The function generates a share URL for a file, either by retrieving an existing access link or
        creating a new one.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by the
        client. It contains information such as the request method (GET, POST, etc.), headers, and any data
        sent with the request. In this case, the `request` object is used to retrieve the value of the
        :return: The function `generate_share_url` returns a JSON response containing the access URL. The
        access URL is either the existing access link if it already exists for the file, or a newly
        generated access link if it doesn't exist.
    """
    if request.method == "GET":
        id = request.GET["Id"]
        FILE = FileTable.objects.get(id=int(id))

        # Check if the file already has an access link
        share_exists = Share.objects.filter(file_id=id, access_link__isnull=False).exists()
        if share_exists:
            # Retrieve the existing access link
            existing_share = Share.objects.get(file_id=id, access_link__isnull=False)
            uidb64 = urlsafe_base64_encode(force_bytes(FILE.id))
            access_url = f"http://localhost:8000/surl/{existing_share.access_link}/{uidb64}"
            return JsonResponse({"res": access_url}, safe=False)
        elif not share_exists:
            # Create a new access link if it doesn't exist
            access_link = str(uuid.uuid4())
            Share.objects.create(
                sharer_id=request.user.id,
                file_id=int(id),
                folder_id=FILE.get_folder,
                access_link=access_link,
            )
            uidb64 = urlsafe_base64_encode(force_bytes(FILE.id))
            access_url = f"http://localhost:8000/surl/{access_link}/{uidb64}"
            return JsonResponse({"res": access_url}, safe=False)

@login_required
def validate_share_url(request, access_link, uidb64):
    """
    The function `validate_share_url` checks if a user has access to a shared file and redirects them to
    the file if they do, otherwise it sends an email and a notification to the file owner and returns an error
    message.
    
    :param request: The request object represents the HTTP request made by the user
    :param access_link: The access_link parameter is a unique identifier for a specific share. It is
    used to retrieve the Share object from the database
    :param uidb64: The `uidb64` parameter is a URL-safe base64 encoded string that represents the user's
    ID. It is used to encode and decode the user's ID when generating and validating share URLs
    :return: The code is returning either a redirect to a specific URL or an HttpResponse with the
    message 'You do not have access to this file'. If an exception occurs, it will return the reverse of
    the 'index' URL.
    """
    try:
        query_share_model = Share.objects.get(access_link=access_link)
        decode_file_id = force_str(urlsafe_base64_decode(uidb64))
        if request.user in query_share_model.sharee.all():
            new_uidb64 = urlsafe_base64_encode(force_bytes(request.user.id))
            query_filedata = FileTable.objects.get(id=int(decode_file_id))
            return redirect(f'/{query_share_model.sharer}/{query_filedata.associate_folder}/{query_filedata.original_filename}/{new_uidb64}')
        else:
            new_uidb64 = urlsafe_base64_encode(force_bytes(request.user.id))
            data = {
                "link": f"http://localhost:8000/authorize/{access_link}/{new_uidb64}/"
            }
            message = f"""{request.user} is trying to gain access to your file"""
            Notification.objects.create(to_user_id=int(query_share_model.sharer_id), message=message)
            sendEmail(request, data["link"])
            return HttpResponse('You do not have access to this file')
    except Exception as e:
        return reverse(index)

def grant_access_via_email(request, access_link, ID):
    """
    The function grants access to a user via email by adding their ID to the sharee list of a Share
    object.
    
    :param request: The `request` parameter is an HTTP request object that contains information about
    the current request being made by the user
    :param access_link: The access link is a unique identifier that is used to grant access to a
    specific resource or functionality. It could be a URL or a token that is generated when a user
    requests access
    :param ID: The ID parameter is a URL-safe base64 encoded string that represents the user ID
    :return: a redirect to the root URL ("/").
    """
    decode_user_id = force_str(urlsafe_base64_decode(ID))
    query_share_model = Share.objects.get(access_link=access_link)
    query_share_model.sharee.add(int(decode_user_id))
    print(query_share_model.sharee)
    return redirect('/')

def third_party_access(request, author, folder, file, external_id):
    """
    The function `third_party_access` checks if the user making the request has access to a file based
    on their user ID and an external ID, and returns the file data if they have access, otherwise it
    returns an error message.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the user making the request, the requested URL, and any data
    sent with the request
    :param author: The `author` parameter is the author of the file
    :param file: The "file" parameter is the file object that the user is trying to access. It is used
    to filter the FileData objects in the database
    :param external_id: The `external_id` parameter is a URL-safe base64 encoded string that represents
    the user's ID. It is used to compare with the ID of the currently logged-in user (`request.user.id`)
    to determine if the user has access to the file
    :return: either a rendered HTML template with the file items and author information, or an HTTP
    response with a message indicating that the user does not have access to the file.
    """
    decode_external_id = force_str(urlsafe_base64_decode(external_id))
    if int(request.user.id) == int(decode_external_id):
        user = User.objects.get(username=author).id
        query_filedata = FileTable.objects.get(user_id=user, associate_folder=folder, original_filename=file)
        context = {"items":query_filedata, 'author':author}
        return render(request, 'index/third_party.html', context)
    else:
        mssg = f"<h1>Haha..., Joke's on you!</h1>\n<p>Now you would never have access to this file bozoo</p>"
        return HttpResponse(mssg)

# Search files functionality
def searchFunc(request):
    extracts = []
    if request.method == "GET":
        if request.GET['search_type'] == 'files':
            data = request.GET["dts"]
            folder = request.GET["folder"]
            folder_path = request.path
            query_file = FileTable.search_files(
                filename=data, 
                user_id=request.user.id, 
                associate_folder=folder
            )
            for i in query_file:
                formatted_date = datetime_converter(i.created)
                extracts.append({
                    "pk":i.pk,
                    "filename":i.original_filename,
                    "folder":i.associate_folder,
                    "path":folder_path,
                    "created":formatted_date,
                })
        elif request.GET['search_type'] == 'folders':
            user = request.user.id
            get_folder = request.GET['dts']
            query_folder = Folder.search_folder(
                user_id=user,
                folder=get_folder
            )
            for folder in query_folder:
                # The above code is converting the creation date of a folder into a formatted date.
                formatted_date = datetime_converter(folder.created)
                extracts.append({
                    "Id":folder.id,
                    "folder":folder.folder,
                    "created":formatted_date
                })
        return JsonResponse({"res":extracts}, safe=False)

# 
def terminal_shell(request):
    return render(request, "terminal/shell.html",context={})


# We define a function in python Django that handles the database query and response to be sent to the frontend
def list_directory(request):
    extract = []
    if request.method=="GET": #This checks if the request made from the client side/frontend is a GET request
        curr_directory = request.GET['curr_dir'] #This is the data we get from the client side/frontend named curr_dir in the jQuery request
        query_folder = Folder.objects.get(user_id=request.user.id, folder=curr_directory) #This queries the database to filter out a folder with the users ID & curr_directory name from the frontend
        for i in query_folder.get_sub_folders:
            folder = {
                "folder":f"<D> ----- {datetime_converter(i.created)} ----- {i.folder}"
            }
            extract.append(folder)
        for j in query_folder.get_associated_files:
            file = {
                "file":f"<F> ----- {datetime_converter(j.created)} ----- {j.original_filename}"
            }
            extract.append(file)
    return JsonResponse({"response":extract}, safe=False)
    # Now let's configure the url path for this view and our requests


def download(request, file_name, folder):
    file = FileTable.objects.get(original_filename=file_name, associate_folder=folder)
    identifier = file.identifier

    # Retrieve the file content from the filesystem using the identifier
    with open(os.path.join(settings.MEDIA_ROOT, identifier), 'rb') as f:
        file_content = f.read()

    # Return the file as a response with the original filename
    response = HttpResponse(file_content, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name
    return response
