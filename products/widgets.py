from django.forms.widgets import ClearableFileInput
# below is used to keep the custom widgets as close to the original as possible
from django.utils.translation import gettext_lazy as _


# below class inhirite the ClearFieldInput, see in between parenteses
# https://github.com/django/django/blob/main/django/forms/widgets.py
class CustomClearableFileInput(ClearableFileInput):
    # overriding the below left site items with our own values right side
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'
