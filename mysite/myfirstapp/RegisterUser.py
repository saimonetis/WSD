
from django import forms

class RegisterUser(forms.Form):
	name = forms.CharField(max_length = 64)
	passwd1 = forms.CharField(widget=forms.PasswordInput)
	passwd2 = forms.CharField(widget=forms.PasswordInput)
	mail = forms.CharField(max_length = 256)
