from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from accounts.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

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
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({
            "token":token.key,
            "user":serializer.data
            }, status=200)
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
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({
            "detail": "Not found"
        }, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({
        "token":token.key,
        "user":serializer.data
    }, status=200)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Valid for {}".format(request.user))