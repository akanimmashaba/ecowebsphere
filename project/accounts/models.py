from django.db import models
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser)

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

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.user_type = self.default_user_type

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
    class UserTypes(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        Landlord = "LANDLORD", "Landlord"

    class Gender(models.TextChoices):
        MALE = 'MALE', ('Male')
        FEMALE = 'FEMALE',('Female')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user_type  = models.CharField(max_length=8,choices=UserTypes.choices,default=UserTypes.STUDENT)    
    gender  = models.CharField(max_length=6,choices=Gender.choices,default=Gender.MALE)    


    def __str__(self):
        return self.user.username


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user_type=User.UserTypes.STUDENT)

class LandlordManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user_type=User.UserTypes.Landlord)

class StudentProfile(models.Model):
    stdent_number = models.CharField("student number",max_length=8)

class LandlordProfile(models.Model):
    ID_number = models.CharField("ID number",max_length=13)

class Student(Profile):
    objects = StudentManager()

    class Meta:
        proxy = True

    def student_(self):
        return "student"

# class Profile(models.Model):
        #     class UserTypes(models.TextChoices):
        #         STUDENT = 'STUDENT', ('STUDENT')
        #         LANDLORD = 'LANDLORD',('LANDLORD')

        #     class Gender(models.TextChoices):
        #         MALE = 'MALE', ('MALE')
        #         fEMALE = 'fEMALE',('fEMALE')

        #     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        #     first_name = models.CharField(max_length=100, blank=True)
        #     last_name = models.CharField(max_length=100, blank=True)
        #     user_type =  models.CharField(max_length=8,choices=UserTypes.choices,default=UserTypes.STUDENT)    
        #     dob = models.DateField('Date of Birth', blank=True, null=True)
        #     gender = models.CharField('Gender', max_length=8,choices=Gender.choices,default=Gender.MALE)
        #     email = models.EmailField('Email Address: ', default="admin@localhost.com")
        #     phone_number = models.CharField("Contact Number: ", max_length=10,default="0000000000")
        #     student_number = models.CharField("Student Number: ", max_length=8, default="00000000")

        #     # student number
        #     # email
        #     # contact number


        #     def __str__(self):
        #         return self.user.username
            
        #     class  Meta:
        #         verbose_name = 'Profile'
        #         verbose_name_plural  =  "Profiles" 
        #         ordering = ("last_name", "first_name")

        #     def is_student(self):
        #         return (self.user_type == 'STUDENT')
            
        #     def is_landlord(self):
        #         return (self.user_type == 'LANDLORD')

        #     def get_absolute_url(self):
        #         return reverse('dashbard', args=[str(self.id)])



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()