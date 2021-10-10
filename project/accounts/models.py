from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse

# Create your models here.



class CustomUser(AbstractUser):
    # date of birth
    # gender
    # 

    def __str__(self):
        return self.email

    class  Meta:  #new
        verbose_name_plural  =  "Users" 
        ordering = ("email", "username")


class Profile(models.Model):
    class UserTypes(models.TextChoices):
        STUDENT = 'STUDENT', ('STUDENT')
        LANDLORD = 'LANDLORD',('LANDLORD')

    class Gender(models.TextChoices):
        MALE = 'MALE', ('MALE')
        fEMALE = 'fEMALE',('fEMALE')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user_type =  models.CharField(max_length=8,choices=UserTypes.choices,default=UserTypes.STUDENT)    
    dob = models.DateField('Date of Birth', blank=True, null=True)
    gender = models.CharField('Gender', max_length=8,choices=Gender.choices,default=Gender.MALE)
    email = models.EmailField('Email Address: ', default="admin@localhost.com")
    phone_number = models.CharField("Contact Number: ", max_length=10,default="0000000000")
    student_number = models.CharField("Student Number: ", max_length=8, default="00000000")

    # student number
    # email
    # contact number


    def __str__(self):
        return self.user.username
    
    class  Meta:
        verbose_name = 'Profile'
        verbose_name_plural  =  "Profiles" 
        ordering = ("last_name", "first_name")

    def is_student(self):
        return (self.user_type == 'STUDENT')
    
    def is_landlord(self):
        return (self.user_type == 'LANDLORD')

    def get_absolute_url(self):
        return reverse('dashbard', args=[str(self.id)])



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()