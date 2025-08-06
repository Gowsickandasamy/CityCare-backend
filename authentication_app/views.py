from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from authentication_app.serializers import ChangePasswordSerializer, LoginSerializer, UserProfileSerializers, UserSerializers
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, World!"})


class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']
            
            user = authenticate(email=email, password=password)
            
            if user is not None:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "Login successful",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "User account is disabled"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error":"Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"message":"Successfully Logged Out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        rawUser = request.user
        userSerializer = UserSerializers(rawUser)
        return Response(userSerializer.data)
    
    def put(self,request):
        user = request.user
        serializer = UserProfileSerializers(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Profile update successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializers(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile partially updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

