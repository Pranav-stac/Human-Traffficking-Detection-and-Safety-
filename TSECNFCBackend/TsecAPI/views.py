import datetime
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import threading
import cv2
import requests
# import tensorflow as tf
# import numpy as np
# import os

from TsecAPI.models import IncidentReport
from TsecAPI.models import SOS


# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    try:
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        # Additional fields from CustomUser, defaulting to None if not provided
        bio = data.get('bio', None)  # Changed default to None
        phone_number = data.get('phone_number', None)  # Changed default to None
        birth_date = data.get('birth_date', None)  # Already defaults to None
        user = get_user_model().objects.create_user(
            username=email,  # Assuming username is the email
            email=email,
            password=password,
            bio=bio,
            phone_number=phone_number,
            birth_date=birth_date
        )
        user.save()
        return JsonResponse({'message': 'User created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    user = authenticate(request, username=email, password=password)  # Ensure username field is used for authentication
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'}, status=200)
    
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def admin_login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    user = authenticate(request, username=email, password=password)  # Ensure username field is used for authentication
    if user is not None:
        login(request, user)
        return redirect('index')
    
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')  # Assuming email is used to identify the user
        name = data.get('name', None)
        mobile_no = data.get('mobile_no', None)
        dob = data.get('dob', None)
        address = data.get('address', None)

        user = get_user_model().objects.get(email=email)  # Fetch the user by email
        if user:
            user.name = name if name else user.name
            user.phone_number = mobile_no if mobile_no else user.phone_number
            user.birth_date = dob if dob else user.birth_date
            user.address = address if address else user.address
            user.save()
            return JsonResponse({'message': 'Profile updated successfully'}, status=200)
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def report_incident(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            location = data['location']
            phone_number = data['phone_number']
            description = data['description']
            email = data['email']
            # file = request.FILES.get('file')  # Assuming file is sent as multipart/form-data

            incident = IncidentReport(
                location=location,
                phone_number=phone_number,
                description=description,
                email=email,
                # file_path=file
            )
            incident.save()

            return JsonResponse({'message': 'Report saved successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def handle_sos(request):
    try:
        data = json.loads(request.body)
        latitude = data['latitude']
        longitude = data['longitude']
        email = data['email']

        sos = SOS(latitude=latitude, longitude=longitude, email=email)
        sos.save()

        return JsonResponse({'message': 'SOS received and saved'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import SuspiciousActivity
import base64
from django.core.files.base import ContentFile
@csrf_exempt
@require_http_methods(["POST"])
def receive_suspicious_activity(request):
    data = json.loads(request.body)
    encoded_images = data.get('images', [])
    
    # Decode images using a separate function
    decoded_images = decode_images(encoded_images)

    # Create a SuspiciousActivity instance
    activity = SuspiciousActivity.objects.create(
        images_json=encoded_images  # Optionally store the original JSON
    )

    # Save the decoded images to the database
    for image_file in decoded_images:
        image_instance = Image(image=image_file)  # Assuming 'Image' is your model and 'image' is an ImageField
        image_instance.activity = activity  # Correctly associate the image with the activity
        image_instance.save()
        activity.images.add(image_instance)  # This line might be redundant if you have a direct ForeignKey from Image to SuspiciousActivity

    # You can modify the response based on your application's needs
    return JsonResponse({'message': 'Images processed and saved successfully'}, status=200)

import matplotlib.pyplot as plt
import base64
from io import BytesIO
def decode_images(encoded_images):
    decoded_images = []
    for image_data in encoded_images:
        try:
            # Check if the image data starts with the expected prefix
            if not image_data.startswith('data:image'):
                print("Skipping improperly formatted image data")
                continue

            format, imgstr = image_data.split(';base64,')  # Splitting the data
            ext = format.split('/')[-1]  # Extracts the extension (png, jpg, etc.)
            image = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')  # Decodes the image
            decoded_images.append(image)
            # Open the decoded image using matplotlib
 
        except ValueError:
            # Handle cases where image_data is not properly formatted
            print("Skipping improperly formatted image data")
    return decoded_images

# def image_display_view(request):
#     images = Image.objects.all()  # Fetch all images from the database
#     return render(request, 'image_display.html', {'images': images})
import os

def image_display_view(request):
    directory = 'media/images'  # Path to the images directory
    # List all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # Sort files by last modified time, descending
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    # Get only the latest 5 images
    latest_images = files[:5]
    
    # Generate URLs for the images
    image_urls = [os.path.join('/media/images', os.path.basename(file)) for file in latest_images]
    print(image_urls)
    return render(request, 'image_display.html', {'images': image_urls})
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
@csrf_exempt
def admin_grievances(request):
    return render(request, 'admin-grievances.html')

def awareness_page(request):
    return render(request, 'awarenessPage.html')

def chatbot(request):
    return render(request, 'chatbot.html')

def community(request):
    return render(request, 'community.html')

from django.core import serializers
from .models import SOS
from django.shortcuts import render
from django.http import HttpResponse

def geolocation_tracker(request):
    sos_data = SOS.objects.all()  # Fetch all SOS records
    sos_data_json = serializers.serialize('json', sos_data)  # Serialize the data to JSON
    return render(request, 'geolocation-tracker.html', {'sos_data': sos_data_json})

def loginpage(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def grievances(request):
    return render(request, 'grievances.html')

def victim(request):
    return render(request, 'victim.html')

from django.http import JsonResponse
from .models import IncidentReport  # Assuming you have a model named IncidentReport

def incident_reports(request):
    if request.method == 'GET':
        # Fetch your incident reports from the database
        reports = IncidentReport.objects.all().values('id', 'location', 'description', 'phone_number', 'email')
        reports_list = list(reports)  # Convert QuerySet to list
        return JsonResponse(reports_list, safe=False)  # Return as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

from django.shortcuts import get_object_or_404
from .models import SuspiciousActivity, Image
# @csrf_exempt
# def receive_suspicious_activity(request):
#     # Assuming you receive image data somehow, e.g., from a form or API
#     image_data = request.FILES.get('image_data')
#     if image_data:
#         activity = SuspiciousActivity()  # Assuming you create a new activity
#         activity.save()  # Save the activity to generate an ID

#         image = Image(image=image_data)
#         image.save()

#         activity.images.add(image)  # Now you can add the image
#         activity.save()  # Save the activity again if necessary

#     return HttpResponse('Image received and added to activity')
def cctv_display(request):
    return render(request, 'image_display.html')





@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            # Load the request body
            data = json.loads(request.body)
            user_message = data.get('message', '')
            chat_session = data.get('chatSession', None)  # Get the current chat session

            # Define the API key and URL
            api_key = 'AIzaSyB3ViKQEbbD-ajd8aTDoQoTZtDqNIxcq60'  # Replace with your actual API key
            api_url = 'https://generativeai.googleapis.com/v1beta2/models/gemini-pro:generateMessage'

            # Define context for the chatbot
            context = "You are a supportive assistant providing information related to help services, emotional support, human trafficking information provider with respect to India, and personal safety."

            # Define headers and payload for the API request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }

            payload = {
                'prompt': {
                    'text': context + "\nUser: " + user_message  # Combine context with the user message
                },
                'chatSession': chat_session  # Use the session if provided
            }

            # Make the API request
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()

            # Process the API response
            response_data = response.json()
            bot_response = response_data.get('text', 'I am unable to provide a response. Please contact local support services.')
            chat_session = response_data.get('chatSession')  # Update the session if provided

            # Return a JSON response
            return JsonResponse({'text': bot_response, 'chatSession': chat_session})

        except requests.RequestException as e:
            # Handle any request-related errors
            return JsonResponse({'error': str(e)}, status=500)

        except json.JSONDecodeError as e:
            # Handle JSON parsing errors
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    # Return an error if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)