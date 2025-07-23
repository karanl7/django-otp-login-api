from django.shortcuts import render

# Create your views here.

import random
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, OTP
from .serializers import RegisterSerializer, OTPRequestSerializer, OTPVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({'message': 'Email already registered.'}, status=400)
            User.objects.create(email=email)
            return Response({'message': 'Registration successful. Please verify your email.'})
        return Response(serializer.errors, status=400)

class RequestOTPView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=404)

            otp_code = str(random.randint(100000, 999999))
            OTP.objects.create(user=user, code=otp_code)
            print(f"Mock Email: Sending OTP {otp_code} to {email}")
            return Response({'message': 'OTP sent to your email.'})
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.filter(user=user, code=code).last()
                if not otp or (timezone.now() - otp.created_at > timedelta(minutes=5)):
                    return Response({'message': 'Invalid or expired OTP.'}, status=400)

                user.is_verified = True
                user.save()
                token = RefreshToken.for_user(user)
                return Response({'message': 'Login successful.', 'token': str(token.access_token)})
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=404)
        return Response(serializer.errors, status=400)
