from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    # meta defines the model and fields we want to include
    class Meta:
        model = Product
        # use dunder __all__ to select all fields from the model
        fields = '__all__'
    # override __init__ method to make a changes on some fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # get all categories friendly names in to a tupple
        categories = Category.objects.all()
        # below is a short way to add items to a list
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # using the friendly name instead of the ids for choices
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
