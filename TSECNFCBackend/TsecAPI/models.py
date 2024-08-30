import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add additional fields if needed
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True)  # New field for name
    address = models.TextField(null=True)  # New field for address

    # You can also add methods
    def __str__(self):
        return self.username
    
class IncidentReport(models.Model):
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    email = models.EmailField(default='pranav@example.com')  # Manually defined default value
    # file_path = models.FileField(upload_to='uploads/')  # Adjust the path as needed

    def __str__(self):
        return f"Incident at {self.location}"
    

class SOS(models.Model):
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOS from {self.email} at {self.timestamp}"    

class Image(models.Model):
    # Assuming each image is related to a SuspiciousActivity, you might want to include a ForeignKey
    # If not needed, you can remove the 'related_name' and 'on_delete' attributes
    activity = models.ForeignKey('SuspiciousActivity', related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/')  # Store images in a directory called 'images' within your MEDIA_ROOT

    def __str__(self):
        if self.activity:
            return f"Image {self.id} for Activity {self.activity.id}"
        else:
            return f"Image {self.id} with no associated activity"

class SuspiciousActivity(models.Model):
    imagesd = models.ManyToManyField(Image)
    images_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Suspicious Activity ID {self.id}"

