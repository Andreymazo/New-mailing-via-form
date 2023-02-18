from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm

from mailing.models import Client, Mssg, Emails

from django import forms


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-control datepicker'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''

class SigninForm(StyleFormMixin, AuthenticationForm):
    pass
class SignupForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = Client
        fields = ("email",)
        field_classes = {"username": UsernameField}
#
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
#
class MssgForm(forms.ModelForm):
    class Meta:
        model = Mssg
        fields = '__all__'
class EmailsForm(forms.ModelForm):
    class Meta:
        model = Emails
        fields = '__all__'