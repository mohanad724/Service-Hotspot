from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from service_hotspot.users.models import User
from .serializers import LogoutSerializer, UserRegistrationSerializer,UserUpdateSerializer,LoginSerializer,UserSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsNotAuthenticated

class UserRegistrationView(APIView):
    """
    View for user registration, allowing only unauthenticated users to access.
    """
    
    permission_classes = [IsNotAuthenticated]  # Allow access to unauthenticated users

    def post(self, request, *args, **kwargs):
        """
        Creates a new user if data is valid.

        Parameters:
            request (Request): Contains user registration data.

        Returns:
            Response: Success message with user details, or error messages if validation fails.
        """
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "mobile_number": user.mobile_number
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserUpdateView(APIView):
    """
    View for updating authenticated user's data, including User and UserProfile data.
    """
    
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        Updates the authenticated user's data, both in User and UserProfile.

        Parameters:
            request (Request): Contains user data to be updated 
            ex of json to update: {
            "username":"mohanad",
            "mobile_number": "12345678904",
            "email": "test4@example.com",
            "profile":{
                "fullname":"mohanadshokal"
            }

        Returns:
            Response: Success message with updated user details, or error messages if validation fails.
        """
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User updated successfully",
                    "user": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    """
    View for handling user login and token generation.
    """

    def post(self, request):
        """
        Authenticates the user and returns JWT tokens if credentials are valid.

        Parameters:
            request (Request): Contains login credentials (e.g., username and password).

        Returns:
            Response: JWT tokens (refresh and access) if login is successful, or error messages if validation fails.
        """
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserDetailView(RetrieveAPIView):
    """
    Retrieves details of a specific authenticated user based on user ID.
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class LogoutView(APIView):
    """
    Handles user logout by blacklisting the user's token.
    """

    def post(self, request):
        """
        Blacklists the user's token, effectively logging the user out.

        Parameters:
            request (Request): Contains token data for logout.

        Returns:
            Response: Success message if logout is successful, or error messages if validation fails.
        """
        
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User logged out successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    Redirects authenticated users to their profile detail page.
    """
    
    permanent = False

    def get_redirect_url(self) -> str:
        """
        Generates the URL for the user's profile page based on username.

        Returns:
            str: URL for the user's profile detail page.
        """
        
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()



