from django.db import models
from django.conf import settings
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.template.defaultfilters import slugify 


class Address(models.Model):
    class ProvinceChoice(models.TextChoices):
        GAUTENG = 'GP', ('Gauteng')

    house_number = models.CharField(max_length=20,default="5714")        
    street_name = models.CharField(max_length=255,default="Tshega street")
    provice = models.CharField(max_length=2,choices=ProvinceChoice.choices,default=ProvinceChoice.GAUTENG)
    locality = models.CharField(max_length=255, null=True,blank=True, default="soshanguve")
    municipality = models.CharField(max_length=255,default="Tshwane")
    postal_code = models.CharField(max_length=10,default="0152")
    country = models.CharField(default="South Africa", editable=False)

    def __str__(self):
        return f"{self.house_number} {self.street_name} {self.locality} {self.postal_code} {self.country}"

class Accomodation(models.Model, HitCountMixin):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, related_name='accomodation_likes')
    image_1 = models.ImageField(upload_to='images', null=True, blank=True)
    image_2 = models.ImageField(upload_to='images', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images', null=True, blank=True)
    image_4 = models.ImageField(upload_to='images', null=True, blank=True)
    image_5 = models.ImageField(upload_to='images', null=True, blank=True)
    
    def current_hit_count(self):
        return self.hit_count.hits

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

     # def get_absolute_url(self):
    #     return reverse('accomodation_detail', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('accomodation-detail', args=[str(self.id)])


class Application(models.Model):
    class ApplicationStatusChoice(models.TextChoices):
        APPROVED = 'APPROVED', ('APPROVED')
        REJECTED = 'REJECTED', ('REJECTED')
        RECEIVED = 'RECEIVED', ('RECEIVED')

    accomodation = models.ForeignKey(Accomodation, verbose_name=("Accomodation"), on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=("Applicant"), on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9,choices=ApplicationStatusChoice.choices,default=ApplicationStatusChoice.RECEIVED)
    # status_reasoning = models.TextField(blank=True, null=True, default="accomodation application recieved, by the landlord, and it is under conciderration by the landlord of the accomodation")