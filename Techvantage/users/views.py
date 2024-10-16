from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from utilities.firebase import create_firebase_user, login_firebase_user, logout_firebase_user
from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from utilities.authentication import FirebaseAuthentication
from utilities.utils import ResponseInfo

class RegisterAPIView(CreateAPIView):
    """
    API view for registering a new user.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = RegisterSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RegisterAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST method to register a new user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        display_name = serializer.validated_data.get('display_name', None)  # Optional field

        try:
            # Create the user in Firebase
            firebase_user = create_firebase_user(email, password, display_name)

            # Save the user to the CustomUser model
            CustomUser.objects.create(uid=firebase_user.uid, email=email, display_name=display_name)

            self.response_format["data"] = {"uid": firebase_user.uid, "email": email, "display_name": display_name}
            self.response_format["message"] = ["User registered successfully"]
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format["error"] = str(e)
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(CreateAPIView):
    """
    API view for logging in a user using Firebase.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = LoginSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST method to log in a user with Firebase.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = login_firebase_user(email, password)
            self.response_format["data"] = user
            self.response_format["message"] = ["Login successful"]
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format["error"] = str(e)
            self.response_format["message"] = ["Login failed"]
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(CreateAPIView):
    """
    API view for logging out a user.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (FirebaseAuthentication,)

    def post(self, request, *args, **kwargs):
        """
        POST method to log out a user.
        """
        uid = request.user.uid
        logout_firebase_user(uid)

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
