from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
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
        return Response({"token": token.key, "user": serializer.data}, status=200)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


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

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUniqueFiles(request):
    user = request.user
    print(request.user)
    file_data = FileTable.objects.filter(user_id=user.id)
    data_list = [{
            'uploaded_by':data.user.username,
            'Id':data.id,
            'file_short':"{}...".format(data.original_filename[:20]),
            'file_long':data.original_filename,
            'created':datetime_converter(data.created),
            'updated':datetime_converter(data.updated)
        } for data in file_data]
    return Response(data_list, status=200)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadable(request):
    file_id = request.data["file_Id"]
    file = FileTable.objects.get(id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file.identifier)

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response