from .models import *
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            k: forms.TextInput(attrs={'class': 'form-control'}) for k in fields
        }
    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['myfield'].widget.attrs.update({'class' : 'myfieldclass'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'gender')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}), 
            'gender': forms.ChoiceField()
        }
        widgets.update({
            k: forms.TextInput(attrs={'class': 'form-control'}) for k in fields[1:]
        })