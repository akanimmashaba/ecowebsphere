from django.db import models
from django.conf import settings
from django.db.models.fields import related
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django_quill.fields import QuillField

class Address(models.Model):
    class ProvinceChoice(models.TextChoices):
        GAUTENG = 'GP', ('Gauteng')

    house_number = models.CharField(max_length=20,default="5714")        
    street_name = models.CharField(max_length=255,default="Tshega street")
    provice = models.CharField(max_length=2,choices=ProvinceChoice.choices,default=ProvinceChoice.GAUTENG)
    locality = models.CharField(max_length=255, null=True,blank=True, default="soshanguve")
    municipality = models.CharField(max_length=255,default="Tshwane")
    postal_code = models.CharField(max_length=10,default="0152")
    country = models.CharField(default="South Africa", max_length=12, editable=False)

    def __str__(self):
        return f"{self.house_number} {self.street_name} {self.locality} {self.postal_code} {self.country}"



class Accomodation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=255, unique=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='accomodation_likes')
    image_1 = models.ImageField(upload_to='images')
    image_2 = models.ImageField(upload_to='images', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images', null=True, blank=True)
    image_4 = models.ImageField(upload_to='images', null=True, blank=True)
    image_5 = models.ImageField(upload_to='images', null=True, blank=True)
    description = QuillField(null=True, blank=True)
    applied = models.ManyToManyField(settings.AUTH_USER_MODEL,default=None, blank=True, related_name="applied")
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total_application(self):
        return self.applied.all().count()

   
    def is_description(self):
            if self.description == None:
                return str("accomodation has no description").upper()
            return str(self.description)
    def __str__(self):
        return str(self.title)

     # def get_absolute_url(self):
    #     return reverse('accomodation_detail', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('accomodation-detail', args=[str(self.id)])

class Application(models.Model):
    class ApplicationStatusChoice(models.TextChoices):
        APPROVED = 'APPROVED', ('APPROVED')
        REJECTED = 'REJECTED', ('REJECTED')
        RECEIVED = 'RECEIVED', ('RECEIVED')
        CANCELLED = 'CANCELLED', ('CANCELLED')

    accomodation = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=("accomodation"), on_delete=models.CASCADE, related_name="application")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=("Applicant"), on_delete=models.CASCADE, related_name="applicant")
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=ApplicationStatusChoice.choices,default=ApplicationStatusChoice.RECEIVED)
    # status_reasoning = models.TextField(blank=True, null=True, default="accomodation application recieved, by the landlord, and it is under conciderration by the landlord of the accomodation")

    def __str__(self):
        return str(f'Application ID #{self.id} submitted by {self.applicant}')
    
    def application_id(self):
        return str(self.id)
    

    def get_absolute_url(self):
        return reverse('applicantion-list', args=[str(self.id)])

