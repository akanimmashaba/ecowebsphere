from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Accomodation

class AccomodationForm(forms.ModelForm):

    class Meta:
        model = Accomodation
        fields = ['title', 'address', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'description']


        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Add Accomodation'))
