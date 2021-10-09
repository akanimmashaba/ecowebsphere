from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# Create your models here.



class CustomUser(AbstractUser):
    # date of birth
    # gender
    def __str__(self):
        return self.email

    class  Meta:  #new
        verbose_name_plural  =  "Users" 
        ordering = ("email", "username")


class Profile(models.Model):
    class UserTypes(models.TextChoices):
        STUDENT = 'STUDENT', ('STUDENT')
        LANDLORD = 'LANDLORD',('LANDLORD')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user_type =  models.CharField(max_length=8,choices=UserTypes.choices,default=UserTypes.STUDENT)    
    dob = models.DateField(blank=True, null=True)


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()