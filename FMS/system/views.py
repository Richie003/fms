from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
import re
from django.db.models import Q
from rest_framework.response import Response
from django.http import HttpResponse
from accounts.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from documents.utils import datetime_converter


@api_view(["POST"])
def sign_up(request):
    """
    The `sign_up` function is used to create a new user account, save the user details, set the
    password, generate a token, and return the token and user data in the response.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, body, and
    other metadata. In this case, it is used to retrieve the data sent by the client during the sign-up
    :return: If the serializer is valid, the function will return a response with a token and user data
    in JSON format, with a status code of 200. If the serializer is not valid, an empty response will be
    returned.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=200)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# --- Check if username exists --- #
@api_view(["GET"])
def validate_username(request):
    username = request.query_params.get("username", None)
    query_user_model = User.objects.filter(username=username)
    if username != "":
        if query_user_model.exists():
            return Response("Not_available")
        else:
            return Response("Available")
    else:
        return Response("")



@api_view(["POST"])
def login(request):
    """
    The `login` function checks if the provided username and password match a user in the database, and
    if so, returns a token and user data.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, and data
    :return: The code is returning a response with a JSON object containing a token and user data. The
    token is obtained or created using the user object, and the user data is serialized using the
    UserSerializer. The response has a status code of 200.
    """
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data}, status=200)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    """
    The function "test_token" returns a response with the message "Valid for [username]" for
    authenticated users.
    
    :param request: The request object represents the HTTP request that was made to the server. It
    contains information such as the request method (GET, POST, etc.), headers, and query parameters
    :return: The response being returned is a string that includes the message "Valid for" followed by
    the username of the authenticated user.
    """
    return Response("Valid for {}".format(request.user))


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createFolder(request):
    """
    The function creates a folder object with the given name and associates it with the current user.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the user making the request, the data sent in the request,
    and other metadata related to the request. In this case, it is used to get the user making the
    request and the
    :return: a Response object with the string "success".
    """
    folder, created = Folder.objects.get_or_create(
        user=request.user, folder=request.data["folder_name"]
    )
    return Response("success")


@api_view(["POST"])
def uploadFile(request):
    """
    The `uploadFile` function processes a file upload request, associates the file with a user, and
    saves the file with additional metadata.
    
    :param request: The `uploadFile` function seems to handle file uploads based on the provided
    `request` object. The `request` object likely contains data such as the user's token, file to be
    uploaded, and associated folder information
    :return: The function `uploadFile` is returning a response with the message "Success" if the file
    upload process is successful. If an exception occurs during the process, it returns a response with
    the error message generated by the exception, along with a status code of 500.
    """
    print(request.data)
    try:
        user_token = Token.objects.get(key=request.data["token"])
        print(user_token.user)
        file_obj, created = FileData.objects.get_or_create(user=user_token.user, file=request.data["file"])
        extras = {"user": user_token.user_id, "folder": request.data["associate_folder"]}
        save_file(request.data["file"], extras)
        return Response("Success")
    except Exception as e:
        print(e)
        return Response("{}".format(str(e)), status=500)

def get_file_type(filename):
    """
    The function `get_file_type` extracts the file extension from a given filename.
    
    :param filename: It looks like you have provided a function `get_file_type` that extracts the file
    extension from a given filename using a regular expression. However, the `re` module is not imported
    in the code snippet you provided. To make the function work, you need to import the `re` module at
    :return: The function `get_file_type` returns the file extension of the given filename.
    """
    match = re.search(r'\.([^\.]+)$', filename)
    if match:
        extension = match.group(1)
        return extension
    else:
        pass

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUniqueFiles(request):
    """
    The function `getUniqueFiles` retrieves unique file data for a specific user and returns a list of
    formatted file information.
    
    :param request: The `getUniqueFiles` function takes a `request` object as a parameter. The `request`
    object likely contains information about the user making the request, such as their user ID. The
    function then retrieves file data from a `FileTable` based on the user ID and constructs a list of
    :return: A list of dictionaries containing information about unique files uploaded by the user, such
    as the uploaded_by username, file ID, shortened and full file names, file type, creation and update
    timestamps. This data is returned as a Response object with a status code of 200.
    """
    user = request.user
    query = Q()
    query &= Q(user_id=user.id, associate_folder="{}_records".format(request.user))
    file_data = FileTable.objects.filter(query)
    data_list = [{
            'uploaded_by':data.user.username,
            'Id':data.id,
            'file_short':"{}...".format(data.original_filename[:20]),
            'file_long':data.original_filename,
            'file_type':get_file_type(data.original_filename),
            'created':datetime_converter(data.created),
            'updated':datetime_converter(data.updated)
        } for data in file_data]
    return Response(data_list, status=200)


@api_view(["GET"])
def downloadable(request):
    """
    The function `downloadable` retrieves a file from the server and allows it to be downloaded if the
    user has a valid token.
    
    :param request: The `request` parameter in the `downloadable` function is typically an object that
    contains information about the current HTTP request, such as the request method, headers, query
    parameters, and more. It is commonly used in web development frameworks like Django or Flask to
    handle incoming HTTP requests and generate appropriate responses
    :return: The `downloadable` function is returning an HTTP response with the file content for
    download if the token provided in the request query parameters is valid. If the token is not found
    in the database, it returns a response saying "User with this token Doesn't exist". If any other
    exception occurs during the process, it returns a response with the error message.
    """
    try:
        if Token.objects.get(key=request.query_params.get("token", None)):
            file_id = request.query_params.get("file_Id", None)
            file = FileTable.objects.get(id=int(file_id))
            file_path = os.path.join(settings.MEDIA_ROOT, file.identifier)

            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read())
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file.original_filename)
                return response
        else:
            return Response("User with this token Doesn't exist")
    except Exception as e:
        return Response(str(e))