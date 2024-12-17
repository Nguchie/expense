from django import forms
from .models import Expenditure
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm, SetPasswordForm as DjangoSetPasswordForm
from django.contrib.auth.models import User

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['ename', 'eamount', 'edate', 'issued_to']
        labels = {
            'ename': 'Item Name',
            'eamount': 'Amount',
            'edate': 'Date',
            'issued_to': 'Issued To',
        }
        widgets = {
            'ename': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
            'eamount': forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
            'edate': forms.DateInput(attrs={'type': 'date'}),
            'issued_to': forms.TextInput(attrs={'placeholder': 'Enter the name of the person to whom the item was issued.'}),
        }



class CustomPasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(max_length=254, required=True)

class CustomSetPasswordForm(DjangoSetPasswordForm):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)
