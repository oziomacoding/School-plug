from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    university_of_study = models.CharField(max_length=255, blank=True)
    course = models.CharField(max_length=255, blank=True)
    year_of_admission = models.DateField(null=True, blank=True)
    year_of_graduation = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    university_of_study = models.CharField(max_length=255, blank=True)
    course = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=255, blank=True, null=True) 
    year_of_admission = models.DateField(null=True, blank=True)
    year_of_graduation = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    reset_code = models.CharField(max_length=4, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
