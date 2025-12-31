from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users with a username, email, mobile number, and password.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'password']

    def create(self, validated_data):
        """
        Creates and returns a new user instance with a hashed password.
        """
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for authenticating users with username and password.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validates user credentials and returns the user if valid.
        """
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            return user
        raise serializers.ValidationError("Invalid credentials")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying basic user information.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for handling additional user information.
    """
    class Meta:
        model = UserProfile
        fields = ['fullname', 'address', 'city', 'state', 'country', 'zip_code', 'accepted_method']

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating both User and UserProfile data.
    """
    profile = UserProfileSerializer(required=False)  # Include profile fields as nested serializer, make it optional

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'profile']  # Include 'profile' fields for nested update

    def update(self, instance, validated_data):
        # Extract profile data and update profile separately if provided
        profile_data = validated_data.pop('profile', None)

        # Update main User instance fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.save()

        # Update profile fields only if profile data is provided and profile exists
        if profile_data:
            profile_instance = getattr(instance, 'profile', None)
            if profile_instance:
                profile_serializer = self.fields['profile']
                profile_serializer.update(profile_instance, profile_data)
            else:
                # If profile does not exist, create a new one if needed
                UserProfile.objects.create(user=instance, **profile_data)

        return instance


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logging out users by blacklisting their refresh token.
    """
    refresh_token = serializers.CharField()

    def validate(self, data):
        """
        Validates the refresh token data.
        """
        self.token = data['refresh_token']
        return data

    def save(self, **kwargs):
        """
        Blacklists the provided refresh token to log out the user.
        """
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except Exception:
            self.fail('bad_token')


