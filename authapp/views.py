from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.core.cache import cache
import random
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, VerificationCodeSerializer, ResetPasswordSerializer, ForgotPasswordSerializer, ProfileUpdateSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import UserProfile
from cart.models import Cart
from rest_framework.views import APIView

VERIFICATION_CODE_TIMEOUT = 1200  

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False  
        user.save()
        UserProfile.objects.create(user=user)
        
        code = str(random.randint(100000, 999999))
        
        send_mail(
            'Your Verification Code',
            f'Your verification code is {code}',
            'info@householdbd.com',
            [user.email],
            fail_silently=False,
        )
        cache.set(f'verification_code_{user.id}', code, timeout=VERIFICATION_CODE_TIMEOUT)

        return Response({
        "message": "User registered successfully. A verification code has been sent to your email.",
        "email": user.email
    }, status=status.HTTP_201_CREATED)

class VerifyCodeView(generics.GenericAPIView):
    serializer_class = VerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
      
        userEmail = request.data.get('email')
      
        if userEmail is None:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=userEmail)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        stored_code = cache.get(f'verification_code_{user.id}')
        if stored_code is None:
            user.delete() 
            return Response({"error": "Verification code has expired. Your account has been deleted. Please register again."}, status=status.HTTP_400_BAD_REQUEST)
        
        if stored_code == code:
            user.is_active = True
            user.save()
            cache.delete(f'verification_code_{user.id}') 
            return Response({"message": "Verification successful. Your account is now active."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
# class LoginView(generics.GenericAPIView):
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
     
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"error": "Invalid Credentials or account not activated."}, status=status.HTTP_400_BAD_REQUEST)
        
#         if user.check_password(password) and user.is_active:
#             token, created = Token.objects.get_or_create(user=user)

#             session_key = request.session.session_key

#             if session_key:
#                 anonymous_cart = Cart.objects.filter(session_key=session_key).first()
#                 if anonymous_cart:
#                     # Move the entire anonymous cart to the user's cart
#                     anonymous_cart.user = user
#                     anonymous_cart.session_key = None  # Remove session key once it's transferred
#                     anonymous_cart.save()

#             return Response({
#                 "token": token.key, 
#                 "user": { 
#                     "id": user.id,
#                     "username": user.username,
#                     "email": user.email,
                    
#                 },
#                 "message": "Login successful."
#             }, status=status.HTTP_200_OK)
        
#         return Response({"error": "Invalid Credentials or account not activated."}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid Credentials or account not activated."}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(password) and user.is_active:
            # Generate or get the token
            token, created = Token.objects.get_or_create(user=user)

            # Get the session key from the request (for anonymous users)
            session_key = request.session.session_key

            if session_key:
                # Get the anonymous cart associated with the session_key
                anonymous_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
                if anonymous_cart:
                    # Retrieve any existing cart for the user (if exists)
                    user_cart = Cart.objects.filter(user=user).first()

                    if user_cart:
                        # If the user already has a cart, merge the anonymous cart into it
                        for item in anonymous_cart.items.all():
                            # Merge cart items (if the item exists, update the quantity)
                            existing_item = user_cart.items.filter(service=item.service).first()
                            if existing_item:
                                existing_item.quantity += item.quantity
                                existing_item.save()
                            else:
                                # Add the new item to the user's cart
                                item.cart = user_cart
                                item.save()

                        # Delete the anonymous cart after merging
                        anonymous_cart.delete()
                    else:
                        # If the user doesn't have an existing cart, assign the anonymous cart to the user
                        anonymous_cart.user = user
                        anonymous_cart.session_key = None  # Remove session_key
                        anonymous_cart.save()

            return Response({
                "token": token.key, 
                "user": { 
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "message": "Login successful."
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid Credentials or account not activated."}, status=status.HTTP_400_BAD_REQUEST)
     
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.auth
        if token:
            Token.objects.filter(key=token).delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No token found."}, status=status.HTTP_400_BAD_REQUEST)

class SendVerificationCodeView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = str(random.randint(100000, 999999))

        try:
            send_mail(
                'Your Password Reset Code',
                f'Your Password Reset code is {code}',
                'info@householdbd.com',
                [email],
                fail_silently=False,
            )

            user = User.objects.get(email=email)
            cache.set(f'verification_code_{user.id}', code, timeout=VERIFICATION_CODE_TIMEOUT)
            return Response({
                "message": "A verification code has been sent to your email.",
                "email": user.email
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class SendVerificationCodeView(generics.GenericAPIView):
#     serializer_class = ForogotPasswordSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         code = str(random.randint(100000, 999999))
  
#         send_mail(
#             'Your Password Reset Code',
#             f'Your Password Reset code is {code}',
#             'from@example.com',
#             [email],
#             fail_silently=False,
#         )
#         try:
#             user = User.objects.get(email=email)  
#             cache.set(f'verification_code_{user.id}', code, timeout=VERIFICATION_CODE_TIMEOUT)  
#             return Response({
#                 "message": "A verification code has been sent to your email.",
#                 "email": user.email
#             }, status=status.HTTP_200_OK)
        
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        userEmail = request.data.get('email')

        try:
            user = User.objects.get(email=userEmail)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
     
        stored_code = cache.get(f'verification_code_{user.id}')
        if stored_code == code:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Update User fields (first_name, last_name) from the validated data
        user = self.request.user
        user.first_name = serializer.validated_data.get('first_name', user.first_name)
        user.last_name = serializer.validated_data.get('last_name', user.last_name)
        user.save()

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        user_data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
        }
        serializer = self.get_serializer(profile)
        return Response({**serializer.data, **user_data}, status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)