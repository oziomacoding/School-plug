from django.shortcuts import render

# Create your views here.
# signup/views.py

# from django.contrib.auth.models import User
from .models import CustomUser  # Import your CustomUser model
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Profile  
import random
import string
import json
import re  # Import regular expression module for phone number validation
import datetime


@csrf_exempt
def primary_signup_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            full_name = data.get('full_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            agree_to_terms = data.get('agree_to_terms')

            # Check for missing fields
            required_fields = [full_name, email, phone_number, password, confirm_password, agree_to_terms]
            if not all(required_fields):
                return JsonResponse({'error': 'Missing fields'}, status=400)

            # Validate email
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'error': 'Invalid email format'}, status=400)

            # Validate phone number
            if not re.match(r'^0\d{10}$', phone_number):
                return JsonResponse({'error': 'Invalid phone number format'}, status=400)

            # Validate password
            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)
            if len(password) < 8:
                return JsonResponse({'error': 'Password must be at least 8 characters long'}, status=400)

            # Check if email or phone number already exists
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email address already in use'}, status=400)
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'error': 'Phone number already in use'}, status=400)

            # Debug: Log the phone number being processed
            print(f"Creating user with phone number: {phone_number}")

            # Create the user
            user = CustomUser.objects.create_user(username=email, email=email, password=password, phone_number=phone_number)
            user.save()

            # Save the full name in the profile
            user.profile.full_name = full_name
            user.profile.save()

            login(request, user)
            return JsonResponse({'message': 'User created successfully'}, status=201)

        except Exception as e:
            # Debug: Log the error
            print(f"Error during user creation: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def educational_details_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Debug: Log the received data
            print(f"Received data: {data}")

            # Assume the user is authenticated and we can get the user from the request
            user = request.user

            # If user is not authenticated, return an error
            if not user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=401)

            university_of_study = data.get('university_of_study')
            course = data.get('course')
            year_of_admission_str = data.get('year_of_admission')
            year_of_graduation_str = data.get('year_of_graduation')
            level = data.get('level')

            # Debug: Log the parsed data
            print(f"university_of_study: {university_of_study}, course: {course}, year_of_admission: {year_of_admission_str}, year_of_graduation: {year_of_graduation_str}, level: {level}")

            # Check for missing fields
            required_fields = [university_of_study, course, year_of_admission_str, year_of_graduation_str, level]
            if not all(required_fields):
                return JsonResponse({'error': 'Missing fields'}, status=400)


            # Convert string dates to datetime.date objects
            year_of_admission = datetime.datetime.strptime(year_of_admission_str, '%Y-%m-%d').date()
            year_of_graduation = datetime.datetime.strptime(year_of_graduation_str, '%Y-%m-%d').date()

            # Save the educational details in the profile
            user.profile.university_of_study = university_of_study
            user.profile.course = course
            user.profile.year_of_admission = year_of_admission
            user.profile.year_of_graduation = year_of_graduation
            user.profile.level = level
            user.profile.save()

            return JsonResponse({'message': 'Educational details updated successfully'}, status=200)

        except Exception as e:
            # Debug: Log the error
            print(f"Error during updating educational details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def profile_picture_view(request):
    if request.method == 'POST':
        try:
            # Assume the user is authenticated and we can get the user from the request
            user = request.user

            # If user is not authenticated, return an error
            if not user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=401)

            # Get the uploaded file
            profile_picture = request.FILES.get('profile_picture')

            # Check if the file was uploaded
            if not profile_picture:
                return JsonResponse({'error': 'No file uploaded'}, status=400)

            # Save the profile picture
            user.profile.profile_picture = profile_picture
            user.profile.save()

            return JsonResponse({'message': 'Profile picture updated successfully'}, status=200)

        except Exception as e:
            # Debug: Log the error
            print(f"Error during profile picture upload: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_or_phone = data.get('email_or_phone')
            password = data.get('password')

            if not email_or_phone or not password:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            # Check if input is a valid email
            try:
                validate_email(email_or_phone)
                is_email = True
            except ValidationError:
                is_email = False

            if not is_email:
                # Check if input matches phone number format
                if not re.match(r'^0[1-9]\d{9}$', email_or_phone):
                    return JsonResponse({'error': 'Invalid phone number or email format'}, status=400)

            # Authenticate user
            user = authenticate(request, username=email_or_phone, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)



# Function to send the 4-digit code via email
def send_reset_code(email, code):
    subject = 'Your Password Reset Code'
    message = f'Your password reset code is: {code}'
    from_email = 'no-reply@yourdomain.com'
    send_mail(subject, message, from_email, [email])

# Function to send the 4-digit code via phone (SMS)
def send_sms(phone_number, code):
    # Implement SMS sending logic here
    pass

@csrf_exempt
def request_password_reset(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        identifier = data.get('identifier')  # This can be email or phone number
        
        if not identifier:
            return JsonResponse({'error': 'Identifier is required'}, status=400)

        try:
            if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
                code = ''.join(random.choices(string.digits, k=4))
                user.profile.reset_code = code
                user.profile.save()
                send_reset_code(user.email, code)
            else:
                user = CustomUser.objects.get(profile__phone_number=identifier)
                code = ''.join(random.choices(string.digits, k=4))
                user.profile.reset_code = code
                user.profile.save()
                send_sms(user.profile.phone_number, code)
            
            return JsonResponse({'message': 'Reset code sent successfully'}, status=200)
        
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

   
@csrf_exempt
def verify_reset_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        identifier = data.get('identifier')
        reset_code = data.get('reset_code')

        if not identifier or not reset_code:
            return JsonResponse({'error': 'Identifier and code are required'}, status=400)

        try:
            if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
            else:
                user = CustomUser.objects.get(phone_number=identifier)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if user.profile.reset_code == reset_code:
            return JsonResponse({'message': 'Reset code is valid.'})
        else:
            return JsonResponse({'error': 'Invalid reset code'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        identifier = data.get('identifier')
        reset_code = data.get('reset_code')
        new_password = data.get('new_password')

        if not identifier or not reset_code or not new_password:
            return JsonResponse({'error': 'Identifier, reset code, and new password are required'}, status=400)

        try:
            if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
            else:
                user = CustomUser.objects.get(phone_number=identifier)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if user.profile.reset_code == reset_code:
            user.set_password(new_password)
            user.profile.reset_code = ''  # Clear the reset code after successful password reset
            user.profile.save()
            user.save()
            return JsonResponse({'message': 'Password reset successful.'})
        else:
            return JsonResponse({'error': 'Invalid reset code'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
