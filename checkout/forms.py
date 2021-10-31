from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        # tell django each model this is associated with
        model = Order
        # tell django each fields wanna rendered
        fields = {'full_name', 'email', 'phone_number',
                    'street_address1', 'street_address2',
                    'town_or_city', 'postcode', 'country',
                    'county',}

    # overwrite the init method
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)  # this is meant to set up the forms
        # ...as by default
        # below will improve the looks of display. It wonb be ugly labels and empty text boxes
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # cursor will start in the full name field once page is loaded
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # navigate through the fields and add a '*' if field is required by the model
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder  # setting the place holder of the field to the value
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'  # adding a css class that we will use lated
            self.fields[field].label = False
