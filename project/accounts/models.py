from django.db import models
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser)
from django.db.models.fields import related

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    class USER_TYPES(models.TextChoices):
        STUDENT = "STUDENT", "STUDENT"
        LANDLORD = "LANDLORD", "LANDLORD"

    class GENDER_TYPES(models.TextChoices):
        MALE = 'MALE', ('MALE')
        FEMALE = 'FEMALE',('FEMALE')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    user_type  = models.CharField(max_length=8,choices=USER_TYPES.choices,default=USER_TYPES.STUDENT)    
    gender  = models.CharField(max_length=6,choices=GENDER_TYPES.choices,default=GENDER_TYPES.MALE)    
    ID_number = models.CharField("ID number",max_length=13,blank=True, null=True)
    # stdent_number = models.CharField("student number",max_length=8)
    phone_number = models.CharField("Contact Number: ", max_length=10,blank=True, null=True)
    date_of_birth = models.DateField('Date of Birth: ', blank=True, null=True)

    def is_student(self):
        return (self.user_type == 'STUDENT')
            
    def is_landlord(self):
        return (self.user_type == 'LANDLORD')

    def my_username(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('dashbard', args=[str(self.id)])

    class  Meta:
        verbose_name = 'Profile'
        verbose_name_plural  =  "Profiles" 
        ordering = ("last_name", "first_name")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()