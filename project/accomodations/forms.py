from django import forms
from django.db.models import fields
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Accomodation, Address

class AccomodationForm(forms.ModelForm):

    class Meta:
        model = Accomodation
        fields = ['owner','title', 'address', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'description']

        widgets = {
            'owner': forms.Select(attrs={'class': 'form-control','Value': 'username', 'id': 'userID','type': ''}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Add Accomodation'))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Add Address'))

